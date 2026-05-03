//! Lowering EML trees to standard mathematical operations.
//!
//! The EML representation is optimal for *discovery* (uniform search space)
//! but inefficient for *execution* (a single multiplication requires 41+ nodes).
//! Lowering converts EML trees to conventional operation trees for efficient
//! evaluation and human-readable output.

use crate::error::EmlError;
use crate::eval::EvalCtx;
use crate::named_const::NamedConst;
use crate::tree::{EmlNode, EmlTree};
use std::fmt;
use std::sync::OnceLock;

/// Sentinel variable index used as a wildcard in structural templates.
///
/// When a template contains `EmlNode::Var(WILDCARD_VAR)`, the matcher
/// captures the corresponding subtree from the candidate and enforces
/// that every wildcard occurrence refers to the same captured subtree.
///
/// Chosen well below `usize::MAX` to avoid overflow in `count_vars`
/// (which computes `i + 1`) and `EmlTree::var` (same), yet far above
/// any realistic user variable index.
const WILDCARD_VAR: usize = usize::MAX / 2;

/// A conventional mathematical operation tree.
///
/// Produced by lowering an EML tree. Supports efficient evaluation
/// and pretty-printing.
#[derive(Clone, Debug, PartialEq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(rename_all = "snake_case"))]
pub enum LoweredOp {
    /// Constant value.
    Const(f64),
    /// Input variable.
    Var(usize),
    /// Addition.
    Add(Box<LoweredOp>, Box<LoweredOp>),
    /// Subtraction.
    Sub(Box<LoweredOp>, Box<LoweredOp>),
    /// Multiplication.
    Mul(Box<LoweredOp>, Box<LoweredOp>),
    /// Division.
    Div(Box<LoweredOp>, Box<LoweredOp>),
    /// Exponential function.
    Exp(Box<LoweredOp>),
    /// Natural logarithm.
    Ln(Box<LoweredOp>),
    /// Sine.
    Sin(Box<LoweredOp>),
    /// Cosine.
    Cos(Box<LoweredOp>),
    /// Power.
    Pow(Box<LoweredOp>, Box<LoweredOp>),
    /// Negation.
    Neg(Box<LoweredOp>),
    /// Tangent.
    Tan(Box<LoweredOp>),
    /// Hyperbolic sine.
    Sinh(Box<LoweredOp>),
    /// Hyperbolic cosine.
    Cosh(Box<LoweredOp>),
    /// Hyperbolic tangent.
    Tanh(Box<LoweredOp>),
    /// Inverse sine (arcsine).
    Arcsin(Box<LoweredOp>),
    /// Inverse cosine (arccosine).
    Arccos(Box<LoweredOp>),
    /// Inverse tangent (arctangent).
    Arctan(Box<LoweredOp>),
    /// Inverse hyperbolic sine.
    Arcsinh(Box<LoweredOp>),
    /// Inverse hyperbolic cosine.
    Arccosh(Box<LoweredOp>),
    /// Inverse hyperbolic tangent.
    Arctanh(Box<LoweredOp>),
    /// A named mathematical constant (π, e, √2, …).
    ///
    /// Created only by the constants-extraction pass in [`crate::symreg`];
    /// never emitted by lowering. Constant-folds down to `Const(value())` on
    /// the first `simplify` call that encounters it in a binary/unary context.
    NamedConst(NamedConst),
}

/// Flat post-order instruction for stack-machine evaluation.
///
/// Produced by [`LoweredOp::to_oxiblas_ops`]. Consumed by scalar or
/// SIMD batch evaluators. Post-order means leaves come before operators:
/// `a + b` encodes as `[Const(a), Const(b), Add]`.
#[derive(Clone, Debug, PartialEq)]
pub enum OxiOp {
    /// Push a constant value.
    Const(f64),
    /// Push variable `vars[i]`.
    Var(usize),
    /// Pop two, push sum.
    Add,
    /// Pop two (a, b), push a - b.
    Sub,
    /// Pop two, push product.
    Mul,
    /// Pop two (a, b), push a / b.
    Div,
    /// Pop one, push negation.
    Neg,
    /// Pop one, push exp.
    Exp,
    /// Pop one, push ln.
    Ln,
    /// Pop one, push sin.
    Sin,
    /// Pop one, push cos.
    Cos,
    /// Pop two (base, exp), push base^exp.
    Pow,
    /// Pop one, push tan.
    Tan,
    /// Pop one, push sinh.
    Sinh,
    /// Pop one, push cosh.
    Cosh,
    /// Pop one, push tanh.
    Tanh,
    /// Pop one, push arcsin (asin).
    Arcsin,
    /// Pop one, push arccos (acos).
    Arccos,
    /// Pop one, push arctan (atan).
    Arctan,
    /// Pop one, push arcsinh (asinh).
    Arcsinh,
    /// Pop one, push arccosh (acosh).
    Arccosh,
    /// Pop one, push arctanh (atanh).
    Arctanh,
}

pub use crate::lower_interval::IntervalLO;

impl EmlTree {
    /// Lower an EML tree to a conventional operation tree.
    ///
    /// Recognizes common EML patterns (exp, ln, arithmetic) and
    /// converts them to their standard equivalents. Unrecognized
    /// subtrees are lowered as literal `exp(left) - ln(right)`.
    pub fn lower(&self) -> LoweredOp {
        lower_node(&self.root)
    }

