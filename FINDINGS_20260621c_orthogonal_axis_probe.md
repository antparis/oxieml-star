# FINDINGS 2026-06-21c -- Orthogonal-axis probe (anti-false-negative) + Maass shadow reservation lifted across order n

## Status
[ESTABLISHED] (executed on Anthony's machine, judge_v2): the Maass weak harmonic
shadow term stays anti-holomorphic for ALL n=1..5 and all k in {0,1/2,1,3/2,2} (25
cases). The reservation "single term n=1 only" (FINDINGS_20260620c) is LIFTED.
[METHOD] a new systematic test -- the orthogonal-axis probe -- is introduced.

## Origin of the method: the 2026 Erdos unit-distance disproof
In May 2026 an internal OpenAI reasoning model disproved Erdos' unit-distance
conjecture (Erdos Problem #90, 1946). Will Sawin (Princeton) did NOT solve it; he
made the AI's bound explicit and optimized it (n^1.014, arXiv:2605.20579). The
transferable lesson is NOT "Sawin's technique" (making each step explicit is
classical analytic number theory). The deep insight is the ORTHOGONAL AXIS, which
the AI found and humans missed for 80 years:
  - Humans varied the "obvious" parameter (size of the region, field FIXED at Q(i))
    -> standard analysis showed NO gradient -> everyone concluded "this can't work".
  - The AI kept the scale FIXED and grew the DEGREE of the number field instead.
  - Sawin proved that at fixed field the analysis exactly reproduces Erdos' bound
    ("no indication the choice of field matters") -- the gradient genuinely did not
    point at the solution, yet the solution was there.
LESSON: absence of a visible gradient is NOT proof of absence of a solution. When the
judge says "not anti" on a single slice, sweep a parameter held fixed BY CONVENTION
before concluding negative.

## The tool: orthogonal_probe.py
Takes a candidate family, sweeps a conventionally-fixed parameter (here the ORDER n,
the eml* analogue of Sawin's field degree), and reports the judge verdict at each
value. Imports the real judge_v2.certify_1field (unpacks its (label, detail) tuple).
DISCIPLINE (anti-false-positive, non-negotiable):
  - the probe DETECTS a possibility; it NEVER declares a discovery;
  - if a verdict flips toward "anti", the probe RAISES A FLAG "submit to SPARC exam"
    (is the z-bar structure physically FORCED or POSED?) -- exactly the test that
    caught Kimi's Candidate 1 as an encoding artefact;
  - judge_v2 stays the sole math authority; the probe is a navigator only.
This keeps the test anti-false-negative (never miss a hidden possibility) WITHOUT
becoming a false-positive generator (never declares a discovery on its own).

## Result on this case (machine, judge_v2)
Command: python3 orthogonal_probe.py
f_{n,k}(z) = Gamma(1-k, -4*pi*n*Im(z)) * exp(2*pi*i*n*z), Gamma argument = Im(z) not |z|^2.
n=1..5 x k in {0,1/2,1,3/2,2} = 25 cases, ALL anti-holomorphic, code 0. No flips.
=> "n=1 only" reservation LIFTED: robust family across the order axis.

## What this is and is NOT
IS: the order axis confirms the shadow is anti for a whole family, not an n=1
accident; the orthogonal-probe mechanism is validated on a real case with the real
judge. A documented reservation is removed.
IS NOT: a discovery. The anti shadow IS the Bruinier-Funke 2004 definition (CAPABILITY
not discovery), THEORETICAL not physical -- it confirms the project conjecture, does
not refute it. The orthogonal axis solidified an existing result; it did not turn a
negative into a positive.

## Next (orthogonal probe generalization)
Extend the probe to the other conventionally-fixed axes, each kept under judge+SPARC:
(2) number of fields (mono -> multi-field, the current single-field judge's blind
spot); (3) composition depth; (4) a continuous physical parameter of a given system.
Apply systematically BEFORE declaring any candidate negative (anti-false-negative
insurance). Reinforced rule: a flipped verdict is a FLAG for SPARC, never a result.

## Files
orthogonal_probe.py (tool, on machine), this FINDINGS. Research report on the Erdos
2026 work archived in the conversation (arXiv:2605.20579 Sawin, arXiv:2605.20695
companion verification).
