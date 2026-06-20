# FINDINGS 2026-06-20d -- C-native bench extended to transcendentals; oracle hardened; Maass-shadow SymPy reservation LIFTED

## Status
[ESTABLISHED] judge calibrated on the transcendental (incomplete-Gamma / Bessel / erf) class:
bench 338/338 on Anthony's machine, with an INDEPENDENT hardened reference oracle.
[DERIVATION] consequence: the Maass weak harmonic shadow verdict (anti, not module-trapped)
is no longer a possible SymPy artefact -- reservation (1) of FINDINGS_20260620c is LIFTED.

## What was done
1. Hardened the bench reference oracle ref_classify. The old module-trap test divided by
   (z*zbar)^k for INTEGER k in {1,2,3} and checked holomorphy of the quotient. That misses
   TRANSCENDENTAL module-traps (e.g. z*exp(|z|^2)): the modulus sits inside a special function,
   not an integer power. New test = ROTATION GENERATOR:
       R = z*d/dz - zbar*d/dzbar
   For f = holo(z)*M(z*zbar): R(M)=0 (modulus is rotation-invariant), so R(f)/f = z*holo'/holo
   depends on z ONLY (no zbar). This holds for ANY holomorphic factor, monomial or not, and is
   INDEPENDENT of the judge's criterion L = zbar*dlog(f)/dzbar (different operator, different
   direction). Oracle and judge now reach the same ground truth by two distinct routes.
2. Added 15 transcendental gold controls (6 module-trap, 3 real-trap, 3 anti, 2 holo, 1 mixed),
   including the critical disguised case z*Gamma(1/2,|z|^2) (incomplete Gamma of the MODULUS).

## Why this lifts the shadow reservation
Reservation (1) of FINDINGS_20260620c: sp.simplify might fail SILENTLY on incomplete Gamma and
mislabel a disguised module-trap as "anti", making the shadow verdict unreliable. The bench now
contains disguised transcendental module-traps with incomplete Gamma of |z|^2, whose TRUE label
is module-trapped, established by the independent rotation oracle. The judge classifies all 6
correctly as module-trapped (not anti). Therefore the judge DOES see through incomplete Gamma:
when an object is a transcendental module-trap, it is caught. So the judge's "anti, not module"
on the Maass shadow (incomplete Gamma of Im(z), NOT |z|^2) is a genuine structural distinction,
not a simplification failure.

## Methodology note (a regression caught a wrong first attempt)
A first hardened oracle used the rephasing RATIO f(e^{it}z)/f(z) independence test. It passed all
transcendentals but FAILED the regression case (z+1)*|z|^2 (non-monomial holomorphic factor):
the ratio (e^{it}z+1)/(z+1) depends on z, so the ratio test wrongly returned MIXED. The rotation
GENERATOR R(f)/f fixed this (it works for any holomorphic factor). The algebraic regression set
caught the error BEFORE delivery -- the transcendental-only set would have hidden it (all those
factors are monomials).

## Exact command
    cd ~/Desktop/oxieml-star && python3 cnative_bench.py

## Raw result (executed on Anthony's ThinkCentre M920q)
    generated/scored : 338 / 338    errors: 0
    PASS : 338/338    FAIL: 0
    Cross-tab diagonal:
      HOL            -> 70 holomorphic
      ANTI           -> 67 anti-holomorphic
      MIXED          -> 48 anti-holomorphic
      MODULE_TRAPPED -> 76 module-trapped   (incl. 6 transcendental disguised module-traps)
      REAL_TRAPPED   -> 77 real-trapped
    Report: cnative_bench_report_20260620T121620Z.json
    backup before change: cnative_bench.py.bak_20260620_pretranscend

## What remains (the other three shadow reservations stand)
- (2) CAPABILITY not discovery: the anti shadow is the Bruinier-Funke definition (known 2004).
- (3) THEORETICAL not physical: CONFIRMS conjecture 4b688563, does not refute it.
- (4) single term n=1 only (full Maass form is a sum over n).
Lifting reservation (1) upgrades the shadow result from [HEURISTIQUE] to [DERIVATION] on the
TOOL side (judge certified on this transcendental class); the object remains a theoretical
capability check, NOT a physical discovery.

## Files
cnative_bench.py (oracle hardened + 15 transcendental controls), this FINDINGS.

## RESERVATION (auditor, 2026-06-20): rotation oracle is WIDER than the judge
The rotation oracle returns MODULE iff f = h(z)*M(z*zbar) for ANY M (real OR complex); the judge requires M REAL (the L_real test). They coincide ONLY on real-modulus forms -- the entire transcendental corpus here (exp, besselj, uppergamma, erf, log of |z|^2 are all real). On a complex phase-of-modulus they DISAGREE. Sandbox-verified 2026-06-20:
  z*exp(|z|^2)  -> oracle MODULE, judge module-trapped  (agree)
  z*exp(i|z|^2) -> oracle MODULE, judge anti            (DISAGREE)
  exp(i|z|^2)   -> oracle MODULE, judge anti            (DISAGREE)
So "two routes to the SAME ground truth" holds ONLY on the real-modulus class, not in general: a bounded cross-check.
This does NOT affect the shadow: Gamma(1-k,-4*pi*n*y)*q^n (arg y=Im z, not |z|^2) is NON-module for BOTH oracle and judge (agree), so the lift of reservation (1) stands (sandbox: shadow-like Gamma(1/2,-y)*e^(2i*pi*z) -> oracle not-module, judge anti).
OPEN DEFINITIONAL QUESTION (do not resolve unilaterally; settle vs history before any LLL/gaussian-packet target): is a phase-of-modulus factor e^{i*g(|z|^2)} module-trapped (reducible) or genuine anti? Judge says anti; rotation oracle says module. Adding z*exp(i|z|^2) to the bench now would FAIL -- that FAIL is a DEFINITIONAL signal, not a code bug.
