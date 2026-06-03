# FINDINGS 2026-05-30 — Vortex detector: run 1 failure + anti-overfit fix

## Context
Synthetic chiral vortex-gas field vortex_gas.csv (3460 rows, natively complex,
purely spatial, no time axis). Field carries transcendental anti-holomorphic
content by construction: a*log(z) + b*log(conj(z)) with chiral imbalance
(a_k != conj(b_k)).
Field property is [ESTABLISHED] (verified at generation, SymPy + numeric):
|df/dz_bar - conj(df/dz)| = 1.27 (escapes the SPARC real-field trap),
both derivatives nonzero (MIXED holo + anti).

## Run 1 — FAILED (overfit to monsters)
- Command: python3 vortex_stack.py --only all --niter 120 --pop 500 --maxsize 40
- Detector: PySR 1.5.10 via kirsch_stack.run_one, toolbox MIXTE+inv+inv_bar.
- Result file: vortex_stack_vortex_result.json (written 2026-05-30 13:39)
- best_mse = 1.3158  (mse_below_1e-3 = false)
- complexity = 31  (near maxsize cap)
- elapsed_s = 56321  (15.6 h for ONE dataset)
- best_equation: nested emlstar(emlstar(emlstar(...))) + nested log(log(...)),
  stuffed with constants. NOT a clean a*log(z)+b*log(conj(z)).

### Verdict: INVALID per guard-rail
MSE 1.32 >= 1e-3 => claim non-exploitable regardless of operator marker.
SymPy judge NOT run: judging the anti-holomorphy of an equation that does not
fit the field would certify a void statement. Guard-rail takes precedence.
Status: [HEURISTIC negative].

### Diagnosis (cause isolated, confirmed on machine)
PySRRegressor had NO structural brake:
- nested_constraints = None  -> emlstar/log nesting unlimited (monster cause)
- constraints = None         -> argument complexity unlimited
- maxsize 40 (launch flag)   -> allowed complexity-31 trees
- adaptive_parsimony_scaling = 1040.0 (already full default — NOT the problem)
- model_selection = "best"   (already optimal — unchanged)

## Fix applied to kirsch_stack.py run_one (PySRRegressor block only)
Backup: kirsch_stack_BACKUP_20260530_*.py
Added: maxdepth=8; nested_constraints (emlstar/eml depth 1, log/exp/sin/cos/inv
depth 0 self+cross); constraints {emlstar:(-1,6), eml:(-1,6)}.
my_conj deliberately NOT constrained (carries the anti directly).
emlstar/eml allowed depth 1 (not 0) so a single emlstar can appear in result.
Syntax validated: Python ast.parse OK; Julia dry-run (1 iter, 10 pts) EXIT 0,
Pareto front showed bounded nesting only. Brake demonstrably works.

## Run 2 — test (in progress)
- Command: python3 vortex_stack.py --only vortex --niter 60 --pop 400 --maxsize 25
- Log: vortex_stack_v2.log
- Goal: confirm brakes yield a SHORT eq (target complexity ~7) with MSE << 1e-3.
- If clean + MSE << 1e-3 -> run holo + shuf controls, THEN judge verify_exact.py.
- If still no clean form at niter=60 -> not a budget issue; investigate design.
- Status: [HEURISTIC] pending execution.

## Next gate (nothing certified yet)
- Field: [ESTABLISHED]. Detector reconstruction: OPEN.
- Certification needs: machine exec + MSE<1e-3 + clean form + SymPy judge
  (df/dz_bar exact) + negative controls (holo->HOLO, shuf->reject).
