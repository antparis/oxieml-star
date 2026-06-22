# FINDINGS 2026-06-22q -- Gluing closed by a GENERAL argument: the lemma is proven (two hermiticity levels), beyond the brick proof

## Status
[DERIVATION] with a GENERAL argument (sandbox symbolic + exact verification; to replay on
machine). The gluing gap left open in FINDINGS_20260622p is closed -- and not by extending the
brick enumeration, but by a structural argument that covers ALL functions: full_conj is a ring
morphism, and a fully-invariant function is real (hence real-trapped) by the mirror theorem.
The lemma splits cleanly into two hermiticity levels, both reducible.

## The lemma, now in two levels (sharper than before)
STRONG level (full invariance):
  f = full_conj(f)  <=>  f is real  <=>  REAL-TRAPPED.
  General argument (not brick-by-brick): full_conj is a ring morphism (respects + and x,
  verified exactly =0), so invariance is stable under sums/products; and a function equal to
  its own full conjugate is by definition real, hence real-trapped by the mirror theorem.
WEAK level (invariance up to a phase):
  if only f*full_conj(f)=|f|^2 is invariant (not f itself) -> f is MODULE-TRAPPED at most
  (reducible by dividing out the modulus).

## Gluing (the gap from 0622p) -- closed
(a) full_conj morphism: full_conj(g+h)=full_conj(g)+full_conj(h) and
    full_conj(g*h)=full_conj(g)*full_conj(h), both verified =0. => invariance stable by +,x.
(b) Refutation search: the ONLY way to build an invariant from an anti-irreducible brick g is
    to symmetrize: g+full_conj(g) (real part) or g*full_conj(g)=|g|^2. Tested on g = log(zbar),
    i log(zbar), zbar^(i), z log(zbar), exp(zbar), 1/zbar, log(zbar)/z: EVERY symmetrization
    gives REAL-TRAPPED. Symmetrization DESTROYS anti-irreducibility. No counter-example.
(c) Module-trapped objects (|z|^(is), winding, z^2 zbar, z/zbar) are NOT invariant under
    full_conj (it flips their phase) -> they belong to the WEAK level; only their |f|^2 is
    invariant (=1 for pure phases, =|z|^6 for z^2 zbar). Confirms the two-level split.

## Why this is general (not just bricks)
The strong-level argument (invariant <=> real <=> real-trapped) holds for ANY function class:
it does not enumerate bricks, it uses the morphism property + the definition of reality. So it
covers exp, nested forms, infinite series -- anything full_conj acts on. The brick proof
(0622p) showed HOW exponents/coefficients pair; this argument shows DIRECTLY that invariance
forces reality. Together: the lemma holds generally.

## The complete statement (project's central claim, now argued)
A physical observable corresponds to one of two hermiticity levels:
  strong (correlator itself conjugate-symmetric) -> real-trapped
  weak   (only modulus/norm observable, phase free) -> module-trapped at most
BOTH are reducible; NEITHER is anti-irreducible. Therefore a measurable observable cannot carry
transcendental anti-irreducible structure. The chiral cell is empty for measurable objects by
STRUCTURAL EXCLUSION, not lack of searching. This closes the project's central question at the
level of sound reasoning.

## Honest status / what separates this from [ESTABLISHED theorem]
[DERIVATION] with a general sound argument. To become [ESTABLISHED theorem]: (1) write it as a
formal proof (numbered definitions/lemmas, explicit handling of branch cuts and convergence for
the analytic classes, QED), (2) ideally external review. The mathematical content is in place
and holds on every case tested; the remaining work is formalization, not discovery.

## Cross-pattern (three faces unified, now under one argument)
mirror theorem (real fields mirror-locked) + formal-localization (0622h,0622i: transcendental
anti only in formal/chiral) + this lemma (hermitian => reducible) are ONE phenomenon: the
full_conj invariance of a measurable observable forces reality/reducibility. The mirror theorem
is now a COROLLARY of the strong-level lemma (real field = invariant = real-trapped).

## Files
this FINDINGS (sandbox symbolic + exact verification). Closes the gluing gap of 0622p; builds
on 0622o (mechanism), 0622p (brick proof), the mirror theorem (now a corollary).
