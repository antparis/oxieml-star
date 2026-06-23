#!/usr/bin/env python3
"""
dolbeault_v0.py -- Axis D foundation engine: several-complex-variables d-bar cohomology.

This is the MULTI-VARIABLE generalization of the eml/eml* judge. The one-variable judge
classifies a FUNCTION f(z,zbar). Axis D classifies a (0,1)-FORM
    alpha = sum_i a_i(z,zbar) dzbar_i
by its position in d-bar cohomology H^{0,1}:

  HOL              : alpha = 0                      (no anti content)
  NOT_CLOSED       : d-bar alpha != 0              (not a cocycle; not a class candidate)
  EXACT            : alpha = d-bar g, g single-valued (removable; multi-var GAUGE wall analog)
  COHOMOLOGY       : closed, primitive g exists but is MULTIVALUED (log/period obstruction)
                     OR closed and no global primitive  -> NON-TRIVIAL class, NON-removable.
  UNDECIDED        : SymPy could not integrate (flag, do not claim)

Why axis D: a non-trivial H^{0,1} class is insensitive to any coboundary d-bar g, so it is
IMMUNE to the gauge wall that killed Ginibre (whose anti was d-bar-exact = a trivial cocycle).

SPARC in axis D: "treatment choice" = adding a coboundary d-bar g. EXACT => SPARC-fails
(artefact). COHOMOLOGY => SPARC-passes by construction.

v0 SCOPE: n-variable Wirtinger, closedness, sequential local exactness solver (Dolbeault-
Poincare homotopy), single-valuedness check of the primitive (log-period flag).
DEFERRED to v1: proper Dolbeault residue / period integral for higher-degree obstructions.

AUTHORITY: results are exact SymPy structural diagnostics but remain INDICATIVE until run on
Anthony's machine. No physical claim until criterion (c) (measurable observable) is separately met.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


class Form01:
    """A (0,1)-form alpha = sum a_i dzbar_i over variables z=(z_i), zbar=(zbar_i)."""
    def __init__(self, comps, zs, zbs):
        assert len(comps) == len(zs) == len(zbs)
        self.a = [sp.sympify(c) for c in comps]
        self.z = list(zs)
        self.zb = list(zbs)
        self.n = len(zs)


def is_closed(form):
    """d-bar alpha = 0  <=>  d a_j/d zbar_i = d a_i/d zbar_j  for all i<j."""
    n = form.n
    for i in range(n):
        for j in range(i + 1, n):
            if not _isz(sp.diff(form.a[j], form.zb[i]) - sp.diff(form.a[i], form.zb[j])):
                return False
    return True


def solve_primitive(form):
    """Sequential Dolbeault-Poincare solve: find g with d g/d zbar_k = a_k.
    Returns (g, ok). ok=False means SymPy could not produce a verifying primitive."""
    g = sp.Integer(0)
    for k in range(form.n):
        r = sp.simplify(form.a[k] - sp.diff(g, form.zb[k]))
        # closedness guarantees r is independent of zbar_0..zbar_{k-1}
        for mlt in range(k):
            if not _isz(sp.diff(r, form.zb[mlt])):
                return None, False
        try:
            incr = sp.integrate(r, form.zb[k])
        except Exception:
            return None, False
        if incr.has(sp.Integral):
            return None, False
        g = sp.simplify(g + incr)
    ok = all(_isz(sp.diff(g, form.zb[i]) - form.a[i]) for i in range(form.n))
    return (g, ok)


def has_branch(g):
    """Primitive multivalued? (log or fractional power -> period obstruction)."""
    if g is None:
        return False
    return g.has(sp.log) or any(
        (isinstance(p, sp.Pow) and p.exp.is_Rational and not p.exp.is_Integer)
        for p in g.atoms(sp.Pow))


def verdict(form):
    if all(_isz(c) for c in form.a):
        return "HOL", None
    if not is_closed(form):
        return "NOT_CLOSED", None
    g, ok = solve_primitive(form)
    if not ok:
        # closed but no verifying single-valued primitive found
        return "COHOMOLOGY", g
    if has_branch(g):
        return "COHOMOLOGY", g     # primitive exists but multivalued -> non-trivial period
    return "EXACT", g


# ----------------------------------------------------------------- calibration corpus
def main():
    z1, z2, zb1, zb2 = sp.symbols('z1 z2 zbar1 zbar2')
    Z, ZB = [z1, z2], [zb1, zb2]

    cases = []
    # HOL
    cases.append(("alpha_zero            [0,0]", Form01([0, 0], Z, ZB), "HOL"))
    # EXACT: g = zbar1^2 * zbar2  -> a = [2 zbar1 zbar2, zbar1^2]
    cases.append(("exact_poly  g=zb1^2 zb2", Form01([2*zb1*zb2, zb1**2], Z, ZB), "EXACT"))
    # EXACT mixed holo x anti: g = z1 * zbar2 -> a = [0, z1]
    cases.append(("exact_mixed g=z1 zb2", Form01([0, z1], Z, ZB), "EXACT"))
    # NOT_CLOSED: [zbar2, 0]
    cases.append(("not_closed  [zb2,0]", Form01([zb2, 0], Z, ZB), "NOT_CLOSED"))
    # COHOMOLOGY (period): [1/zbar1, 0] -> g=log zbar1 (multivalued around zbar1=0)
    cases.append(("cohomology  [1/zb1,0]", Form01([1/zb1, 0], Z, ZB), "COHOMOLOGY"))
    # EXACT transcendental: g = exp(zbar1)*zbar2 -> a=[exp(zbar1) zbar2, exp(zbar1)]
    cases.append(("exact_transc g=e^zb1 zb2", Form01([sp.exp(zb1)*zb2, sp.exp(zb1)], Z, ZB), "EXACT"))

    # one-variable-with-puncture (n=1): cohomology via period
    za, zba = sp.symbols('z zbar')
    cases.append(("n1_pole     [1/zbar]", Form01([1/zba], [za], [zba]), "COHOMOLOGY"))
    cases.append(("n1_local    [zbar^2]", Form01([zba**2], [za], [zba]), "EXACT"))

    print("=" * 84)
    print("DOLBEAULT v0  -- axis D foundation (several complex variables, H^{0,1})")
    print("=" * 84)
    print(f"{'case':28s} {'expected':12s} {'verdict':12s} {'agree':6s} primitive g")
    print("-" * 84)
    nok = 0
    for name, form, exp in cases:
        v, g = verdict(form)
        agree = "OK" if v == exp else "XX"
        nok += (v == exp)
        gs = "-" if g is None else str(g)
        print(f"{name:28s} {exp:12s} {v:12s} {agree:6s} {gs}")
    print("-" * 84)
    print(f"{nok}/{len(cases)} self-consistent")


if __name__ == "__main__":
    main()
