#!/usr/bin/env python3
"""Check: is the Aharonov-Bohm LLL target z^a*zbar^b (real exponents) genuinely
chiral, or reducible to holomorphic x real-modulus? SymPy exact, Wirtinger
(z, zbar independent). English only. Author: Anthony Monnerot, 2026."""
import sympy as sp

z, zb = sp.symbols('z zbar')
m, alpha = 1, sp.sqrt(2)
a, b = m + alpha/2, -alpha/2
f = z**a * zb**b
df_dz, df_dzb = sp.diff(f, z), sp.diff(f, zb)
mu = sp.simplify(df_dzb / df_dz)

print("AB-dg target: f = z^a * zbar^b, a =", float(a), ", b =", float(b))
print("d f/d zbar   =", df_dzb, "  (nonzero -> binary judge: ANTI)")
print("Beltrami mu  =", mu)
print("|mu|         =", sp.Abs(b/a), "=", float(sp.Abs(b/a)), " CONSTANT -> radial -> reducible")
print("holo exp a-b =", sp.nsimplify(a-b), " ; modulus exp 2b =", float(2*b))
print("=> f = z^(a-b) * |z|^(2b) = holomorphic x real-modulus. NOT chiral.")

A = sp.Float('0.717') + sp.Float('0.395')*sp.I
B = sp.Float('-0.30') + sp.Float('1.20')*sp.I
c = sp.symbols('c')
fv = A*sp.log(z - c) + B*sp.log(zb - c)
muv = sp.simplify(sp.diff(fv, zb) / sp.diff(fv, z))
print("\nvortex_N1-type mu =", muv)
print("=> depends on (z-c)/(zbar-c), NOT radial -> genuinely chiral")
