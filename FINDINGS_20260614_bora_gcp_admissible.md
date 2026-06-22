# FINDINGS 2026-06-14 -- Bora Delta(54) field content ADMITS a physical generalized CP (certified GAP), despite the group being type-I

## What this is
The decisive restricted test of the CP Stage-3 program. The abstract group Delta(54) is
type-I (no global class-inverting involution -> CP geometrically forced). BUT a concrete
model using only a SUBSET of irreps can escape. This tests whether the SPECIFIC Bora et al.
field content escapes. File: GAP script /tmp/bora_bd.g.

## Bora field content (read from PRIMARY sources, not from search summary)
From arXiv:2311.11611 Table 2 (and consistent across 2305.08963, 2402.18906, 2407.05753,
2605.11124): the Delta(54) irreps actually used are
- 2 singlets (1_1, 1_2)  [GAP idx 1,2]
- exactly 1 doublet (2_1) [GAP idx 3]   <- they use ONLY ONE of the four doublets
- all 4 triplets          [GAP idx 7,8,9,10]
Doublets 2_2, 2_3, 2_4 (GAP idx 4,5,6) are NOT used. Bora themselves note "the
representations of Delta(54) are real, guaranteeing the construction of the Lagrangian".

## Test executed on Anthony's machine (GAP 4.12.1)
Restricted to Bora content {idx 1,2,3,7,8,9,10}:
- An involution in Aut(Delta54) exists that conjugates ALL these irreps to their complex
  conjugates (true for each of the 4 possible doublet choices).
- Twisted Frobenius-Schur indicator eps_u = +1 for EVERY Bora irrep (computed on a genuine
  involution -> valid; earlier eps=1/3 bug came from a non-involution and is fixed).
- => Bickerstaff-Damhus criterion SATISFIED -> a PHYSICAL generalized CP transformation
  EXISTS for the Bora field content.

## Status: [ESTABLISHED-userrun] for the group-theory fact; NUANCED on novelty
ESTABLISHED (executed + correct criterion + calibrated on Delta(27) known case):
The Bora Delta(54) field content admits a physical generalized CP (gCP) transformation,
even though the full group is type-I. Therefore the CP violation in the Bora models is
NOT forced by the Delta(54) group structure; their CP phases (delta_CP, J) are put in by
hand via complex flavon VEVs, not symmetry-protected. They COULD impose gCP (their irreps
allow it), which would constrain the phases and make the model predictive -- they did not.

NOVELTY (honest): the CRITERION is known (Nilles-Ratz-Trautner-Vaudrevange 1808.07060
"<=2 doublets -> gCP admissible"; Ding-King 1510.03188 "subset of irreps"). What is NEW
is APPLYING it to the specific Bora models, which no one (Bora included) has done. This is
"open in execution, closed in method" -- a modest but real, publishable observation, NOT a
new theoretical method or a fundamental discovery. Per Anthony's rule: applying a known
method to an unanalyzed case = a real contribution, but it must not be oversold as a
method-level discovery.

## Limit (do NOT overclaim)
"A gCP exists for the representation content" is a group/representation-theory statement.
It does NOT yet prove that imposing this gCP yields a phenomenologically viable model
(survival under higher-dim operators, and the constrained predictions for delta_CP /
Majorana phases / m_bb, are NOT computed). Existence of the transformation =/= viability.

## NEXT (optional, cold session)
Construct the explicit gCP matrix X_r for the Bora content, impose it, and derive the
constrained predictions (delta_CP, Majorana phases, m_bb). That would convert a
non-predictive fit into a predictive model -- the genuinely valuable follow-up.
