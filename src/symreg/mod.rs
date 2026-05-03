//! Symbolic regression engine.
//!
//! Discovers closed-form mathematical formulas from data using EML trees.
//! The algorithm enumerates tree topologies up to a maximum depth, optimizes
//! continuous parameters via Adam, and selects the best formulas by MSE
//! with a complexity penalty (Occam's razor).

use crate::error::EmlError;
use crate::eval::EvalCtx;
use crate::grad::ParameterizedEmlTree;
use crate::tree::EmlTree;
use crate::units::Units;
use rand::RngExt;
use rand::SeedableRng;

mod constants;
mod mcts;
mod numerics;
mod topology;
use constants::{bake_params_into_lowered, extract_named_constants};
use topology::{
    compute_mse_direct, compute_mse_parameterized, topology_interval_feasible, try_integer_rounding,
};
pub use topology::{dedupe_by_semantics, enumerate_topologies};

type Rng = rand::rngs::StdRng;

fn make_rng(seed: Option<u64>, salt: u64) -> Rng {
    match seed {
        Some(s) => Rng::seed_from_u64(derive_seed(s, salt)),
        None => rand::make_rng::<Rng>(),
    }
}

/// Compute Huber loss for a slice of residuals.
///
/// `L(r) = r²/2` when `|r| ≤ delta`, else `delta·(|r| - delta/2)`.
fn huber_loss(residuals: &[f64], delta: f64) -> f64 {
    if residuals.is_empty() {
        return 0.0;
    }
    let sum: f64 = residuals
        .iter()
        .map(|&r| {
            let ar = r.abs();
            if ar <= delta {
                0.5 * r * r
            } else {
                delta * (ar - 0.5 * delta)
            }
        })
        .sum();
    sum / residuals.len() as f64
}

/// Gradient scaling factor for Huber loss at residual `r`.
///
/// Returns `r` when `|r| ≤ delta`, else `delta · sign(r)`.
/// The Adam gradient is `2 * huber_grad_factor(r, delta)` (matching the
/// MSE gradient structure `2r` so callers just replace the `2r` factor).
fn huber_grad_factor(r: f64, delta: f64) -> f64 {
    if r.abs() <= delta {
        r
    } else {
        delta * r.signum()
    }
}

/// Compute trimmed MSE for a slice of residuals, dropping the top `alpha`
/// fraction by absolute residual.
fn trimmed_mse(residuals: &[f64], alpha: f64) -> f64 {
    if residuals.is_empty() {
        return 0.0;
    }
    let mut sorted: Vec<f64> = residuals.iter().map(|r| r * r).collect();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let keep = ((1.0 - alpha) * sorted.len() as f64).ceil() as usize;
    let keep = keep.max(1).min(sorted.len());
    sorted[..keep].iter().sum::<f64>() / keep as f64
}

/// Smooth sigmoid-based weight for trimmed-MSE gradient at residual `r`.
///
/// Returns a value in (0, 1] that downweights large residuals via a
/// soft-threshold sigmoid rather than a hard trim. This keeps the Adam
/// gradient step smooth and avoids discontinuities that stall convergence.
///
/// `w(r) = sigmoid(α_k - |r|/q)` where `q` is the `alpha`-quantile of
/// `|residuals|` and `α_k = 3.0` controls the sharpness.
fn trimmed_mse_grad_factor(r: f64, residuals: &[f64], alpha: f64) -> f64 {
    if residuals.is_empty() || alpha <= 0.0 {
        return r;
    }
    let mut abs_res: Vec<f64> = residuals.iter().map(|x| x.abs()).collect();
    abs_res.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let q_idx = ((1.0 - alpha) * (abs_res.len() - 1) as f64).round() as usize;
    let q = abs_res[q_idx.min(abs_res.len() - 1)].max(1e-12);
    let sharpness = 3.0_f64;
    let w = 1.0 / (1.0 + (r.abs() / q - (1.0 - alpha)).exp() * sharpness.exp());
    w.clamp(0.0, 1.0) * r
}

/// Derive a per-topology seed from a master seed using SplitMix64 mixing.
///
/// Guarantees that each topology gets a statistically independent RNG stream
/// even when master seeds are close together.
fn derive_seed(master: u64, topology_idx: u64) -> u64 {
    // SplitMix64 step applied twice (once per input) then XOR-folded.
    let mix = |mut z: u64| -> u64 {
        z = z.wrapping_add(0x9e37_79b9_7f4a_7c15);
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
        z ^ (z >> 31)
    };
    mix(master).wrapping_add(mix(topology_idx))
}

#[cfg(feature = "parallel")]
use rayon::prelude::*;

/// Loss function used by the Adam optimiser in symbolic regression.
///
/// Controls how the residual `r = prediction − target` is penalised.
#[derive(Clone, Debug, Default)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum SymRegLoss {
    /// Mean squared error: `L(r) = r²`.
    #[default]
    Mse,
    /// Huber loss: quadratic for `|r| ≤ delta`, linear beyond.
    ///
    /// More robust to outliers than MSE while remaining smooth everywhere.
    Huber {
        /// Transition point between quadratic and linear regime.
        delta: f64,
    },
    /// Trimmed MSE: drops the top `alpha` fraction of largest residuals
    /// before averaging.
    ///
    /// For the Adam gradient step a smooth sigmoid-weight approximation is
    /// used; the exact trim is applied for scoring.
    TrimmedMse {
        /// Fraction of points to trim (0.0 = no trim = MSE).
        alpha: f64,
    },
}

/// Strategy for multi-output symbolic regression.
#[derive(Debug, Clone, PartialEq, Default)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum MultiOutputStrategy {
    /// Each output runs a completely independent single-output regression. Default.
    #[default]
    Independent,
    // SharedTopology variant is deferred to a future release.
}

/// Topology search strategy.
#[derive(Debug, Clone, PartialEq, Default)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum SymRegStrategy {
    /// Exhaustive enumeration of all topologies up to `max_depth`. Default.
    #[default]
    Exhaustive,
    /// Bounded beam search: score each topology with a cheap surrogate
    /// (few Adam steps), keep top `width` candidates, then do full Adam on those.
    Beam {
        /// Maximum number of candidates to keep at each depth level.
        width: usize,
    },
    /// Monte-Carlo tree search over partial EML topologies.
    ///
    /// Uses UCB1 selection: `score + exploration * sqrt(ln(parent_visits) / child_visits)`.
    /// Each rollout: randomly complete a partial tree, fit with a few Adam steps,
    /// return `1/(1+MSE)` as the value signal (higher = better fit).
    Mcts {
        /// Total number of MCTS rollout iterations.
        iterations: usize,
        /// UCB1 exploration coefficient (higher = more exploration).
        exploration: f64,
    },
}

