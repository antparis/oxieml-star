#!/usr/bin/env python3
"""
singularity_reader.py -- profile-AGNOSTIC reader of complex singularities from a SAMPLED profile.

Interface:  read(x, u, func=None, true_delta=None)
  x, u        : real-axis arrays (the level-3 interface: real numerical profiles arrive as grids).
  func        : optional profile callable, calibration only (for the precise radial lens).
  true_delta  : optional known singularity distance, calibration only (radial needs it exactly).

TWO LENSES (Fourier strip deliberately NOT included: our analyticity-strip Fourier instrument is
documented broken -- wrong k-band on slowly-decaying profiles -- and AAA is its replacement):
  - AAA on U'/U  : LOCATOR + spectrum. Finds ALL singularities (delta, x_loc), resolves multiple /
                   equidistant ones. gamma_aaa = -Re(residue): EXACT for poles, ~5% biased for
                   branch cuts (the cut leaks a pole-string, filtered out as cut-tail).
  - radial       : PRECISE exponent, CALIBRATION ONLY (needs func AND the exact true_delta):
                   |func(i s)| ~ (delta - s)^{-gamma}. Hyper-sensitive to delta, so it uses
                   true_delta, never the AAA estimate.

CONVENTION (settled, arXiv:2010.01201): gamma = spatial order = 1/(1-a); Fourier p = 1 - gamma.
These lenses report gamma.

ARTIFACT FILTER: near-real U'/U poles -> zeros of u / edges (discarded); off-axis clusters with
gamma <= gamma_floor -> cut-tail / Froissart (discarded). Genuine = off-axis, gamma > gamma_floor.

OPEN INSTRUMENT GAP: reading gamma of a genuine BRANCH point from a real array WITHOUT a formula
is currently only ~5% accurate (AAA residue); the clean route would be a modified-for-branch-
points AAA (cf. Lushnikov et al. sec. 10). Flagged, not hidden.

NOT the cube: real-analytic profile -> forced holomorphic; question is (delta, gamma), not holo/anti.

Run:  python3 singularity_reader.py     (self-test on CLM, a=1/2, probes A/B/C)
"""
import numpy as np
from scipy.linalg import eig

# ----------------------------------------------------------------- AAA primitives
def aaa(F, Z, tol=1e-13, mmax=120):
    F = np.asarray(F, dtype=complex); Z = np.asarray(Z, dtype=complex)
    m = np.isfinite(F); F, Z = F[m], Z[m]
    M = len(Z); Rg = np.mean(F) * np.ones(M, dtype=complex)
    zj = np.empty(0, dtype=complex); fj = np.empty(0, dtype=complex); J = list(range(M)); w = None
    for _ in range(mmax):
        j = max(J, key=lambda i: abs(F[i] - Rg[i]))
        zj = np.append(zj, Z[j]); fj = np.append(fj, F[j]); J.remove(j)
        if not J:
            break
        Ja = np.array(J); C = 1.0 / (Z[Ja][:, None] - zj[None, :])
        Am = (F[Ja][:, None] - fj[None, :]) * C
        _, _, Vh = np.linalg.svd(Am, full_matrices=False); w = Vh.conj().T[:, -1]
        Rg = F.copy(); Rg[Ja] = (C @ (w * fj)) / (C @ w)
        if np.max(np.abs(F[Ja] - Rg[Ja])) <= tol * np.max(np.abs(F)):
            break
    return zj, fj, w

def prz(zj, fj, w):
    m = len(w); B = np.eye(m + 1, dtype=complex); B[0, 0] = 0.0
    E = np.zeros((m + 1, m + 1), dtype=complex)
    E[0, 1:] = w; E[1:, 0] = 1.0; E[1:, 1:] = np.diag(zj)
    ev = eig(E, B, right=False); pol = ev[np.isfinite(ev)]
    res = [np.sum(w * fj / (p - zj)) / (-np.sum(w / (p - zj) ** 2)) for p in pol]
    return pol, np.array(res)

def cluster(off, eps=0.15):
    used = [False] * len(off); cl = []
    for i, (p, r) in enumerate(off):
        if used[i]:
            continue
        mem = [(p, r)]; used[i] = True
        for j, (p2, r2) in enumerate(off):
            if (not used[j]) and abs(p2 - p) < eps:
                mem.append((p2, r2)); used[j] = True
        cl.append((np.mean([m[0] for m in mem]), np.sum([m[1] for m in mem]), len(mem)))
    return cl

