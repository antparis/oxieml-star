#!/usr/bin/env python3
"""jordan_ep_cross.py -- M-VIII minimal derivation: non-reciprocal EP Jordan block
to cross-correlator topology, with the bifurcation criterion target vs wall.

GOAL. Turn the [DERIVATION] status of the non-reciprocal exceptional point (EP) into
something the judge can certify: derive exactly (a) the Jordan block is non-diagonalizable
(Naimark lock by construction), (b) its resolvent has a DOUBLE pole, (c) its time propagator
carries a linear-t factor (LCFT log signature), then (d) show which cross-correlator TOPOLOGY
is target-type vs wall, and extract the exact physical criterion that selects the target.

KEY RESULT (the new bit): asymmetry of conformal weights is NOT enough. A product topology
log(z1)+log(z2b) factorizes -> WALL even with distinct coefficients. Only a MIXED additive
argument log(z1 - z2b) gives d_z1 d_z2b log f != 0 -> target. So the non-reciprocity must
produce a mixed argument, not merely asymmetric weights. This refines the spec.

Sandbox = indicative oracle. Authority = judge_v2 / nonseparable_judge / verify_exact on the
machine. English only."""
import sympy as sp

print("="*78)
print("PART A -- Jordan block of a non-reciprocal EP (exact algebra)")
print("="*78)
lam, g, w, t = sp.symbols('lambda g omega t')
H = sp.Matrix([[lam, g], [0, lam]])            # non-reciprocal: coupling 2->1 only
print("H =", H.tolist())
# Non-diagonalizable for g != 0: only ONE eigenvector.
evects = H.eigenvects()
n_indep = sum(len(basis) for (val, mult, basis) in evects)
print("eigenvectors (independent):", n_indep, "/ 2  -> non-diagonalizable iff 1 (Naimark lock)")
# Resolvent (wI - H)^-1 : look at the cross component (1,2) for the double pole.
R = (w*sp.eye(2) - H).inv()
R12 = sp.simplify(R[0, 1])
print("resolvent cross component R12 =", R12, " (double pole in (w-lambda))")
# Time propagator exp(-iHt): cross component carries linear-t factor.
P = sp.simplify(sp.exp(-sp.I*H*t))
P12 = sp.simplify(P[0, 1])
print("propagator cross component P12 =", P12, " (linear-t = LCFT log signature)")

print()
print("="*78)
print("PART B -- log emergence by weight degeneracy (exact LCFT mechanism)")
print("="*78)
z1, z2b, h, dh = sp.symbols('z1 z2b h dh')
# Standard LCFT log: the logarithmic partner is the h-derivative of the power correlator.
base = z1**(-2*h)
partner = sp.simplify(sp.diff(base, h))
print("d/dh [z1^(-2h)] =", partner, "  -> log partner ~ -2 log(z1)  (log is forced by degeneracy)")

print()
print("="*78)
print("PART C -- three cross topologies at the judge (cross discriminant)")
print("="*78)
def disc(f):                                   # nonseparable_judge core: d_z1 d_z2b log f
    return sp.simplify(sp.diff(sp.log(f), z1, z2b))
a, b = sp.symbols('a b')
cases = [
    ("T1 product, equal weights:  z1*z2b",                 z1*z2b),
    ("T2 product, ASYM weights:   z1**a * z2b**b",         z1**a * z2b**b),
    ("T3 mixed additive:          z1 - z2b",               z1 - z2b),
]
for name, f in cases:
    d = disc(f)
    verdict = "WALL (factorizes)" if d == 0 else "TARGET-TYPE (non-factorizable)"
    print(f"  {name:42s} | d = {str(d):22s} | {verdict}")

print()
print("="*78)
print("PART D -- verdict and refined criterion")
print("="*78)
print("EXACT (judge-certifiable): Jordan block non-diagonalizable; double-pole resolvent;")
print("  linear-t propagator; log forced by degeneracy. Cross topology:")
print("   - product (even with ASYMMETRIC weights) -> d=0 -> WALL.")
print("   - mixed additive argument log(z1 - z2b)   -> d!=0 -> TARGET-TYPE.")
print("REFINED CRITERION [DERIVATION]: the non-reciprocity must mix the two sectors into a")
print("  SINGLE additive argument (z1 - z2b). Asymmetric weights alone stay a wall. The open")
print("  physical question is whether a real non-reciprocal EP device produces the MIXED")
print("  argument (target) or only asymmetric weights (wall) -- to settle by deriving one")
print("  device's closed-form correlator and certifying it on the machine.")
