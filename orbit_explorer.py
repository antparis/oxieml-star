#!/usr/bin/env python3
"""
orbit_explorer.py  --  eml / eml(star) project, oxieml-star

Maps the INTERIOR cells of the removability cube (Anthony's "inner cubies").
Layer ON TOP of judge_v2 (NOT a new judge). judge_v2 stays the authority.

IDEA
----
The removability group has generators reality / gauge(module) / base. Each
generator that makes f removable is one bit of a SIGNATURE S(f). The subsets of
generators form a lattice = the corners of the cube:
  - empty set      -> removable by NONE = the chiral sector (incl. the target)
  - singletons     -> pure walls (real-trapped, module-trapped, basis-removable)
  - pairs / triple -> INTERIOR cells (removable by SEVERAL generators at once)

certify_1field returns the FIRST label in its order (holo -> real -> module ->
anti), so it MASKS interior cells: e.g. |z|^2 is real-trapped AND module-trapped,
but the judge only prints 'real-trapped'. The orbit explorer computes the FULL
signature, revealing the interior cell the judge collapses.

SCOPE (this step): the 2x2 lattice of the two OPERATIONAL generators
  - reality : full_conj(f) == f      (real-trapped test)
  - module  : is_module_trapped(f)   (gauge/module test)
'base' (basis-removable) needs its own operational criterion -> later, 2^3 cube.

A cell only COUNTS if inhabited by concrete f the judge confirms. Defined-but-
empty cells are analogy, not structure.

STATUS: [DERIVATION] until run on the M920q. Wirtinger exact. Marker != verdict.
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field, is_module_trapped, full_conj


def signature(expr):
    """Full removability signature {reality?, module?} -- NOT first-label-only."""
    expr = sp.expand(expr)
    is_real = (sp.simplify(expr - full_conj(expr)) == 0)
    is_mod = is_module_trapped(expr)
    judge, _ = certify_1field(expr)        # authority, first-label-only
    return is_real, is_mod, judge


def cell_name(is_real, is_mod):
    if is_real and is_mod:
        return "{reality, module}  INTERIOR"
    if is_real:
        return "{reality}          pure wall"
    if is_mod:
        return "{module}           pure wall"
    return "{}  empty-sig (chiral sector: holo / anti / mixed / TARGET)"


def line(c="=", n=82):
    print(c * n)


# Panel covering all four cells. c is a holomorphic constant (vortex center).
c = sp.symbols("c")
A = sp.Float("0.717") + sp.Float("0.395") * sp.I
B = sp.Float("-0.30") + sp.Float("1.20") * sp.I

PANEL = [
    ("z  (holo)",                 z),
    ("zbar  (anti)",              zbar),
    ("z + 0.3*zbar  (mixed)",     z + sp.Rational(3, 10) * zbar),
    ("z + zbar",                  z + zbar),
    ("Im z = (z-zbar)/2i",        (z - zbar) / (2 * sp.I)),
    ("z/zbar",                    z / zbar),
    ("z**2 * zbar",               z**2 * zbar),
    ("z*zbar  (|z|^2)",           z * zbar),
    ("log z + log zbar (log|z|^2)", sp.log(z) + sp.log(zbar)),
    ("A log(z-c) + B log(zbar-c)", A * sp.log(z - c) + B * sp.log(zbar - c)),
]


if __name__ == "__main__":
    line()
    print("orbit_explorer -- full removability signature {reality, module} (over judge_v2)")
    line()
    print(f"{'form':<32}{'judge(1st label)':<20}{'signature cell'}")
    print("-" * 82)
    cells = {}
    for name, expr in PANEL:
        is_real, is_mod, judge = signature(expr)
        cn = cell_name(is_real, is_mod)
        cells.setdefault(cn, []).append(name)
        masked = "  <-- judge masks module" if (is_real and is_mod) else ""
        print(f"{name:<32}{judge:<20}{cn}{masked}")

    line()
    print("CELL MAP (occupied cells of the 2x2 reality x module lattice):")
    for cn in ["{reality, module}  INTERIOR",
               "{reality}          pure wall",
               "{module}           pure wall",
               "{}  empty-sig (chiral sector: holo / anti / mixed / TARGET)"]:
        occ = cells.get(cn, [])
        status = ", ".join(occ) if occ else "(empty)"
        print(f"  {cn:<55} : {status}")

    line()
    interior = cells.get("{reality, module}  INTERIOR", [])
    print("FINDING [DERIVATION]:")
    if interior:
        print(f"  Interior cell {{reality & module}} is NON-EMPTY: {', '.join(interior)}.")
        print("  These are real radial functions, removable by BOTH generators")
        print("  (doubly-removable). The judge's ordered labels print only the first")
        print("  ('real-trapped'), MASKING that they are also module-trapped.")
        print("  => the cube's interior is real: walls OVERLAP, and the judge collapses")
        print("     the overlap. BUT doubly-removable is MORE trapped, not less --")
        print("     this is cartography, NOT a path to the empty target cell.")
    else:
        print("  Interior cell empty -> walls do not overlap for these two generators.")
    print()
    print("  The empty-signature cell is COARSE: it holds holo, anti, mixed AND the")
    print("  target together. Isolating the target needs the full forcing_filter")
    print("  (unpaired / transcendental / non-factorizable / spatial_carrier...).")
    line()
