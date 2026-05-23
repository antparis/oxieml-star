# FINDINGS — eml-star definition inconsistency (canonical MIXTE vs code PURE)

Date: 2026-05-23
Status: [ESTABLISHED] for the mapping. [OPEN DECISION] for which def is canonical.

## The problem
eml-star has TWO different definitions in the ecosystem:
  MIXTE (paper/Zenodo/README, canonical): eml-star(x,y) = exp(x) - log(conj(y))
  PURE  (compute repo, drifted):          eml-star(x,y) = exp(conj(x)) - log(conj(y))
They are DIFFERENT objects (one anti gate vs two = conj(eml)). Both pass the
binary holo/anti test, which is why the inconsistency survived unnoticed.
Theorem 3.1 holds for both (first arg = 0, conj(0)=0).

## Map (grep-verified 2026-05-23)
Paper repo ~/Desktop/eml_star/ : CLEAN, MIXTE everywhere (verify_theorem4.py:29,
  core.py:13, PDF). No publication is affected.
Compute repo ~/Desktop/oxieml-star/ : drifted to PURE.
  ACTIVE/CRITICAL: verify_exact.py:76 (the judge), pysr_stacking.py:155+170.
  OLD (PURE, mostly invalidated galaxy data): double_validation v1-v6, lensing,
    detect_real_data, discover_pysr, eml_evolution, eml_star_decomposition,
    eml_wm_pipeline, noise_robustness, significance_metric, translate_formula,
    verify_decomposition.
  ALREADY MIXTE: test_generative_power.py

## Impact on tonight's results
B2 shear: formulas used my_imag/eml, NOT emlstar -> verdicts UNAFFECTED.
Penning anti+hybrid: formulas contained emlstar, judged with PURE. Both defs are
  anti-holomorphic so "anti" is likely robust, but [TO RE-CERTIFY] under the
  chosen def. No published artifact affected.

## Decision (provisional-strong, NOT rushed)
Direction: keep MIXTE (align code to paper). Reason: the paper is published and
  clean; fixing private code is cheap and reversible, editing a publication is
  not. Consequence: align the CODE to MIXTE later, do NOT touch the PAPER until
  the Theorem 4.3 proof is read.
Correction scope when done: 2 active files (verify_exact.py + pysr_stacking.py)
  + re-certify Penning. The 17 old scripts are archived/historical, NOT patched
  one by one.

## Status
[ESTABLISHED] Inconsistency mapped; paper clean MIXTE; code drifted PURE.
[ESTABLISHED] Penning & B2 calibrations stand.
[TO VERIFY later] Does the Theorem 4.3 proof REQUIRE mixte? (read PDF = clue,
  not verdict; Anthony's math validation is the arbiter).
[TO RE-CERTIFY] Penning under MIXTE once code aligned.
[OPEN] EML-WM must NOT hardwire which eml-star until this is closed.
