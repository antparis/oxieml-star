#!/usr/bin/env python3
"""
reaudit_after_fix.py -- Step 5: re-judge all ESTABLISHED anti results with the FIXED judge_v2,
verify NONE flips to module-trapped (no collateral damage from the blind-spot patch).
Also confirms known module cases (incl. the newly-caught |z|^(is)) are module.

Run from ~/Desktop/oxieml-star/ :  python3 reaudit_after_fix.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def verdict(expr):
    v, _ = certify_1field(expr)
    return v


c = sp.symbols("c"); s = sp.symbols("s", real=True, positive=True)
A = sp.Float('0.717') + sp.Float('0.395')*sp.I
B = sp.Float('-0.30') + sp.Float('1.20')*sp.I
n, k = 1, sp.Rational(1, 2)
x = (z + zbar)/2; y = (z - zbar)/(2*sp.I)
maass = sp.simplify(sp.uppergamma(1 - k, -4*sp.pi*n*y) * sp.exp(2*sp.pi*sp.I*n*(x + sp.I*y)))

ESTABLISHED_ANTI = [
    ("Maass shadow n=1 k=1/2",      maass),
    ("vortex_N1 (gold chiral)",     A*sp.log(z - c) + B*sp.log(zbar - c)),
    ("z+0.3zbar",                   z + sp.Rational(3, 10)*zbar),
    ("i*zbar",                      sp.I*zbar),
    ("exp(zbar)",                   sp.exp(zbar)),
    ("fractal z^2+zbar+c",          z**2 + zbar + c),
    ("fractal z^3+zbar^2+c",        z**3 + zbar**2 + c),
    ("fractal z^5+zbar^3+c",        z**5 + zbar**3 + c),
    ("fractal z^4+zbar+c",          z**4 + zbar + c),
    ("additive z^2+conj(z)",        z**2 + zbar),
]
KNOWN_MODULE = [
    ("|z|^(is) NEW (was anti?)",    (z*zbar)**(sp.I*s/2)),
    ("z^2*zbar",                    z**2*zbar),
    ("z/zbar",                      z/zbar),
    ("z^1.7*zbar^-0.7",             z**sp.Rational(17, 10)*zbar**sp.Rational(-7, 10)),
]

print("=" * 78)
print("RE-AUDIT (Step 5) -- established ANTI must stay anti with the FIXED judge")
print("=" * 78)
all_ok = True
for label, expr in ESTABLISHED_ANTI:
    v = verdict(expr); ok = (v == "anti-holomorphic")
    if not ok:
        all_ok = False
    print(f"  {label:<32} -> {v:<18} {'OK' if ok else '<<< FLIPPED!!'}")
print("-" * 78)
print(f">>> All established anti stay anti after fix: {'YES' if all_ok else 'NO -- ONE FLIPPED'}")

print("\nKnown module cases (must be module, incl. newly-caught |z|^(is)):")
mod_ok = True
for label, expr in KNOWN_MODULE:
    v = verdict(expr); ok = (v == "module-trapped")
    if not ok:
        mod_ok = False
    print(f"  {label:<32} -> {v:<18} {'OK' if ok else '<<< NOT MODULE!!'}")
print("-" * 78)
print(f">>> All module cases module (incl. |z|^(is) now fixed): {'YES' if mod_ok else 'NO'}")
print("=" * 78)
print(f"VERDICT: blind-spot patch {'CLEAN (no collateral damage)' if (all_ok and mod_ok) else 'HAS A PROBLEM -- revert to backup'}")
