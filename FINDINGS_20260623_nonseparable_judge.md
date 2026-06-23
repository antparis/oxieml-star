# FINDINGS 2026-06-23 — Non-separable two-mode judge: entanglement != chirality

**Status:** [ESTABLISHED] classifier self-consistent (this machine) · [DERIVATION] entanglement!=chirality law · [CONJECTURE] physical realization.

## What was built and tested

nonseparable_judge.py -- multi-variable (two-mode z1,z2) extension of judge_v2 (one-field). For an
amplitude f(z1,z2,zbar1,zbar2) it reports simultaneously: base verdict (HOL/REAL/ANTI/MODULE),
inter-mode separability (d2 log f / d(mode1)d(mode2)=0 => f=g(mode1)h(mode2)), and chiral
factorization (d2 log f / dz_i dzbar_j=0 => f=holo(z)*anti(zbar)). Tests whether a NON-SEPARABLE
(entangled) state carries genuine chiral anti, or is merely holomorphic entanglement (eml wall).

## Exact command

cd ~/Desktop/oxieml-star && python3 nonseparable_judge.py; echo "EXIT=$?"

## Raw result (this machine), EXIT=0

ctrl_holo  z1^2                            HOL     sep=T  cf=T   HOL separable
ctrl_anti  log zbar1                       ANTI    sep=T  cf=T   SEPARABLE half-chiral WALL
sep_holo  z1*z2                            HOL     sep=T  cf=T   HOL separable
ENT_holo  z1z2+(z1z2)^2                    HOL     sep=F  cf=T   ENTANGLED HOLO (eml WALL)
sep_chiral  z1*zbar2                       MODULE  sep=T  cf=T   WALL (mirror/modulus)
real_paired  |z1|^2+|z2|^2                 REAL    sep=F  cf=F   WALL (mirror/modulus)
EPR_chiral  z1 zbar2 + z2 zbar1            REAL    sep=F  cf=F   WALL (mirror/modulus)
chiral_fact_uneq  exp(i pi z1+i phi zbar2) ANTI    sep=T  cf=T   SEPARABLE half-chiral WALL
TARGET  1+pi log z1+phi log zbar2          ANTI    sep=F  cf=F   ENTANGLED CHIRAL ANTI (target type)
TARGET_eq  1+pi log z1+pi log zbar2        ANTI    sep=F  cf=F   ENTANGLED CHIRAL ANTI (target type)

## Conclusion — [DERIVATION]

ENTANGLEMENT != CHIRALITY (the seductive quantum analogy is a WALL):
- Holomorphic entanglement (non-separable inter-mode but d-bar=0): z1z2+(z1z2)^2 -> ENTANGLED HOLO
  = eml WALL. Entanglement alone carries NO anti.
- Symmetric chiral coupling z1 zbar2 + z2 zbar1 (EPR-like): full_conj-invariant -> REAL = wall.
- The ONLY two-mode form reaching the target is a NON-FACTORIZABLE CROSS-MODE chiral coupling
  (mode1 via its holo part log z1, mode2 via its anti part log zbar2, additive): -> ENTANGLED
  CHIRAL ANTI.

REFINEMENT (corrects tonight's earlier pi!=phi emphasis): TARGET_eq (equal coefficients pi,pi)
ALSO reaches the target. So the essential ingredient is the CROSS-MODE chiral non-factorizable
structure (z1-holo crossed with z2-anti), NOT the incommensurability pi!=phi. The pairing that
would make it a real wall requires z1 with zbar1 (same mode); crossed z1-zbar2 escapes even with
equal coefficients.

New tool: two-mode classifier with dual diagnostics (inter-mode separability + chiral factorization).

## Holo / anti ledger update

- eml (holo): z1^2, z1*z2; ENTANGLED HOLO z1z2+(z1z2)^2 (entanglement is holomorphic = eml wall).
- eml* (anti) SEPARABLE (half-chiral wall): log zbar1, exp(i pi z1+i phi zbar2).
- eml* (anti) ENTANGLED CHIRAL (target type, FORM only): 1+pi log z1+phi log zbar2, and equal-coeff version.
- Walls: REAL (|z1|^2+|z2|^2, EPR symmetric coupling), MODULE (z1 zbar2).
- ANTI forced + measurable + gauge-invariant + entangled-chiral: still ZERO. Chiral cell EMPTY.
- Key law: entanglement != chirality; target = cross-mode chiral non-factorizable coupling.

## Open verrou — [CONJECTURE]

A physical two-mode system whose measurement couples the HOLO part of one mode to the ANTI part of
the other (cross-mode chiral, non-factorizable), forced and read by interference. Candidates to
frame next: chiral optical couplers, Sagnac cross-coupling between two arms, two-valley Hall mixing
(left-valley x right-valley). (b)+(c) together -- never realized.

## Files
- nonseparable_judge.py (classifier)
- this trace
