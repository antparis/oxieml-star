#!/usr/bin/env python3
"""
diagnose_blindspot.py -- OBSERVE the judge_v2 module-trapped blind spot WITHOUT changing anything.

Confirms on YOUR machine that:
  (1) |z|^(is) (the inverse-square supercritical radial part) has L = pure-imaginary CONSTANT,
      so the current criterion (L_real + product-only) misclassifies it as anti?;
  (2) NO genuine anti (z+0.3zbar, vortex_N1, i*zbar, exp(zbar)) has the signature
      (L constant AND L pure-imaginary), so the proposed fix is SAFE.

The proposed fix (NOT applied here): treat as module-trapped if
   (L_real OR (L pure-imaginary AND L constant)) AND product-only.
A constant L with no z,zbar dependence means dlog(f)/dzbar has no genuine anti content
-- it is a modulus power (real or imaginary exponent). This closes the blind spot.

Run from ~/Desktop/oxieml-star/ :  python3 diagnose_blindspot.py
"""
import sympy as sp
from judge_v2 import z, zbar, full_conj, certify_1field


def diagnose_L(expr):
    expr = sp.expand(expr)
    dfdzbar = sp.simplify(sp.diff(expr, zbar)); dfdz = sp.simplify(sp.diff(expr, z))
    if dfdzbar == 0: return ("holo (dfdzbar=0)", None, None, None, None)
    if dfdz == 0:    return ("pure-anti (dfdz=0)", None, None, None, None)
    try:
        L = sp.simplify(zbar*dfdzbar/expr)
        L_real = sp.simplify(L - full_conj(L)) == 0
        t = sp.symbols("t", positive=True)
        prod_only = sp.simplify(L.subs({z: t*z, zbar: zbar/t}) - L) == 0
        L_is_const = (sp.simplify(sp.diff(L, z)) == 0 and sp.simplify(sp.diff(L, zbar)) == 0)
        L_pure_imag = (sp.simplify(L + full_conj(L)) == 0)
        return (str(L), bool(L_real), bool(prod_only), bool(L_is_const), bool(L_pure_imag))
    except Exception as e:
        return (f"ERR:{type(e).__name__}", None, None, None, None)


s = sp.symbols("s", real=True, positive=True)
a = sp.sqrt(2); c = sp.symbols("c")
A = sp.Float('0.717') + sp.Float('0.395')*sp.I
B = sp.Float('-0.30') + sp.Float('1.20')*sp.I
vortex = A*sp.log(z - c) + B*sp.log(zbar - c)

CASES = [
    ("|z|^(is) BLIND SPOT (target=module)", (z*zbar)**(sp.I*s/2), "module"),
    ("z+0.3zbar GENUINE anti",              z + sp.Rational(3, 10)*zbar, "anti"),
    ("i*zbar GENUINE anti",                 sp.I*zbar, "anti"),
    ("exp(zbar) GENUINE anti",              sp.exp(zbar), "anti"),
    ("vortex_N1 GENUINE anti",              vortex, "anti"),
    ("z^2*zbar MODULE",                     z**2*zbar, "module"),
    ("z/zbar MODULE",                       z/zbar, "module"),
    ("z^1.7*zbar^-0.7 MODULE",              z**sp.Rational(17, 10)*zbar**sp.Rational(-7, 10), "module"),
]

print("=" * 104)
print("BLIND-SPOT DIAGNOSTIC (judge_v2 unchanged) -- observe L and current verdict")
print("=" * 104)
print(f"{'case':<40}{'L':<20}{'Lreal':<7}{'prod':<6}{'const':<7}{'pureIm':<7}{'verdict_now':<16}{'target'}")
print("-" * 104)
safe = True
for label, expr, target in CASES:
    L, Lr, po, isc, pim = diagnose_L(expr)
    v, _ = certify_1field(expr)
    print(f"{label:<40}{L[:18]:<20}{str(Lr):<7}{str(po):<6}{str(isc):<7}{str(pim):<7}{v:<16}{target}")
    if target == "anti" and isc and pim:
        safe = False  # a genuine anti has the (const+pureImag) signature -> fix unsafe
print("-" * 104)
print(f">>> |z|^(is) misclassified by current judge: "
      f"{'YES (verdict=anti, should be module) -- blind spot confirmed' if certify_1field((z*zbar)**(sp.I*s/2))[0]=='anti-holomorphic' else 'no'}")
print(f">>> Proposed fix SAFE (no genuine anti has const+pureImag signature): {'YES' if safe else 'NO -- DO NOT PATCH'}")
