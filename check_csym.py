#!/usr/bin/env python3
"""check_csym.py -- chiral-cross discriminant on the c_L vs c_R axis (M-IV hunt).

Question: is an asymmetric central charge (c_L != c_R, gravitational anomaly)
enough to reach the ENTANGLED_CHIRAL_ANTI target? Answer (this script): NO.
Varying the central-charge symmetry only moves between two WALLS:
  - c = cbar (paired sectors)   -> separation/module argument  -> WALL  (witness A)
  - c_L != c_R (anomaly)        -> asymmetric JUXTAPOSED logs   -> WALL  (witness B)
The target needs a CROSS-MIX: z1 and z2b inside the SAME transcendental argument
(witnesses C, D), i.e. an explicit left-right interaction, not two charges side by side.

Discriminant (master law): d = d_z1 d_z2b log f.  d = 0 => factorizable => wall.
Symbolic-exact (z1,z2,z1b,z2b independent); verdict identical to nonseparable_judge.
Authority remains the judge on Anthony's machine. English only."""
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
    print(f"{name:42s} | d = {str(d):26s} | {verdict}")
print("="*112)
chiral_cross((z1-z2)*(z1b-z2b),  "A separation (z1-z2)(z1b-z2b) [c=cbar]")
chiral_cross(z1**pi * z2b**phi,  "B asym juxtaposed z1^pi*z2b^phi [cL!=cR]")
chiral_cross(z1 - z2b,           "C cross-mix log(z1 - z2b)")
chiral_cross(1 + z1*z2b,         "D cross-mix log(1 + z1*z2b)")
print("="*112)
print("RESULT: A,B FACTORIZE (walls); C,D NON-FACTORIZABLE (target type).")
print("=> c_L != c_R alone is NOT sufficient: anomaly -> B -> separable wall.")
print("=> target requires a cross-sector MIX (explicit left-right interaction), Naimark-irreducible.")
