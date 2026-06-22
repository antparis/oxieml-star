# FINDINGS 2026-06-10b -- GW PySR test: asymmetry is REAL but NOT anti-holomorphic in h22

## Setup
Following the clean asymmetry result (FINDINGS_20260610_gw_first_run.md, hash
2aba64c2). Gate passed: real mode-asymmetry on precessing binaries, clean
negative control, 0163 (2,2) anomaly explained as physical (spin-exchange
asymmetry chi1_z vs chi2_z). THEN: feed to PySR to test eml* structure.

## Question tested
Is the chiral mode-asymmetry A_33(t) an ANTI-HOLOMORPHIC function of the
dominant mode z=h_22(t) (co-precessing frame)? z=h_22 chosen as the
least-reducible native-complex observable (not an analysis artefact). Symmetric
test: HOLO [Re z, Im z] vs ANTI [Re z, -Im z] vs SHUFFLE, on 0161/0163/0164.

## Method (honest about the limit)
PySR has no native complex; it is the DISCOVERER (indicative), NOT the judge.
True anti-holo verdict would come from verify_exact.py on a found formula.
gw_pysr_run.py: niterations=80, deterministic, serial, maxsize=25. Target Re(A33).
Data: gw_extract_for_pysr.py -> gw_pysr_data.npz (resampled 4000 pts, co-prec).

## RESULT: NEGATIVE
loss table (lower=better):
  sim    holo      anti      shuffle
  0161   1.53e-6   1.49e-6   2.28e-6
  0163   2.47e-6   2.76e-6   3.41e-6
  0164   2.62e-6   2.71e-6   3.54e-6
Three red flags for ANY anti-holo claim:
1. HOLO ~ ANTI everywhere (within 5-15%, anti even WORSE on 0163/0164). No
   anti-holomorphic preference. If A_33 were anti-holo in h22, anti would win
   clearly and reproducibly. It does not.
2. SHUFFLE only ~1.5x worse than holo/anti. A genuine functional relation
   A_33=f(h22) should be DESTROYED by time-shuffling. It is not -> PySR fits the
   value distribution, not a point-by-point structure. Signal weak/trivial.
3. Formulas decorative: sin(sin(sin(...))), log(cos(log(cos(...)))) -- overfit.

## Verdict: [DERIVATION/LIMIT] -- NEGATIVE, gate to judge NOT opened
- Mode-asymmetry of precessing binaries is REAL (raw measure, control-validated).
- But NO anti-holomorphic structure as a function of h_22, by PySR.
- verify_exact.py NOT run: nothing worth certifying (holo==anti, shuffle uncasse).
  Certifying here would certify noise. PySR->judge gate stays CLOSED.

## Two open readings (later, cold session -- do NOT rush)
A. Wrong variable: anti-holo might live elsewhere (orbital phase exp(i*phi), or a
   different mode pair), not in h22. z=h22 was reasoned but not unique.
B. GW asymmetry simply NOT anti-holomorphic in eml* sense -> GW lead joins the
   others: known asymmetry (Boyle 2014), not chiral in strict sense.

## holo/anti ledger update
- ANTI column: GW (z=h22, mode 3,3) -> NO anti-holo structure. NEGATIVE.
- Chiral cell (forced + transcendental + physical + non-reducible) REMAINS EMPTY.

## Pointer
Builds on FINDINGS_20260610_gw_first_run.md (2aba64c2). PySR/eml* stage.
Scripts: gw_extract_for_pysr.py, gw_pysr_run.py, gw_pysr_results.json (on disk).