    /// Evaluate the tree at real-valued variables **via the lowered IR**.
    ///
    /// Unlike [`EmlTree::eval_real`], which walks the raw EML tree through
    /// complex arithmetic (and accumulates ~1e-2 precision drift on deep
    /// constructions such as `Canonical::sin(x)`), this method first lowers
    /// the tree (recognising `sin`/`cos`/arithmetic patterns), simplifies
    /// the lowered IR, and evaluates through the `OxiOp` stack machine.
    ///
    /// Because the stack machine dispatches directly to `f64::sin`/`f64::cos`
    /// when the lowering recognised a trig pattern, the result attains
    /// full `f64` precision (~1e-15).
    ///
    /// # Errors
    /// Returns `Err(EmlError::NanEncountered)` if the IR evaluates to NaN.
    pub fn eval_real_lowered(&self, ctx: &EvalCtx) -> Result<f64, EmlError> {
        let lowered = self.lower().simplify();
        let ops = lowered.to_oxiblas_ops();
        let result = LoweredOp::eval_ops(&ops, ctx.as_slice());
        if result.is_nan() {
            return Err(EmlError::NanEncountered);
        }
        Ok(result)
    }
}

/// Lower a single EML node to a `LoweredOp`.
fn lower_node(node: &EmlNode) -> LoweredOp {
    match node {
        EmlNode::One => LoweredOp::Const(1.0),
        EmlNode::Var(i) => LoweredOp::Var(*i),
        EmlNode::Eml { left, right } => {
            // Try to recognize known patterns before falling back to exp(l) - ln(r).
            // Patterns are checked most-specific first to avoid premature matches.

            // Most specific: recognise canonical `Canonical::sin(x)` / `Canonical::cos(x)`
            // tree shapes and lower them to native `LoweredOp::Sin` / `LoweredOp::Cos`,
            // giving f64::sin / f64::cos precision (~1e-15) instead of the ~1e-2 drift
            // that complex-arithmetic evaluation accumulates over the deep Euler-formula
            // EML tree.
            if let Some(inner) = match_sin_structure(node) {
                return LoweredOp::Sin(Box::new(lower_node(&inner)));
            }
            if let Some(inner) = match_cos_structure(node) {
                return LoweredOp::Cos(Box::new(lower_node(&inner)));
            }

            // Pattern: eml(x, One) = exp(x)
            if matches!(right.as_ref(), EmlNode::One) {
                // Sub-pattern: eml(ln_tree, One) = exp(ln(x)) = x
                if let Some(inner) = match_ln_structure(left) {
                    return lower_node(&inner);
                }
                return LoweredOp::Exp(Box::new(lower_node(left)));
            }

            // Pattern: eml(One, One) = e
            if matches!(left.as_ref(), EmlNode::One) && matches!(right.as_ref(), EmlNode::One) {
                return LoweredOp::Const(std::f64::consts::E);
            }

            // Pattern: eml(One, eml(eml(One, x), One)) = ln(x)
            // MUST be checked before the e-x pattern since it's more specific.
            if matches!(left.as_ref(), EmlNode::One) {
                if let Some(inner) = match_ln_of_right(right) {
                    return LoweredOp::Ln(Box::new(lower_node(&inner)));
                }
            }

            // Pattern: eml(One, eml(x, One)) = e - x
            if matches!(left.as_ref(), EmlNode::One) {
                if let EmlNode::Eml {
                    left: inner_l,
                    right: inner_r,
                } = right.as_ref()
                {
                    if matches!(inner_r.as_ref(), EmlNode::One) {
                        let x_lowered = lower_node(inner_l);
                        return LoweredOp::Sub(
                            Box::new(LoweredOp::Const(std::f64::consts::E)),
                            Box::new(x_lowered),
                        );
                    }
                }
            }

            // Pattern: eml(ln(x), eml(y, One)) = x - y (subtraction)
            // This is the sub() canonical construction.
            if let Some(x_inner) = match_ln_structure(left) {
                if let EmlNode::Eml {
                    left: y_node,
                    right: y_one,
                } = right.as_ref()
                {
                    if matches!(y_one.as_ref(), EmlNode::One) {
                        // eml(ln(x), eml(y, 1)) = exp(ln(x)) - ln(exp(y)) = x - y
                        return LoweredOp::Sub(
                            Box::new(lower_node(&x_inner)),
                            Box::new(lower_node(y_node)),
                        );
                    }
                }
            }

            // Default: eml(left, right) = exp(left) - ln(right)
            let left_lowered = lower_node(left);
            let right_lowered = lower_node(right);
            LoweredOp::Sub(
                Box::new(LoweredOp::Exp(Box::new(left_lowered))),
                Box::new(LoweredOp::Ln(Box::new(right_lowered))),
            )
        }
    }
}

