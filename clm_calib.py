#!/usr/bin/env python3
"""
clm_calib.py -- LEVEL-2a calibration of the complex-singularity instruments on the EXACT
Constantin-Lax-Majda (CLM) self-similar profile: a real fluid-model PDE solution in CLOSED
FORM, distinct in shape from the synthetic toys of complex_singularity.py --toys.

PROFILE (Elgindi-Jeong exact self-similar profile of CLM  omega_t = omega * H[omega]):
    Omega(x) = -2x / (1 + x^2)
TRUTH (verified by hand, not just cited): nearest complex singularities are SIMPLE POLES at
    x = +-i.  =>  delta_true = 1.0 ,  spatial exponent p_true = 1.0  (pole order 1; U'/U
    residue = -1).
    Check: Omega(i s) = -2 i s / (1 - s^2) ~ -i/(1-s) as s->1^-  => (delta - s)^(-p), p=1, delta=1.
    Check: U'/U = Omega'/Omega = (1 - x^2) / ( x (x^2 + 1) ) has poles at x=0 (res +1, the REAL
           ZERO of Omega) and x=+-i (res -1 each, the genuine off-axis singularities => p=1).

NEW WRINKLE vs toys: Omega has a REAL-AXIS ZERO at x=0, so U'/U carries an extra pole there
    (residue +1). The AAA instrument must DISCARD it (Im~0 and/or positive residue = a zero of
    U, not a singularity) and keep only the off-axis poles. The toy profiles had no zeros.

NOT the cube: a real-analytic profile continued to C is FORCED holomorphic (unique
continuation); the SPARC test passes. The question is location delta + exponent p, not holo vs
anti.

ORTHOGONAL AXIS (on the METHOD, not the object): read INTO the complex plane (imaginary axis),
extract the closed-form exponent, cross-check two independent lenses.

INSTRUMENTS (must AGREE with truth AND with each other):
  (I)  RADIAL log-log on Omega(i s) ~ (delta - s)^(-p) as s->delta^- ; given delta, slope = -p.
       (For a true unknown profile, delta would be taken from AAA; here delta_true is used to
       mirror the toy protocol exactly, apples-to-apples.)
  (II) AAA on U'/U formed FROM SAMPLES (numerical derivative), poles + residues. U'/U is built
       from samples (NOT the analytic ratio) to match the eventual real-data pipeline where only
       grid values are available. Off-axis pole gives delta = |Im(pole)|, p = -Re(residue).

Run:  python3 clm_calib.py
"""
import sys
import numpy as np
from scipy.linalg import eig

# ----------------------------------------------------------------------------- profile
def omega(x):
    x = np.asarray(x, dtype=complex)
    return -2.0 * x / (1.0 + x * x)

DELTA_TRUE = 1.0
P_TRUE = 1.0
TOL = 0.02  # 2% acceptance, same spirit as the toys gate

# ----------------------------------------------------------------- instrument I: radial
def instrument_radial(delta, n=400):
    """Fit log|Omega(i s)| vs log(delta - s) on a NEAR-singularity log-spaced band; slope = -p.
    The band is taken very close to delta so the slowly-varying prefactor is ~constant, otherwise
    a wide window biases the slope (CLM has a prefactor 2s/(1+s) -> 1 that contaminates wide fits)."""
    d = delta * np.logspace(-5.0, -1.3, n)      # d = delta - s : from 1e-5*delta to ~0.05*delta
    s = delta - d
    vals = np.abs(omega(1j * s))
    ok = np.isfinite(vals) & (vals > 0)
    X = np.log(d[ok])
    Y = np.log(vals[ok])
    A = np.vstack([X, np.ones_like(X)]).T
    slope, _ = np.linalg.lstsq(A, Y, rcond=None)[0]
    return -slope  # p

# --------------------------------------------------------------------- AAA (NST 2018)
def aaa(F, Z, tol=1e-13, mmax=100):
    F = np.asarray(F, dtype=complex)
    Z = np.asarray(Z, dtype=complex)
    M = len(Z)
    mask = np.isfinite(F)
    F, Z = F[mask], Z[mask]
    M = len(Z)
    Rg = np.mean(F) * np.ones(M, dtype=complex)
    zj = np.empty(0, dtype=complex)
    fj = np.empty(0, dtype=complex)
    J = list(range(M))
    w = None
    for _ in range(mmax):
        j = max(J, key=lambda i: abs(F[i] - Rg[i]))
        zj = np.append(zj, Z[j]); fj = np.append(fj, F[j])
        J.remove(j)
        if not J:
            break
        Jarr = np.array(J)
        C = 1.0 / (Z[Jarr][:, None] - zj[None, :])
        Amat = (F[Jarr][:, None] - fj[None, :]) * C
        _, _, Vh = np.linalg.svd(Amat, full_matrices=False)
        w = Vh.conj().T[:, -1]
        num = C @ (w * fj)
        den = C @ w
        Rg = F.copy()
        Rg[Jarr] = num / den
        err = np.max(np.abs(F[Jarr] - Rg[Jarr]))
        if err <= tol * np.max(np.abs(F)):
            break
    return zj, fj, w

