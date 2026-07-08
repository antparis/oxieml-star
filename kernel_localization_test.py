#!/usr/bin/env python3
"""N detuned chiral tears (#041 candidate, v2): conflict, cancellation,
EMERGENT LOCALIZATION along the cut, and the N-behaviour -- with THREE
independent estimators (orthogonal-axis correction after the v1 sandbox
failure: a thresholdless extrema counter mistook 1e-17 rounding noise for
structure and missed monotone contrast).

Pure mathematics: no time, no data, no physical constants. Extends #039
(intrinsic emergent boundary) and #040 (chiral tear: jump phase rotates
along the cut as x^(-c); reciprocal control frozen at +90 deg).

Scenarios:
 S1 CONFLICT: exact global cancellation (identical offsets, opposite
    weights) vs progressive detuning. Widened window, edge-excluded:
    is the dip a true INTERIOR localized zero or a border artefact?
 S2 LOCALIZATION, three estimators on the normalized profile
    P(x) = |sum_k w_k x^(-(1+c_k))| * x  (trivial 1/x envelope removed):
    (a) CONTRAST above numerical floor; (b) extrema WITH noise threshold;
    (c) dip position/depth as offsets rotate -- does "the place" move in a
    controlled way (motion capture: points command the silhouette)?
 S3 N-BEHAVIOUR (v1 surprise: contrast DECREASED with N, 0.099 -> 0.024):
    disentangle N at FIXED spread vs spread at FIXED N. Hypotheses:
    phase averaging (blur, ~1/sqrt(N)?) vs grid artefact.
 S4 RECIPROCAL CONTROL: all offsets real -> expected flat at machine zero
    on all three estimators. The differential IS the result.

Route (validated #039/#040): disc Phi(x,2,a) = 2*pi*i x^(-a) ln(x),
machine-exact on the a=1 dilog control. Common envelope 2*pi*ln(x)/x is
divided out everywhere below (it multiplies every tear identically).
No verdict hardcoded. Authority: THIS execution on Anthony's machine.
"""
import numpy as np

KAPPA = 0.2
c_of = lambda delta: -1j * KAPPA / (2.0 * delta)

# window: interior of the cut, edges excluded from all searches
XS = np.geomspace(1.05, 200.0, 1200)
EDGE = 25                                  # exclude this many points per side
NOISE = 1e-12                              # numerical floor for structure

def prof(weights, offsets):
    """Normalized profile P(x) = |sum w_k x^(-(1+c_k))| * x on XS."""
    s = np.zeros_like(XS, dtype=complex)
    for w, c in zip(weights, offsets):
        s += w * XS.astype(complex) ** (-(1.0 + c))
    return np.abs(s) * XS

def contrast(v):
    hi, lo = float(np.max(v)), float(np.min(v))
    return (hi - lo) / (hi + lo) if hi + lo > 0 else 0.0

def extrema_thresholded(v, rel=1e-6):
    """Interior extrema whose prominence exceeds rel * max(v)."""
    thr = rel * float(np.max(v))
    idx = []
    for i in range(1 + EDGE, len(v) - 1 - EDGE):
        if (v[i] - v[i-1]) * (v[i+1] - v[i]) < 0:
            left = np.max(np.abs(v[max(0, i-40):i] - v[i]))
            right = np.max(np.abs(v[i+1:i+41] - v[i]))
            if min(left, right) > thr:
                idx.append(i)
    return idx

print("=" * 74)
print("S1. CONFLICT: exact cancel vs detuned dip (interior, edge-excluded)")
c1 = c_of(1.0)
v = prof([1, -1], [c1, c1])
print(f"  identical offsets, w=(+1,-1): max|P| over window = {float(np.max(v)):.2e}"
      f"  (exact global cancel at machine zero)")