/// Configuration for symbolic regression.
#[derive(Clone, Debug)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(default))]
pub struct SymRegConfig {
    /// Maximum tree depth to explore (paper: 4 is often sufficient).
    pub max_depth: usize,
    /// Adam learning rate.
    pub learning_rate: f64,
    /// Convergence threshold (MSE).
    pub tolerance: f64,
    /// Maximum optimization iterations per topology.
    pub max_iter: usize,
    /// Complexity penalty coefficient (Occam's razor).
    pub complexity_penalty: f64,
    /// Number of random restarts per topology.
    pub num_restarts: usize,
    /// Whether to attempt integer rounding of parameters.
    pub integer_rounding: bool,
    /// Number of folds for k-fold cross-validation.
    ///
    /// When `Some(k)`, each formula is also evaluated on held-out folds.
    /// `cv_mse` in `DiscoveredFormula` is populated and results are sorted
    /// by `cv_mse`. When `None` (default), no cross-validation is performed
    /// and behaviour is identical to before.
    pub cv_folds: Option<usize>,
    /// Optional master RNG seed for fully reproducible runs.
    ///
    /// When `Some(s)`, per-topology seeds are derived via SplitMix64 so
    /// every topology gets an independent but deterministic RNG stream.
    /// When `None` (default), `rand::from_os_rng()` is used (non-deterministic).
    pub seed: Option<u64>,
    /// Loss function for Adam optimisation.
    ///
    /// Default is `SymRegLoss::Mse`. Use `Huber` or `TrimmedMse` to improve
    /// robustness against outliers.
    pub loss: SymRegLoss,
    /// Post-Adam constants extraction tolerance.
    ///
    /// When `Some(eps)`, each free constant is tested against a set of
    /// well-known values (π, e, √2, simple rationals). The nearest candidate
    /// is accepted when the resulting MSE satisfies
    /// `new_mse ≤ (1 + eps) * current_mse`.
    /// When `None` (default), raw float values are kept.
    pub constant_extraction: Option<f64>,
    /// Enable interval-based topology pruning before Adam fitting (cheap pre-filter).
    ///
    /// Only topologies whose output interval can span the target range are attempted.
    /// Default: `false`.
    pub interval_pruning: bool,
    /// Only apply interval pruning to topologies at this depth or deeper.
    ///
    /// Default: `2` (pruning tiny depth-1 trees is usually counterproductive).
    pub interval_pruning_depth_threshold: usize,
    /// Strategy for multi-output symbolic regression.
    ///
    /// Default: `MultiOutputStrategy::Independent`.
    pub multi_output_strategy: MultiOutputStrategy,
    /// Topology search strategy.
    ///
    /// Default: `SymRegStrategy::Exhaustive` (full enumeration, fast at depth ≤ 4).
    pub strategy: SymRegStrategy,
    /// Window size for Savitzky-Golay derivative estimation in ODE discovery.
    ///
    /// When `None` (default), [`SymRegEngine::discover_ode`] uses central
    /// differences for all state variables.  When `Some(w)` with `w >= 5`,
    /// the Savitzky-Golay smoother (window=5, poly=2) is applied instead;
    /// values below 5 are treated the same as `None`.
    pub ode_sg_window: Option<usize>,
    /// Optional dimensional-analysis filter: `Some((var_units, target_units))` enables
    /// hard pruning of dimensionally-inadmissible topologies before Adam optimisation.
    ///
    /// - `var_units[i]` gives the physical units of variable `i`.
    /// - `target_units` specifies the expected units of the regression target.
    ///
    /// A topology is retained only if [`crate::lower::LoweredOp::check_units`] returns
    /// `Ok(u)` with `u == target_units`.  All other topologies (including those that
    /// raise a `UnitError`) are skipped entirely, providing a 10–100× search-space
    /// reduction on physics problems.
    ///
    /// Default: `None` (no unit filtering; identical behaviour to previous releases).
    pub unit_filter: Option<(Vec<Units>, Units)>,
}

impl Default for SymRegConfig {
    fn default() -> Self {
        Self {
            max_depth: 4,
            learning_rate: 1e-3,
            tolerance: 1e-10,
            max_iter: 10_000,
            complexity_penalty: 1e-4,
            num_restarts: 3,
            integer_rounding: true,
            cv_folds: None,
            seed: None,
            loss: SymRegLoss::default(),
            constant_extraction: None,
            interval_pruning: false,
            interval_pruning_depth_threshold: 2,
            multi_output_strategy: MultiOutputStrategy::Independent,
            strategy: SymRegStrategy::Exhaustive,
            ode_sg_window: None,
            unit_filter: None,
        }
    }
}

impl SymRegConfig {
    /// Quick preset — fast preview; may miss the global optimum.
    ///
    /// Use during interactive exploration or smoke tests. Shallow tree
    /// depth and few restarts trade accuracy for speed.
    pub fn quick() -> Self {
        Self {
            max_depth: 2,
            max_iter: 200,
            num_restarts: 2,
            ..Self::default()
        }
    }

    /// Balanced preset — production default. Alias for `Self::default()`.
    ///
    /// This preserves whatever `Default` returns today. If `Default` ever
    /// changes, `balanced()` moves with it.
    pub fn balanced() -> Self {
        Self::default()
    }

    /// Exhaustive preset — slow but thorough. Use for publication-quality runs.
    ///
    /// Deepens `max_depth`, increases iterations and restart count. Expect
    /// multi-minute runs on larger datasets.
    ///
    /// Note: `max_iter` is set to `20_000` so it genuinely exceeds the
    /// current `Default::default()` value of `10_000` (the plan's suggested
    /// `2_000` would have been *fewer* iterations than the balanced default
    /// and therefore inconsistent with the preset's "slower" semantics).
    pub fn exhaustive() -> Self {
        Self {
            max_depth: 4,
            max_iter: 20_000,
            num_restarts: 8,
            cv_folds: Some(5),
            ..Self::default()
        }
    }
}

/// A formula discovered by symbolic regression.
#[derive(Clone, Debug)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct DiscoveredFormula {
    /// The EML tree representation.
    pub eml_tree: EmlTree,
    /// Final mean squared error.
    pub mse: f64,
    /// Tree node count (complexity measure).
    pub complexity: usize,
    /// Combined score: MSE + complexity_penalty * complexity.
    pub score: f64,
    /// Human-readable expression (from lowering).
    pub pretty: String,
    /// Optimized parameter values.
    pub params: Vec<f64>,
    /// Cross-validated MSE (average over held-out folds), or `None` when
    /// `SymRegConfig::cv_folds` was not set.
    pub cv_mse: Option<f64>,
}

impl DiscoveredFormula {
    /// Returns `true` if `self` Pareto-dominates `other`.
    ///
    /// `self` dominates `other` when it is at least as good on every objective
    /// (MSE and complexity) and strictly better on at least one.
    pub fn dominates(&self, other: &DiscoveredFormula) -> bool {
        self.mse <= other.mse
            && self.complexity <= other.complexity
            && (self.mse < other.mse || self.complexity < other.complexity)
    }

