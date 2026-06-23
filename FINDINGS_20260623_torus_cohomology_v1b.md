# FINDINGS 2026-06-23 — Torus cohomology v1b: GENUINE Dolbeault H^{0,1} (eml*) & H^{1,0} (eml)

**Status:** [ESTABLISHED] torus engine (12/12, this machine) + [DERIVATION/LIMIT] label correction of v0/v1.

## Critical correction of dolbeault_v0/v1 — [DERIVATION/LIMIT]

On Stein domains (all 1-variable local cases, even punctured) H^{0,1}_dbar = 0 (Dolbeault-
Grothendieck). So the v0/v1 "COHOMOLOGY" verdict (multivalued elementary primitive, e.g. [1/zbar]
-> log zbar) was MISLABELED: it detects a PERIOD/RESIDUE obstruction (de Rham/Cech H^1; no single-
valued elementary primitive), NOT smooth Dolbeault H^{0,1}. The detected obstruction is real and
gauge-immune (a nonzero period cannot be removed by single-valued gauge), but it is NOT Dolbeault
cohomology. Two distinct non-removable obstructions now separated:
  (i) period/residue  -> de Rham/Cech H^1, exists in 1 variable WITH topology   (v0/v1)
  (ii) Dolbeault H^{0,1} -> nonzero only on a COMPACT/non-Stein manifold (torus) (v1b)

## What was built and tested

torus_cohomology_v1b.py — genuine Dolbeault H^{0,1} (eml*) and H^{1,0} (eml) on the torus
T = C/(Z + tau*Z). RIGOROUS criterion (replaces the v0/v1 heuristic): a doubly-periodic (0,1)-form
a*dzbar is dbar-EXACT iff its AVERAGE over the fundamental domain vanishes (constant Fourier mode =
the only obstruction). Average != 0 <=> COHOMOLOGY, represented by the harmonic class [dzbar].
This is v1a-bis (rigorous period = average, no heuristic) AND v1b (torus). Calibration tau=i;
criterion is tau-independent. Symmetric for d / [dz] (eml side).

## Exact command

cd ~/Desktop/oxieml-star && python3 torus_cohomology_v1b.py; echo "EXIT=$?"

## Raw result (this machine) — 12/12 self-consistent, EXIT=0

anti  harmonic a=1            COHOMOLOGY  avg=1     (the genuine non-trivial class [dzbar])
anti  harmonic a=i            COHOMOLOGY  avg=I
anti  exact a=dbar(sin2pix)   EXACT       avg=0
anti  exact a=dbar(e^2pix)    EXACT       avg=0
anti  exact a=e^2pix          EXACT       avg=0
anti  cohom a=1+e^2pix        COHOMOLOGY  avg=1
anti  exact a=cos2piy         EXACT       avg=0
anti  zero  a=0               ZERO        avg=0
holo  harmonic b=1            COHOMOLOGY  avg=1     (the genuine non-trivial class [dz])
holo  exact b=dz(sin2pix)     EXACT       avg=0
holo  exact b=e^2pix          EXACT       avg=0
holo  cohom b=2+e^2piy        COHOMOLOGY  avg=2

First GENUINE non-trivial Dolbeault class of the project: harmonic [dzbar] (eml*) and [dz] (eml),
each 1-dimensional on the torus, gauge-immune (compact-manifold Dolbeault, not a residue).

## Scope and limits

- v0/v1 kept as the PERIOD/RESIDUE detector (obstruction (i)); v1b is the Dolbeault detector (ii).
- [dzbar] is the class GENERATOR (math object). NOT yet a Projet A hit: criterion (c) — a measurable
  observable carrying it with FORCED tau-bar dependence — is open (= v1d).
- Pure SymPy; tau=i calibration; general tau same criterion.

## Holo / anti ledger update

- eml (holo) H^{1,0} and eml* (anti) H^{0,1} both certified on the torus, symmetric, plus EXACT/ZERO controls.
- First non-trivial NON-removable, GAUGE-IMMUNE anti class certified: [dzbar] on the torus.
- ANTI forced + measurable (criterion c): still ZERO. Chiral cell EMPTY (generator found, physical realization pending).

## Next (v1d) — physical forced tau-bar

Branch v1b onto E2*(tau,tau-bar) = E2 - 3/(pi Im tau) and eml-mod: test whether the FORCED tau-bar
dependence (holomorphic anomaly / quasi-modular completion) is a non-trivial H^{0,1} class on moduli
space. This is the only route attacking (b) and (c) together, reusing eml-mod.

## Files
- torus_cohomology_v1b.py (engine)
- this trace
