# FINDINGS 2026-06-24 — DRUM field level (1+1D) = SPARC-closed; device closed entirely

**Status:** [DERIVATION] (exact Wirtinger algebra + SPARC argument; a framing
result, not a judge certification of a physical anti closed-form). Executed on the
M920q. Follows FINDINGS_20260624_drum_tcmt_sparc_wall.md (modal level).

## What was tested

Whether the DRUM, taken at the FIELD level (1+1D field in the ring, not the 2-mode
TCMT), can carry a genuine anti-holomorphic structure where the modal level could
not. Frame-before-simulate: the question is settled by framing; no simulation run.

## Command

    cd ~/Desktop/oxieml-star && python3 drum_field_sparc.py

Witness: `drum_field_sparc.py`. Transparent Wirtinger test, z = x + i y,
d/d(zbar) = 1/2 (d/dx + i d/dy).

## Raw result (three branches, all closed)

- (a) Real light-cone: u = s - v t (CW), w = s + v t (CCW). With s, t, v real,
  conj(u) = s - v t = u, while w = s + v t; hence `w - conj(u) = 2 v t != 0`.
  The two movers are NOT complex conjugates -> (u, w) is NOT (z, zbar). Chirality
  here is FACTORIZATION on real coordinates, not Wirtinger anti-holomorphy.
  Encoding z = u (real) gives conj(z) = z, so eml = eml(star): SPARC option A.

- (b) Wick t -> -i tau_E: z = s + v tau_E is genuinely complex and conj(z) =
  s - v tau_E, so the Wirtinger test applies. BUT Wick is an ERASABLE treatment
  choice (the DRUM lives in real time); it reverts to (a) in real time. Forced
  only under thermal/KMS periodicity, which a passive DRUM does not have. SPARC.

- (c) Non-Hermiticity: `d/d(zbar) exp(-i*lambda*z) = 0 -> HOL` even for
  lambda = omega0 - i gamma complex. The loss gamma is a PARAMETER in the
  exponent, not an independent zbar. A complex (non-Hermitian) frequency creates
  NO spatial anti-holomorphy. Same mechanism as the Yang-Mills NH LCFT wall
  (commit 07792fd).

## Verdict

DRUM is CLOSED ENTIRELY — modal AND field level. Its physical complex content
lives either in real light-cone coordinates (factorization, not anti), in an
erasable Euclidean rotation (Wick, SPARC), or in a temporal/spectral exponent
(non-Hermitian frequency, HOL). None of these is a genuine spatial d/d(zbar).
Chiral cell: still empty.

## Derived method gain — 7th sieve condition (for forcing_filter.py)

complexity_carrier == SPATIAL-anti-holomorphic, NOT temporal-exponent.

This eliminates upfront, without simulation, every candidate whose complexity sits
in a temporal/spectral exponent of a real variable: Hatano-Nelson, Yang-Mills NH
LCFT, PT free-fermion, and now DRUM. It sharpens the standing invariant: "non-
Hermitian" is necessary but NOT sufficient — the non-Hermiticity must inject the
complex into the spatial (anti-holomorphic) sector of the correlator, not into a
temporal exponent.

## Live door (next)

Non-equilibrium two-bath steady state (Lindblad): the only remaining carrier where
the complex can enter the SPATIAL correlator via stationary currents rather than a
temporal exponent. To be framed next, with its own SPARC test (is the current that
carries the complex PHYSICAL — non-removable — or GAUGE — removable?).

## Symmetry ledger update

WALL added: DRUM, field level (1+1D) — SPARC-closed (light-cone real / Wick choice
/ non-Hermitian exponent), [DERIVATION]. Combined with the modal-level FINDINGS,
the DRUM is closed in full. Chiral cell: empty.

## Trace files

- drum_field_sparc.py (witness, reproducible)
- FINDINGS_20260624_drum_field_level_sparc_closed.md (this file)
- (companion) drum_tcmt_wall.py + FINDINGS_20260624_drum_tcmt_sparc_wall.md (modal level)
