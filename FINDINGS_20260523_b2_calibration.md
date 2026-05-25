# FINDINGS 2026-05-23 — B2 planar harmonic calibration

## What was tested
Detector = PySR + exact SymPy judge (Wirtinger d/dzbar) on B2 planar harmonic
mappings, Clunie--Sheil-Small shear. Closed form KNOWN and injected on purpose.
  phi(z)=z, omega(z)=z  =>  h(z) = -log(1-z),  g(z) = -z - log(1-z)
  D0 (control): f = h(z)              -> holomorphic expected
  D1 (shear):   f = h(z) + conj(g(z)) -> anti-holomorphic expected

## Exact commands
  python3 b2_shear_run.py --gen
  python3 b2_shear_run.py --which holo
  python3 b2_shear_run.py --which shear
  python3 b2_shear_run.py --report
(light config: maxsize=18, niter=80)

## Raw results (judge = arbiter, not PySR marker)
  D0 holo : judge_verdict=holomorphic,      dfdzbar=0,    mse=5.436560712928567e-06 -> PASS
  D1 shear: judge_verdict=anti-holomorphic, dfdzbar!=0,   mse=2.0868553218753585e-06 -> PASS

## Status: [ESTABLISHED] -- but CALIBRATION, NOT discovery
The conjugate in D1 is injected by hand in the dataset generator. The judge
recovering it confirms the instrument discriminates; it proves no new math.
PySR did not recover the exact canonical form: D1 uses my_imag (carries z̄
implicitly), mse ~2e-6 not ~1e-32 -> anti-holomorphic APPROXIMATION. Verdict
correct, form approximate. Calibration criterion = judge verdict only.
