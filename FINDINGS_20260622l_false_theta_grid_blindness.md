# FINDINGS 2026-06-22l -- Rogers false theta: the grid is BLIND to (false-)modularity; defines the tool's domain of validity

## Status
[ESTABLISHED] (sandbox grid, to replay on machine). Rogers false theta functions are
classified HOLOMORPHIC by the three-operator grid, INDISTINGUISHABLE from genuine modular
theta. Negative on the target (no new class), but a clean POSITIVE result on the TOOL: the
grid detects LOCAL anti-holomorphy (d/dzbar, modulus, phase), and is BLIND to GLOBAL
(false-)modularity (a transformation property, not a local zbar property). Defines the
domain of validity of eml/eml*/eml0.

## What false theta are (research-confirmed)
Rogers false theta: a theta-like q-series WITH an extra sign (sgn) term that BREAKS modularity
(arXiv:2212.06337). They are the HOLOMORPHIC Eichler integrals -- when a mock theta's shadow
is a weight-3/2 unary theta, the mock theta is the mock modular form and the FALSE theta is
the (holomorphic) Eichler integral (Royal Soc. rsta.2018.0439). They have NO proper modular
completion; they are "quantum modular" (defined at roots of unity, Folsom-Ono-Rhoades). So a
false theta is a pure q-series (holomorphic), no zbar part at all.

## Grid result (sandbox)
  Rogers false theta Sum (-1)^n q^(n(n+1)/2)   eml:holo  eml*:holomorphic  eml0:not-pure-phase
  partial theta Sum (-1)^n q^(n^2)             eml:holo  eml*:holomorphic  eml0:not-pure-phase
  truncated theta                              eml:holo  eml*:holomorphic  eml0:not-pure-phase
  Jacobi theta3 (genuine modular)              eml:holo  eml*:holomorphic  eml0:not-pure-phase
  Eisenstein-like                              eml:holo  eml*:holomorphic  eml0:not-pure-phase
  mock theta f(q) bare                         eml:holo  eml*:holomorphic  eml0:not-pure-phase
ALL identical: holomorphic, not-pure-phase. The grid does NOT distinguish false theta from
genuine modular theta.

## Why (the real result -- tool domain of validity)
The grid measures LOCAL anti-holomorphy: how zbar enters the function (d/dzbar, |f|, phase).
False-modularity is NOT local in zbar -- it is a GLOBAL transformation property (behavior
under tau -> -1/tau; the sgn term breaks the modular law). That information lives in HOW the
function transforms, not in its LOCAL zbar-dependence. The grid is structurally blind to it.
This is correct, not a bug: it delimits what eml/eml*/eml0 can and cannot see.

## Ramanujan map now complete (three neighboring objects, three statuses)
- mock theta BARE        -> holomorphic [measurable]      (zbar absent)
- mock theta COMPLETION  -> anti transcendental [formal]  (zbar from non-holo completion)
- Rogers FALSE theta     -> holomorphic, = genuine theta   (zbar absent; false-modularity invisible)
Three Ramanujan objects, three statuses in our framework; the false theta marks where the
tool's power ends.

## Significance
Knowing what an instrument CANNOT see is as important as knowing what it can. The grid is a
LOCAL anti-holomorphy detector, not a modularity detector. To probe (false-)modularity one
would need a different tool (transformation-based, e.g. testing tau -> -1/tau behavior), which
is OUTSIDE the eml family's design. This sharpens the project's self-understanding.

## Honest note
Negative on novelty (no new grid class, no measurable transcendental anti), positive on
tool-characterization (domain of validity defined). Capability/limit, not discovery.

## Files
this FINDINGS (sandbox grid; light forms, replayable via the eml_zero_and_grid.py pattern).
Builds on 0622j (grid), 0622k (mock theta family universality).
