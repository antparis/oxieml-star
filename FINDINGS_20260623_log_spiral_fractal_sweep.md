# FINDINGS 2026-06-23 — Log-spiral / fractal under the orthogonal axis + all Layer-1 tools

**Status:** [ESTABLISHED] 8/8 judge verdicts (this machine) · [DERIVATION] master pattern + fractal verdict.

## What was tested

A logarithmic spiral = a COMPLEX exponent: z^(alpha+i*beta) has log-spiral level curves. Fractals /
discrete scale invariance produce complex critical exponents = log-periodicity cos(omega*ln|z|) = the
same structure. Physical realization: conformal QM (-g/r^2, Efimov, Calogero), psi ~ r^(i*nu) (forced
log spiral in a complex amplitude). Each form run through judge_v2 + ALL Layer-1 tools at once
(verdict, spin s=h-hbar, poly_anti order, sigma reality) via axis_fingerprint.

## Exact command

cd ~/Desktop/oxieml-star && python3 log_spiral_fractal_sweep.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 8/8 agree, EXIT=0

logspiral_holo  z^(1+i)              HOL             spin 1+i    one-sided log spiral (eml)
logspiral_phase  |z|^i               MODULE_TRAPPED  spin 0      scale-free phase (|z|^is blind-spot, patched)
logspiral_anti  zbar^(1+i)           ANTI            spin -1-i   PURE-anti = half-chiral WALL (mirror of holo)
logspiral_balanced z^s zbar^sbar     REAL_TRAPPED    spin 2i     balanced log spiral -> real
complex_unbalanced z^(1+i)zbar^(2-i) MODULE_TRAPPED  spin -1+2i  complex powers pair -> module
fractal_logperiodic cos(3 ln|z|)     REAL_TRAPPED    spin 0      DSI / fractal log-periodicity (real)
efimov_radial  |z|^(i/3)             MODULE_TRAPPED  spin 0      conformal QM psi~r^(i nu) (Efimov) -> module
escape_unpaired z^-1 zbar^-1(1+log zbar) ANTI        spin n/a    the ONLY genuine independent escape

Nuance: logspiral_anti (pure zbar^s) reads ANTI but is the HALF-CHIRAL WALL (mirror of the holo
z^s), NOT independent anti. The only genuine INDEPENDENT anti is the MIXED unpaired log
(escape_unpaired).

## Conclusion — [DERIVATION]

1. Every log-spiral / fractal / complex-exponent form is HOL or WALL_PAIRED. The spin column shows
   even COMPLEX/irrational spin (1+i, 2i, -1+2i) -> still a wall; scale-freeness (fractal) does NOT
   move the verdict off the wall.
2. The only genuine INDEPENDENT anti is the unpaired transcendental log. No power, no phase, no
   complex exponent, no fractal reaches it.
3. MASTER LAW: zbar is genuine (independent) ONLY when UNPAIRED + transcendental. Rotation / spin /
   scale (phi, pi, helix, log spiral, fractal) all PAIR zbar with z -> mirror/modulus -> wall.

=> A FRACTAL CANNOT fill the chiral cell: it supplies a sophisticated wall (log-spiral phase / DSI),
   not independent anti. Conformal QM (Efimov) log spiral is module-trapped; its observable is real.
   The cell still needs an unpaired forced log in a natively-complex measurable.

## Holo / anti ledger update

- eml (holo): z^(1+i) (one-sided log spiral).
- eml* (anti) genuine INDEPENDENT: only escape_unpaired (unpaired log). Pure-anti zbar^s = half-chiral wall.
- Walls: REAL_TRAPPED (balanced spiral, fractal log-periodic), MODULE_TRAPPED (|z|^is phase, complex
  powers, Efimov radial).
- ANTI forced + measurable + gauge-invariant + independent: still ZERO. Chiral cell EMPTY.
- New mapping: scale/rotation (incl. fractal complex exponents) always pair zbar -> wall.

## Files
- log_spiral_fractal_sweep.py (harness)
- this trace
