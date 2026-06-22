# FINDINGS 2026-06-17 -- [ESTABLISHED on this case] Newman-Janis (spin-as-imaginary-part, xi = r + i a cos theta) does NOT break the conjecture: it falls into REALITY-LOCK (a), and constitutively so. The Kerr central function 2Mr/rho^2 = M/xi + M/xibar is SEPARABLE (mixed d2/dxi dxibar = 0) BUT REAL, so the anti-holo part is the exact FORCED MIRROR of the holo part. New methodological refinement: mixed=0 alone is insufficient -- it must be coupled with a reality test (mixed=0 + real => reality-lock; mixed=0 + non-real => independent z-bar, as in the toy model). 6th concordant case, the most "definitive" (reality is the GOAL of the algorithm). Gravity sector now closed.
## The candidate and why it was the last serious hope
Newman-Janis builds Kerr from Schwarzschild by a COMPLEX coordinate shift r -> xi = r + i a cos theta,
encoding the black-hole spin a as the IMAGINARY part of a coordinate -- the one place in classical
gravity where an imaginary part is "physical" (spin), not constructed from real arguments. The hope:
it might escape spinor-lock (d). It does not.
## Test (executed on Anthony's machine)
With xi = r + i a cos theta (ac := a cos theta real), rho^2 = xi*xibar, r = (xi+xibar)/2:
  Kerr central function 2 M r / rho^2 = M/xi + M/xibar.
  mixed d2/dxi dxibar = 0  => SEPARABLE.
  physical value = 2 M r / (r^2 + ac^2), Im = 0 => REAL.
  anti part M/xibar == mirror of holo M/xi (xi<->xibar): TRUE.
=> separable AND real => anti-holo is the FORCED MIRROR of holo => REALITY-LOCK (a).
## Methodological refinement forced by this case
The mixed-derivative discriminant alone is NOT sufficient:
  mixed == 0 AND real     => reality-lock (a): anti = forced mirror of holo (Kerr/Newman-Janis).
  mixed == 0 AND non-real => independent z-bar (the toy model, e1c7318e), would break conjecture.
So the pipeline test for separable objects must be: mixed==0 THEN reality test. Add to the toolkit
alongside verify_exact.py and the mixed discriminant.
## Why this closes the gravity sector (constitutive, not accidental)
Newman-Janis CANNOT escape reality-lock because the GOAL of the algorithm is to produce the Kerr
metric, which is real (a spacetime geometry has a real metric by definition). The spin-as-imaginary-
part is a calculational device; the physical output is real. Classical gravity is structurally
reality-locked: every physical object is a real metric / real curvature.
## Status, honest limits, and a caution (Milo's reserve, accepted)
[ESTABLISHED on this case] -- certified on Anthony's machine. 6th concordant did-not-break system
(T' 616640ad, toy e1c7318e, QGT f5df28ad, Tricorn 3cbada22 certified; chiral SC, exceptional point,
Psi4 static, Newman-Janis -- last is certified here). CAUTION: this case was predictable once one
recalls the metric must be real; accumulating a 7th/8th concordant case adds little. The conjecture
is now at the point where the next step is NOT "one more case" but EITHER the general exhaustion
argument (does every measured complex observable fall into a-e?) OR a candidate of a radically
different nature. Gravity sector exhausted (reality-locked structurally). The lasting gain here is
the mixed+reality refinement, independent of the Newman-Janis verdict.
Files: newman_janis sandbox/machine test (this session). Arbiter = Anthony's machine (done).