/// Match the ln structure: `eml(1, eml(eml(1, x), 1))` → returns `x`.
fn match_ln_structure(node: &EmlNode) -> Option<EmlNode> {
    if let EmlNode::Eml { left, right } = node {
        if !matches!(left.as_ref(), EmlNode::One) {
            return None;
        }
        if let EmlNode::Eml {
            left: mid_l,
            right: mid_r,
        } = right.as_ref()
        {
            if !matches!(mid_r.as_ref(), EmlNode::One) {
                return None;
            }
            if let EmlNode::Eml {
                left: inner_l,
                right: inner_r,
            } = mid_l.as_ref()
            {
                if matches!(inner_l.as_ref(), EmlNode::One) {
                    return Some(inner_r.as_ref().clone());
                }
            }
        }
    }
    None
}

/// Match ln pattern in the right subtree of `eml(1, right)`.
/// Looks for `eml(eml(1, x), 1)` inside right, giving `ln(x)`.
fn match_ln_of_right(right: &EmlNode) -> Option<EmlNode> {
    if let EmlNode::Eml {
        left: mid_l,
        right: mid_r,
    } = right
    {
        if !matches!(mid_r.as_ref(), EmlNode::One) {
            return None;
        }
        if let EmlNode::Eml {
            left: inner_l,
            right: inner_r,
        } = mid_l.as_ref()
        {
            if matches!(inner_l.as_ref(), EmlNode::One) {
                return Some(inner_r.as_ref().clone());
            }
        }
    }
    None
}

/// Lazily-initialised canonical `sin(x_placeholder)` tree, where `x_placeholder`
/// is `EmlNode::Var(WILDCARD_VAR)`. Used as a unification template.
fn sin_template() -> &'static EmlNode {
    static TEMPLATE: OnceLock<EmlNode> = OnceLock::new();
    TEMPLATE.get_or_init(|| {
        let placeholder = EmlTree::var(WILDCARD_VAR);
        let tree = crate::canonical::Canonical::sin(&placeholder);
        (*tree.root).clone()
    })
}

/// Lazily-initialised canonical `cos(x_placeholder)` tree.
fn cos_template() -> &'static EmlNode {
    static TEMPLATE: OnceLock<EmlNode> = OnceLock::new();
    TEMPLATE.get_or_init(|| {
        let placeholder = EmlTree::var(WILDCARD_VAR);
        let tree = crate::canonical::Canonical::cos(&placeholder);
        (*tree.root).clone()
    })
}

/// Unify `candidate` against `template`, where `template` may contain wildcards
/// (`EmlNode::Var(WILDCARD_VAR)`). On success, returns `Some(captured_subtree)`.
///
/// All wildcard occurrences in the template must capture the **same** subtree
/// structurally. If any mismatch or inconsistent capture is found, returns `None`.
///
/// Non-wildcard leaves and internal nodes must match exactly; two `Eml` nodes
/// recurse on both children.
fn unify_with_wildcard<'a>(
    candidate: &'a EmlNode,
    template: &EmlNode,
    captured: &mut Option<&'a EmlNode>,
) -> bool {
    // Wildcard in template captures (or must agree with previous capture).
    if let EmlNode::Var(idx) = template {
        if *idx == WILDCARD_VAR {
            match captured {
                None => {
                    *captured = Some(candidate);
                    return true;
                }
                Some(prev) => {
                    return nodes_structurally_equal(prev, candidate);
                }
            }
        }
    }

    match (candidate, template) {
        (EmlNode::One, EmlNode::One) => true,
        (EmlNode::Var(a), EmlNode::Var(b)) => a == b,
        (
            EmlNode::Eml {
                left: la,
                right: ra,
            },
            EmlNode::Eml {
                left: lb,
                right: rb,
            },
        ) => {
            unify_with_wildcard(la.as_ref(), lb.as_ref(), captured)
                && unify_with_wildcard(ra.as_ref(), rb.as_ref(), captured)
        }
        _ => false,
    }
}

/// Structural equality on `EmlNode` references.
fn nodes_structurally_equal(a: &EmlNode, b: &EmlNode) -> bool {
    match (a, b) {
        (EmlNode::One, EmlNode::One) => true,
        (EmlNode::Var(i), EmlNode::Var(j)) => i == j,
        (
            EmlNode::Eml {
                left: la,
                right: ra,
            },
            EmlNode::Eml {
                left: lb,
                right: rb,
            },
        ) => {
            nodes_structurally_equal(la.as_ref(), lb.as_ref())
                && nodes_structurally_equal(ra.as_ref(), rb.as_ref())
        }
        _ => false,
    }
}

/// Recognise the canonical `Canonical::sin(x)` EML tree shape.
/// Returns the captured `x` subtree on success.
fn match_sin_structure(node: &EmlNode) -> Option<EmlNode> {
    let mut captured: Option<&EmlNode> = None;
    if unify_with_wildcard(node, sin_template(), &mut captured) {
        captured.cloned()
    } else {
        None
    }
}

/// Recognise the canonical `Canonical::cos(x)` EML tree shape.
/// Returns the captured `x` subtree on success.
fn match_cos_structure(node: &EmlNode) -> Option<EmlNode> {
    let mut captured: Option<&EmlNode> = None;
    if unify_with_wildcard(node, cos_template(), &mut captured) {
        captured.cloned()
    } else {
        None
    }
}

