#!/usr/bin/env python3
"""
fractal_parity_confirm.py -- Confirm the parity law at high resolution on your machine.

LAW (to confirm): for mixed anti fractal z^a+conj(z)^b+c (a!=b), the imaginary-axis
mirror symmetry is PERFECT (=1.000) iff BOTH a and b are odd. If either is even, broken.

GEOMETRIC REASON: under reflection z -> -conj(z) (imag-axis mirror), z^a picks up
(-1)^a and conj(z)^b picks up (-1)^b. Both odd -> both flip sign coherently -> set
invariant. Mixed parity -> invariance broken.

The 8 cases separate "b odd" from "a AND b odd":
  a,b odd     (5,3)(7,3)(3,1)(5,1) -> expected 1.000 (SYM)
  a even,b odd(4,3)(6,3)(4,1)(6,1) -> expected < 1.000 (broken), refuting "b odd alone"

Symmetry = EXACT array flip (no interpolation, reliable). judge_v2 also confirms anti on
the 4 a,b-odd cases. Escape radius R=50. Res 1500.

Run from ~/Desktop/oxieml-star/ :  python3 fractal_parity_confirm.py
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


def im_mirror(img):
    ins = (img == img.max())
    return np.mean(ins == ins[:, ::-1])   # exact left/right flip


BOX = (-1.9, 1.9, -1.9, 1.9)
CASES = [
    (5, 3, "a,b odd"), (7, 3, "a,b odd"), (3, 1, "a,b odd"), (5, 1, "a,b odd"),
    (4, 3, "a even,b odd"), (6, 3, "a even,b odd"),
    (4, 1, "a even,b odd"), (6, 1, "a even,b odd"),
]

print("=" * 64)
print("PARITY LAW confirmation -- res 1500, exact imag-axis mirror")
print("=" * 64)
print(f"{'(a,b)':>7} {'class':>14} {'im_sym':>9} {'verdict':>9}")
print("-" * 64)
abodd, aeven = [], []
for a, b, cl in CASES:
    img = fractal(lambda z, c, a=a, b=b: z**a + np.conj(z)**b + c, BOX, 1500, 1500, 250)
    s = im_mirror(img)
    tag = "SYM" if s > 0.999 else "broken"
    (abodd if cl == "a,b odd" else aeven).append(s)
    print(f"  ({a},{b}) {cl:>14} {s:>9.4f} {tag:>9}")
print("-" * 64)
print(f"a,b ODD     : min={min(abodd):.4f}  (law predicts ~1.000)")
print(f"a even,bodd : max={max(aeven):.4f}  (law predicts < 1.000, broken)")
gap = min(abodd) - max(aeven)
print(f"separation (min_abodd - max_aeven) = {gap:+.4f}  ({'CLEAN' if gap > 0 else 'OVERLAP'})")

print("\n-- judge_v2 on the 4 a,b-odd cases (must be anti) --")
for a, b in [(5, 3), (7, 3), (3, 1), (5, 1)]:
    print(f"  z^{a}+zbar^{b} -> {_verdict(zS**a + zbarS**b)}")
print("\n>>> CLEAN separation + anti verdicts => LAW established: a AND b odd <=> perfect")
print("    mirror symmetry; anti-holomorphy DECOUPLED from geometric symmetry.")
