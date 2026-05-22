# FINDINGS 2026-05-22 — Penning-trap sanity check (detector calibration)

Trace file (rule #12). English only.

## What is tested
Validate that the eml / eml-star / eml-zero detector classifies physically
motivated, **natively complex** maps with their mathematically guaranteed
holomorphic class. This is a CALIBRATION / SANITY CHECK, not a discovery: the
verdicts are known in advance.

Motivation: Penning-trap transverse motion is natively complex, rho = x + i*y
(Cohen-Tannoudji, College de France 1984-85). A time curve rho(t) is parametrised
by REAL t and is therefore NOT testable by a d/dz-bar judge (conj(t)=t -> SPARC
artefact). The testable objects are the maps of the complex plane the physics
provides:
  - cyclotron rotation                z -> e^{i theta} z              (holomorphic)
  - opposite-chirality / mirror        z -> e^{i theta} conj(z)        (anti-holomorphic)
  - squeezing / Bogoliubov             z -> cosh(r) z + e^{i phi} sinh(r) conj(z)  (hybrid)
The squeezing map is exactly the S(xi) operation in J. Foo's trapped-ion control
scheme; it mixes alpha and alpha* by construction -> natively anti-holomorphic.

## Exact command
    python3 simulate_penning_maps.py

Produces: penning_holo.csv, penning_anti.csv, penning_hybrid.csv,
penning_holo_shuffled.csv  (columns z_re, z_im, f_re, f_im).

## Raw result obtained so far
SymPy Wirtinger ground truth (authoritative, computed in the generator):
  HOLO     d f / d z-bar = 0                       -> HOLOMORPHIC
  ANTI     d f / d z     = 0                       -> ANTI-HOLOMORPHIC
  HYBRID   d f / d z = cosh(r),  d f / d z-bar = e^{i phi} sinh(r)  -> HYBRID

Self-audit of the generated data (this environment):
  corr(Re z, Im z) ~ -0.01  (natively complex, no SPARC degeneracy)
  max | f - exact map | ~ 1e-15 for all three maps (machine precision)
  negative control: Im(f) permuted, Re(f) identical (structure destroyed)

## Status
[ESTABLISHED] exact holomorphic class of each map (SymPy, above).
[PENDING]     detector recovery. The PySR run + verify_exact.py judge MUST be
              executed on the local machine. No MSE / no PySR verdict is
              produced or claimed here.

## Expected detector verdicts (to confirm by the judge on the local machine)
  penning_holo.csv          -> HOLO
  penning_anti.csv          -> ANTI
  penning_hybrid.csv        -> HYBRID
  penning_holo_shuffled.csv -> NOT clean HOLO (negative control)

A mismatch on any of the first three would indicate a detector bug, not a
physics result. A "clean HOLO" verdict on the shuffled control would indicate
the detector is over-eager and not trustworthy.

## RESEARCH_LOG.md line to append
2026-05-22 [ESTABLISHED-groundtruth/PENDING-detector] Penning-trap sanity check: 3 natively-complex maps (cyclotron=holo, mirror=anti, squeezing=hybrid) + shuffle control; exact SymPy classes set; detector run pending. trace: simulate_penning_maps.py, FINDINGS_20260522_penning.md
