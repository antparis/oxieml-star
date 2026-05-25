# FINDINGS 2026-05-25 — Landau levels: detector reads poly-analytic degree

## Goal
Test (B): does the eml-star detector recover the growing zbar-degree of Landau
levels? Real physical system (electron in magnetic field), z = spatial position
(NOT time/frequency -> no Kramers-Kronig oracle). Polynomial part only (no Gaussian
e^{-|z|^2/4}), symmetric gauge, m=2 fixed, n in {0,1,2}.
Targets (verified exactly via SymPy assoc_laguerre):
  n=0: z**2                              (0 zbar, holomorphic)
  n=1: -z**3*zb/2 + 3*z**2               (1 zbar)
  n=2: z**4*zb**2/8 - 2*z**3*zb + 6*z**2 (2 zbar)
Script: landau_test.py (N=1500, niter=80, pop=300, seed 42). Run on PC Linux.

## Results — all three [ÉTABLI] (executed on PC Linux + judged by verify_exact.py)

n=0 (target z**2, 0 zbar):
  PySR best_mse = 2.48e-29. Best simple form: x0*x0.
  Judge verify_exact.py --formula "x0*x0" -> simplified z**2 -> df/d(zbar)=0 -> HOLOMORPHIC.
  Detector recovers the holomorphic target with NO conjugation (no my_conj). Clean.

n=1 (target with 1 zbar):
  PySR best_mse = 3.21e-06 (< 1e-3). Formula uses my_conj.
  Judge -> df/d(zbar) != 0 -> ANTI-HOLOMORPHIC. The my_conj marker is here a TRUE
  signal (judge confirms it does not cancel out).

n=2 (target with 2 zbar):
  PySR best_mse = 1.81e-31 (< 1e-3). Formula uses my_abs2 (=z*zbar) nested.
  Judge -> simplified polynomial contains a z**4*zbar**2 term -> df/d(zbar) != 0 ->
  ANTI-HOLOMORPHIC, AND at the correct degree 2 in zbar.

Contrast certified: holomorphic level -> no conjugation; anti-holomorphic levels ->
conjugation captured, with degree matching the Landau quantum number.

## Interpretation — what this IS and is NOT
STATUS: this is a VALIDATION, not a discovery. The poly-analytic structure of
Landau levels is known physics (~90 years). The detector confirms it; it does not
reveal anything unknown about nature.

What is genuinely shown:
  - On a real physical system (electron in a magnetic field), with z = spatial
    position (NOT time/frequency, so NO Kramers-Kronig oracle), the pipeline
    PySR + SymPy Wirtinger judge correctly separates holomorphic (n=0) from
    anti-holomorphic (n=1, n=2) levels, and reads the zbar-degree.
  - This is the first non-trivial POSITIVE signal of the session: all other real
    datasets (SPARC, VLA, EHT, UMD detS) were null or symmetry-dictated oracles.

Caveats (kept explicit):
  - n=1 fit (1e-6) is good but far less exact than n=0 and n=2 (1e-29, 1e-31):
    the operator APPROXIMATES n=1 rather than reconstructing it exactly.
  - Targets are the polynomial part only; the universal Gaussian confinement factor
    e^{-|z|^2/4} was removed by design (it would make every level trivially anti-holo).
    Representation = Schrodinger / symmetric gauge (Haldane: other representations
    make all levels holomorphic; the verdict is representation-dependent and stated).
