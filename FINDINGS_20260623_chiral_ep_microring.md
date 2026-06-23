# FINDINGS 2026-06-23 — Chiral exceptional point (microring): reciprocal EP is a WALL

**Status:** [DERIVATION/LIMITE] eigenvalue holomorphic wall + reciprocal-EP SPARC artefact; target reached as FORM (level ii) only.

## Context

Candidate from web search: chiral exceptional point (EP) in a non-Hermitian microring (CW/CCW
counter-propagating modes). Two levels analysed: (i) the EP eigenvalue/transmission in complex
frequency; (ii) the ring field psi = a*z + b*zbar (CW amplitude a, CCW amplitude b).

## Judge verdicts (this analysis; pure SymPy; z=omega at level i, z=e^{i theta} at level ii)

LEVEL (i) -- spectral observable in omega only:
  EP eigenvalue  sqrt(omega - omega_EP)   -> HOL  (function of omega only -> eml WALL, branch in omega)
  transmission   1/(omega - E_pole)       -> HOL  (eml WALL; like the GW causality branch cut)

LEVEL (ii) -- ring field psi = a z + b zbar (non-factorizable in all cases):
  reciprocal  b = conj(a)   (1+i)z+(1-i)zbar  -> REAL_TRAPPED         (mirror wall)
  chiral asym b != conj(a)  (1+i)z+2 zbar     -> ANTI, non-factorizable -> ENTANGLED CHIRAL ANTI
  chiral asym mode m=2      (1+i)z^2+2 zbar^2 -> ANTI, non-factorizable -> ENTANGLED CHIRAL ANTI
  pure CW one helicity      (1+i)z            -> HOL                 (eml wall)

## Conclusion — [DERIVATION/LIMITE]

The chiral EP candidate is a WALL on the decisive (SPARC) grounds, despite level (ii) reaching the
target FORM:

1. Level (i): the EP eigenvalue sqrt(omega-omega_EP) and the transmission 1/(omega-E) are functions
   of omega ALONE -> holomorphic -> eml WALL (branch/pole in omega, a de Rham period like the GW
   causality wall already certified). The spectral observable carries no independent anti.

2. Level (ii): the ring field a*z + b*zbar is non-factorizable; with b != conj(a) it reads ENTANGLED
   CHIRAL ANTI (the target form). BUT the asymmetry b != conj(a) of a STANDARD chiral EP (Mie
   scatterer) "arises entirely from combinations of fully reciprocal optical elements and is by no
   means an indication of non-reciprocal behavior" (Nat. Commun./Light Sci. Appl. microring EP
   papers, 2024-2025). => the chirality is BASIS-REMOVABLE -> SPARC artefact -> WALL.

3. Moreover (Sweeney, Hsu, Stone, PRL 122, 093901 (2019)): an EP of the operator is generally NOT an
   EP of the scattering matrix; the MEASURABLE S-matrix does not inherit the EP branch structure.

=> The reciprocal chiral EP does NOT fill the chiral cell. The target form (level ii, b != conj(a)
   FORCED) is reached only by GENUINE time-reversal breaking (magneto-optic/Faraday, time-modulation
   a la Sounas-Alu), NOT by a reciprocal Mie-scatterer EP. And even then the measurable observable
   must be shown to carry it (open).

## Holo / anti ledger update

- eml (holo): EP eigenvalue sqrt(omega-omega_EP), transmission 1/(omega-E), pure-helicity field.
- eml* (anti) FORM-only (target type, level ii): a z + b zbar with b != conj(a) -- but basis-removable
  for a reciprocal EP (SPARC artefact).
- Walls: reciprocal ring field (real), spectral observable (holomorphic), reciprocal chiral EP (basis).
- ANTI forced + measurable + gauge/basis-invariant + non-factorizable: still ZERO. Chiral cell EMPTY.
- New wall entry: reciprocal chiral EP = basis-removable artefact; spectral EP branch = holomorphic wall.

## Open

A genuinely NON-RECIPROCAL two-mode system (broken time-reversal: magneto-optic Faraday ring,
time-modulated coupler) where b != conj(a) is FORCED (not basis), AND a measurable interference
observable carries the cross-chiral non-factorizable anti. Needs a primary-source closed-form
S-matrix of such a T-broken device to judge. Not available yet.

## Files
- ep_check.py (sandbox harness; to be added to repo if kept)
- this trace
