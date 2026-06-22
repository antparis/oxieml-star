# FINDINGS 2026-06-22i -- Zwegers completion ESCAPES the wall (real factor modulates, not reduces) -- 2nd formal localization of transcendental eml-star

## Status
[ESTABLISHED] (machine, corrected judge, code 0, structural AND exact forms agree). The
Zwegers completion of Ramanujan's 3rd-order mock theta f(q) carries a genuine TRANSCENDENTAL
IRREDUCIBLE anti-holomorphic structure that ESCAPES the module/real wall -- the FIRST object
this session to do so. BUT it lives in the COMPLETION (formal object); the measurable mock
theta f(q) itself is holomorphic. So: confirms conjecture HALF 1 (transcendental anti exists,
in the formal), does NOT contradict HALF 2 (not in a measurable observable).

## The mechanism (why Zwegers differs from the 6 walls)
The non-holomorphic completion is entangled with the REAL quantity y = Im(tau) = (tau-taubar)/2i
via an incomplete gamma factor (Zwegers/Zagier exact form). Key distinction confirmed on machine:
  - y^(-1/2) alone                       -> REAL-TRAPPED (real factor is a wall by itself)
  - beta(y)=uppergamma(1/2,pi y) alone   -> REAL-TRAPPED
  - conj(g3) alone                       -> anti-holomorphic (function of taubar)
  - y^(-1/2) * conj(g3)                  -> ANTI-HOLOMORPHIC (real factor MODULATES, not reduces)
Unlike the 6 walls (AB, inverse-square, superconductor, LCFT spin-2, winding angle, c=-2 scalar)
where zbar was TRAPPED INSIDE the real (symmetric modulus / real angle), here conj(g3) stays a
genuine function of taubar; multiplying by a real factor y does NOT symmetrize it under
tau<->taubar. The anti is not reducible by division (y is real, not a z^a zbar^b modulus).

## Exact Zwegers forms tested (from research, 3rd-order f(q))
  shadow      g3(tau) = sum_n (-12/n) n q^(n^2/24)            [weight 3/2 unary theta]
  derivative  d f_hat/d taubar ~ y^(-1/2) conj(g3)            [k=1/2]
  completion  R3(tau) = sum_{n≡1(6)} sgn(n) beta(n^2 y/6) q^(-n^2/24),  beta=uppergamma(1/2,pi x)/sqrt(pi)
  full        f_hat = q^(-1/24) f(q) + R3

## Results (machine, judge corrected, code 0)
PART 1 structural (class is exponent-independent, authoritative):
  (a) y^(-1/2)*conj(g3)        -> anti-holomorphic
  (b) beta(y)*q^(-1) [R3]      -> anti-holomorphic
  (c) f(q)+beta(y)*q^(-1)      -> anti-holomorphic
  (d) bare mock f(q)=q+q^2     -> HOLOMORPHIC  [MEASURABLE object]
PART 2 exact (n^2/24, real shadow, time-guarded -- all finished, no timeout):
  (a-exact) y^(-1/2)*conj(g3)  -> anti-holomorphic
  (b-exact) R3 incomplete gamma-> anti-holomorphic
  conj(g3) exact               -> anti-holomorphic

## Interpretation
HALF 1 [ESTABLISHED, reinforced]: transcendental irreducible anti EXISTS and is judge-certified.
Zwegers completion is the 2nd independent formal localization (after symplectic fermions c=-2).
Two independent math families (chiral CFT + mock modular forms) carry the same transcendental
anti, both in the FORMAL component.
HALF 2 [CONJECTURE, not contradicted]: the MEASURABLE object (bare mock theta f(q), a partition
generating function) is HOLOMORPHIC (d). The anti appears only in the completion f_hat, a
mathematical construction (added to restore modularity), not a measured quantity. Criterion (c)
NOT met. Consistent with the hermiticity conjecture.

## Significance
First object this session to escape the module/real wall. Sharpens the picture: the wall is
not "any real factor kills the anti" -- a real factor MULTIPLYING a genuine taubar-function
only modulates. The wall is specifically "zbar trapped inside a symmetric real structure
(modulus, angle)". Zwegers avoids that trap. But measurability (c) still fails: the escape
happens in the formal completion, not the measurable mock theta.

## Files
zwegers_exact_judge_v2.py (structural + time-guarded exact), this FINDINGS.
Builds on 0622h (symplectic fermion localization), the Zwegers/Zagier exact-form research.