impl LoweredOp {
    /// Flatten this tree into a post-order instruction list for stack-machine evaluation.
    ///
    /// The returned slice can be fed to [`Self::eval_ops`] for scalar evaluation
    /// or to `simd_eval::eval_batch_simd` for SIMD-accelerated batch evaluation.
    pub fn to_oxiblas_ops(&self) -> Vec<OxiOp> {
        let mut ops = Vec::new();
        self.collect_ops(&mut ops);
        ops
    }

    fn collect_ops(&self, ops: &mut Vec<OxiOp>) {
        match self {
            Self::Const(c) => ops.push(OxiOp::Const(*c)),
            Self::NamedConst(nc) => ops.push(OxiOp::Const(nc.value())),
            Self::Var(i) => ops.push(OxiOp::Var(*i)),
            Self::Add(a, b) => {
                a.collect_ops(ops);
                b.collect_ops(ops);
                ops.push(OxiOp::Add);
            }
            Self::Sub(a, b) => {
                a.collect_ops(ops);
                b.collect_ops(ops);
                ops.push(OxiOp::Sub);
            }
            Self::Mul(a, b) => {
                a.collect_ops(ops);
                b.collect_ops(ops);
                ops.push(OxiOp::Mul);
            }
            Self::Div(a, b) => {
                a.collect_ops(ops);
                b.collect_ops(ops);
                ops.push(OxiOp::Div);
            }
            Self::Exp(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Exp);
            }
            Self::Ln(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Ln);
            }
            Self::Sin(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Sin);
            }
            Self::Cos(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Cos);
            }
            Self::Pow(a, b) => {
                a.collect_ops(ops);
                b.collect_ops(ops);
                ops.push(OxiOp::Pow);
            }
            Self::Neg(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Neg);
            }
            Self::Tan(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Tan);
            }
            Self::Sinh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Sinh);
            }
            Self::Cosh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Cosh);
            }
            Self::Tanh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Tanh);
            }
            Self::Arcsin(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arcsin);
            }
            Self::Arccos(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arccos);
            }
            Self::Arctan(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arctan);
            }
            Self::Arcsinh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arcsinh);
            }
            Self::Arccosh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arccosh);
            }
            Self::Arctanh(a) => {
                a.collect_ops(ops);
                ops.push(OxiOp::Arctanh);
            }
        }
    }

    /// Evaluate a flat instruction list over scalar variable values.
    ///
    /// Runs a stack machine: push leaves, pop operands for each operator.
    /// Returns `f64::NAN` for stack underflow (malformed instruction sequence).
    pub fn eval_ops(ops: &[OxiOp], vars: &[f64]) -> f64 {
        let mut stack: Vec<f64> = Vec::with_capacity(ops.len());
        for op in ops {
            match op {
                OxiOp::Const(c) => stack.push(*c),
                OxiOp::Var(i) => {
                    stack.push(vars.get(*i).copied().unwrap_or(f64::NAN));
                }
                OxiOp::Add => {
                    let b = stack.pop().unwrap_or(f64::NAN);
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a + b);
                }
                OxiOp::Sub => {
                    let b = stack.pop().unwrap_or(f64::NAN);
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a - b);
                }
                OxiOp::Mul => {
                    let b = stack.pop().unwrap_or(f64::NAN);
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a * b);
                }
                OxiOp::Div => {
                    let b = stack.pop().unwrap_or(f64::NAN);
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a / b);
                }
                OxiOp::Neg => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(-a);
                }
                OxiOp::Exp => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.exp());
                }
                OxiOp::Ln => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.ln());
                }
                OxiOp::Sin => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.sin());
                }
                OxiOp::Cos => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.cos());
                }
                OxiOp::Pow => {
                    let b = stack.pop().unwrap_or(f64::NAN);
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.powf(b));
                }
                OxiOp::Tan => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.tan());
                }
                OxiOp::Sinh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.sinh());
                }
                OxiOp::Cosh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.cosh());
                }
                OxiOp::Tanh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.tanh());
                }
                OxiOp::Arcsin => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.asin());
                }
                OxiOp::Arccos => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.acos());
                }
                OxiOp::Arctan => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.atan());
                }
                OxiOp::Arcsinh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.asinh());
                }
                OxiOp::Arccosh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.acosh());
                }
                OxiOp::Arctanh => {
                    let a = stack.pop().unwrap_or(f64::NAN);
                    stack.push(a.atanh());
                }
            }
        }
        stack.pop().unwrap_or(f64::NAN)
    }

    /// Evaluate a batch of data points using the flat IR. Uses SIMD when the
    /// `simd` feature is enabled; otherwise delegates to scalar evaluation.
    ///
    /// Returns a `Vec<f64>` of the same length as `data`. Unlike
    /// [`crate::eval::EvalCtx`]-based evaluation, NaN/inf propagate silently
    /// (no `Result` wrapping) — the IR layer treats them as valid f64 values.
    pub fn eval_batch(&self, data: &[Vec<f64>]) -> Vec<f64> {
        let ops = self.to_oxiblas_ops();
        #[cfg(feature = "simd")]
        {
            crate::simd_eval::eval_batch_simd(&ops, data)
        }
        #[cfg(not(feature = "simd"))]
        {
            Self::eval_batch_scalar_from_ops(&ops, data)
        }
    }

    /// Scalar batch evaluation over a pre-built flat IR slice.
    ///
    /// Exposed as `pub` so the `simd_eval` stub and SIMD remainder path can
    /// delegate to it without re-encoding the tree.
    pub fn eval_batch_scalar_from_ops(ops: &[OxiOp], data: &[Vec<f64>]) -> Vec<f64> {
        data.iter().map(|row| Self::eval_ops(ops, row)).collect()
    }

    /// Scalar batch evaluation building the flat IR internally.
    pub fn eval_batch_scalar(&self, data: &[Vec<f64>]) -> Vec<f64> {
        let ops = self.to_oxiblas_ops();
        Self::eval_batch_scalar_from_ops(&ops, data)
    }

    /// Compute a structural hash of this tree.
    ///
    /// Used by the symbolic regression pruner to detect semantically equivalent
    /// topologies after lowering + simplification.
    ///
    /// **f64 note**: constants are hashed as `c.to_bits()` (a `u64`) since
    /// `f64` does not implement `Hash`.
    pub fn structural_hash<H: std::hash::Hasher>(&self, state: &mut H) {
        use std::hash::Hash;
        match self {
            Self::Const(c) => {
                0u8.hash(state);
                c.to_bits().hash(state);
            }
            Self::NamedConst(nc) => {
                // Hash as if it were the equivalent Const so structural
                // deduplication treats NamedConst(Pi) == Const(PI).
                0u8.hash(state);
                nc.value().to_bits().hash(state);
            }
            Self::Var(i) => {
                1u8.hash(state);
                i.hash(state);
            }
            Self::Add(a, b) => {
                a.structural_hash(state);
                b.structural_hash(state);
                2u8.hash(state);
            }
            Self::Sub(a, b) => {
                a.structural_hash(state);
                b.structural_hash(state);
                3u8.hash(state);
            }
            Self::Mul(a, b) => {
                a.structural_hash(state);
                b.structural_hash(state);
                4u8.hash(state);
            }
            Self::Div(a, b) => {
                a.structural_hash(state);
                b.structural_hash(state);
                5u8.hash(state);
            }
            Self::Exp(a) => {
                a.structural_hash(state);
                6u8.hash(state);
            }
            Self::Ln(a) => {
                a.structural_hash(state);
                7u8.hash(state);
            }
            Self::Sin(a) => {
                a.structural_hash(state);
                8u8.hash(state);
            }
            Self::Cos(a) => {
                a.structural_hash(state);
                9u8.hash(state);
            }
            Self::Pow(a, b) => {
                a.structural_hash(state);
                b.structural_hash(state);
                10u8.hash(state);
            }
            Self::Neg(a) => {
                a.structural_hash(state);
                11u8.hash(state);
            }
            Self::Tan(a) => {
                a.structural_hash(state);
                12u8.hash(state);
            }
            Self::Sinh(a) => {
                a.structural_hash(state);
                13u8.hash(state);
            }
            Self::Cosh(a) => {
                a.structural_hash(state);
                14u8.hash(state);
            }
            Self::Tanh(a) => {
                a.structural_hash(state);
                15u8.hash(state);
            }
            Self::Arcsin(a) => {
                a.structural_hash(state);
                16u8.hash(state);
            }
            Self::Arccos(a) => {
                a.structural_hash(state);
                17u8.hash(state);
            }
            Self::Arctan(a) => {
                a.structural_hash(state);
                18u8.hash(state);
            }
            Self::Arcsinh(a) => {
                a.structural_hash(state);
                19u8.hash(state);
            }
            Self::Arccosh(a) => {
                a.structural_hash(state);
                20u8.hash(state);
            }
            Self::Arctanh(a) => {
                a.structural_hash(state);
                21u8.hash(state);
            }
        }
    }

    /// Convert to a human-readable mathematical expression string.
    pub fn to_pretty(&self) -> String {
        format!("{self}")
    }

    /// Convert to a LaTeX math expression string.
    ///
    /// Produces valid LaTeX for use inside `$...$` or `\[...\]` math mode.
    ///
    /// # Examples
    /// ```
    /// use oxieml::LoweredOp;
    /// let expr = LoweredOp::Div(
    ///     Box::new(LoweredOp::Const(1.0)),
    ///     Box::new(LoweredOp::Var(0)),
    /// );
    /// assert_eq!(expr.to_latex(), r"\frac{1}{x_{0}}");
    /// ```
    pub fn to_latex(&self) -> String {
        fn render(op: &LoweredOp, top_level: bool) -> String {
            match op {
                LoweredOp::NamedConst(nc) => nc.to_latex().to_string(),
                LoweredOp::Const(c) => {
                    if (*c - std::f64::consts::E).abs() < 1e-15 {
                        "e".to_string()
                    } else if (*c - std::f64::consts::PI).abs() < 1e-15 {
                        r"\pi".to_string()
                    } else if (*c - std::f64::consts::TAU).abs() < 1e-15 {
                        r"2\pi".to_string()
                    } else if (*c - (-1.0_f64)).abs() < 1e-15 {
                        "-1".to_string()
                    } else if (c - c.round()).abs() < 1e-10 && c.abs() < 1e15 {
                        format!("{}", *c as i64)
                    } else {
                        format!("{c:.6}")
                    }
                }
                LoweredOp::Var(i) => format!("x_{{{i}}}"),
                LoweredOp::Add(a, b) => {
                    let inner = format!("{} + {}", render(a, false), render(b, false));
                    if top_level {
                        inner
                    } else {
                        format!("({inner})")
                    }
                }
                LoweredOp::Sub(a, b) => {
                    let inner = format!("{} - {}", render(a, false), render(b, false));
                    if top_level {
                        inner
                    } else {
                        format!("({inner})")
                    }
                }
                LoweredOp::Mul(a, b) => {
                    let inner = format!(r"{} \cdot {}", render(a, false), render(b, false));
                    if top_level {
                        inner
                    } else {
                        format!("({inner})")
                    }
                }
                LoweredOp::Div(a, b) => {
                    format!(r"\frac{{{}}}{{{}}}", render(a, true), render(b, true))
                }
                LoweredOp::Exp(a) => {
                    let arg = render(a, true);
                    format!("e^{{{arg}}}")
                }
                LoweredOp::Ln(a) => {
                    format!(r"\ln\left({}\right)", render(a, true))
                }
                LoweredOp::Sin(a) => {
                    format!(r"\sin\left({}\right)", render(a, true))
                }
                LoweredOp::Cos(a) => {
                    format!(r"\cos\left({}\right)", render(a, true))
                }
                LoweredOp::Pow(base, exp) => {
                    let b = render(base, false);
                    let e = render(exp, true);
                    format!("{b}^{{{e}}}")
                }
                LoweredOp::Neg(a) => {
                    let inner = render(a, false);
                    format!("-{inner}")
                }
                LoweredOp::Tan(a) => {
                    format!(r"\tan{{{}}}", render(a, true))
                }
                LoweredOp::Sinh(a) => {
                    format!(r"\sinh{{{}}}", render(a, true))
                }
                LoweredOp::Cosh(a) => {
                    format!(r"\cosh{{{}}}", render(a, true))
                }
                LoweredOp::Tanh(a) => {
                    format!(r"\tanh{{{}}}", render(a, true))
                }
                LoweredOp::Arcsin(a) => {
                    format!(r"\arcsin{{{}}}", render(a, true))
                }
                LoweredOp::Arccos(a) => {
                    format!(r"\arccos{{{}}}", render(a, true))
                }
                LoweredOp::Arctan(a) => {
                    format!(r"\arctan{{{}}}", render(a, true))
                }
                LoweredOp::Arcsinh(a) => {
                    format!(r"\operatorname{{arcsinh}}{{{}}}", render(a, true))
                }
                LoweredOp::Arccosh(a) => {
                    format!(r"\operatorname{{arccosh}}{{{}}}", render(a, true))
                }
                LoweredOp::Arctanh(a) => {
                    format!(r"\operatorname{{arctanh}}{{{}}}", render(a, true))
                }
            }
        }
        render(self, true)
    }

    /// Evaluate the lowered operation tree with the given variable values.
    pub fn eval(&self, vars: &[f64]) -> f64 {
        match self {
            Self::Const(c) => *c,
            Self::NamedConst(nc) => nc.value(),
            Self::Var(i) => vars[*i],
            Self::Add(a, b) => a.eval(vars) + b.eval(vars),
            Self::Sub(a, b) => a.eval(vars) - b.eval(vars),
            Self::Mul(a, b) => a.eval(vars) * b.eval(vars),
            Self::Div(a, b) => a.eval(vars) / b.eval(vars),
            Self::Exp(a) => a.eval(vars).exp(),
            Self::Ln(a) => a.eval(vars).ln(),
            Self::Sin(a) => a.eval(vars).sin(),
            Self::Cos(a) => a.eval(vars).cos(),
            Self::Pow(a, b) => a.eval(vars).powf(b.eval(vars)),
            Self::Neg(a) => -a.eval(vars),
            Self::Tan(a) => a.eval(vars).tan(),
            Self::Sinh(a) => a.eval(vars).sinh(),
            Self::Cosh(a) => a.eval(vars).cosh(),
            Self::Tanh(a) => a.eval(vars).tanh(),
            Self::Arcsin(a) => a.eval(vars).asin(),
            Self::Arccos(a) => a.eval(vars).acos(),
            Self::Arctan(a) => a.eval(vars).atan(),
            Self::Arcsinh(a) => a.eval(vars).asinh(),
            Self::Arccosh(a) => a.eval(vars).acosh(),
            Self::Arctanh(a) => a.eval(vars).atanh(),
        }
    }
}

