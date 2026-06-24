#!/usr/bin/env python3
"""layers_bench.py -- emergence by superposition (orthogonal-axis bench, M-IV).

Question: can the cross-coupling (target-type, d_z1 d_z2b log f != 0) appear WITHOUT
an explicit coupling term g*z1*z2b -- just by stacking factorized layers (walls)?
Answer: YES, if you stack by SUM, not by PRODUCT.

  PRODUCT of factored layers  -> log(product) = sum of separate logs -> d = 0 -> WALL.
  SUM of two DISTINCT fields   -> log(sum) does NOT separate          -> d != 0 -> EMERGES.
  ONE field + its own mirror (z + zbar) = 2 Re(z)                     -> REAL_TRAPPED wall (the trap).
  Mixing amplitude a tunes the weight; a=0 decouples (channel off).

Consequence for the hunt: the target no longer requires an exotic explicit coupling.
ANY additive superposition of two distinct channels (interferometer, two paths, two baths,
two resonances) carries the cross term. Remaining lock (physical, untestable on a toy form):
the two channels must be genuinely DISTINCT and non-reducible (else z+zbar, a wall).

Discriminant d = d_z1 d_z2b log f, symbolic-exact (verdict identical on the judge machine).
Authority remains judge_v2 / nonseparable_judge. English only."""
import sympy as sp
z1, z2b = sp.symbols('z1 z2b')        # two DISTINCT fields: left (holo), right (anti)
z, zb   = sp.symbols('z zb')           # ONE field and its own conjugate
a       = sp.symbols('a')
def disc(f):
    return sp.simplify(sp.diff(sp.log(f), z1, z2b))
def full_conj(f):                       # reality test for one-field forms: z<->zb, I->-I
    return f.subs({z: zb, zb: z, sp.I: -sp.I}, simultaneous=True)
def show(f, name):
    d = disc(f)
    print(f"{name:46s} | d = {str(d):28s} | {'WALL' if d==0 else 'EMERGES -> target-type'}")
print("="*108)
print("PRODUCT layering (multiply walls) -> stays a wall:")
show(sp.exp(z1)*sp.exp(z2b),            "exp(z1)*exp(z2b)")
show((z1**2*z2b)*(z1*z2b**3),           "(z1^2 z2b)*(z1 z2b^3)")
print("-"*108)
print("SUM layering (superpose two DISTINCT fields) -> emerges:")
show(z1 + z2b,                          "z1 + z2b")
show(sp.exp(z1) + sp.exp(z2b),          "exp(z1) + exp(z2b)")
show(z1*z2b + 1,                        "z1*z2b + 1")
print("-"*108)
print("TRAP: one field + its own reflection (z + zbar):")
ex = z + zb
print(f"  z + zb : full_conj invariant = {sp.simplify(full_conj(ex)-ex)==0}  -> REAL_TRAPPED (=2 Re z, wall)")
print("-"*108)
print("INTERFERENCE: mixing amplitude a tunes the weight, a=0 decouples:")
show(z1 + a*z2b,                        "z1 + a*z2b")
print("="*108)
print("READ: product->wall ; sum of two distinct fields->emerges ; one-field self-sum->real-trapped.")
print("The cross-coupling needs NO explicit g -- additive superposition of two distinct channels suffices.")
