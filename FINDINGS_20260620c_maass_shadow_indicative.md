# FINDINGS 2026-06-20c -- TRUE Maass weak harmonic shadow term judged ANTI (INDICATIVE, not certified)

## Status
[HEURISTIQUE] INDICATIVE numerical/symbolic signal, NOT bench-certified.
This is a CAPABILITY check (recovering a known property), NOT a discovery.
The object is THEORETICAL (arithmetic), NOT a physical concrete system.
Tested on a SINGLE term (n=1), not the full sum-over-n form.

## What was tested
The exact non-holomorphic part of a weight-k harmonic weak Maass form
(Bruinier-Funke decomposition), single term:
    f-_term = Gamma(1-k, -4*pi*n*y) * q^n ,   q^n = e^{2*pi*i*n*(x+i*y)}
with x = (z+zbar)/2, y = (z-zbar)/(2i), rewritten in independent Wirtinger
symbols (z, zbar) and passed to the repo judge judge_v2.certify_1field
(4-label: holomorphic / real-trapped / module-trapped / anti-holomorphic).

KEY POINT distinguishing this from an earlier caricature: the incomplete-Gamma
argument is y = Im(z), NOT |z|^2 = z*zbar. A simplified version Gamma(1/2, z*zbar)
(argument = modulus) is module-trapped (reducible, wall). The TRUE form, with
argument y = Im(z) coupled to q^n = e^{2*pi*i*n*z}, does NOT factor as
holo(z) * real_modulus(|z|^2) -- which is why it may escape module-trap.

## Exact command
    cd ~/Desktop/oxieml-star && python3 maass_shadow_judge.py
(maass_shadow_judge.py sha256 759cb390195f2d7a1a270a7934c0a9967c86ae00bfdd9ff179bad7ebe089e56e,
 imports the repo judge_v2.py sha256 36b289571224dc9c034d3f01a0c091d3730885e3ca6308dc8f10f0fbd383feab)

## Raw result (executed on Anthony's ThinkCentre M920q, against repo judge_v2.py)
    k=1/2  n=1   verdict = anti-holomorphic   d/dz nonzero=True   d/dzbar nonzero=True
    k=3/2  n=1   verdict = anti-holomorphic   d/dz nonzero=True   d/dzbar nonzero=True
    k=0    n=1   verdict = anti-holomorphic   d/dz nonzero=False  d/dzbar nonzero=True  (PURE anti)
    k=1    n=1   verdict = anti-holomorphic   d/dz nonzero=True   d/dzbar nonzero=True
    k=2    n=1   verdict = anti-holomorphic   d/dz nonzero=True   d/dzbar nonzero=True

The judge classifies every weight as anti-holomorphic and NOT module-trapped.
The factorization test (L = zbar*dlog(f)/dzbar real and product-only) fails,
so it is not a disguised module-trap. k=0 is pure anti (d/dz = 0).

## Reading (first object this session to clear all three walls)
This is the first object in the whole session that is NOT real-trapped, NOT
module-trapped, NOT a periodicity artefact. Maass forms (real-valued) were
real-trapped; Hecke characters (pure phase) were module-trapped; vortices
were module-trapped or periodic. The Maass weak harmonic shadow escapes all
three, indicatively.

## FOUR RESERVATIONS (must travel with this result -- do NOT overclaim)
1. INDICATIVE, not certified. The judge was NEVER calibrated on this
   transcendental class (incomplete Gamma) in the C-native bench. The module
   test rests on sp.simplify, which can fail SILENTLY on special functions:
   it may return "not factorable" when a factorization exists but SymPy did
   not find it. So "not module-trapped" could be a SymPy artefact, not a
   mathematical truth. THIS IS THE PRIMARY RESERVATION. It can only be lifted
   by extending the bench to transcendentals with an INDEPENDENT ground truth.
2. CAPABILITY, not discovery. That the Maass weak harmonic shadow is non-trivially
   anti-holomorphic is the DEFINITION of a harmonic weak Maass form (Bruinier-Funke
   2004). We recover a known property; we do not discover it. This validates the
   TOOL, it is not a mathematical finding. Never present as "we discovered the
   Maass shadow is anti".
3. THEORETICAL, not physical -- and it CONFIRMS the conjecture, not breaks it.
   The shadow is pure arithmetic (a modular form). The standing conjecture
   (Milo hash 4b688563) says independent anti lives in theoretical forms but
   NEVER in concrete physical objects. An independent anti in a theoretical
   form REINFORCES that conjecture; it does not refute it. Refutation would
   require this in a physical system. The Maass shadow is not one.
4. SINGLE TERM (n=1). A genuine harmonic weak Maass form is a sum over n.
   We judged one brick, not the assembled object.

## Next step (to lift reservation 1)
Extend cnative_bench.py to transcendental generators (exp, log, Bessel,
incomplete Gamma) WITH an independent reference oracle for the 4 labels,
so the judge's verdict on the incomplete-Gamma class becomes bench-certified
rather than indicative. Only then is "not module-trapped" trustworthy on this
object. Until then this result stays [HEURISTIQUE].

## Files
maass_shadow_judge.py (sha256 759cb390...e56e), this FINDINGS.

## UPDATE 2026-06-20d: reservation (1) LIFTED (with a scope bound)
Reservation (1) (judge not bench-calibrated on incomplete-Gamma; sp.simplify may fail silently) is LIFTED by FINDINGS_20260620d: the bench now certifies the judge on disguised transcendental module-traps (incomplete Gamma/Bessel/erf of |z|^2 -> module-trapped) via an INDEPENDENT rotation-generator oracle, 338/338. The judge does see through incomplete Gamma, so the shadow "anti, not module" is a genuine structural distinction, not a simplification failure. SCOPE BOUND: the oracle/judge cross-check is validated on REAL-modulus forms only; on complex phase-of-modulus (e^{i|z|^2}) they disagree, but the shadow is non-module for both so the lift holds. Reservations (2) capability, (3) theoretical, (4) n=1 stand.
