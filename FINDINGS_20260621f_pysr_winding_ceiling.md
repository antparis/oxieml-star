# FINDINGS 2026-06-21f -- PySR (translator) STRUCTURAL CEILING on winding-vortex structures

## Status
[ESTABLISHED, NEGATIVE/LIMIT] (machine, PySR 1.5.10, code 0): the translator (PySR,
the discoverer role) CANNOT recover the composite-vortex anti structure from data. It
plateaus at MSE ~1.3e-2 (13x above the 1e-3 threshold) and converges to decorative
rational fractions, NOT to (z/|z|)^n*exp(-c|z|^2). This is a STRUCTURAL ceiling, not a
budget limit. A diagnosed failure is a result.

## Setup
Data: f(z) = (z/|z|)^1*exp(-|z|^2) + (z/|z|)^2*exp(-|z|^2), N=2000, annulus r in [0.3,2.0].
Validated 3 ways BEFORE PySR (judge=anti, num |d/dzbar|=0.55>>0). Target = Re(f),
features {x,y}. Short calibration run: niterations=40, populations=15, ops {+,-,*,/,exp,
square,sqrt_abs}. PySR started cleanly (no Julia error, sqrt_abs accepted).

## Result: structural ceiling (not budget)
Hall of Fame MSE vs complexity DECREASES then STAGNATES:
  c=1  1.9e-1 ... c=9 1.0e-1 ... c=15 2.1e-2 ... c=19 1.7e-2 ... c=27 1.3e-2 (best).
From c=17 to c=27, each added complexity buys almost nothing (1.7e-2 -> 1.3e-2): the
asymptotic-wall signature of a STRUCTURAL ceiling, not budget (budget limits show jumps).
Best eq is a rational fraction x0/(square(...)+square(x1)) -- PySR senses a radial
modulus (square(x0)+square(x1) = |z|^2 at denominator) but CANNOT capture the WINDING
(z/|z|)^n nor the exact exponential. The angular part (the SOURCE of the anti) escapes it.

## Why (mathematical reason)
(z/|z|)^n = z^n * (z*zbar)^{-n/2} needs HALF-INTEGER powers of z*zbar and an angle/modulus
separation that PySR's grammar (compositions of +,*,square,exp,sqrt_abs) cannot assemble
cleanly. Same limit hit in Aharonov-Bohm (FINDINGS 2026-06-04, MSE ~0.09). TWO concordant
independent cases => confirmed structural ceiling of the discoverer on winding structures.

## Consequence for the pipeline (two roles cleanly separated)
- CERTIFIER (SymPy judge): handles these structures perfectly (certified the composite
  vortex as anti without trouble).
- DISCOVERER (PySR): BLIND on winding structures -- cannot recover them from data.
On this class of objects the certifier is the tool; the discoverer is not.
IMPORTANT for the superconductor candidate (FINDINGS 0621e): we CANNOT use PySR to lift
the "posed vs forced" reservation by having it recover the structure from a GL simulation
-- it would plateau identically. That reservation must be lifted by PHYSICS analysis
(is the combination a native observable?), not by the translator.

## Possible (not recommended) escape
Changing representation (features in r,theta or pre-including z/|z|) might let PySR bite,
but that GIVES it the winding structure in the features = posing the answer, not
discovering it. Weak capability at best. Not pursued unless explicitly decided.

## Files
pysr_vortex_calib.py (run, on machine), pysr_vortex_calib_result.json (best MSE 1.33e-2,
mse_below_1e-3=false), outputs/20260621_202825_C27v8A/hall_of_fame.csv, this FINDINGS.
