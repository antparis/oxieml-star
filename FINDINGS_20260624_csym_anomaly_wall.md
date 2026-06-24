# FINDINGS 2026-06-24 -- [DERIVATION + ESTABLISHED discriminant] c_L != c_R is NOT enough: gravitational anomaly lands on the separable wall; target needs a cross-sector MIX

## M-IV hunt, orthogonal axis on the central-charge symmetry

**Question.** The only live door for ENTANGLED_CHIRAL_ANTI is a non-Hermitian cross
correlator. The orthogonal axis pointed at the parameter every fallen candidate kept
fixed: the symmetry of the two sectors. Io-Huang-Hsieh (arXiv:2602.02649, c=cbar=-2)
fell because its cross-log G_{-+} ~ ln(|x-y|/L) has a MODULE argument -> paired ->
REAL_TRAPPED. So: does breaking c_L != c_R reach the target?

**Reconnaissance (literature).** The physical mechanism for c_L != c_R is the
GRAVITATIONAL ANOMALY: unequal left/right central charges, anomalous divergence
nabla_mu T^{mu nu} ~ (c_L - c_R), vanishing exactly at c_L = c_R (arXiv:2504.19694,
arXiv:2202.00683). It is realized on chiral edges of 2+1D topological phases, integer
(abelian) or non-integer (non-abelian) central charge (arXiv:1707.08048). REMOVABILITY
TRAP: many non-Hermitian c != cbar systems are reducible to a Hermitian one by Naimark
dilation, e.g. c=-4 -> c=2 (arXiv:2211.12525) -> gauge/basis wall, like Hatano-Nelson.

**Discriminant test (check_csym.py, symbolic-exact d = d_z1 d_z2b log f).**
    A separation (z1-z2)(z1b-z2b)   [c=cbar]    d=0                   -> WALL (separable)
    B asym juxtaposed z1^pi*z2b^phi  [cL!=cR]    d=0                   -> WALL (separable)
    C cross-mix log(z1 - z2b)                    d=(z1-z2b)^-2 != 0    -> TARGET
    D cross-mix log(1 + z1*z2b)                  d=(z1*z2b+1)^-2 != 0  -> TARGET
Command: cd ~/Desktop/oxieml-star && python3 check_csym.py
Note: B (= pi*log z1 + phi*log z2b, pi != phi) is ALREADY the wall row z1^pi*z2b^phi
of anchor 20204b2; the asymmetric-juxtaposed case was already certified a wall.

**Verdict.** c_L != c_R ALONE is NOT sufficient. Both physical knobs on sector symmetry
land on walls: c=cbar -> paired (A); c_L != c_R -> asymmetric but JUXTAPOSED -> separable
(B). The gravitational anomaly is ELIMINATED as a direct route. The target requires a
CROSS-SECTOR MIX (C/D): z1 and z2b inside the SAME transcendental argument, i.e. an
EXPLICIT left-right interaction, and Naimark-irreducible (not reducible to Hermitian).

**Status.** Discriminant frontier A/B/C/D = [ESTABLISHED] (symbolic-exact, reproducible,
identical to nonseparable_judge). Physical interpretation (anomaly -> B -> wall) =
[DERIVATION]. Io-Huang-Hsieh reconfirmed as case A = double wall (paired + separable).

**Symmetry ledger update.** chiral cell: still EMPTY. Walls now include both
central-charge knobs (paired AND anomaly-juxtaposed). Refined target criterion for the
next physical hunt: a non-Hermitian / non-equilibrium correlator with an EXPLICIT
left-right coupling that survives in a single transcendental argument (cross-mix),
non-reciprocal and Naimark-irreducible. Candidates to probe next: non-Hermitian L-R
inter-mode tunneling on a chiral edge; cross-branch Keldysh correlator in a NESS.
