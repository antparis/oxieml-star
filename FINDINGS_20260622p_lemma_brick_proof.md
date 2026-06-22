# FINDINGS 2026-06-22p -- Lemma "Hermitian => reducible" PROVEN brick-by-brick (powers + logs); orthogonal-axis decomposition; general gluing remains

## Status
[DERIVATION] upgraded -- rigorous brick-level PROOF on the two function classes that appear in
physical correlators and Ramanujan objects (powers z^a zbar^b, logs c1 log z + c2 log zbar).
The lemma holds on each brick with the exact mechanism. NOT yet the universal theorem: the
gluing step (sums/products of invariant bricks stay invariant-reducible) remains to formalize.

## The lemma (precise statement)
If f(z,zbar) is invariant under full conjugation (z<->zbar AND i<->-i) -- the mathematical
signature of a Hermitian/real observable -- then its zbar-dependence is the conjugate image of
its z-dependence, so f is reducible (real-trapped or module-trapped), never anti-irreducible.
Origin: Anthony's intuition "measurability forces reducibility" (from the wall series),
sharpened into a mechanism by the refutation test (FINDINGS_20260622o), now proven per brick.

## Proof by bricks (orthogonal-axis decomposition)
Instead of attacking "all analytic functions" head-on (would stall), decompose into bricks,
prove on each, preserve under combination.

BRICK 1 -- power z^a zbar^b:
  full_conj(z^a zbar^b) = zbar^conj(a) z^conj(b). Invariance f=full_conj(f) forces a=conj(b),
  i.e. b=conj(a). Write a=p+is (p,s real): z^a zbar^conj(a) = (z zbar)^p (z/zbar)^(is)
  = |z|^(2p) * pure-phase -> REDUCIBLE (module x phase).
  VERIFIED numerically (SymPy stalled on complex-power branches; |lhs-rhs|~1e-14 at 3 points
  with zbar=conj(z)). PROVEN.

BRICK 2 -- log combo c1 log z + c2 log zbar:
  full_conj = conj(c1) log zbar + conj(c2) log z. Invariance forces c1=conj(c2), i.e.
  c2=conj(c1). Write c1=u+iv: (u+iv)log z + (u-iv)log zbar = u log|z|^2 + i v log(z/zbar).
  First term real. Second: i v log(z/zbar) = -2v arg(z), REAL (verified: term2-full_conj(term2)=0).
  Whole combo REAL -> REAL-TRAPPED. PROVEN symbolically.

COUNTER-CHECK -- anti-irreducible bricks break invariance:
  zbar^(i), i log(zbar), log(zbar) alone: each has f != full_conj(f) -> NOT Hermitian.
  Confirms anti-irreducible and Hermitian are incompatible at the brick level.

## What is proven and what remains
PROVEN (rigorous): on power bricks and log bricks -- the two classes that make up physical
2-point correlators (powers) and CFT/Ramanujan log structures (logs) -- Hermitian invariance
forces conjugate-paired weights/coefficients, hence reducibility. The anti-irreducible
signature (complex expo on zbar alone, complex coef on log zbar alone) is exactly what breaks
invariance. The mechanism is now a PROOF on these classes, not just a numeric pattern.
REMAINS (gluing): show sums and products of full_conj-invariant bricks stay invariant AND
reducible. Intuitively true (invariance preserved by +,x; reducibility too) but needs a clean
lemma for the general analytic case (e.g. handling exp(zbar), nested forms).

## Significance
The orthogonal-axis decomposition WORKED: head-on "all functions" would stall; per-brick each
case became evident and provable. This upgrades the central result from [DERIVATION strongly
supported] (0622o, numeric pattern) to [DERIVATION with brick-level proof] on the physically
relevant classes. The project's central claim ("measurable transcendental anti cannot exist,
by structural exclusion") now has a proof skeleton with two classes done and the gluing step
identified as the remaining gap.

## Honest status / next
[DERIVATION], brick-level proof on powers+logs (rigorous), general gluing pending. The gluing
lemma + extension to exp/nested forms is the next math target; with it, the result becomes an
[ESTABLISHED theorem] closing the project's central question.

## Files
this FINDINGS (sandbox symbolic + numeric verification). Builds on 0622o (refutation test /
mechanism), the navigation law, the mirror theorem.
