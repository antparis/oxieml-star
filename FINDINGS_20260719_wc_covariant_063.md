# FINDINGS 2026-07-19 -- Covariant reciprocity witness W_C (#063)

Status: [ESTABLISHED machine+judge]
Harness: wc_covariant_test.py (sha256 650ce332, 10968 bytes)
Executed: Anthony's machine (ThinkCentre M920q, Ubuntu), 2026-07-19
Command: python3 wc_covariant_test.py
Raw verdict: 13/13 clauses PASS, exit 0

## What was tested

Extension of the comparative reciprocity witness W = D_X - D_Y (#057,
certified in port basis C = I only) to general diagonal calibrations
C = diag(c1, c2), closing the "open certification target" declared in
the one-way paper v11. Candidate: W_C = D_X - (c1/c2) D_Y, with
S_C(A) = C^{-1} A^T C (C symmetric) plus sector swap X <-> Y,
R_C = G - S_C(G) on the complete 2x2 kernel. Sixth-audit block-diagonal
counter-example (build_v10 trace) used as the C-reciprocal probe:
G21 = (c1/c2) F(X), G12 = F(Y), F = log(1-u), cut discontinuities
computed by exact SymPy directional limits (D = -2*I*pi at u=2 and u=3).

## Certified results (SymPy exact, Wirtinger convention #059,
## c1 c2 unrestricted nonzero COMPLEX symbols)

- J0  [LIMITE/scope] Non-diagonal symmetric C mixes the sectors
      (S_C(G)_11 = b*d*log(1-X)/(a*d-b^2) != 0): W_C is scoped to
      sector-preserving (diagonal) calibrations. Not a defect: a
      domain statement.
- J1  The C-reciprocal tour-6 kernel has R_C = 0 (4 entries); the raw
      witness fires falsely on it (W_raw = 2*I*pi*(c2-c1)/c2 != 0 for
      c1 != c2); the covariant witness is exactly silent (W_C = 0).
- J2  W_C reduces to W identically at C = I (generic discs).
- J3  Covariance/antisymmetry: W_C(S_C(G)) = -W_C(G) exactly on
      generic two-sector kernels.
- J4  Sufficiency-never-necessity TRANSPORTS: calibrated K_eps
      (cut-free deformation eps*X^2) has R_C[21] = eps*X^2 != 0 yet
      W_C = 0.
- J5  SIZE LAW (generalized #057): W_C = (c1/c2)(rho-1)*D exactly;
      reduces to W = (rho-1)*D at C = I; holds with the FULL complex
      ratio c1/c2 = r*exp(I*theta) -- the witness must carry the
      ratio's modulus AND angle. Grand-ledger refinement: the
      calibration is a relative size with both components load-bearing.
- J6  Chirality-agnostic (same identity in the holomorphic sector;
      the witness formalism carries no chirality claim by itself);
      shuffle guard: the wrong pairing D_X - (c2/c1) D_Y does NOT
      vanish (W_wrong = 2*I*pi*(c2^2-c1^2)/(c1*c2)).

## Anti-tamper

Negative sweep performed in sandbox before delivery: mutant with
inverted witness fails J5a/J5c; mutant with sabotaged kernel fails
J1c/J6b. No hardcoded verdict; every symbolic zero double-checked by
random complex numeric substitution (|residue| < 1e-12).

## Semantic consequences

- Paper v11 "open certification target" (covariant extension of the
  witness): CLOSED by this entry. A future paper version may cite
  W_C = D_X - (c1/c2) D_Y as certified, scoped to diagonal C,
  separable two-sector class (#057b), sufficient-never-necessary.
- #057/#057b remain intact (their C = I scope was correct); this entry
  SUPERSEDES nothing, it extends.

## Files

- wc_covariant_test.py (sha256 650ce332) -- harness, standalone,
  < 1 min, exit 0 iff 13/13.
- This trace file.
