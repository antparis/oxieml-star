# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-05-03

### Added

- Trig precision: `src/lower.rs` now detects the canonical `Canonical::sin(x)`
  and `Canonical::cos(x)` EML tree shapes and lowers them directly to
  `LoweredOp::Sin(x)` / `LoweredOp::Cos(x)`, giving 0.0 error vs `f64::sin`/
  `f64::cos` on canonical trig trees.
- `EmlTree::eval_real_lowered(&EvalCtx) -> Result<f64, EmlError>` convenience
  that routes through lowering → pattern recognition → `LoweredOp::Sin`/`Cos`
  → `f64::sin`/`cos` precision.
- `LoweredOp::grad(wrt: usize) -> LoweredOp` symbolic differentiation with
  chain, product, quotient, and general `Pow(base, expo)` (via exp-log) rules.
  Result is `.simplify()`'d for clean pretty-printing. 13 cross-check tests
  against central-difference numerical derivatives in
  `tests/lowered_grad_test.rs`.
- Optional `tensorlogic` feature gated on `tensorlogic-ir`. Exposes
  `to_tlexpr(&LoweredOp) -> TLExpr`,
  `from_tlexpr(&TLExpr) -> Result<LoweredOp, EmlError>`, and
  `canonical_simplify(&TLExpr) -> TLExpr` (algebraic identities + const
  folding). `Neg(x)` lowers to `Sub(Const(0), x)` since `TLExpr` has no unary
  negation. `canonical_rewrite_rules()` is a stub returning `vec![]` pending
  upstream `Pattern` enum extension in `tensorlogic-ir`.
- `EmlError::UnsupportedTlExpr(String)` variant (feature-gated) for
  non-arithmetic `TLExpr` nodes encountered during conversion.
- CLI: `--grad`/`-d <wrt>` subcommand in `src/bin/oxieml.rs` that parses an
  EML expression, lowers it, and prints both the expression and its symbolic
  derivative with respect to `x{wrt}`.
- Symbolic regression examples: `examples/physics_pipeline.rs` (projectile
  motion, 3-var end-to-end symreg → compile → batch eval),
  `examples/pendulum.rs` (T = 2π√(L/g), 1-var), and
  `examples/harmonic_oscillator.rs` (x(t) = A·cos(ωt), 3-var).
- `benches/trig_bench.rs` criterion benchmarks comparing `eval_real` (raw
  tree walk) vs `eval_real_lowered` (lowered stack-machine) for sin/cos/exp/
  composite on 1000 points each.
- 13 symbolic-gradient tests in `tests/lowered_grad_test.rs`, 13 trig
  precision tests in `tests/trig_precision_test.rs`, and 8 TensorLogic
  bridge tests in `tests/tensorlogic_test.rs`.
- CLI `--symreg` / `-s` subcommand: runs `SymRegEngine::discover` on
  whitespace-separated data from stdin or `--file` and prints top-K
  ranked formulas with MSE, complexity, and score. Supports forwarding
  flags for every `SymRegConfig` field (`--max-depth`, `--max-iter`,
  `--learning-rate`, `--tolerance`, `--complexity-penalty`,
  `--num-restarts`) plus `--vars` and `--top`. Integration tests in
  `tests/cli_symreg_test.rs` via `assert_cmd` + `predicates`
  (new `[dev-dependencies]`).
- `SymRegConfig::quick()`, `::balanced()`, `::exhaustive()` ergonomic
  preset constructors. `balanced()` aliases `Default::default()`;
  `quick()` shortens search for fast iteration; `exhaustive()` deepens
  for publication-quality runs.

### Changed

- Bumped version 0.1.0 → 0.1.1 (branch-driven).
- `LoweredOp::simplify` now handles Sin/Cos/Exp/Ln constant folding (guarded
  for finite ln arg and positive domain), `Mul(Const(-1), x) → Neg(x)`,
  `Add(a, Neg(b)) → Sub(a, b)`, `Sub(a, Neg(b)) → Add(a, b)`,
  `Neg(Sub(a, b)) → Sub(b, a)`, and guards `Pow(Const(b), Const(e))` folding
  against non-finite results.
- `src/bin/oxieml.rs` now dispatches to `run_grad()` when `--grad`/`-d` is
  supplied; default path remains the evaluator.
- `canonical_rewrite_rules()` rustdoc now explains why the function
  returns `vec![]` (upstream `tensorlogic_ir::Pattern` lacks arithmetic
  variants), lists the rules that will emit once that blocker clears,
  and points to `canonical_simplify` as the current workaround.

### Internal

- `EvalCtx::as_slice() -> &[f64]` accessor for SIMD / batch evaluators.

### Notes

- No SciRS2 integration in this release; deferred pending OxiEML's final
  crate-placement decision.

## [0.1.0] - 2026-04-14

### Added
- EML operator `eml(x, y) = exp(x) - ln(y)` implementation
- Uniform binary tree representation for all elementary functions
- Tree evaluation: real (`eval_real`) and complex (`eval_complex`) modes
- Batch evaluation with optional SIMD acceleration (`simd` feature)
- Parallel batch evaluation (`parallel` feature via rayon)
- Expression simplification and normalization
- Canonical form derivations (exp, ln, neg, add, sub, mul, div, pow, sqrt, abs, trig, hyperbolic, inverse trig/hyperbolic)
- Symbolic differentiation (gradient computation)
- Expression compiler with lowered IR for fast evaluation
- S-expression parser supporting `E(...)` and `eml(...)` notation
- SMT constraint solving via OxiZ (`smt` feature)
- Symbolic regression engine for discovering EML formulas from data
- CLI tool (`oxieml`) with eval, simplify, lower, grad, parse, symreg, and smt commands
- Comprehensive test suite (173 tests)
- Criterion benchmarks for evaluation and symbolic regression
