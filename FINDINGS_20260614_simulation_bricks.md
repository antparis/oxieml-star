# FINDINGS 2026-06-14 -- [DERIVATION/IN-PROGRESS] g1=0 ablation simulation: bricks 1-2 calibrated on Anthony's machine.

## Goal
Build the Qu-Lu-Ding 2506.19822 T' lepton model numerically to run the g1=0 ablation
(never done by anyone): does removing the non-holomorphic weight-1 doublet Y2hat''^(1)
coupling g1 break the fit? Build brick by brick, each CALIBRATED against published values
before proceeding (Anthony's chosen "slow, safe" path).

## Bricks done (executed + calibrated on Anthony's machine)
- BRICK 1 [CALIBRATED]: weight-1 level-3 non-holo Maass form Y2hat''^(1).
  Constant a0 = 0.113229... reproduces Qu-Ding eq.3.26 published ~0.1132. PASS.
  FINDING: at best-fit tau (Im=1.108) the form is ~48% non-holomorphic / 52% holomorphic,
  the non-holo part DOMINATED by log y (~0.10); the deep mock-Gamma part is only 0.37% of
  the non-holo (exponentially suppressed). xi_1(log y) = -1 exactly (non-holo content lifts
  to a trivial O(1) holomorphic shadow). File maass_form_calib.py.
  CORRECTION logged: an initial mislabel of log y as "holomorphic" gave a wrong 0.18%; the
  correct figure is ~48%. Caught before reporting. (log y depends on taubar -> non-holo.)
- BRICK 2 [CALIBRATED]: holomorphic weight-2 level-3 triplet reproduces Feruglio 1706.08749
  q-expansion (Y1=1+12q, Y2/q^{1/3}=-6, Y3/q^{2/3}=-18). PASS. Weight-4 triplet Y3^(4)
  (ingredient of Majorana matrix M_N) built on it, finite/nonzero at best-fit tau.
  File maass_brick2_weight4.py.

## Bricks remaining (cold, brick by brick, each to calibrate)
- BRICK 3: non-holomorphic weight-0 triplet Y3^(0) (for charged-lepton M_e). NO holomorphic
  counterpart (weight 0) -> intrinsically non-holo. Calibrate constant term.
- BRICK 4: weight-1 doublets FULL -- both components of Y2hat^(1) (holo) and Y2hat''^(1)
  (non-holo), in correct T' basis, for the Dirac matrix M_D (eq.4.3).
- BRICK 5: T' Clebsch-Gordan + assemble M_e (3x3), M_D (2x3), M_N (2x2) per eq.4.3.
- BRICK 6: seesaw m_nu = M_D^T M_N^{-1} M_D, diagonalize, extract masses+PMNS, build chi^2 vs
  NuFIT. Calibrate the FULL model against Qu-Ding Table 2 best-fit (chi^2, angles) BEFORE ablation.
- ABLATION: set g1=0, re-minimize; chi^2 stays bad => non-holo NECESSARY; holo-only refit
  recovers => decorative. Arbiter = executed on Anthony's machine.

## Status
[DERIVATION/IN-PROGRESS]. 2 of ~6 bricks calibrated. NOT yet an ablation result.
Honest: this reproduces no one (the g1=0 test is unpublished), so every brick must be
calibrated against published values before the final verdict is trusted.
