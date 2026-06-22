#!/usr/bin/env python3
"""
fractal_parity_law.py -- Resolve the (5,3) anomaly: mirror symmetry of mixed anti
fractals z^a+conj(z)^b+c is governed by the PARITY of the anti exponent b, NOT by a-b.
And anti-holomorphy (judge) is DECOUPLED from geometric mirror symmetry.

Two parts, both on YOUR machine:
(1) judge_v2 confirms z^5+conj(z)^3 (and neighbors) are genuinely ANTI (the conj^3 does
    NOT reduce) -- so the anomaly is real: an authentically anti object can be fully
    mirror-symmetric.
(2) parity sweep over 12 pairs: does imag-axis mirror symmetry =1.000 track b odd?
    Sandbox finding: b odd -> symmetric (~1.000); b even -> broken (<0.97).

DISCIPLINE: mirror symmetries are EXACT array flips (reliable). Judge is the authority
on anti. If b=3 cases sit at ~0.95 (not 1.000), note them as intermediate to confirm at
higher resolution. Escape radius R=50.

Run from ~/Desktop/oxieml-star/ :  python3 fractal_parity_law.py
"""
import numpy as np
from judge_v2 import z as zS, zbar as zbarS, certify_1field


def _verdict(expr):
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def fractal(f_next, box, W, H, maxit, R=50.0):
    xmin, xmax, ymin, ymax = box
    xs = np.linspace(xmin, xmax, W); ys = np.linspace(ymin, ymax, H)
    C = xs[None, :] + 1j*ys[:, None]; Z = np.zeros_like(C)
    out = np.full(C.shape, maxit, dtype=int); alive = np.ones(C.shape, bool)
    for i in range(maxit):
        Z[alive] = f_next(Z[alive], C[alive])
        esc = alive & (np.abs(Z) > R); out[esc] = i; alive &= ~esc
        if not alive.any(): break
    return out


def mirrors(img):
    ins = (img == img.max())
    return (np.mean(ins == ins[::-1, :]), np.mean(ins == ins[:, ::-1]),
            np.mean(ins == ins[::-1, ::-1]))


BOX = (-1.9, 1.9, -1.9, 1.9)

print("=" * 70)
print("PART 1 -- judge_v2: is the anomaly z^5+conj(z)^3 genuinely anti?")
print("=" * 70)
for a, b in [(5, 3), (4, 2), (3, 2), (5, 2), (3, 1), (5, 1)]:
    v = _verdict(zS**a + zbarS**b)
    print(f"  z^{a}+zbar^{b:<2} -> {v}")

print("\n" + "=" * 70)
print("PART 2 -- parity sweep: does mirror symmetry track parity of b?")
print("=" * 70)
print(f"{'(a,b)':>7} {'b parity':>9} {'im_sym':>8} {'verdict':>10}")
print("-" * 70)
TESTS = [(5, 3), (4, 2), (3, 2), (5, 2), (4, 3), (5, 4),
         (3, 1), (4, 1), (5, 1), (6, 2), (6, 3), (7, 3)]
rows = []
for a, b in TESTS:
    img = fractal(lambda z, c, a=a, b=b: z**a + np.conj(z)**b + c, BOX, 700, 700, 220)
    m = mirrors(img)
    bp = "odd" if b % 2 else "even"
    sym = "SYM" if m[1] > 0.99 else ("broken" if m[1] < 0.97 else "~mid")
    rows.append((a, b, bp, m[1], sym))
    print(f"  ({a},{b}) {bp:>9} {m[1]:>8.3f} {sym:>10}")
print("-" * 70)
odd_syms = [r[3] for r in rows if r[2] == "odd"]
even_syms = [r[3] for r in rows if r[2] == "even"]
print(f"b ODD  im_sym: min={min(odd_syms):.3f} (should be high, near 1.000)")
print(f"b EVEN im_sym: max={max(even_syms):.3f} (should be lower, broken)")
print(">>> If b-odd are all high and b-even all broken: LAW = mirror symmetry tracks")
print("    parity of anti exponent b. Anti-holomorphy (judge) DECOUPLED from symmetry.")
