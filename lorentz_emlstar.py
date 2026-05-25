#!/usr/bin/env python3
"""
lorentz_emlstar.py — apply the holo/anti-holo lens to a Lorentz boost.
Spacetime as complex plane: z = x + i*ct. A boost of rapidity phi maps
  ct' = ct*cosh(phi) - x*sinh(phi)
  x'  = x*cosh(phi)  - ct*sinh(phi)
Then z' = x' + i*ct'. Question: is z'(z) holomorphic, anti-holomorphic, or MIXED?
Expectation [DERIVATION]: a Euclidean ROTATION would be holomorphic (z'=e^{i th} z,
no zbar). A Lorentz boost is HYPERBOLIC -> should be MIXED (carry zbar). If so,
the zbar content is the signature of Minkowski (hyperbolic/causal) geometry vs
Euclidean. NO data, NO PySR. Pure symbolic. Judge: compute d z'/d zbar.
"""
import sympy as sp

z, zb = sp.symbols('z zb')
phi = sp.symbols('phi', real=True)

# Recover x and ct from z, zbar (z = x + i ct)
x  = (z + zb)/2
ct = (z - zb)/(2*sp.I)

# Lorentz boost (rapidity phi)
ctp = ct*sp.cosh(phi) - x*sp.sinh(phi)
xp  = x*sp.cosh(phi)  - ct*sp.sinh(phi)

# z' = x' + i ct'
zp = sp.simplify(xp + sp.I*ctp)
print("=== z' as function of z, zbar ===")
print("z' =", zp)

# Wirtinger derivative wrt zbar: is the boost holomorphic?
dzp_dzb = sp.simplify(sp.diff(zp, zb))
dzp_dz  = sp.simplify(sp.diff(zp, z))
print("\n=== JUDGE (Wirtinger) ===")
print("dz'/dz    =", dzp_dz)
print("dz'/dzbar =", dzp_dzb)

if dzp_dzb == 0:
    print("VERDICT: HOLOMORPHIC (boost = pure holomorphic map, no mirror).")
else:
    print("VERDICT: MIXED / ANTI-HOLOMORPHIC content present.")
    print("-> the zbar term is the signature of the hyperbolic (Minkowski) boost.")
    # express the zbar coefficient
    coeff_zb = sp.simplify(sp.diff(zp, zb))
    print("   zbar-coefficient =", coeff_zb)

print("\n=== CONTROL: Euclidean rotation (should be HOLOMORPHIC) ===")
th = sp.symbols('theta', real=True)
# rotation: x' = x cos - y sin, y' = x sin + y cos, with y = ct
yp_rot  = x*sp.sin(th) + ct*sp.cos(th)
xp_rot  = x*sp.cos(th) - ct*sp.sin(th)
zrot = sp.simplify(xp_rot + sp.I*yp_rot)
print("z'_rot =", zrot)
print("dz'_rot/dzbar =", sp.simplify(sp.diff(zrot, zb)))
