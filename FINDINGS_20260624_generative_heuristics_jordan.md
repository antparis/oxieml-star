# FINDINGS 2026-06-24 -- [DERIVATION] Generative heuristics (duals of the orthogonal axis) + non-reciprocal EP bifurcation criterion

## Context

History check confirmed: the detection-lens inventory is exhausted and convergent (object axes A-E,
meta-methods M-I..M-V, axis_fingerprint.py all converge on the non-Hermitian sector or the empty cell).
The bottleneck is NOT methodological: the #1 physical candidate (non-reciprocal exceptional point /
Jordan block, structure log(z1 - z2b) target-type) is already framed; the only wall is that no
closed-form correlator of a REAL device has been derived and certified. So new DETECTION lenses would
not help. The orthogonal axis was applied to ITSELF to derive GENERATIVE heuristics instead.

## The orthogonal axis applied to itself

Invariant the orthogonal axis holds fixed: it assumes novelty comes from VARYING a held-fixed
parameter. Breaking that yields three generative siblings:

- M-VI -- Perturbation around a wall [CONJECTURE]. Start from a wall with a known closed form
  (reciprocal EP microring = certified wall) and add the minimal physical term that breaks its
  removability invariant (reciprocity), to first order. The order-1 term IS the target-type
  correction. Generative version of the orthogonal axis (deform a known closed form, read order 1).

- M-VII -- Invariant / anomaly (inverse Noether) [CONJECTURE, RISKY]. The orthogonal axis seeks what
  VARIES; this dual seeks what is CONSERVED when the anti is removable (the charge of the full_conj
  involution), then the system that VIOLATES it anomalously. WARNING: risk of collapsing back onto the
  gravitational anomaly wall (c_L!=c_R, separable, commit 9019436). The REALITY anomaly (full_conj) is
  NOT the central-charge anomaly -- must be distinguished rigorously before investing, else it re-walls.

- M-VIII -- Minimal derivation [DECISIVE, executed below]. Invert "device -> form" into
  "minimal form -> device". The object is in hand (2x2 Jordan block); derive its closed form exactly,
  certify, then look for the device that realizes it.

These three exhaust the genuine duals (variation -> perturbation, conservation, degeneracy/minimality).
Listing more would be filler.

## M-VIII result (jordan_ep_cross.py)

Command: cd ~/Desktop/oxieml-star && python3 jordan_ep_cross.py

EXACT (judge-certifiable), all SymPy:
  - Jordan block [[lambda,g],[0,lambda]]: 1 eigenvector / 2 -> non-diagonalizable (Naimark by construction).
  - Resolvent cross component R12 = g/(lambda-omega)^2 -> DOUBLE pole.
  - Time propagator cross component P12 = -i*g*t*exp(-i*lambda*t) -> linear-t (LCFT log signature).
  - log forced by weight degeneracy: d/dh[z1^(-2h)] = -2*log(z1)/z1^(2h).

Cross discriminant d = d_z1 d_z2b log f on three topologies:
  T1 product equal weights   z1*z2b        -> d = 0                 -> WALL
  T2 product ASYM weights    z1^a * z2b^b  -> d = 0                 -> WALL
  T3 mixed additive          z1 - z2b      -> d = (z1-z2b)^(-2)     -> TARGET-TYPE

## Refined criterion (the new bit) [DERIVATION]

Asymmetric conformal weights are NOT sufficient: T2 stays a wall despite distinct exponents. Only a
MIXED additive argument (z1 - z2b) is non-factorizable -> target. Therefore the non-reciprocity must
mix the two sectors into a SINGLE additive argument, not merely produce asymmetric weights. This
sharpens the spec and removes a candidate false lead (asymmetry-as-sufficient).

## Open physical question (unchanged bottleneck)

Does a real non-reciprocal EP device (e.g. DRUM) produce the MIXED argument (target) or only
asymmetric weights (wall)? To settle by deriving one device's closed-form spatial correlator and
certifying it with nonseparable_judge on the machine. Until then the chiral cell stays EMPTY.

## Status

A/B/C [ESTABLISHED on certification] -- exact algebra + cross discriminant, to confirm on the machine.
Refined criterion [DERIVATION]. M-VI, M-VII [CONJECTURE], M-VII carries a re-wall warning. Cell EMPTY.

## Symmetry ledger update

New generative heuristics added: M-VI perturbation, M-VII anomaly, M-VIII minimal derivation.
New refined criterion: target needs a MIXED additive cross-argument, not asymmetric weights.
Walls unchanged. Chiral cell: still empty. Next: derive one real non-reciprocal EP correlator.