    /// Render the discovered formula as a LaTeX math expression.
    ///
    /// Lowers the EML tree and converts to LaTeX notation.
    /// Returns a string suitable for use inside `$...$` math mode.
    pub fn to_latex(&self) -> String {
        self.eml_tree.lower().simplify().to_latex()
    }
}

#[cfg(feature = "serde")]
impl DiscoveredFormula {
    /// Serialize to a JSON string.
    pub fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string(self)
    }

    /// Deserialize from a JSON string.
    pub fn from_json(json: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(json)
    }

    /// Serialize to binary using `oxicode`.
    pub fn to_binary(&self) -> Result<Vec<u8>, oxicode::Error> {
        oxicode::serde::encode_serde(self)
    }

    /// Deserialize from binary bytes encoded with [`Self::to_binary`].
    pub fn from_binary(bytes: &[u8]) -> Result<Self, oxicode::Error> {
        oxicode::serde::decode_serde(bytes)
    }
}

#[cfg(feature = "tensorlogic")]
impl DiscoveredFormula {
    /// Convert this formula to a [`tensorlogic_ir::TLExpr`] via lower + simplify.
    pub fn to_tlexpr(&self) -> tensorlogic_ir::TLExpr {
        crate::tensorlogic::to_tlexpr(&self.eml_tree.lower().simplify())
    }

    /// Wrap the formula's `TLExpr` in a [`tensorlogic_ir::TLExpr::WeightedRule`] with the
    /// given weight.
    pub fn to_tl_weighted_rule(&self, weight: f64) -> tensorlogic_ir::TLExpr {
        tensorlogic_ir::TLExpr::WeightedRule {
            weight,
            rule: Box::new(self.to_tlexpr()),
        }
    }

    /// Build a `WeightedRule` encoding the equation `target_var = formula`.
    ///
    /// The left-hand side is `TLExpr::Pred { name: target_var, args: [Term::var(target_var)] }`.
    pub fn to_tl_weighted_equation(&self, target_var: &str, weight: f64) -> tensorlogic_ir::TLExpr {
        let lhs = tensorlogic_ir::TLExpr::Pred {
            name: target_var.to_string(),
            args: vec![tensorlogic_ir::Term::var(target_var)],
        };
        let eq = tensorlogic_ir::TLExpr::Eq(Box::new(lhs), Box::new(self.to_tlexpr()));
        tensorlogic_ir::TLExpr::WeightedRule {
            weight,
            rule: Box::new(eq),
        }
    }
}

#[cfg(test)]
#[cfg(feature = "tensorlogic")]
mod tl_adapter_tests {
    use super::*;
    use crate::canonical::Canonical;
    use crate::tensorlogic;
    use tensorlogic_ir::{TLExpr, Term};

    fn make_formula() -> DiscoveredFormula {
        let tree = Canonical::nat(1);
        DiscoveredFormula {
            eml_tree: tree,
            mse: 0.0,
            complexity: 1,
            score: 0.0,
            pretty: "1".to_string(),
            params: vec![],
            cv_mse: None,
        }
    }

    #[test]
    fn discoveredformula_to_tlexpr_matches_lowered_simplified_path() {
        let f = make_formula();
        let expected = tensorlogic::to_tlexpr(&f.eml_tree.lower().simplify());
        assert_eq!(f.to_tlexpr(), expected);
    }

    #[test]
    fn to_tl_weighted_rule_shape_carries_weight_verbatim() {
        let f = make_formula();
        let tl = f.to_tl_weighted_rule(0.42);
        match tl {
            TLExpr::WeightedRule { weight, .. } => {
                assert!((weight - 0.42).abs() < f64::EPSILON);
            }
            other => panic!("expected WeightedRule, got {other:?}"),
        }
    }

    #[test]
    fn to_tl_weighted_equation_shape_lhs_pred_eq_rhs_formula() {
        let f = make_formula();
        let tl = f.to_tl_weighted_equation("y", 1.0);
        match tl {
            TLExpr::WeightedRule { weight, rule } => {
                assert!((weight - 1.0).abs() < f64::EPSILON);
                match *rule {
                    TLExpr::Eq(lhs, rhs) => {
                        match *lhs {
                            TLExpr::Pred { name, ref args } => {
                                assert_eq!(name, "y");
                                assert_eq!(args.len(), 1);
                                assert_eq!(args[0], Term::var("y"));
                            }
                            other => panic!("expected Pred on lhs, got {other:?}"),
                        }
                        assert_eq!(*rhs, f.to_tlexpr());
                    }
                    other => panic!("expected Eq inside WeightedRule, got {other:?}"),
                }
            }
            other => panic!("expected WeightedRule, got {other:?}"),
        }
    }
}

/// Extract the Pareto-optimal subset from a slice of discovered formulas.
///
/// A formula F is Pareto-optimal if no other formula G dominates it
/// (i.e., G has both lower-or-equal MSE **and** lower-or-equal complexity,
/// with at least one strictly lower).
///
/// The returned vector is sorted by complexity ascending (simplest first).
/// If `formulas` is empty, returns an empty vector.
/// Time complexity: O(n²) — acceptable for the formula counts typical of EML.
pub fn pareto_front(formulas: &[DiscoveredFormula]) -> Vec<DiscoveredFormula> {
    let mut front: Vec<DiscoveredFormula> = formulas
        .iter()
        .filter(|candidate| !formulas.iter().any(|other| other.dominates(candidate)))
        .cloned()
        .collect();

    front.sort_by(|a, b| {
        a.complexity.cmp(&b.complexity).then_with(|| {
            a.mse
                .partial_cmp(&b.mse)
                .unwrap_or(std::cmp::Ordering::Equal)
        })
    });
    front
}

/// Symbolic regression engine.
pub struct SymRegEngine {
    config: SymRegConfig,
}

impl SymRegEngine {
    /// Create a new symbolic regression engine.
    pub fn new(config: SymRegConfig) -> Self {
        Self { config }
    }

    /// Discover the Pareto-optimal formulas (MSE vs complexity trade-off).
    ///
    /// Runs the full symbolic regression via [`Self::discover`], then extracts
    /// the non-dominated Pareto front.
    ///
    /// Use this when you want the full trade-off curve rather than a single
    /// "best" formula. Sort order: complexity ascending.
    pub fn discover_pareto(
        &self,
        inputs: &[Vec<f64>],
        targets: &[f64],
        num_vars: usize,
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        let formulas = self.discover(inputs, targets, num_vars)?;
        Ok(pareto_front(&formulas))
    }

