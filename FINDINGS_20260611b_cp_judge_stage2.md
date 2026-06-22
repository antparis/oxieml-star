# FINDINGS 2026-06-11b -- CP-judge Stage 2 VALIDATED (executed): rephasing certifier

## What
Second executed brick of the CP judge: rephasing certifier. Distinguishes PHYSICAL
phases (survive M -> PL M PR) from REMOVABLE ones -- the Kirsch test in CP form.
File: cp_judge_stage2.py (57 lines).

## Tests (executed, all PASS)
- TEST A rephasing-invariance: CKM polluted with 6 arbitrary rephasing phases ->
  J(polluted)-J(std)=0 exactly. The 6 added phases evaporate, the physical delta
  survives in J. PASS.
- TEST B physical-phase count: N=2->0, N=3->1 (Dirac phase), N=4->3. Matches known
  (N-1)(N-2)/2. PASS.
STAGE 2 VALIDATED.

## Status: [ESTABLISHED] (executed + matches known results)
On GENERAL mixing matrices, the certifier correctly separates forced from removable
phases. Two CP-judge bricks now calibrated (Stage 1 invariants + Stage 2 rephasing).

## CRITICAL for next step
NAIVE diagonal rephasing is correct here but WRONG for Delta(54) (type-I discrete
group): it would wrongly declare the omega=e^(2pi i/3) Clebsch-Gordan phases
removable. Stage 3 MUST use the generalized-CP module (class-inverting automorphism
+ twisted Frobenius-Schur), not this Stage 2 tool. Do not apply Stage 2 to Delta(54).

## Pointer
Follows FINDINGS_20260611_cp_judge_stage1.md. CP/natively-complex front.
