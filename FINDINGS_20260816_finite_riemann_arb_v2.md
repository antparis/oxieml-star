# FINDINGS 2026-08-16 — finite two-channel Riemann certificate v2 (#069)

Status: **[ESTABLISHED machine+judge] for the finite certificate only.**
All-height Riemann hypothesis: **NOT TESTED, NOT PROVED.**
EML / eml0 / eml-star / EML2PI: **no claim, no promotion.**
Mathematical novelty: **none.**

Executed on Anthony's ThinkCentre M920q, Ubuntu, 2026-08-16T09:06:57Z–09:09:32Z
(FLINT 3.0.1, cc 13.3.0, Python 3.12.3, SymPy 1.14.0).
Sealed run: `runs/finite_riemann_arb_v2/20260816T090657Z`.

## Exact claim that passed

In the rectangle `-1/2 <= Re(s) <= 3/2`, `|Im(s)| <= T_CERT`, with

```text
T_CERT = [237.1470250733707049028560669410250432418 +/- 4.51e-38]
```

the producer reports a unique even winding `N_TOTAL_FULL_RECTANGLE = 200`
from a certified `xi'/xi` contour integral, and serializes `K = 100`
distinct positive Hardy-Z intervals. Conjugate symmetry of `xi` then
gives 200 critical-line zeros in that finite rectangle. Equality leaves
no room for an extra off-line, real-axis or missed-multiplicity xi zero
**below this T only**.

`K` is a positive-zero **index**, not a height. The 100th serialized
interval is `[236.5242296658162058024755079556629786895 +/- 2.95e-38]`,
matching the classical tables.

Producer status: `PASS_FINITE`. `RH_ALL_HEIGHTS=NOT_TESTED`.

## What was refused first

v1 (`EML2PI_RIEMANN_FINITE_ARB_CANDIDATE_20260816.zip`) used
`acb_dirichlet_zeta_nzeros()` as the "total" channel. That routine
shares FLINT's `_separated_list` machinery with the Hardy-Z isolator, so
the two channels were not algorithmically independent. v1 also treated
a zero-free `xi` contour as if it were an argument-principle count.
v1 is **[REFUSED]**. It was not re-run as a passing certificate.

## What v2 actually does

Two counting algorithms, one shared ball backend:

1. Total channel: `acb_calc_integrate` of the exact logarithmic
   derivative of FLINT's `xi(s) = (1/2) s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)`
   around the full symmetric rectangle. Left edge uses `xi(s)=xi(1-s)`.
   `acb_dirichlet_zeta_nzeros` is forbidden in executable C (static
   wiring gate; the binary contains no such symbol).
2. Line channel: `_acb_dirichlet_isolate_turing_hardy_z_zero` at indices
   K and K+1, plus `acb_dirichlet_hardy_z_zeros` for K serialized
   positive intervals. T_CERT sits strictly between the refined K-th
   and (K+1)-st balls.

Independence label, sealed in the certificate:
`CHANNEL_INDEPENDENCE=ALGORITHMIC_SHARED_BALL_BACKEND`.
Not software-independent. Not backend-independent.

## Machine result on Anthony's disk

| Item | Digest / value |
|---|---|
| Archive | `f067aac32503caf6d47df40d4858fee3ededb69759140047af1e9d41a37f3059` (17178 bytes) |
| C producer | `9ef3e329b29bc932df488333298b1762f996a51e43d79d6cb558f01dcca66fe7` |
| SymPy judge | `d24c027671674c1d26e55145c29c4c0e1e83f4fb36a7cf71be2fca2352024a1e` |
| Runner | `d4ebe6f40ee3fac95417782fbf89a70f714784b1aa809f39d8dbe2a110c0cdcf` |
| Audit | `b64da44ba97cb5d75344c0b6c4cea1cfbacea2c111e86b2a8178f9abf47003cb` |
| Certificate | `dd654112186e998ea3faa06b5a8a77707545e0ac057019b8f7dd2ae7a8481c0e` |
| Line intervals | `ee2ba2f7640f0786d5029a0665157977a53b45e2007e43f94d51a3cd556f73f3` |
| Judge output | `ff432119485c901f98410fb5719e5c6e7aa3b1d777a8c2d6b5eab5a8f07e7468` |
| Compile / producer / judge / overall | 0 / 0 / 0 / 0 |
| Compile, producer, judge stderr | empty |
| Judge | 23/23 PASS |
| Portable manifest | 24/24 files re-checked on disk |

Location (outside every repository):

`~/Téléchargements/eml2pi_riemann_finite_arb_v2_20260816/`

## What the judge does and does not do

The 23 clauses check the sealed contract, the exact `xi'/xi` identity,
and three symbolic reach controls:

- M2 even-multiplicity zero retained by argument counting;
- M3 off-line symmetric quartet makes total and line counts disagree;
- M4 a symmetric quartet may still sit above every finite T.

They do **not** re-run FLINT arithmetic. They do **not** compile four
separate mutant binaries. A4 assumes xi conjugate symmetry rather than
serializing the 100 negative intervals. That symmetry is a theorem, not
a second isolation.

## Scope locks

- Finite height only. The runner itself prints `[PENDING REVIEW]` and
  refuses all-height promotion.
- Classical Turing / Hardy-Z / argument-principle architecture already
  in FLINT and in Platt–Trudgian-type verifications. No new theorem.
- The earlier meta-audit `AUDIT_20260816_EML2PI_RIEMANN.md` still holds:
  a winding number does not locate zeros. This package is a **locator
  plus counter** pair, not an EML primitive.
- `winding_lens.py` remains heuristic. It is not this certificate.

## Authoritative references (method, not novelty)

- https://flintlib.org/doc/acb_dirichlet.html
- https://flintlib.org/doc/acb_calc.html
- Turing, PLMS 1953, https://doi.org/10.1112/plms/s3-3.1.99
- Platt–Trudgian, https://arxiv.org/abs/2004.09765
