#!/usr/bin/env python3
"""
fractal_compass.py -- The "compass": does anti-holomorphy leave a measurable
GEOMETRIC fingerprint in mixed holomorphic/anti-holomorphic fractals?

For each fractal it confronts TWO verdicts:
  - the JUDGE (judge_v2) on the iteration formula: holo / anti / module / real-trapped
  - the GEOMETRY of the generated set: symmetries + fractal dimension of the boundary
If "judge=anti" systematically matches a distinct geometric signature, we have linked
the algebra (judge) to the geometry (image).

LITERATURE STATUS (research 2026-06-21): the SYMMETRIC z^2+zbar^2+c and the pure
anti conj(z)^d+c are known (Tricorn/Multicorn). The ASYMMETRIC mixed cases
z^a + conj(z)^b + c with a != b appear UNEXPLORED (no dedicated study, no name).
Those [NEW] rows are the interesting territory.

DISCIPLINE: low-res dimension is an [INDICE], not a result. A persistent gap across
higher resolution is needed before claiming "anti thickens the boundary".

Run from ~/Desktop/oxieml-star/ :  python3 fractal_compass.py
"""
import numpy as np
from judge_v2 import z as zS, zbar as zbarS, certify_1field


def _verdict(expr):
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def fractal(f_next, box, W=400, H=400, maxit=80, R=10.0):
    xmin, xmax, ymin, ymax = box
    xs = np.linspace(xmin, xmax, W); ys = np.linspace(ymin, ymax, H)
    C = xs[None, :] + 1j*ys[:, None]; Z = np.zeros_like(C)
    out = np.full(C.shape, maxit, dtype=int); alive = np.ones(C.shape, bool)
    for i in range(maxit):
        Z[alive] = f_next(Z[alive], C[alive])
        esc = alive & (np.abs(Z) > R); out[esc] = i; alive &= ~esc
        if not alive.any(): break
    return out


def measure(img):
    inside = (img == img.max())
    sym_real = np.mean(inside == inside[::-1, :])
    sym_imag = np.mean(inside == inside[:, ::-1])
    sym_rot180 = np.mean(inside == inside[::-1, ::-1])
    edge = (np.abs(np.diff(img.astype(float), axis=0))[:, :-1] +
            np.abs(np.diff(img.astype(float), axis=1))[:-1, :]) > 0
    def boxcount(Zb, k):
        S = np.add.reduceat(np.add.reduceat(Zb, np.arange(0, Zb.shape[0], k), axis=0),
                            np.arange(0, Zb.shape[1], k), axis=1)
        return np.count_nonzero(S)
    sizes = [2, 4, 8, 16, 32]; counts = np.array([boxcount(edge, k) for k in sizes])
    valid = counts > 0
    dim = (-np.polyfit(np.log(np.array(sizes)[valid]), np.log(counts[valid]), 1)[0]
           if valid.sum() >= 2 else float('nan'))
    return sym_real, sym_imag, sym_rot180, dim


CASES = [
    ("Mandelbrot z^2+c",        zS**2,            lambda z, c: z**2+c,              (-2.2, 1.2, -1.7, 1.7)),
    ("Tricorn zbar^2+c",        zbarS**2,         lambda z, c: np.conj(z)**2+c,     (-2.2, 1.2, -1.7, 1.7)),
    ("z^3+c",                   zS**3,            lambda z, c: z**3+c,              (-1.6, 1.6, -1.6, 1.6)),
    ("zbar^3+c Multicorn",      zbarS**3,         lambda z, c: np.conj(z)**3+c,     (-1.6, 1.6, -1.6, 1.6)),
    ("MIXED z^2+zbar+c [NEW]",  zS**2+zbarS,      lambda z, c: z**2+np.conj(z)+c,   (-2.2, 1.5, -1.8, 1.8)),
    ("MIXED z^3+zbar^2+c [NEW]",zS**3+zbarS**2,   lambda z, c: z**3+np.conj(z)**2+c,(-1.8, 1.8, -1.8, 1.8)),
    ("MIXED z^2+zbar^2+c",      zS**2+zbarS**2,   lambda z, c: z**2+np.conj(z)**2+c,(-1.8, 1.8, -1.8, 1.8)),
]

print("=" * 92)
print(f"{'fractal':<26}{'judge':<16}{'sym_re':>7}{'sym_im':>7}{'rot180':>7}{'dim_frac':>9}")
print("-" * 92)
rows = []
for name, fsym, fnum, box in CASES:
    v = _verdict(fsym)
    img = fractal(fnum, box, W=400, H=400, maxit=80)
    sr, si, sR, dim = measure(img)
    rows.append((name, v, dim))
    print(f"{name:<26}{v:<16}{sr:>7.3f}{si:>7.3f}{sR:>7.3f}{dim:>9.3f}")
print("=" * 92)
# pair comparison: anti vs holo at equal exponent
print("Pairwise dim (anti minus holo at equal exponent):")
d = {n: dm for n, vv, dm in rows}
print(f"  exp2: Tricorn - Mandelbrot = {d['Tricorn zbar^2+c'] - d['Mandelbrot z^2+c']:+.3f}")
print(f"  exp3: Multicorn - z^3      = {d['zbar^3+c Multicorn'] - d['z^3+c']:+.3f}")
print(">>> If anti-minus-holo is consistently POSITIVE, anti may thicken the boundary.")
print(">>> [INDICE] at this resolution. Confirm at higher res before any claim.")
