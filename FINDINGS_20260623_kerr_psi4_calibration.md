# FINDINGS 2026-06-23 — Kerr/Psi4 calibration: known GW objects are walls

**Status:** [ESTABLISHED] 6/6 judge verdicts (this machine) · [DERIVATION] calibration baseline + target.

## What was tested

CALIBRATION FIRST for the Kerr/Psi4 gravitational-wave front (per the standing rule: calibrate on
known chiral cases before any discovery). Psi4 is spin-weight -2 (graviton helicity +-2), so the
complex strain h = h+ - i hx is natively complex (helicity-forced), not an h+,hx encoding. Complex
variable z = stereographic coordinate on the celestial sphere (real conformal geometry of S^2).
SPARC-pass on native complexity. Question: do known chiral GW objects fill the chiral cell?

## Exact command

cd ~/Desktop/oxieml-star && python3 kerr_psi4_calibration.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 6/6 agree, EXIT=0

ctrl_holo  z^2                      HOL            holomorphic reference (eml)
target_sig  log zbar               ANTI           the eml* signature we hunt (branch cut)
gw_linear_pol  z+zbar              REAL_TRAPPED   linear polarization, real strain (non-chiral)
gw_circular_phase  z/zbar          MODULE_TRAPPED circular polarization, helicity phase (eml0)
gw_spinweight2  zbar^2/(1+|z|^2)^2 MODULE_TRAPPED pure spin-weight -2 (orthogonal-axis spin wall)
gw_intensity  z*zbar               REAL_TRAPPED   measured intensity (real) -> mirror

## Conclusion — [DERIVATION]

Known chiral GW objects are WALLS, none is genuine eml*:
- linear polarization (real strain)          -> REAL_TRAPPED (non-chiral real field)
- circular polarization (helicity phase)     -> MODULE_TRAPPED (eml0; |h|=const)
- pure spin-weight -2                         -> MODULE_TRAPPED (orthogonal-axis spin wall)
- measured intensity |Psi|^2                  -> REAL_TRAPPED (mirror)
The tool DOES catch the target signature log(zbar) -> ANTI (eml*), so it is calibrated to detect
the eml* signature if present.

DISCOVERY TARGET (next, not done here): the branch cut of the QNM Green function in complex
frequency omega (Price tail from curvature backscattering). A branch cut = log-type structure in
the complex frequency variable, FORCED by curvature (non-removable), natively complex, and in
principle measurable (late-time tail). This is the only GW object that could escape the walls.

## Holo / anti ledger update

- eml (holo) confirmed: z^2 (reference).
- eml* (anti) reference: log zbar caught as ANTI (tool calibrated).
- Walls reconfirmed for GW: REAL_TRAPPED (linear pol, intensity), MODULE_TRAPPED (circular pol, spin-weight).
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.
- New entry: known GW polarization/spin-weight objects are walls; target = QNM Green branch cut.

## Files
- kerr_psi4_calibration.py (harness)
- this trace
