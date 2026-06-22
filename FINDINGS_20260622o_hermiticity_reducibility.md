# FINDINGS 2026-06-22o -- Hermiticity and anti-irreducibility are MUTUALLY EXCLUSIVE (half-conjecture strongly supported; mechanism sketches the theorem)

## Status
[DERIVATION] strongly supported (sandbox, corrected judge; to replay on machine). The
half-conjecture "a Hermitian-observable correlator is always reducible (real or
module-trapped), never anti-irreducible" is supported by a REPRODUCIBLE MECHANISM, not blind
accumulation: every attempt to force anti-irreducibility BREAKS Hermiticity, and restoring
Hermiticity EVAPORATES the anti-irreducibility. The two properties are mutually exclusive on
all tested cases. This is NOT a proof of the universal conjecture (which needs a theorem), but
the observed mechanism IS the skeleton of that theorem.

## Setup
Hermiticity of a 2-point correlator <O O^dag> is encoded as f = full_conj(f) (invariance under
z<->zbar AND i->-i, the reflection/reality symmetry). Anti-irreducible signature (established
nav law): complex exponent on zbar ALONE, or complex coefficient on log(zbar) alone. The test
ACTIVELY seeks refutation: can a function be BOTH Hermitian AND anti-irreducible?

## Results (corrected judge)
FACE 1 -- standard Hermitian correlators (real weights), expected reducible:
  scalar h=hbar=1            hermitian=True   -> real-trapped
  spin h=2,hbar=1            hermitian=False  -> module-trapped
  with symmetric log         hermitian=True   -> real-trapped
  scalar + log|z|^2          hermitian=True   -> real-trapped
FACE 2 -- refutation attempts (force anti-irreducible, check Hermiticity):
  zbar^(i)  complex expo on zbar alone      hermitian=False  -> anti-holomorphic
  z^(-i) zbar^(i)  (Hermitianized)          hermitian=True   -> real-trapped   [anti GONE]
  i log(zbar)  complex coef on log zbar     hermitian=False  -> anti-holomorphic
  i log(z) - i log(zbar)  (Hermitianized)   hermitian=True   -> real-trapped   [anti GONE]
  i(log z - log zbar)                       hermitian=True   -> real-trapped
  log(z)*i + conj  (Hermitianized)          hermitian=True   -> real-trapped

## The mechanism (the real result)
Every anti-irreducible structure BREAKS Hermiticity (hermitian=False). Restoring Hermiticity
(adding the conjugate holomorphic partner) makes the anti EVAPORATE -> real-trapped. The two
are mutually exclusive, reproducibly. WHY: Hermiticity demands f = full_conj(f), a symmetry
that PAIRS the holomorphic and anti-holomorphic parts as conjugates -> equal-modulus weights
-> reducible by construction. Anti-irreducibility demands precisely the opposite: a zbar-part
that is NOT the conjugate of the z-part. The two requirements contradict.

## Toward the theorem (this test sketches the proof)
The observed mechanism is the skeleton of a general argument:
  Hermitian observable correlator  =>  f invariant under full_conj (z<->zbar, i->-i)
  =>  the zbar-dependence is the conjugate-image of the z-dependence (paired)
  =>  holo and anti weights are conjugate (equal modulus)
  =>  reducible (real-trapped or module-trapped), never anti-irreducible.
This is a [DERIVATION] (sound reasoning, not yet a rigorous proof): the gap is showing that
"f = full_conj(f)" rigorously forces "paired conjugate weights" for ALL function classes
(established here for power and log forms; general case needs a clean lemma).

## Significance
This is the central conjecture of the project ("measurability forces reducibility") tested at
its sharpest, refutable form, and it survived a deliberate refutation attempt. It explains
WHY the chiral cell is empty for measurable transcendental anti: not lack of searching, but a
structural exclusion (Hermiticity vs anti-irreducibility contradict). Cross-pattern note: this
joins the mirror theorem (real fields mirror-locked) and the formal-localization results
(0622h, 0622i: transcendental anti lives only in formal/chiral objects, never measurable) --
three faces of one phenomenon: a reality/symmetry constraint forces reducibility.

## Honest status / next
[DERIVATION] strongly supported, NOT proven. To replay on machine. The clean lemma
("f = full_conj(f) => conjugate-paired weights, for all analytic classes") would upgrade this
to [ESTABLISHED theorem] and close the project's central question. That lemma is the next
mathematical target.

## Files
this FINDINGS (sandbox). Builds on the navigation law (anti-irreducible signature), the mirror
theorem, and 0622h/0622i (formal localization).
