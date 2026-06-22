# FINDINGS 2026-06-21e -- Two-band superconductor composite vortex: anti-coupling candidate (eta=0), 3 SPARC reservations open

## Status
[ESTABLISHED] (machine, judge_v2 + independent rotation oracle, code 0): in the
eta=0 (U(1)xU(1), independent phases) regime of a two-band superconductor, a composite
vortex Psi1+Psi2 with DIFFERENT windings is anti-holomorphic irreducible, confirmed by
two independent criteria. [CANDIDATE, not discovery] three SPARC reservations remain
open; the witness is not yet shown physically forced.

## Path that led here (orthogonal axis = number of fields, applied to physics)
The multi-field blind spot (FINDINGS_20260621d) is non-empty. Hunting a real two-scale
physical system: Hall MHD ruled out a priori (history 2026-06-04 mirror wall + velocity-
field category error). Chose two-band superconductors: order parameters Psi_j natively
complex (escape the real-trapped wall), two coherence lengths xi_j (type-1.5, measured
in MgB2, Sr2RuO4). Got the exact GL functional (Babaev-Carlstrom arXiv:1007.1965):
F = ... -eta|Psi1||Psi2|cos(t2-t1) ... The Josephson term LOCKS phases t1=t2 ->
single common phase -> module-trapped (WALL, Hecke-type). Only escape: eta=0 regime,
phases independent.

## Test and result (machine)
Model near a vortex core: Psi_j = (z/|z|)^{n_j} * exp(-c_j*|z|^2). Criterion: combination
Psi1+Psi2 anti-irreducible iff neither holo/real/module, confirmed by judge_v2 AND
rotation oracle. Results (all agree):
  Psi isolated (any n,c)                 -> module (pure phase x real modulus)
  same winding, DIFFERENT scale c1!=c2   -> module   (scale alone insufficient!)
  DIFFERENT winding n1!=n2, same scale   -> ANTI / NOT-module
  different winding AND scale            -> ANTI / NOT-module
MECHANISM (corrects initial hypothesis): the flip is driven by DIFFERENT WINDINGS
(topological), NOT by different scales. (z/|z|)^n = z^n*(z*zbar)^{-n/2}; different n =
different holomorphic powers z^{n1} vs z^{n2} = the "different holomorphic parts"
condition of the 0621d witness. Scale (real modulus) alone does not suffice.

## Three SPARC reservations (OPEN -- why this is a candidate, not a discovery)
(1) eta=0 is an IDEALIZATION. Real two-band SC has residual Josephson eta!=0 that locks
    phases -> module. Type-1.5 survives moderate eta, but eta=0 strict is a limit.
(2) Is the COMPLEX SUM Psi1+Psi2 a NATIVE observable? Total density |Psi1|^2+|Psi2|^2
    is real; the measured quantities (density, current) are not the complex sum. If the
    sum is posed by us, it is a SPARC artefact.
(3) Co-located DIFFERENT windings n1!=n2 may be ENERGETICALLY UNSTABLE. Babaev notes
    single-band-winding vortices have diverging energy; stable configs tend to co-wind.
Only if all three are answered by physics (forced, not posed) is this Project-A.

## Honest standing
Best candidate obtained so far -- structurally beats Kimi's Candidate 1 (which posed
zbar ad hoc): here the structure emerges from a real GL functional and a named physical
regime. But mathematically-real != physically-forced. The anti is real in the formula;
whether physics forces this exact observable is unresolved. NOT a discovery yet.

## Next
Lift the reservations against real physics, in order: (2) find whether any native
two-band observable IS the complex combination with different windings (interband
phase-difference observables? Leggett mode? interband Josephson current?); (1) check if
a near-eta=0 material exists or if weak residual coupling preserves the structure;
(3) check energetic stability of n1!=n2 configs (fractional/composite vortices lit.).
Each answer must be FORCED by physics, tested by judge + SPARC.

## Files
superconductor_vortex_probe.py (test, on machine), this FINDINGS. Builds on
FINDINGS_20260621d (multi-field criterion) and the orthogonal-axis method (0621c).
