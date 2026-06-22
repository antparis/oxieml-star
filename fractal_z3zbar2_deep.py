#!/usr/bin/env python3
"""
fractal_z3zbar2_deep.py -- Decisive test on the best candidate z^3 + conj(z)^2 + c
(mixed asymmetric, anti-holomorphic, apparently UNEXPLORED in the literature).

GOAL (two questions):
(a) DIMENSION LAW: is the anti-vs-holo boundary-dimension gap a REAL LAW or a
    resolution artefact? Measure z^3 (holo witness) vs z^3+conj(z)^2 (anti) at
    1000..3000 px. Gap shrinking to 0 = artefact; stabilizing positive = law.
(b) SYMMETRY: characterize the EXACT symmetry. Preliminary (1000px): z^3 is fully
    symmetric (real axis, imag axis, rot180 all = 1.0); z^3+conj(z)^2 keeps the
    REAL-axis symmetry but BREAKS imag-axis and rot180 (~0.93). The anti term leaves
    a measurable symmetry fingerprint.

DISCIPLINE: a law is claimed only if the gap stays positive AND stabilizes across
resolutions. Escape radius R=50 (non-holomorphic maps don't obey the usual R=2).

Output: fractal_z3zbar2_deep.txt (progressive). Run detached:
  setsid nohup python3 -u fractal_z3zbar2_deep.py > fractal_z3zbar2_deep.log 2>&1 &
"""
import numpy as np

BOX = (-1.9, 1.9, -1.9, 1.9)   # square, centered -> clean symmetry measures
RES = [1000, 1500, 2000, 2500, 3000]
MAXIT = 250
holo = lambda z, c: z**3 + c
anti = lambda z, c: z**3 + np.conj(z)**2 + c


def fractal(f_next, W, H, maxit, R=50.0):
    xmin, xmax, ymin, ymax = BOX
    xs = np.linspace(xmin, xmax, W); ys = np.linspace(ymin, ymax, H)
    C = xs[None, :] + 1j*ys[:, None]; Z = np.zeros_like(C)
    out = np.full(C.shape, maxit, dtype=int); alive = np.ones(C.shape, bool)
    for i in range(maxit):
        Z[alive] = f_next(Z[alive], C[alive])
        esc = alive & (np.abs(Z) > R); out[esc] = i; alive &= ~esc
        if not alive.any(): break
    return out


def dimension(img, sizes=(2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128)):
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


def symmetries(img):
    inside = (img == img.max())
    sre = np.mean(inside == inside[::-1, :])
    sim = np.mean(inside == inside[:, ::-1])
    srot = np.mean(inside == inside[::-1, ::-1])
    return sre, sim, srot


def log(msg, path="fractal_z3zbar2_deep.txt"):
    print(msg, flush=True)
    open(path, "a").write(msg + "\n")


open("fractal_z3zbar2_deep.txt", "w").write("")  # reset
log("DEEP TEST z^3+conj(z)^2+c (anti) vs z^3+c (holo) -- dimension law + symmetry")
log("box=(-1.9,1.9)^2, R=50, maxit=250")
log("")
log(f"{'res':>5} {'holo_dim':>9} {'anti_dim':>9} {'gap':>8}  {'holo_sym(re,im,rot)':>22} {'anti_sym(re,im,rot)':>22}")
log("-" * 100)
for W in RES:
    iH = fractal(holo, W, W, MAXIT)
    iA = fractal(anti, W, W, MAXIT)
    dH, rH = dimension(iH); dA, rA = dimension(iA)
    sH = symmetries(iH); sA = symmetries(iA)
    log(f"{W:>5} {dH:>9.4f} {dA:>9.4f} {dA-dH:>+8.4f}  "
        f"({sH[0]:.3f},{sH[1]:.3f},{sH[2]:.3f})        "
        f"({sA[0]:.3f},{sA[1]:.3f},{sA[2]:.3f})")
log("-" * 100)
log("READING: gap -> 0 across res = ARTEFACT; gap stabilizes positive = LAW.")
log("SYMMETRY: anti breaks imag-axis/rot180 while keeping real-axis = measurable")
log("anti-holomorphic fingerprint (if it persists at all resolutions).")
log("[DONE]")
