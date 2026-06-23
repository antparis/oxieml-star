#!/usr/bin/env python3
"""
torus_cohomology_v1b.py -- GENUINE Dolbeault H^{0,1} (eml*) and H^{1,0} (eml) on the torus.

CORRECTION OF v0/v1: on Stein domains (all 1-variable local cases) H^{0,1}_dbar = 0, so the
v0/v1 "COHOMOLOGY" label (multivalued elementary primitive) actually detected a PERIOD/RESIDUE
obstruction (de Rham/Cech H^1), NOT smooth Dolbeault cohomology. Genuine H^{0,1} != 0 requires a
COMPACT complex manifold. The torus T = C/(Z + tau*Z) is the simplest: H^{0,1}(T) ~ C, H^{1,0}(T) ~ C.

RIGOROUS criterion (replaces the v0/v1 heuristic): a doubly-periodic (0,1)-form a*dzbar is
dbar-EXACT iff its AVERAGE over the fundamental domain vanishes (the constant Fourier mode is the
only obstruction; dbar is invertible on all nonzero modes). Average != 0  <=>  COHOMOLOGY,
represented by the harmonic class [dzbar]. Symmetric statement for d and [dz] (eml side).

This is v1a-bis (rigorous period = average, no multivalued-primitive heuristic) AND v1b (torus).
Calibration uses the square torus tau=i; the criterion (average over fundamental domain) is
tau-independent. z = x + i y, dbar = (d/dx + i d/dy)/2, d = (d/dx - i d/dy)/2.

AUTHORITY: exact SymPy integration over the fundamental domain. INDICATIVE until run on
Anthony's machine. No physical claim until criterion (c) (measurable observable) is met.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp

x, y = sp.symbols('x y', real=True)
pi, I = sp.pi, sp.I


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def average(a):
    """Average of a doubly-periodic coefficient over the square fundamental domain [0,1]^2."""
    return sp.simplify(sp.integrate(sp.integrate(a, (x, 0, 1)), (y, 0, 1)))


def verdict_torus(a):
    """a = coefficient of dzbar (anti) or dz (holo); criterion is identical (harmonic = constant mode)."""
    if _isz(a):
        return "ZERO", sp.Integer(0)
    avg = average(a)
    if _isz(avg):
        return "EXACT", avg
    return "COHOMOLOGY", avg


# dbar / d in real coordinates, for building EXACT test forms from periodic g(x,y)
def dbar(g):
    return sp.simplify((sp.diff(g, x) + I*sp.diff(g, y)) / 2)


def dz(g):
    return sp.simplify((sp.diff(g, x) - I*sp.diff(g, y)) / 2)


def main():
    e1 = sp.exp(2*pi*I*x)         # periodic in x (period 1), trivial in y
    g_sin = sp.sin(2*pi*x)        # periodic
    g_exp = e1                    # periodic

    # (id, coefficient, direction, expected)
    cases = [
        # ---- ANTI (eml*, H^{0,1}, coefficient of dzbar) ----
        ("anti  harmonic  a=1",          sp.Integer(1),        "anti", "COHOMOLOGY"),
        ("anti  harmonic  a=i",          I,                    "anti", "COHOMOLOGY"),
        ("anti  exact  a=dbar(sin2pix)", dbar(g_sin),          "anti", "EXACT"),
        ("anti  exact  a=dbar(e^2pix)",  dbar(g_exp),          "anti", "EXACT"),
        ("anti  exact  a=e^2pix",        e1,                   "anti", "EXACT"),
        ("anti  cohom  a=1+e^2pix",      1 + e1,               "anti", "COHOMOLOGY"),
        ("anti  exact  a=cos2piy",       sp.cos(2*pi*y),       "anti", "EXACT"),
        ("anti  zero   a=0",             sp.Integer(0),        "anti", "ZERO"),
        # ---- HOLO (eml, H^{1,0}, coefficient of dz) : symmetric ----
        ("holo  harmonic b=1",           sp.Integer(1),        "holo", "COHOMOLOGY"),
        ("holo  exact  b=dz(sin2pix)",   dz(g_sin),            "holo", "EXACT"),
        ("holo  exact  b=e^2pix",        e1,                   "holo", "EXACT"),
        ("holo  cohom  b=2+e^2piy",      2 + sp.exp(2*pi*I*y), "holo", "COHOMOLOGY"),
    ]

    print("=" * 92)
    print("TORUS COHOMOLOGY v1b -- GENUINE Dolbeault H^{0,1} (eml*) & H^{1,0} (eml)")
    print("rigorous criterion: average over fundamental domain != 0  <=>  COHOMOLOGY")
    print("=" * 92)
    print(f"{'case':30s} {'dir':5s} {'expected':12s} {'verdict':12s} {'agree':6s} average")
    print("-" * 92)
    nok = 0
    for name, coef, direction, exp in cases:
        v, avg = verdict_torus(coef)
        agree = "OK" if v == exp else "XX"
        nok += (v == exp)
        print(f"{name:30s} {direction:5s} {exp:12s} {v:12s} {agree:6s} {avg}")
    print("-" * 92)
    print(f"{nok}/{len(cases)} self-consistent")
    print("\nGENUINE non-trivial class found: the harmonic [dzbar] (eml*) and [dz] (eml),")
    print("each 1-dimensional on the torus, gauge-immune (compact-manifold Dolbeault, not a residue).")


if __name__ == "__main__":
    main()
