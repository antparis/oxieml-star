#!/usr/bin/env python3
"""
fractal_generalize.py -- Does the anti-holomorphic geometric fingerprint of
z^3+conj(z)^2+c GENERALIZE into a LAW over the mixed asymmetric family z^a+conj(z)^b+c?

For each (a,b) pair we measure, vs the holo witness z^a+c:
  (1) judge would say anti (known: different exponents -> anti);
  (2) DIMENSION gap (anti - holo) at two resolutions -> stable positive?
  (3) SYMMETRY: real/imag/rot180 mirrors + rotation orders (scipy) to find which
      symmetry the anti object keeps, and whether it depends on (a,b) or (a-b).

GOAL: find a RULE (e.g. surviving rotational symmetry order = f(a,b)). If a consistent
pattern emerges across pairs -> general law on mixed anti fractals. If each object is
idiosyncratic -> no law, z^3+conj(z)^2 stays a single characterized object.

DISCIPLINE: rotation-symmetry via image interpolation is APPROXIMATE (edge blur). Treat
rotation numbers as indicative; the mirror symmetries (exact array flips) are reliable.
Escape radius R=50.

Output: fractal_generalize.txt (progressive). Run detached:
  setsid nohup python3 -u fractal_generalize.py > fractal_generalize.log 2>&1 &
"""
import numpy as np
from scipy.ndimage import rotate as ndrotate

BOX = (-1.9, 1.9, -1.9, 1.9)
RES = [1000, 2000]   # two resolutions to check dimension-gap stability
MAXIT = 250


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


def dimension(img, sizes=(2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96)):
    edge = (np.abs(np.diff(img.astype(float), axis=0))[:, :-1] +
            np.abs(np.diff(img.astype(float), axis=1))[:-1, :]) > 0
    def bc(Z, k):
        S = np.add.reduceat(np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                            np.arange(0, Z.shape[1], k), axis=1)
        return np.count_nonzero(S)
    counts = np.array([bc(edge, k) for k in sizes]); valid = counts > 0
    s = np.array(sizes)[valid]; c = counts[valid]
    return -np.polyfit(np.log(s), np.log(c), 1)[0]


def mirrors(img):
    ins = (img == img.max())
    return (np.mean(ins == ins[::-1, :]), np.mean(ins == ins[:, ::-1]),
            np.mean(ins == ins[::-1, ::-1]))


def rot_sym(img, deg):
    ins = (img == img.max()).astype(float)
    r = ndrotate(ins, deg, reshape=False, order=0)
    return np.mean((ins > 0.5) == (r > 0.5))


def holo(a): return lambda z, c: z**a + c
def anti(a, b): return lambda z, c: z**a + np.conj(z)**b + c


def log(m, p="fractal_generalize.txt"):
    print(m, flush=True); open(p, "a").write(m + "\n")


PAIRS = [(3, 2), (4, 2), (5, 2), (4, 3), (5, 3), (5, 4)]
open("fractal_generalize.txt", "w").write("")
log("GENERALIZATION TEST: mixed anti fractal z^a+conj(z)^b+c, fingerprint vs (a,b)")
log("box=(-1.9,1.9)^2, R=50, maxit=250. Mirrors exact; rotations approximate (scipy).")
log("")
log(f"{'(a,b)':>6} {'a-b':>3} | {'holo_d':>7} {'anti_d':>7} {'gap1k':>7} {'gap2k':>7} | "
    f"{'re':>5} {'im':>5} {'r180':>5} {'r90':>5} {'r120':>5} {'r72':>5} {'r60':>5}")
log("-" * 104)

# pre-compute holo witnesses (dimension only, at both res)
holo_dims = {}
for a in sorted(set(p[0] for p in PAIRS)):
    dd = [dimension(fractal(holo(a), W, W, MAXIT)) for W in RES]
    holo_dims[a] = dd

for (a, b) in PAIRS:
    # anti at both resolutions for gap
    iA1 = fractal(anti(a, b), RES[0], RES[0], MAXIT)
    iA2 = fractal(anti(a, b), RES[1], RES[1], MAXIT)
    dA1 = dimension(iA1); dA2 = dimension(iA2)
    dH1, dH2 = holo_dims[a]
    mir = mirrors(iA2)
    r90 = rot_sym(iA2, 90); r120 = rot_sym(iA2, 120)
    r72 = rot_sym(iA2, 72); r60 = rot_sym(iA2, 60)
    log(f"({a},{b}) {a-b:>3} | {dH2:>7.3f} {dA2:>7.3f} {dA1-dH1:>+7.3f} {dA2-dH2:>+7.3f} | "
        f"{mir[0]:>5.3f} {mir[1]:>5.3f} {mir[2]:>5.3f} {r90:>5.3f} {r120:>5.3f} {r72:>5.3f} {r60:>5.3f}")
log("-" * 104)
log("LOOK FOR: does gap stay positive for all pairs (dimension law general)?")
log("Does a rotation order ~1.000 track a-b or a or b (symmetry law)?")
log("Mirrors are reliable; rotation numbers indicative only.")
log("[DONE]")
