# FINDINGS 2026-06-21d -- Multi-field anti-coupling criterion: the blind spot is NON-EMPTY

## Status
[ESTABLISHED] (executed on Anthony's machine, judge_v2 + independent rotation oracle,
code 0): a holomorphic-coefficient combination of SEPARATELY-REDUCIBLE module fields
can be irreducibly anti-holomorphic when the real moduli differ. The multi-field blind
spot of the single-field judge is NON-EMPTY. [RESERVATION] the witness is POSED, not
physically forced -- this is a tool justification, NOT a physical discovery.

## Why this question (orthogonal axis = number of fields)
The single-field judge certify_1field sees one field f(z,zbar) at a time. The
"number of fields" orthogonal axis asks: for a system of several distinct scalar
fields f1, f2, ..., is there anti structure in their COUPLING that no single field
reveals alone (scenario 3)? This is the only multi-field case not reducible to
judging each field separately. NOTE (history, 2026-06-04 theorem): a velocity field
w = vx - i*vy is the WRONG object (complex by construction, category error, retired);
the discriminant is defined on scalar fields. So "multi-field" here = several distinct
SCALAR fields, sense (a), not decomposing one object into re/im parts.

## The criterion (correct one; first attempt was wrong)
FIRST ATTEMPT (rejected by calibration): "ratio f2/f1 is anti" -> FALSE. Counterexample
caught at calibration: f1=z (holo), f2=|z|^2 (real), ratio=zbar (anti) -- but this is a
DIVISION ARTEFACT, no real coupling. Dividing fields manufactures zbar. Discarded.
CORRECT CRITERION (no division): the coupling is anti-irreducible if a holomorphic
combination a(z)*f1 + b(z)*f2 is neither holo, real-trapped, nor module -- confirmed
by BOTH judge_v2 AND the independent rotation oracle (R = z*d/dz - zbar*d/dzbar;
module iff R(f)/f depends on z only). Two independent criteria must agree.

## Calibration on machine (judge_v2 + rotation oracle, all agree, code 0)
  CANDIDATE  z^2*e^{|z|^2} + z*e^{2|z|^2} (DIFFERENT moduli) -> anti / NOT-module
  CONTROL    z^2*e^{|z|^2} + z*e^{|z|^2}  (SAME modulus)     -> module / module
  CONTROL    z*e^{|z|^2}  (single module)                    -> module / module
  CONTROL    gold additive anti A*z + B*zbar                 -> anti / NOT-module
Judge and INDEPENDENT oracle agree on all four. The flip is driven by the DIFFERENCE
of real moduli (e^{|z|^2} vs e^{2|z|^2}, two scales), not by summation per se: same
modulus stays module. No single common real modulus can be factored out -> the zbar
is irreducible. This is NOT a single-field judge limitation: an independent criterion
(rotation oracle) confirms anti, so it is not a false-anti on sums.

## What is established vs reserved
ESTABLISHED: (1) a correct, calibrated multi-field anti-coupling criterion exists;
(2) the multi-field blind spot is non-empty -- sums of different-scale real moduli are
irreducibly anti while each component module is reducible; (3) confirmed by two
independent criteria on Anthony's machine.
RESERVED / NOT a discovery: the witness z^2*e^{|z|^2}+z*e^{2|z|^2} is POSED (a
hand-built combination), not DERIVED from physics. At the Project-A level this proves
the multi-field tool has a reason to exist; it is NOT a physical finding. SPARC rule
stands: is the structure physically FORCED or POSED? Here POSED.

## Next
Find a REAL two-scale physical system (two coupled scalar fields with DIFFERENT
physical length/energy scales) where such a different-moduli combination is the natural
observable -- e.g. the two generalized vorticities of Hall MHD (scales 1 and d_i,
flagged in history 2026-06-04), or a two-band / two-gap system. Then run this criterion
and submit any anti to the SPARC examination. Only a forced (not posed) witness would
be a Project-A candidate. Build a proper multi-field judge module if the lead survives.

## Files
multifield_probe_calib.py (criterion + calibration, on machine), this FINDINGS.
Builds on the orthogonal-axis method (FINDINGS_20260621c).