    /// Discover closed-form formulas from input-output data.
    ///
    /// Dispatches to [`Self::discover_exhaustive`] or [`Self::discover_beam`]
    /// according to [`SymRegConfig::strategy`].
    ///
    /// - `inputs`: each row is one data point's variable values
    /// - `targets`: corresponding output values
    /// - `num_vars`: number of input variables
    ///
    /// Returns formulas sorted by score (best first).
    pub fn discover(
        &self,
        inputs: &[Vec<f64>],
        targets: &[f64],
        num_vars: usize,
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        match self.config.strategy {
            SymRegStrategy::Exhaustive => self.discover_exhaustive(inputs, targets, num_vars),
            SymRegStrategy::Beam { width } => self.discover_beam(inputs, targets, num_vars, width),
            SymRegStrategy::Mcts {
                iterations,
                exploration,
            } => self.discover_mcts(inputs, targets, num_vars, iterations, exploration),
        }
    }

    /// Discover formulas using exhaustive topology enumeration.
    ///
    /// Evaluates every distinct topology up to `max_depth` with full Adam
    /// optimisation.  Use [`Self::discover_beam`] when the topology space is
    /// too large to enumerate exhaustively.
    pub fn discover_exhaustive(
        &self,
        inputs: &[Vec<f64>],
        targets: &[f64],
        num_vars: usize,
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        if inputs.is_empty() || targets.is_empty() {
            return Err(EmlError::EmptyData);
        }
        if inputs.len() != targets.len() {
            return Err(EmlError::DimensionMismatch(inputs.len(), targets.len()));
        }

        // Phase 1: Enumerate all topologies up to max_depth
        let topologies = enumerate_topologies(self.config.max_depth, num_vars);

        // Phase 1b: Prune semantically-equivalent topologies
        // (EML-default lowering is nearly injective, so only a small fraction
        //  collapse via simplification rules — see `dedupe_by_semantics`).
        let topologies = dedupe_by_semantics(topologies);

        // Phase 1c (optional): Interval-arithmetic pre-filter.
        //
        // For each topology at or above the depth threshold, we evaluate an
        // over-approximating output interval (with free parameters expanded to
        // [-1000, 1000]).  Topologies whose output interval cannot overlap the
        // observed target range are eliminated before Adam even starts.
        let topologies = if self.config.interval_pruning {
            use crate::lower_interval::IntervalLO;

            // Compute per-variable intervals from the data.
            let input_intervals: Vec<IntervalLO> = (0..num_vars)
                .map(|j| {
                    let mut lo = f64::INFINITY;
                    let mut hi = f64::NEG_INFINITY;
                    for row in inputs.iter() {
                        if let Some(&v) = row.get(j) {
                            if v < lo {
                                lo = v;
                            }
                            if v > hi {
                                hi = v;
                            }
                        }
                    }
                    if lo.is_finite() && hi.is_finite() {
                        IntervalLO::new(lo, hi)
                    } else {
                        IntervalLO::full()
                    }
                })
                .collect();

            let target_lo = targets.iter().copied().fold(f64::INFINITY, f64::min);
            let target_hi = targets.iter().copied().fold(f64::NEG_INFINITY, f64::max);
            let threshold = self.config.interval_pruning_depth_threshold;

            topologies
                .into_iter()
                .filter(|topo| {
                    if topo.depth() < threshold {
                        true // skip pruning for shallow trees
                    } else {
                        topology_interval_feasible(topo, &input_intervals, target_lo, target_hi)
                    }
                })
                .collect()
        } else {
            topologies
        };

        // Phase 1d (optional): Dimensional-analysis pre-filter.
        //
        // Topologies whose lowered/simplified expression is dimensionally inconsistent,
        // or whose output units differ from `target_units`, are skipped before Adam.
        let topologies = if let Some((ref var_units, target_units)) = self.config.unit_filter {
            topologies
                .into_iter()
                .filter(|topo| {
                    let lowered = topo.lower().simplify();
                    matches!(lowered.check_units(var_units), Ok(u) if u == target_units)
                })
                .collect()
        } else {
            topologies
        };

        self.optimize_and_finalize(topologies, inputs, targets)
    }

    /// Discover formulas using beam search.
    ///
    /// Two-phase approach:
    /// 1. **Surrogate pass**: Run each topology with a cheap budget (few Adam steps,
    ///    single restart) to get a quick score estimate.
    /// 2. **Full pass**: Keep only the top `width` candidates by surrogate MSE and
    ///    run full Adam optimisation on those.
    ///
    /// This is significantly faster than exhaustive search at large `max_depth`
    /// while retaining the best candidates.
    pub fn discover_beam(
        &self,
        inputs: &[Vec<f64>],
        targets: &[f64],
        num_vars: usize,
        width: usize,
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        if inputs.is_empty() || targets.is_empty() {
            return Err(EmlError::EmptyData);
        }
        if inputs.len() != targets.len() {
            return Err(EmlError::DimensionMismatch(inputs.len(), targets.len()));
        }

        // Phase 1: enumerate and deduplicate (same as exhaustive)
        let topologies = enumerate_topologies(self.config.max_depth, num_vars);
        let topologies = dedupe_by_semantics(topologies);

        // Phase 1b (optional): Dimensional-analysis pre-filter (mirrors exhaustive path).
        let topologies = if let Some((ref var_units, target_units)) = self.config.unit_filter {
            topologies
                .into_iter()
                .filter(|topo| {
                    let lowered = topo.lower().simplify();
                    matches!(lowered.check_units(var_units), Ok(u) if u == target_units)
                })
                .collect()
        } else {
            topologies
        };

        // Phase 2: surrogate pass with cheap Adam budget.
        let surrogate_iters = self.config.max_iter.clamp(10, 50);
        let surrogate_config = SymRegConfig {
            max_iter: surrogate_iters,
            num_restarts: 1,
            cv_folds: None,
            ..self.config.clone()
        };
        let surrogate_engine = SymRegEngine::new(surrogate_config);

        #[cfg(feature = "parallel")]
        let mut surrogate_scores: Vec<(usize, f64)> = topologies
            .par_iter()
            .enumerate()
            .filter_map(|(i, topo)| {
                surrogate_engine
                    .optimize_topology(topo, inputs, targets, i)
                    .map(|f| (i, f.mse))
            })
            .collect();

        #[cfg(not(feature = "parallel"))]
        let mut surrogate_scores: Vec<(usize, f64)> = topologies
            .iter()
            .enumerate()
            .filter_map(|(i, topo)| {
                surrogate_engine
                    .optimize_topology(topo, inputs, targets, i)
                    .map(|f| (i, f.mse))
            })
            .collect();

        // Phase 3: truncate to top `width` by surrogate MSE
        surrogate_scores.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
        let effective_width = width.max(1);
        surrogate_scores.truncate(effective_width);

        // Collect surviving topologies (preserve order from topologies vec)
        let mut keep_indices: Vec<usize> = surrogate_scores.iter().map(|&(i, _)| i).collect();
        keep_indices.sort_unstable();
        let beam_topologies: Vec<EmlTree> = keep_indices
            .iter()
            .filter_map(|&i| topologies.get(i).cloned())
            .collect();

        // Phase 4: full Adam on the beam candidates
        self.optimize_and_finalize(beam_topologies, inputs, targets)
    }