for eps in [0.01, 0.1, 0.5, 2.0]:
    c2 = c_of(1.0 + eps)
    v = prof([1, -1], [c1, c2])
    interior = v[EDGE:-EDGE]
    imin = int(np.argmin(interior)) + EDGE
    at_edge = (imin <= EDGE + 2) or (imin >= len(v) - EDGE - 3)
    print(f"  detune eps={eps:4.2f}: min|P|={float(v[imin]):.3e} at x={XS[imin]:8.2f}"
          f"   max|P|={float(np.max(v)):.3e}   dip-at-edge: {at_edge}")
print("  reading: exact cancellation = measure-zero tuning (c1=c2, w2=-w1);")
print("  detuning breaks it; WHERE the residual dip sits is printed above.")

print("=" * 74)
print("S2. LOCALIZATION: three estimators, one-way pair (delta=1 vs 3)")
c2 = c_of(3.0)
v = prof([1, 1], [c1, c2])
ext = extrema_thresholded(v)
print(f"  (a) contrast = {contrast(v):.6f}   (floor {NOISE:.0e})")
print(f"  (b) thresholded interior extrema = {len(ext)}"
      + (f" at x={[round(float(XS[i]),2) for i in ext[:6]]}" if ext else ""))
print("  (c) dip steering: rotate the second tear's offset scale")
for d2 in [2.0, 3.0, 6.0, 12.0]:
    v = prof([1, 1], [c1, c_of(d2)])
    interior = v[EDGE:-EDGE]
    imin = int(np.argmin(interior)) + EDGE
    print(f"      delta2={d2:5.1f}: dip at x={XS[imin]:8.2f}"
          f"   depth={float(v[imin]):.4f}   contrast={contrast(v):.4f}")
print("  reading: if the dip position moves monotonically with delta2, the")
print("  offsets STEER the place -- motion capture confirmed at pair level.")

print("=" * 74)
print("S3. N-BEHAVIOUR: N at fixed spread vs spread at fixed N (one-way)")
print("  (i) fixed spread delta in [0.3, 30], N grows:")
for N in [2, 3, 5, 20, 80, 200]:
    offs = [c_of(d) for d in np.geomspace(0.3, 30.0, N)]
    v = prof([1] * N, offs)
    print(f"    N={N:4d}: contrast={contrast(v):.4f}"
          f"   extrema={len(extrema_thresholded(v))}")
print("  (ii) fixed N=20, spread grows (delta in [1/S, S]):")
for S in [2.0, 5.0, 30.0, 200.0]:
    offs = [c_of(d) for d in np.geomspace(1.0/S, S, 20)]
    v = prof([1] * 20, offs)
    print(f"    S={S:6.1f}: contrast={contrast(v):.4f}"
          f"   extrema={len(extrema_thresholded(v))}")
print("  reading: separates 'more tears' from 'wider detuning' -- which one")
print("  builds structure and which one blurs it is decided by the numbers.")

print("=" * 74)
print("S4. RECIPROCAL CONTROL: all offsets real, varied weights")
for N in [2, 20, 200]:
    wts = list(np.linspace(0.5, 1.5, N))
    v = prof(wts, [0.0] * N)
    print(f"  N={N:4d} (recip): contrast={contrast(v):.2e}"
          f"   extrema={len(extrema_thresholded(v))}"
          f"   (expected: machine-zero contrast, 0 extrema)")

print("=" * 74)
print("READING (computed above, no prior):")
print(" 1. S1: exact cancellation is fine-tuned (measure-zero); detuning")
print("    leaves a residual dip whose interior/edge nature is printed.")
print(" 2. S2: localization measured by CONTRAST (not raw extrema); the")
print("    dip position steered by the offset scale = the network commands")
print("    the place (motion capture) -- if the printed positions move.")
print(" 3. S3: N and spread disentangled; growth = structure, decay = blur.")
print(" 4. S4: reciprocal control flat at machine zero -> any structure in")
print("    S2/S3 is a ONE-WAY phenomenon (phase winding is the only source).")
print("STATUS: pure mathematics of OUR object; extends #039/#040; says")
print("nothing about nature, space, or physical localization. Shared FORM,")
print("never identity.")
