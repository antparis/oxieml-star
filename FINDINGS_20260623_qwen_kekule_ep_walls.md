# FINDINGS 2026-06-23 — Kekule/STM-Friedel and EP-microring candidates are WALLS

**Status:** [DERIVATION/LIMITE] both reduced candidates refuted at the judge; reality of the measured observable forces the mirror.

## Context

Two candidates reduced to closed form (external note, "Qwen") for the (b)+(c) hunt:
(1) chiral EP microring resolvent; (2) graphene Kekule intervalley coherence read by STM Friedel
oscillations. The note concluded Kekule is the target because d_z d_zbar log G != 0. Tested at judge.

## Judge verdicts (this analysis; pure SymPy)

EP microring  ln z (Jordan resolvent off-diagonal)   -> HOL          (holomorphic, z only = eml WALL)
Kekule/STM   cos(Q z + Qbar zbar)/(z zbar)            -> REAL_TRAPPED (arg = 2 Re(Qz) is REAL = mirror)
Kekule bare  ln(z zbar)  (Dirac K0 short distance)    -> REAL_TRAPPED (paired log)
contrast     cos(Q z + R zbar), R independent (!=conj Q) -> ANTI      (what the target would require)

## Conclusion — [DERIVATION/LIMITE]

Both candidates are WALLS.

1. EP microring: the resolvent/eigenvalue structure (ln z, sqrt(omega-omega_EP)) is HOLOMORPHIC
   (function of z/omega alone) -> eml WALL, as already found for GW branch cuts and TMG.

2. Kekule/STM Friedel: the note's claim "target because d_z d_zbar log != 0" is WRONG. d_z d_zbar
   log != 0 (non-factorizable) is NECESSARY but NOT SUFFICIENT. The judge gives REAL_TRAPPED: the
   Friedel modulation cos(Q.r) = cos(Q z + Qbar zbar) has a REAL argument (Qbar = conj(Q) =>
   Q z + Qbar zbar = 2 Re(Q z)), so it is a non-factorizable REAL = mirror, not eml*. The measured
   LDOS is real; reality forces R = conj(Q). Confusing "non-factorizable" with "target" is the error
   nonseparable_judge corrects: the target needs ANTI AND non-factorizable, not non-factorizable alone.

3. The discriminant cos(Q z + R zbar) with R INDEPENDENT (R != conj(Q)) reads ANTI -- this is what
   the target requires, and it is exactly what a REAL observable (LDOS, intensity) cannot provide,
   because reality ties R = conj(Q).

## Deep pattern (reinforced) — [DERIVATION]

Every observable MEASURED AS REAL (modular free energy, |G|^2 in GW, Friedel LDOS, intensity) forces
anti = conj(holo) -> mirror / REAL_TRAPPED, even when non-factorizable. The eml* target requires a
NATIVELY COMPLEX observable whose anti wavevector/coefficient is DECOUPLED from the holo (R != conj Q)
-- an amplitude/phase, never a real density. All search candidates (KFP, Kekule-Friedel, EP) hit this
reality wall.

## Holo / anti ledger update

- eml (holo): EP resolvent ln z, sqrt branch.
- Walls (real/mirror): Kekule cos(Qz+Qbar zbar), bare ln(z zbar); reciprocal EP (basis, prior trace).
- eml* (anti) FORM that would be needed: cos(Q z + R zbar) with R decoupled (R != conj Q) -- not
  realized by any real measured observable.
- ANTI forced + measurable + non-factorizable + decoupled-anti: still ZERO. Chiral cell EMPTY.

## Files
- qwen_candidates.py (harness; to be added to repo if kept)
- this trace
