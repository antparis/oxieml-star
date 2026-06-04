# SUPERSEDED 2026-06-04 -- see FINDINGS_20260604_aharonov_bohm.md
# The chirality claim below is WRONG. z^(m+a/2)*zbar^(-a/2) with REAL exponents
# factorizes as z^(a-b)*|z|^(2b) = holomorphic x real-modulus (MODULE-TRAPPED):
# the anti part is removable by dividing out |z|, so it is NOT independent/chiral.
# Also: the "PySR structural limit" below misread the run -- only route A (MSE 0.09)
# was read; route B fit the target at MSE 3.6e-19 with NO log(zbar), proving the
# target has no additive anti structure to recover. Kept for trace; conclusion void.

# FINDINGS 2026-06-03 -- Aharonov-Bohm wavefunction: transcendental chiral anti-holo [DERIVATION]

## Status
[DERIVATION] Wirtinger judge confirmed on Anthony's machine (exact d/dzbar).
First POSITIVE chirality candidate of the whole search. Not yet [ESTABLISHED]:
PySR must still RECOVER the form from data + judge certify it (next step).

## The object (natively-complex quantum wavefunction)
Aharonov-Bohm flux alpha in a magnetic field, lowest Landau level, symmetric gauge:
  psi(z,zbar) = z^(m + alpha/2) * zbar^(-alpha/2) * exp(-z*zbar/(4 lB^2))
With alpha = magnetic flux / flux quantum (gauge-invariant), m integer.

## Why this escapes the frozen-real-field wall
- NATIVELY COMPLEX: a wavefunction (amplitude AND phase), not a packaging of real fields.
- The anti-holo content is a non-integer (irrational) power zbar^(-alpha/2), forced by
  the physical flux alpha, NOT a mirror of the holo part (z-power = m+alpha/2 carries m,
  zbar-power = -alpha/2 does not => independent => NOT mirror-locked).

## Verified on Anthony's machine (exact Wirtinger, alpha=sqrt(2), m=1)
  dpsi/dzbar = z^(sqrt2/2+1) * zbar^(-1-sqrt2/2) * (-z*zbar - sqrt2/2) * exp(-z*zbar)
  => anti-holomorphic, TRANSCENDENTAL (irrational power of zbar). Confirmed != 0.

## Double encadrement (verified)
- alpha -> 0 (no flux): dpsi/dzbar = -z*psi only (Gaussian/mirror), transcendental anti GONE.
- alpha integer: angular factor (z/zbar)^(alpha/2) single-valued => gauge-removable (Byers-Yang).
- alpha irrational (e.g. sqrt2): multivalued, NON-removable by any single-valued gauge e^{i chi}.
  => chirality is physically forced AND gauge-non-reducible exactly when alpha is non-integer.

## Key reframing (honest)
The chirality is NOT an additive holo+anti split (a g(z) + b gbar(zbar)); it is a
MULTIPLICATIVE non-integer power zbar^(-alpha/2). In magnetic/flux systems, non-reducible
chirality lives in multivalued powers, not additive decompositions. This is the form the
physics gives -- accepted as-is, not forced into the additive mould.

## Next (to reach [ESTABLISHED])
- Build a generator: sample psi on a grid, fixing a BRANCH for the multivalued zbar^(-alpha/2)
  (principal branch, cut on negative real axis). Handle multivaluedness carefully.
- Run PySR (add non-integer powers / the eml* toolbox); see if it RECOVERS the transcendental
  anti form. Then judge-certify.
- Controls: alpha=0 (must come out holomorphic), alpha integer (gauge-trivial), shuffle (reject).

## Generator built + sandbox-validated (2026-06-03); PySR run DEFERRED with a strategy
aharonov_bohm_gen.py written and validated in sandbox:
  - psi_AB with branch fixed (polar, theta in (-pi,pi]; origin + negative-real-axis cut masked).
  - Numeric d/dzbar matches the analytic formula to 7 decimals at test points.
  - 4 datasets generated on machine: ab_candidate.csv (alpha=sqrt2), ab_alpha0.csv,
    ab_integer.csv (alpha=2), ab_shuffled.csv. ~4790 points each.

## Why PySR run is DEFERRED (honest risk identified)
A quick numeric Wirtinger ratio test on the scattered grid did NOT discriminate the
four datasets (|mu| ~2.6/2.3/2.1, shuffled ~1.0 -- the shuffled came out LOWEST,
showing the finite-difference test is too crude/noisy to measure chirality here).
This does NOT condemn the target (the SymPy judge sees the transcendental term
exactly on the FORMULA), but it flags a real risk: the transcendental anti term
zbar^(-alpha/2) is masked by the dominant real Gaussian background exp(-|z|^2/4).
PySR might fit the Gaussian and miss the small transcendental term.

## STRATEGY for the cold reprise (the key idea)
Divide OUT the known Gaussian background BEFORE PySR:
  psi / exp(-|z|^2/4)  =  z^(m+alpha/2) * zbar^(-alpha/2)   [pure chiral structure]
