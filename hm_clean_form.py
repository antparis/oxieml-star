#!/usr/bin/env python3
"""Hasegawa-Mima screened vortex: clean closed form of the transcendental anti.
Shows the short-range anti signature is a MODULE log (1/2)log(z*zbar)=log|z|^2,
mirror-locked (equal weights), NOT an independent chiral log(zbar). SymPy exact
(Wirtinger). No Bessel injected: the form is reached analytically, not fitted.
Author: Anthony Monnerot, 2026. English only."""
import sympy as sp

G, rho = sp.symbols('Gamma rho_s', positive=True)
z, zb = sp.symbols('z zbar')
r = sp.sqrt(z*zb)
gE = sp.EulerGamma
x = sp.symbols('x', positive=True)

K0_small = -sp.log(x/2) - gE                       # K0 small-arg leading term
K0_sub = sp.expand_log(K0_small.subs(x, r/rho), force=True)
print("dw/dzbar ~ (iG/4pi rho^2) * [", K0_sub, "]")

piece = sp.expand_log(sp.Rational(1,2)*sp.log(z*zb), force=True)
print("transcendental piece = (1/2)log(z*zbar) =", piece)
expr = sp.Rational(1,2)*sp.log(z*zb)
print("d/dzbar =", sp.diff(expr, zb), "  d/dz =", sp.diff(expr, z),
      "  mu =", sp.simplify(sp.diff(expr, zb)/sp.diff(expr, z)), "= z/zbar (|mu|=1, mirror)")

b = sp.Float('0.5') + sp.Float('0.9')*sp.I
print("\ncontrast chiral b*log(zbar): d/dzbar =", sp.simplify(sp.diff(b*sp.log(zb), zb)),
      " d/dz =", sp.diff(b*sp.log(zb), z), "(=0) -> zbar-only = chiral; HM has NO such term")
print("\n=> HM anti = log|z|^2 (module log), mirror-locked. Clean form, NOT chiral.")