# ----------------------------------------------------------------- lens 1: AAA locator
def aaa_spectrum(x, u, gamma_floor=0.15, im_thresh=2e-2):
    h = x[1] - x[0]
    uu = np.real(u)
    du = np.gradient(uu, h, edge_order=2)
    g = du / uu
    ok = np.isfinite(g) & (np.abs(g) < 1e3)
    zj, fj, w = aaa(g[ok].astype(complex), x[ok].astype(complex), tol=1e-12, mmax=80)
    pol, res = prz(zj, fj, w)
    off = [(p, r) for p, r in zip(pol, res) if abs(p.imag) > im_thresh]
    genuine, discarded = [], []
    for ctr, tot, k in cluster(off):
        if ctr.imag <= im_thresh:
            continue
        gamma = -np.real(tot)
        rec = (round(abs(ctr.imag), 4), round(gamma, 4), round(ctr.real, 4), k)
        (genuine if gamma > gamma_floor else discarded).append(rec)
    genuine.sort()
    return genuine, discarded

# ----------------------------------------------------------------- lens 2: radial (calibration)
def radial(func, true_delta, n=400):
    d = true_delta * np.logspace(-5.0, -1.3, n); s = true_delta - d
    v = np.abs(func(1j * s)); ok = np.isfinite(v) & (v > 0)
    sl, _ = np.linalg.lstsq(np.vstack([np.log(d[ok]), np.ones(ok.sum())]).T,
                            np.log(v[ok]), rcond=None)[0]
    return round(-sl, 4)

# ----------------------------------------------------------------- top-level read
def read(x, u, func=None, true_delta=None, label=""):
    print("=" * 84)
    print(f"READ  {label}")
    genuine, discarded = aaa_spectrum(x, u)
    print("  AAA spectrum (delta, gamma, x_loc, nodes), nearest first:")
    for s in genuine:
        print(f"      {s}")
    if discarded:
        print(f"  discarded cut-tail/Froissart (gamma<=floor): {len(discarded)} nodes, "
              f"deepest delta up to {max(d[0] for d in discarded)}")
    if not genuine:
        print("  VERDICT: no genuine off-axis singularity found.")
        print("=" * 84); return

    delta_p, gamma_aaa, xloc, _ = genuine[0]
    equidistant = sum(1 for s in genuine if abs(s[0] - delta_p) < 0.05 * max(delta_p, 1e-9))
    near_int = abs(gamma_aaa - round(gamma_aaa)) < 0.05
    typ = "pole (integer order)" if near_int else "branch point (non-integer)"

    print(f"  PRIMARY: delta={delta_p}  x_loc={xloc}  gamma_aaa(residue)={gamma_aaa}  -> {typ}")
    if func is not None and true_delta is not None:
        gr = radial(func, true_delta)
        dev = abs(gr - gamma_aaa)
        note = "agree" if dev < 0.03 else f"AAA off by {round(dev,3)} (branch-cut bias; radial is truth)"
        print(f"  radial gamma (calibration, true_delta={true_delta}) = {gr}   [{note}]")
    if len(genuine) > 1:
        kind = "EQUIDISTANT (Fourier single-fit would oscillate)" if equidistant > 1 else "different depths (Fourier would miss the deeper)"
        print(f"  MULTI-SINGULARITY: {len(genuine)} resolved -- {kind}.")
    print("=" * 84)


# ============================================================ self-test
def _grid(L, n):
    return np.linspace(-L, L, n) + (L / n) * 0.37

if __name__ == "__main__":
    f0 = lambda z: -2.0 * np.asarray(z, dtype=complex) / (np.asarray(z, dtype=complex) ** 2 + 1.0)
    x = _grid(14, 2000); read(x, f0(x), func=f0, true_delta=1.0,
                              label="CLM a=0  (truth: delta=1, gamma=1, simple pole)")

    fh = lambda z: (16.0 / 3.0) * np.asarray(z, dtype=complex) / (np.asarray(z, dtype=complex) ** 2 + 1.0) ** 2
    x = _grid(14, 2000); read(x, fh(x), func=fh, true_delta=1.0,
                              label="gCLM a=1/2  (truth: delta=1, gamma=2, double pole)")

    g = 0.7
    fA = lambda z: (np.asarray(z, dtype=complex) - 1j) ** (-g) + (np.asarray(z, dtype=complex) + 1j) ** (-g)
    x = _grid(14, 2000); read(x, fA(x), func=fA, true_delta=1.0,
                              label="probe A branch  (truth: delta=1, gamma=0.7)")

    fB = lambda z: 1.0 / (np.asarray(z, dtype=complex) ** 2 + 0.25) + 1.0 / (np.asarray(z, dtype=complex) ** 2 + 2.25)
    x = _grid(14, 2000); read(x, fB(x), label="probe B  (truth: delta=0.5 & 1.5, gamma=1 each)")

    fC = lambda z: 1.0 / ((np.asarray(z, dtype=complex) - 2.0) ** 2 + 1.0) + 1.0 / ((np.asarray(z, dtype=complex) + 2.0) ** 2 + 1.0)
    x = _grid(14, 2000); read(x, fC(x), label="probe C equidistant  (truth: x=+-2+-i, delta=1, gamma=1)")