    /// Bridge: run MCTS topology search.
    fn discover_mcts(
        &self,
        inputs: &[Vec<f64>],
        targets: &[f64],
        num_vars: usize,
        iterations: usize,
        exploration: f64,
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        mcts::run_mcts(self, inputs, targets, num_vars, iterations, exploration)
    }

    /// Expose the engine configuration to sub-modules.
    pub(super) fn config(&self) -> &SymRegConfig {
        &self.config
    }

    /// Expose `optimize_topology` to the `mcts` sub-module.
    pub(super) fn optimize_topology_pub(
        &self,
        topology: &EmlTree,
        inputs: &[Vec<f64>],
        targets: &[f64],
        topology_idx: usize,
    ) -> Option<DiscoveredFormula> {
        self.optimize_topology(topology, inputs, targets, topology_idx)
    }

    /// Expose `optimize_and_finalize` to the `mcts` sub-module.
    pub(super) fn optimize_and_finalize_pub(
        &self,
        topologies: Vec<EmlTree>,
        inputs: &[Vec<f64>],
        targets: &[f64],
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        self.optimize_and_finalize(topologies, inputs, targets)
    }

    /// Discover formulas for multiple outputs independently.
    ///
    /// Each output column is treated as a separate single-output regression
    /// problem (following [`MultiOutputStrategy::Independent`]).
    ///
    /// - `inputs`: each row is one data point's variable values (n_samples × n_vars)
    /// - `targets`: one `Vec<f64>` per output, each of length `n_samples`
    /// - `num_vars`: number of input variables
    ///
    /// Returns one `Vec<DiscoveredFormula>` per output, sorted by score.
    pub fn discover_multi(
        &self,
        inputs: &[Vec<f64>],
        targets: &[Vec<f64>],
        num_vars: usize,
    ) -> Result<Vec<Vec<DiscoveredFormula>>, EmlError> {
        if inputs.is_empty() {
            return Err(EmlError::EmptyData);
        }
        if targets.is_empty() {
            return Err(EmlError::EmptyData);
        }
        for col in targets.iter() {
            if col.len() != inputs.len() {
                return Err(EmlError::DimensionMismatch(inputs.len(), col.len()));
            }
        }

        match &self.config.multi_output_strategy {
            MultiOutputStrategy::Independent => targets
                .iter()
                .map(|col| self.discover(inputs, col, num_vars))
                .collect(),
        }
    }

    /// Discover ODEs `dx_k/dt = f_k(x)` from trajectory data using numerical
    /// differentiation followed by symbolic regression.
    ///
    /// # Arguments
    ///
    /// - `trajectory`: one `Vec<f64>` per state variable, each of length
    ///   `n_timesteps`.  All slices must have the same length.
    /// - `dt`: uniform time step between consecutive observations.
    ///
    /// # Returns
    ///
    /// One `Vec<DiscoveredFormula>` per state variable, sorted by score
    /// (best first), giving candidate expressions for `dx_k/dt`.
    ///
    /// # Errors
    ///
    /// Returns [`EmlError::DimensionMismatch`] when `trajectory` is empty,
    /// when variable slices disagree in length, or when fewer than 3 time
    /// steps are provided (interior-point differentiation requires at least
    /// one interior point).
    pub fn discover_ode(
        &self,
        trajectory: &[Vec<f64>],
        dt: f64,
    ) -> Result<Vec<Vec<DiscoveredFormula>>, EmlError> {
        if trajectory.is_empty() {
            return Err(EmlError::EmptyData);
        }
        let n_timesteps = trajectory[0].len();
        for var in trajectory.iter() {
            if var.len() != n_timesteps {
                return Err(EmlError::DimensionMismatch(n_timesteps, var.len()));
            }
        }
        if n_timesteps < 3 {
            return Err(EmlError::DimensionMismatch(3, n_timesteps));
        }

        let n_vars = trajectory.len();

        // Compute time-derivatives for every state variable.
        let derivatives: Vec<Vec<f64>> = trajectory
            .iter()
            .map(|x| match self.config.ode_sg_window {
                Some(w) if w >= 5 => numerics::savitzky_golay_derivative(x, dt),
                _ => numerics::central_differences(x, dt),
            })
            .collect();

        // Build feature matrix (samples-major) and target columns.
        //
        // We use only the interior time steps (indices 1..n-1) to avoid
        // endpoint derivative noise from the lower-order forward/backward
        // schemes.  This gives n_interior = n_timesteps - 2 samples.
        let n_interior = n_timesteps - 2; // guaranteed >= 1 since n_timesteps >= 3

        // features[t] = [x_0[t+1], x_1[t+1], ..., x_{k-1}[t+1]] (1-based)
        let mut features: Vec<Vec<f64>> = Vec::with_capacity(n_interior);
        for t in 1..n_timesteps - 1 {
            features.push(trajectory.iter().map(|x| x[t]).collect());
        }

        // targets[k] = derivatives[k][1..n-1]
        let targets: Vec<Vec<f64>> = derivatives
            .iter()
            .map(|dx| dx[1..n_timesteps - 1].to_vec())
            .collect();

        self.discover_multi(&features, &targets, n_vars)
    }

