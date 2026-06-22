# FINDINGS 2026-06-15 -- [DERIVATION/CALIBRATED] Brick 3 of g1=0 ablation: non-holomorphic weight-0 level-3 triplet Y3^(0), triple-calibrated on Anthony's machine.

## What this is
Brick 3 of the Qu-Ding 2506.19822 lepton-model rebuild (for the g1=0 ablation test).
The weight-0 level-3 (A4) polyharmonic Maass triplet Y3^(0), Qu-Ding 2406.02527 Eq. C.32.
PURELY non-holomorphic: no holomorphic weight-0 form exists -> empty-slot forced. Ingredient
of the charged-lepton matrix M_e.

## Source (exact, fetched)
Eq. C.32 of 2406.02527. comp1 = y - 9 log3/(4pi) + holo q-series + non-holo e^{-4 pi n y}/q^n
series (holo and non-holo coeffs share magnitudes 3/pi, 9/2pi, 1/pi, 21/4pi, 18/5pi, 3/2pi).
comp2, comp3 = pure q^{1/3}, q^{2/3} series, no constant, no y-term. Constant -9 log3/(4pi)
= -0.78682. Built/checked via master eq C.31: D(Y3^(0)) = -(1/4pi) Y3^(2),
xi_0(Y3^(0)) = Omega Y3^(2) (Omega = 2<->3 swap).

## Calibration (executed on Anthony's machine) -- 3 independent checks vs calibrated brick 2
- CALIB 1 (constant): -9 log3/(4pi) = -0.7868230932736345. PASS.
- CALIB 2 (operator D, HOLOMORPHIC part, all 3 comps): D(Y3,i^(0)) = -(1/4pi) Y_i^(2).
  ratios = 1.0000000000000002 / 1.0000000000000047 / 1.0000000000000304. PASS (machine precision).
- CALIB 3 (operator xi_0, NON-HOLOMORPHIC part): xi_0(Y3,1^(0)) = -conj(Y1^(2)).
  ratio = 1.0000000000000002. PASS (machine precision).
=> BRICK 3 fully calibrated: True.

## Bug caught and fixed (logged)
First attempt FAILED CALIB 2 (ratio ~8e-6 instead of 1). Cause: the D operator was coded as a
real-axis derivative d/d(Re tau) instead of the true Wirtinger d/dtau = (1/2)(d/dx - i d/dy).
On a form with explicit y=Im(tau) dependence this is wrong. Fixed: D and xi now use the full
Wirtinger (1/2)(d/dx -+ i d/dy). After fix all checks pass to machine precision. This is exactly
the kind of error the calibration is designed to catch on the test that reproduces no one.

## Resolved: literature typo
The q^1 coefficient is -3/pi (NOT -3/2pi, which some downstream papers print). The D cross-check
confirms -3/pi (the wrong coefficient would fail CALIB 2).

## Status
[DERIVATION/CALIBRATED]. 3 of ~6 bricks done (brick1 weight-1 a0=0.1132; brick2 weight-2/4
Feruglio; brick3 weight-0 C.32). File maass_brick3_weight0.py. NOT yet an ablation result.
REMAINING: brick4 full weight-1 doublets for M_D; brick5 T' Clebsch + assemble M_e/M_D/M_N;
brick6 seesaw + diagonalize + chi2 vs NuFIT, CALIBRATE full model vs Qu-Ding Table2 BEFORE
ablation; then set g1=0 re-minimize. Arbiter = executed on Anthony's machine.
