# FINDINGS 2026-05-22 — Optical phase problem and the eml-star conjugation (theoretical lead)

Trace file (rule #12). English only. STATUS: [CONJECTURE] — nothing tested,
nothing certified. This note exists so the lead survives; it does NOT claim a result.

## Origin
While searching for natively-complex real data to feed the detector, found:
  Oh, Hugonnet, Park (KAIST), "Quantitative phase imaging via the holomorphic
  property of complex optical fields", Phys. Rev. Research 5, L022014 (2023);
  arXiv:2208.13168.

## What the paper establishes (their result, not ours)
- An optical field E(x) = |E| e^{i phi} is natively complex. By the Paley-Wiener
  theorem, band-limited optical fields (limited by the numerical aperture) are
  HOLOMORPHIC in the upper half-plane (UHP). So most imaging fields are holo by
  construction.
- Phase retrieval (Kramers-Kronig / Hilbert) works by applying the Hilbert
  transform to Re[log(1 + f(z))], i.e. it lives in the exp/log algebra of the
  complex field. Conditions: |R| > |S| and band-limit k > C = 2*NA/lambda.
- When holomorphy is violated, f acquires ZEROS in the UHP. The fundamental
  ambiguity of the 1D phase problem is "zero flipping": a zero z_j and its
  complex conjugate z_jbar give the SAME measured amplitude |f(x)| but DIFFERENT
  complex fields (Blaschke product, their Eq. 7-8). This is the origin of phase
  non-uniqueness.

## The lead (why this could matter for eml-star) — [CONJECTURE]
1. exp/log algebra overlap. Their machinery (log(1+f), exp, arg) is exactly the
   algebra of the eml family: eml(x,y)=exp(x)-log(y), eml-zero isolates arg.
   The phase-retrieval problem is phrased in the same operators as our toolbox.
   [DERIVATION-level observation, not a result.]

2. Zero-flipping IS a conjugation. Replacing z_j by z_jbar in the Blaschke
   product is, structurally, the holomorphic <-> anti-holomorphic swap that
   eml vs eml-star encode. The fundamental ambiguity of the optical phase
   problem is therefore a conjugation ambiguity — exactly the axis our detector
   is built to read.

## The hard question (must be answered before any claim) — DO NOT SKIP
What does eml-star ADD here that the existing tools (Blaschke products, Hilbert
transform, Hadamard factorization, minimum-phase theory) do NOT already provide?
The optics literature solved the zero-flipping description in 1975-1985
(refs [35-38] in the paper). If eml-star only RE-DESCRIBES this in our notation,
it is a reformulation, not a contribution. A genuine contribution would require
showing eml-star resolves, classifies, or computes something about the zeros
that the standard machinery does not. As of now this is UNKNOWN.

## Why this is NOT a detector test
Their fields are holomorphic by construction (Paley-Wiener). Feeding them to the
eml-star detector would return "holo" — a calibration, not a discovery. The lead
is conceptual (the conjugation structure of the phase ambiguity), not a dataset.

## Status summary
[CONJECTURE] zero-flipping <-> eml-star conjugation link is structurally real but
unproven and possibly not novel. No data, no judge, no MSE. Next step IF pursued:
answer the hard question above on paper, with explicit comparison to Blaschke /
minimum-phase, before writing a single line claiming significance.

## RESEARCH_LOG.md line to append
2026-05-22 [CONJECTURE] Optical phase-problem zero-flipping = conjugation; possible eml-star link via exp/log algebra. Unproven, possibly not novel (optics 1975-85). Hard question logged. trace: FINDINGS_20260522_optics.md
