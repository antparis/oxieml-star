#!/usr/bin/env python3
"""
orthogonal_probe_generic.py -- Generic orthogonal-axis probe for eml*.

Sweeps ANY parameterized family f(param) and reports the judge verdict at each
value, flagging any value whose verdict differs from the expected baseline.
Unifies the orthogonal axes: order n, composition depth, continuous physical
parameter -- the probe does not care about the NATURE of the parameter, only
that you provide a factory make_f(param) and a list of values.

(The "number of fields" axis (mono -> multi-field) is NOT covered here: it needs
a multi-field judge that does not yet exist. Noted for a future build.)

PRINCIPLE (2026 Erdos unit-distance disproof, the AI's orthogonal axis): absence
of a visible gradient is not proof of absence of a solution. Sweep a parameter
held fixed by convention before concluding negative.

DISCIPLINE (anti-false-positive, non-negotiable):
  - DETECTS a possibility; NEVER declares a discovery.
  - A verdict differing from baseline is a FLAG -> SPARC examination (is the
    structure physically FORCED or POSED?), never a result.
  - judge_v2 is the sole math authority; this is a navigator.

CALIBRATED (sandbox, 3 controls): stable anti -> 0 flip; z+a*zbar -> flips at a=0
(holo) and a=1 (real! z+zbar is real-valued); z*(z*zbar)^n -> all flip. The probe
correctly catches flips toward holo / real-trapped / module, not just "anti".

Run from ~/Desktop/oxieml-star/ . Example usage at the bottom (Maass shadow).
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def _verdict(expr):
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def orthogonal_sweep(make_f, params, axis_name="param",
                     baseline="anti-holomorphic", title=""):
    """Sweep make_f over params; print verdicts; flag deviations from baseline.
    Returns (rows, flips). flips is the list to submit to SPARC examination."""
    print("=" * 78)
    print(f"ORTHOGONAL PROBE -- axis = {axis_name}")
    if title:
        print(title)
    print(f"baseline expected: {baseline}")
    print("=" * 78)
    print(f"{axis_name:>10}   verdict")
    print("-" * 78)
    rows, flips = [], []
    for p in params:
        try:
            f = make_f(p)
            v = _verdict(f)
        except Exception as e:
            v = f"ERR:{type(e).__name__}"
        rows.append((p, v))
        tag = ""
        if v != baseline:
            tag = "  <-- DEVIATION (FLAG for SPARC exam)"
            flips.append((p, v))
        print(f"{str(p):>10}   {v}{tag}")
    print("-" * 78)
    if not flips:
        print(f">>> All values -> {baseline}. Robust family across this axis.")
        print("    (Confirms robustness; NOT a discovery on its own.)")
    else:
        print(f">>> {len(flips)} value(s) deviate from baseline -- POSSIBILITY flagged:")
        for p, v in flips:
            print(f"      {axis_name}={p} -> {v}")
        print("    DISCIPLINE: this is a FLAG, not a result. Submit to SPARC exam")
        print("    (is the structure physically FORCED or POSED?) before any claim.")
    print("=" * 78)
    return rows, flips


# ---- Example families (edit / add your own) -------------------------------

def maass_shadow(n_and_k):
    """Maass weak harmonic shadow term; param = (n, k)."""
    n, k = n_and_k
    x = (z + zbar) / 2
    y = (z - zbar) / (2 * sp.I)
    qn = sp.exp(2 * sp.pi * sp.I * n * (x + sp.I * y))
    return sp.simplify(sp.uppergamma(1 - k, -4 * sp.pi * n * y) * qn)


def composition_depth(d):
    """Axis = composition depth. Example base g(z,zbar)=zbar+z**2 composed d times
    in the anti slot. Edit the base to probe your own candidate."""
    base = zbar + z**2
    e = base
    for _ in range(d - 1):
        e = e.subs(zbar, base)
    return e


if __name__ == "__main__":
    # Axis 1 -- order n (Maass shadow), k swept too
    ks = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1),
          sp.Rational(3, 2), sp.Integer(2)]
    params = [(n, k) for n in range(1, 6) for k in ks]
    orthogonal_sweep(maass_shadow, params, axis_name="(n,k)",
                     title="Maass shadow Gamma(1-k,-4pi*n*Im z)*e^{2pi i n z}")

    # Axis 3 -- composition depth (example; edit the base for real candidates)
    orthogonal_sweep(composition_depth, range(1, 5), axis_name="depth",
                     title="composition depth of base = zbar + z**2")
