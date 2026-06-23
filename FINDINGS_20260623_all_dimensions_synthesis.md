# FINDINGS 2026-06-23 — Explore all dimensions: master synthesis

**Status:** [DERIVATION] convergence law (Layer 1 certified by judge_v2; Layer 2 exact SymPy).

## What was run

explore_all_dimensions.py orchestrates EVERY axis built this session on one corpus, in two layers.
- LAYER 1 (functions f(z,zbar), 1 variable) via axis_fingerprint: verdict (judge_v2),
  poly-analytic order (axis A), spin s=h-hbar (orthogonal axis), sigma reality (axis B),
  gauge-removability (Ginibre finding).
- LAYER 2 (forms, several variables / topology) via dolbeault_v1: H^{0,1} (eml*) and H^{1,0} (eml).

## Exact command

cd ~/Desktop/oxieml-star && python3 explore_all_dimensions.py; echo "EXIT=$?"

## Raw result (this machine), EXIT=0

LAYER 1 -- physical functions with GENUINELY non-removable ANTI (gauge-invariant): NONE
  (ginibre_q2_ker reads ANTI but is gauge-removable -> excluded)
LAYER 2 -- NON-REMOVABLE (COHOMOLOGY): anti direction AND holo direction.

## Master synthesis — [DERIVATION]

non-removable anti  <=>  non-trivial Dolbeault class (Layer 2).

- All Layer-1 axes (verdict, poly-analytic order A, conformal spin / orthogonal axis,
  sigma reality B, gauge) REFINE the classification but never yield a physical non-removable anti.
- Every wall of the session (real-trapped, module-trapped, gauge wall) is a Layer-1 REMOVABILITY wall.
- The chiral cell cannot exist in Layer 1 (functions on a contractible domain). It can ONLY live in
  Layer 2 (Dolbeault cohomology), the sole place where anti is immune to BOTH coboundary and gauge.
- The remaining frontier collapses to ONE: criterion (c) — a MEASURABLE observable carrying a
  non-trivial class. Target = v1b+v1d (torus / period ratio tau).

Exploring all dimensions did not scatter the hunt; it concentrated it on a single front.

## Holo / anti ledger update

- Confirmed (both columns): eml (holo) and eml* (anti) detected symmetrically; controls pass.
- Non-removable structure exists ONLY as a Dolbeault class (Layer 2), in both directions.
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.

## Files
- explore_all_dimensions.py (orchestrator)
- this trace
