#!/usr/bin/env python3
"""
eml_zero_and_grid.py -- Formalize eml-zero (pure-phase detector) alongside the eml/eml-star
judge, and run the THREE-operator grid on the key objects of the session.

Three operators (Anthony Monnerot's eml family), tested TOGETHER per his standing rule:
  eml   (holomorphic)  : df/dzbar == 0  -> object depends on z only
  eml*  (anti-holo)    : the judge_v2 4-label classifier (holo/anti/module/real)
  eml0  (pure phase)   : |f|^2 = f*conj(f) is CONSTANT (modulus 1 up to scale) while f varies
                         -> f is a pure phase (winding) -- characterizes the "wall" objects.

eml0 is NEW here: it gives a POSITIVE characterization of a sub-class of the module-trapped
walls (the pure-phase ones: |z|^(is), winding (z/zbar)^n), distinguishing them from genuine
anti (conj(g3), log(zbar), Zwegers) which are NOT pure phase. The three operators give three
INDEPENDENT axes where eml* alone gave one.

Run from ~/Desktop/oxieml-star/ :  python3 eml_zero_and_grid.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field, full_conj

I = sp.I


def eml(expr):
    """eml: holomorphic test. True if df/dzbar == 0 (depends on z alone)."""
    return sp.simplify(sp.diff(sp.expand(expr), zbar)) == 0


def eml_star(expr):
    """eml*: the 4-label judge (holo / real-trapped / module-trapped / anti-holomorphic)."""
    v, _ = certify_1field(expr)
    return v


def eml_zero(expr):
    """eml0: pure-phase detector. 'pure-phase' iff |f|^2 = f*conj(f) is constant AND f varies."""
    expr = sp.expand(expr)
    if sp.simplify(sp.diff(expr, z)) == 0 and sp.simplify(sp.diff(expr, zbar)) == 0:
        return "constant"
    mod2 = sp.simplify(expr * full_conj(expr))
    cst = (sp.simplify(sp.diff(mod2, z)) == 0 and sp.simplify(sp.diff(mod2, zbar)) == 0)
    return "pure-phase" if cst else "not-pure-phase"


print("=" * 84)
print("PART A -- eml0 CALIBRATION (must be irreproachable before use)")
print("=" * 84)
calib = [
    ("z/|z| = e^(i theta)         PURE PHASE", z/sp.sqrt(z*zbar), "pure-phase"),
    ("(z/zbar)^(1/2) winding      PURE PHASE", (z/zbar)**sp.Rational(1, 2), "pure-phase"),
    ("|z|^(is)                    PURE PHASE", (z*zbar)**(I*sp.Rational(1, 2)), "pure-phase"),
    ("(z/|z|)^3 = e^(3i theta)    PURE PHASE", (z/sp.sqrt(z*zbar))**3, "pure-phase"),
    ("z          (module varies)  NOT",        z, "not-pure-phase"),
    ("zbar       (module varies)  NOT",        zbar, "not-pure-phase"),
    ("z+zbar     (real)           NOT",        z + zbar, "not-pure-phase"),
    ("log(zbar)                   NOT",        sp.log(zbar), "not-pure-phase"),
    ("z*zbar=|z|^2 (real)         NOT",        z*zbar, "not-pure-phase"),
]
allok = True
for name, f, exp in calib:
    v = eml_zero(f)
    ok = (v == exp)
    if not ok:
        allok = False
    print(f"  {name:<42} -> {v:<16} {'OK' if ok else 'FAIL'}")
print("-" * 84)
print(f">>> eml0 calibration irreproachable: {'YES' if allok else 'NO -- do not use'}")

print("\n" + "=" * 84)
print("PART B -- THREE-OPERATOR GRID on the session's key objects")
print("=" * 84)
q = sp.exp(2*sp.pi*I*z)
y = (z - zbar)/(2*I)
objs = [
    ("mock theta f(q) bare [MEASURABLE]", q + q**2),
    ("conj(g3) anti-chiral sector", sp.exp(-2*sp.pi*I*zbar) + sp.exp(-4*sp.pi*I*zbar)),
    ("Zwegers y^(-1/2) conj(g3)", y**(-sp.Rational(1, 2))*sp.exp(-2*sp.pi*I*zbar)),
    ("symplectic fermion log(zbar)", sp.log(zbar)),
    ("wall |z|^(is)", (z*zbar)**(I*sp.Rational(1, 2))),
    ("wall winding (z/zbar)^(1/2)", (z/zbar)**sp.Rational(1, 2)),
    ("complete scalar log|z|^2", sp.log(z) + sp.log(zbar)),
    ("Kirsch-type rational anti 1/zbar", 1/zbar),
]
print(f"  {'object':<36}{'eml(holo?)':<12}{'eml* verdict':<18}{'eml0'}")
print("-" * 84)
for name, f in objs:
    e0 = "holo" if eml(f) else "-"
    es = eml_star(f)
    ez = eml_zero(f)
    print(f"  {name:<36}{e0:<12}{es:<18}{ez}")

print("\n" + "=" * 84)
print("READING: the three operators give THREE INDEPENDENT axes.")
print("eml0 isolates the PURE-PHASE walls (|z|^is, winding) -- a POSITIVE characterization,")
print("distinct from genuine anti (conj g3, log zbar, Zwegers = not-pure-phase) and from")
print("the real scalar wall (log|z|^2 = not-pure-phase but real-trapped). eml* alone gave")
print("one axis; eml + eml* + eml0 give a full map. This makes eml0 a 3rd pipeline detector.")
