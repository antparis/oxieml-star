# FINDINGS 2026-07-10 — Ballast law (#048): the first-order incoherent formula is REFUTED, and its diagnosis yields the registry's first CLOSED-FORM LAW — the roughness floor is the window-contrast of the FOURIER TRANSFORM of the weighted winding measure

## What
The analytic-floor candidate opened by #046/#047: ONE formula unifying
the q-family, the foam asymmetry, and the grid behaviours. Three stages
inside one harness, each faced by machine: (i) a first-order incoherent
"ballast law" (announced, tested, REFUTED with structured deviations);
(ii) its diagnosed failure promoted to the true candidate: the
FOURIER-LIMIT LAW; (iii) the reciprocal differential recovered as a
THEOREM of the law rather than a control.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-10)
```
cd ~/Desktop/oxieml-star && timeout 300 python3 kernel_ballast_law_test.py
```

## Raw result (machine output, identical to sandbox)
D. TWO-NEEDLE ANALYTIC ANCHOR: one ballast + one active needle —
   contrast = w_a/w_s exactly (|diff| = 7.1e-10 / 2.1e-10 / 4.2e-11 at
   three settings). Hand-derivable; the law's exact corner.
B. FIRST-ORDER INCOHERENT LAW (contrast ~ c0 * sqrt(sum (w a)^2)/sum w):
   REFUTED — worst deviation factor 10.26 with STRUCTURED pattern:
   near-uniform spectra fall far BELOW (q=0.2 ratio 0.10: dense uniform
   spectra cancel better than incoherent), log-uniform spectra rise
   ABOVE with N (geom ratios 1.31 -> 2.54 -> 5.04 at N=64/256/1024: the
   floor is a COHERENT phenomenon; the sqrt was the wrong hypothesis).
C. METHOD ORTHOGONAL: the binary active/ballast criterion is DEGENERATE
   at theta = pi (X = 0 on 15/15 configs) — structural insight kept:
   on the roughness window NO needle completes a turn (max phi ~ 1.75
   rad); ROUGHNESS IS THE PARTIAL-ROTATION REGIME; full turns exist
   only in the tide regime (#044 tie-in). Continuous activity a(phi) =
   sqrt(1 - (2 sin(phi/2)/phi)^2) usable on 15/15 but spread 2.33 —
   first-order in any dress fails; the failure is coherence, not the
   criterion.
E. RECIPROCAL AS THEOREM: nu_k = 0 => X = 0 => predicted contrast 0;
   machine 0.00e+00. The one-way differential now FOLLOWS from the law
   (measure concentrated at nu = 0 => constant Fourier transform =>
   zero relief) instead of being only an empirical control.
F. FOURIER-LIMIT LAW — the result: as N -> inf at fixed shape,
   P(u)/N -> |mu_hat(u)| = |integral e^{i nu u} dmu(nu)|, the Fourier
   transform of the weighted winding measure; THE FLOOR IS THE
   WINDOW-CONTRAST OF |mu_hat|. Machine face (C at N=64 vs N=16384
   limit proxy): saturating shapes sit ON their limit — q=3.0: 1.00;
   foam big-slow: 1.01; geom: 1.07; foam big-fast: 1.08; q=1.0: 0.93 —
   the graved #046/#047 values ARE the Fourier contrast of their
   shapes. Shapes far from their limit converge toward it (linear:
   2.04; q=0.2: 0.57): the decay #046-C measured was CONVERGENCE toward
   this law — the exponent p = 0.188 (and the auditor's 1/sqrt(N),
   twice refuted) never had universal meaning: there is no exponent,
   there is a destination.

## Verdict — the registry's first closed-form law
THE ROUGHNESS FLOOR IS THE WINDOW-CONTRAST OF THE FOURIER TRANSFORM OF
THE WEIGHTED WINDING MEASURE. Retroactively, three graved entries become
corollaries: #046-B ("the shape decides") — literally, the floor is a
functional of the shape; #046-C (the linear-grid "decay") — a journey,
not a law; #047-D (the foam asymmetry) — reweighting the measure
reshapes its transform, by the computed amount. And the Lyapunov lens
closes its loop with a caution kept: the Fourier transform of a
probability measure is the CHARACTERISTIC FUNCTION — the very tool of
CLT proofs, Lyapunov's included; our needles remain deterministic, the
lens remains a lens, but the kinship is now tool-level, not
surface-level.

## Status
- Panels D, E, F: [ESTABLISHED machine] (run 2026-07-10, identical to
  sandbox, no hardcoded verdict).
- Fourier-limit convergence P/N -> mu_hat: [DERIVATION] (Riemann-sum
  convergence of the deterministic sum; N=16384 used as limit proxy,
  not a symbolic proof — the hand-proof is the natural next step and
  the registry's first theorem candidate).
- First-order incoherent law and binary criterion: REFUTED, kept with
  their structured failure patterns (two auditor refutations graved).
- Says nothing about nature. Shared FORM, never identity.

## Opens (traced, not started)
- HAND PROOF of the Fourier-limit law (Riemann convergence + contrast
  continuity): the registry's first theorem candidate, cheap.
- Closed-form floors: compute mu_hat analytically for the canonical
  shapes (log-uniform => incomplete-exponential-integral forms) and
  predict floors to all digits.
- Inverse problem (#053 germ): read the shape from the measured relief
  — mu_hat inversion on a finite window (ill-posedness to frame).
- Convergence-rate law: WHAT sets the approach speed to the limit
  (linear grid still 2x off at N=64)? Replaces the dead exponent p.
- Carried: prior-art pass log-periodicity/DSI partially done
  (conversation report 2026-07-09: Sornette/DSI = partial precedent on
  FORM, mechanism route apparently new; NH-topology witnesses adjacent
  but distinct object; dual-comb = thin bridge) — to be traced in a
  dedicated FINDINGS before any v3 wording.

## Traces
- kernel_ballast_law_test.py (harness; the refuted first-order law, the
  degenerate binary criterion, and their diagnoses are documented in
  the script itself)
- FINDINGS_20260709_{lyapunov_dominance, size_vs_speed}.md (#046, #047
  — now corollaries of the law)
- This file: FINDINGS_20260710_fourier_floor_law.md
