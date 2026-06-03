# FINDINGS 2026-06-01 -- Vortex N1: pipeline recovers transcendental chiral anti (CALIBRATION)

## Status
[ESTABLISHED] executed on machine + SymPy-judge certified + both negative
controls passed. NATURE: CALIBRATION on a SYNTHETIC target. NOT a physical
discovery (vortex_N1 built anti by vortex_gen_N1.py).

## What is tested
Pipeline = PySR (MIXTE+inv+inv_bar) -> judge verify_exact.certify -> reality
flag reality_check.py. Question: recover a TRANSCENDENTAL chiral anti
a*log(z)+b*log(conj z), b!=conj(a), on a clean single-vortex target, while
passing a holo control and a shuffle control. (The 2026-05-30 multi-vortex
run FAILED to do this; N1 is the simplified retry.)

## Commands (exact)
Config (from JSON): niter=30 pop=300 maxsize=25 parsimony=0.001 precision=64,
toolbox MIXTE+inv+inv_bar, via kirsch_stack.run_one.
  controls: python3 vortex_N1_controls.py --only holo
            python3 vortex_N1_controls.py --only shuf
  judge   : python3 reality_check.py vortex_N1_result.json
            python3 reality_check.py vortex_N1_holo_result.json
WARNING: precision MUST stay 64. precision=32 breaks the eml operator
(Julia: eml returns ComplexF64 on ComplexF32 inputs).

## Raw results (judge-certified)
  vortex_N1      MSE=2.69e-18  ANTI-HOLOMORPHIC  flag=complex   GENUINE
                 = (0.717+0.395i)log(z-c) + b log(zbar-c), b!=conj(a)
                 df/dzbar = b/(zbar-c)  (log term, infinite order)
  vortex_N1_holo MSE=2.62e-24  HOLOMORPHIC       df/dzbar=0     HOLO OK
                 = (0.717+0.395i)log(z-c), NO log(zbar)
  vortex_N1_shuf MSE=12.75     mse_below_1e-3=false             REJECTED OK

## Interpretation
- Transcendental (infinite-order) anti: anti part is log(zbar), never killed
  by finite d/dzbar. Distinct from algebraic anti (Kirsch, Landau: rational poles).
- Chiral imbalance |a|=0.82, |b|=1.25: escapes SPARC real-field trap (flag complex).
- FIRST end-to-end pipeline success on a transcendental chiral anti WITH controls.

## Limits / next gate
- vortex_N1 is SYNTHETIC. "Transcendental anti on a PHYSICAL system" remains
  UNDEMONSTRATED. This is a calibration, it unblocks the physical test.
- Next: optical_vortex_gen.py (physical) through the same gate
  (ANTI + flag complex + MSE<1e-3 + holo->HOLO + shuf->reject).
- reality_check.py: [ESTABLISHED], both branches certified, certify() unchanged.
  EXACT only on symbolic formulas; on real noisy data the arbiter stays the
  negative control + exploitable MSE, never this flag alone.
