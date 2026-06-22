# FINDINGS 2026-06-15 -- [DERIVATION/CALIBRATED] Brick 4 of g1=0 ablation: weight-1 level-3 doublets (holo Y2hat + non-holo Y2hat'') for M_D, fully calibrated on Anthony's machine.

## What this is
Brick 4 of the Qu-Lu-Ding 2506.19822 lepton-model rebuild. The two weight-1 level-3 (T')
doublets that build the neutrino Dirac matrix M_D (eq. 4.3):
  Y2hat^(1)   in rep 2-hat   = HOLOMORPHIC     -> coupling g2
  Y2hat''^(1) in rep 2-hat'' = NON-HOLOMORPHIC -> coupling g1  (the term to ABLATE)
Each doublet has 2 components. File maass_brick4_weight1.py.

## Sources (exact, fetched from 2506.19822)
- Holo doublet eq. 3.11 / D.10: Y1 = -3sqrt2 eta^3(3tau)/eta(tau) = -3sqrt2 q^{1/3}(1+q+2q^2+...);
  Y2 = 1 + 6 sum_{n>=1}(sum_{d|n} chi2(d)) q^n (theta_{-3}, A2-lattice theta). chi2 = Legendre mod 3.
- Non-holo doublet eq. 3.25: comp1 = a0 + log y + holo q-series + non-holo Gamma(0,4pi n y)/q^n
  (brick 1, a0=0.1132); comp2 = -6sqrt2 q^{2/3}(log2 + q log5 + ...) [holo] - 3sqrt2 sum
  (sum_{d|(3n+1)}chi2(d)) q^{-(3n+1)/3} Gamma(0,(12n+4)pi y/3) [non-holo].

## TWO paper typos corrected (not guessed -- forced by eq. 3.22, verified by tests)
- comp2 non-holo prefactor is q^{-1/3} (paper prints q^{2/3}); negative q-power required by the
  Fourier expansion 2.12-2.13. Verified: literal q^{2/3} version VIOLATES the harmonic condition
  (Delta_1 = 6e-4), corrected q^{-1/3} version satisfies it (Delta_1 = 1e-8).
- 3rd gamma argument is (12n+4)pi y/3 = 28pi y/3 at n=2 (paper prints 2pi y/3); the divisor-sum
  coefficient sum_{d|7}chi2=2 matches.

## Calibrations (executed on Anthony's machine)
- CALIB H (holo doublet vs eq. 3.11): Y1/(-3sqrt2 q^{1/3}) = 1+q+2q^2+..., Y2 = 1+6q+6q^2+... PASS.
- CALIB Delta1 (weight-1 harmonic condition Delta_1 f = 0 on both non-holo comps):
  Delta_1(comp1) = 3.3e-9, Delta_1(comp2) = 1.2e-8. PASS.
- CALIB xi1 (Maass shadow): xi_1 maps the non-holo doublet to conj of the holo doublet, with the
  S-induced component swap: xi_1(comp1)/(-conj Y_holo2) = 1.0000000000002,
  xi_1(comp2)/(conj Y_holo1) = 1.0000000000025. PASS (machine precision).
=> BRICK 4 fully calibrated: True.

## Variant discrimination (logged)
Two variants passed Delta_1=0 AND T-covariance: A (non-holo indexing 3n+1) and C (3n+2). The
xi1 SHADOW test discriminated them: variant A reboucle exactly on the holo doublet (ratio 1.0),
variant C gives a NULL shadow (~4e-13) -> C rejected. Same Maass cross-check that validated brick 3.

## Status
[DERIVATION/CALIBRATED]. 4 of ~6 bricks done. ALL Maass forms now coded+calibrated:
brick1 (w1 comp1), brick2 (w2/w4 holo), brick3 (w0 non-holo), brick4 (w1 both doublets).
NOT yet an ablation result. REMAINING: brick5 = T' Clebsch-Gordan + assemble M_e (3x3, uses
Y3^(0,2,4)), M_D (2x3, uses the w1 doublets with g1,g2), M_N (2x2, uses Y3^(4)) per eq. 4.3;
brick6 = seesaw m_nu = M_D^T M_N^{-1} M_D + diagonalize + chi2 vs NuFIT, CALIBRATE full model
vs Qu-Ding Table 2 BEFORE ablation; then set g1=0 re-minimize. Arbiter = Anthony's machine.
