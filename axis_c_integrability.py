#!/usr/bin/env python3
"""
axis_c_integrability.py -- Axis C: Newlander-Nirenberg integrability (eml/eml* lens).

An almost-complex structure on C^2 is given by a deformed (0,1) frame (Beltrami form):
    Zb_1 = d/dz1bar + a1 d/dz1 + a2 d/dz2
    Zb_2 = d/dz2bar + b1 d/dz1 + b2 d/dz2
NEWLANDER-NIRENBERG: local holomorphic coordinates exist (the anti content d-bar f is removable
by a coordinate choice) IFF the (0,1) bundle is involutive: [Zb_1, Zb_2] in span{Zb_1, Zb_2}.
The component of the Lie bracket OUTSIDE that span is the Nijenhuis obstruction N.

  N = 0  -> INTEGRABLE  : eml-coordinates exist, anti is REMOVABLE (SPARC-removable).
  N != 0 -> NON_INTEGRABLE : NO holomorphic coordinates exist, anti is FORCED, NON-removable
            by any coordinate choice -> the strongest possible SPARC-pass (a THEOREM, not a heuristic).

Structural fact: in complex dimension 1 every almost-complex structure is integrable (N == 0);
axis C, like axis D, is non-trivial only for complex dimension >= 2.

Criterion (c) (measurable observable) is NOT addressed here: non-integrable J (S^6, twistor spaces)
realize FORCED non-removable anti, but whether a measurable observable carries it stays open.

AUTHORITY: exact SymPy. INDICATIVE until run on Anthony's machine.
Author: Anthony Monnerot, 2026.
"""
import sympy as sp

z1, z2, z1b, z2b = sp.symbols('z1 z2 z1bar z2bar')
COORDS = [z1, z2, z1b, z2b]   # vector-field basis: d/dz1, d/dz2, d/dz1bar, d/dz2bar


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def lie_bracket(X, Y):
    """[X,Y]^k = sum_j X^j d_j Y^k - Y^j d_j X^k, vectors over COORDS."""
    out = []
    for k in range(4):
        s = 0
        for j in range(4):
            s += X[j]*sp.diff(Y[k], COORDS[j]) - Y[j]*sp.diff(X[k], COORDS[j])
        out.append(sp.simplify(s))
    return out


def nijenhuis_obstruction(a1, a2, b1, b2):
    """Return the residual of [Zb_1,Zb_2] outside span{Zb_1,Zb_2} (the Nijenhuis obstruction)."""
    Zb1 = [a1, a2, sp.Integer(1), sp.Integer(0)]   # d/dz1bar + a1 d/dz1 + a2 d/dz2
    Zb2 = [b1, b2, sp.Integer(0), sp.Integer(1)]   # d/dz2bar + b1 d/dz1 + b2 d/dz2
    B = lie_bracket(Zb1, Zb2)
    # zbar-block of the frame is identity -> coefficients are c1 = B[2], c2 = B[3]
    c1, c2 = B[2], B[3]
    R = [sp.simplify(B[k] - c1*Zb1[k] - c2*Zb2[k]) for k in range(4)]
    return R


def verdict(a1, a2, b1, b2):
    R = nijenhuis_obstruction(a1, a2, b1, b2)
    return ("INTEGRABLE" if all(_isz(r) for r in R) else "NON_INTEGRABLE"), R


def main():
    O = sp.Integer(0)
    cases = [
        # (name, a1,a2,b1,b2, expected)
        ("standard J0 (a=b=0)",              O, O, O, O,        "INTEGRABLE"),
        ("holomorphic defo a2=z1",           O, z1, O, O,       "INTEGRABLE"),
        ("anti defo a2=z1bar (other var)",   O, z1b, O, O,      "INTEGRABLE"),
        ("NON-integrable a2=z2bar",          O, z2b, O, O,      "NON_INTEGRABLE"),
        ("NON-integrable b1=z1bar",          O, O, z1b, O,      "NON_INTEGRABLE"),
        ("integrable a2=z2 (holo)",          O, z2, O, O,       "INTEGRABLE"),
        ("integrable a1=z1bar (same var)",   z1b, O, O, O,      "INTEGRABLE"),
        ("NON-integrable a1=z2bar",          z2b, O, O, O,      "NON_INTEGRABLE"),
    ]
    print("=" * 92)
    print("AXIS C -- Newlander-Nirenberg integrability (Nijenhuis obstruction)")
    print("N=0 INTEGRABLE (anti removable, eml-coords exist) | N!=0 NON_INTEGRABLE (anti FORCED)")
    print("=" * 92)
    print(f"{'case':34s} {'expected':16s} {'verdict':16s} {'agree':6s} obstruction R")
    print("-" * 92)
    nok = 0
    for name, a1, a2, b1, b2, exp in cases:
        v, R = verdict(a1, a2, b1, b2)
        agree = "OK" if v == exp else "XX"
        nok += (v == exp)
        Rs = "0" if all(_isz(r) for r in R) else str(R)
        print(f"{name:34s} {exp:16s} {v:16s} {agree:6s} {Rs}")
    print("-" * 92)
    print(f"{nok}/{len(cases)} self-consistent")
    print()
    print("VERDICT [DERIVATION]: axis C gives the strongest SPARC-pass available.")
    print("  N != 0 (non-integrable J) => NO holomorphic coordinates exist (Newlander-Nirenberg)")
    print("  => the anti content d-bar_J f is FORCED, non-removable by ANY coordinate choice -- a")
    print("  THEOREM, not a heuristic or a period. Requires complex dim >= 2 (like axis D).")
    print("  OPEN: criterion (c) -- a MEASURABLE observable on a non-integrable manifold (S^6,")
    print("  twistor space) carrying this forced anti. Strongest (b), (c) still the verrou.")


if __name__ == "__main__":
    main()
