# FINDINGS 2026-06-24 -- [DERIVATION] Refined ENTANGLED_CHIRAL_ANTI target: distinct-spin cross-correlator in a non-unitary regime

## Decision (orthogonal axis applied to the choice itself)

Three options were on the table: (1) polish the tooling, (2) merge the tools, (3) move to the
physical hunt. Options 1-2 hold fixed the invariant "stay on the tool side". The whole history
converges on one statement: the tool is ready, the bottleneck is physical. The orthogonal move
is therefore option 3 (object side). Correction 2 below is carried INTO option 3 as a prerequisite,
because the hunt consumes this very result.

## Orthogonal axis applied to the four fallen non-Hermitian walls

| Wall | L/R asymmetry | form | removable by |
|------|---------------|------|--------------|
| Yang-Mills NH LCFT (commit 07792fd) | radial log (dilatation) | PAIRED | reality |
| PT free-fermion LCFT (commit b775917) | symmetric sectors | PAIRED | symmetry |
| Hatano-Nelson | uniform imaginary phase | GAUGE | imaginary similarity transf. |
| Gravitational anomaly c_L!=c_R (commit 9019436) | juxtaposed sectors | SEPARABLE | factorizes |

Shared invariant: the two-sector combination is always paired, symmetric, gauge, or juxtaposed
-- NEVER mixed irreducibly inside a single transcendental argument. Breaking it yields the spec.

## Refined target (falsifiable spec)

Form:  f = 1 + alpha*log(z1) + beta*log(conj z2)   (additive: SUM, not PRODUCT -- see layers_bench.py)
with   alpha != conj(beta)   (breaks pairing -> unpaired)
and    z1, z2 non-reducible  (Naimark-irreducible -> not z+zbar).

Physical lever that FORCES alpha != conj(beta) without an analyst choice: two conformal operators
of DISTINCT spin (h1 != h2, so s1 = h1 - h1bar != s2). In a NON-UNITARY regime (the only live door),
orthogonality fails: a cross-correlator <O1(z) O2(0)> between distinct-spin operators becomes
(a) non-zero AND (b) not self-conjugate, because the indefinite inner product separates left/right
states. Both sieve conditions (unpaired, reality_relaxed_nongauge) are realized in the SAME regime.

## SPARC test for this class

Question: is the similarity transformation that re-pairs the cross-correlator PHYSICAL or GAUGE?
  - PHYSICAL (changes spectrum / observables) -> non-removable -> genuine candidate.
  - GAUGE (free relabeling) -> wall (Hatano-Nelson case).
This is the question to settle on a concrete closed-form correlator, by the judge, on the machine.

## Correction 2 carried in (epistemic guard-rail)

A standard UNITARY interferometer is NOT a candidate: its two amplitudes share one Hilbert space and
|A1+A2|^2 makes zbar the conjugate of the SAME object -> paired -> REAL_TRAPPED (the z+zbar trap).
The "much larger candidate class" claim of FINDINGS_20260624_emergence_by_superposition.md is
narrowed: the candidate class is the conjunction (natively complex AND non-gauge reality-relaxed
AND non-reducible channels), i.e. exactly the layer-3 sieve, not "any interference".

## Sieve consistency

layers_bench.py answers ONE sieve condition (nonfactorizable: emerges iff SUM of distinct fields).
forcing_filter.py adds the other five necessary conditions. Together = full upstream sieve. The
refined target SURVIVES the sieve; the four NH walls are REJECTED, each for the logged reason.

## Status

[DERIVATION] -- sound reasoning, not certified. No concrete closed-form distinct-spin cross-correlator
of a non-unitary system has been fed to the judge yet. Chiral cell remains EMPTY.

## Next physical hunt

Find a closed-form cross-correlator <O1(z) O2(0)> between two distinct-spin conformal operators in a
non-unitary / non-Hermitian / Lindblad-steady-state system; feed it to nonseparable_judge; apply the
SPARC test above. Search non-explored parameter regimes, not textbook cases.
