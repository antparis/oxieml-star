# FINDINGS 2026-07-08 — Localization along the tear emerges from DETUNING, not from number: the choir's second emergence law (complement of #039)

## What
Anthony's motion-capture idea, framed as #041: N chiral tears with detuned
offsets on the one-way kernel cut — can opposed tears CANCEL (conflict)?
does an interference pattern along the cut create emergent "here vs there"
structure that no single tear carries? what builds the pattern: the NUMBER
of tears or their DETUNING? Four scenarios, three independent estimators
(orthogonal-axis correction after a v1 sandbox failure: a thresholdless
extrema counter mistook 1e-17 rounding noise for structure — diagnosed,
method fixed: noise-thresholded extrema + contrast + edge exclusion).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-08)
```
cd ~/Desktop/oxieml-star && timeout 200 python3 kernel_localization_test.py
```

## Raw result (machine output, identical to sandbox)
S1 CONFLICT: exact global cancellation at machine zero (max|P| = 0.00e+00)
  for IDENTICAL offsets + opposite weights — a measure-zero, fine-tuned
  condition (Silva-like). Any detuning (eps = 0.01..2.0) breaks it into a
  residual dip that sits AT THE WALL side of the window (x = 1.17,
  dip-at-edge: True at every eps) — the conflict residue hugs the
  boundary, it is NOT an interior "place".
S2 PAIR LOCALIZATION (delta = 1 vs 3): contrast = 0.0078 (floor 1e-12),
  0 thresholded interior extrema; steering scan (delta2 = 2..12): contrast
  grows 0.0044 -> 0.0149 but the dip POSITION does not move (x = 179.26,
  window edge, at all four settings). At pair level the network commands
  the DEPTH of the relief, not yet its LOCATION — two capture points do
  not draw a silhouette.
S3 N vs SPREAD, disentangled (the central result):
  (i) fixed spread (delta in [0.3,30]), N grows: contrast DECREASES
      0.2183 (N=2) -> 0.0486 (N=200), saturating; 0 extrema throughout.
      MORE TEARS BLUR (phase averaging).
  (ii) fixed N=20, spread grows (delta in [1/S,S]): contrast GROWS
      0.0143 (S=2) -> 0.4703 (S=200), and interior extrema APPEAR:
      0 -> 0 -> 4 (S=30) -> 30 (S=200). WIDER DETUNING BUILDS structure —
      real oscillations along the cut, thresholded, edge-excluded.
S4 RECIPROCAL CONTROL: all offsets real, varied weights: contrast
  5.55e-17 / 4.44e-16 / 2.98e-15 at N = 2/20/200, extrema = 0 everywhere —
  flat at machine zero. Phase winding is the ONLY source of structure.

## Verdict — the second emergence law of the boundary
Along the one-way kernel's tear, "here vs there" structure (interference
relief) EXISTS and is a ONE-WAY phenomenon (reciprocal control machine-
flat). Its source is the DIVERSITY of phase-winding speeds (detuning),
not the number of voices: number averages and blurs, detuning builds and
localizes. Anthony's live formulation, machine-confirmed: "c'est suivant
les situations que nous obtenons certains resultats" — same choir, two
regimes. Complement of #039: THE BOUNDARY emerges from NUMBER (infinite
choir); THE RELIEF along it emerges from DETUNING. Two distinct emergence
laws on the same object. Exact cancellation between tears is fine-tuned
(measure-zero), consistent with the navigation law (tuned agreement =
Silva-like, not structure).

## Status
- Scenarios S1-S4: [ESTABLISHED machine] (run 2026-07-08, identical to
  sandbox v2, no hardcoded verdict; v1 estimator failure diagnosed and
  documented — thresholdless counter, noise floor, edge artefacts).
- Route: disc linearity + theory formula controlled machine-exact on the
  a=1 dilog (#039/#040); a-complex jumps inherit [DERIVATION] via the
  Lerch->dilog reduction, as before.
- Nuances kept honest: (i) the conflict dip hugs the wall (edge), not an
  interior place; (ii) at pair level the dip position is not steered —
  full motion-capture (position control) is NOT established, only depth
  control; (iii) the extrema-rich regime needs LARGE spread (S >= 30).
- Says nothing about nature, space, or physical localization. Shared
  FORM (emergent "position" structure along a boundary), never identity.

## Opens (traced, not started)
- Position steering: can a richer choir (N >= 3, engineered offsets,
  varied weights/phases) MOVE the relief's features along the cut —
  full motion capture? (The pair only controls depth.)
- The blur law: is the N-decay of contrast at fixed spread a 1/sqrt(N)
  law (incoherent phase averaging) or something else? One cheap scan.
- v3 boundary section candidates now form a quartet: #039 (wall from
  number) + #040 (chiral crossing) + #041 (relief from detuning) + the
  blur/steering opens.

## Traces
- kernel_localization_test.py (harness v2, sandbox-tested 2026-07-08,
  machine-run 2026-07-08; v1 estimator failure documented above)
- FINDINGS_20260708_chiral_tear.md (#040, the chirality this builds on)
- FINDINGS_20260705_kernel_boundary.md (#039, the wall-from-number law)
- This file: FINDINGS_20260708_tear_localization.md
