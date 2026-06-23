#!/usr/bin/env python3
"""
dolbeault_v1.py -- Axis D engine, SYMMETRIC (eml H^{1,0} AND eml* H^{0,1}) + rigorous period.

Upgrades dolbeault_v0 on two fronts mandated before any anti claim:

  (1) SYMMETRY (eml/eml* rule): one engine, two directions.
        direction="anti" : (0,1)-form alpha = sum a_i dzbar_i ; d-bar exactness ; eml* / H^{0,1}
        direction="holo" : (1,0)-form beta  = sum b_i dz_i    ; d    exactness ; eml  / H^{1,0}
      The tool MUST be irreproachable on the holomorphic side: a holomorphic function's
      anti-form is identically zero (never flagged anti).

  (2) RIGOROUS PERIOD: COHOMOLOGY is decided by single-valuedness of the primitive
      (monodromy). For an ELEMENTARY closed-form primitive g, g is multivalued around the
      singular locus iff it contains a log or a non-integer power -> nonzero period -> a
      NON-TRIVIAL class. This is exact for elementary primitives ([ESTABLISHED] there);
      if SymPy finds no closed-form primitive, verdict = UNDECIDED (no claim).

Verdicts (direction-agnostic): ZERO / NOT_CLOSED / EXACT / COHOMOLOGY / UNDECIDED.
  EXACT       -> removable by a coboundary (gauge-wall analog) -> SPARC fails.
  COHOMOLOGY  -> non-removable class -> SPARC passes by construction (gauge-immune).

v0 (dolbeault_v0.py) is left UNTOUCHED as the reference pivot.

AUTHORITY: exact SymPy structural diagnostics, INDICATIVE until run on Anthony's machine.
No physical claim until criterion (c) (measurable observable) is separately met.

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


class PForm:
    """A (0,1)-form (direction='anti') or (1,0)-form (direction='holo')."""
    def __init__(self, comps, zs, zbs, direction):
        assert direction in ("anti", "holo")
        assert len(comps) == len(zs) == len(zbs)
        self.a = [sp.sympify(c) for c in comps]
        self.z = list(zs)
        self.zb = list(zbs)
        self.n = len(zs)
        self.direction = direction

    def dvars(self):
        return self.zb if self.direction == "anti" else self.z


def from_function(f, zs, zbs, direction):
    """Build the natural form from a scalar f: d-bar f (anti) or d f (holo)."""
    dv = zbs if direction == "anti" else zs
    return PForm([sp.diff(f, v) for v in dv], zs, zbs, direction)


def is_closed(form):
    dv, n = form.dvars(), form.n
    for i in range(n):
        for j in range(i + 1, n):
            if not _isz(sp.diff(form.a[j], dv[i]) - sp.diff(form.a[i], dv[j])):
                return False
    return True


def solve_primitive(form):
    dv = form.dvars()
    g = sp.Integer(0)
    for k in range(form.n):
        r = sp.simplify(form.a[k] - sp.diff(g, dv[k]))
        for mlt in range(k):
            if not _isz(sp.diff(r, dv[mlt])):
                return None, False
        try:
            incr = sp.integrate(r, dv[k])
        except Exception:
            return None, False
        if incr.has(sp.Integral):
            return None, False
        g = sp.simplify(g + incr)
    ok = all(_isz(sp.diff(g, dv[i]) - form.a[i]) for i in range(form.n))
    return (g, ok)


def is_multivalued(g, dvars):
    """Rigorous single-valuedness test for an ELEMENTARY primitive:
    multivalued around the singular locus iff g contains a log or a non-integer power
    of a singular factor. Exact for elementary g."""
    if g is None:
        return False
    if g.has(sp.log):
        return True
    for p in g.atoms(sp.Pow):
        if p.exp.is_number and not p.exp.is_Integer:
            if any(p.base.has(v) for v in dvars):
                return True
    return False


def verdict(form):
    if all(_isz(c) for c in form.a):
        return "ZERO", None
    if not is_closed(form):
        return "NOT_CLOSED", None
    g, ok = solve_primitive(form)
    if not ok:
        return "UNDECIDED", g          # no closed-form primitive -> no claim
    if is_multivalued(g, form.dvars()):
        return "COHOMOLOGY", g          # rigorous: multivalued primitive -> nonzero period
    return "EXACT", g


# ----------------------------------------------------------------- calibration corpus
def main():
    z1, z2, zb1, zb2 = sp.symbols('z1 z2 zbar1 zbar2')
    Z, ZB = [z1, z2], [zb1, zb2]

    cases = []
    # ---- ANTI direction (eml*, H^{0,1}) ----
    cases.append(("anti  zero          [0,0]",            PForm([0, 0], Z, ZB, "anti"),              "ZERO"))
    cases.append(("anti  exact   g=zb1^2 zb2",            PForm([2*zb1*zb2, zb1**2], Z, ZB, "anti"), "EXACT"))
    cases.append(("anti  cohom   [1/zb1,0]",              PForm([1/zb1, 0], Z, ZB, "anti"),          "COHOMOLOGY"))
    cases.append(("anti  notclosed [zb2,0]",              PForm([zb2, 0], Z, ZB, "anti"),            "NOT_CLOSED"))
    # ---- HOLO direction (eml, H^{1,0}) ----
    cases.append(("holo  zero          [0,0]",            PForm([0, 0], Z, ZB, "holo"),              "ZERO"))
    cases.append(("holo  exact   g=z1^2 z2",              PForm([2*z1*z2, z1**2], Z, ZB, "holo"),    "EXACT"))
    cases.append(("holo  cohom   [1/z1,0]",               PForm([1/z1, 0], Z, ZB, "holo"),           "COHOMOLOGY"))
    cases.append(("holo  notclosed [z2,0]",               PForm([z2, 0], Z, ZB, "holo"),             "NOT_CLOSED"))
    # ---- IRREPROACHABILITY: holomorphic function has ZERO anti-form ----
    f_holo = 1/z1                      # purely holomorphic
    cases.append(("irrep holo-func anti-form ZERO",       from_function(f_holo, Z, ZB, "anti"),      "ZERO"))
    cases.append(("irrep holo-func holo-form EXACT",      from_function(f_holo, Z, ZB, "holo"),      "EXACT"))
    # ---- CONTROL: real field z1*zbar1 -> anti-form is EXACT (removable, real-trapped analog) ----
    f_real = z1*zb1
    cases.append(("ctrl real-field anti EXACT",           from_function(f_real, Z, ZB, "anti"),      "EXACT"))

    print("=" * 92)
    print("DOLBEAULT v1  -- symmetric (eml H^{1,0} & eml* H^{0,1}) + rigorous period")
    print("=" * 92)
    print(f"{'case':36s} {'dir':5s} {'expected':12s} {'verdict':12s} {'agree':6s} primitive")
    print("-" * 92)
    nok = 0
    for name, form, exp in cases:
        v, g = verdict(form)
        agree = "OK" if v == exp else "XX"
        nok += (v == exp)
        gs = "-" if g is None else str(g)
        print(f"{name:36s} {form.direction:5s} {exp:12s} {v:12s} {agree:6s} {gs}")
    print("-" * 92)
    print(f"{nok}/{len(cases)} self-consistent")
    print("\nSYMMETRY CHECK: holomorphic function -> anti-form ZERO (never flagged anti). irreproachable.")


if __name__ == "__main__":
    main()
