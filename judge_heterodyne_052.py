#!/usr/bin/env python3
"""Judge companion for #052 -- SYMBOLIC certification of the two clauses.
J1 (mirror conjugation): for real atoms nu_k and real weights,
    mu_hat_mirror(u) == exp(i(a+b)u) * conj(mu_hat(u))  -- exactly.
J2 (symmetric self-mirror): a measure reflection-symmetric about the
    band center has a REAL centered field: Im s(u) == 0 identically
    (nothing for the heterodyne to break -- the asymmetry law's zero).
SymPy exact; generic 3-atom measure for J1, generic mirror pair for J2.
"""
import sympy as sp

u, a, b = sp.symbols('u a b', real=True)
n1, n2, n3 = sp.symbols('nu1 nu2 nu3', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', positive=True)

mu = w1*sp.exp(sp.I*n1*u) + w2*sp.exp(sp.I*n2*u) + w3*sp.exp(sp.I*n3*u)
mu_mir = (w1*sp.exp(sp.I*(a+b-n1)*u) + w2*sp.exp(sp.I*(a+b-n2)*u)
          + w3*sp.exp(sp.I*(a+b-n3)*u))
J1 = sp.simplify(mu_mir - sp.exp(sp.I*(a+b)*u)*sp.conjugate(mu))
print("J1 residue (expect 0):", J1)
assert J1 == 0, "J1 FAILED"

c, d, w = sp.symbols('c d', real=True) + (sp.Symbol('w', positive=True),)
mu_sym = w*sp.exp(sp.I*(c+d)*u) + w*sp.exp(sp.I*(c-d)*u)
J2 = sp.simplify(sp.im(sp.simplify(mu_sym * sp.exp(-sp.I*c*u))))
print("J2 Im s (expect 0):", J2)
assert J2 == 0, "J2 FAILED"

print("JUDGE VERDICT: J1 CERTIFIED (mirror conjugation, exact) ;"
      " J2 CERTIFIED (symmetric measure is its own mirror).")
