# FINDINGS 2026-06-22j -- eml-zero formalized as a THIRD pipeline detector (pure-phase); three-operator grid

## Status
[ESTABLISHED] (machine, code 0, calibration irreproachable). eml-zero (pure-phase detector)
is formalized and calibrated alongside the eml/eml-star judge. The three operators
eml / eml-star / eml-zero now give THREE INDEPENDENT classification axes, where eml-star
alone gave one. eml-zero gives a POSITIVE characterization of the pure-phase sub-class of
the module-trapped walls.

## The three operators (Anthony Monnerot's eml family), tested TOGETHER (standing rule)
  eml   (holomorphic) : df/dzbar == 0  -> depends on z alone
  eml*  (anti-holo)   : judge_v2 4-label (holo / real-trapped / module-trapped / anti)
  eml0  (pure phase)  : |f|^2 = f*conj(f) is CONSTANT while f varies -> pure winding phase

## eml0 definition (rigorous)
eml0(f) = "pure-phase" iff f is non-constant AND f*full_conj(f) has zero derivative in both
z and zbar (modulus is constant). Else "not-pure-phase" (or "constant"). Distinct from eml*
which tests df/dzbar; eml0 tests the MODULUS. Complementary axis.

## Calibration (PART A, all OK)
pure-phase detected: z/|z|, (z/zbar)^(1/2) winding, |z|^(is), (z/|z|)^3.
not-pure-phase (correctly rejected): z, zbar, z+zbar, log(zbar), z*zbar=|z|^2.
=> eml0 irreproachable.

## Three-operator grid (PART B, machine)
  object                         eml      eml*              eml0
  mock theta f(q) bare [MEAS.]   holo     holomorphic       not-pure-phase
  conj(g3) anti-chiral           -        anti-holomorphic  not-pure-phase
  Zwegers y^(-1/2)conj(g3)       -        anti-holomorphic  not-pure-phase
  symplectic log(zbar)           -        anti-holomorphic  not-pure-phase
  wall |z|^(is)                  -        module-trapped    PURE-PHASE
  wall winding (z/zbar)^(1/2)    -        module-trapped    PURE-PHASE
  complete scalar log|z|^2       -        real-trapped      not-pure-phase
  Kirsch-type 1/zbar             -        anti-holomorphic  not-pure-phase

## Significance
eml0 isolates the PURE-PHASE walls (|z|^is, winding) -- objects that rotate without changing
amplitude -- as a POSITIVE category, not just "module-trapped, discard". It distinguishes:
  - pure-phase walls (|z|^is, winding): eml* module + eml0 pure-phase
  - genuine algebraic anti (1/zbar Kirsch): eml* anti + eml0 not-pure-phase
  - genuine transcendental anti (log zbar, conj g3, Zwegers): eml* anti + eml0 not-pure-phase
  - real scalar wall (log|z|^2): eml* real + eml0 not-pure-phase
Before, eml* alone gave "wall or not". Now eml+eml*+eml0 give a full map: holomorphic axis,
anti-irreducibility axis, pure-phase axis. This was Anthony's standing point (always use the
three operators); it converts the under-used eml0 into a working 3rd detector that
CHARACTERIZES the walls instead of merely rejecting them.

## Use going forward
The three-operator grid is the new default lens. Apply to: other mock theta functions (lost
notebook, orders 5/7/10), other physical/formal objects. eml0 turns "module-trapped" from a
dead-end label into a structured one (pure-phase vs general module).

## Files
eml_zero_and_grid.py, this FINDINGS. Builds on 0622i (Zwegers), 0622h (symplectic), the
fixed judge_v2. eml0 not yet a separate .py module in the pipeline -- candidate for promotion
to a standalone detector alongside verify_exact.py / judge_v2.py if used routinely.
