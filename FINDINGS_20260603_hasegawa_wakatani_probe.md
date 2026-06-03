# FINDINGS 2026-06-03 -- Hasegawa-Wakatani frozen-state probe [HEURISTIC/incomplete]

## Status
[HEURISTIC] preliminary SymPy probe, NOT established. Construction not clean
(unsimplified conjugate(z) in output, Test1/Test2b inconsistency). To redo cold
with the exact HW dispersion relation, not the cos(kx-delta) approximation used here.

## What IS established
- Naive frozen HW (S = phi + i*n, isotropic real modes phi=cos(kx), n=cos(kx-delta)):
  comes out MIRROR / REAL-TRAPPED. Same wall as Hall equilibrium. A uniform phase
  lag between two REAL fields does not create scalar chirality.

## The encouraging HINT (not a result)
With an ORIENTED background gradient (kappa along x, the "stream direction") AND
resistivity nu, the linear density response R(k) = omega_*/(omega - omega_* + i nu)
with omega_* = ky*kappa depends on sign(ky) (perpendicular to gradient). Test:
  R(-ky) - conj(R(ky)) != 0  => the density response is NOT mirror-symmetric.
This is a candidate mechanism: oriented gradient + resistivity could break the
mirror. DIFFERENT from Hall (which had no such oriented-gradient + dissipative lag).

## Why it is NOT yet a result (honest)
- Test "does mirror-breaking vanish as nu->0" came back INCONSISTENT (residual did
  not cleanly vanish), and SymPy left unsimplified conjugate(z) terms => the scalar
  object as constructed is not clean. Cannot distinguish (a) genuine
  resistivity-forced chirality from (b) an encoding artefact like Hall.

## Next (cold, not improvised)
- Use the EXACT HW linear response n_k/phi_k = (1 - i*delta_k) form from the real
  dispersion relation (parallel resistive coupling), not a hand-shifted cosine.
- Define the scalar observable precisely (density n alone? potential phi? a HW
  invariant?) and test b vs conj(a) cleanly with the project judge.
- Encadrement to verify: chirality must vanish as nu->0 (adiabatic/Boltzmann limit
  n=phi, in phase, mirror) AND as kappa->0 (no gradient, no stream direction).
- WARNING: keep everything spatial (frozen snapshot). Do NOT encode time as the
  imaginary axis (SPARC trap).
