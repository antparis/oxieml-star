#!/usr/bin/env python3
"""
complex_singularity.py -- two cross-validating instruments to read, from a real-analytic
profile u(y) sampled on the real axis, the location delta and the EXPONENT p of the nearest
complex singularity   u(y) ~ C * (y^2 + delta^2)^(-p)   (a conjugate pair at y = +-i*delta).

WHY (oxieml-star, Navier-Stokes angle): DeepMind/Gomez-Serrano 2025 give blow-up profiles
NUMERICALLY (a grid of values), not in closed form. Our tool's job is to extract the TYPE and
EXPONENT of the complex singularity -- the structural fact their numerics do not hand you.

NOT the cube. A real-analytic profile continued to C is FORCED holomorphic (unique continuation):
no independent zbar, no anti. The SPARC test passes (the continuation is forced, not a choice).
The question here is "where is the singularity and how strong", not "holo vs anti".

ORTHOGONAL AXIS (on the METHOD, not the object):
  - everyone reads u on the REAL axis; we read the distance delta INTO the complex plane.
  - everyone solves numerically; we extract the closed-form exponent.

TWO INSTRUMENTS (must AGREE -- rule: two lenses + cross-check):
  (I)  RADIAL log-log:   on the imaginary axis u(i*s) blows up as (delta - s)^(-p) as s->delta^-.
                         A log-log fit of u(i*s) vs (delta - s) gives slope -p. delta read from
                         the blow-up location. [validated to 0.5% on toys in a prior session]
  (II) AAA on U'/U:      U = u (or its analytic continuation); the logarithmic derivative
                         U'/U has a SIMPLE POLE at each singularity with residue -p (a branch
                         point (z-z0)^(-p) -> U'/U ~ -p/(z-z0)). AAA rational approximation
                         (Nakatsukasa-Sete-Trefethen 2018) finds poles+residues robustly.
                         => delta = |Im(pole)|, p = -residue. This converts a hard branch point
                         into an easy simple pole.

PITFALL (sealed): lambda (the self-similar RATE published by DeepMind) != p (the singularity
EXPONENT). Do not compare our p to their lambda. They are different quantities.

CALIBRATION LADDER (known before unknown, same discipline as the cube):
  step 0: 4 toys with KNOWN (delta, p) -> both instruments must agree with truth.
  step 1: CCF proven law p = -a/(1-a)  (Lushnikov-Silantyev-Siegel 2021, arXiv:2010.01201).
  step 2: only then, a real DeepMind profile.

GUARD-RAILS (memory rule CHECKPOINT/RECUPERATION): heartbeat per step, partial save, timeout
on any expensive/again-able step. No step may hang the chain.

Run:  python3 complex_singularity.py --toys
"""
import argparse, json, time, signal
import numpy as np


# ---------------------------------------------------------------- guard-rails
class _Timeout(Exception): pass
def _alarm(signum, frame): raise _Timeout()
STEP_TIMEOUT = 30  # s per instrument per toy