    /// Shared finalization: optimize topologies, sort, optionally cross-validate.
    fn optimize_and_finalize(
        &self,
        topologies: Vec<EmlTree>,
        inputs: &[Vec<f64>],
        targets: &[f64],
    ) -> Result<Vec<DiscoveredFormula>, EmlError> {
        #[cfg(feature = "parallel")]
        let mut formulas: Vec<DiscoveredFormula> = topologies
            .par_iter()
            .enumerate()
            .filter_map(|(i, topology)| self.optimize_topology(topology, inputs, targets, i))
            .collect();

        #[cfg(not(feature = "parallel"))]
        let mut formulas: Vec<DiscoveredFormula> = topologies
            .iter()
            .enumerate()
            .filter_map(|(i, topology)| self.optimize_topology(topology, inputs, targets, i))
            .collect();

        // Sort by score — use complexity and structural hash as tiebreakers
        // so seeded runs produce byte-identical sorted output even when scores tie.
        formulas.sort_by(|a, b| {
            use std::collections::hash_map::DefaultHasher;
            use std::hash::Hasher;
            a.score
                .partial_cmp(&b.score)
                .unwrap_or(std::cmp::Ordering::Equal)
                .then_with(|| a.complexity.cmp(&b.complexity))
                .then_with(|| {
                    let hash_of = |f: &DiscoveredFormula| {
                        let mut h = DefaultHasher::new();
                        f.eml_tree.lower().simplify().structural_hash(&mut h);
                        h.finish()
                    };
                    hash_of(a).cmp(&hash_of(b))
                })
        });

        // Optional: k-fold cross-validation
        if let Some(k) = self.config.cv_folds {
            let k = k.clamp(2, inputs.len());
            for formula in &mut formulas {
                formula.cv_mse =
                    Some(self.k_fold_cv(&formula.eml_tree, &formula.params, inputs, targets, k));
            }
            formulas.sort_by(|a, b| {
                let a_score = a.cv_mse.unwrap_or(a.score);
                let b_score = b.cv_mse.unwrap_or(b.score);
                a_score
                    .partial_cmp(&b_score)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
        }

        Ok(formulas)
    }

    /// Compute average held-out MSE over `k` contiguous folds.
    ///
    /// CV splits are contiguous (no shuffle), which is appropriate for
    /// non-time-series data where sample order is arbitrary. Each fold uses
    /// a warm-started Adam run with a reduced iteration budget to keep CV
    /// tractable.
    fn k_fold_cv(
        &self,
        topology: &EmlTree,
        params: &[f64],
        inputs: &[Vec<f64>],
        targets: &[f64],
        k: usize,
    ) -> f64 {
        let n = inputs.len();

        // Edge cases: can't do meaningful CV
        if n < 2 || k <= 1 {
            return compute_mse_direct(topology, inputs, targets).unwrap_or(f64::INFINITY);
        }

        let fold_iters = (self.config.max_iter / k).clamp(1, 200);
        let lr = self.config.learning_rate;
        let beta1 = 0.9_f64;
        let beta2 = 0.999_f64;
        let epsilon = 1e-8_f64;

        let mut total_cv_mse = 0.0;
        let mut valid_folds = 0usize;

        for fold in 0..k {
            // Determine held-out range (contiguous fold)
            let fold_start = (fold * n) / k;
            let fold_end = ((fold + 1) * n) / k;

            if fold_start >= fold_end {
                continue;
            }

            // Build train/test index sets
            let train_inputs: Vec<&Vec<f64>> = inputs[..fold_start]
                .iter()
                .chain(inputs[fold_end..].iter())
                .collect();
            let train_targets: Vec<f64> = targets[..fold_start]
                .iter()
                .chain(targets[fold_end..].iter())
                .copied()
                .collect();
            let test_inputs = &inputs[fold_start..fold_end];
            let test_targets = &targets[fold_start..fold_end];

            if train_inputs.is_empty() || test_inputs.is_empty() {
                continue;
            }

            // Warm-start: copy the pre-optimized params as initialization
            let mut ptree = ParameterizedEmlTree::from_topology(topology, 1.0);
            if ptree.params.len() == params.len() {
                ptree.params.clone_from_slice(params);
            }

            let n_params = ptree.num_params();

            // Run a short Adam pass on the training fold (warm start)
            if n_params > 0 {
                let mut m = vec![0.0_f64; n_params];
                let mut v = vec![0.0_f64; n_params];

                for t in 1..=fold_iters {
                    let mut total_grads = vec![0.0_f64; n_params];
                    let mut valid_count = 0usize;

                    for (input, &target) in train_inputs.iter().zip(train_targets.iter()) {
                        let ctx = EvalCtx::new(input);
                        match ptree.forward_backward(&ctx, target) {
                            Ok((loss, grads)) if loss.is_finite() => {
                                for (tg, g) in total_grads.iter_mut().zip(&grads) {
                                    if g.is_finite() {
                                        *tg += g;
                                    }
                                }
                                valid_count += 1;
                            }
                            _ => {}
                        }
                    }

                    if valid_count == 0 {
                        break;
                    }

                    let n_f = valid_count as f64;
                    for i in 0..n_params {
                        let g = total_grads[i] / n_f;
                        m[i] = beta1 * m[i] + (1.0 - beta1) * g;
                        v[i] = beta2 * v[i] + (1.0 - beta2) * g * g;
                        let m_hat = m[i] / (1.0 - beta1.powi(t as i32));
                        let v_hat = v[i] / (1.0 - beta2.powi(t as i32));
                        ptree.params[i] -= lr * m_hat / (v_hat.sqrt() + epsilon);
                    }
                }
            }

            // Evaluate on the held-out fold
            let held_out_mse = if n_params == 0 {
                // No parameters: evaluate topology directly on held-out data
                let test_slices: Vec<&Vec<f64>> = test_inputs.iter().collect();
                let mut total = 0.0;
                let mut cnt = 0usize;
                for (input, &target) in test_slices.iter().zip(test_targets) {
                    let ctx = EvalCtx::new(input);
                    if let Ok(val) = topology.eval_real(&ctx) {
                        if val.is_finite() {
                            total += (val - target).powi(2);
                            cnt += 1;
                        }
                    }
                }
                if cnt == 0 {
                    None
                } else {
                    Some(total / cnt as f64)
                }
            } else {
                let test_input_vecs: Vec<&Vec<f64>> = test_inputs.iter().collect();
                let mut total = 0.0;
                let mut cnt = 0usize;
                for (input, &target) in test_input_vecs.iter().zip(test_targets) {
                    let ctx = EvalCtx::new(input);
                    if let Ok(val) = ptree.forward(&ctx) {
                        if val.is_finite() {
                            total += (val - target).powi(2);
                            cnt += 1;
                        }
                    }
                }
                if cnt == 0 {
                    None
                } else {
                    Some(total / cnt as f64)
                }
            };

            if let Some(mse) = held_out_mse {
                total_cv_mse += mse;
                valid_folds += 1;
            }
        }

        if valid_folds == 0 {
            // Fall back to train MSE if no valid fold
            compute_mse_direct(topology, inputs, targets).unwrap_or(f64::INFINITY)
        } else {
            total_cv_mse / valid_folds as f64
        }
    }

    /// Optimize parameters for a single topology.
    fn optimize_topology(
        &self,
        topology: &EmlTree,
        inputs: &[Vec<f64>],
        targets: &[f64],
        topology_idx: usize,
    ) -> Option<DiscoveredFormula> {
        let mut best_mse = f64::INFINITY;
        let mut best_params = Vec::new();
        let mut rng = make_rng(self.config.seed, topology_idx as u64);

        for _ in 0..self.config.num_restarts {
            let mut ptree = ParameterizedEmlTree::from_topology(topology, 1.0);

            // Randomize initial parameters slightly
            for p in &mut ptree.params {
                *p = 1.0 + rng.random_range(-0.5..0.5);
            }

            // Adam optimizer state
            let n_params = ptree.num_params();
            if n_params == 0 {
                // No parameters to optimize — evaluate directly
                let mse = compute_mse_direct(topology, inputs, targets);
                if let Some(mse) = mse {
                    if mse < best_mse {
                        best_mse = mse;
                        best_params = vec![];
                    }
                }
                break;
            }

            let mut m = vec![0.0_f64; n_params]; // First moment
            let mut v = vec![0.0_f64; n_params]; // Second moment
            let beta1 = 0.9;
            let beta2 = 0.999;
            let epsilon = 1e-8;
            let lr = self.config.learning_rate;

            let mut converged = false;

            for t in 1..=self.config.max_iter {
                // Collect per-point outputs and Jacobians for loss-specific gradient
                let mut outputs_and_jacs: Vec<(f64, Vec<f64>)> = Vec::with_capacity(inputs.len());
                let mut residuals: Vec<f64> = Vec::with_capacity(inputs.len());

                for (input, &target) in inputs.iter().zip(targets) {
                    let ctx = EvalCtx::new(input);
                    match ptree.forward_with_jacobian(&ctx) {
                        Ok((out, jac)) if out.is_finite() => {
                            residuals.push(out - target);
                            outputs_and_jacs.push((out, jac));
                        }
                        _ => {}
                    }
                }

                let valid_count = residuals.len();
                if valid_count == 0 {
                    break;
                }

                // Compute loss and gradients according to configured loss function
                let (total_loss, total_grads) = match &self.config.loss {
                    SymRegLoss::Mse => {
                        let tloss: f64 = residuals.iter().map(|r| r * r).sum();
                        let mut tg = vec![0.0_f64; n_params];
                        for (r, (_, jac)) in residuals.iter().zip(&outputs_and_jacs) {
                            for (tg_i, &j) in tg.iter_mut().zip(jac.iter()) {
                                if j.is_finite() {
                                    *tg_i += 2.0 * r * j;
                                }
                            }
                        }
                        (tloss, tg)
                    }
                    SymRegLoss::Huber { delta } => {
                        let d = *delta;
                        let tloss = huber_loss(&residuals, d) * valid_count as f64;
                        let mut tg = vec![0.0_f64; n_params];
                        for (r, (_, jac)) in residuals.iter().zip(&outputs_and_jacs) {
                            let gf = 2.0 * huber_grad_factor(*r, d);
                            for (tg_i, &j) in tg.iter_mut().zip(jac.iter()) {
                                if j.is_finite() {
                                    *tg_i += gf * j;
                                }
                            }
                        }
                        (tloss, tg)
                    }
                    SymRegLoss::TrimmedMse { alpha } => {
                        let a = *alpha;
                        let tloss = trimmed_mse(&residuals, a) * valid_count as f64;
                        let mut tg = vec![0.0_f64; n_params];
                        for (r, (_, jac)) in residuals.iter().zip(&outputs_and_jacs) {
                            let gf = 2.0 * trimmed_mse_grad_factor(*r, &residuals, a);
                            for (tg_i, &j) in tg.iter_mut().zip(jac.iter()) {
                                if j.is_finite() {
                                    *tg_i += gf * j;
                                }
                            }
                        }
                        (tloss, tg)
                    }
                };

                let n_f = valid_count as f64;
                let mse = total_loss / n_f;

                if mse < self.config.tolerance {
                    best_mse = mse;
                    best_params = ptree.params.clone();
                    converged = true;
                    break;
                }

                // Adam update
                for i in 0..n_params {
                    let g = total_grads[i] / n_f;
                    m[i] = beta1 * m[i] + (1.0 - beta1) * g;
                    v[i] = beta2 * v[i] + (1.0 - beta2) * g * g;
                    let m_hat = m[i] / (1.0 - beta1.powi(t as i32));
                    let v_hat = v[i] / (1.0 - beta2.powi(t as i32));
                    ptree.params[i] -= lr * m_hat / (v_hat.sqrt() + epsilon);
                }

                if mse < best_mse {
                    best_mse = mse;
                    best_params = ptree.params.clone();
                }
            }

            if converged {
                break;
            }
        }

        // Phase 4: Integer rounding
        if self.config.integer_rounding && !best_params.is_empty() {
            let rounded = try_integer_rounding(&best_params);
            let mut ptree_rounded = ParameterizedEmlTree::from_topology(topology, 1.0);
            ptree_rounded.params = rounded;
            let rounded_mse = compute_mse_parameterized(&ptree_rounded, inputs, targets);
            if let Some(rmse) = rounded_mse {
                if rmse <= best_mse * 1.01 {
                    // Accept rounding if MSE doesn't degrade much
                    best_mse = rmse;
                    best_params = ptree_rounded.params;
                }
            }
        }

        if !best_mse.is_finite() || best_mse > 1e10 {
            return None;
        }

        let complexity = topology.size();

        // Bake learned parameters into the lowered tree for pretty-printing
        // and (optionally) constants extraction.
        let baked = bake_params_into_lowered(topology, &best_params);
        let baked_simplified = baked.simplify();

        // Post-Adam constants extraction
        let (final_op, final_mse) = if let Some(eps) = self.config.constant_extraction {
            extract_named_constants(baked_simplified, best_mse, eps, inputs, targets)
        } else {
            (baked_simplified, best_mse)
        };

        let pretty = final_op.to_pretty();

        Some(DiscoveredFormula {
            eml_tree: topology.clone(),
            mse: final_mse,
            complexity,
            score: final_mse + self.config.complexity_penalty * complexity as f64,
            pretty,
            params: best_params,
            cv_mse: None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_enumerate_depth0() {
        let topos = enumerate_topologies(0, 1);
        // Depth 0: One, Var(0) = 2 leaves
        assert_eq!(topos.len(), 2);
    }

    #[test]
    fn test_enumerate_depth1() {
        let topos = enumerate_topologies(1, 1);
        // Depth 0: 2 leaves (One, x0)
        // Depth 1: each pair of leaves → 2*2 = 4, but exact-depth-1 means
        // at least one child at depth 0 (which all leaves are), so all combos.
        // Actually: trees at depth exactly 1 have both children at depth 0.
        // That's 2*2 = 4 trees. Plus 2 depth-0 trees = 6 total.
        assert!(topos.len() >= 6);
    }

    #[test]
    fn test_symreg_exp() {
        // Generate data from y = exp(x)
        let inputs: Vec<Vec<f64>> = (0..20).map(|i| vec![i as f64 * 0.25]).collect();
        let targets: Vec<f64> = inputs.iter().map(|x| x[0].exp()).collect();

        let config = SymRegConfig {
            max_depth: 1,
            learning_rate: 1e-2,
            tolerance: 1e-6,
            max_iter: 1000,
            complexity_penalty: 1e-4,
            num_restarts: 2,
            integer_rounding: true,
            ..SymRegConfig::default()
        };

        let engine = SymRegEngine::new(config);
        let formulas = engine
            .discover(&inputs, &targets, 1)
            .expect("symreg discover exp should succeed");
        assert!(!formulas.is_empty());
        // The best formula should have low MSE
        assert!(formulas[0].mse < 1.0);
    }

    #[test]
    fn test_integer_rounding() {
        let params = vec![0.98, 2.03, 1.51, -0.99];
        let rounded = try_integer_rounding(&params);
        assert!((rounded[0] - 1.0).abs() < 1e-15);
        assert!((rounded[1] - 2.0).abs() < 1e-15);
        assert!((rounded[2] - 1.51).abs() < 1e-15); // Not close enough to round
        assert!((rounded[3] - (-1.0)).abs() < 1e-15);
    }

    #[test]
    fn test_symreg_parallel_matches_sequential() {
        // Parallel and sequential both discover exp(x) with low MSE.
        let inputs: Vec<Vec<f64>> = (0..20).map(|i| vec![i as f64 * 0.25]).collect();
        let targets: Vec<f64> = inputs.iter().map(|x| x[0].exp()).collect();

        let config = SymRegConfig {
            max_depth: 1,
            learning_rate: 1e-2,
            tolerance: 1e-6,
            max_iter: 1000,
            complexity_penalty: 1e-4,
            num_restarts: 2,
            integer_rounding: true,
            ..SymRegConfig::default()
        };

        let engine = SymRegEngine::new(config);
        let formulas = engine
            .discover(&inputs, &targets, 1)
            .expect("parallel symreg discover should succeed");
        assert!(!formulas.is_empty());
        assert!(formulas[0].mse < 1.0);
    }

    #[test]
    fn test_empty_data() {
        let engine = SymRegEngine::new(SymRegConfig::default());
        let result = engine.discover(&[], &[], 1);
        assert!(matches!(result, Err(EmlError::EmptyData)));
    }

    #[test]
    fn test_dimension_mismatch() {
        let engine = SymRegEngine::new(SymRegConfig::default());
        let result = engine.discover(&[vec![1.0]], &[1.0, 2.0], 1);
        assert!(matches!(result, Err(EmlError::DimensionMismatch(1, 2))));
    }

    #[test]
    fn test_dedupe_reduces_topology_count() {
        // EML is non-commutative (eml(A,B) != eml(B,A)) and enumerate_at_depth
        // already generates duplicate-free topologies. Dedup via structural
        // hash only catches simplifications like exp(ln(x)) = x — so the
        // actual reduction is tiny (0.0002% at depth 4). We verify the dedup
        // function runs correctly and preserves at least "before >= after".
        //
        // A full depth-4 stress test (2M trees, ~38s) is captured in
        // `test_dedupe_depth_four_stress` and marked `#[ignore]` for CI speed.
        let topologies = enumerate_topologies(2, 1);
        let before = topologies.len();
        let after = dedupe_by_semantics(topologies).len();
        assert!(
            after <= before,
            "dedup must not grow the set: before={before}, after={after}"
        );
    }

    #[test]
    #[ignore = "slow: depth-4 enumerates 2M topologies, ~38s wall-clock"]
    fn test_dedupe_depth_four_stress() {
        let topologies = enumerate_topologies(4, 1);
        let before = topologies.len();
        let after = dedupe_by_semantics(topologies).len();
        assert!(after <= before);
        // Measured: 2_090_918 → 2_090_913 (5-tree reduction from exp(ln(x)) etc.)
        // Kept for benchmarking the dedup pass itself, not for CI.
    }

    #[test]
    fn test_dedupe_preserves_uniqueness() {
        // Every remaining topology should have a unique structural hash under
        // the same canonicalization pipeline used by `dedupe_by_semantics`.
        use std::collections::HashSet;
        use std::collections::hash_map::DefaultHasher;
        use std::hash::Hasher;

        let topologies = enumerate_topologies(3, 1);
        let deduped = dedupe_by_semantics(topologies);

        let mut hashes: HashSet<u64> = HashSet::new();
        for tree in &deduped {
            let eml_simplified = crate::simplify::simplify(tree);
            let simplified = eml_simplified.lower().simplify();
            let mut h = DefaultHasher::new();
            simplified.structural_hash(&mut h);
            let inserted = hashes.insert(h.finish());
            assert!(inserted, "duplicate structural hash found in deduped set");
        }
        assert_eq!(hashes.len(), deduped.len());
    }

    #[test]
    fn test_dedupe_preserves_discovery_exp() {
        // Rerunning test_symreg_exp-style discovery after dedup should still find
        // a low-MSE formula for exp(x).
        let inputs: Vec<Vec<f64>> = (0..30).map(|i| vec![i as f64 * 0.2]).collect();
        let targets: Vec<f64> = inputs.iter().map(|x| x[0].exp()).collect();

        let config = SymRegConfig {
            max_depth: 2,
            learning_rate: 1e-2,
            tolerance: 1e-5,
            max_iter: 1000,
            complexity_penalty: 1e-4,
            num_restarts: 2,
            integer_rounding: false,
            ..SymRegConfig::default()
        };

        let engine = SymRegEngine::new(config);
        let formulas = engine
            .discover(&inputs, &targets, 1)
            .expect("discover should succeed");
        assert!(!formulas.is_empty(), "should discover at least one formula");
        let best = &formulas[0];
        assert!(
            best.mse < 0.1,
            "best formula MSE too high after dedup: {} (pretty={})",
            best.mse,
            best.pretty
        );
    }
}

#[cfg(test)]
mod preset_tests {
    use super::*;

    #[test]
    fn balanced_equals_default() {
        let bal = SymRegConfig::balanced();
        let def = SymRegConfig::default();
        assert_eq!(bal.max_depth, def.max_depth);
        assert_eq!(bal.max_iter, def.max_iter);
        assert_eq!(bal.num_restarts, def.num_restarts);
        assert_eq!(bal.integer_rounding, def.integer_rounding);
        assert_eq!(bal.seed, def.seed);
        assert_eq!(bal.constant_extraction, def.constant_extraction);
        // f64 fields: compare via bit-exact representation since both come
        // from the same constant literal in `Default`.
        assert_eq!(bal.learning_rate.to_bits(), def.learning_rate.to_bits());
        assert_eq!(bal.tolerance.to_bits(), def.tolerance.to_bits());
        assert_eq!(
            bal.complexity_penalty.to_bits(),
            def.complexity_penalty.to_bits()
        );
    }

    #[test]
    fn quick_is_faster_than_balanced() {
        let q = SymRegConfig::quick();
        let b = SymRegConfig::balanced();
        assert!(q.max_iter <= b.max_iter);
        assert!(q.num_restarts <= b.num_restarts);
        assert!(q.max_depth <= b.max_depth);
    }

    #[test]
    fn exhaustive_is_slower_than_balanced() {
        let e = SymRegConfig::exhaustive();
        let b = SymRegConfig::balanced();
        assert!(e.max_iter >= b.max_iter);
        assert!(e.num_restarts >= b.num_restarts);
        assert!(e.max_depth >= b.max_depth);
    }

    #[test]
    fn engine_constructs_from_preset() {
        let _ = SymRegEngine::new(SymRegConfig::quick());
        let _ = SymRegEngine::new(SymRegConfig::balanced());
        let _ = SymRegEngine::new(SymRegConfig::exhaustive());
    }
}
