# FINDINGS 2026-06-23 — pi and phi as a double helix under the orthogonal axis

**Status:** [ESTABLISHED] 9/9 judge verdicts (this machine) · [DERIVATION] pairing/factorization law · [CONJECTURE] physical realization.

## What was tested

pi and phi as a double helix (two strands, two pitches) under the orthogonal axis. Decisive
question: are the holo/anti strands PAIRED (anti coeff = conj of holo coeff -> mirror/modulus ->
wall) or UNPAIRED (different coeffs)? Since pi != phi (incommensurate), unequal strand coefficients
are unpaired. A finer FACTORIZATION diagnostic (d_z d_zbar log f = 0 <=> f = holo(z)*anti(zbar))
splits "ANTI" into separable (half-chiral wall) vs entangled (target type).

## Exact command

cd ~/Desktop/oxieml-star && python3 pi_phi_double_helix.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 9/9 agree, EXIT=0

dh_powers_pitch  z^(i pi) zbar^(i phi)        MODULE_TRAPPED  spin i(pi-phi)  fact=True   WALL_PAIRED
dh_plane_mult    exp(i pi z + i phi zbar)     ANTI            spin n/a        fact=True   SEPARABLE half-chiral WALL
dh_plane_paired  exp(i pi z - i pi zbar)      REAL_TRAPPED    spin n/a        fact=True   WALL_PAIRED
dh_plane_neqpair exp(i pi z - i phi zbar)     ANTI            spin n/a        fact=True   SEPARABLE half-chiral WALL
dh_log_unpaired  P(1+pi log z+phi log zbar)   ANTI            spin n/a        fact=False  ENTANGLED unpaired ANTI (target)
dh_log_paired    P(1+pi log z+pi log zbar)    REAL_TRAPPED    spin 0          fact=False  WALL_PAIRED
dh_ratio_holo    z^(i phi/pi)                 HOL             spin i phi/pi   fact=True   HOL (one-sided)
ctrl_real  z+zbar                             REAL_TRAPPED    spin n/a        fact=False  WALL_PAIRED
ctrl_anti  log zbar (pure)                    ANTI            spin n/a        fact=True   SEPARABLE half-chiral WALL

## Conclusion — [DERIVATION]

The double-helix verdict is governed by PAIRING; pi != phi (incommensurability) is what breaks it.
- As EXPONENTS (spiral pitches) z^(i pi) zbar^(i phi): powers always pair -> MODULE (wall),
  regardless of the different pitches. spin is complex i(pi-phi) but still a wall.
- As MULTIPLICATIVE strands exp(i pi z)*exp(i phi zbar): FACTORIZES (d_z d_zbar log f = 0) -> the
  anti is a pure-anti factor dressed by a holo factor = SEPARABLE half-chiral WALL, NOT entangled.
- As ADDITIVE unequal log coefficients (1 + pi log z + phi log zbar), pi != phi: does NOT factorize
  -> ENTANGLED unpaired ANTI = the orthogonal-axis target type.

New diagnostic added to the toolset: FACTORIZATION (d_z d_zbar log f). It separates SEPARABLE anti
(half-chiral wall, f = holo x anti) from ENTANGLED anti (genuine target), a distinction the 4-label
judge alone does not make. ANTI + factorizes = wall; ANTI + non-factorizes = target type.

This is the FIRST intuition of the session to reach the genuine-target side -- but only as a FORM.

## Open verrou — [CONJECTURE]

The entangled unpaired form (dh_log_unpaired) is genuine-target-type, but: (b)+(c) unproven. Is the
unequal-coefficient unpairing FORCED by a physical system (SPARC: can it be gauged to paired?), and
is it carried by a MEASURABLE natively-complex observable (interference, non-separable coupled modes)?
Lead to frame next: two coupled waves in a NON-SEPARABLE state (cannot write as left x right) with an
incommensurate phase offset, read out by interference (entanglement / incommensurate beats / coupled
non-factorizable modes).

## Holo / anti ledger update

- eml (holo): z^(i phi/pi), dh_ratio_holo (one-sided log spirals).
- eml* (anti) SEPARABLE (half-chiral wall): exp(i pi z + i phi zbar), exp(i pi z - i phi zbar), log zbar.
- eml* (anti) ENTANGLED (genuine target type, FORM only): P(1+pi log z+phi log zbar).
- Walls: MODULE (powers w/ complex pitch), REAL (paired plane wave, paired log, real curve).
- ANTI forced + measurable + gauge-invariant + entangled: still ZERO. Chiral cell EMPTY.
- New tool: factorization diagnostic (separable vs entangled anti).

## Files
- pi_phi_double_helix.py (harness)
- this trace
