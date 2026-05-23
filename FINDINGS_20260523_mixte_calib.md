# FINDINGS — MIXTE tool calibration (full pipeline PySR -> judge)

Date: 2026-05-23
Status: [ESTABLISHED] executed on machine + judge-certified (MIXTE).
Nature: CALIBRATION of the corrected MIXTE tool. NOT a discovery (targets known).

## Why
After applying the MIXTE correction (verify_exact.py + pysr_stacking.py), the
full chain (PySR generates -> SymPy judge certifies) had to be re-validated on
KNOWN targets, not just the judge alone.

## Test (anti_calib_test.py, light config pop=100/niter=60/maxsize=16)
Targets, natively complex, |z|>0.15:
  holo    : f(z)=z^2          -> expect HOLOMORPHIC
  anti    : f(z)=conj(z)^2    -> expect ANTI-HOLOMORPHIC
  shuffle : anti with targets permuted -> negative control, expect MSE>=1e-3

## Results (judge-certified)
  holo    : eq=x0*x0           MSE=1.09e-32  HOLOMORPHIC      OK
  anti    : eq=my_conj(x0*x0)  MSE=1.09e-32  ANTI-HOLOMORPHIC OK
  shuffle : MSE=6.10e-01 (>=1e-3) REJECTED                   OK
  --report: PASS

## Notes
- PySR captured the anti target via my_conj, NOT emlstar. Consistent with the
  Penning lesson: under MIXTE, pure anti-holomorphy is carried by my_conj/my_real,
  while emlstar keeps a holomorphic exp(x) part. Expected, not a defect.
- Negative control rejected at MSE (0.61 >> 1e-3): the tool does not fabricate
  structure on shuffled noise. Anti-SPARC guardrail working.

## Status
[ESTABLISHED] MIXTE tool calibrated end-to-end: detects holo, detects anti,
rejects noise. Safe to use for known-class work. NOT a discovery.
