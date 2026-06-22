# FINDINGS 2026-06-22c -- Parity symmetry law for mixed anti fractals; anti/symmetry decoupling [ESTABLISHED]

## Status
[ESTABLISHED] (machine, judge_v2 + exact high-res symmetry, code 0): for a mixed anti
fractal z^a+conj(z)^b+c (a!=b), the imaginary-axis mirror symmetry is PERFECT iff BOTH a
and b are odd. Anti-holomorphy (algebraic, judge) is DECOUPLED from geometric mirror
symmetry: an authentically anti object can be fully symmetric.

## How we got here (anomaly -> law)
Generalization (FINDINGS 0622b) found the dimension law generalizes but the symmetry law
"via a-b" FAILED, with one anomaly: (5,3) had full mirror symmetry despite its anti term.
Creusing the anomaly: first hypothesis "b odd -> symmetric" was REFUTED (cases (4,3),(6,3)
have b odd but are broken). Correct rule found and confirmed high-res: a AND b odd.

## The law (confirmed on machine, res 1500, EXACT flip symmetry)
imag-axis mirror symmetry of z^a+conj(z)^b+c:
  a,b ODD:      (5,3)=1.0000 (7,3)=0.9998 (3,1)=1.0000 (5,1)=1.0000  -> PERFECT
  a even,b odd: (4,3)=0.9452 (6,3)=0.9606 (4,1)=0.9906 (6,1)=0.9938  -> BROKEN (<1)
  separation min(a,b-odd) - max(a-even) = +0.0060 -> CLEAN (no overlap)
=> LAW: perfect imag-axis mirror symmetry  <=>  a and b both odd.
NUANCE: the breaking AMPLITUDE varies; (4,1),(6,1) break only weakly (~0.99) while
(4,2)-type even-b cases break hard (~0.87, FINDINGS 0622b). But the 1.000-vs-<1 split is
clean. judge_v2 confirms the 4 a,b-odd cases are ALL anti-holomorphic.

## Geometric reason (derivation)
Under the imag-axis reflection z -> -conj(z): a term z^a picks up (-1)^a and conj(z)^b
picks up (-1)^b. If both a,b odd, both terms flip sign coherently and the iterated set is
invariant -> perfect mirror symmetry. If parities differ (one even), the invariance is
broken. [DERIVATION] -- explains the numerical law, consistent on all 8 cases.

## The deeper point: anti-holomorphy DECOUPLED from geometric symmetry [ESTABLISHED]
The judge calls z^5+conj(z)^3 anti (algebraic property of the formula), yet the object is
fully mirror-symmetric (geometric property of the set). These are DISTINCT and not
implied by one another. This explains why the dimension law generalizes (it tracks a real
anti property -- boundary roughness) while the symmetry "law via a-b" failed (mirror
symmetry tracks parity, a separate axis). Two different things were being conflated.

## Full fractal result set (this session, all on machine)
- z^a+conj(z)^b+c with a!=b: anti-holomorphic (judge), apparently unexplored in literature.
- DIMENSION LAW [ESTABLISHED, 0622b]: anti boundary rougher than holo witness, +0.03..+0.09,
  stable non-artefact over 6 pairs (the d=2 low-res +0.068 was an artefact, collapsed to
  +0.005 -- killed by multi-resolution).
- PARITY SYMMETRY LAW [ESTABLISHED, this file]: perfect imag mirror <=> a,b both odd.
- DECOUPLING [ESTABLISHED]: anti (algebra) != geometric symmetry.
NOT a physical discovery (mathematical objects); a clean characterization of unexplored
mixed asymmetric anti-holomorphic fractals. Origin: the orthogonal-axis method (Erdos
2026 insight) applied to fractals.

## Files
fractal_parity_confirm.py (high-res confirmation, on machine), fractal_parity_law.py
(parity sweep), fractal_generalize.py, fractal_z3zbar2_deep.py, fractal_compass.py,
fractal_highres.py, fractal_images/*.png. Builds on FINDINGS 0622a and 0622b.
