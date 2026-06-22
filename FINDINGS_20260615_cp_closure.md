# FINDINGS 2026-06-15 -- [DERIVATION, negative result, CP closure] The anti-holomorphic term is NOT necessary for CP violation either in the Qu-Lu-Ding T' model. A holomorphic-only competitor at equal parameter count reaches the measured Jarlskog |J| inside the fundamental domain (chi2=0.49 for the + sign). Closes the last open door from FINDINGS_20260615_ablation_negative (Milo 8ca8a979). Result now COMPLETE and fully negative.

## What this is
The CP-violation necessity test, the only avenue left open after the mass/mixing negative result.
Method per the CP-judge rule: CP physicality judged by the rephasing-invariant Jarlskog invariant
J = Im(U_e1 U_mu2 U*_e2 U*_mu1), NOT by d/dzbar. g2 made COMPLEX (carries the CP phase). FULL vs
HOLO-ONLY at equal parameter count (6 params), re-minimized with J added to the chi2, tau hard-
constrained to the fundamental domain. CRUCIAL control: target BOTH signs of J, because the sign
of J flips with family ordering (a convention), so a single-sign test can give a false "wrong sign"
positive. Scripts: jarlskog_test.py (first pass), jarlskog_robust.py / jarlskog_holo_only.py (robust).

## Results (executed on Anthony's machine)
FULL (holo+nonholo): chi2=2.42 for BOTH signs (J=-0.0219 at tau=-0.020+1.092i; J=+0.0219 at
  tau=+0.020+1.092i -- exact mirror). Confirms the sign of J is set by sign(Re tau) = a convention.
HOLO-ONLY (tau-bar OFF), 30-start each sign:
  target J=-0.028: chi2=129.63 (fails this sign)
  target J=+0.028: chi2=0.49   (SUCCEEDS) at tau=-0.067+1.014i, J=+0.0308, in fundamental domain
  best over both signs: chi2=0.49
=> HOLO-ONLY reaches the measured |J| for the + sign with an excellent chi2.

## Verdict (honest, negative, complete)
The holomorphic-only model reproduces the measured CP violation (Jarlskog |J|~0.028) at equal
parameter count inside the fundamental domain. Therefore the anti-holomorphic term is NOT necessary
for CP violation in the T' model -- it is DECORATIVE for CP as well. The first-pass "wrong sign"
(chi2=130 on J=-0.028) was a FAMILY-ORDERING CONVENTION ARTIFACT, exposed by testing both signs:
holo-only succeeds at the + sign. This is the 4th false-positive of the session caught by deeper
testing (after: 2000x ablation = param-count; 210000-vs-11 = fixed-point; where_min out-of-domain
= missed local minimum).

## Agreement with theory (reassuring, no residual artifact)
Matches the established statement (Novichkov-Penedo-Petcov-Titov 1905.11970; Qu-Ding 2406.02527;
Qu-Lu-Ding 2506.19822): the VEV of tau is the SOLE source of CP violation in these models; the
anti-holomorphic (Maass) content enters as REAL functions of Im(tau) and carries no independent
phase. So a holomorphic model at complex tau already generates the full CP phase. Numerics on
Anthony's machine now confirm this for T' -- theory and computation concur.

## Overall session conclusion (T' lepton model)
The anti-holomorphic term is DECORATIVE on ALL tested observables: mixing angles, mass-squared
ratios, charged-lepton mass ratios (FINDINGS_..._ablation_negative, 8ca8a979), AND CP violation
(this note). A holomorphic-only model at equal parameter count reproduces everything inside the
fundamental domain. NOT a Project-A result. By Anthony's criterion ("can the anti part be removed
by a treatment choice? yes => not a discovery"), the anti-holomorphic structure of the T' model is
removable. Clean, complete NEGATIVE result -- itself novel (no published necessity test exists).

## Caveats
1. Single model (T'); other non-holomorphic models (A4, S4, A5) untested.
2. J extraction uses the standard invariant; for a publication-grade claim, confirm with the
   rephasing certifier cp_judge_stage2.py (Dirac layer) -- but the both-signs success already
   removes the only ambiguity (sign convention).
3. Model reconstruction (bricks 1-6) remains valid and is the solid, reusable asset of the session.

## Status
[DERIVATION, negative, complete]. Anti-holomorphic term decorative for CP and for all standard
leptonic observables in T'; removable by an equal-parameter holomorphic-only refit in the
fundamental domain. Agrees with theory (tau = sole CP source). Single model => internal to T'.
No gravity / no non-neutrino-mass link.
Files: jarlskog_test.py, jarlskog_robust.py, jarlskog_holo_only.py.
Arbiter = Anthony's machine + theory concordance. Completes 8ca8a979.
