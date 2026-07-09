# FINDINGS 2026-07-09 — Lyapunov-dominance (#046): the roughness floor is COLLECTIVE (the distribution's shape decides), the extreme-dominance form is refuted, the 1/sqrt(N) bridge is refuted, and the roughness/tide regime boundary is stated

## What
Mechanism test for the blur floor of #042/#043, born from Anthony reading
a popularization of Lyapunov's CLT (X post, 2026-07-09) and recognizing
the motif against our graved facts. Hypothesis (Anthony's bridge,
auditor-framed): the floor exists when some frequencies DOMINATE the
phasor sum; full blur requires non-dominance. CAUTION kept throughout:
our phasors are DETERMINISTIC rotations in ln x, not random variables —
Lyapunov is a LENS, not the theorem.

## v1 failure (diagnosed, documented — and promoted to a result)
v1 used a wide ln-x window (u <= 400) that crossed the deep log-periodic
rendezvous (#044): the contrast estimator measured TIDE DEPTH, not the
short-window ROUGHNESS whose floor #042/#043 established. Orthogonal
axis broken: "there is only ONE contrast" — false. v2 separates the two
regimes explicitly; the mis-windowing became the discovery of the
regime boundary (panel D).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-09)
```
cd ~/Desktop/oxieml-star && timeout 250 python3 kernel_dominance_test.py
```

## Raw result (machine output, identical to sandbox)
A. ABLATION on ROUGHNESS (u <= 5.3, log-uniform N=64, delta [0.3,30]):
   full choir 0.05080 (rejoins #043's value on the same window —
   inter-test continuity check passed); extremes removed (4): 0.03907
   (ratio 0.769); middles removed (4): 0.05367 (ratio 1.057).
   -> A real but modest extreme effect; the form "the extremes CARRY
   the floor" is REFUTED: ablation dents it, does not kill it.
B. q-TRANSITION on ROUGHNESS (N=64, spread warped by exponent q):
   contrast = 0.11498 / 0.09813 / 0.04437 / 0.00906 / 0.00040 for
   q = 3.0 / 2.0 / 1.0 / 0.5 / 0.2 — a CONTINUOUS, monotone transition
   over ~3 orders of magnitude.
   -> THE MECHANISM IS COLLECTIVE: the SHAPE of the whole frequency
   distribution sets the floor; as the distribution approaches
   uniformity (no contribution over-weighted — the exact spirit of
   Lyapunov's condition), blur becomes total. Anthony's bridge survives
   in its collective form, which is truer to the actual theorem (whose
   condition constrains the whole distribution, never two terms).
C. LINEAR-GRID EXPONENT on ROUGHNESS (to N=2048): contrast 0.011587 ->
   0.005793, fitted p = 0.188, tail flattening (~0.006 quasi-floor).
   -> The auditor's 1/sqrt(N) prediction is REFUTED a second time; the
   direct bridge to law #008 (random ~ sqrt(N)) does not hold in this
   deterministic system. The linear grid has its own, lower quasi-floor.
D. TIDE REGIME (long window u <= 400, same choirs): 0.87087
   (log-uniform) / 0.41086 (linear) — every choir saturates once its
   rendezvous enter the window.
   -> REGIME BOUNDARY STATED: roughness (short window, pre-rendezvous)
   and tides (long window) are distinct regimes; the #042/#043 floor
   statements live in the roughness regime ONLY.
E. RECIPROCAL CONTROL (nu_k = 0): max - min = 0.00e+00 on BOTH windows.

## Verdict
The blur floor of one-way tear roughness is a COLLECTIVE property of the
winding-speed distribution: its shape (not its extremes, not the number
of voices) sets the residual contrast, with a continuous transition to
total blur as the distribution approaches non-dominance. Two announced
predictions refuted and graved: the extreme-dominance form (Anthony's
bridge as first framed) and the auditor's 1/sqrt(N) law. The hypothesis
survives in the collective form — closer to Lyapunov's actual condition.
Born from a popularization post read on a phone during a family visit,
recognized by pattern against the graved corpus.

## Status
- Panels A-E: [ESTABLISHED machine] (run 2026-07-09, identical to
  sandbox, no hardcoded verdict; v1 window failure diagnosed and kept
  as the regime-boundary discovery).
- Lyapunov framing: [HEURISTIC LENS] — deterministic phasors, not
  random variables; no CLT theorem is claimed or used.
- Says nothing about nature. Shared FORM, never identity.

## Opens (traced, not started)
- Analytic floor: derive the roughness floor from the frequency
  distribution's shape (moments? spectral gap structure?) — the q-curve
  is smooth enough to suggest a formula. Best analytic candidate.
- The linear grid's own quasi-floor (~0.006): same collective law with
  a different shape parameter, or a distinct mechanism?
- Where exactly does the roughness/tide boundary sit as a function of
  the spread (first-rendezvous position vs window end)?
- Carried: wall-location theorem (#047 candidate); rendezvous fine
  structure (#049); prior-art pass log-periodicity/DSI before v3.

## Traces
- kernel_dominance_test.py (harness v2; the v1 mis-windowing and its
  promotion to the regime boundary are documented in the script)
- FINDINGS_20260709_genericity_audit.md (#045)
- FINDINGS_20260709_logperiodic_rendezvous.md (#044, the tides)
- FINDINGS_20260709_orthogonal_audit.md (#043, the floor facts)
- This file: FINDINGS_20260709_lyapunov_dominance.md
