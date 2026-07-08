#!/usr/bin/env python3
"""Position steering of the tear relief (#042 candidate): can a richer
choir MOVE the interference features along the cut -- full motion capture?
Plus the blur law (contrast decay with N at fixed spread).

Pure mathematics: no time, no data, no physical constants. Extends #041
(relief from detuning; at pair level the network commands DEPTH, not
position: the dip stayed frozen at x=179.26 under all detunings).

Panels (auditor predictions announced before code, falsifiable):
 A. WEIGHT LEVER: N=3 tears, fixed offsets (spread scales), vary RELATIVE
    real weights. Prediction: the main dip position moves, but modestly
    (bounded range) -- weights shift the interference balance point.
 B. PHASE LEVER (the true motion-capture handle, new vs #041): give each
    tear a COMPLEX weight w_k = |w| e^{i phi_k} (an initial phase, not
    only an amplitude). Rotating phi_k should SLIDE the destructive-
    meeting points of the windings along the cut. Prediction: clean
    steering, potentially across the whole window.
 C. BLUR LAW: at fixed spread, contrast decayed with N in #041
    (0.218 -> 0.049). Measure the exponent: contrast ~ N^(-p).
    Prediction: p ~ 0.5 (incoherent phase averaging, 1/sqrt(N)) --
    which would independently rejoin accumulation law #008
    (coherent ~N, random ~sqrt(N)).
 D. RECIPROCAL CONTROL: complex weights but REAL offsets (a_k = 1).
    Prediction: complex weights alone give a CONSTANT profile in x
    (nothing rotates along the cut -> no structure to steer); the
    one-way/reciprocal differential stays sharp.

Method (v2 lessons kept): normalized profile P(x)=|sum w_k x^(-(1+c_k))|*x,
noise floor, edge exclusion, contrast + thresholded extrema + dip position
as estimators. No verdict hardcoded. Authority: Anthony's machine.
"""
import numpy as np

KAPPA = 0.2
c_of = lambda d: -1j * KAPPA / (2.0 * d)
XS = np.geomspace(1.05, 200.0, 1200)
EDGE = 25

def prof(weights, offsets):
    s = np.zeros_like(XS, dtype=complex)
    for w, c in zip(weights, offsets):
        s += w * XS.astype(complex) ** (-(1.0 + c))
    return np.abs(s) * XS

def contrast(v):
    hi, lo = float(np.max(v)), float(np.min(v))
    return (hi - lo) / (hi + lo) if hi + lo > 0 else 0.0

def dip_x(v):
    interior = v[EDGE:-EDGE]
    return float(XS[int(np.argmin(interior)) + EDGE])

def extrema_thresholded(v, rel=1e-6):
    thr = rel * float(np.max(v))
    n = 0
    for i in range(1 + EDGE, len(v) - 1 - EDGE):
        if (v[i] - v[i-1]) * (v[i+1] - v[i]) < 0:
            left = np.max(np.abs(v[max(0, i-40):i] - v[i]))
            right = np.max(np.abs(v[i+1:i+41] - v[i]))
            if min(left, right) > thr:
                n += 1
    return n

OFFS3 = [c_of(d) for d in (0.3, 3.0, 30.0)]   # N=3, wide spread (S=10 style)

print("=" * 74)
print("A. WEIGHT LEVER (real weights, N=3, offsets delta=0.3/3/30)")
print("   w2 varies, w1=w3=1: dip position and contrast")
for w2 in [0.25, 0.5, 1.0, 2.0, 4.0]:
    v = prof([1.0, w2, 1.0], OFFS3)
    print(f"   w2={w2:5.2f}: dip at x={dip_x(v):8.2f}   contrast={contrast(v):.4f}"
          f"   extrema={extrema_thresholded(v)}")

print("=" * 74)
print("B. PHASE LEVER (complex weights: w2 = e^{i*phi}, N=3, same offsets)")
for phi_deg in [0, 45, 90, 135, 180, 270]:
    phi = np.deg2rad(phi_deg)
    v = prof([1.0, np.exp(1j * phi), 1.0], OFFS3)
    print(f"   phi={phi_deg:4d} deg: dip at x={dip_x(v):8.2f}"
          f"   contrast={contrast(v):.4f}   extrema={extrema_thresholded(v)}")
print("   reading: if dip position sweeps with phi, the PHASES steer the")
print("   place -- full motion capture; if frozen, the relief is anchored.")

print("=" * 74)
print("C. BLUR LAW: contrast vs N at fixed spread (delta in [0.3,30]), fit p")
Ns, Cs = [], []
for N in [2, 4, 8, 16, 32, 64, 128, 256]:
    offs = [c_of(d) for d in np.geomspace(0.3, 30.0, N)]
    v = prof([1.0] * N, offs)
    Ns.append(N); Cs.append(contrast(v))
    print(f"   N={N:4d}: contrast={Cs[-1]:.5f}")
# power-law fit on the decaying tail (N>=8)
ln = np.log(np.array(Ns[2:], float)); lc = np.log(np.array(Cs[2:], float))
p = -np.polyfit(ln, lc, 1)[0]
print(f"   fitted exponent (N>=8): contrast ~ N^(-p), p = {p:.3f}")
print(f"   prediction was p ~ 0.5 (incoherent 1/sqrt(N)); verdict printed above.")

print("=" * 74)
print("D. RECIPROCAL CONTROL: complex weights, REAL offsets (a_k = 1)")
for phi_deg in [0, 90, 180]:
    phi = np.deg2rad(phi_deg)
    v = prof([1.0, np.exp(1j * phi), 1.0], [0.0, 0.0, 0.0])
    print(f"   phi={phi_deg:4d} deg: contrast={contrast(v):.2e}"
          f"   extrema={extrema_thresholded(v)}   (expected: machine-flat)")

print("=" * 74)
print("READING (computed above, no prior):")
print(" 1. A: real weights move the dip (range printed) -- balance lever.")
print(" 2. B: complex phases -- steering verdict read from the dip sweep.")
print(" 3. C: blur exponent p printed; p~0.5 would independently rejoin")
print("    accumulation law #008 (coherent ~N vs random ~sqrt(N)).")
print(" 4. D: reciprocal control flat -> steering, if any, is ONE-WAY only.")
print("STATUS: pure mathematics of OUR object; extends #041; says nothing")
print("about nature, space, or physical localization. Shared FORM, never")
print("identity.")
