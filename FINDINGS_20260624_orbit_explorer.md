# FINDINGS 2026-06-24 — orbit_explorer: removability lattice, interior cell non-empty

**Status:** [DERIVATION] — Wirtinger-exact, executed on the M920q (imports the
authoritative judge_v2.py). Structural cartography, NOT a path to the target.

## What was tested

Anthony's "inner cubies" intuition, made operational: the removability generators
(reality / module / base) form a lattice whose subsets are the cube's corners.
Are the INTERIOR cells (removable by several generators at once) non-empty, with
concrete f the judge confirms — or do they collapse onto the pure walls?

Scope of this step: the 2x2 lattice of the two OPERATIONAL generators,
reality (full_conj(f) == f) x module (is_module_trapped(f)). 'base'
(basis-removable) needs its own operational criterion -> later (2^3 cube).

## Command

    cd ~/Desktop/oxieml-star && python3 orbit_explorer.py

`orbit_explorer.py` is a layer ON TOP of judge_v2 (not a new judge). It computes
the FULL removability signature, not certify_1field's first-label-only output.

## Raw result (cell map)

  {reality, module}  INTERIOR : |z|^2 (z*zbar), log|z|^2 (log z + log zbar)
  {reality}          pure     : z + zbar, Im z
  {module}           pure     : z/zbar, z**2 * zbar
  {} empty-signature          : z, zbar, z + 0.3 zbar, vortex A log(z-c)+B log(zbar-c)

## Finding

The interior cell {reality & module} is NON-EMPTY: real radial functions like
|z|^2 and log|z|^2 are removable by BOTH generators (doubly-removable). The judge
masks this: certify_1field stops at the first label in its order
(holo -> real -> module -> anti), printing only 'real-trapped' and never
revealing that these forms are ALSO module-trapped. So:
 - the judge's 4 labels are NOT mutually exclusive; reality and module OVERLAP;
 - the test ORDER collapses the overlap; the full signature recovers it.

Anthony's intuition is confirmed (there IS information in the cube's interior),
but the content is "more trapped", not closer to the target: doubly-removable is
the opposite of the chiral cell. This is cartography (walls overlap, judge masks
it), NOT a breakthrough. No exotic cell, no path to the empty target corner.

## Caveat on the empty-signature cell

{} is COARSE: it lumps holo, anti, mixed AND the chiral target together. Isolating
the target is not orbit_explorer's job — it stays forcing_filter's (unpaired /
transcendental / non-factorizable / spatial_carrier...). The two are complementary:
orbit_explorer maps trap-overlap, forcing_filter isolates the target.

## Open continuation

- Operational criterion for 'base' (existence of a linear similarity rendering f
  holomorphic) -> complete the 2^3 lattice; test whether triple/other pair cells
  are non-empty.
- Note for rigour: the judge's label order is a convention that hides overlaps;
  documented here, judge_v2 left unchanged (authority).

## Trace files

- orbit_explorer.py (reproducible; imports judge_v2.py)
- FINDINGS_20260624_orbit_explorer.md (this file)