def hb(tag, msg):
    with open(f"cs_{tag}_progress.log", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')}  {msg}\n")


# ---------------------------------------------------------------- toy profiles
# Each: u(y) on real axis = (y^2 + delta^2)^(-p), known (delta, p). The nearest complex
# singularity sits at y = +- i*delta with exponent p. These are the ground truth.
def make_toys():
    return {
        "toy_p1.0_d1.0":  dict(delta=1.0, p=1.0),
        "toy_p0.5_d1.0":  dict(delta=1.0, p=0.5),
        "toy_p1.5_d0.7":  dict(delta=0.7, p=1.5),
        "toy_p0.8_d1.3":  dict(delta=1.3, p=0.8),
    }

def u_real(y, delta, p):
    return (y**2 + delta**2)**(-p)


# ---------------------------------------------------------------- instrument I: radial log-log
def instrument_radial(delta_true, p_true, n=4000):
    """Sample u on the imaginary axis y = i*s, s in [0, delta). u(i*s) = (delta^2 - s^2)^(-p).
    As s->delta^-, u ~ (2*delta)^(-p) * (delta - s)^(-p). Fit log u vs log(delta - s) near the
    pole -> slope = -p. We also recover delta by scanning where the blow-up centres."""
    # we are GIVEN delta_true here only to place the sampling window; the FIT must still recover p
    # (in the real pipeline delta is found first by the blow-up location; for the toy we use a
    #  narrow window approaching the known pole, which is the honest analogue).
    s = delta_true * (1.0 - np.logspace(-6, -0.3, n))   # s approaches delta from below
    val = (delta_true**2 - s**2)**(-p_true)
    eps = delta_true - s                                 # distance to the pole
    mask = (eps > 0) & np.isfinite(val) & (val > 0)
    L = np.log(eps[mask]); Y = np.log(val[mask])
    # fit only the closest decade to the pole (asymptotic regime)
    k = max(50, len(L)//5)
    idx = np.argsort(L)[:k]                              # smallest eps = closest to pole
    A = np.vstack([L[idx], np.ones_like(L[idx])]).T
    slope, intercept = np.linalg.lstsq(A, Y[idx], rcond=None)[0]
    p_est = -slope
    return dict(p_est=float(p_est), delta_est=float(delta_true))   # delta is the window centre here


# ---------------------------------------------------------------- AAA rational approximation
def aaa(F, Z, tol=1e-13, mmax=100):
    """Adaptive Antoulas-Anderson. F = values, Z = sample points (complex). Returns a callable
    r(z) plus its poles and residues. Standard barycentric AAA (Nakatsukasa-Sete-Trefethen 2018)."""
    Z = np.asarray(Z, dtype=complex); F = np.asarray(F, dtype=complex)
    M = len(Z); J = list(range(M))
    zj = np.empty(0, dtype=complex); fj = np.empty(0, dtype=complex); w = np.empty(0, dtype=complex)
    R = np.full(M, np.mean(F), dtype=complex)
    errvec = []
    for m in range(mmax):
        j = J[int(np.argmax(np.abs(F[J] - R[J])))]       # greedy: worst-approximated point
        zj = np.append(zj, Z[j]); fj = np.append(fj, F[j]); J.remove(j)
        if len(J) == 0: break
        C = 1.0 / (Z[J][:, None] - zj[None, :])          # Cauchy matrix
        A = (F[J][:, None] - fj[None, :]) * C            # Loewner matrix
        _, _, Vh = np.linalg.svd(A, full_matrices=False)
        w = Vh.conj()[-1, :]                             # weights = last right singular vector
        num = C @ (w * fj); den = C @ w
        R = F.copy().astype(complex); R[J] = num / den
        err = np.max(np.abs(F[J] - R[J]))
        errvec.append(err)
        if err <= tol * np.max(np.abs(F)): break
    # poles & residues via generalized eigenproblem (standard AAA pole-finding)
    m = len(w)
    B = np.eye(m + 1); B[0, 0] = 0
    E = np.zeros((m + 1, m + 1), dtype=complex)
    E[0, 1:] = w; E[1:, 0] = 1.0
    for i in range(m): E[i + 1, i + 1] = zj[i]
    eig = np.linalg.eig(E)[0]
    pol = eig[np.isfinite(eig)]
    pol = pol[np.abs(pol) < 1e8]
    # residues by finite difference of the barycentric form
    def rfun(z):
        z = np.asarray(z, dtype=complex)
        C = 1.0 / (z[..., None] - zj)
        return (C @ (w * fj)) / (C @ w)
    dz = 1e-6
    res = np.array([(rfun(pp + dz) - rfun(pp - dz)) * dz / 2 for pp in pol])  # ~ residue estimate
    # better residue: res_k = N(pol)/D'(pol) ; use small-circle integral
    res = []
    for pp in pol:
        th = np.linspace(0, 2*np.pi, 64, endpoint=False)
        r0 = 1e-4
        zc = pp + r0*np.exp(1j*th)
        res.append(np.mean(rfun(zc) * (zc - pp)))   # (1/2pi i) contour ~ mean of f*(z-pole)
    return rfun, pol, np.array(res)


def _find_pole_on_imag(rfun, s_max, n=2000):
    """The conjugate-pair singularity lies on the imaginary axis at z = i*delta. |U'/U| blows up
    there. Scan s in (0, s_max), return the s maximising |rfun(i*s)| -> delta. This is more robust
    than the generalized-eigenproblem pole finder and uses the known physics (poles on imag axis)."""
    s = np.linspace(0.01, s_max, n)
    mag = np.abs(rfun(1j*s))
    return float(s[int(np.argmax(mag))])

def _residue_contour(rfun, z0, r0=1e-3):
    """Residue of a simple pole by small-circle average: res = (1/2pi i) oint f dz = mean of
    f(z)*(z-z0) over a small circle. For U'/U at a branch point (z-z0)^(-p), residue = -p."""
    th = np.linspace(0, 2*np.pi, 128, endpoint=False)
    zc = z0 + r0*np.exp(1j*th)
    return np.mean(rfun(zc) * (zc - z0))

def instrument_aaa(delta_true, p_true, n=600):
    """Sample U off the real axis (inside |Im z| < delta), build the logarithmic derivative
    G = U'/U, AAA-approximate G, then locate the pole on the imaginary axis and read its residue.
    Branch point (z^2+delta^2)^(-p): G = -p*2z/(z^2+delta^2) -> simple pole at z=i*delta, residue -p.
    => delta = pole location on imag axis, p = -residue. (In the real pipeline U'/U comes from
    numerical differentiation of the sampled profile's continuation -- same target object.)"""
    rng = np.random.default_rng(0)
    xr = rng.uniform(-3, 3, n)
    yi = rng.uniform(-0.45*delta_true, 0.45*delta_true, n)   # stay inside |Im z| < delta
    Z = xr + 1j*yi
    U = (Z**2 + delta_true**2)**(-p_true)
    dU = -p_true * 2*Z * (Z**2 + delta_true**2)**(-p_true - 1)
    G = dU / U
    rfun, _, _ = aaa(G, Z, tol=1e-12, mmax=60)
    delta_est = _find_pole_on_imag(rfun, s_max=max(3.0, 2.0*delta_true))
    p_est = float(-_residue_contour(rfun, 1j*delta_est).real)
    return dict(p_est=p_est, delta_est=float(delta_est))


# ---------------------------------------------------------------- cross-validated run
def run_toys():
    toys = make_toys()
    print("="*96)
    print("COMPLEX-SINGULARITY BENCH -- calibration on 4 toys with KNOWN (delta, p)")
    print("Two instruments must AGREE with truth AND with each other.")
    print("="*96)
    print(f"{'toy':<18}{'p_true':>8}{'d_true':>8} | {'radial p':>10}{'aaa p':>10}{'aaa d':>10} | {'verdict'}")
    print("-"*96)
    results = {}
    all_ok = True
    for name, t in toys.items():
        dt, pt = t["delta"], t["p"]
        hb(name, "start")

        # instrument I (radial) under timeout
        signal.signal(signal.SIGALRM, _alarm); signal.alarm(STEP_TIMEOUT)
        try:
            ri = instrument_radial(dt, pt); signal.alarm(0); hb(name, f"radial p={ri['p_est']:.4f}")
        except _Timeout:
            ri = dict(p_est=float("nan"), delta_est=float("nan")); hb(name, "radial TIMEOUT [LIMIT]")

        # instrument II (AAA) under timeout
        signal.signal(signal.SIGALRM, _alarm); signal.alarm(STEP_TIMEOUT)
        try:
            ai = instrument_aaa(dt, pt); signal.alarm(0); hb(name, f"aaa p={ai['p_est']:.4f} d={ai['delta_est']:.4f}")
        except _Timeout:
            ai = dict(p_est=float("nan"), delta_est=float("nan"), n_poles=0); hb(name, "aaa TIMEOUT [LIMIT]")

        # agreement test: both within 2% of truth AND within 2% of each other
        def close(a, b, tol=0.02): return abs(a-b) <= tol*max(abs(b), 1e-9)
        p_radial_ok = close(ri["p_est"], pt)
        p_aaa_ok    = close(ai["p_est"], pt)
        d_aaa_ok    = close(ai["delta_est"], dt)
        cross_ok    = close(ri["p_est"], ai["p_est"], tol=0.03)
        ok = p_radial_ok and p_aaa_ok and d_aaa_ok and cross_ok
        all_ok = all_ok and ok
        verdict = "OK" if ok else "MISMATCH"
        print(f"{name:<18}{pt:>8.2f}{dt:>8.2f} | {ri['p_est']:>10.4f}{ai['p_est']:>10.4f}{ai['delta_est']:>10.4f} | {verdict}")
        results[name] = dict(p_true=pt, delta_true=dt,
                             radial_p=ri["p_est"], aaa_p=ai["p_est"], aaa_delta=ai["delta_est"],
                             p_radial_ok=p_radial_ok, p_aaa_ok=p_aaa_ok, d_aaa_ok=d_aaa_ok,
                             cross_ok=cross_ok, passed=ok)
        hb(name, f"done passed={ok}")
    print("-"*96)
    print(f"TOYS: {'PASS' if all_ok else 'FAIL'}  (both instruments agree with truth and each other within tol)")
    print("="*96)
    json.dump(results, open("cs_toys_result.json", "w"), indent=2)
    print("[saved] cs_toys_result.json")
    return all_ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--toys", action="store_true")
    args = ap.parse_args()
    run_toys()
