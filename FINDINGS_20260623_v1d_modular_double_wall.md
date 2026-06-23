# FINDINGS 2026-06-23 — v1d modular: the tau front is a DOUBLE WALL

**Status:** [ESTABLISHED] 7/7 judge verdicts (this machine) · [DERIVATION] double-wall conclusion.

## What was tested

CERTIFIER test of the FORCED tau-bar dependence of modular completions (tau==z, taub==zbar),
the front recommended last as "candidate n.1" (holomorphic anomaly / E2*). Adversarial result:
the modular/tau front splits into two walls, neither fills the chiral cell.

E2*(z,zbar) = E2(z) - 3/(pi*Im z), Im z = (z-zbar)/(2i).

## Exact command

cd ~/Desktop/oxieml-star && python3 v1d_modular.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 7/7 agree, EXIT=0

E2star_completion -3/(pi Im z)   REAL_TRAPPED   W1: forced but REAL -> fails (b)
mock_completion_schematic        ANTI           W2: complex anti -> passes (b), fails (c)
E4(z) holomorphic                HOL            holomorphic control (eml)
E6(z) holomorphic                HOL            holomorphic control (eml)
y = Im z (real control)          REAL_TRAPPED   real control
z^2 (holo control)               HOL            holo control
z/zbar (module control)          MODULE_TRAPPED module control (eml0)

dbar E2* = -6i/(pi (z-zbar)^2) = 3i/(2 pi (Im z)^2) != 0  (anti EXISTS, forced; but E2* is REAL -> mirror)

## Conclusion — [DERIVATION]

The modular/tau front is a DOUBLE WALL:
- W1 quasi-modular / holomorphic-anomaly (E2*): the forced completion -3/(pi Im z) is REAL-valued
  -> mirror -> REAL_TRAPPED. dbar E2* != 0 (anti exists, forced by modularity) but it is the forced
  reflection of a real correction, NOT independent. FAILS criterion (b). "forced != chiral".
- W2 mock modular (Zwegers): the non-holomorphic Eichler integral is genuinely COMPLEX -> ANTI
  (passes (b)), but it is not a measured observable -> FAILS (c). (project-known, reconfirmed.)

Reinforced navigation law: every measurable carrier of E2* (torus partition function, string
threshold corrections to gauge couplings, topological-string free energy F_g / BCOV propagator,
modular determinants / eta) is a REAL-valued physical quantity -> forced tau-bar part = mirror =
real-trapped. Measurability is achievable but useless here because the carrier is real. Genuine
chiral anti requires a NATIVELY COMPLEX measurable (amplitude / phase / visibility), NOT a real
free energy. This closes/refines the modular front and redirects the hunt to natively-complex
measurables (Kerr/Psi4, amplitude visibilities).

## Holo / anti ledger update

- eml (holo) confirmed: E4, E6, z^2 -> HOL.
- eml* (anti) genuine: mock_completion_schematic -> ANTI (but not measurable).
- Walls: E2* completion + y -> REAL_TRAPPED; z/zbar -> MODULE_TRAPPED.
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.
- New wall sub-type recorded: "forced-but-real" (modular completion) = real-trapped.

## Files
- v1d_modular.py (harness)
- this trace
