# FINDINGS 2026-06-22k -- Indefinite theta gives SAME grid class as unary: Zwegers motif is UNIVERSAL across the mock theta family

## Status
[ESTABLISHED] (machine, code 0). The indefinite-theta (mixed-signature) Zwegers completion
gives the SAME three-operator grid class as the unary order-3 case. The orthogonal axis
"definite vs indefinite shadow" reveals NO new class. Negative on the distinction, but
ROBUST: the "real factor modulates, not reduces" motif is universal across the whole mock
theta family. Settles the order-5/7/10 question definitively (all same grid cell).

## Why this was the right axis to test (not orders 5/7/10)
Research confirmed: ALL mock theta (orders 3,5,7,10) have the SAME Zwegers structure --
holomorphic mock part + non-holo completion via a weight-3/2 unary theta shadow. Testing
5/7/10 would only re-confirm the known theorem (capability, not discovery). The genuinely
DIFFERENT structure is the INDEFINITE theta (mixed-signature quadratic form, Andrews order-5
quotients Theta/theta, Moore order-10 via Mordell integrals): its raw sum diverges, Zwegers
regularizes sgn(...) -> erf(sqrt(2y)...) INSIDE the sum (vs unary where the y-term sits
beside). That internal real factor is structurally different -- the only form whose grid
verdict was not known in advance.

## Result (machine, three-operator grid)
  indef raw (holo in q)                 eml:holo  eml*:holomorphic       eml0:not-pure-phase
  indef completed erf(sqrt y) q^n       eml:-     eml*:anti-holomorphic  eml0:not-pure-phase
  erf(sqrt y) alone                     eml:-     eml*:real-trapped      eml0:not-pure-phase
  erf(sqrt y) * q^(-1)                  eml:-     eml*:anti-holomorphic  eml0:not-pure-phase
  erf(sqrt y) * exp(-2pi i zbar)        eml:-     eml*:anti-holomorphic  eml0:not-pure-phase
  unary anchor y^(-1/2) conj(g3)        eml:-     eml*:anti-holomorphic  eml0:not-pure-phase
=> indefinite completion == unary anchor (anti, not-pure-phase). erf(sqrt y) alone is
real-trapped: same mechanism as unary (real factor modulates conj-modular without reducing).

## Interpretation
The Zwegers motif (real y-factor MODULATES the anti, does NOT reduce it) is UNIVERSAL: it
holds for unary shadows (order 3) AND indefinite/mixed-signature shadows (orders 5,10). The
whole mock theta family occupies ONE grid cell: raw = holomorphic [measurable], completion =
anti-holomorphic + not-pure-phase [formal]. Mixed signature changes the convergence/
regularization (sgn->erf inside vs y-term beside) but NOT the (z,zbar) class.

## Consequences
- Settles "test orders 5/7/10": unnecessary. Same cell, and we now know WHY (universal motif).
- Reinforces the formal-localization picture (0622h, 0622i): the entire mock theta family is a
  formal habitat of transcendental anti; the measurable object (raw mock theta) is always holo.
- The three-operator grid is robust: it gives a consistent, structural classification across
  a whole mathematical family, not case-by-case accidents.

## Honest note
This is a NEGATIVE result on novelty (no new grid class from indefinite theta) but a POSITIVE
result on robustness/universality. It confirms capability (the grid classifies the family
consistently), not a discovery. Per the standing rule, recovering a consistent known-structure
classification = capability, not revelation. No measurable transcendental anti found here.

## Files
indefinite_theta_grid.py, this FINDINGS. Builds on 0622i (Zwegers unary), 0622j (eml0 / grid).