impl fmt::Display for LoweredOp {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NamedConst(nc) => write!(f, "{}", nc.to_pretty()),
            Self::Const(c) => {
                if (*c - std::f64::consts::E).abs() < 1e-15 {
                    write!(f, "e")
                } else if (*c - std::f64::consts::PI).abs() < 1e-15 {
                    write!(f, "π")
                } else if (c - c.round()).abs() < 1e-10 && c.abs() < 1e15 {
                    write!(f, "{}", *c as i64)
                } else {
                    write!(f, "{c:.6}")
                }
            }
            Self::Var(i) => write!(f, "x{i}"),
            Self::Add(a, b) => write!(f, "({a} + {b})"),
            Self::Sub(a, b) => write!(f, "({a} - {b})"),
            Self::Mul(a, b) => write!(f, "({a} * {b})"),
            Self::Div(a, b) => write!(f, "({a} / {b})"),
            Self::Exp(a) => write!(f, "exp({a})"),
            Self::Ln(a) => write!(f, "ln({a})"),
            Self::Sin(a) => write!(f, "sin({a})"),
            Self::Cos(a) => write!(f, "cos({a})"),
            Self::Pow(a, b) => write!(f, "({a})^({b})"),
            Self::Neg(a) => write!(f, "-{a}"),
            Self::Tan(a) => write!(f, "tan({a})"),
            Self::Sinh(a) => write!(f, "sinh({a})"),
            Self::Cosh(a) => write!(f, "cosh({a})"),
            Self::Tanh(a) => write!(f, "tanh({a})"),
            Self::Arcsin(a) => write!(f, "arcsin({a})"),
            Self::Arccos(a) => write!(f, "arccos({a})"),
            Self::Arctan(a) => write!(f, "arctan({a})"),
            Self::Arcsinh(a) => write!(f, "arcsinh({a})"),
            Self::Arccosh(a) => write!(f, "arccosh({a})"),
            Self::Arctanh(a) => write!(f, "arctanh({a})"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lower_one() {
        let t = EmlTree::one();
        let lowered = t.lower();
        assert_eq!(lowered, LoweredOp::Const(1.0));
    }

    #[test]
    fn test_lower_var() {
        let t = EmlTree::var(0);
        let lowered = t.lower();
        assert_eq!(lowered, LoweredOp::Var(0));
    }

    #[test]
    fn test_lower_exp() {
        // eml(x, 1) → exp(x)
        let x = EmlTree::var(0);
        let one = EmlTree::one();
        let exp_x = EmlTree::eml(&x, &one);
        let lowered = exp_x.lower();
        assert_eq!(lowered, LoweredOp::Exp(Box::new(LoweredOp::Var(0))));
    }

    #[test]
    fn test_lower_e_minus_x() {
        // eml(1, eml(x, 1)) → e - x
        let x = EmlTree::var(0);
        let one = EmlTree::one();
        let exp_x = EmlTree::eml(&x, &one);
        let e_minus_x = EmlTree::eml(&one, &exp_x);
        let lowered = e_minus_x.lower();
        assert_eq!(
            lowered,
            LoweredOp::Sub(
                Box::new(LoweredOp::Const(std::f64::consts::E)),
                Box::new(LoweredOp::Var(0)),
            )
        );
    }

    #[test]
    fn test_lower_ln() {
        // eml(1, eml(eml(1, x), 1)) → ln(x)
        let x = EmlTree::var(0);
        let one = EmlTree::one();
        let inner = EmlTree::eml(&one, &x); // eml(1, x)
        let middle = EmlTree::eml(&inner, &one); // eml(eml(1,x), 1)
        let ln_x = EmlTree::eml(&one, &middle); // eml(1, eml(eml(1,x), 1))
        let lowered = ln_x.lower();
        assert_eq!(lowered, LoweredOp::Ln(Box::new(LoweredOp::Var(0))));
    }

    #[test]
    fn test_lowered_eval() {
        let op = LoweredOp::Add(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Const(3.0)));
        assert!((op.eval(&[2.0]) - 5.0).abs() < 1e-15);
    }

