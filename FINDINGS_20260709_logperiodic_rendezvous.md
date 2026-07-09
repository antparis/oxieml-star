# FINDINGS 2026-07-09 — Log-periodic rendezvous (#044): the exact structure behind the #041/#042 "anchors" — the relief is an almost-periodic function of log scale, calendar set by the winding spread, one-way only

## What
Closure of the arc opened by the #043 audit. The traced conjecture is
upgraded to an EXACT reduction: with the trivial 1/x envelope removed,
the normalized relief equals, for ALL x > 1 (not asymptotically),
    P(u) = | sum_k w_k exp(i nu_k u) |,  u = ln x,  nu_k = kappa/(2 delta_k)
— a finite sum of unit phasors rotating in log scale: almost-periodic by
construction. Four machine panels verify the consequences.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-09)
```
cd ~/Desktop/oxieml-star && timeout 200 python3 kernel_logperiod_test.py
```

## Raw result (machine output, identical to sandbox)
A. N=2 EXACT PERIODICITY (delta = 1, 3): theory T = 2*pi/|nu1-nu2| =
   94.247780; 8 dips found, spacings 94.243..94.256, max |spacing - T| =
   7.89e-3 — equal to the sampling step (grid resolution, not a law
   deviation; panel C's mean-based measure is tighter).
B. N=3 RECURRENCE (the #041/#042 config, delta = 0.3/3/30), u in
   [0.05, 80] (x up to ~6e34): 4 deep dips at u = 10.00 / 29.98 / 49.93 /
   69.81, spacings 19.98 / 19.95 / 19.88 (near the extreme-winding beat
   2*pi/(nu_max - nu_min) = 19.04; almost-periodic, not strictly
   periodic, as expected for 3 incommensurate frequencies).
   KEY RESOLUTION: the old windows saw u <= 5.3 (x <= 200) — ZERO deep
   dips inside. The "fleeing anchors" of #041/#042 were not even these
   rendezvous: they were the partial descents toward the FIRST one
   (at x ~ 2.2e4), which no old window reached.
C. PERIOD LAW (N=2, delta_2 = 2/3/6/12): T_measured vs T_theory =
   125.6650/125.6637, 94.2486/94.2478, 75.3987/75.3982, 68.5435/68.5438
   — |diff| <= 1.3e-3 at every spread. The winding spread SETS the
   rendezvous calendar: T = 2*pi/|delta nu|.
D. RECIPROCAL CONTROL (nu_k = 0): max - min = 0.00e+00, zero dips —
   the relief is EXACTLY constant; the calendar exists one-way only.

## Verdict — the arc #041 -> #044 closes coherently
The true structure along the one-way kernel's cut is LOG-PERIODIC
RENDEZVOUS: interference dips recurring indefinitely in ln x, with a
calendar set by the spread of phase-winding speeds (T = 2*pi/|dnu|,
exact at N=2; almost-periodic at N >= 3), existing only on the one-way
side (reciprocal control exactly constant). This replaces, on machine
evidence, the provisional #042 pictures ("anchored positions",
"topological switch"), which the #043 audit had already downgraded to
window artifacts: every finite window catches partial descents toward
(or one of) the rendezvous. The story is now self-consistent across
six entries: wall from number (#039), chiral crossing (#040), relief
from detuning (#041), provisional anchors (#042, caution graved),
audit and downgrades (#043), exact log-periodic law (#044).

## Status
- Reduction P(u) = |sum w_k e^{i nu_k u}|: EXACT algebraic identity
  (modulus factorization), machine-faced by all four panels.
- Panels A-D: [ESTABLISHED machine] (run 2026-07-09, identical to
  sandbox, no hardcoded verdict).
- The #041 detuning law and #042 floor (log-uniform) remain valid and
  are now INTERPRETABLE as phasor-sum statistics in log scale — the
  floor question becomes "statistics of |sum of N unit phasors with
  log-uniform frequencies|", traced as open.
- Says nothing about nature, scales, or physical log-periodicity
  (e.g. discrete scale invariance literature) — shared FORM, never
  identity; no bridge claimed without a dedicated prior-art pass.

## Opens (traced, not started)
- Almost-periodic fine structure at N >= 3 (spacing fluctuations
  19.88..19.98 vs the beat 19.04): quasi-period vs frequency ratios.
- Floor as phasor statistics: derive the log-uniform saturation value
  and the linear-grid decay exponent from first principles (cheap,
  possibly analytic).
- Prior-art pass on log-periodicity/discrete scale invariance BEFORE
  any v3 wording (vocabulary risk: "log-periodic" is a loaded term in
  other fields; ours is a statement about OUR kernel only).
- Paper v3 boundary section: #039+#040 stand as written (v2c); the
  #041-#044 relief arc should enter, if ever, as ONE coherent block
  with the audit and this law — never the provisional pictures alone.

## Traces
- kernel_logperiod_test.py (harness, sandbox-tested and machine-run
  2026-07-09)
- FINDINGS_20260709_orthogonal_audit.md (#043, the audit this closes)
- FINDINGS_20260708_{tear_localization, position_steering}.md (#041,
  #042, the provisional pictures now explained)
- This file: FINDINGS_20260709_logperiodic_rendezvous.md
