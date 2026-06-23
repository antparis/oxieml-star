# FINDINGS 2026-06-23b -- Neutrino anti-holomorphic term DECORATIVE on real observables (confirmed by clean re-run)

Status: [DERIVATION, negative] -- re-executed on machine, clean test (7 obs, fundamental
domain, 21 starts). Confirms FINDINGS_20260615_ablation_negative. Resolves a standing
contradiction in the repo. NOT a Project A discovery.

## Why this was re-run
The repo held CONTRADICTORY verdicts on whether the anti-holomorphic (eml*) ingredient
of the Qu-Lu-Ding T' lepton model is necessary or decorative:
  - ablation_g1.py (4 obs, M_e fixed, tau unconstrained):        prints "anti NECESSARY" (chi2 g1=0 = 1871)
  - ablation_g1_robust.py (4 obs, tau unconstrained, FULL=0.0):  prints "anti necessary" (overfit: 5 params/4 obs)
  - FINDINGS_20260615_ablation_negative (memory):                 "anti DECORATIVE"
The clean script full_chi2_test.py (7 obs, tau hard-constrained to fundamental domain,
21 starts) was re-executed to settle it.

## Exact command + raw result (on machine, 2026-06-23)
    cd ~/Desktop/oxieml-star && python3 full_chi2_test.py    # detached
  --- full    --- chi2=0.91  tau=-0.051+1.089i
  --- holo    --- chi2=0.23  tau=-0.058+1.012i
  --- nonholo --- chi2=0.04  tau=-0.063+1.035i
  (all three IN the fundamental domain, equal parameter count)

## Verdict (read from the chi2, NOT from the script's hardcoded VERDICT line)
holo-only chi2 = 0.23  <=  full chi2 = 0.91. eml-only (holomorphic) reproduces the 7
observables AS WELL AS (in fact better than) the full model, in-domain, at equal param
count. => the eml* (anti-holomorphic) term is DECORATIVE on the standard leptonic
observables. Rejected as a Project A discovery. Consistent with the navigation law:
masses / mixing angles are REAL observables -> mirror-locked -> anti is the forced
reflection, not independent information.

The earlier "anti necessary" signals (ablation_g1*.py) were artefacts of overfitting
(4 obs / 5 params, FULL chi2 -> 0) and tau left outside the fundamental domain.

## BUG / DEBT (must fix)
Three scripts print a verdict CONTRADICTED by their own numbers:
  - full_chi2_test.py  final line "anti NECESSARY"  -- FALSE (holo 0.23 < full 0.91); hardcoded, not recomputed.
  - ablation_g1.py / ablation_g1_robust.py  "anti necessary" -- overfit/out-of-domain artefact.
These Reading/VERDICT lines are stale text, not computed from chi2. To be corrected.

## OPEN DOOR (not closed by this test)
delta_CP is NOT tested: in all scripts dcp=1.15 is a dead placeholder and the computed
Jarlskog J is discarded. So "decorative" holds for the 6 REAL observables only, not for
the natively-complex CP phase. delta_CP via the two tribunals (Wirtinger judge + CP-judge
Jarlskog on the in-domain fit) remains the only open neutrino question. [CONJECTURE]

## Files
full_chi2_test.py (clean test, but its final VERDICT line is wrong), fullchi2_run.log,
ablation_g1.py / ablation_g1_robust.py (stale verdicts), FINDINGS_20260615_ablation_negative.md.
