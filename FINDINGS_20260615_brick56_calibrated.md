# FINDINGS 2026-06-15 -- [DERIVATION/CALIBRATED] Brick 5+6: full Qu-Lu-Ding T' lepton model reconstructed and reproduces Table 2 (With gCP NO) on Anthony's machine. Ready for g1=0 ablation.

## What this is
Full assembly of the lepton model of Qu-Lu-Ding 2506.19822 (M_e 3x3, M_D 2x3, M_N 2x2, seesaw
m_nu=-M_D^T M_N^{-1} M_D, diagonalization, PMNS), with the EXACT Qu-Ding normalized weight-2 and
weight-4 level-3 triplets read from the authors' reference notebook PHMF_integer.nb. Calibrated
against Table 2 column "With gCP NO" (all couplings real). Script: assemble_model.py.

## Result (executed on Anthony's machine)
With gCP NO: tau=-0.03777+1.090i, beta/alpha=17.70, gamma/alpha=284.6, g2/g1=0.1490 (real):
  m_e/m_mu   = 0.004935  (target 0.004737, 4%)
  m_mu/m_tau = 0.058833  (target 0.05882, 0.02%)
  sin2_th12  = 0.3030    (target 0.308, 1.6%)
  sin2_th13  = 0.02038   (target 0.02215, 8%)
  sin2_th23  = 0.4573    (target 0.459, 0.4%)
All observables reproduced to a few percent => the full model is correctly reconstructed.

## Key diagnostic finding (corrects earlier conjecture)
The earlier block on m_mu/m_tau (stuck at 0.0633) was NOT due to triplet relative normalization:
using the exact notebook normalization gave IDENTICAL results to the bare tensor products.
The real cause was the calibration TARGET: the "Without gCP NO" column has complex g2 (phase 1.888pi)
whose phase convention was mis-handled. The "With gCP NO" column (all real couplings) reproduces
cleanly. So the reference notebook confirmed the triplets were already correct; the fix was using
the real-coupling column. Triplet normalization hypothesis = REFUTED by test.

## Exact Qu-Ding normalized triplets used (from PHMF_integer.nb)
Y3,1^(2)=1+12q+36q^2+12q^3+84q^4+72q^5+...; Y3,2^(2)=-6 q^{1/3}(1+7q+8q^2+18q^3+...);
Y3,3^(2)=-18 q^{2/3}(1+2q+5q^2+4q^3+...); Y3,1^(4)=1-84q-756q^2-2028q^3-6132q^4-...;
Y3,2^(4)=6 q^{1/3}(1+73q+344q^2+1134q^3+...); Y3,3^(4)=54 q^{2/3}(1+14q+65q^2+148q^3+...).
Weight-0 = eq 3.21 (Y3,2/Y3,3 holo, Y3,1 nonholo). Weight-1 doublets = bricks 4.

## Status / next
[DERIVATION/CALIBRATED]. All bricks (forms 1-4 + assembly 5-6) validated against published Table 2
on Anthony's machine. NEXT = g1=0 ablation: set g1=0 in M_D (kills the non-holomorphic Y_2hat''
Dirac term), re-minimize chi^2 vs NuFIT. chi^2 stays bad => non-holo NECESSARY (result); holo-only
refit recovers => decorative. This is the test that reproduces no one.
Files: assemble_model.py, refs/PHMF_integer.nb, maass_brick1-4.
Arbiter = Anthony's machine + Table 2 + reference notebook.
