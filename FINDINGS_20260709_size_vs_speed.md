# FINDINGS 2026-07-09 — Size vs speed (#047): size disparity alone writes NOTHING (machine zero); speed disparity is the only pen; correlated size-speed is ASYMMETRIC — big-slow calms the sea (ballast), big-fast roughens it

## What
Anthony's foam image isolated at last: every choir since #041 had
disparate SPEEDS but (near-)equal SIZES — the orthogonal parameter never
broken. Question: does size disparity do the same work as speed
disparity? Four configurations on the roughness window (u <= 5.3, the
#046 object): sizes alone, speeds alone (reference), both uncorrelated,
both correlated (the physical foam: big bubbles slow — and the reverse).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-09)
```
cd ~/Desktop/oxieml-star && timeout 250 python3 kernel_size_speed_test.py
```

## Raw result (machine output, identical to sandbox)
A. SIZES ALONE (random weights [0.2,1.8], ALL speeds equal): contrast =
   9.61e-16 — MACHINE ZERO, confirming the announced algebraic
   prediction: one common frequency makes the sum a single fixed-length
   needle; |sum| is constant. SIZE DISPARITY ALONE WRITES NOTHING.
B. SPEEDS ALONE (equal weights, log-uniform grid): 0.05080 — exact
   continuity with #046's reference (inter-test check passed).
C. BOTH, UNCORRELATED (3 random weight draws on the same speed grid):
   0.05320 / 0.04409 / 0.04260 — modest modulation around the
   reference (second-order effect, as predicted).
D. BOTH, CORRELATED — the discovery, and an auditor refutation:
   w ~ 1/nu (big bubbles SLOW, the physical foam): contrast = 0.00568,
   ratio 0.11 — the floor COLLAPSES by ~9x.
   w ~ nu (big bubbles FAST): contrast = 0.07031, ratio 1.38 — RAISED.
   [Auditor prediction "BOTH correlation signs raise the floor" —
   REFUTED: the response is ASYMMETRIC.]
   Mechanism read from the mathematics: on the short window the slow
   needles barely rotate (nu_min * u_max ~ 0.02 rad — quasi-static);
   weighting them creates a STATIC BALLAST that drowns the relative
   relief; weighting the fast rotators amplifies the ripples.
E. RECIPROCAL CONTROL (nu_k = 0, disparate weights): 0.00e+00 exactly.

## Verdict — Anthony's foam image, fully dissected (three laws)
1. SIZE ALONE IS MUTE: without behavioral difference, size difference
   writes nothing — machine zero, algebraically forced.
2. SPEED IS THE ONLY PEN: all relief along the one-way cut originates
   in winding-speed disparity (consistent with #041 and #046).
3. THE MARRIAGE IS ASYMMETRIC: when sizes correlate with speeds, the
   DIRECTION decides — big-slow (the physical-foam direction) CALMS
   the roughness (ballast effect, floor / 9); big-fast ROUGHENS it
   (floor x 1.38).
REFINEMENT OF #046 TRACED: the collective law's operative object is the
WEIGHTED, WINDOW-ACTIVE frequency distribution — quasi-static
frequencies (nu * u_window << 1) act as spectators/ballast, not as
voices. "Concentration raises the floor" holds only among ACTIVE
frequencies.

## Status
- Panels A-E: [ESTABLISHED machine] (run 2026-07-09, identical to
  sandbox, no hardcoded verdict; panel A doubles as an algebraic
  identity faced by the machine).
- The ballast mechanism reading: [DERIVATION] (read directly from the
  phasor form; not yet varied systematically).
- Third auditor refutation of the day graved (symmetric-correlation
  prediction false).
- Says nothing about nature or real foams. Shared FORM, never identity.

## Opens (traced, not started)
- Ballast law: floor vs the weighted fraction of window-active
  frequencies — could unify #046's q-curve and #047's asymmetry into
  ONE formula (the analytic-floor candidate, now better framed).
- Window-scaling: does the big-slow collapse invert on longer windows
  (slow needles become active)? Regime-boundary interplay with #046-D.
- Carried: wall-location theorem, rendezvous fine structure, prior-art
  pass log-periodicity/DSI before v3.

## Traces
- kernel_size_speed_test.py (harness, sandbox-tested and machine-run
  2026-07-09)
- FINDINGS_20260709_lyapunov_dominance.md (#046, the collective law
  this refines)
- This file: FINDINGS_20260709_size_vs_speed.md