    #[test]
    fn test_pretty_print() {
        let op = LoweredOp::Mul(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
        assert_eq!(op.to_pretty(), "(x0 * x1)");
    }

    #[test]
    fn test_simplify_exp_ln() {
        // exp(ln(x)) → x
        let op = LoweredOp::Exp(Box::new(LoweredOp::Ln(Box::new(LoweredOp::Var(0)))));
        let simplified = op.simplify();
        assert_eq!(simplified, LoweredOp::Var(0));
    }

    #[test]
    fn test_simplify_constants() {
        let op = LoweredOp::Add(
            Box::new(LoweredOp::Const(2.0)),
            Box::new(LoweredOp::Const(3.0)),
        );
        let simplified = op.simplify();
        assert_eq!(simplified, LoweredOp::Const(5.0));
    }

    #[test]
    fn test_to_oxiblas_ops_roundtrip() {
        use crate::Canonical;
        // exp(x)
        let x = crate::tree::EmlTree::var(0);
        let exp_x = Canonical::exp(&x);
        let lowered = exp_x.lower();
        let ops = lowered.to_oxiblas_ops();
        let result = LoweredOp::eval_ops(&ops, &[1.5_f64]);
        assert!(
            (result - 1.5_f64.exp()).abs() < 1e-12,
            "exp roundtrip failed: {result}"
        );

        // ln(x)
        let ln_x = Canonical::ln(&x);
        let lowered_ln = ln_x.lower();
        let ops_ln = lowered_ln.to_oxiblas_ops();
        let result_ln = LoweredOp::eval_ops(&ops_ln, &[2.0_f64]);
        assert!(
            (result_ln - 2.0_f64.ln()).abs() < 1e-12,
            "ln roundtrip failed: {result_ln}"
        );

        // sin(x) — directly construct LoweredOp::Sin to test the Sin opcode
        // (Canonical::sin uses complex arithmetic and requires complex evaluation)
        let lowered_sin = LoweredOp::Sin(Box::new(LoweredOp::Var(0)));
        let ops_sin = lowered_sin.to_oxiblas_ops();
        let result_sin = LoweredOp::eval_ops(&ops_sin, &[std::f64::consts::PI / 6.0]);
        assert!(
            (result_sin - 0.5_f64).abs() < 1e-9,
            "sin roundtrip failed: {result_sin}"
        );
    }

    #[test]
    fn test_eval_batch_scalar_matches_eval() {
        use crate::Canonical;
        let x = crate::tree::EmlTree::var(0);
        let exp_x = Canonical::exp(&x);
        let lowered = exp_x.lower();

        let data: Vec<Vec<f64>> = (0..100).map(|i| vec![i as f64 * 0.05]).collect();
        let batch_results = lowered.eval_batch_scalar(&data);
        assert_eq!(batch_results.len(), 100);
        for (row, result) in data.iter().zip(batch_results.iter()) {
            let expected = lowered.eval(row);
            assert!(
                (result - expected).abs() < 1e-12,
                "mismatch at x={}: got {result}, expected {expected}",
                row[0]
            );
        }
    }

    #[test]
    fn test_structural_hash_differs() {
        use crate::Canonical;
        use std::collections::hash_map::DefaultHasher;
        use std::hash::Hasher;

        let x = crate::tree::EmlTree::var(0);
        let exp_x = Canonical::exp(&x).lower().simplify();
        let ln_x = Canonical::ln(&x).lower().simplify();

        let mut h1 = DefaultHasher::new();
        exp_x.structural_hash(&mut h1);
        let mut h2 = DefaultHasher::new();
        ln_x.structural_hash(&mut h2);
        assert_ne!(
            h1.finish(),
            h2.finish(),
            "exp and ln should have different structural hashes"
        );
    }

    #[test]
    fn test_structural_hash_same_for_equiv() {
        use crate::Canonical;
        use std::collections::hash_map::DefaultHasher;
        use std::hash::Hasher;

        let x = crate::tree::EmlTree::var(0);
        let exp_x1 = Canonical::exp(&x).lower().simplify();
        let exp_x2 = Canonical::exp(&x).lower().simplify();

        let mut h1 = DefaultHasher::new();
        exp_x1.structural_hash(&mut h1);
        let mut h2 = DefaultHasher::new();
        exp_x2.structural_hash(&mut h2);
        assert_eq!(
            h1.finish(),
            h2.finish(),
            "identical trees should have the same structural hash"
        );
    }

    #[test]
    fn latex_var() {
        assert_eq!(LoweredOp::Var(0).to_latex(), "x_{0}");
        assert_eq!(LoweredOp::Var(3).to_latex(), "x_{3}");
    }

    #[test]
    fn latex_const_pi() {
        assert_eq!(LoweredOp::Const(std::f64::consts::PI).to_latex(), r"\pi");
    }

    #[test]
    fn latex_const_e() {
        assert_eq!(LoweredOp::Const(std::f64::consts::E).to_latex(), "e");
    }

    #[test]
    fn latex_const_integer() {
        assert_eq!(LoweredOp::Const(2.0).to_latex(), "2");
        assert_eq!(LoweredOp::Const(-1.0).to_latex(), "-1");
    }

    #[test]
    fn latex_div() {
        let op = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), r"\frac{1}{x_{0}}");
    }

    #[test]
    fn latex_exp() {
        let op = LoweredOp::Exp(Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), r"e^{x_{0}}");
    }

    #[test]
    fn latex_ln() {
        let op = LoweredOp::Ln(Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), r"\ln\left(x_{0}\right)");
    }

    #[test]
    fn latex_sin_cos() {
        let op = LoweredOp::Sin(Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), r"\sin\left(x_{0}\right)");
        let op2 = LoweredOp::Cos(Box::new(LoweredOp::Var(0)));
        assert_eq!(op2.to_latex(), r"\cos\left(x_{0}\right)");
    }

    #[test]
    fn latex_pow() {
        let op = LoweredOp::Pow(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Const(2.0)));
        assert_eq!(op.to_latex(), "x_{0}^{2}");
    }

    #[test]
    fn latex_neg() {
        let op = LoweredOp::Neg(Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), "-x_{0}");
    }

    #[test]
    fn latex_mul() {
        let op = LoweredOp::Mul(Box::new(LoweredOp::Const(2.0)), Box::new(LoweredOp::Var(0)));
        assert_eq!(op.to_latex(), r"2 \cdot x_{0}");
    }

    #[test]
    fn latex_composite() {
        let op = LoweredOp::Div(
            Box::new(LoweredOp::Sin(Box::new(LoweredOp::Var(0)))),
            Box::new(LoweredOp::Cos(Box::new(LoweredOp::Var(0)))),
        );
        let latex = op.to_latex();
        assert!(latex.contains(r"\frac"));
        assert!(latex.contains(r"\sin"));
        assert!(latex.contains(r"\cos"));
    }
}
