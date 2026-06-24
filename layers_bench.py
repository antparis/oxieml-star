#!/usr/bin/env python3
"""layers_bench.py -- emergence by superposition (orthogonal-axis bench, M-IV).

Question: can a target-type cross-coupling appear by stacking factorized layers?
Answer: it depends, and the bench is now honest about what is ALGEBRAIC vs PHYSICAL.

WHAT IS ALGEBRAICALLY DECIDABLE (this bench):
  (1) NON-FACTORIZABLE: d = d_z1 d_z2b log f != 0  (cross discriminant). Robust.
  (2) EXPLICIT pairing: a separated form with COMPLEX conjugate coefficients
      (alpha*u(z1) + conj(alpha)*u(z2b)) is full_conj-invariant -> REAL_TRAPPED. Robust.

WHAT IS NOT ALGEBRAICALLY DECIDABLE (corrected 2026-06-24, after f644663):
  For two DISTINCT fields, the full_conj swap z1<->z2b is NOT the reality involution: it
  identifies z2b as conj(z1), valid only for ONE field. The true involution sends z1->conj(z1)
  and z2b->z2 (variables absent from the form). So whether z1+z2b is real-trapped or a genuine
  crossing is a PHYSICAL question (are the two channels reality-related?), NOT readable from the
  symbolic form. Earlier version wrongly swapped z1<->z2b universally and mislabeled z1+z2b.

VERDICTS (two distinct fields z1, z2b):
  d == 0                                  -> WALL (factorizes)
  d != 0, full_conj-invariant, has I      -> WALL (real-trapped: explicit conjugate coefficients)
  d != 0, full_conj-invariant, no I       -> PHYSICAL (non-factorizable; pairing is a physical question)
  d != 0, NOT full_conj-invariant         -> CANDIDATE (non-factorizable AND not explicitly paired)
ONE field (z, zb): full_conj z<->zb is the true involution; z+zb -> REAL_TRAPPED.

The full_conj swap is valid for ONE field, and for the EXPLICIT-coefficient signature only.
Authority remains judge_v2 / nonseparable_judge / nh_lcft_pairing_judge on the machine."""
import sympy as sp
z1, z2b = sp.symbols('z1 z2b')
z, zb   = sp.symbols('z zb')
a       = sp.symbols('a')
ar, ai  = sp.symbols('ar ai', real=True)
I       = sp.I

def disc(f):
    return sp.simplify(sp.diff(sp.log(f), z1, z2b))
def fc2(f):                                # two-field swap + conjugate (I->-I)
    return f.subs({z1: z2b, z2b: z1, I: -I}, simultaneous=True)
def verdict2(f):
    d = disc(f)
    if d == 0:
        return "WALL (factorizes)"
    if sp.simplify(fc2(f) - f) == 0:
        return ("WALL (real-trapped: explicit conj coeffs)" if f.has(I)
                else "PHYSICAL (non-factorizable; pairing is physical)")
    return "CANDIDATE (non-factorizable AND not explicitly paired)"
def show(f, name):
    print(f"{name:42s} | {verdict2(f)}")

print("="*100)
print("PRODUCT layering -> factorizes -> wall:")
show(sp.exp(z1)*sp.exp(z2b),            "exp(z1)*exp(z2b)")
show((z1**2*z2b)*(z1*z2b**3),           "(z1^2 z2b)*(z1 z2b^3)")
print("-"*100)
print("SUM of two distinct fields (no explicit g) -> non-factorizable, pairing PHYSICAL:")
show(z1 + z2b,                          "z1 + z2b")
show(sp.exp(z1) + sp.exp(z2b),          "exp(z1) + exp(z2b)")
print("-"*100)
print("EXPLICIT COUPLING (anchor 20204b2, g=z1*z2b):")
show(z1*z2b + 1,                        "z1*z2b + 1")
print("-"*100)
print("REGRESSION 1 -- explicit conj-paired coeffs MUST be WALL:")
acmp = ar + I*ai
show(1 + acmp*sp.log(z1) + (ar - I*ai)*sp.log(z2b), "1 + a*log z1 + conj(a)*log z2b")
print("REGRESSION 2 -- z1+z2b MUST be PHYSICAL (not target, not wall):")
show(z1 + z2b,                          "z1 + z2b (re-check)")
print("-"*100)
print("MIXED additive argument -> not explicitly paired -> CANDIDATE:")
show(sp.log(z1 - z2b),                  "log(z1 - z2b)")
print("-"*100)
print("ONE field + its mirror (true involution z<->zb):")
ex = z + zb
inv1 = sp.simplify(ex.subs({z: zb, zb: z, I: -I}, simultaneous=True) - ex) == 0
print(f"  z + zb : full_conj(z<->zb) invariant = {inv1} -> REAL_TRAPPED (=2 Re z, wall)")
print("="*100)
print("READ: target needs d!=0 AND genuinely non-paired. Explicit conj coeffs = wall.")
print("      z1+z2b is PHYSICAL: only the physical system decides if the channels are distinct.")
