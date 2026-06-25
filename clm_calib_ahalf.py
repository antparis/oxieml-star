#!/usr/bin/env python3
"""
clm_calib_ahalf.py -- LEVEL-2b calibration on the EXACT a=1/2 generalized-CLM closed-form profile.

CONVENTION LOCK (resolved from Lushnikov-Silantyev-Siegel, arXiv:2010.01201):
  - gamma = SPATIAL singularity order: omega ~ (x - i v_c)^(-gamma)   (their Eq. 13/17).
  - Theorem 1 (Eq. 21):  gamma = 1/(1-a).
  - Fourier exponent p (their Eq. 62/63):  |omega_hat_k| ~ C e^(-delta|k|)/|k|^p  with  p = 1 - gamma.
    => p = -a/(1-a).
  THESE INSTRUMENTS MEASURE gamma (the spatial order), NOT the Fourier p. The quantity the
  sister file clm_calib.py prints as "p" is in fact gamma. We print gamma explicitly here and
  cross-print the Fourier p = 1 - gamma only for traceability against the paper.

PROFILE (their Eq. 38, exact a=1/2 self-similar solution, v_c = 1):
    Omega(xi) = (16/3) * xi / (xi^2 + 1)^2
TRUTH (verified by hand): DOUBLE poles at xi = +-i  =>  gamma_true = 2 , delta_true = 1.
    Cross-check law: gamma = 1/(1 - 1/2) = 2.  Fourier p = 1 - 2 = -1 = -a/(1-a) with a=1/2.
    U'/U = Omega'/Omega = (1 - 3 xi^2)/( xi (xi^2 + 1) ): poles at xi=0 (res +1, REAL ZERO of
    Omega, to discard) and xi=+-i (res -2 each => gamma = 2). Note the log-derivative turns a
    pole of ANY order gamma into a SIMPLE pole of U'/U with residue -gamma.

NON-CIRCULAR: a genuine a != 0 PDE solution in closed form, with a singularity order (gamma=2,
double pole) DIFFERENT from the level-2a CLM case (gamma=1, simple pole). By Theorem 3 of the
paper, a=0 and a=1/2 are the ONLY values with a pure closed-form leading-order singularity, so
this is the only non-trivial closed-form a!=0 calibration available; other a require the
numerical profile (the level-3 unknown).

NOT the cube: real-analytic profile -> forced holomorphic (unique continuation); question is
delta + gamma, not holo vs anti. Orthogonal axis is on the METHOD (read into the complex plane;
extract the closed-form order; two cross-checking lenses).

Run:  python3 clm_calib_ahalf.py
"""
import numpy as np
from scipy.linalg import eig

# ----------------------------------------------------------------------------- profile (a=1/2)
def omega(x):
    x = np.asarray(x, dtype=complex)
    return (16.0 / 3.0) * x / (x * x + 1.0) ** 2

A_PARAM = 0.5
DELTA_TRUE = 1.0
GAMMA_TRUE = 2.0           # spatial order = 1/(1-a) = 2
P_FOURIER_TRUE = 1.0 - GAMMA_TRUE   # = -1 ; only for cross-reference with the paper's "p"
TOL = 0.02

# ----------------------------------------------------------------- instrument I: radial
def instrument_radial(delta, n=400):
    """Fit log|Omega(i s)| vs log(delta - s) on a near-singularity log-spaced band; slope = -gamma.
    Tight band near s->delta^- so the slowly-varying prefactor is ~constant (a double pole has an
    even stronger prefactor, so the tight window matters more here)."""
    d = delta * np.logspace(-5.0, -1.3, n)      # d = delta - s in [1e-5, ~0.05]*delta
    s = delta - d
    vals = np.abs(omega(1j * s))
    ok = np.isfinite(vals) & (vals > 0)
    X = np.log(d[ok]); Y = np.log(vals[ok])
    A = np.vstack([X, np.ones_like(X)]).T
    slope, _ = np.linalg.lstsq(A, Y, rcond=None)[0]
    return -slope  # gamma

# --------------------------------------------------------------------- AAA (NST 2018)
def aaa(F, Z, tol=1e-13, mmax=100):
    F = np.asarray(F, dtype=complex); Z = np.asarray(Z, dtype=complex)
    m = np.isfinite(F); F, Z = F[m], Z[m]
    M = len(Z)
    Rg = np.mean(F) * np.ones(M, dtype=complex)
    zj = np.empty(0, dtype=complex); fj = np.empty(0, dtype=complex)
    J = list(range(M)); w = None
    for _ in range(mmax):
        j = max(J, key=lambda i: abs(F[i] - Rg[i]))
        zj = np.append(zj, Z[j]); fj = np.append(fj, F[j]); J.remove(j)
        if not J:
            break
        Ja = np.array(J)
        C = 1.0 / (Z[Ja][:, None] - zj[None, :])
        Am = (F[Ja][:, None] - fj[None, :]) * C
        _, _, Vh = np.linalg.svd(Am, full_matrices=False)
        w = Vh.conj().T[:, -1]
        num = C @ (w * fj); den = C @ w
        Rg = F.copy(); Rg[Ja] = num / den
        if np.max(np.abs(F[Ja] - Rg[Ja])) <= tol * np.max(np.abs(F)):
            break
    return zj, fj, w

