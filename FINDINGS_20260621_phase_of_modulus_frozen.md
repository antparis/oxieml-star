# FINDINGS 2026-06-21 -- Phase-of-modulus definitional question: FROZEN (deliberate), with facts established

## Status
[ESTABLISHED] facts (executed on Anthony's machine via the side comparator).
[DECISION] the definitional question is deliberately FROZEN: keep the current judge
(phase-of-modulus -> anti); do NOT adopt Kimi's structural redefinition yet.
Rationale: no current physical target depends on the choice; a distinction earns its
place only when a downstream claim depends on which side of it one falls.

## Origin
Kimi (external AI) was briefed on the open question: is a phase-of-modulus factor
e^{i*g(|z|^2)} (g real) module-trapped (reducible) or genuine anti? It produced a
[DERIVATION] argument (settle_phase_of_modulus.md). We AUDITED it by replaying every
symbolic claim on Anthony's machine -- did NOT trust its self-reported "symbolic
verification".

## What the execution ESTABLISHED (replayed, not trusted)
1. KIMI MADE A REAL ERROR. Kimi claimed (z/|z|)^alpha is "genuine ANTI" (reconstructed
   h=z^alpha multivalued). Execution shows L[(z/|z|)^alpha] = -alpha/2, which is REAL
   and constant -> the judge classifies it MODULE-trapped. Kimi's "verification" of
   this row was wrong. THIS VINDICATES THE RULE: an LLM does not execute code; replay
   everything.
2. NO TENSION WITH HECKE. Because (z/|z|)^alpha is module (judge agrees with the sealed
   2026-06-19 Hecke result, hash ee7000cf), the feared contradiction with history does
   NOT exist. The sealed Hecke wall stands.
3. THE BLIND SPOT IS REAL, BUT NARROW. On the genuine phase-of-modulus z*e^{i|z|^2}:
   L = i*z*zbar (purely imaginary) -> judge says ANTI; R(f)/f = 1 (zbar-independent)
   -> oracle says MODULE. They DISAGREE. Confirmed by execution.
4. KIMI'S DEFINITION IS SAFE BUT CHANGES ONLY COMPLEX PHASE-OF-MODULUS. The side
   comparator (current judge vs Kimi's structural def with REAL/PHASE sub-labels) shows
   EXACTLY TWO cases change:
     z*e^{i|z|^2}            : current ANTI -> Kimi MODULE(PHASE)
     z*e^{(-1/4+i)|z|^2}     : current ANTI -> Kimi MODULE(PHASE)   (LLL complex)
   Everything else is IDENTICAL, crucially:
     vortex_N1 (reference chiral) -> ANTI in BOTH (guard holds)
     Maass shadow k=1/2          -> ANTI in BOTH (yesterday's result does NOT flip)
     Hecke z/zbar, z^2*zbar      -> MODULE in both
     zbar, z+0.3*zbar            -> ANTI in both

## Kimi's argument (recorded for the day a real target forces the choice)
[DERIVATION, Kimi] e^{i*g(|z|^2)} is pure gauge: A = grad g(|z|^2) has zero curl
(curl computed = 0), hence zero magnetic flux, single-valued, removable by a local U(1)
transformation. R(f)/f = 1 identical to the real Gaussian z*e^{-|z|^2/4}, so angular
momentum is unchanged. Physically the radial phase is inert (Berry phase around a
contractible loop = 0). => phase-of-modulus is structurally reducible (MODULE).
Proposed criterion (Kimi Theorem 2): module-trapped iff R(L)=0 AND reconstructed
h(z)=f/M is holomorphic & regular; sub-label REAL_MODULE (L real) vs PHASE_MODULE
(L imaginary). This is mathematically sound (verified: it keeps vortex_N1 and the
shadow as anti).

## DECISION: FROZEN (why not adopt now)
- No current target is a complex phase-of-modulus. Adopting now = abstract refinement
  with a real cost (judge complexity, regression risk, two extra sub-labels) for a
  hypothetical benefit.
- The choice has a real consequence ONLY for Aharonov-Bohm / LLL-type phases. When such
  a PHYSICAL target is actually on the table, decide THEN, with the concrete stake in
  view. Until then: keep the current judge unchanged (phase -> anti), frozen consciously.
- This is the engagement discipline both ways: do not reopen a sealed question without
  new info; do not settle a frozen one without necessity.

## Files
settle_phase_of_modulus.md (Kimi's argument, audited -- contains one wrong row on
(z/|z|)^alpha, otherwise sound), this FINDINGS. Judge code UNCHANGED.

## What remains for the rest of the Kimi deliverable (not yet audited)
hardened_judge.py (Task A), new_physical_targets_proposal.md (Task C),
task_d_proposals.md (Task D), analysis.md, the HTML/PDF report. To be audited next.
