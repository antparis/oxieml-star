# FINDINGS 2026-06-24 — Lindblad / NESS two-bath: eliminated upstream (reconnaissance)

**Status:** [DERIVATION] — literature reconnaissance + upstream sieve (forcing_filter,
7 conditions). NOT a judge certification of a closed form: it is an argued fallback
onto already-certified walls. No simulation run (frame-before-simulate: the framing
settles it).

## What was tested

Whether a two-bath Lindblad / non-equilibrium steady state (NESS) can carry a
genuine, non-paired, SPATIAL anti-holomorphic structure forced by the steady
current — the only live carrier where the complex could enter the spatial
correlator rather than a temporal exponent (FINDINGS_20260624_drum_field_level,
7th sieve condition).

## Method

Reconnaissance of concrete NESS systems (boundary-driven spin chains, exclusion
processes, non-Hermitian topological chains, Keldysh transport, 2D driven-
dissipative lattices), then upstream sieve. Focus on the 7th condition:
is the complex carried in the SPATIAL anti sector, or in a temporal/spectral
exponent of a real variable?

## Three rejection modes

1. Real-field NESS -> REAL-TRAPPED. Boundary-driven NESS correlators are
   correlators of REAL fields, e.g. C_{i,j} = <sigma_i^z sigma_j^z>
   (random spin chain, arXiv:1701.05090). Navigation law: a real scalar in a
   frozen state is mirror-locked -> real-trapped. Rejected on `unpaired`.

2. Non-Hermitian NESS -> complex in the SPECTRUM, not in zbar. In the 1D
   topological non-Hermitian chain (arXiv:2111.02223), gamma adds an imaginary
   part to the eigenvalues (a loop in the complex spectral plane) and the
   steady current comes from the WINDING of that loop. The complex is a spectral
   exponent -> 7th sieve condition rejects (spatial_carrier = False), exactly
   like DRUM and Hatano-Nelson.

3. Keldysh IR -> classical real reflux. Driven-dissipative many-body systems
   generically flow at large scales to effectively CLASSICAL field theories
   (Ising/XY/KPZ) with an effective temperature (Maghrebi et al. 2015, via
   emergentmind NESS review). The IR reverts to real-trapped. The DC current of
   1D rings is treated in a "temporal gauge" (linearly increasing flux,
   arXiv:1506.04957) -> gauge, hence removable on the SPARC test.

## Cold-conjecture residual [CONJECTURE]

A natively complex order parameter Delta in a 2D non-equilibrium superconductor
(2D Hubbard coupled to electrodes, arXiv:1012.0980): the ANOMALOUS correlator
<Delta(z) Delta(0)> (not <Delta Delta*>, paired by conjugation) could in
principle carry a non-paired zbar. But:
  - uniform supercurrent (pair momentum q != 0): Delta ~ Delta0 * exp(i Re(q* z)),
    |Delta| constant -> MODULE-TRAPPED (as Landau / Aharonov-Bohm). Wall.
  - vortex/antivortex: Delta ~ z (holo) or zbar (pure anti) -> ALGEBRAIC and
    paired, not transcendental. Wall (WALL_PAIRED).
Non-equilibrium adds spectral (relaxation-rate) complexity, not a non-paired
spatial transcendental. The residual most likely falls back onto mapped walls;
left as a COLD conjecture, not judged.

## Verdict

The two-bath Lindblad / NESS family is eliminated UPSTREAM, without simulation:
real-field correlators -> real-trapped; non-Hermitian carrier -> 7th condition
(spectral winding); IR -> classical real; ring flux -> gauge. The freshly added
7th sieve condition does the discriminating work on the non-Hermitian sub-type.
This is reconnaissance, not a certified wall. Constructing a minimal Liouvillian
now would be simulating an already-eliminated case.

## Symmetry ledger update

WALL (reconnaissance) added: Lindblad/NESS two-bath — real-trapped / spectral-
exponent / gauge, [DERIVATION]. Chiral cell: still empty.

## Trace files

- FINDINGS_20260624_lindblad_ness_reconnaissance.md (this file)
- (sieve) forcing_filter.py (7th condition spatial_carrier, commit 7f9323b)
