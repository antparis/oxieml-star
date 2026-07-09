# FINDINGS 2026-07-09 — Genericity audit (#045): the class forces the properties, the choices only pick the specimen — wall existence generic (location = weight asymptotics), chiral drift law s-independent, log-periodic calendar survives random choirs

## What
Anthony's question, verbatim intent: "did we manufacture these results,
or would ANY object of this kind be forced to show them?" Orthogonal axis
applied one layer above #043: vary the MODEL itself — weight decay
exponent s (1/lambda^s for s = 1, 2, 3), geometric weights r^m, and a
fully RANDOM choir (random weights, random log-uniform ladder spacings) —
and measure what survives.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-09)
```
cd ~/Desktop/oxieml-star && timeout 250 python3 kernel_genericity_audit.py
```

## Raw result (machine output, identical to sandbox)
A. WALL: term growth flips exactly at the predicted wall in EVERY model —
   polynomial weights s = 1, 2, 3: shrink at x = 0.98, GROW at x = 1.02
   (wall at 1 for all s); geometric weights r = 0.5: shrink at x = 1.90,
   GROW at x = 2.10 (wall at 1/r = 2). Wall EXISTENCE is generic for
   infinite ladders; its LOCATION is the specimen's signature (weight
   asymptotics). [Auditor's earlier claim "the wall will move" CORRECTED:
   it moves only under geometric weights; every polynomial decay pins it
   at 1.]
B. CHIRALITY (route #040: theory formula + polylog control):
   (i) disc Phi(x,s,a) = 2*pi*i x^(-a) (ln x)^(s-1)/Gamma(s) controlled
   machine-exact at a = 1 via Phi(x,s,1) = Li_s(x)/x crossings at x = 2:
   relative error 3.2e-10 / 5.7e-10 / 2.0e-10 for s = 1 / 2 / 3.
   (ii) complex a = 1+c [DERIVATION inherited from the controlled
   formula, same status discipline as #040]: the jump phase is
   pi/2 + (kappa/2delta) ln x plus the argument of a REAL POSITIVE
   envelope (ln x)^(s-1)/Gamma(s) — the drift law
   (kappa/2delta) ln(x2/x1) = +3.9714 deg between x = 1.5 and 3.0 is
   IDENTICAL at every s; reciprocal (a real): drift 0. The envelope is
   the specimen; the twist is the class.
C. CALENDAR: (i) s-independence is an ALGEBRAIC IDENTITY (the real
   envelope factors out of the modulus); the s-common profile's dips sit
   at u = 10.00 / 29.98 / 49.93 / 69.81 — identical to #044. (ii) A fully
   RANDOM choir (N = 5, weights in [0.5, 1.5], log-uniform spacings,
   seed 20260709) still produces recurring rendezvous (u = 20.00, 59.24
   over u <= 80). (iii) Reciprocal random choir: max - min = 0.00e+00
   exactly.

## Verdict — the answer to the manufactured-vs-forced question
ON MACHINE: our choices fix the OBJECT (which wall location, which
calendar schedule, which envelope); the CLASS of one-way kernels fixes
WHAT THE OBJECT MUST DO (a wall exists; the crossing twists with the
same drift law; the relief keeps log-periodic rendezvous; the reciprocal
twin shows none of it). Nothing in the pipeline manufactures the
structure: it survives changing the weight law, the decay exponent, and
even randomizing the choir — and it dies, exactly and always, on the
reciprocal control.

## Method incident (documented, part of the answer itself)
A naive lerchphi cut-crossing was tried first for panel B and produced
s-dependent garbage (-33 / -52 / -57 deg): mpmath's lerchphi is
branch-smooth on x > 1 for complex a — a lesson ALREADY GRAVED in #040
that the auditor violated; the sandbox caught it before delivery and the
panel was corrected to the #040-validated route. A complacent pipeline
would not have refuted its own auditor mid-test.

## Status
- Panels A, B(i), C: [ESTABLISHED machine] (run 2026-07-09, identical to
  sandbox, no hardcoded verdict).
- Panel B(ii) (complex-a drift law): [DERIVATION] via the machine-
  controlled formula — same status as #040's a-complex case.
- Says nothing about nature. Shared FORM, never identity.

## Opens (traced, not started)
- Wall-location law: sharpen "location = weight asymptotics" into a
  stated theorem (radius of convergence of the weight series) — cheap,
  possibly one paragraph.
- Floor as phasor statistics (carried over from #044) — still the best
  analytic candidate.
- Prior-art pass on log-periodicity/DSI before any v3 wording (graved
  in #044, still pending).

## Traces
- kernel_genericity_audit.py (harness; the refuted naive method and its
  correction are documented in the script itself)
- FINDINGS_20260709_logperiodic_rendezvous.md (#044)
- FINDINGS_20260709_orthogonal_audit.md (#043)
- This file: FINDINGS_20260709_genericity_audit.md
