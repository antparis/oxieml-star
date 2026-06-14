[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20152989.svg)](https://doi.org/10.5281/zenodo.20152989)

# OxiEML-Star

**All elementary functions from a single binary operator — now with anti-holomorphic support.**

A Pure Rust crate that implements the EML operator `eml(x, y) = exp(x) - ln(y)`
and builds uniform binary trees expressing **all elementary functions** using only
this operator and the constant `1`.

Based on [arXiv:2603.21852](https://arxiv.org/abs/2603.21852) — *"All elementary
functions from a single binary operator"* by Andrzej Odrzywolek (Jagiellonian
University, Institute of Theoretical Physics).

## Key Capabilities

1. **Uniform Tree Representation** — Every elementary function (exp, ln, sin, cos,
   +, -, *, /, ^, sqrt, abs, ...) is expressed via the grammar `S -> 1 | eml(S, S)`.

2. **Symbolic Regression** — Discover closed-form mathematical formulas from
   input/output data using gradient-based search over EML tree topologies.

3. **Lowering & Code Generation** — Convert discovered EML trees to standard
   operation trees for efficient evaluation, pretty-printing, and Rust code emission.

4. **CLI Tool** — Parse, evaluate, and generate EML expressions from the command line.

5. **SMT Integration** — Constraint solving via EML tree interval narrowing
   (feature-gated for oxiz integration).

6. **Gradient / Jacobian / Hessian** — Symbolic differentiation on `LoweredOp` with
   `LoweredOp::grad(wrt)`, `grad_all()`, `jacobian(n)`, `hessian(n)`.

## eml★ Extension (Monnerot 2026)

This fork adds the companion operator `eml★(x, y) = exp(x) - ln(conj(y))`,
which extends the EML grammar to cover **anti-holomorphic** functions.

**Extended grammar:** `S → 1 | eml(S, S) | eml★(S, S)`

Two operators and one constant generate **all** elementary functions — holomorphic
and anti-holomorphic — including:

- `conj(z)` at depth 2 (Theorem 3.1, valid for Im(z) ∈ [-π, π))
- `Re(z)`, `Im(z)`, `|z|²`, `|z|`
- Conformal primary wavefunctions for 2D CFT

To our knowledge, no prior symbolic regression framework covers
anti-holomorphic function spaces via a dedicated operator; eml★
is introduced for this purpose.

### Canonical constructions

```rust
use oxieml_star::canonical::Canonical;

let z = EmlTree::var(0);
let conj_z = Canonical::conj(&z);          // conj(z) at depth 2
let re_z = Canonical::real_part(&z);       // Re(z) at depth 3
let mod_sq = Canonical::mod_squared(&z);   // |z|² at depth 3
```

### Reference

Monnerot, A. (2026). *eml★: Minimal Anti-Holomorphic Extension of the EML Sheffer Operator*.
DOI: [10.5281/zenodo.20091022](https://doi.org/10.5281/zenodo.20091022)
GitHub: [antparis/eml_star](https://github.com/antparis/eml_star)



---

## Application: Galaxy Rotation Curves (May 2026)

The eml★ framework was applied to real astrophysical data — galaxy rotation curves — demonstrating its first empirical application.

### What we found

Using genetic programming (PySR + DEAP) with eml★ operators on **125 SPARC galaxies** and **23 LITTLE THINGS dwarf galaxies**:

1. **eml★ is a non-holomorphicity detector** — 0/10 false positives on holomorphic functions, 10/10 detection on anti-holomorphic functions.
2. **Low-luminosity galaxies need anti-holomorphic terms** — Spearman rho = -0.27, p = 0.004.
3. **Signal replicates independently** — 43.5% on LITTLE THINGS, consistent with SPARC.
4. **MOND and dark matter fraction ruled out** as predictors (p = 0.35 and p = 0.81).

### Tools

| Tool | Description |
|------|-------------|
| `discover_gp.py` | GP engine (DEAP) with eml★ operators |
| `pysr_complex_wrapper.py` | PySR (Julia) wrapper for high-power batch runs |
| `meta_analysis.py` | Statistical analysis + Plotly dashboard |
| `formula_translator.py` | GP formulas to LaTeX |
| `galaxy_analysis.py` | 9-panel per-galaxy diagnostics |
| `make_3d_viz.py` | 3D interactive visualization |

### Galaxy Paper

[**eml★ galaxy rotation curves paper (PDF)**](eml_star_galaxy_paper.pdf) — "Symbolic regression with anti-holomorphic operators reveals non-holomorphic structure in low-luminosity galaxy rotation curves"

### Interactive Demo

[**eml★ Interactive Explorer**](https://antparis.github.io/oxieml-star/emlstar_explorer.html) — Try eml★ operators in your browser (3D visualization, no installation needed).

### Paper

[Draft on GitHub](https://github.com/antparis/oxieml-star/blob/master/eml_star_paper_draft3.md) |
[eml★ theory on Zenodo (DOI: 10.5281/zenodo.20091022)](https://zenodo.org/records/20091023)

## Related Work

- **OxiEML** (COOLJAPAN OU, 2026): The original EML operator implementation in Rust.
  [cool-japan/oxieml](https://github.com/cool-japan/oxieml)
- **Odrzywołek (2026)**: "All elementary functions from a single binary operator."
  [arXiv:2603.21852](https://arxiv.org/abs/2603.21852)
- **Complex Equation Learner** (Garmaev et al., EPFL, 2026): Gradient-based symbolic
  regression with complex weights to bypass real-axis singularities.
  [arXiv:2605.03841](https://arxiv.org/abs/2605.03841)
  Note: CEQL uses complex weights for optimization stability but does NOT include
  complex conjugation as a primitive operator. OxiEML-Star fills this gap with eml★.
- **Zwegers (2002)**: Mock theta functions and harmonic Maass forms — the mathematical
  framework where eml★'s anti-holomorphic capabilities are directly applicable.

## Verification Summary

- **Pipeline calibrated** end-to-end (PySR discoverer -> SymPy Wirtinger judge), validated on known holo/anti targets and negative (shuffle) controls.
- **Kirsch elasticity** [ESTABLISHED]: anti-holomorphic structure forced by physics (traction-free boundary), judge-certified, MSE 3e-31.
- **Structural no-go** [ESTABLISHED]: genuine forced-transcendental-physical anti-holomorphy is closed on three fronts (mirror / repackaging / Vekua-Balk); the "chiral cell" is empty and explained, conditional on ellipticity.
- **CP front** [ESTABLISHED]: generalized-CP judge (Stages 1-2, Dirac+Majorana); Delta(54) type-I and Bora gCP-admissibility certified in GAP.
- Several systems were calibrations or returned negative/invalidated results (EHT, VLA, KiDS, Aharonov-Bohm, gravitational waves) -- traced honestly in RESEARCH_LOG.md.
- **Ramanujan**: mock theta functions (order 3, 5) computed; the raw mock theta series is HOLOMORPHIC (judge-verified, df/dzbar=0). The anti-holomorphic structure lives in the modular completion (Zwegers shadow), which is NOT yet tested. Shadow/completion test PENDING.

### Credits

Original OxiEML by **COOLJAPAN OU** ([cool-japan/oxieml](https://github.com/cool-japan/oxieml)).
eml★ extension by **Anthony Monnerot**.

7. **Extended Transcendentals** — `LoweredOp` has `Tan`, `Sinh`, `Cosh`, `Tanh`,
   `Arcsin`, `Arccos`, `Arctan`, `Arcsinh`, `Arccosh`, `Arctanh` with canonical EML
   shape recognition.

8. **Interval Arithmetic** — `LoweredOp::eval_interval` for range analysis and
   symreg pruning.

9. **JIT Compilation** — Cranelift-based JIT for hot evaluation paths (feature: `jit`).

10. **ODE Discovery** — SINDy-style ODE/PDE discovery from trajectory data
    (`SymRegEngine::discover_ode`).

11. **Multi-output Symbolic Regression** — `SymRegEngine::discover_multi` for
    vector-valued formulas.

12. **Dimensional Analysis** — SI unit-aware regression with `Units` algebra; rejects
    dimensionally-inconsistent formulas.

13. **Python Bindings** — PyO3-based Python bindings via maturin (feature: `python`).

14. **WASM Bindings** — wasm-bindgen target with npm package `@cool-japan/oxieml`
    (feature: `wasm`).

15. **Noise-Robust Loss** — Huber and TrimmedMSE loss functions (`SymRegLoss` enum).

16. **Constants Extraction** — Post-Adam rounding of floats to π, e, simple rationals.

17. **Beam Search** — `SymRegStrategy::Beam{width}` for depth > 4 topology exploration.

18. **MCTS Search** — Monte Carlo Tree Search topology exploration (`symreg/mcts.rs`).

19. **Serde Serialization** — JSON + oxicode binary for `EmlTree`/`LoweredOp`/
    `DiscoveredFormula` (feature: `serde`).

20. **TensorLogic Integration** — Bidirectional `LoweredOp ↔ TLExpr` mapping + soft-prior
    export (feature: `tensorlogic`).

21. **SciRS2 Integration** — ndarray adapter (feature: `scirs2`).

## CLI Tool

The `oxieml` CLI can evaluate EML expressions, generate EML from function names,
and verify claims about mathematical constants.

```bash
# Evaluate an EML expression
oxieml "E(1, 1)"
#=> MATCH: e (Euler's number) = 2.718281828459045

# Generate EML from a function/constant name
oxieml -g pi
#=> E(1,E(E(1,E(E(1,E(E(1,E(1,E(1,1))),1)),E(E(1,1),1))),1))
#=> MATCH: Im ~ pi (diff = 0.00e0)

oxieml -g e
#=> E(1,1)

oxieml -g sin x0=0.5
#=> Result: 0.4794255386042034

# Evaluate with variables
oxieml "E(x0, 1)" x0=2.0
#=> Result: 7.38905609893065  (= exp(2))

# Read from file
oxieml --file expression.txt

# List all available functions and constants
oxieml -l

# Show help / version
oxieml --help
oxieml --version
```

If the input is not a valid EML expression, the CLI auto-detects function names:

```bash
oxieml pi          # same as: oxieml -g pi
oxieml sin         # generates sin(x0) template
```

## Quick Start (Library)

```rust
use oxieml::{EmlTree, Canonical, EvalCtx};

// Build exp(x) = eml(x, 1)
let x = EmlTree::var(0);
let exp_x = Canonical::exp(&x);

// Evaluate at x = 1.0 -> e
let ctx = EvalCtx::new(&[1.0]);
let result = exp_x.eval_real(&ctx).unwrap();
assert!((result - std::f64::consts::E).abs() < 1e-10);

// Euler's number: eml(1, 1) = exp(1) - ln(1) = e
let e = Canonical::euler();
println!("{}", e); // "eml(1, 1)"

// Negation, addition, multiplication — all from eml and 1
let y = EmlTree::var(1);
let sum = Canonical::add(&x, &y);
let product = Canonical::mul(&x, &y);

// Lower to standard operations for efficient evaluation
let lowered = exp_x.lower();
println!("{}", lowered.to_pretty()); // "exp(x0)"
let fast_result = lowered.eval(&[1.0]);

// Generate Rust source code
let code = oxieml::compile::compile_to_rust(&exp_x, "my_exp");
println!("{code}");
```

## Parser

Parse EML expressions from strings and convert back:

```rust
use oxieml::parser::{parse, to_compact_string};

// Parse E(x, y) notation
let tree = parse("E(E(1, 1), 1)").unwrap();
assert_eq!(tree.depth(), 2);

// Also accepts eml(x, y) notation
let tree = parse("eml(E(1, x0), 1)").unwrap();

// Convert back to compact string
let compact = to_compact_string(&tree);
assert_eq!(parse(&compact).unwrap(), tree); // roundtrip
```

## Symbolic Regression

```rust
use oxieml::symreg::{SymRegConfig, SymRegEngine};

// Generate data from an unknown function
let inputs: Vec<Vec<f64>> = (0..50).map(|i| vec![i as f64 * 0.1]).collect();
let targets: Vec<f64> = inputs.iter().map(|x| x[0].exp()).collect();

let config = SymRegConfig {
    max_depth: 2,
    learning_rate: 1e-2,
    tolerance: 1e-8,
    ..Default::default()
};

let engine = SymRegEngine::new(config);
let formulas = engine.discover(&inputs, &targets, 1).unwrap();

println!("Best formula: {}", formulas[0].pretty);
println!("MSE: {:.2e}", formulas[0].mse);
```

## SMT / Constraint Solving

With the `smt` feature, oxieml integrates [OxiZ](https://crates.io/crates/oxiz) 0.2
as a backend for deciding EML constraints. The solver uses **interval propagation**
(EML-aware forward/backward rules for exp/ln) followed by **linear relaxation**
(secant + tangent bounds) for OxiZ's LRA theory.

```rust,ignore
use oxieml::{EmlTree, Canonical, EmlConstraint, EmlSmtSolver, SmtResult};

// Constraint: exp(x) > 0 — trivially true for all x
let x = EmlTree::var(0);
let one = EmlTree::one();
let exp_x = EmlTree::eml(&x, &one);
let c = EmlConstraint::GtZero(exp_x);

let solver = EmlSmtSolver::new(vec![(-10.0, 10.0)]);
match solver.check_sat(&c).unwrap() {
    SmtResult::Sat(sol) => println!("SAT: x = {}", sol.assignments[0]),
    SmtResult::Unsat => println!("UNSAT — impossible"),
    SmtResult::Unknown => println!("unknown"),
}
```

The `EmlSmtSolver` can prove **UNSAT** for cases the legacy `EmlNraSolver`
(interval bisection) cannot — e.g., `ln(x) > 0` with `x ∈ [-2, -1]` (ln
undefined for non-positive reals). It falls back to bisection on OxiZ-tightened
bounds to extract concrete SAT witnesses, since extracting real-valued models
from OxiZ 0.2 is not yet ergonomic.

Enable with:

```toml
[dependencies]
oxieml = { version = "0.1", features = ["smt"] }
```

The `IntervalDomain` type is always available (no feature) for lightweight
propagation use-cases.

## What's New in v0.1.1

Released 2026-05-03.

- Symbolic gradient, Jacobian, and Hessian on `LoweredOp`
- Extended transcendentals in `LoweredOp` (`Tan`, `Sinh`, `Cosh`, `Tanh`, `Arcsin`,
  `Arccos`, `Arctan`, `Arcsinh`, `Arccosh`, `Arctanh`)
- Interval arithmetic on `LoweredOp` for domain analysis and symreg pruning
- Noise-robust loss (`Huber`, `TrimmedMSE`) and constants extraction (π, e, rationals)
- Beam search and MCTS topology strategies for depth > 4
- ODE/PDE discovery via `SymRegEngine::discover_ode`
- Multi-output symbolic regression via `SymRegEngine::discover_multi`
- Dimensional analysis: SI unit-aware regression with hard pruning
- JIT compilation (Cranelift, `jit` feature): 5–20× speedup on long batches
- Serde serialization for all types (`serde` feature)
- Python bindings (`python` feature, maturin-packaged)
- WASM bindings (`wasm` feature, npm: `@cool-japan/oxieml`)
- TensorLogic integration (`tensorlogic` feature): soft-prior export
- SciRS2 integration (`scirs2` feature): ndarray adapters
- Constraint-guided symreg pruning via `EmlSmtSolver` (UNSAT-prune topologies)
- CLI: `--grad`/`-d`, `--symreg`/`-s`, `--format`, `--output`, `--strategy` flags

## Canonical Constructions (Complete Phylogenetic Tree)

All functions from the paper's phylogenetic tree (Figure 1) are implemented:

### Table 1: Basic Operations

| Function    | EML Construction               | Depth |
|-------------|--------------------------------|-------|
| `exp(x)`    | `eml(x, 1)`                   | 1     |
| `e`         | `eml(1, 1)`                   | 1     |
| `ln(x)`     | `eml(1, eml(eml(1, x), 1))`   | 3     |
| `-x`        | via `(e-x) - e` composition   | 6     |
| `0`         | `ln(1)`                        | 3     |

### Table 2: Arithmetic

| Function    | EML Construction               | Depth |
|-------------|--------------------------------|-------|
| `x + y`     | `sub(x, neg(y))`              | ~12   |
| `x - y`     | `eml(ln(x), eml(y, 1))`       | ~7    |
| `x * y`     | `exp(ln(x) + ln(y))`          | ~14   |
| `x / y`     | `exp(ln(x) - ln(y))`          | ~14   |
| `x ^ y`     | `exp(y * ln(x))`              | ~18   |
| `1/x`       | `exp(-ln(x))`                 | ~10   |
| `x^2`       | `pow(x, 2)`                   | deep  |

### Table 3: Trigonometric

| Function      | EML Construction                       | Depth |
|---------------|----------------------------------------|-------|
| `pi` (iπ)     | `ln(-1)` in complex domain            | 9     |
| `sin(x)`      | `(exp(ix) - exp(-ix)) / 2i`           | ~52   |
| `cos(x)`      | `(exp(ix) + exp(-ix)) / 2`            | ~52   |
| `tan(x)`      | `sin(x) / cos(x)`                     | deep  |

### Table 4: Inverse Trigonometric

| Function      | EML Construction                              |
|---------------|-----------------------------------------------|
| `arcsin(x)`   | `-i * ln(ix + sqrt(1 - x^2))`                |
| `arccos(x)`   | `-i * ln(x + i * sqrt(1 - x^2))`             |
| `arctan(x)`   | `(-i/2) * ln((1 + ix) / (1 - ix))`           |

### Table 5: Hyperbolic

| Function    | EML Construction                |
|-------------|---------------------------------|
| `sinh(x)`   | `(exp(x) - exp(-x)) / 2`      |
| `cosh(x)`   | `(exp(x) + exp(-x)) / 2`      |
| `tanh(x)`   | `sinh(x) / cosh(x)`           |

### Table 6: Inverse Hyperbolic

| Function      | EML Construction                        |
|---------------|-----------------------------------------|
| `arcsinh(x)`  | `ln(x + sqrt(x^2 + 1))`               |
| `arccosh(x)`  | `ln(x + sqrt(x^2 - 1))`               |
| `arctanh(x)`  | `(1/2) * ln((1 + x) / (1 - x))`       |

### Table 7: Other Functions & Constants

| Function    | EML Construction         |
|-------------|--------------------------|
| `sqrt(x)`   | `x^0.5`                 |
| `abs(x)`    | `sqrt(x^2)`             |
| `nat(n)`    | `1 + 1 + ... + 1`       |
| `-1`        | `neg(1)`                |
| `-2`        | `neg(nat(2))`           |
| `i`         | `exp(iπ/2)`             |

## Architecture

```
Discovery Phase              Execution Phase
─────────────────           ──────────────────
EML tree space     lower()  Standard ops
S -> 1 | eml(S,S) -------> Add/Sub/Mul/Exp/Ln...
     |                           |
     | Adam optimizer            | to_pretty()
     | (symreg)                  | compile_to_rust()
     |                           | eval()
  DiscoveredFormula         Fast evaluation

     parse()                to_compact_string()
"E(1,1)" -----> EmlTree ---------> "E(1,1)"
                   |
                   | -g pi / -g sin
                   |
              CLI evaluation & constant matching
```

## Module Overview

| Module           | Purpose |
|------------------|---------|
| `tree`           | `EmlNode`/`EmlTree` — Arc-shared uniform binary trees |
| `eval`           | Stack-machine evaluation (real, complex, batch) |
| `grad`           | Automatic differentiation for parameter optimization |
| `canonical`      | Complete phylogenetic tree: 30+ elementary functions |
| `parser`         | Parse `E(x,y)` / `eml(x,y)` notation, roundtrip |
| `simplify`       | EML tree algebraic simplification + CSE + constant folding |
| `lower`          | EML → standard operation trees + pretty-print |
| `lower_grad`     | Symbolic differentiation on `LoweredOp` (grad, Jacobian, Hessian) |
| `lower_simplify` | Simplification rules on `LoweredOp` (constant folding, algebraic) |
| `lower_interval` | Interval arithmetic on `LoweredOp` for range analysis |
| `lower_units`    | SI unit inference and dimensional consistency checking |
| `named_const`    | Named constant detection (π, e, √2, rationals) post-Adam |
| `compile`        | EML → Rust source code generation (scalar, batch, closure) |
| `symreg`         | Symbolic regression engine (topology enum + Adam + beam + MCTS) |
| `symreg/topology`| Topology enumeration and semantic deduplication |
| `symreg/mcts`    | Monte Carlo Tree Search topology exploration |
| `symreg/numerics`| Adam optimizer, k-fold CV, noise-robust loss functions |
| `symreg/constants`| Post-Adam constant extraction and rounding |
| `smt`            | [feature: smt] Constraint solving (interval propagation + OxiZ LRA) |
| `simd_eval`      | [feature: simd] SIMD batch evaluation via oxiblas-core |
| `jit`            | [feature: jit] Cranelift JIT for OxiOp sequences |
| `tensorlogic`    | [feature: tensorlogic] Bidirectional `LoweredOp ↔ TLExpr` |
| `scirs2`         | [feature: scirs2] ndarray adapter for SciRS2 integration |
| `python`         | [feature: python] PyO3 bindings for Python |
| `wasm`           | [feature: wasm] wasm-bindgen bindings for browser/Node.js |
| `units`          | SI unit algebra (7-exponent vector, `Units` struct) |
| `solve`          | Symbolic equation solving |
| `error`          | Error types |

## Features

```toml
[dependencies]
oxieml = { version = "0.1", features = ["smt", "simd", "parallel"] }
```

| Feature        | Description |
|----------------|-------------|
| `smt`          | OxiZ SMT backend + interval propagation + NRA solver |
| `simd`         | SIMD batch evaluation via oxiblas-core (aarch64 + x86_64) |
| `parallel`     | Rayon parallel batch evaluation |
| `tensorlogic`  | Bidirectional `LoweredOp ↔ TLExpr` bridge |
| `scirs2`       | ndarray `Array2`/`Array1` adapters for SciRS2 workflows |
| `serde`        | JSON + oxicode binary serialization for all types |
| `python`       | PyO3 Python bindings (use `python-extension` for `.so`) |
| `wasm`         | wasm-bindgen WASM bindings for browser/Node.js |
| `jit`          | Cranelift JIT compiler for hot OxiOp sequences |

Combine `simd,parallel` for SIMD-per-worker batch evaluation.

## Performance

Measured on Apple M1 (8-core, NEON 128-bit), M1 MacBook Air, 2026-04:

**Speedup from `parallel` feature** (RAYON_NUM_THREADS=1 → 8):

| Workload | 1 thread | 8 threads | Speedup |
|---|---|---|---|
| `eval_batch` 10K points (exp tree walk) | 436 µs | 235 µs | **1.85×** |
| `lowered_eval_batch` 100K points (SIMD) | 2.71 ms | 682 µs | **3.97×** |
| `symreg_discover` (topology optimization) | 73.7 ms | 17.3 ms | **4.26×** |

**Speedup from `simd` feature** (10K-point batch, LoweredOp IR):

| Variant | time | Speedup |
|---|---|---|
| Scalar stack machine | 159.8 µs | 1.0× |
| SIMD (F64x2 NEON via oxiblas-core) | 57.0 µs | **2.80×** |

Parallelism helps most for coarse-grained work (symreg topology optimization).
SIMD gives ~2.8× on batch evaluation regardless of batch size. Combining both
scales near-linearly on large batches (100K+ points).

## Design Decisions

- **`Arc<EmlNode>`** — O(1) subtree sharing during symbolic regression
- **Stack-machine evaluator** — Post-order traversal avoids recursion overflow
  on deep trees (sin alone needs 543 nodes)
- **Complex64 internally** — Trig functions and π require `ln(-1) = iπ`;
  complex eval is an internal detail, API is real-valued
- **Discovery vs execution separation** — EML trees for search, lowered ops for speed
- **Parser roundtrip** — `parse(to_compact_string(tree)) == tree`
- **Pure Rust, zero FFI** — Deps: `num-complex`, `rand`;
  optional: `rayon` (parallel), `oxiblas-core` (simd), `oxiz` + `num-rational` (smt)

## Test Coverage

434 tests covering:
- Canonical tree construction (correctness, complex, symbolic)
- Lowering, compilation, pretty-print, LaTeX
- Symbolic gradient, Jacobian, Hessian (central-difference cross-checks)
- Property-based gradient tests (proptest, 1024 cases)
- Trig precision (sin/cos via canonical shapes, 0.0 vs ~1e-14 walk error)
- Interval arithmetic containment and tightness
- Serde round-trip (JSON + oxicode binary)
- SIMD/parallel equivalence
- SMT/constraint solving: interval propagation, OxiZ backend, SAT/UNSAT
- Symbolic regression: Adam, Pareto, k-fold CV, beam, MCTS, multi-output, ODE
- Unit-aware regression (dimensional analysis)
- JIT compilation (scalar, vectorized, cache, hash stability)
- TensorLogic bridge (to/from TLExpr, rewrite rules, soft-prior export)
- CLI integration (eval, lower, grad, symreg, format, output flags)

```bash
cargo nextest run --all-features    # 434 tests
cargo clippy --all-targets --all-features -- -D warnings   # zero warnings
cargo bench --features simd,parallel                       # criterion benchmarks
```

## References

- Paper: Andrzej Odrzywolek, *"All elementary functions from a single binary operator"*,
  [arXiv:2603.21852](https://arxiv.org/abs/2603.21852) (v2: 2026-04-04),
  Jagiellonian University, Institute of Theoretical Physics

## COOLJAPAN Ecosystem

OxiEML is part of the **COOLJAPAN Pure Rust Ecosystem** — one of the largest pure-Rust sovereignty stacks in existence, comprising 660 crates, ~26M SLoC, and 350,000+ passing tests across 50+ production-grade libraries. All projects enforce `fail0 + Clippy0` with zero C/Fortran dependencies by default.

### Core Projects

| Domain | Project | Description |
|--------|---------|-------------|
| Scientific Computing | [SciRS2](https://github.com/cool-japan/scirs) | Complete NumPy/SciPy/scikit-learn replacement (3M SLoC) |
| Scientific Computing | [NumRS2](https://github.com/cool-japan/numrs) | High-performance numerical computing in Rust |
| Scientific Computing | [QuantRS2](https://github.com/cool-japan/quantrs) | Full quantum computing framework |
| Deep Learning | [ToRSh](https://github.com/cool-japan/torsh) | PyTorch-compatible framework with native sharding |
| LLM | [OxiBonsai](https://github.com/cool-japan/oxibonsai) | Pure Rust 1-Bit LLM inference engine for PrismML Bonsai models |
| GPU (CUDA) | [OxiCUDA](https://github.com/cool-japan/oxicuda) | NVIDIA CUDA Toolkit with type-safe, memory-safe Rust code |
| Media & CV | [OxiMedia](https://github.com/cool-japan/oximedia) | FFmpeg + OpenCV replacement (106 crates) |
| Geospatial | [OxiGDAL](https://github.com/cool-japan/oxigdal) | Pure Rust GDAL replacement (cloud-native, full CRS & formats) |
| Semantic Web | [OxiRS](https://github.com/cool-japan/oxirs) | SPARQL 1.2, GraphQL, Digital Twin (Apache Jena replacement) |
| Physics | [OxiPhysics](https://github.com/cool-japan/oxiphysics) | Unified physics engine — Bullet/OpenFOAM/LAMMPS/CalculiX replacement |
| Formal Verification | [OxiLean](https://github.com/cool-japan/oxilean) | Memory-safe interactive theorem prover (Lean 4 inspired) |
| Formal Verification | [OxiZ](https://github.com/cool-japan/oxiz) | High-performance SMT solver (Z3 replacement) |
| Legal Technology | [Legalis-RS](https://github.com/cool-japan/legalis-rs) | Legal statute parser, analyzer & simulator |
| Digital Humans | [OxiHuman](https://github.com/cool-japan/oxihuman) | Privacy-first parametric human body generator (WASM/WebGPU) |
| Signal Processing | [Kizzasi](https://github.com/cool-japan/kizzasi) | Rust-native AGSP for continuous audio, sensor, robotics & video streams |
| Tensor Logic | [TensorLogic](https://github.com/cool-japan/tensorlogic) | Logical rules → tensor equations (einsum graphs) with DSL + IR |
| Math | **OxiEML** | All elementary functions from a single binary operator (this crate) |

Full project list & latest releases → [cooljapan.tech](https://cooljapan.tech/) · [GitHub](https://github.com/cool-japan)


## Python Wrapper (no Rust needed)

A pure Python implementation is included for users who don't want to compile Rust.
Requires only numpy and deap.

    pip install numpy deap

### Basic usage

    from oxieml_star import eml, eml_star, conj_eml, mod_squared, real_part

    z = 1.0 + 0.5j
    print(conj_eml(z))       # (1-0.5j) exact via Theorem 3.1
    print(mod_squared(z))     # 1.25
    print(real_part(z))       # 1.0

### Discover formulas from data (GP)

    from discover_gp import run_gp
    import numpy as np

    z = np.array([1+0.5j, 2-1j, 0.5+2j, -1+0.3j, 3-0.7j])
    targets = np.conj(z)
    results = run_gp(z, targets, pop=300, gen=40, runs=5)

### Discover formulas from CSV

    python3 discover_gp.py --csv data.csv --pop 300 --gen 40 --runs 10

CSV format: z_real, z_imag, target_real, target_imag

The GP engine uses eml, eml-star, conj_eml, add, mul as primitives
and discovers closed-form complex-valued formulas automatically.

Paper: Monnerot (2026) https://doi.org/10.5281/zenodo.20091022

## Sponsorship

OxiEML is developed and maintained by **COOLJAPAN OU (Team Kitasan)**.

The COOLJAPAN Ecosystem represents one of the largest Pure Rust scientific computing efforts in existence — spanning 50+ projects, 650+ crates, and millions of lines of Rust code across scientific computing, machine learning, quantum computing, geospatial analysis, legal technology, multimedia processing, and more. Every line is written and maintained by a small dedicated team committed to a C/Fortran-free future for scientific software.

If you find OxiEML or any COOLJAPAN project useful, please consider sponsoring to support continued development.

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=github)](https://github.com/sponsors/cool-japan)

**[https://github.com/sponsors/cool-japan](https://github.com/sponsors/cool-japan)**

Your sponsorship helps us:
- Maintain and expand the COOLJAPAN ecosystem (50+ projects, 650+ crates)
- Keep the entire stack 100% Pure Rust — no C/Fortran/system library dependencies
- Develop production-grade alternatives to OpenCV, FFmpeg, SciPy, NumPy, scikit-learn, PyTorch, TensorFlow, GDAL, and more
- Provide long-term support, security updates, and documentation
- Fund research into novel Rust-native algorithms and optimizations

## License

Apache-2.0

2026 COOLJAPAN OU (Team KitaSan)
