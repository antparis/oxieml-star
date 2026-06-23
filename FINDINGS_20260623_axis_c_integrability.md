# FINDINGS 2026-06-23 — Axis C: Newlander-Nirenberg integrability (strongest SPARC-pass)

**Status:** [ESTABLISHED] engine 8/8 (this machine) · [DERIVATION] structural conclusion · criterion (c) OPEN.

## What was built and tested

axis_c_integrability.py -- almost-complex structure on C^2 as a deformed (0,1) frame (Beltrami):
  Zb_1 = d/dz1bar + a1 d/dz1 + a2 d/dz2 ;  Zb_2 = d/dz2bar + b1 d/dz1 + b2 d/dz2.
NEWLANDER-NIRENBERG: holomorphic coordinates exist (anti content d-bar_J f is REMOVABLE by a
coordinate choice) IFF the (0,1) bundle is involutive: [Zb_1,Zb_2] in span{Zb_1,Zb_2}. The Lie-
bracket component OUTSIDE that span is the Nijenhuis obstruction N.
  N = 0  -> INTEGRABLE      : eml-coordinates exist, anti REMOVABLE (SPARC-removable).
  N != 0 -> NON_INTEGRABLE  : NO holomorphic coordinates exist, anti FORCED, non-removable by ANY
            coordinate choice -> strongest possible SPARC-pass (a THEOREM, not a period/heuristic).

## Exact command

cd ~/Desktop/oxieml-star && python3 axis_c_integrability.py; echo "EXIT=$?"

## Raw result (this machine) — 8/8 self-consistent, EXIT=0

standard J0 (a=b=0)            INTEGRABLE       R=0
holomorphic defo a2=z1         INTEGRABLE       R=0
anti defo a2=z1bar (other var) INTEGRABLE       R=0
NON-integrable a2=z2bar        NON_INTEGRABLE   R=[0,-1,0,0]
NON-integrable b1=z1bar        NON_INTEGRABLE   R=[1,0,0,0]
integrable a2=z2 (holo)        INTEGRABLE       R=0
integrable a1=z1bar (same var) INTEGRABLE       R=0
NON-integrable a1=z2bar        NON_INTEGRABLE   R=[-1,0,0,0]

Bug fixed during build: the engine caught a WRONG expected label in the calibration corpus
(a1=z1bar with Zb_2=d/dz2bar is INTEGRABLE, since the bracket only probes d/dz2bar of the
coefficients and z1bar has no z2bar dependence). Corpus expectation corrected; engine unchanged.

## Conclusion — [DERIVATION]

Axis C gives the strongest SPARC-pass available: N != 0 (non-integrable J) => NO holomorphic
coordinates exist (Newlander-Nirenberg) => the anti content d-bar_J f is FORCED and non-removable
by ANY coordinate choice -- a THEOREM, not a heuristic or a de Rham period. Like axis D, it requires
complex dimension >= 2 (in complex dim 1 every almost-complex structure is integrable, N == 0).

OPEN -- criterion (c): a MEASURABLE observable on a non-integrable almost-complex manifold (S^6 with
its octonionic J, twistor spaces) carrying this forced anti. Axis C maximizes criterion (b) but
(c) remains the verrou, as on every other front.

## Holo / anti ledger update

- New operator dimension: integrability (Nijenhuis). eml = J-holomorphic (d-bar_J f = 0);
  eml* forced when N != 0 (no holomorphic coordinates).
- Strongest (b) achieved: theorem-level non-removability (Newlander-Nirenberg).
- ANTI forced + measurable (criterion c): still ZERO. Chiral cell EMPTY.
- Structural map: the forced-non-removable-anti axes (C integrability, D cohomology) both need
  complex dim >= 2; one variable is too rigid for either.

## Files
- axis_c_integrability.py (engine)
- this trace
