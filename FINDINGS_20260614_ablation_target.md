# FINDINGS 2026-06-14 -- [DERIVATION/TARGET] Non-holomorphy in Qu-Ding models: "empty-slot forced" YES, "physically necessary" NEVER TESTED. The g1=0 ablation is our virgin ground.

## What this is
Result of an EXHAUSTIVE reading of both Qu-Ding papers (2406.02527 founding, 2506.19822 odd-weight T' model), full text, all sections/appendices. Goal: is non-holomorphy ever IRREPLACEABLE?

## Two senses of "irreplaceable" -- the key distinction [DERIVATION, primary source]
1. EMPTY-SLOT sense (TRUE, established): at weight 1 in rep 2-hat'' (eq. D.11 of 2506.19822 the holomorphic combination VANISHES identically) and at ALL weights <= 0, NO holomorphic modular form exists. Those slots can ONLY be filled by non-holomorphic polyharmonic Maass forms. So within a fixed field content, non-holo is mathematically forced in several places (weight-1 2-hat'' doublet; weight-0 triplet Y3^(0) in M_e; negative-weight forms in quark sector). Anthony's intuition "non-holo is essential somewhere" is CORRECT at this level.
2. PHYSICALLY-NECESSARY sense (NEVER demonstrated): no paper ever sets a non-holo coupling to zero, none compares to a holomorphic-only model. The non-holo term always sits ALONGSIDE a holomorphic term with its own free coupling, and its ANTI-holomorphic part is the xi_k-image (shadow) of a holomorphic form -- so the anti part often carries NO information independent of the holomorphic sector.

## The opening (our virgin ground) [DERIVATION]
In the 2506.19822 lepton model (eq. 4.2), the neutrino Dirac term is
  g1 (N^c L H Y2-hat''^(1))_1  +  g2 (N^c L H Y2-hat^(1))_1
where Y2-hat'' is NON-holomorphic (weight-1, rep 2-hat'', no holomorphic counterpart) and Y2-hat is holomorphic, each with its own free coupling. AT EVERY BEST-FIT POINT the non-holo coupling g1 DOMINATES: |g2/g1| = 0.2946 (NO no-gCP), 0.081 (IO no-gCP), 0.149 (NO gCP), 0.081 (IO gCP). So g1 carries the LEADING contribution to M_D.
=> Setting g1 = 0 should gut M_D. BUT the authors NEVER do this. The g1=0 ablation (and a refit) is NOWHERE in the literature. This is the first test where we reproduce NO ONE.

## Status
- "Non-holo fills empty weight/rep slots": [ESTABLISHED, primary source, eq. D.11 + weight<=0 fact].
- "Non-holo is physically necessary (data forces it)": [OPEN, never tested by anyone].
- Foundational principle (Laplacian condition Delta_k Y=0) origin: authors admit "obscure".
- Anti-holo part slaved to holomorphic shadow via xi_k (Anthony's own operator): the genuinely
  NEW content at weight 1 is the mock/holomorphic part (log-coefficients), NOT the anti part.

## NEXT -- THE SIMULATION (our test, nobody has done it)
Build the 2506.19822 lepton model numerically. TWO levels:
  (A) STRUCTURAL [HEURISTIC]: at fixed best-fit tau, set g1=0, recompute the seesaw m_nu =
      M_D^T M_N^{-1} M_D; check if a neutrino mass / mixing collapses (rank drop). Fast.
  (B) FULL ABLATION [the real test]: set g1=0 and RE-MINIMIZE chi^2 over all remaining params
      (tau, g2, alpha,beta,gamma, scales) vs NuFIT. If chi^2 stays bad -> non-holo is NECESSARY
      (forced by data) -> genuine result. If a holomorphic-only refit recovers the fit -> non-holo
      is decorative here.
CRITICAL build step: code the level-3 Maass forms (Y2-hat''^(1) eq.3.25, a0~0.1132; Y3^(0,2,4))
and CALIBRATE against the paper's published values BEFORE trusting any ablation output.
Arbiter remains: executed on Anthony's machine. Sandbox run by Claude = debug only.
