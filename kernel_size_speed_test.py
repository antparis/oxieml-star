#!/usr/bin/env python3
"""SIZE vs SPEED disparity test (#047 candidate): Anthony's foam question
isolated -- do disparate SIZES (weights) do the same work as disparate
SPEEDS (winding frequencies)? The parameter every choir since #041 held
fixed: weights were (near-)equal; only speeds were ever disparate.

Auditor predictions announced before code (falsifiable):
 A. SIZES ALONE (all speeds equal): contrast EXACTLY ZERO -- algebraic:
    a single common frequency makes the sum one fixed-length needle,
    |sum| constant. Size disparity alone can write NOTHING.
 B. SPEEDS ALONE (equal sizes): the known #046 reference (0.05080 at
    N=64, log-uniform delta in [0.3,30], roughness window).
 C. BOTH, UNCORRELATED (random sizes on the same speed grid): modest
    effect -- weights only reshape the EFFECTIVE speed distribution
    (second order vs the shape itself).
 D. BOTH, CORRELATED (Anthony's foam: big-slow w~1/nu, and the reverse
    w~nu): prediction via the #046 collective law: BOTH correlation
    signs RAISE the floor vs equal weights -- any correlation
    concentrates effective weight (more dominated distribution).
 E. RECIPROCAL (nu_k = 0): exactly constant, every variant.
Roughness window (u <= 5.3), the #046 object. No verdict hardcoded.
Authority: Anthony's machine.
"""
import numpy as np

KAPPA = 0.2
U = np.linspace(0.05, 5.3, 40000)
nu_of = lambda d: KAPPA / (2.0 * d)

def contrast(nus, wts):
    v = np.abs(sum(w * np.exp(1j * nv * U) for w, nv in zip(wts, nus)))
    hi, lo = float(np.max(v)), float(np.min(v))
    return (hi - lo) / (hi + lo) if hi + lo > 0 else 0.0

N = 64
ds = np.geomspace(0.3, 30.0, N)
nus = np.array([nu_of(d) for d in ds])
rng = np.random.default_rng(20260709)
w_rand = rng.uniform(0.2, 1.8, N)

print("=" * 74)
print("A. SIZES ALONE: disparate weights, ALL speeds equal (nu = nu_mid)")
nu_mid = float(np.median(nus))
c = contrast([nu_mid] * N, w_rand)
print(f"   random weights [0.2,1.8], single speed: contrast = {c:.2e}")
print(f"   (prediction: EXACTLY zero -- one needle, fixed length)")

print("=" * 74)
print("B. SPEEDS ALONE: equal weights on the log-uniform grid (reference)")
c_ref = contrast(nus, np.ones(N))
print(f"   equal weights: contrast = {c_ref:.5f}   (#046 reference 0.05080)")

print("=" * 74)
print("C. BOTH, UNCORRELATED: random weights on the same speed grid")
cs = []
for seed in [1, 2, 3]:
    w = np.random.default_rng(seed).uniform(0.2, 1.8, N)
    cs.append(contrast(nus, w))
print(f"   3 random draws: contrast = " + " / ".join(f"{c:.5f}" for c in cs)
      + f"   (reference {c_ref:.5f})")

print("=" * 74)
print("D. BOTH, CORRELATED (the foam): w ~ 1/nu (big-slow) and w ~ nu")
w_bigslow = (1.0 / nus); w_bigslow *= N / w_bigslow.sum()
w_bigfast = nus.copy();  w_bigfast *= N / w_bigfast.sum()
c_bs = contrast(nus, w_bigslow)
c_bf = contrast(nus, w_bigfast)
print(f"   w ~ 1/nu (big bubbles slow): contrast = {c_bs:.5f}"
      f"   ratio vs equal = {c_bs/c_ref:.2f}")
print(f"   w ~ nu   (big bubbles fast): contrast = {c_bf:.5f}"
      f"   ratio vs equal = {c_bf/c_ref:.2f}")
print("   (prediction: BOTH raise the floor -- correlation concentrates")
print("    effective weight = more dominated distribution, #046 law)")

print("=" * 74)
print("E. RECIPROCAL CONTROL (nu_k = 0), disparate weights")
v0 = np.abs(np.sum(w_rand) * np.exp(1j * 0.0 * U))
print(f"   max - min = {float(np.max(v0) - np.min(v0)):.2e}   (expected 0)")

print("=" * 74)
print("READING (computed above, no prior):")
print(" 1. A: sizes alone write nothing (if ~0) -- speed disparity is the")
print("    ONLY pen; size disparity has no pen of its own.")
print(" 2. C: uncorrelated sizes only modulate (second order).")
print(" 3. D: correlated sizes reshape the EFFECTIVE speed distribution;")
print("    the direction of the shift tests the #046 collective law from")
print("    a new angle (concentration -> higher floor).")
print(" 4. E: reciprocal flat -- one-way only, as always.")
print("STATUS: completes the isolation of Anthony's foam image: bubble")
print("SIZE vs bubble SPEED, separated then correlated. Pure mathematics")
print("of OUR object; says nothing about nature or real foams.")
