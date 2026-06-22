# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine] Sequential weak values (the last speculative open thread) are CLOSED: they carry NO irreducible new geometric object. Setup: prepare |psi>, weakly measure A (first) then B (second), post-select <phi|; W_seq = <phi|B A|psi>/<phi|psi>. Certified on Anthony's machine (weak_value_sequential_test.py): (1) order-dependence is REAL -- W(A then B) != W(B then A) when [A,B]!=0 (non-commutativity genuinely matters); (2) BUT W_seq is EXACTLY a sum of 4-state Bargmann terms sum_ij b_j a_i <phi|j><j|i><i|psi>/<phi|psi> (residue 2.08e-14 over 200 cases => no residue); (3) AND each 4-point geometric phase reduces exactly to a sum of triangle (3-state Pancharatnam-Berry) phases (diff 8.88e-16 over 200 cases, triangulation by a diagonal). So the sequential weak value -- even with non-commuting observables and multiple 'moments' between past and future -- is still a weighted sum of KNOWN Pancharatnam-Berry phases. Non-commutativity is real but is fully carried by these known terms; it does NOT produce a new irreducible (non-abelian / higher-order) geometric object. Door CLOSED: capability, not discovery. Do NOT overclaim non-commutativity as 'new geometry'.
## Auditor self-correction (important)
First sandbox run reported match=False in the decomposition [2]. I did NOT treat it as a possible
discovery -- I suspected my own code first (the SPARC guard: a disagreement is a bug until proven
otherwise). It WAS a bug: operator order in the bra-ket chain (B A = sum_ij b_j a_i |j><j|i><i|, the
inner overlap is <j|i> between B-eigenvectors and A-eigenvectors). Fixed -> match=True, residue zero.
Lesson reaffirmed: an unexplained disagreement must be resolved before any claim; claiming novelty on
a bug would be exactly the self-deception we guard against.
## Tests (executed on Anthony's machine, weak_value_sequential_test.py)
 - [1] order dependence: W(A then B) != W(B then A), |[A,B]| ~ 2.4-4.9, order matters True (4 cases). [certified]
 - [2] decomposition: W_direct == sum of 4-state Bargmann terms, residue 2.08e-14 over 200 cases. [certified]
 - [3] 4-point phase == sum of triangle (3-state) phases, diff 8.88e-16 over 200 cases. [certified]
## What this settles
The whole weak-value geometric analysis is now closed on every axis tested: single projector
(cdeee2e5), generic observable (13a7bd4e), and now SEQUENTIAL / non-commuting (this file). In every
case the chirality is built entirely from known Pancharatnam-Berry phases; no irreducible new object
appears. The framework eml/eml*/eml0 is a faithful geometric calculator retrieving known physics.
Genuine contribution = the unified ASSEMBLY, not a new prediction. The non-commutativity result is
itself worth noting: a natural place to hope for 'new geometry' (operator ordering), checked and found
reducible. Do NOT overclaim.
## Status
[ESTABLISHED sandbox->machine] sequential weak value = sum of known Berry phases, no irreducible
residue (2.08e-14), 4-point phase reducible to triangles (8.88e-16), non-commutativity real but
carried by known terms. Reconnects: projector thumb=Pancharatnam (cdeee2e5); generic observable
closed (13a7bd4e); weak value candidate (232398dd). Do NOT overclaim non-commutativity as new geometry.
Files: weak_value_sequential_test.py. Arbiter = Anthony's machine (done).
