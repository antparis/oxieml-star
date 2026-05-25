#!/usr/bin/env python3
"""
dbar_solve_A.py — B1 / voie A: pure SYMBOLIC solution of a Wirtinger PDE.
Equation: df/dzbar = z * f   (z, zbar independent Wirtinger variables).
Expected closed form: f = h(z) * exp(z*zbar), h holomorphic arbitrary.
Dirac point: any nonzero solution MUST contain zbar (no holomorphic survivor).
NO data, NO PySR — exact resolution only. HEURISTIQUE until verified.
"""
import sympy as sp

z, zb = sp.symbols('z zb')
h = sp.Function('h')

print("=== EQUATION ===")
print("df/dzbar = z * f   (z held as parameter, integrate over zbar)")

fz = sp.Function('f')
ode = sp.Eq(sp.Derivative(fz(zb), zb), z*fz(zb))
sol = sp.dsolve(ode, fz(zb))
print("\n=== SymPy general solution (C1 plays the role of h(z)) ===")
print(sol)

f_claim = h(z) * sp.exp(z*zb)
lhs = sp.diff(f_claim, zb)
rhs = z * f_claim
residual = sp.simplify(lhs - rhs)
print("\n=== VERIFY claimed form f = h(z)*exp(z*zbar) ===")
print("f_claim   =", f_claim)
print("df/dzbar  =", sp.simplify(lhs))
print("z*f       =", sp.simplify(rhs))
print("residual  =", residual, " (must be 0)")
assert residual == 0, "claimed form does NOT satisfy the PDE"
print("OK: claimed closed form satisfies the PDE exactly.")

print("\n=== DIRAC POINT (no holomorphic survivor) ===")
print("Holomorphic f => df/dzbar = 0 => PDE gives z*f = 0 => f = 0.")
print("=> any NONZERO solution must carry zbar. The mirror is FORCED by the law.")

f_repr = sp.exp(z*zb)
dbar = sp.diff(f_repr, zb)
print("\n=== representative h(z)=1: f = exp(z*zbar) ===")
print("df/dzbar =", sp.simplify(dbar), " (nonzero => anti-holomorphic content)")
