# FINDINGS 2026-06-22d -- Inverse-square supercritical wavefunction is module-trapped (NEW WALL) + judge_v2 blind spot found

## Status
[ESTABLISHED] negative result (sandbox, 3 independent tests concordant; to replay on
machine before final). The supercritical inverse-square-potential wavefunction's radial
part r^(is) = |z|^(is) is MODULE-TRAPPED, not a genuine anti candidate. Also REVEALS a
blind spot in judge_v2: its module-trapped criterion misses L = pure imaginary constant.

## Origin
Applying the "anti has multiple faces" idea: reopened Aharonov-Bohm (only natively-complex
wall of the three; galaxies & MHD-Hall stay sealed = real-data walls, mirror theorem).
History confirmed AB form z^(m+a/2) zbar^(-a/2) is module-trapped by EXACT identity
(real power -> module). PIVOTED to the right question: find a physical variant where zbar
carries a COMPLEX exponent or additive log (the only forms escaping module-reduction).
web_search found: INVERSE SQUARE POTENTIAL, supercritical regime kappa>kappa_cr, gives
wavefunction Q^(-i|s|+1/2) = Q^(1/2) e^(-i|s| log Q) -- a COMPLEX exponent FORCED by
physics (crossing critical coupling = scale anomaly / PT-symmetry-breaking transition;
arXiv:2107.01511, 0909.3477). Looked promising: complex exponent, physically forced.

## The decisive test (3 independent methods, all concordant)
Planar form psi = e^(im theta) r^(-1/2+is); the core is the radial r^(is)=(z*zbar)^(is/2).
[1] Symmetry z<->zbar: f - f(swap) = 0 -> INVARIANT = function of the modulus.
[2] Rotation oracle R = z*d/dz - zbar*d/dzbar: R(f)/f = 0 -> rotation-invariant, no phase
    chirality. (Independent of judge_v2's criterion.)
[3] |z|^(is) = e^(is log|z|) = pure phase (modulus 1) winding with log|z|.
ALL THREE say: function of the SYMMETRIC modulus -> reducible -> MODULE-TRAPPED. The
complex exponent is carried by the MODULUS (z*zbar, symmetric), not by zbar alone.
=> NEW WALL. Like AB but with imaginary exponent instead of real. Not a Project-A candidate.

## Judge blind spot found (concrete fix needed)
Under criterion L = zbar*d/dzbar(log f):
  |z|^(is) spirale      : L = i*s/2  (PURE IMAGINARY CONSTANT)  Lreal=False prodonly=True
  AB module z*zbar^0.5  : L = 1/2    (real constant)            Lreal=True  prodonly=True -> module
  genuine anti z+zbar   : L = zbar/(z+zbar)                     Lreal=False prodonly=False -> anti
  log additif log(zbar) : L = 1/log(zbar)                       Lreal=False prodonly=False -> anti
judge_v2 tests "L real + product-only -> module-trapped" and so MISCLASSIFIES |z|^(is) as
"anti(irreducible?)" because L is imaginary (not real), even though prodonly=True.
FIX: module-trapped test should accept L = constant (real OR pure imaginary) + product-only.
A constant L (any phase) means the log-derivative has no z,zbar dependence = modulus power.
This blind spot may have produced spurious "anti?" verdicts elsewhere; re-audit recommended.

## Refined navigation law
A complex exponent is NOT sufficient for genuine anti. It must be carried by zbar ALONE
(z̄^(is) -> judge says anti-holomorphic pure), NOT by the symmetric modulus |z|^(is)
(= (z*zbar)^(is/2), module-trapped). Genuine transcendental anti still requires: additive
log(zbar) with complex coef, OR complex exponent on zbar alone -- never on the modulus.
No physics has yet produced the zbar-alone form; the inverse-square gives modulus form.

## Walls status after this session
- Galaxies / SPARC: sealed (real data, encoding artefact, mirror theorem). NOT reopened.
- MHD Hall frozen: sealed (real, mirror-locked). NOT reopened.
- Aharonov-Bohm z^a zbar^b real powers: sealed (module-trapped, exact identity).
- Inverse-square supercritical |z|^(is): NEW sealed wall (module-trapped, imaginary expo).

## Next
(1) Replay the 3 tests on machine to confirm [ESTABLISHED]. (2) Optionally patch judge_v2
to catch L = imaginary constant + product-only as module-trapped (closes blind spot),
backup first. (3) The zbar-alone complex-exponent form remains the unfound target.

## Files
this FINDINGS; sandbox tests (to be scripted for machine replay). Builds on
FINDINGS_20260604_aharonov_bohm.md (AB module-trapped, real power).
