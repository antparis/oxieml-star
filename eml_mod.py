#!/usr/bin/env python3
"""eml_mod.py -- modularity-defect detector (eml-mod), a transformation operator of a
DIFFERENT TYPE from the three local eml operators.

The eml family:
  eml   (holomorphic)  : df/dzbar == 0                         [LOCAL, symbolic, autonomous]
  eml*  (anti-holo)    : judge_v2.certify_1field 4-label       [LOCAL, symbolic, autonomous]
  eml0  (pure phase)   : |f|^2 constant while f varies          [LOCAL, symbolic, autonomous]
  eml-mod (modularity) : defect under S: tau -> -1/tau          [GLOBAL, numeric, certificatory]

eml-mod is NOT a 4th local eml on equal footing. It is GLOBAL (relates f(tau) to f(-1/tau)),
NUMERIC (cannot simplify q-series under S symbolically), and CERTIFICATORY (classifies the
transformation behavior of a GIVEN function; does not discover structure from a derivative).

CRITICAL -- weight/automorphy convention (eml-mod is FRAGILE to this, by its nature):
The automorphy factor of S = [[0,-1],[1,0]] is (c tau + d)^k = tau^k. For HALF-INTEGER weight
theta-type forms there is an extra multiplier system: theta3 uses (-i tau)^(1/2) instead of
tau^(1/2). Pass multiplier='theta' for that case; default multiplier=None uses tau^k.
Getting this wrong yields a SPURIOUS defect (a local eml cannot make this error; eml-mod can).

Verdict delta_S(f)(tau) = f(-1/tau) - W(tau) f(tau), W = automorphy factor:
  delta_S ~ 0 at all sample points          -> 'modular'
  delta_S/tau constant (linear anomaly)      -> 'quasi-modular'   (E2: delta_S/tau = -6i/pi)
  delta_S != 0, not a clean linear anomaly   -> 'non-modular'     (mock period / false cocycle)

Established 2026-06-22 (FINDINGS_20260622m, 0622n): separates genuine theta (modular),
E2 (quasi-modular), false theta (non-modular). Mock-theta period sub-case = DERIVATION/LIMITE
(weight-1/2 multiplier system not fully resolved numerically).

Author: Anthony Monnerot, 2026.
"""
import mpmath as mp


def automorphy_factor(tau, k, multiplier=None):
    """Automorphy factor W(tau) for S: tau->-1/tau, weight k.
    multiplier=None -> tau^k (standard). multiplier='theta' -> (-i tau)^k (theta multiplier system)."""
    if multiplier == 'theta':
        return (-1j*tau)**k
    return tau**k


def modular_defect(f, tau, k, multiplier=None):
    """delta_S(f)(tau) = f(-1/tau) - W(tau) f(tau)."""
    return f(-1/tau) - automorphy_factor(tau, k, multiplier) * f(tau)


def eml_mod(f, k, multiplier=None, points=None, tol=None):
    """Classify f's modularity behavior under S, weight k.
    Returns 'modular' / 'quasi-modular' / 'non-modular'. Sample points are off the S fixed
    point tau=i (where the test is degenerate)."""
    if points is None:
        points = [1j*mp.mpf('1.3'), 1j*mp.mpf('1.6'), 1j*mp.mpf('2.0'), 1j*mp.mpf('0.7')]
    if tol is None:
        tol = mp.mpf(10)**(-12)
    defects = [modular_defect(f, t, k, multiplier) for t in points]
    if max(abs(d) for d in defects) < tol:
        return 'modular'
    # quasi-modular probe: delta_S/tau constant (E2-type linear anomaly)?
    ratios = [defects[i]/points[i] for i in range(len(points))]
    spread = max(abs(ratios[i]-ratios[0]) for i in range(len(ratios)))
    if spread < mp.mpf(10)**(-8):
        return 'quasi-modular'
    return 'non-modular'


if __name__ == "__main__":
    mp.mp.dps = 25
    print("=" * 72)
    print("eml_mod self-validation (each line must say OK)")
    print("=" * 72)

    def sigma1(n): return sum(d for d in range(1, n+1) if n % d == 0)

    def theta3(tau):
        return mp.jtheta(3, 0, mp.e**(1j*mp.pi*tau))

    def E2(tau):
        q = mp.e**(2j*mp.pi*tau); s = mp.mpf(1)
        for n in range(1, 200):
            t = -24*sigma1(n)*q**n; s += t
            if abs(t) < mp.mpf(10)**(-30): break
        return s

    def false_theta(tau):
        q = mp.e**(1j*mp.pi*tau); s = mp.mpf(0)
        for n in range(0, 400):
            t = (-1)**n * q**(mp.mpf(n*(n+1))/2); s += t
            if abs(t) < mp.mpf(10)**(-30): break
        return s

    cases = [
        ("Jacobi theta3 (k=1/2, theta mult.)", theta3,      mp.mpf(1)/2, 'theta', "modular"),
        ("E2 Eisenstein (k=2)",                E2,          mp.mpf(2),   None,    "quasi-modular"),
        ("false theta (k=1/2, theta mult.)",   false_theta, mp.mpf(1)/2, 'theta', "non-modular"),
    ]
    allok = True
    for label, f, k, mult, expected in cases:
        v = eml_mod(f, k, multiplier=mult)
        ok = (v == expected)
        if not ok: allok = False
        print(f"   {label:<38} -> {v:<16} {'OK' if ok else 'FAIL (exp '+expected+')'}")
    print("-" * 72)
    print(f"eml_mod sound: modular / quasi-modular / non-modular. {'PASS' if allok else 'FAIL'}")
