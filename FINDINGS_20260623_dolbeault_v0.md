# FINDINGS 2026-06-23 — Axis D foundation: dolbeault_v0 (several complex variables, H^{0,1})

**Status:** [ESTABLISHED] for v0 engine (8/8, this machine) · [HEURISTIC] for the COHOMOLOGY label (period heuristic, not yet a rigorous Dolbeault residue).

## What was built and tested

dolbeault_v0.py — the MULTI-VARIABLE generalization of the eml / eml* judge. The one-variable
judge classifies a FUNCTION f(z,zbar); axis D classifies a (0,1)-FORM alpha = sum a_i dzbar_i by
its position in d-bar cohomology H^{0,1}.

Why axis D (eml/eml* lens): in one variable, a function's anti content d f/d zbar is locally
ALWAYS removable (Dolbeault-Poincare), which is why every 1-variable wall (real/module/GAUGE)
is a removability wall. A NON-TRIVIAL H^{0,1} class is closed but NOT exact -> insensitive to any
coboundary d-bar g -> IMMUNE to the gauge wall that killed Ginibre. The one-variable judge cannot
structurally see this anti; it appears only for n>=2, or n=1 WITH topology (puncture -> period).

Verdicts: HOL (alpha=0) / NOT_CLOSED (d-bar alpha != 0) / EXACT (alpha=d-bar g, single-valued g =
removable, multi-var gauge-wall analog) / COHOMOLOGY (closed, primitive multivalued or absent =
non-trivial class, non-removable) / UNDECIDED (SymPy could not integrate).

SPARC in axis D: "treatment choice" = adding a coboundary d-bar g. EXACT => SPARC-fails.
COHOMOLOGY => SPARC-passes by construction.

## Exact command

cd ~/Desktop/oxieml-star && python3 dolbeault_v0.py; echo "EXIT=$?"

## Raw result (this machine) — 8/8 self-consistent, EXIT=0

alpha_zero    [0,0]            HOL
exact_poly    g=zb1^2 zb2      EXACT       g=zbar1**2*zbar2
exact_mixed   g=z1 zb2         EXACT       g=z1*zbar2
not_closed    [zb2,0]          NOT_CLOSED
cohomology    [1/zb1,0]        COHOMOLOGY  g=log(zbar1)   (multivalued -> period)
exact_transc  g=e^zb1 zb2      EXACT       g=zbar2*exp(zbar1)
n1_pole       [1/zbar]         COHOMOLOGY  g=log(zbar)
n1_local      [zbar^2]         EXACT       g=zbar**3/3

Engine validated end-to-end. [ESTABLISHED] for v0 classification logic.

## Scope and limits

- v0 SCOPE: n-variable Wirtinger, closedness, sequential Dolbeault-Poincare exactness solver,
  single-valuedness (log / fractional-power) period flag.
- LIMIT [HEURISTIC]: COHOMOLOGY currently rests on detecting a multivalued primitive (log/branch),
  NOT on an exact Dolbeault residue/period integral. Upgrading this is v1a.
- No external dependency (pure SymPy); standalone from judge_v2.

## Roadmap (next bricks)

- v1a  Dolbeault residue: replace the period heuristic by an exact cycle integral -> [ESTABLISHED] COHOMOLOGY.
- v1b  Compact manifolds (torus, Riemann surface): generic non-trivial H^{0,1} (dim = genus) WITHOUT punctures.
- v1c  Holomorphic dual H^{1,0} (eml side): the tool must detect BOTH classes + control (symmetry rule).
- v1d  Physical realization (criterion (c)): candidate = quantum Hall on a torus (Jacobi theta, modular tau)
       and Riemann-surface period ratios (tau natively complex AND measurable).

## Adversarial caveat — [DERIVATION]

Axis D beats the gauge wall, but does NOT guarantee criterion (c). The residual danger: a
measurable observable may extract only the real gauge-invariant (e.g. Chern number = integral of
curvature = integer), leaving the complex class unmeasured. The only clean escape: a system where
the complex PERIOD RATIO tau is itself the observable. That is the v1b+v1d target.

## Holo / anti ledger update

- New operator dimension opened: H^{0,1} (eml* cohomological) vs H^{1,0} (eml cohomological, v1c pending).
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.
- v0 supplies the first engine able to certify a NON-removable anti (COHOMOLOGY), pending v1a rigor
  and v1d physical realization.

## Files

- dolbeault_v0.py (engine)
- this trace
