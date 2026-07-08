# FINDINGS 2026-07-08 — The one-way kernel's branch tear is CHIRAL: the jump's phase rotates along the cut by the exact law x^(-c); the reciprocal tear is not

## What
Extension of #039, framed from Anthony's questions (does the jump VARY? does
it GIVE a direction? is there a RHYTHM across multiple crossings? what do
SEVERAL tears do together?). Four panels on the one-way kernel
K ~ Phi(x, 2, 1+c), c = -i*kappa/(2*delta) (complex offset = the one-way
signature), against the reciprocal dilog control (a = 1, real).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-08)
```
cd ~/Desktop/oxieml-star && timeout 200 python3 kernel_crossing_test.py
```

## Raw result (machine output, identical to sandbox of 2026-07-05)
ROUTE CONTROL: polylog cut measured vs theory 2*pi*i*ln(x): worst
  |diff| = 2.7e-9 over x = 1.2..5.0 (exact at x=2.0: 7.9e-19). Route valid.
B. JUMP PROFILE: (i) zipper — |disc| = 6.28e-4 at x=1.0001 (vanishes at the
  wall), grows beyond; (ii) PHASE: one-way jump phase rotates
  +90.0057 deg (x=1.001) -> +99.2214 deg (x=5), total drift +9.2157 deg;
  reciprocal control frozen at +90.0000 deg at every x. The rotation law
  is EXACT: jump_ow/jump_rec = x^(-c), verified digit-for-digit at x=2
  (+0.997599+0.069259j both sides, modulus 1.000000).
A. ORIENTATION DIFFERENTIAL: crossing is odd (up = -down, |up+down| = 0.0)
  in BOTH kernels — oddness is NOT the signature. The differential lives
  entirely in the phase law of panel B: rotating (one-way) vs frozen
  (reciprocal). The one-way tear is CHIRAL; the reciprocal tear is not.
C. STACKING RHYTHM: monodromy staircase at x=1.5, sheets n=0..5:
  successive steps all equal (-0.068846+1.697012j), ratios = 1 to
  max |ratio-1| = 4.3e-21. Rhythm is ARITHMETIC (equal steps) — a regular
  staircase, not a fractal cascade. Auditor prediction confirmed;
  Anthony's fractal hypothesis cleanly ruled out on this axis (a result,
  not a disappointment).
D. CHOIR (two ladders, delta=1 and delta=2): tears stack on the same ray
  x>1; jumps ADD linearly (disc is linear) BUT phases wind differently
  (+93.97 vs +91.99 deg at x=2) -> nonzero interference term
  |j1+j2|^2 - |j1|^2 - |j2|^2 = +9.478067. Locked additively in value,
  independent in phase law: the choir's total tear INTERFERES.

## Verdict
The crossing of the one-way kernel's boundary is ORIENTED in a precise
sense: not by the sign of the jump (odd in both kernels) but by a CHIRAL
PHASE LAW — the jump's phase rotates along the cut as x^(-c), where c is
exactly the complex offset produced by one-way coupling. The reciprocal
control has no rotation. Answers to Anthony's framing: the jump VARIES
(zipper opening from 0 at the wall) and it DOES give a direction (through
its phase, position-dependently — "head up or down depending on where you
stand on the tear"); the multi-crossing rhythm is arithmetic; multiple
tears interfere through their phase windings.

## Status
- Panels A-D + route control: [ESTABLISHED machine] (run 2026-07-08,
  identical to 2026-07-05 sandbox, no hardcoded verdict).
- Scope note: kernel-side jumps are computed by the THEORY FORMULA
  (disc Phi = 2*pi*i x^(-a) ln x), controlled machine-exactly on the a=1
  dilog case; the a-complex case inherits [DERIVATION] status from the
  Lerch->dilog reduction (mpmath lerchphi remains branch-smooth on x>1,
  library choice — direct eps-probe inapplicable, as in #039). The x^(-c)
  RATIO law between the two kernels is exact within the formula and is
  the certified content.
- Says nothing about nature, black holes, or physical horizons. Shared
  FORM with "oriented horizon" pictures — never identity (Anthony's own
  framing: "peut-etre qu'il n'y a pas de lien, tout simplement").

## Opens (traced, not started)
- #041 candidate (Anthony's motion-capture idea): N tears with detuned
  phases — can opposed tears CANCEL (conflict)? does an interference
  pattern along the cut create emergent "here vs there" structure
  (localization) that no single tear carries? threshold in N (2, 3, 20,
  200): sudden switch or #039-style progressive sharpening? With the
  mandatory reciprocal control.
- Candidate material for a future paper v3 boundary section, alongside
  #039 (open question 3).

## Traces
- kernel_crossing_test.py (harness, sandbox-tested 2026-07-05, machine-run
  2026-07-08)
- FINDINGS_20260705_kernel_boundary.md (#039, the base result)
- This file: FINDINGS_20260708_chiral_tear.md
