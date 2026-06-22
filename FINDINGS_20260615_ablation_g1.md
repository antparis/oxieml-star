# FINDINGS 2026-06-15 -- [HEURISTIC, strong, NOT established] g1=0 ablation on Qu-Lu-Ding T' lepton model: cutting the non-holomorphic Dirac term collapses the fit; holo/anti asymmetry confirmed. To consolidate before [ESTABLISHED].

## What this is
Ablation test on the reconstructed+calibrated Qu-Lu-Ding 2506.19822 lepton model (bricks 5+6,
FINDINGS_20260615_brick56_calibrated, Milo 640e6fe8). g1 = coupling of the NON-holomorphic
Y_2hat'' Dirac term in M_D; g2 = holomorphic Y_2hat term. Question (Project A): is the
anti-holomorphic structure NECESSARY (physics forces it) or decorative (refit recovers)?
Scripts: ablation_g1.py (M_e fixed), ablation_g1_robust.py (M_e free + inverse control).

## Results (executed on Anthony's machine)
PASS 1 -- M_e FIXED, re-minimize (tau, g2) only [the clean test]:
  FULL (g1=1)      chi2_nu = 0.91   (matches published gCP-NO chi2 = 0.90 -> minimizer calibrated)
  ABL-ANTI (g1=0)  chi2_nu = 1871   (collapse, ~2000x; refit cannot recover)
PASS 2 -- M_e FREE, re-minimize (tau, g2, beta, gamma) + inverse control:
  FULL (g1,g2 free)   chi2 = 0.0    (SEE RED FLAG below)
  ABL-ANTI (g1=0)     chi2 = 656.7  (collapse)
  ABL-HOLO (g2=0)     chi2 = 76.1   (degraded ~9x less than ABL-ANTI)

## Reading
- Asymmetry is real: cutting the ANTI-holomorphic term (657) is ~9x worse than cutting the
  HOLOMORPHIC term (76). So it is NOT "cutting any term breaks everything" -- the inverse control
  rules that out. The anti-holomorphic term carries specifically more weight.
- PASS 1 (M_e fixed) is the clean test: FULL=0.91 (=published), ABL-ANTI=1871 (massive collapse).
  The effect is huge, so it is not drowned in reconstruction noise.

## RED FLAG (why this is NOT [ESTABLISHED] yet)
- PASS 2 FULL chi2 = 0.0 is a sign of OVERFITTING, not a good fit: 5 free params (tau_re, tau_im,
  g2, beta, gamma) for only 4 observables -> the fit can always reach 0 regardless of physics.
  So PASS 2's FULL value must NOT be read as validation; PASS 2 is useful only for the asymmetry
  control (657 vs 76), not for fit quality. PASS 1 (M_e fixed) is the trustworthy fit-quality test.
- Both terms still seem needed: ABL-HOLO=76 is also a bad chi2 (good fit ~ 1). The claim is
  "anti >> holo in importance", not "only anti matters".

## To consolidate before [ESTABLISHED]
1. Break the overfitting: add more observables (m_e/m_mu, m_mu/m_tau, delta_CP) so #obs > #params.
2. Check whether Qu-Ding's statement "g1 dominates at best-fit" already implies necessity, or
   whether the necessity demonstration (refit cannot recover) is genuinely our contribution.
3. More multi-starts on ABL-ANTI to be certain no recovering minimum exists.

## Status
[HEURISTIC, strong]. Robust holo/anti asymmetry + massive collapse under M_e-fixed ablation point
toward the anti-holomorphic term being NECESSARY in this model -- a candidate Project A result
(2nd forced-anti case after Kirsch, in a new domain: neutrino masses). NOT [ESTABLISHED]: PASS 2
overfitting flag + consolidation pending. A single working model proves internal necessity to THIS
model, not that nature is anti-holomorphic. No link to gravity or to non-neutrino masses.
Files: ablation_g1.py, ablation_g1_robust.py.
Arbiter = Anthony's machine + published Table 2 + (pending) consolidation.
