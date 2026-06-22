#!/usr/bin/env python3
"""
orthogonal_probe.py -- Orthogonal-axis anti-false-negative probe for eml*.

PRINCIPLE (inspired by the 2026 AI disproof of Erdos' unit-distance problem,
made explicit by Will Sawin): the absence of a visible gradient is NOT proof of
absence of a solution. When the judge says "not anti" on a single slice of a
candidate, do NOT conclude negative before sweeping a parameter that is kept
fixed BY CONVENTION. Here the parameter is the ORDER n (Sawin's analogue: degree
of the number field). We sweep n instead of testing n=1 only.

DISCIPLINE (non-negotiable, anti-false-positive):
  - This probe DETECTS a possibility; it NEVER declares a discovery.
  - If a verdict flips toward "anti", the probe RAISES A FLAG: the case must go
    through the SPARC examination (is the z-bar DERIVED by physics or POSED?).
  - The judge (judge_v2) remains the sole math authority; this is a navigator.

CASE: Maass weak harmonic shadow term f_{n,k}(z) = Gamma(1-k, -4*pi*n*Im(z)) * e^{2 pi i n z}.
We sweep n = 1..N and k in {0, 1/2, 1, 3/2, 2}. Reservation 'n=1 only' is tested here.

Run from ~/Desktop/oxieml-star/ :  python3 orthogonal_probe.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def _verdict(expr):
    """certify_1field returns (label, detail); we want the label only."""
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def shadow_term(n, k):
    """Maass weak harmonic shadow term. Gamma argument is Im(z), NOT |z|^2."""
    x = (z + zbar) / 2
    y = (z - zbar) / (2 * sp.I)            # = Im(z)
    qn = sp.exp(2 * sp.pi * sp.I * n * (x + sp.I * y))   # holomorphic in z
    Gam = sp.uppergamma(1 - k, -4 * sp.pi * n * y)
    return sp.simplify(Gam * qn)


def orthogonal_sweep_order(N=5, ks=None):
    if ks is None:
        ks = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1),
              sp.Rational(3, 2), sp.Integer(2)]
    print("=" * 78)
    print("ORTHOGONAL PROBE -- axis = order n  (Maass weak harmonic shadow term)")
    print("f_{n,k}(z) = Gamma(1-k, -4*pi*n*Im(z)) * exp(2*pi*i*n*z)")
    print(f"Sweeping n = 1..{N}, k in {{0, 1/2, 1, 3/2, 2}} via judge_v2.")
    print("=" * 78)
    print(f"{'n':>2} {'k':>5}   verdict")
    print("-" * 78)
    flips = []
    for n in range(1, N + 1):
        for k in ks:
            try:
                f = shadow_term(n, k)
                v = _verdict(f)
            except Exception as e:
                v = f"ERR:{type(e).__name__}"
            tag = ""
            if v != "anti-holomorphic":
                tag = "  <-- VERDICT CHANGE (FLAG for SPARC exam)"
                flips.append((n, str(k), v))
            print(f"{n:>2} {str(k):>5}   {v}{tag}")
    print("-" * 78)
    if not flips:
        print(f">>> ALL n=1..{N}, all k -> anti-holomorphic.")
        print("    Reservation 'n=1 only' LIFTED: the shadow stays anti across the")
        print("    order axis -- a robust family, not an n=1 accident.")
        print("    STATUS: capability confirmed across n (NOT a discovery; this IS")
        print("    the Bruinier-Funke definition, theoretical, not physical).")
    else:
        print(">>> VERDICT CHANGED on some cases -- orthogonal axis revealed a POSSIBILITY:")
        for n, k, v in flips:
            print(f"      n={n}, k={k} -> {v}")
        print("    DISCIPLINE: this is a FLAG, not a result. Submit to SPARC examination")
        print("    (is the structure physically forced or posed?) before any claim.")
    print("=" * 78)
    return flips


if __name__ == "__main__":
    orthogonal_sweep_order(N=5)
