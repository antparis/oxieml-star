# FINDINGS 2026-06-23 — KFP nu=2/3 edge is a (half-chiral / multiplicative) WALL

**Status:** [DERIVATION] from primary source + judge; both pasted "candidate" forms refuted.

## Context

Hunt for (b)+(c): a forced, non-factorizable, cross-chiral anti carried by a measurable complex
amplitude. Candidate proposed by web search: disordered nu=2/3 fractional quantum Hall edge
(Kane-Fisher-Polchinski, PRL 72, 4129 (1994)). Two pasted notes proposed closed forms; both were
treated as candidates to TEST, not accepted.

## Primary source (verified)

KFP action (reproduced from KFP PRL 1994): two modes phi1 (right-mover -> holomorphic z),
phi2 (left-mover/counter-propagating -> anti-holomorphic zbar); disorder/electron vertex operator
xi(x) e^{i(phi1+3phi2)}. Vertex correlator = exp(sum coeff * <phi phi>), <phi phi> ~ -log:
  G_electron ~ z^{-1} * zbar^{-3}   (charge z^-1  x  neutral zbar^-3) = MULTIPLICATIVE product.

## Judge verdicts (this analysis; pure SymPy)

KFP vertex   z^-1 zbar^-3                    : d_z d_zbar log = 0  -> factorizes -> WALL (MODULE)
KFP note#2   z^-1 zbar^-3 (A + B ln zbar)    : d_z d_zbar log = 0  -> factorizes -> SEPARABLE half-chiral WALL
KFP note#1   z^-2 ln z (holomorphic Jordan)  : d/dzbar = 0         -> HOL = eml WALL (same as TMG/LCFT)
TARGET cross z^-1 zbar^-1 (1+ln z1+ln zbar2) : d_z d_zbar log != 0 -> ENTANGLED CHIRAL ANTI (target)
same-mode    z^-1 zbar^-1 (2+ln(z1 zbar1))   : real (ln|z|^2)      -> WALL paired

## Conclusion — [DERIVATION]

KFP nu=2/3 electron correlator is MULTIPLICATIVE (product of charge-sector and neutral-sector chiral
power laws), hence FACTORIZES (d_z d_zbar log G = 0) -> SEPARABLE half-chiral WALL. It does NOT fill
the chiral cell.

Both pasted candidate forms are REFUTED:
- Note #1 (z^-2h ln z, Jordan/LCFT): holomorphic (function of z) -> eml WALL, identical to the
  TMG/log-gravity wall already certified this session (FINDINGS_20260623_orthogonal_sweep). The
  claim "KFP = logarithmic CFT with additive-log Jordan block" is UNSUPPORTED by the primary source:
  the KFP fixed point is a free (Gaussian) boson fixed point with emergent SU(2), not an LCFT; the
  electron correlator is a vertex product, not a Jordan additive-log.
- Note #2 (z^-2hc zbar^-2hn (A + B ln zbar), cross-chiral factorizable): factorizes -> SEPARABLE
  half-chiral WALL. The note itself admits "factorisable mais cross-chiral", then tries to REDEFINE
  the target as "log anywhere in the neutral sector". REJECTED: the target (non-factorizable,
  d_z d_zbar log f != 0) is settled in this session (nonseparable_judge); a log isolated in one
  chiral sector and multiplied by the rest is separable = wall, regardless of whether it is in z or zbar.

Clarification (corrects a sloppy label during analysis): the PAIRED wall is ln(z1 zbar1)=ln|z1|^2
(same mode -> real). A CROSS-mode log ln(z1 zbar2) (holo of one mode, anti of the other, in the same
log argument) is non-factorizable -> target. KFP places its neutral log in zbar alone, factorized
from the charge power -> wall.

## Holo / anti ledger update

- eml (holo): KFP charge sector, note#1 Jordan-holo log.
- eml* (anti) SEPARABLE (half-chiral wall): KFP full correlator z^-1 zbar^-3 (A+B ln zbar).
- eml* (anti) ENTANGLED (target, FORM only): cross-mode log / additive non-separable -- NOT realized by KFP.
- ANTI forced + measurable + gauge-invariant + non-factorizable: still ZERO. Chiral cell EMPTY.
- New wall entry: KFP nu=2/3 = multiplicative/separable half-chiral wall; LCFT-Jordan claim refuted.

## Open

A physical two-mode system whose correlator is genuinely NON-FACTORIZABLE in z and zbar
(d_z d_zbar log != 0) with anti content, forced and measurable by interference. KFP does not qualify.
Secondary candidates from the search (graphene Kekule intervalley coherence; non-Hermitian microring
exceptional point with branch structure) remain to be reduced to a closed form and judged.

## Files
- kfp_verified.py (harness, in repo or to be added)
- this trace