def prz(zj, fj, w):
    """Poles and residues of the AAA barycentric rational."""
    m = len(w)
    B = np.eye(m + 1, dtype=complex); B[0, 0] = 0.0
    E = np.zeros((m + 1, m + 1), dtype=complex)
    E[0, 1:] = w
    E[1:, 0] = 1.0
    E[1:, 1:] = np.diag(zj)
    ev = eig(E, B, right=False)
    pol = ev[np.isfinite(ev)]
    # residues via the barycentric formula  res = N(p)/D'(p)
    res = []
    for p in pol:
        d = p - zj
        N = np.sum(w * fj / d)
        Dp = -np.sum(w / d**2)
        res.append(N / Dp)
    return pol, np.array(res)

# ------------------------------------------------------ instrument II: AAA on U'/U
def cluster_poles(off, eps=0.1):
    """Greedy-cluster nearby poles (AAA often splits one physical pole into a doublet) and
    SUM their residues per cluster, so a split pole is read as a single singularity."""
    used = [False] * len(off)
    clusters = []
    for i, (p, r) in enumerate(off):
        if used[i]:
            continue
        members = [(p, r)]; used[i] = True
        for j, (p2, r2) in enumerate(off):
            if (not used[j]) and abs(p2 - p) < eps:
                members.append((p2, r2)); used[j] = True
        ctr = np.mean([m[0] for m in members])
        tot = np.sum([m[1] for m in members])
        clusters.append((ctr, tot, len(members)))
    return clusters

def instrument_aaa(n=1200, L=12.0):
    """Build U'/U from SAMPLES (numerical derivative) on a real grid, AAA, cluster off-axis poles,
    select the cluster nearest the real axis -> delta = |Im|, p = -Re(summed residue)."""
    # uniform real grid, offset so it never lands exactly on 0 or +-1 etc.
    x = np.linspace(-L, L, n) + (L / n) * 0.37
    h = x[1] - x[0]
    u = np.real(omega(x))                       # real samples of the profile
    du = np.gradient(u, h, edge_order=2)        # numerical derivative
    g = du / u                                  # U'/U from samples
    ok = np.isfinite(g) & (np.abs(g) < 1e3)     # drop blow-ups right next to the real zero
    Z = x[ok].astype(complex)
    F = g[ok].astype(complex)
    zj, fj, w = aaa(F, Z, tol=1e-12, mmax=60)
    pol, res = prz(zj, fj, w)
    # classify raw poles: off-axis (genuine singularity) vs near-real (zero of U / edges)
    off = [(p, r) for p, r in zip(pol, res) if abs(p.imag) > 1e-2]
    near_real = [(p, r) for p, r in zip(pol, res) if abs(p.imag) <= 1e-2]
    if not off:
        return None, None, near_real, off, []
    clusters = cluster_poles(off)
    # keep upper-half-plane clusters only (lower half mirrors by conjugation -> avoid double count)
    upper = [c for c in clusters if c[0].imag > 1e-2]
    if not upper:
        return None, None, near_real, off, clusters
    ctr, tot, _ = min(upper, key=lambda c: abs(c[0].imag))   # nearest the real axis = dominant
    delta_aaa = abs(ctr.imag)
    p_exp = -np.real(tot)
    return delta_aaa, p_exp, near_real, off, clusters

# ------------------------------------------------------------------------- runner
def run():
    print("=" * 78)
    print("LEVEL-2a  CLM exact self-similar profile  Omega(x) = -2x/(1+x^2)")
    print(f"truth:  delta_true = {DELTA_TRUE}   p_true = {P_TRUE}   (simple poles at +-i)")
    print("-" * 78)

    p_radial = instrument_radial(DELTA_TRUE)
    delta_aaa, p_aaa, near_real, off, clusters = instrument_aaa()

    print(f"radial   : p = {p_radial:.4f}   (delta given = {DELTA_TRUE})")
    if delta_aaa is None:
        print("AAA      : NO off-axis cluster found  -> FAIL")
    else:
        print(f"AAA      : delta = {delta_aaa:.4f}   p = {p_aaa:.4f}")
    print(f"AAA off-axis clusters (center, summed_res, n) : "
          f"{[(round(c[0].real,3)+round(c[0].imag,3)*1j, round(c[1].real,3), c[2]) for c in clusters]}")
    print(f"AAA discarded (real-axis: zero of U / edges) : "
          f"{[(round(p.real,3), round(p.imag,3), round(r.real,3)) for p,r in near_real]}")
    print("-" * 78)

    ok = True
    reasons = []
    if not (abs(p_radial - P_TRUE) <= TOL):
        ok = False; reasons.append(f"radial p off by {abs(p_radial-P_TRUE):.3f}")
    if delta_aaa is None:
        ok = False; reasons.append("AAA found no off-axis pole")
    else:
        if not (abs(p_aaa - P_TRUE) <= TOL):
            ok = False; reasons.append(f"AAA p off by {abs(p_aaa-P_TRUE):.3f}")
        if not (abs(delta_aaa - DELTA_TRUE) <= TOL):
            ok = False; reasons.append(f"AAA delta off by {abs(delta_aaa-DELTA_TRUE):.3f}")
        if not (abs(p_radial - p_aaa) <= TOL):
            ok = False; reasons.append(f"instruments disagree on p by {abs(p_radial-p_aaa):.3f}")
    verdict = "PASS" if ok else "FAIL"
    print(f"VERDICT (tol={TOL}): {verdict}")
    if not ok:
        print("  reasons: " + "; ".join(reasons))
    print("=" * 78)
    return ok

if __name__ == "__main__":
    run()
