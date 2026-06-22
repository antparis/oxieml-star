#!/usr/bin/env python3
"""Iterated anti-holomorphic dynamics vs the anti-holo conjecture.
Tests two regimes with the mixed-derivative discriminant d2 f / dz dzbar:
(1) PURE anti-holo iteration (Tricorn, w -> conj(w)^2 + c): parity lock (e).
(2) MIXED iteration (w -> conj(w)^2 + w + c): algebraic entanglement, reducibility check.
Run on Anthony's machine. Arbiter = this execution + judgment of separability/reality."""
import sympy as sp
z, zbar, c, cbar = sp.symbols('z zbar c cbar')

def mixed(fz): return sp.simplify(sp.diff(fz, z, zbar))
def kind(fz):
    dz = (sp.diff(fz,z)!=0); dzb = (sp.diff(fz,zbar)!=0)
    return "HOLO" if not dzb else "ANTI" if not dz else "MIXED"

print("="*64)
print("(1) PURE anti-holo iteration: w -> conj(w)^2 + c  (Tricorn)")
print("="*64)
Z, Zbar = z, zbar
for n in range(1,5):
    Z, Zbar = Zbar**2 + c, Z**2 + cbar
    fz = sp.expand(Z)
    print(f"  iter {n}: {kind(fz):5s}  mixed d2/dz dzbar = {mixed(fz)}")
print("  => alternates ANTI (odd) / HOLO (even), mixed=0 throughout => PARITY LOCK (e).")
print("     No independent z-bar is ever created by pure anti-holo iteration.")

print("\n"+"="*64)
print("(2) MIXED iteration: w -> conj(w)^2 + w + c")
print("="*64)
Z, Zbar = z, zbar
fz2 = None
for n in range(1,3):
    Z, Zbar = Zbar**2 + Z + c, Z**2 + Zbar + cbar
    fz2 = sp.expand(Z)
    print(f"  iter {n}: {kind(fz2):5s}  mixed d2/dz dzbar = {mixed(fz2)}")
# reducibility checks on iter-2
fconj = fz2.subs({z:zbar, zbar:z, c:cbar, cbar:c}, simultaneous=True)
is_real = sp.simplify(fz2 - fconj) == 0
poly = sp.Poly(fz2, z, zbar)
cross = [(m,co) for m,co in poly.terms() if m[0]>0 and m[1]>0]
print(f"\n  iter2 reality-lock (a)? f==conj(f): {is_real}  (False => not disguised-real)")
print(f"  iter2 separable? mixed==0: {mixed(fz2)==0}  (False => genuine z/zbar coupling)")
print(f"  iter2 cross terms (couple z AND zbar): {cross}")
print("\n  => MIXED iteration: NOT real (escapes lock a), NOT separable (genuine z^2*zbar")
print("     coupling). Reducibility to spinor-lock (d) depends on PHYSICAL realization:")
print("     real (x,y) substrate => lock d (decorative); natively-complex independent")
print("     z,zbar => potentially NEW irreducible structure. Algebra cannot decide;")
print("     only a physical mixed-dynamics system with a native-complex variable can.")
print("="*64)