Then PySR targets the clean power structure with NO masking background. Steps:
  1. Add an option to aharonov_bohm_gen.py to emit the de-Gaussianed target
     (target = psi * exp(+|z|^2/4)), giving pure z^(m+alpha/2) zbar^(-alpha/2).
  2. Run PySR on the de-Gaussianed candidate (toolbox already has log(conj) via emlstar,
     so zbar^p = exp(p log(zbar)) is reachable). One dataset first, not all four.
  3. Judge-certify the recovered form (expect d/dzbar != 0 with the 1/zbar term).
  4. Controls: alpha=0 de-Gaussianed -> pure z^m (holomorphic, judge says HOLO);
     alpha=2 -> (z/zbar)^1 structure (gauge-trivial); shuffle -> reject (high MSE).
This is the clean path from [DERIVATION] to [ESTABLISHED]. Do it cold, not at session end.

## PySR run 1 (2026-06-04, de-Gaussianed candidate, maxsize=20): FAILED but DIAGNOSTIC
detect_real_data.py ab_dg_candidate.csv --niter 60, population=50, maxsize=20.
Result: MSE = 0.0928 (>> 1e-3 threshold) => INVALID per guardrail, despite the
PySR marker saying 'anti/emlstar'. Marker is NEVER the verdict; MSE invalidates it.

KEY DIAGNOSTIC (the failure is informative, not a wall):
The Hall of Fame final entries contain the constants 0.7071067812... (= sqrt2/2 = alpha/2)
and 2.414213562... (= 1+sqrt2 = 1+alpha). PySR FOUND the right irrational exponents but
could NOT assemble them into a low-MSE form. => the transcendental structure
exp((m+alpha/2)log z) * exp(-(alpha/2) log conj(z)) IS reachable, but maxsize=20 is too
tight to build the full form. This is a BUDGET artefact (cf. Kirsch borderline lesson),
NOT an impossibility.

## Next: rerun with bigger budget
maxsize 35-40, population 100-200, same de-Gaussianed candidate. Test whether the
budget was the limiter. If MSE drops < 1e-3 AND judge certifies emlstar/anti -> [ESTABLISHED].

## PySR run 1 (2026-06-04, de-Gaussianed candidate, maxsize=20): FAILED but DIAGNOSTIC
detect_real_data.py ab_dg_candidate.csv --niter 60, population=50, maxsize=20.
Result: MSE = 0.0928 (>> 1e-3 threshold) => INVALID per guardrail, despite the
PySR marker saying 'anti/emlstar'. Marker is NEVER the verdict; MSE invalidates it.

KEY DIAGNOSTIC (the failure is informative, not a wall):
The Hall of Fame final entries contain the constants 0.7071067812... (= sqrt2/2 = alpha/2)
and 2.414213562... (= 1+sqrt2 = 1+alpha). PySR FOUND the right irrational exponents but
could NOT assemble them into a low-MSE form. => the transcendental structure
exp((m+alpha/2)log z) * exp(-(alpha/2) log conj(z)) IS reachable, but maxsize=20 is too
tight to build the full form. This is a BUDGET artefact (cf. Kirsch borderline lesson),
NOT an impossibility.

## Next: rerun with bigger budget
maxsize 35-40, population 100-200, same de-Gaussianed candidate. Test whether the
budget was the limiter. If MSE drops < 1e-3 AND judge certifies emlstar/anti -> [ESTABLISHED].

## PySR run 2 (2026-06-04, de-Gaussianed, BIG budget maxsize=40 pop=150 niter=100): FAILED
Same plateau as small budget: best MSE ~0.0906 (>> 1e-3) => INVALID. The bigger
budget did NOT help; it produced bloated overfit equations (complexity 32-38,
nested log/my_conj/eml/emlstar) without lowering MSE. Two concordant runs (small
and big budget, same ~0.09 plateau) => this is a STRUCTURAL limit, not a budget
artefact.

DIAGNOSIS (a real tool limitation, cleanly identified):
PySR cannot practically RECOVER the irrational power z^(m+sqrt2/2) zbar^(-sqrt2/2)
from data with this toolbox, even though the SymPy judge sees the transcendental
structure exactly when GIVEN the formula. The irrational zbar power is reachable
in principle (exp(p log conj z)) but PySR does not assemble it at low MSE.

CONSEQUENCE: Aharonov-Bohm stays [DERIVATION] (mathematically chiral transcendental,
judge-confirmed on the formula) but CANNOT be promoted to [ESTABLISHED] via the PySR
route. The blocker is the numeric detector's inability to rediscover irrational
exponents, NOT the physics. This is a genuine, traced limit of the PySR stage.

HOLO/ANTI BALANCE NOTE: the judge (symbolic) handles transcendental anti correctly;
the PySR translator does NOT recover it from scattered data. Tool is reliable as a
CERTIFIER (judge on a given formula) but limited as a DISCOVERER (PySR from data) for
irrational-power anti-holomorphy.