def prz(zj, fj, w):
    m = len(w)
    B = np.eye(m + 1, dtype=complex); B[0, 0] = 0.0
    E = np.zeros((m + 1, m + 1), dtype=complex)
    E[0, 1:] = w; E[1:, 0] = 1.0; E[1:, 1:] = np.diag(zj)
    ev = eig(E, B, right=False)
    pol = ev[np.isfinite(ev)]
    res = []
    for p in pol:
        d = p - zj
        res.append(np.sum(w * fj / d) / (-np.sum(w / d**2)))
    return pol, np.array(res)

def cluster_poles(off, eps=0.1):
    used = [False] * len(off); clusters = []
    for i, (p, r) in enumerate(off):
        if used[i]:
            continue
        mem = [(p, r)]; used[i] = True
        for j, (p2, r2) in enumerate(off):
            if (not used[j]) and abs(p2 - p) < eps:
                mem.append((p2, r2)); used[j] = True
        clusters.append((np.mean([m[0] for m in mem]), np.sum([m[1] for m in mem]), len(mem)))
    return clusters

# ------------------------------------------------------ instrument II: AAA on U'/U
def instrument_aaa(n=1600, L=14.0):
    """U'/U from SAMPLES (numerical derivative), AAA, cluster off-axis poles, nearest-real cluster
    -> delta = |Im|, gamma = -Re(summed residue). (Log-derivative reads gamma for any pole order.)"""
    x = np.linspace(-L, L, n) + (L / n) * 0.37
    h = x[1] - x[0]
    u = np.real(omega(x))
    du = np.gradient(u, h, edge_order=2)
    g = du / u
    ok = np.isfinite(g) & (np.abs(g) < 1e3)
    Z = x[ok].astype(complex); F = g[ok].astype(complex)
    zj, fj, w = aaa(F, Z, tol=1e-12, mmax=60)
    pol, res = prz(zj, fj, w)
    off = [(p, r) for p, r in zip(pol, res) if abs(p.imag) > 1e-2]
    near_real = [(p, r) for p, r in zip(pol, res) if abs(p.imag) <= 1e-2]
    if not off:
        return None, None, near_real, []
    clusters = cluster_poles(off)
    upper = [c for c in clusters if c[0].imag > 1e-2]
    if not upper:
        return None, None, near_real, clusters
    ctr, tot, _ = min(upper, key=lambda c: abs(c[0].imag))
    return abs(ctr.imag), -np.real(tot), near_real, clusters

# ------------------------------------------------------------------------- runner
def run():
    print("=" * 80)
    print(f"LEVEL-2b  exact a={A_PARAM} gCLM profile  Omega(xi) = (16/3) xi/(xi^2+1)^2")
    print(f"truth:  delta_true = {DELTA_TRUE}   gamma_true = {GAMMA_TRUE}   (double poles at +-i)")
    print(f"        Fourier p = 1 - gamma = {P_FOURIER_TRUE}  (paper's symbol; NOT what we measure)")
    print("-" * 80)
    g_radial = instrument_radial(DELTA_TRUE)
    delta_aaa, g_aaa, near_real, clusters = instrument_aaa()
    print(f"radial   : gamma = {g_radial:.4f}   (delta given = {DELTA_TRUE})")
    if delta_aaa is None:
        print("AAA      : NO off-axis cluster found  -> FAIL")
    else:
        print(f"AAA      : delta = {delta_aaa:.4f}   gamma = {g_aaa:.4f}")
    print(f"AAA off-axis clusters (center, summed_res, n) : "
          f"{[(round(c[0].real,3)+round(c[0].imag,3)*1j, round(c[1].real,3), c[2]) for c in clusters]}")
    print(f"AAA discarded (real-axis: zero of U / edges) : "
          f"{[(round(p.real,3), round(p.imag,3), round(r.real,3)) for p,r in near_real]}")
    print("-" * 80)
    ok = True; why = []
    if not (abs(g_radial - GAMMA_TRUE) <= TOL):
        ok = False; why.append(f"radial gamma off by {abs(g_radial-GAMMA_TRUE):.3f}")
    if delta_aaa is None:
        ok = False; why.append("AAA found no off-axis cluster")
    else:
        if not (abs(g_aaa - GAMMA_TRUE) <= TOL):
            ok = False; why.append(f"AAA gamma off by {abs(g_aaa-GAMMA_TRUE):.3f}")
        if not (abs(delta_aaa - DELTA_TRUE) <= TOL):
            ok = False; why.append(f"AAA delta off by {abs(delta_aaa-DELTA_TRUE):.3f}")
        if not (abs(g_radial - g_aaa) <= TOL):
            ok = False; why.append(f"instruments disagree on gamma by {abs(g_radial-g_aaa):.3f}")
    print(f"VERDICT (tol={TOL}): {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  reasons: " + "; ".join(why))
    print("=" * 80)
    return ok

if __name__ == "__main__":
    run()
