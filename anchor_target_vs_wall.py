#!/usr/bin/env python3
"""Anchor test: does the master discriminant d_z1 d_z2bar log f separate the
ENTANGLED_CHIRAL_ANTI target from separable/half-chiral walls?
Self-contained exact Wirtinger check (z1,z2,z1b,z2b independent). English only.
Authority remains verify_exact.py / nonseparable_judge on this machine; this is the anchor."""
import sympy as sp

z1, z2, z1b, z2b = sp.symbols('z1 z2 z1b z2b')
pi, phi = sp.pi, sp.GoldenRatio

def chiral_cross(f, name):
    L = sp.log(f)
    d = sp.simplify(sp.diff(L, z1, z2b))
    has_anti = sp.simplify(sp.diff(f, z2b)) != 0 or sp.simplify(sp.diff(f, z1b)) != 0
    if not has_anti:
        verdict = "HOL (no anti)"
    elif d == 0:
        verdict = "FACTORIZABLE -> WALL (separable/half-chiral)"
    else:
        verdict = "NON-FACTORIZABLE -> ENTANGLED_CHIRAL_ANTI (target)"
    print(f"{name:34s} | d_z1 d_z2b logf = {str(d):28s} | {verdict}")

print("="*100)
chiral_cross(1 + pi*sp.log(z1) + phi*sp.log(z2b),      "target 1+pi*log z1+phi*log z2b")
chiral_cross(z1**pi * z2b**phi,                        "wall product z1^pi*z2b^phi")
chiral_cross(sp.exp(sp.I*pi*z1 + sp.I*phi*z2b),        "wall exp e^{i pi z1+i phi z2b}")
chiral_cross(z1**2 * z2**3,                            "holo control z1^2*z2^3")
print("="*100)
print("PASS criterion: only the first row is NON-FACTORIZABLE; the two walls FACTORIZE; holo has no anti.")
