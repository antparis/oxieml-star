# FINDINGS 2026-06-23 — Axis D engine v1: symmetric (eml H^{1,0} & eml* H^{0,1}) + rigorous period

**Status:** [ESTABLISHED] symmetric engine (11/11, this machine) · COHOMOLOGY [ESTABLISHED for elementary primitive] / UNDECIDED otherwise.

## What was built and tested

dolbeault_v1.py upgrades v0 on the two fronts mandated before any anti claim:
(1) SYMMETRY (eml/eml* rule): one engine, two directions — anti (d-bar, H^{0,1}, eml*) and
    holo (d, H^{1,0}, eml). Irreproachable on holo: a holomorphic function's anti-form is ZERO.
(2) RIGOROUS PERIOD: COHOMOLOGY decided by single-valuedness (monodromy) of the primitive —
    exact for an elementary closed-form primitive (log / non-integer power => nonzero period);
    UNDECIDED if SymPy finds no closed-form primitive (no claim).

v0 (dolbeault_v0.py) left UNTOUCHED as reference pivot.

## Exact command

cd ~/Desktop/oxieml-star && python3 dolbeault_v1.py; echo "EXIT=$?"

## Raw result (this machine) — 11/11 self-consistent, EXIT=0

anti  zero [0,0]            ZERO
anti  exact g=zb1^2 zb2     EXACT
anti  cohom [1/zb1,0]       COHOMOLOGY  log(zbar1)
anti  notclosed [zb2,0]     NOT_CLOSED
holo  zero [0,0]            ZERO
holo  exact g=z1^2 z2       EXACT
holo  cohom [1/z1,0]        COHOMOLOGY  log(z1)
holo  notclosed [z2,0]      NOT_CLOSED
irrep holo-func anti-form   ZERO        (never flagged anti)
irrep holo-func holo-form   EXACT       1/z1
ctrl  real-field anti       EXACT       z1*zbar1

SYMMETRY CHECK passed: holomorphic function -> anti-form ZERO. Irreproachable.

## Scope and limits

- COHOMOLOGY rigorous for ELEMENTARY primitives only; non-elementary -> UNDECIDED.
- True Dolbeault residue for non-elementary primitives is future (v1a-bis).
- Pure SymPy; standalone from judge_v2.

## Holo / anti ledger update

- Tool now symmetric: eml (H^{1,0}) and eml* (H^{0,1}) both detected, plus control.
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.

## Files
- dolbeault_v1.py (symmetric engine)
- this trace
