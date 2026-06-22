# FINDINGS 2026-06-12 -- CP-judge Stage 2 EXTENDED to Majorana (executed, validated)
## What changed since FINDINGS_20260611b
The 20260611b note covered Stage 2 for the DIRAC case only (J + count 0/1/3). That
validation was INSUFFICIENT for the real target: Delta(54) neutrinos are Majorana,
and J is BLIND to Majorana phases. Stage 2 now adds a Majorana layer and the crossing
test that 20260611b lacked. File cp_judge_stage2.py now has tests A-E (101 lines).
## Tests executed on Anthony's machine (all PASS)
- A: Dirac J rephasing-invariant (J polluted - J std = 0). PASS.
- B: Dirac physical-phase count 0/1/3 for N=2/3/4. PASS.
- C: Majorana I_ij rephasing-invariant under M->P M P (symmetric). PASS.
- D (THE crossing test): on m_nu = U diag(m) U^T with Majorana phases,
    J(delta=0, maj!=0) = 0.00e+00  -> J BLIND to Majorana phases
    I12               = -6.42e-08  -> I_ij SEES them (threshold 1e-10, scale-adapted)
    I12(all phases 0) = 0.00e+00   -> vanishes when nothing is on
    J(delta!=0,maj=0) = 2.40e-02   -> control: J still SEES Dirac (not trivially zero)
  PASS. This proves the two layers carry DIFFERENT information.
- E: Majorana physical-phase count 1/3/6 for N=2/3/4 = N(N-1)/2. PASS.
## Honest scope / caveats
- The 1e-10 threshold in D is scale-adapted to m_i ~ 0.01-0.05; re-check if masses change.
- Iij uses two conjugations; for symmetric M this is Im(m_ii m_jj conj(m_ij)^2), phase-sensitive.
- This validates Dirac+Majorana on GENERAL/PMNS matrices ONLY. It does NOT cover Delta(54):
  naive diagonal rephasing is WRONG for type-I groups. Stage 3 (gCP / class-inverting
  automorphism + twisted Frobenius-Schur) is REQUIRED before any Delta(54)/Bora claim.
## Provenance note (method worked)
Majorana idea: Milo (but shipped a modulus-blind Iij bug). Crossing-test idea: other
Claude window (but shipped a mis-calibrated 1e-6 threshold -> would false-FAIL here).
Fix + control J-sees-Dirac + execution: Anthony's machine. No single source was reliable
alone; the arbiter was the run. 
## Status: [ESTABLISHED-userrun] Stage 2 Dirac+Majorana. Delta(54) OUT OF SCOPE until Stage 3.
