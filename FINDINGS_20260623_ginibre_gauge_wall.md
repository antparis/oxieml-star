# FINDINGS 2026-06-23 — Ginibre / polyanalytic ensemble: axis A is a GAUGE WALL

**Status:** [ESTABLISHED] for the 9 judge verdicts · [DERIVATION/LIMIT] for the gauge-wall conclusion.

## What was tested

CERTIFIER-mode test of axis A (poly-analytic order) on the Ginibre / polyanalytic
random-matrix ensemble — a NATIVELY COMPLEX physical object (non-Hermitian RMT eigenvalues;
passes SPARC criterion (a)). Question: does the q-polyanalytic (higher-Landau-level) Ginibre
kernel fill the EMPTY cell "genuine ANTI at finite poly-analytic order" in a way that
survives SPARC and is carried by a MEASURABLE observable?

Bulk kernel, w0 = 1 fixed second point:
K_q(z,w0) = e^{-|z-w0|^2/2} * e^{(z w0bar - zbar w0)/2} * L_{q-1}(|z-w0|^2),
with L_0 = 1 (ordinary Ginibre) and L_1(x) = 1 - x (q=2).
Split: radial = measurable envelope; cocycle = GAUGE factor (magnetic translation);
Laguerre = polyanalytic prefactor.

## Exact command

cd ~/Desktop/oxieml-star && python3 ginibre_sweep.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 9/9 agree, EXIT=0

ctrl_anti              ANTI            control
ctrl_real              REAL_TRAPPED    control
cocycle_1pt            ANTI            gauge factor alone (non-observable)
radial_envelope        REAL_TRAPPED    measurable modulus
ginibre_q1_kernel      MODULE_TRAPPED  ordinary Ginibre kernel, 1-pt
ginibre_q1_gaugestrip  REAL_TRAPPED    q1 kernel minus gauge -> real
ginibre_q2_kernel      ANTI            q=2 polyanalytic kernel, 1-pt (finite-order ANTI)
ginibre_q2_gaugestrip  REAL_TRAPPED    DECISIVE SPARC: q2 minus gauge -> REAL
ginibre_corr_modsq_q2  REAL_TRAPPED    measurable correlation |K|^2 (observable)

All 9 judge verdicts equal the independent oracle. [ESTABLISHED]

## Conclusion — [DERIVATION/LIMIT]

1. The q=2 polyanalytic kernel reads ANTI at FINITE poly-analytic order — it is the FIRST
   physically-motivated object in the whole hunt to land in a genuine-ANTI cell at finite order.
2. But the anti is a GAUGE ARTEFACT. Stripping the gauge cocycle (a gauge choice;
   magnetic-translation phase) collapses ANTI -> REAL_TRAPPED (ginibre_q2_gaugestrip).
   The anti can be removed by a treatment choice -> FAILS SPARC.
3. The measurable observable (density is constant; correlation |K|^2 is real) reads
   REAL_TRAPPED -> criterion (c) fails independently.

=> Ginibre does NOT fill the chiral cell. It defines a new sub-type of the observable
wall: a GAUGE WALL — the anti lives in a gauge cocycle, removable, and absent from the
measurable observable. Same wall reached from non-Hermitian RMT, an angle independent of
LCFT / TMG / Zwegers.

## Navigation-law refinement

The SPARC test now has an explicit GAUGE sub-clause: when the anti sits in a U(1) cocycle
(magnetic translation / Berry connection), it is gauge-removable and counts as artefact, even
when the judge reads ANTI on a fixed-gauge representative. Check gauge-invariance before
claiming a finite-order anti is physical.

## Holo / anti ledger update

- ANTI confirmed (form-level, fixed gauge, NOT physical/measurable): cocycle_1pt, ginibre_q2_kernel.
- Walls reconfirmed: MODULE_TRAPPED = ginibre_q1_kernel; REAL_TRAPPED = radial_envelope,
  both gauge-stripped kernels, the measurable correlation.
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.

## Files

- ginibre_sweep.py (harness)
- this trace
