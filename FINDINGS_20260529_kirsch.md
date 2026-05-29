# FINDING: Kirsch elasticity — anti-holomorphic, CERTIFIED

Date: 2026-05-29
Status: [ESTABLISHED]  (executed on machine + SymPy judge certified)

## What was tested
Kolosov-Muskhelishvili displacement field w = u_x + i u_y for a plate with a
circular traction-free hole under uniaxial tension. Natively complex, spatial,
time-free. Anti-holomorphic content forced by the traction-free hole boundary.

## Exact command
cd ~/Desktop/oxieml-star
nohup python3 -u kirsch_stack.py --only kirsch --niter 120 --pop 500 --maxsize 40 > kirsch_stack_bigbudget.log 2>&1 &
python3 verify_exact.py --formula "<best_equation from kirsch_stack_kirsch_result.json>"

## Raw result (big-budget run, Linux)
- best_mse  = 3.03e-31   (<< 1e-3, exploitable)
- complexity = 29
- equation recovers Kolosov bricks: z, 1/z, zbar, 1/zbar, 1/zbar^3
- Judge (SymPy, exact): df/dzbar = -1.3 z/zbar^3 + 0.65 + 0.65/zbar^2 - 1.95/zbar^4  != 0
- VERDICT: ANTI-HOLOMORPHIC (certified, not a marker)

## Controls (both machines, reproducible)
- holo control:  MSE 0.0, eq = x0           (no false anti)
- shuf control:  MSE ~8.7, rejected         (not fooled by noise)

## Key lesson
Borderline at niter=60/pop=300 (MSE 1.5e-3 / 2.85e-3, 2 of 3 runs failed) was a
BUDGET artifact, NOT irreducibility. Big budget (120/500/40) -> MSE 3e-31,
recovered the 1/zbar^3 brick that small budget missed. Decision to re-run was correct.

## Status tag
[ESTABLISHED] — validation (not discovery): Kolosov-Muskhelishvili known since ~1909.
Second physical spatial system after Landau where anti-holo is forced by physics.
