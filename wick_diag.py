#!/usr/bin/env python3
# Wick artefact diagnostic for the eml-star mass-detector test (Dirac 1+1D).
# Purpose: let SymPy (the impartial arbiter) decide, in its own language,
# whether the naive d/dzbar test is corrupted by the Wick rotation z=x+it.
# This is a DIAGNOSTIC, not the final judge run. Pure symbolic, no numerics.

import sympy as sp

x, t, mu = sp.symbols('x t mu', real=True)

# Wirtinger operator d/dzbar in terms of real (x,t), with z = x + i t:
#   d/dzbar = 1/2 ( d/dx + i d/dt )
def d_dzbar(expr):
    return sp.Rational(1, 2) * (sp.diff(expr, x) + sp.I * sp.diff(expr, t))

# Light-cone operator d/dv with v = x + t :
#   d/dv = 1/2 ( d/dx + d/dt )
def d_dv(expr):
    return sp.Rational(1, 2) * (sp.diff(expr, x) + sp.diff(expr, t))

# Light-cone operator d/du with u = x - t :
#   d/du = 1/2 ( d/dx - d/dt )
def d_du(expr):
    return sp.Rational(1, 2) * (sp.diff(expr, x) - sp.diff(expr, t))

print("="*70)
print("WICK ARTEFACT DIAGNOSTIC  (z = x + i t)")
print("="*70)

# ---------------------------------------------------------------------------
# TEST 1: a trivial massless right-moving wave  phi = cos(x - t).
# Physically it is PURE chirality (depends only on u = x - t). No mass at all.
# Question to SymPy: does the naive d/dzbar test wrongly flag it?
# ---------------------------------------------------------------------------
phi = sp.cos(x - t)
r1_zbar = sp.simplify(d_dzbar(phi))
r1_v    = sp.simplify(d_dv(phi))
r1_u    = sp.simplify(d_du(phi))
print("\nTEST 1 : phi = cos(x - t)  [massless, pure right-mover]")
print("  d phi/dzbar =", r1_zbar, "   -> zero?", r1_zbar == 0)
print("  d phi/dv    =", r1_v,    "   -> zero?", r1_v == 0)
print("  d phi/du    =", r1_u,    "   -> zero?", r1_u == 0)
print("  VERDICT: naive d/dzbar test is", 
      "BROKEN (flags a massless wave)" if r1_zbar != 0 else "ok",
      "| light-cone d/dv is", "CLEAN (=0)" if r1_v == 0 else "not clean")

# ---------------------------------------------------------------------------
# TEST 2: general right-mover phi = f(x - t) with f an arbitrary function.
# This is the EXACT massless Dirac solution. Confirm it holds for any f.
# ---------------------------------------------------------------------------
f = sp.Function('f')
phi_gen = f(x - t)
r2_v = sp.simplify(d_dv(phi_gen))
r2_zbar = sp.simplify(d_dzbar(phi_gen))
print("\nTEST 2 : phi = f(x - t)  [general massless right-mover]")
print("  d phi/dv    =", r2_v,    "   -> zero for ALL f?", r2_v == 0)
print("  d phi/dzbar =", r2_zbar)
print("  VERDICT: d/dv = 0 identically (clean chirality test);")
print("           d/dzbar is generally NONZERO even with NO mass (Wick artefact).")

# ---------------------------------------------------------------------------
# TEST 3: what the MASS actually adds.
# Massless Dirac (mu=0): d phi/dv = 0  and  d chi/du = 0.
# With mass: the Dirac eqs are  d phi/dv = -(mu/2) chi ,  d chi/du = -(mu/2) phi.
# So the CLEAN observable of mass is  (d phi/dv) evaluated on a solution,
# which is exactly -(mu/2) chi : zero iff mu=0 (chi not identically zero).
# We verify the algebra of the operator identity, symbolically.
# ---------------------------------------------------------------------------
# Verify the operator identities relating real derivatives to z,zbar and u,v.
g = sp.Function('g')
test_expr = g(x, t)
# Identity A: d/dx + d/dt  ==  2 * d/dv
lhsA = sp.diff(test_expr, x) + sp.diff(test_expr, t)
rhsA = 2 * d_dv(test_expr)
# Identity B: (d/dx + d/dt) in terms of Wirtinger:  d/dx + d/dt = 2 Re-part mix
# We just confirm d/dv != d/dzbar as operators by applying to cos(x-t) (done above).
print("\nTEST 3 : operator identity check")
print("  (d/dx + d/dt) - 2 d/dv =", sp.simplify(lhsA - rhsA), 
      "  -> identity holds?", sp.simplify(lhsA - rhsA) == 0)

print("\n" + "="*70)
print("CONCLUSION (decided by SymPy, not by reasoning):")
print("  - The naive  d/dzbar = 0  test FAILS on a massless wave (Test 1):")
print("    z = x + i t injects zbar-dependence mechanically  => SPARC-type artefact.")
print("  - The light-cone  d/dv = 0  test is CLEAN for every massless f (Test 2).")
print("  - Therefore the legitimate mass observable is d/dv (real), not d/dzbar.")
print("  => Thursday's script must FIRST bridge d/dv to whatever verify_exact.py")
print("     certifies, before any Dirac mass test.")
print("="*70)
