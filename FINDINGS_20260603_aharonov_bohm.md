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
