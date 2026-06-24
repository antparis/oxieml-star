# FINDINGS 2026-06-24 — DRUM non-reciprocal EP, TCMT level = SPARC wall

**Status:** [DERIVATION] (exact algebra + SPARC argument; not a judge certification
of a physical closed-form anti). Executed on the M920q.

## What was tested

Whether the DRUM non-reciprocal exceptional point, taken at the level of its
actual physical model — Temporal Coupled Mode Theory (TCMT), two discrete
counter-propagating modes CW/CCW — can produce a genuine anti-holomorphic
structure `log(z1 - conj(z2))` (the refined ENTANGLED_CHIRAL_ANTI target).

Device physics (sourced, Light: Sci. Appl. 2026, DRUM): microresonator with two
tunable side waveguides (MZI + phase shifter), independent amplitude/phase of the
coupling coefficients between counter-propagating modes; chiral EP realised at
beta_21 = 0, beta_12 != 0 (only CW<-CCW coupling). Model = TCMT.

## Command

    cd ~/Desktop/oxieml-star && python3 drum_tcmt_wall.py

Witness: `drum_tcmt_wall.py` (144 lines). Transparent Wirtinger test
`d/d(zbar) = 1/2 (d/dx + i d/dy)`, z = x + i y.

## Raw result

- `H_ep = [[lambda, kappa1],[0, lambda]]` is NON-diagonalizable -> Jordan block,
  non-reducible by construction (Naimark lock).
- Exact cross propagator in TIME: `<CW| e^{-iHt} |CCW> = -i*kappa1*t*e^{-i*lambda*t}`
  (linear-in-t Jordan factor). In FREQUENCY: `kappa1/(omega - lambda)^2` (double pole).
  Physical variables = {t, omega}, both REAL.
- `d/d(zbar) log(z) = 0` -> HOL. `d/d(zbar) 1/(z-lambda)^2 = 0` -> HOL.
  A single-sector log/pole carries no independent anti (half-chiral wall).
- Grafted `log(z1 - conj z2)`: `d/d(zbar2) = -1/(z1 - conj z2) != 0` (genuine-anti
  SHAPE) — BUT z1, z2 are 2D spatial coordinates ABSENT from the TCMT model.

## Verdict

The TCMT description has no complex spatial variable. The cross propagator lives
in real t / real omega; the transcendental it yields is single-sector (HOL) or
over a real variable (real-trapped) — a WALL either way. The target
`log(z1 - conj z2)` is reachable ONLY by grafting a 2D-CFT cross propagator
`1/(z1 - conj z2)` onto a device that does not realise such a spatial structure.
That graft is the SPARC encoding trap (cf. SPARC galaxies; spacetime_trap.py):
the anti is created by the analyst's coordinate choice, not forced by physics.

=> DRUM at the MODAL (TCMT) level is a SPARC wall. The chiral target is
   unreachable at the modal level. Escaping the trap requires DROPPING TCMT and
   working at the FIELD level (1+1D in the ring), where the spatial coordinate is
   physical — a separate test (step 2), with its OWN SPARC question (are the
   light-cone coordinates s ∓ v t natively complex, or real coordinates
   re-encoded?).

## Consequence for the target / kickoff

Confirms and sharpens the d80395f correction: not only do asymmetric weights fail,
the mixed-argument `log(z1 - conj z2)` is itself a SPARC artefact when sourced from
a 2x2 modal Hamiltonian. A Jordan block alone CANNOT supply the target; a genuine
spatial field is required. The kickoff section 1 target line must be regenerated
to record this (modal level closed, field level open).

## Symmetry ledger update

WALL added: DRUM non-reciprocal EP, TCMT/modal level — SPARC graft, HOL/real-trapped
[DERIVATION]. Chiral cell: still empty. Only live door unchanged: distinct-spin
cross-correlator in a non-unitary regime, now to be sought at the FIELD level.

## Trace files

- drum_tcmt_wall.py (witness, reproducible)
- FINDINGS_20260624_drum_tcmt_sparc_wall.md (this file)
