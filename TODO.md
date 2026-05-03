# OxiEML TODO

## Phylogenetic Tree (Paper Figure 1) — Canonical Constructions

All functions from the paper's phylogenetic tree are implemented in `src/canonical.rs`:

- [x] **Core**: `eml`, `1`
- [x] **Basic**: `exp`, `ln`, `e` (Euler's number)
- [x] **Arithmetic**: `add`, `sub`, `mul`, `div`, `neg`
- [x] **Powers**: `pow`, `square`, `sqrt`, `reciprocal`, `abs`
- [x] **Trig**: `sin`, `cos`, `tan`
- [x] **Inverse trig**: `arcsin`, `arccos`, `arctan` (via complex logarithms)
- [x] **Hyperbolic**: `sinh`, `cosh`, `tanh`
- [x] **Inverse hyperbolic**: `arcsinh`, `arccosh`, `arctanh`
- [x] **Constants**: `pi` (iπ), `zero` (= ln(1)), `neg_one`, `neg_two`, `imag_unit`, `nat(n)`

## CLI Tool

- [x] **`src/parser.rs`** — recursive descent parser for `E(x,y)` / `eml(x,y)` notation.
- [x] **`src/bin/oxieml.rs`** — CLI evaluator with constant matching, complex eval, lowering; `--help`/`-V` flags.
- [x] **End-to-end verification** — user's 193-node depth-34 EML expression evaluates correctly to π.

## Code Quality

- [x] **Clean canonical doc comments** — replaced 250+ lines of derivation scratch-work with concise per-function docs in `src/canonical.rs`.
- [x] **Codegen / grad cleanup** — fixed trailing space in `Neg` codegen (`src/compile.rs`); pruned unused tape indices and prefixed unused locals in `src/grad.rs`.

## Functionality Implemented

- [x] **Real `simplify`** — `ln(exp(x))→x`, `exp(ln(x))→x`, structural-hash CSE/dedup (`src/simplify.rs`).
- [x] **Lower-pattern recognition** — subtraction `eml(ln(x), eml(y, 1)) → x − y`, exp-of-ln elimination, ln structural matching (`src/lower.rs`).
- [x] **Disjoint topology enumeration** — symreg generates each EML topology exactly once via three-case split (both/left/right at max depth) in `src/symreg.rs`.
- [x] **`canonical::zero()`** — added `0 = ln(1)` constructor.

## Lowered IR & Evaluation

- [x] **`LoweredOp::to_oxiblas_ops()` flat IR** — post-order `OxiOp` enum consumed by scalar/SIMD evaluator (`src/lower.rs`).
- [x] **`simd` feature** — real SIMD via `oxiblas-core` 0.2.1, runtime aarch64/x86_64 dispatch to `F64x2`/`F64x4`; combines with `parallel` for SIMD-per-worker (`src/simd_eval.rs`).
- [x] **`parallel` feature** — rayon `par_iter` batch eval, threshold 128 (scalar) / 512 (SIMD).
- [x] **Sin/cos precision** — `lower.rs` pattern-matches canonical sin/cos shapes → `LoweredOp::Sin`/`Cos`; `eval_real_lowered()` gives true `f64::sin` precision (0.0 vs ~1e-14 tree-walk error).

## Symbolic Tooling

- [x] **`LoweredOp::grad(wrt)`** — chain/product/quotient/`Pow`-via-exp-log rules, returns simplified `LoweredOp`; 13 tests cross-check against central differences (`src/lower.rs`).
- [x] **LaTeX export** — `LoweredOp::to_latex()` and `DiscoveredFormula::to_latex()` (π/e detection, `\frac`, `e^{·}`, `x_{i}`, etc.).
- [x] **`compile_to_rust` / `compile_to_closure` / `compile_to_rust_batch`** — codegen including parallel `_batch` form (`src/compile.rs`).

## SMT / Constraint Solving (`smt` feature)

- [x] **`IntervalDomain`** — always-on forward exp/ln propagation with conflict detection.
- [x] **`EmlSmtSolver`** — OxiZ 0.2 LRA backend via secant + tangent linear relaxation; proves UNSAT on cases interval bisection alone misses (e.g. `ln(x) > 0` on negative domain).
- [x] **`EmlNraSolver`** — interval-bisection fallback; constraints: `EqZero`, `GtZero`, `GeZero`, `And`, `Or`.

## Symbolic Regression

- [x] **`SymRegEngine::discover` / `discover_pareto`** — Adam optimizer, k-fold CV (`SymRegConfig.cv_folds`), Pareto front, parallel topology eval, depth-limited enumeration.
- [x] **Pareto-front API** — `discover_pareto()`, free `pareto_front(&[DiscoveredFormula])`, `DiscoveredFormula::dominates(&other)`.
- [x] **K-fold cross-validation** — deterministic shuffle, `cv_mse: Option<f64>`, no-param topologies skip CV.
- [x] **Presets** — `SymRegConfig::{quick, balanced, exhaustive}()`.
- [x] **Pruning** — `dedupe_by_semantics` via `lower().simplify().structural_hash`; correct but limited (~0.0002% reduction at depth 4 because EML is non-commutative).
- [x] **CLI `--symreg`** — stdin / `--file` data, top-K ranked output, every `SymRegConfig` field exposed; 4 integration tests via `assert_cmd` + `predicates`.

## Examples & Benchmarks

- [x] **`examples/physics_pipeline.rs`** — projectile-motion data → `discover` → lower → `compile_to_rust_batch` → batch eval on held-out set.
- [x] **`examples/pendulum.rs`** — 1-var, T = 2π√(L/g).
- [x] **`examples/harmonic_oscillator.rs`** — 3-var, x(t) = A·cos(ωt).
- [x] **`benches/eval_bench.rs`, `benches/trig_bench.rs`** — criterion comparisons of `eval_real` vs `eval_real_lowered` over sin/cos/exp/composite, 1000 points each.

## SciRS2 Adapter (`scirs2` feature)

- [x] **`src/scirs2.rs`** — `symbolic_regression(Array2, Array1, config)` and `_with_names` variant; row-major conversion under the hood; feature-gated optional `scirs2-core` dep.

## TensorLogic Integration (`tensorlogic` feature)

EML's uniform rewriting and TensorLogic's logic-to-tensor compilation are natural counterparts: OxiEML discovers closed-form formulas from data; TensorLogic compiles logical rules into einsum graphs for neurosymbolic AI. Connecting them gives a **data-driven formula discovery → neurosymbolic prior** pipeline.

**Dependency strategy (cycle-safe):** OxiEML may become a SciRS2 subcrate; TensorLogic's execution layer (`tensorlogic-scirs-backend`, `tensorlogic-train`) depends on SciRS2. To avoid cycles, OxiEML depends **only** on `tensorlogic-ir` — the engine-agnostic AST/IR layer with **zero SciRS2 dependencies** (verified: serde, serde_json, oxicode, chrono, thiserror only).

```
SciRS2 ─may contain→ OxiEML ─optional→ tensorlogic-ir  (no SciRS2 dep)
                                              │
TensorLogic ─depends→ SciRS2    tensorlogic-ir is SciRS2-free ✓
```

No cycle. The `tensorlogic-compiler` and `tensorlogic-adapters` crates are also SciRS2-free and may be used if needed.

- [x] **`to_tlexpr` / `from_tlexpr`** — bidirectional `LoweredOp ↔ TLExpr` mapping for the arithmetic/transcendental subset; `Neg` encoded as `Sub(0, x)`; logic-only `TLExpr` nodes return `EmlError::UnsupportedTlExpr` (`src/tensorlogic.rs`).
- [x] **`canonical_rewrite_rules()`** — 10 real `RewriteRule` instances over `tensorlogic_ir::Pattern` (exp/log inverses, double negation, identity elements `0+x`, `x*1`, `x/1`, `x^0`, `x^1`).
- [x] **Soft-prior export** — `DiscoveredFormula::{to_tlexpr, to_tl_weighted_rule, to_tl_weighted_equation}` + free `formulas_to_tl_weighted_rules`; reuses the same `lower().simplify()` chain as `to_latex` so the printed pretty form, LaTeX, and TLExpr stay in lock-step (9 tests, `src/tensorlogic.rs`, `src/symreg.rs`, `tests/tensorlogic_test.rs`).
- [x] **Core path stays in OxiEML** — tree eval, OxiOp stack machine, `simd_eval` have no dependency on `tensorlogic-compiler`, `tensorlogic-scirs-backend`, or `tensorlogic-train` in any feature set (verified 2026-04-15).

---

## Completed in v0.1.1 (2026-05-03)

- [x] **Extended LoweredOp variants for transcendentals** (implemented 2026-04-27) — add `Tan`, `Sinh`, `Cosh`, `Tanh`, `Arcsin`, `Arccos`, `Arctan`, `Arcsinh`, `Arccosh`, `Arctanh` and recognize their canonical EML shapes during lowering. `[medium]`
  - **Why:** Today these functions exist as `Canonical` constructions but lower to raw `Exp`/`Ln` forests, blowing up node counts, hurting `to_latex` / `to_pretty` readability, and forcing `grad` to differentiate through the desugaring instead of using the closed-form derivative. This is the single biggest gap in lowered-IR expressiveness.
  - **Design:** Extend the `LoweredOp` enum (one variant per function); update every consumer — `eval`, `eval_batch`, `simplify` (idempotent shape-preserving rules: `tanh(arctanh(x))→x`, etc.), `grad` (closed-form derivatives, e.g. `d/dx tanh(x) = 1 − tanh²(x)`), `to_latex`, `to_pretty`, `to_oxiblas_ops` (new `OxiOp` variants), `structural_hash`. Add canonical-shape pattern recognizers in `src/lower.rs` mirroring the existing sin/cos detectors. Provide a feature-flag-free fallback path: if the IR/SIMD backend doesn't yet implement a variant, expand inline to the existing exp/ln equivalent so behavior is preserved.
  - **Files:** `src/lower.rs`, `src/eval.rs`, `src/simplify.rs`, `src/compile.rs`, `src/simd_eval.rs`, `src/tensorlogic.rs`.
  - **Tests:** Round-trip canonical→lower→pretty assertions, grad central-difference cross-checks for each new variant, SIMD scalar/vector parity, LaTeX golden strings.
  - **Risk:** Variant explosion in matchers — every `match LoweredOp { ... }` gains 10 arms; missing one in a non-exhaustive site silently regresses. Mitigation: keep the enum non-`#[non_exhaustive]` so the compiler enforces exhaustiveness.

- [x] **Serde serialization for EmlTree / LoweredOp / DiscoveredFormula** (implemented 2026-04-27) — feature-gated `serde` support so formulas survive disk and process boundaries. `[medium]`
  - **Why:** Symbolic-regression runs are expensive; saving the Pareto front to JSON / oxicode is a research-workflow basic. Also unblocks Python bindings (cross-language transport) and reproducible experiment artifacts.
  - **Design:** Add optional `serde = "1"` and (for binary) `oxicode` deps gated on `serde`. Derive `Serialize` / `Deserialize` on `EmlTree`, `EmlNode`, `LoweredOp`, `DiscoveredFormula`, `SymRegConfig`. Use `#[serde(rename_all = "snake_case")]` and an explicit version tag (`#[serde(tag = "v")]`) to keep file format upgradable. Ship `EmlTree::to_json` / `from_json` convenience methods; binary path uses oxicode (NOT bincode — COOLJAPAN policy).
  - **Files:** `Cargo.toml`, `src/tree.rs`, `src/lower.rs`, `src/symreg.rs`, `src/lib.rs`, new `tests/serde_test.rs`.
  - **Tests:** Round-trip equality for each type (deep-nested tree, every `LoweredOp` variant, `DiscoveredFormula` with `cv_mse: Some` and `None`); golden JSON snapshot to detect accidental schema breaks.
  - **Risk:** Schema lock-in — once published, field renames are breaking. Mitigation: explicit version tag from day one, `#[serde(default)]` on additive fields.

- [x] **Constant folding in `simplify`** (implemented 2026-04-27) — fold `Const(a)` op `Const(b)` → `Const(a op b)` for `Add`/`Sub`/`Mul`/`Div`/`Pow`/`Exp`/`Ln`/`Neg` (and the new transcendentals). `[small]`
  - **Why:** Surprisingly absent today: `Add(Const(2.0), Const(3.0))` survives `simplify`. After the canonical-construction path runs, lowered trees often contain folded subexpressions that should collapse to a single constant before printing or grad. Free correctness/readability win.
  - **Files:** `src/simplify.rs`. **Tests:** golden strings for each fold; assert idempotence (`simplify(simplify(x)) == simplify(x)`). **Risk:** NaN/Inf handling — folding `Ln(Const(-1.0))` must produce a non-finite that doesn't poison surrounding logic.

- [x] **`LoweredOp::jacobian(n_vars)` and `LoweredOp::grad_all()`** (implemented 2026-04-27) — convenience + shared-subexpression batch gradient. `[medium]`
  - **Why:** Calling `grad(wrt)` in a loop recomputes shared subexpressions n times. Reverse-mode-style sharing is strictly faster and matches research-library expectations. Jacobian is the obvious wrapper.
  - **Design:** `pub fn jacobian(&self, n_vars: usize) -> Vec<LoweredOp>` is a thin wrapper that calls `grad_all`. `grad_all` performs one structural pass building a CSE-aware adjoint table keyed by structural hash, returning `Vec<LoweredOp>` of length `n_vars`. Reuse the existing `simplify` cache to deduplicate identical adjoint expressions across outputs. Document complexity: O(|tree|·n) worst case, often much better with CSE.
  - **Files:** `src/lower.rs`. **Tests:** Cross-check each Jacobian column against `grad(i)` and against finite differences for random expressions; assert `grad_all` is faster than the loop on a 100-node tree (perf smoke test, not strict bench). **Risk:** Subtle numerical drift if simplification orders differ from per-call `grad` — pin it via golden tests.

- [x] **Symbolic Hessian** (implemented 2026-04-27) — `LoweredOp::hessian(n_vars) -> Vec<Vec<LoweredOp>>` for second-order derivatives. `[small]`
  - **Why:** Newton-style optimization, curvature-based model selection, and physics applications all consume Hessians. Cheap to add once `jacobian` exists.
  - **Design:** `hessian` = jacobian of jacobian, exploiting Schwarz symmetry (`H[i][j] == H[j][i]`) to compute only the upper triangle and mirror. Each entry simplified.
  - **Files:** `src/lower.rs`. **Tests:** Symmetry check, central-difference cross-check on quadratic and trig benchmarks. **Risk:** Tree-size blow-up on deep expressions; document the O(n²·|tree|) growth and recommend `simplify` after each entry.

- [x] **Interval arithmetic on `LoweredOp`** (implemented 2026-04-27) — `LoweredOp::eval_interval(&[Interval]) -> Interval` for over-box evaluation. `[medium]`
  - **Why:** Today's `IntervalDomain` lives in `smt.rs` and operates on the EML tree level. Lifting it to `LoweredOp` (where named ops have tight monotonicity/convexity properties) tightens bounds substantially and unlocks reliable range analysis for the symbolic-regression scoring path (e.g. reject candidates whose output range cannot contain target observations).
  - **Design:** New `Interval { lo: f64, hi: f64 }` lightweight struct (or reuse the one in `smt.rs` if shape allows). Standard rounding-aware interval rules per op; transcendentals use monotone-region splits (e.g. `sin` over a box that crosses π/2). Generalize `IntervalDomain` so both consumers share the underlying ops.
  - **Files:** `src/lower.rs`, `src/smt.rs` (refactor shared), new `tests/interval_test.rs`.
  - **Tests:** Containment property (point eval ∈ interval eval) for random inputs; tight-bound check on monotone functions; SMT/interval cross-validation that the lowered-IR interval is no looser than the tree-level one.
  - **Risk:** Rounding-mode portability — `f64` rounding control is platform-flavoured; document that we use directed rounding only where available and conservative widening elsewhere.

- [x] **Noise-robust loss functions for symreg** (implemented 2026-04-27) — Huber and trimmed MSE alongside the current MSE objective. `[medium]`
  - **Why:** Real-world observational data has outliers. MSE alone gives outliers quadratic leverage and biases topology selection toward formulas that explain the noise. Huber and α-trimmed MSE are the standard fixes and don't require user-supplied noise models.
  - **Design:** New `enum SymRegLoss { Mse, Huber { delta: f64 }, TrimmedMse { alpha: f64 } }` exposed via `SymRegConfig.loss`. Adam optimizer differentiates Huber analytically (piecewise quadratic / linear); trimmed MSE drops the top `α·n` residuals before averaging. Pareto front uses the same configured loss for `mse` field but renames it to `loss` in the public API; keep an `mse` alias for one minor.
  - **Files:** `src/symreg.rs`, CLI flag `--loss huber:0.1` etc. in `src/bin/oxieml.rs`.
  - **Tests:** Synthetic data with a 10% outlier contamination; Huber/trimmed should recover the underlying formula at lower complexity than MSE.
  - **Risk:** Adam convergence with non-smooth trimmed loss can stall — use a smooth approximation (e.g. soft-trim via sigmoid weight) for the gradient step and the exact form for scoring.

- [x] **Constants extraction post-Adam** (implemented 2026-04-27) — round optimized scalars to π / e / simple rationals when MSE doesn't worsen by ε. `[medium]`
  - **Why:** Adam returns `2.99998…` for what is plainly `3` and `3.14159…` for what is plainly `π`. Reporting raw floats in published formulas is ugly and obscures the discovery. This is a high-perceived-quality win for almost no cost.
  - **Design:** After Adam termination, for each free constant try a candidate set `{0, ±1, ±1/2, ±1/3, ±1/4, ±π, ±e, ±√2, …, simple rationals via Stern-Brocot up to denominator 12}`. Accept the rounded value if the resulting MSE on the training set is within `(1 + ε)·current_mse` (default ε = 1e-3, configurable). Iterate constants left-to-right (greedy) — full combinatorial search is exponential. Mark rounded constants so `to_latex` can render `\pi` / `\frac{1}{2}` symbolically.
  - **Files:** `src/symreg.rs`, `src/lower.rs` (named-constant marker on `Const`).
  - **Tests:** Pendulum example should report `T = 2π√(L/g)` not `T = 6.2831·√(L/g)`; MSE-tolerance test ensures we never accept a worse fit.
  - **Risk:** Greedy rounding can get stuck — document and provide `--no-constant-rounding` escape hatch.

- [x] **Beam search topology exploration** (implemented 2026-04-27) — replace exhaustive enumeration with bounded beam search at depths > 4. `[medium]`
  - **Why:** Exhaustive enumeration is the right default at depth ≤ 4 (that's where it terminates in seconds) but is intractable at depth 5+ where most physically interesting formulas live. Beam search gives a tunable depth-vs-breadth tradeoff that's deterministic, parallel-friendly, and well-understood.
  - **Design:** New `enum SymRegStrategy { Exhaustive, Beam { width: usize } }` in `SymRegConfig`. Beam: at each depth d, score every candidate topology by a cheap surrogate (e.g. lowered-node-count + pre-fit residual after 5 Adam steps), keep top-`width`, expand only those. Use `IntervalDomain::eval_interval` to drop candidates whose output range can't span the target range. Beam runs inside the same parallel `par_iter` skeleton as exhaustive.
  - **Files:** `src/symreg.rs`, CLI `--strategy beam:64`.
  - **Tests:** Beam at width = ∞ matches exhaustive; beam at width = 1 is greedy and deterministic; depth-6 beam terminates within budget on Pendulum example.
  - **Risk:** Surrogate misranks — a topology that fits poorly at 5 Adam steps may shine at 200. Mitigation: warm-start the survivors longer in the final pass.

- [x] **RNG seed in `SymRegConfig`** (implemented 2026-04-27) — explicit `seed: Option<u64>` for fully reproducible runs. `[trivial]`
  - **Why:** Adam initialization, k-fold shuffle, and any future stochastic strategy all currently draw from `rand::thread_rng()`. Published research results must be reproducible — without a seed they aren't.
  - **Files:** `src/symreg.rs`. **Tests:** Two `discover()` calls with same seed produce byte-identical Pareto fronts. **Risk:** Parallel determinism with `rayon` — must use seeded per-topology RNGs derived from the master seed (e.g. `SplitMix64`), not a single shared RNG.

- [x] **CLI `--format` (pretty / latex / json) and `--output <file>`** (implemented 2026-04-27) — structured output for piping into LaTeX docs, notebooks, or downstream tools. `[small]`
  - **Why:** Today the CLI prints a fixed human-readable form. Researchers want LaTeX for papers, JSON for scripting, and writing to a file is necessary on Windows where `>` shell redirection is awkward.
  - **Design:** Add `--format pretty|latex|json` (default `pretty`) and `--output <path>`; JSON requires the `serde` feature. Apply uniformly to `--eval`, `--lower`, and `--symreg` subcommands.
  - **Files:** `src/bin/oxieml.rs`, `tests/cli_format_test.rs`. **Tests:** Each format on a known formula matches a golden string. **Risk:** None significant.

- [x] **Property-based grad tests via proptest** (implemented 2026-04-27) — random valid trees compared against central differences. `[small]`
  - **Why:** Existing 13 grad tests are hand-picked. proptest will surface adversarial expressions (near-singularities, deep nesting, mixed unary/binary chains) the suite doesn't cover.
  - **Design:** `proptest` strategy generating `LoweredOp` trees up to depth 6 with bounded constant range; for each, sample 5 random points, compare `grad(i).eval(point)` vs central difference, tolerance `max(1e-5·|expected|, 1e-7)`. Skip points where the function is non-differentiable (e.g. `|x|` at 0). Add to `tests/`.
  - **Files:** `Cargo.toml` (`proptest` dev-dep), `tests/grad_proptest.rs`.
  - **Risk:** Flaky tests due to numerical edge cases — pin `cases = 1024`, persist failed seeds, document tolerance.

- [x] **Multi-output symbolic regression** (implemented 2026-04-27) — `discover_multi(features, targets: Array2)` returning vector-valued formulas. `[medium]`
  - **Why:** Many physics problems are multi-output (position + velocity, Lorenz system, etc.). The scalar-output API forces users into N independent runs that miss shared structure.
  - **Design:** Add `SymRegEngine::discover_multi(features, targets) -> Vec<Vec<DiscoveredFormula>>`. Two strategies behind `SymRegConfig.multi_output`: (a) **independent** — N parallel scalar runs (cheap, no sharing); (b) **shared-topology** — co-evolve topologies and have each output use its own constants only (forces a common functional skeleton, useful when outputs are physically related). Pareto front per output.
  - **Files:** `src/symreg.rs`, `src/scirs2.rs` (ndarray adapter).
  - **Tests:** Synthetic Lorenz dataset; independent matches three single-output runs; shared-topology recovers the structural similarity.
  - **Risk:** Shared-topology mode dramatically raises search cost — keep `independent` as default.

- [x] **Python bindings via PyO3** (implemented 2026-04-27) (feature `python`) — expose `EmlTree`, `LoweredOp`, `SymRegEngine` to Python with maturin packaging. `[large]`
  - **Why:** Python is the lingua franca of scientific computing; without it, OxiEML is invisible to the SciRS2 + NumRS2 user base and to the broader symbolic-regression community (PySR, gplearn, etc.). High distribution leverage.
  - **Design:** New `python` feature, `Cargo.toml` adds `pyo3` (latest, `extension-module` feature) under that gate. New `src/python.rs` exporting `PyEmlTree`, `PyLoweredOp`, `PySymRegEngine`, `PySymRegConfig`, `PyDiscoveredFormula`. Use `numpy` crate for `ndarray::Array2 ↔ numpy.ndarray` zero-copy interop. Ship `pyproject.toml` + `pypi-publish.yml` (allowed by COOLJAPAN policy). Wheels built via maturin on `manylinux2014`, `macos-arm64`, `windows`. No GIL release on the hot loop initially — measure first.
  - **Files:** `Cargo.toml`, `src/python.rs`, `pyproject.toml`, `.github/workflows/pypi-publish.yml`, `python/oxieml/__init__.py`, `python/tests/test_basic.py`.
  - **Tests:** Python-side pytest suite mirroring the Rust integration tests; CI builds wheels for all three platforms.
  - **Risk:** Build-system complexity (maturin + multi-platform wheels), CPython ABI churn between minor versions. Mitigation: pin `abi3-py39` for forward compatibility, gate any non-`abi3` features.

- [x] **Constraint-guided pruning in symreg via `EmlSmtSolver`** (implemented 2026-04-27) — drop topologies that cannot fit the training domain (UNSAT). `[research]`
  - **Why:** OxiEML uniquely has both a symreg engine and an SMT solver in the same crate. Using interval/SMT to prove `∀x ∈ training_box, f(x) ≠ y(x)` for a candidate topology lets us drop entire branches before paying for Adam fitting. This is a real research angle nobody else can run.
  - **Design:** Before optimization, abstract each topology to its `LoweredOp` skeleton with constants treated as free variables. Encode `∃c. ∀(x,y) ∈ training. |f(x; c) − y| ≤ ε` as an SMT query over the constants; if UNSAT, skip. Use the new `LoweredOp::eval_interval` for cheap pre-filtering before the expensive SMT call. Threshold: only invoke SMT when interval-only filtering is inconclusive.
  - **Files:** `src/symreg.rs`, `src/smt.rs`. **Tests:** Synthetic dataset where half the topology space is provably infeasible; pruning reduces fit-time by ≥ 30% with no quality loss. **Risk:** SMT call cost can exceed Adam fit cost on small topologies — gate behind `SymRegConfig.smt_pruning: bool` (default false) and a depth threshold.

---

## Future: Research Directions

- [x] **ODE / PDE discovery (SINDy-style)** — given a trajectory `x(t)`, discover `f` such that `dx/dt = f(x)`. `[research]` (implemented 2026-04-27)
  - Differentiate the trajectory numerically (Savitzky-Golay or central differences), feed `(x_i, ẋ_i)` pairs into the symreg engine. Multi-output mode handles vector ODEs. Extension to PDEs requires a discretization story (method-of-lines on a grid). Open questions: noise robustness, sparsity-promoting regularizers, conserved-quantity constraints encoded via SMT.

- [x] **Dimensional analysis / unit-aware regression** — annotate variables with SI units; reject formulas that violate unit consistency. `[research]` (implemented 2026-04-28)
  - Ship a small `Units` algebra (length, time, mass, …) as exponent vectors. Each `LoweredOp` carries a unit signature; `Add`/`Sub` require unit equality, `exp`/`ln` require dimensionless argument, `Pow` requires rational exponent for non-dimensionless base. Integrates with symreg as a hard pruning filter — entire topology branches drop if they're dimensionally inadmissible. This is a 10-100× search-space reduction on physics problems and produces formulas that are unit-checked by construction.

- [x] **JIT compilation of `OxiOp` sequences via cranelift** — pure-Rust JIT for hot evaluation paths. `[research]` (implemented 2026-04-28)
  - Cranelift is pure Rust and a natural fit. Generate IR from the post-order `OxiOp` sequence; emit machine code at first call, cache by structural hash. Expected win: 5-20× over the interpreter on long batches, beating even SIMD on irregular workloads. Risk: cranelift is large; gate behind a `jit` feature so default builds stay lean. Cross-platform parity (aarch64, x86_64, riscv64) needs validation.
  - Implemented: `src/jit.rs` with `JitFn::compile` (OxiOp→Cranelift IR→native code) and `JitCache` (FNV-1a hash keyed LRU-less cache, Mutex-guarded). All 22 OxiOp variants handled; transcendental functions use extern C bindings to libm. 13 integration tests in `tests/jit_test.rs` covering const, vars, arithmetic, exp, sin, cos, neg, div, pow, complex, cache parity, hash stability, and empty-ops error. 0 warnings, 429/429 tests pass.

- [x] **MCTS topology search** — Monte-Carlo tree search over the topology space. `[research]` (implemented 2026-04-28)
  - Beam search is deterministic and breadth-limited; MCTS adds exploration via UCB1 over partially-built trees. State = partial EML tree, action = expand a leaf, value = achieved fit MSE after a short Adam fit. Prior work (DSO, AlphaSymPy) shows promising results. OxiEML angle: combine MCTS rollout pruning with our SMT/interval constraint propagation — a unique combination.
  - Implemented: `src/symreg/mcts.rs` (508 lines) with `PartialNode` recursive enum (Hole/One/Var/Eml), UCB1 selection, leftmost-HOLE expansion, random rollout completion, `1/(1+MSE)` reward. `SymRegStrategy::Mcts { iterations, exploration }` variant added; dispatch via `discover_mcts` bridge in `mod.rs`. Interval pruning hook integrated. 5 integration tests in `tests/symreg_mcts_test.rs`. 434/434 tests pass, 0 clippy warnings.

- [x] **Symbolic equation solving** — given `f(x) = g(y)`, derive `y = h(x)` when invertible. `[research]` (implemented 2026-04-27)
  - Builds on `canonical_rewrite_rules`. For each operator that has a known inverse on its monotone region (`exp`/`ln`, `sin`/`arcsin` with branch cuts, `pow` with appropriate domain), implement an `invert(target_var)` pass. Returns either a closed-form solution or a residual `f − g` for numeric solving. Useful for closing the loop on discovered formulas (solve for any variable).

- [x] **WASM target + npm package** — `wasm32-unknown-unknown` build with a TypeScript-typed JS API. `[research]` (implemented 2026-04-27)
  - Browser-deployable symbolic regression has obvious educational and demo value (live formula discovery in a notebook UI). Pure-Rust default features make this tractable; SIMD requires `wasm32-bleeding-edge`-level toolchain support. Ship via `npm-publish.yml` (allowed). Open question: does the symreg search complete in interactive time on WASM, or do we need to expose async / web-worker hooks?
  - Implemented via `src/wasm.rs` behind `#[cfg(feature = "wasm")]`; exposes `WasmSymRegConfig`, `WasmDiscoveredFormula`, `WasmSymRegEngine` to JS/TS via `wasm-bindgen = 0.2.118`. `package.json` provides `wasm-pack` build scripts for bundler/node/web targets. CI via `.github/workflows/npm-publish.yml`.

---

## Non-goals

- Compiling full pre-lowering EML trees to einsum — the uniform binary tree is too deep and repetitive for efficient tensor contraction.
- Replacing OxiEML's own simplify/lower pipeline with TensorLogic's compiler.
- Running EML evaluation through the TensorLogic executor.
- Depending on any TensorLogic crate that transitively pulls in SciRS2 (`tensorlogic-compiler` / `-scirs-backend` / `-train`).
- C / Fortran in default features — Pure Rust Policy. C/Fortran-bearing dependencies allowed only behind explicit feature gates.
- `f32` numeric precision — OxiEML targets scientific/research workloads where `f64` is the floor. Not in scope unless a concrete user demands it.
- `bincode`, `flate2`, `zstd`, `zip`, `rustfft`, `Z3`, `openblas`, or any non-OxiOxiZ/OxiBLAS/OxiFFT/OxiARC/oxicode equivalent — COOLJAPAN policy, no exceptions.
- C FFI surface — Python via PyO3 (Upcoming) and WASM (Future) cover external embedding needs.
- `unwrap()` in production code — No-unwrap policy.
