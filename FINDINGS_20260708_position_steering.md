# FINDINGS 2026-07-08 — Position steering (#042): the relief is ANCHORED in position but SWITCHABLE by phase; the blur has an incompressible floor

## What
Follow-up of #041's opens: can a richer choir MOVE the interference
features along the one-way kernel cut (full motion capture)? And what is
the blur law (contrast decay with N at fixed spread)? Four panels: real
weight lever (A), complex phase lever (B), blur exponent fit (C),
reciprocal control with complex weights (D). Two auditor predictions
announced before code were REFUTED by the machine — documented below.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-08)
```
cd ~/Desktop/oxieml-star && timeout 200 python3 kernel_steering_test.py
```

## Raw result (machine output, identical to sandbox)
A. WEIGHT LEVER (N=3, offsets delta = 0.3/3/30; w2 = 0.25..4.0):
   dip position FROZEN at x = 179.26 across the whole weight range;
   only the contrast moves (0.2061 -> 0.0870). Real amplitude is a
   VOLUME knob, not a steering wheel.
   [Auditor prediction A: "dip moves modestly with weights" — FALSE.]
B. PHASE LEVER (w2 = e^{i phi}, same offsets):
   the dip does NOT slide. It SWITCHES: at phi = 135 deg it jumps from
   x = 179.26 (upper edge) to x = 1.17 (the wall), then returns at
   phi = 180 deg. A transient interior extremum exists for
   phi = 45..135 deg (count 1), gone outside. Contrast is also strongly
   phase-dependent (0.0605 at 135 deg vs 0.3887 at 270 deg).
   The phase CHOOSES which basin wins (topological switch); it does not
   translate the relief continuously.
   [Auditor prediction B: "clean continuous steering across the window"
    — FALSE in form; a phase control exists but it is discrete.]
C. BLUR LAW (fixed spread delta in [0.3,30], N = 2..256):
   contrast 0.21831 -> 0.04839, fitted exponent (N>=8) p = 0.131 —
   NOT the predicted 0.5 (incoherent 1/sqrt(N)); the decay SATURATES
   toward a floor ~0.048 (tail: 0.05077 / 0.04917 / 0.04839).
   The blur has an INCOMPRESSIBLE RESIDUAL RELIEF: a crowded choir never
   fully erases the structure. Plausible mechanism (untested, traced as
   open): the extreme windings of the spread dominate the tail.
   [Auditor prediction C: "p ~ 0.5, rejoining accumulation law #008"
    — FALSE; the #008 bridge does not hold in this form.]
D. RECIPROCAL CONTROL (complex weights, real offsets): machine-flat —
   contrast 1.48e-16 / 1.99e-16 / 5.55e-17 at phi = 0/90/180 deg,
   0 extrema. Complex weights alone create no structure in x; everything
   above is a one-way phenomenon.

## Verdict
Full motion capture is REFUTED at N=3: the relief's positions are
ANCHORED (weights and phases do not translate them). What exists instead
is richer than a failure: (i) a PHASE SWITCH — a discrete, topological
control where the initial phase selects which anchored basin (wall side
vs far side) carries the main dip, with a transient interior extremum in
the crossover window; and (ii) a BLUR FLOOR — the N-averaging of #041
does not extinguish the relief but saturates at an incompressible
residual (~0.048 at this spread). The anchoring is consistent with #041
(dip frozen at pair level): position appears to be set by the GEOMETRY
of the winding spread, not by the excitation of the choir.

## Status
- Panels A-D: [ESTABLISHED machine] (run 2026-07-08, identical to
  sandbox, no hardcoded verdict; two auditor predictions refuted and
  documented — the machine corrects the auditor, as designed).
- Route: disc linearity + theory formula, controlled machine-exact on
  the a=1 dilog (#039/#040); a-complex jumps inherit [DERIVATION] via
  the Lerch->dilog reduction, as before.
- Floor mechanism (extreme-winding dominance) is [CONJECTURE], traced.
- Says nothing about nature, space, or physical localization. Shared
  FORM, never identity.

## Opens (traced, not started)
- Switch cartography: map the basin boundary in (phi, weight, offset)
  space — is the 135-deg flip a codim-1 wall? Does N>3 add basins?
- Floor law: how does the residual contrast depend on the spread S?
  (Prediction to frame later: floor set by the two extreme windings.)
- Anchor law: what sets x = 179.26 and x = 1.17? (Window edges are
  suspicious — widen the window before interpreting the anchors.)
- v3 boundary section: the quartet #039-#041 plus the switch/floor pair.

## Traces
- kernel_steering_test.py (harness, sandbox-tested and machine-run
  2026-07-08)
- FINDINGS_20260708_tear_localization.md (#041, the opens this answers)
- This file: FINDINGS_20260708_position_steering.md
