#!/usr/bin/env python3
"""
fractal_highres.py -- (a) test if the anti-vs-holo dimension gap is a REAL LAW or a
resolution artefact, across exponents 2..5 and multiple resolutions; (b) generate
images of the new mixed asymmetric fractals.

WHY MULTI-RESOLUTION: at 400px the exp2 gap was +0.068, at 800px it dropped to +0.034.
A gap that shrinks toward 0 with resolution = ARTEFACT. A gap that stabilizes at a
positive value = real law. We must see the trend before claiming anything.

DISCIPLINE: no claim of "anti thickens the boundary" unless the gap stays positive AND
stable across resolutions AND across exponents. Otherwise it is traced as an artefact.

LITERATURE (2026-06-21 research): asymmetric mixed z^a+conj(z)^b+c (a!=b) appear
UNEXPLORED. Escape radius for non-holomorphic maps is NOT the usual 2 -> use R=50.

Output: fractal_highres_dims.txt (the dimension table) + PNG images in fractal_images/.
Run detached:  setsid nohup python3 -u fractal_highres.py > fractal_highres.log 2>&1 &
"""
import numpy as np
import os

OUTDIR = "fractal_images"
os.makedirs(OUTDIR, exist_ok=True)


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


def dimension(img, sizes=(2, 3, 4, 6, 8, 12, 16, 24, 32, 48)):
    edge = (np.abs(np.diff(img.astype(float), axis=0))[:, :-1] +
            np.abs(np.diff(img.astype(float), axis=1))[:-1, :]) > 0
    def bc(Z, k):
        S = np.add.reduceat(np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                            np.arange(0, Z.shape[1], k), axis=1)
        return np.count_nonzero(S)
    counts = np.array([bc(edge, k) for k in sizes]); valid = counts > 0
    s = np.array(sizes)[valid]; c = counts[valid]
    coeffs = np.polyfit(np.log(s), np.log(c), 1)
    fit = np.polyval(coeffs, np.log(s)); resid = float(np.std(np.log(c) - fit))
    return -coeffs[0], resid


# ---- (a) dimension law: holo vs anti, exponents 2..5, multiple resolutions ----
BOX = (-2.2, 1.6, -1.9, 1.9)
holo = {d: (lambda z, c, d=d: z**d + c) for d in range(2, 6)}
anti = {d: (lambda z, c, d=d: np.conj(z)**d + c) for d in range(2, 6)}
RES = [400, 800, 1200]

lines = []
lines.append("DIMENSION LAW TEST: anti-holo gap vs resolution and exponent")
lines.append("(gap shrinking to 0 with resolution = artefact; stable positive = law)")
lines.append("")
for d in range(2, 6):
    lines.append(f"exponent d={d}:")
    for W in RES:
        iH = fractal(holo[d], BOX, W, W, 200)
        iA = fractal(anti[d], BOX, W, W, 200)
        dH, rH = dimension(iH); dA, rA = dimension(iA)
        lines.append(f"  res={W:>4}: holo={dH:.4f} anti={dA:.4f} gap={dA-dH:+.4f} "
                     f"(resid h={rH:.3f} a={rA:.3f})")
    lines.append("")
report = "\n".join(lines)
print(report)
open("fractal_highres_dims.txt", "w").write(report)
print("[saved] fractal_highres_dims.txt")

# ---- (b) images of the NEW mixed asymmetric fractals ----
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    NEW = [
        ("mandelbrot_z2",   lambda z, c: z**2 + c,                (-2.2, 1.2, -1.7, 1.7)),
        ("tricorn_zbar2",   lambda z, c: np.conj(z)**2 + c,       (-2.2, 1.2, -1.7, 1.7)),
        ("mixed_z2_zbar1",  lambda z, c: z**2 + np.conj(z) + c,   (-2.4, 1.6, -2.0, 2.0)),
        ("mixed_z3_zbar2",  lambda z, c: z**3 + np.conj(z)**2 + c,(-1.9, 1.9, -1.9, 1.9)),
        ("mixed_z4_zbar1",  lambda z, c: z**4 + np.conj(z) + c,   (-1.7, 1.7, -1.7, 1.7)),
        ("mixed_z3_zbar1",  lambda z, c: z**3 + np.conj(z) + c,   (-1.8, 1.8, -1.8, 1.8)),
    ]
    for name, f, box in NEW:
        img = fractal(f, box, 1000, 1000, 250)
        plt.figure(figsize=(6, 6))
        plt.imshow(img, cmap="twilight_shifted", extent=box, origin="lower")
        plt.title(name); plt.axis("off")
        path = os.path.join(OUTDIR, f"{name}.png")
        plt.savefig(path, dpi=130, bbox_inches="tight"); plt.close()
        print(f"[image] {path}")
    print("[done] images in", OUTDIR)
except Exception as e:
    print(f"[image error] {type(e).__name__}: {e} -- dimension table still saved.")
