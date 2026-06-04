# FINDINGS 2026-06-04 -- Aharonov-Bohm LLL is NOT a chiral transcendental anti (NEGATIVE)

## Status
[ESTABLISHED] negative result. Executed on machine + SymPy judge exact (Wirtinger).
The candidate is REJECTED as a Project-A chiral transcendental anti-holomorphic system.

## What was tested
Hypothesis: the lowest-Landau-level wavefunction in an Aharonov-Bohm flux,
  psi(z,zbar) = z^(m+alpha/2) * zbar^(-alpha/2) * exp(-|z|^2/4),  m=1, alpha=sqrt(2),
is a physically-forced, gauge-non-reducible TRANSCENDENTAL chiral anti field (the
irrational power zbar^(-alpha/2) being the anti content forced by the flux).
Generator: aharonov_bohm_gen.py. De-Gaussianed target ab_dg_candidate.csv (4790 pts)
= z^(1+sqrt2/2) * zbar^(-sqrt2/2), Gaussian background divided out.

## Commands (exact)
  python3 aharonov_bohm_gen.py
  python3 detect_real_data_bigbudget.py ab_dg_candidate.csv   # niter=60 PySR
  python3 ab_chirality_check.py                               # SymPy exact

## Raw result (judge-certified, on machine)
  d psi_dg/d zbar = -sqrt(2)*z^(sqrt2/2+1)/(2*zbar*zbar^(sqrt2/2))  (nonzero)
  Beltrami mu = (b/a)*(z/zbar) = -sqrt(2)*z/(zbar*(sqrt2+2)), |mu| = sqrt2-1 = 0.4142 CONSTANT
  Factorization: z^a*zbar^b (a,b REAL) = z^(a-b)*(z*zbar)^b = z^(1+sqrt2) * |z|^(-sqrt2)
  PySR niter=60 route B: exp(my_real(eml(z)) + d*eml(z)), MSE=3.6e-19, NO log(zbar) term
  PySR niter=60 route A: MSE=0.093 -> rejected (>=1e-3)

## Verdict: NOT chiral -- "module-trapped"
A power zbar^p with p REAL is never chiral: f = z^a*zbar^b = z^(a-b)*|z|^(2b), so the
anti content is entirely carried by the real modulus |z|. Guardrail test "can the anti
part be removed by a treatment choice?": YES -- dividing by |z|^sqrt2 leaves z^(1+sqrt2),
purely holomorphic. The anti is a mirror of the modulus, not independent info. ARTEFACT.
Constant |mu| (radial Beltrami) is the symbolic signature of this reducibility.

## Contrast: vortex_N1 (genuine chiral)
vortex_N1 = a*log(z-c) + b*log(zbar-c), a,b COMPLEX independent (ADDITIVE log). mu depends
on (z-c)/(zbar-c), NOT radial. The b*log(zbar-c) term cannot be divided out. Genuine.

## Lessons (Project-A navigation, refined)
1. A fractional phase e^{i*alpha*theta} = (z/zbar)^(alpha/2) is NEVER chiral (always
   modulus x holomorphic). Phase winding alone is not chiral content.
2. Genuine transcendental chirality requires an ADDITIVE log(zbar) with a COMPLEX
   independent coefficient, OR a COMPLEX exponent on zbar -- never a real power.
3. Detector blind spot: reality_check.py labels z^a*zbar^b (a!=b) GENUINE ANTI (f!=conj f),
   missing the "module-trapped" class. Add test: mu radial (k*z/zbar, |k| const) -> reducible.

## Next
- Candidate search must require additive-log or complex-exponent zbar structure, not phase
  winding. AB / anyons / vortex phase-only fields ruled out by lesson 1.
- Optional: add radial-mu test to the Beltrami sieve.
