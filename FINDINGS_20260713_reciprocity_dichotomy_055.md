# FINDINGS 2026-07-13 -- #055 the reciprocity dichotomy: exchange-Hermiticity
# is NOT reciprocity (external counter-example confirmed machine+judge)

## Origin
Adversarial audit by an external AI (GPT-5.6 "Fable 5"), tasked with attacking
the central theorem of the published one-way paper (DOI 10.5281/zenodo.21317960).
Its counter-example class: reciprocal-DISSIPATIVE kernels. Constructions C0
(damped reciprocal oscillator ladder) and C1 (paired doublets reproducing the
(m+a)^-2 double-pole structure, A_m symmetric, Hermitian part negative).

## Result (Anthony's machine, judge_reciprocity_control.py, SymPy exact)
Two independent invariants on two-point kernels:
  Delta = K - M(S(K))   (exchange-Hermiticity, the paper's criterion)
  R     = K - S(K)      (plain transpose/Lorentz reciprocity, no conjugation)
Table (truncation N=3, generic symbols):
  decoy  (single-direction, real coeff):  Delta==0,  R!=0
  C0     (reciprocal-dissipative):        Delta!=0,  R==0   <- FALSE POSITIVE for old theorem
  C1     (reciprocal-dissipative Lerch):  Delta!=0,  R==0   <- FALSE POSITIVE for old theorem
  one-way (the paper's kernel):           Delta!=0,  R!=0   <- correctly flagged by BOTH
C1 structural checks all pass: A_m^T = A_m exact; Hermitian-part eigenvalues
-kappa/2 +/- g; Fable 5's closed-form Green's function verified EXACTLY
(symbolic difference 0).

## Interpretation [DERIVATION]
Delta==0  <=>  kernel Hermiticity  <=>  real modal coefficients (a detailed-
balance / time-reversal axis). R==0 <=> transpose symmetry (physical Lorentz
reciprocity). These are INDEPENDENT axes (all three off-diagonal quadrants
realized). The published theorem's biconditional conflated them; dissipation
(complex coefficients) separates them. All published NUMERICAL conclusions
stand (the one-way kernel violates both); the THEOREM STATEMENT must be
repaired with R as the master reciprocity invariant and Delta demoted to a
structural (Hermiticity) property. v3 is sealed; repair goes in the next
linked deposit (errata note), consistent with the hedged wording of p.16.

## Open flag [DERIVATION -- Q3 pending]
C1 = the paper's Lerch kernel on X PLUS the same on Y: each sector carries a
rotating cut-jump phase. The phase-law witness therefore fires PER SECTOR on
reciprocal-dissipative systems; one-wayness requires the COMPARATIVE witness
(phase rotation AND absence of the partner sector / directional asymmetry).
To be machine-confirmed; question posed to the external auditor.

## Traces
judge_reciprocity_control.py -- reciprocity_control_run.log (local) -- this file.
Credit: counter-example class proposed by the external auditor; verified,
translated to kernel language, and certified by us.
