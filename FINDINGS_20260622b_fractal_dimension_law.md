# FINDINGS 2026-06-22b -- Dimension law GENERALIZES over mixed anti fractals; symmetry law does NOT

## Status
[ESTABLISHED] (machine, 6 exponent pairs, 2 resolutions, code 0): the anti-holomorphic
boundary-roughness law generalizes -- every tested mixed anti fractal z^a+conj(z)^b+c
(a!=b) has a boundary fractal dimension HIGHER than its holomorphic witness z^a+c, with a
stable positive gap. [NEGATIVE] no clean symmetry law: the surviving symmetry is NOT
predicted by a-b. [OPEN] one anomaly: (5,3) has full mirror symmetry despite its anti term.

## Setup
For each pair (a,b): anti = z^a+conj(z)^b+c, holo witness = z^a+c. box=(-1.9,1.9)^2,
R=50, maxit=250. Dimension = box-counting on the boundary at res 1000 and 2000 (gap
stability check). Mirror symmetries = exact array flips (reliable). Rotational symmetries
= scipy image rotation (APPROXIMATE, edge blur, indicative only).

## Result 1: DIMENSION LAW -- generalizes [ESTABLISHED]
Gap = dim(anti) - dim(holo witness) at 2000px:
  (3,2): +0.093   (4,2): +0.026   (5,2): +0.077
  (4,3): +0.061   (5,3): +0.049   (5,4): +0.069
ALL SIX positive, none collapses between 1000px and 2000px. Anti dimension ~1.46-1.51,
holo witness ~1.41-1.44. The anti term thickens the boundary across the whole tested
family (amplitude varies +0.03..+0.09; weakest is (4,2) at +0.026, still positive).
=> "mixed anti fractals have a rougher boundary than their holo witness" is GENERAL,
not specific to z^3+conj(z)^2. Consistent with the d=2 artefact lesson: that one
collapsed to 0; these do not.

## Result 2: SYMMETRY LAW -- does NOT hold [NEGATIVE]
Reliable mirror symmetries (real, imag, rot180) of the anti object:
  (3,2): (1.000,0.926,0.926)   (4,2): (1.000,0.874,0.874)   (5,2): (1.000,0.964,0.964)
  (4,3): (1.000,0.945,0.945)   (5,3): (1.000,1.000,1.000)   (5,4): (1.000,0.938,0.938)
All keep the REAL axis (=1.000 everywhere -- expected, c real-axis structure). But the
imag-axis breaking is NOT predicted by a-b: (4,2) and (5,3) BOTH have a-b=2, yet (4,2)
breaks (0.874) while (5,3) is fully symmetric (1.000). So the hoped-for "symmetry =
f(a-b)" rule FAILS. Rotational numbers (approximate) show scattered near-1 values
((4,2) rot120=0.999) without a clean (a,b)-pattern. No symmetry law established.

## Result 3: ANOMALY (5,3) -- OPEN QUESTION
z^5+conj(z)^3+c has FULL mirror symmetry (1.000,1.000,1.000) like a holomorphic object,
despite carrying an anti term conj(z)^3. Yet its dimension gap is positive (+0.049), and
the judge would still call it anti. Hypothesis to test: does conj(z)^3 partially reduce
or align with z^5 in a way that restores mirror symmetry while keeping anti-holomorphy?
This is the next target (creuser).

## Honest standing
WON: a general, robust, non-artefact dimension law over unexplored mixed anti fractals --
a real (modest) contribution. LOST: the symmetry generalization (a-b does not predict).
A half-law: roughness generalizes, symmetry is object-specific. The (5,3) anomaly is a
concrete open lead. NOT a physical discovery (math objects).

## Files
fractal_generalize.py (run, on machine), fractal_generalize.txt (the table),
builds on FINDINGS_20260622a (the z^3+conj(z)^2 single-object characterization).
