# FINDINGS 2026-07-11 -- #052 reference-needle heterodyne: the mirror blindness of #051 is LIFTED; the breaking measures the ASYMMETRY of the weighted winding measure

## What
The one proven hard limit of the inverse spectroscopy (#051) -- exact
mirror blindness of modulus-only relief data -- is lifted by injecting a
KNOWN reference needle r*e^{i(nu_r u + phi_r)} and demodulating the beat.

## Law (machine-faced at r = 0.5, 2, 10)
With the centered field s(u) = mu_hat(u) e^{-i(a+b)u/2} (mirror acts as
s -> conj(s)), the choir-minus-mirror difference obeys
  D(u) = -2 Im s(u) * sin(((a+b)/2 - nu_r) u - phi_r) + O(|mu|^2 / r).
ASYMMETRY LAW: the breaking ceiling is ASYM = max_u 2|Im s(u)| -- the
heterodyne reveals exactly the asymmetry of the weighted winding measure.
A quadrature pair (phi_r = 0, pi/2) saturates it: sat/ASYM = 0.987-0.991
on all 8 weight families (incl. size-disparate and size-speed-correlated,
per the size ledger).

## Results (Anthony's machine, 2026-07-11, seed 7, verdict 24/24)
- Passive blindness reconfirmed: |choir - mirror| < 1.6e-15 (8/8).
- Heterodyne breaking: equal 3.29e-2, ballast 5.05e-2 (strongest:
  most asymmetric measure), clock 2.93e-5 (symmetric effective measure
  = its own mirror; residue is finite-sampling only and obeys the #049
  grid clause: midpoint/endpoint ratio = N -- 67.4 / 266.6 / 1063.3 at
  N = 64 / 256 / 1024 -- accidental cross-reconfirmation of the theorem).
- Demodulation law: |D - law| under the O(|mu|^2/2r) bound at all r.
- QUADRATURE RECOVERY: full complex mu_hat to 4.999e-2 vs bound 5.000e-2
  at r = 10; TRUE choir identified vs mirror (separation 1.4e0):
  the mirror ambiguity is DISSOLVED, not voted.
- Controls: reciprocal REFUSED (flat relief, contrast 0 < 1e-4 floor);
  shuffle tracks its own ASYM; noise discrimination 20/20 at 1% and 5%.

## Judge (SymPy, exact)
J1 mirror-conjugation identity: residue 0. J2 symmetric measure is its
own mirror (Im s == 0 identically): residue 0. CERTIFIED.

## Provenance (three-implementation convergence)
Mother-instance seed (2026-07-10 sandbox), sister-instance independent
harness (spec-hardened, lost in transfer), mother-instance rebuild from
spec -- all three converge to the last digit on Anthony's machine; the
same control-definition trap (reciprocal formal reflection) was hit and
fixed INDEPENDENTLY by both implementations.

## Status
[ESTABLISHED machine + judge]. Says nothing about physics; the
instrument upgrade is mathematical. Opens: closed-form breaking for the
canonical measures; staircase tears (#053); hierarchical choirs C4
[CONJECTURE] (Sornette route vs hierarchy-free route in one object).

## Traces
kernel_heterodyne_test.py -- judge_heterodyne_052.py --
heterodyne_machine_run.log -- this file.
