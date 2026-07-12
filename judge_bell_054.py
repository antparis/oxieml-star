#!/usr/bin/env python3
"""Judge for the oriented bell -- SYMBOLIC certification of J3.
J3 rests on: the mirror map M[mu](u) = exp(i(a+b)u) * conj(mu(u)) is an
INVOLUTION (M[M[mu]] = mu exactly), hence D = |mu+ref| - |M[mu]+ref| obeys
D_mirror = -D identically (swap of the two terms). SymPy exact, generic
3-atom measure."""
import sympy as sp
u, a, b = sp.symbols('u a b', real=True)
n1, n2, n3 = sp.symbols('nu1 nu2 nu3', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', positive=True)
mu = w1*sp.exp(sp.I*n1*u) + w2*sp.exp(sp.I*n2*u) + w3*sp.exp(sp.I*n3*u)
M = lambda f: sp.exp(sp.I*(a+b)*u) * sp.conjugate(f)
J3 = sp.simplify(M(M(mu)) - mu)
print("J3 involution residue (expect 0):", J3)
assert J3 == 0, "J3 FAILED"
print("JUDGE VERDICT: J3 CERTIFIED (mirror is an exact involution;"
      " bell antisymmetry D_mir = -D follows identically).")
