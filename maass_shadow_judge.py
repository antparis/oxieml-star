#!/usr/bin/env python3
"""maass_shadow_judge.py -- Judge the TRUE Maass weak harmonic shadow term with the 4-label judge.
Exact non-holomorphic part (Bruinier-Funke): f- term = Gamma(1-k, -4*pi*n*y) * q^n,
with q^n = exp(2*pi*i*n*(x+i*y)), x=(z+zbar)/2, y=(z-zbar)/(2i).
The Gamma argument is y=Im(z), NOT |z|^2 -- this is why it may escape module-trap.
Status: INDICATIVE (judge not yet calibrated on this transcendental class in the bench).
Author: Anthony Monnerot, 2026."""
import signal
import sympy as sp
from judge_v2 import z, zbar, certify_1field, full_conj


class TimeoutErr(Exception):
    pass


def _handler(signum, frame):
    raise TimeoutErr()


def with_timeout(fn, seconds):
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(seconds)
    try:
        return fn()
    finally:
        signal.alarm(0)


def build_shadow_term(k, n):
    """Single shadow term Gamma(1-k, -4*pi*n*y) * q^n in (z, zbar).
    x=(z+zbar)/2, y=(z-zbar)/(2i). q^n is holomorphic (function of z only)."""
    x = (z + zbar) / 2
    y = (z - zbar) / (2 * sp.I)
    qn = sp.exp(2 * sp.pi * sp.I * n * x - 2 * sp.pi * n * y)
    arg = -4 * sp.pi * n * y
    return sp.uppergamma(1 - k, arg) * qn


def diagnose(k, n, per_case_seconds=30):
    term = build_shadow_term(k, n)
    out = {"k": str(k), "n": n}
    try:
        verdict = with_timeout(lambda: certify_1field(term), per_case_seconds)
        if isinstance(verdict, tuple):
            verdict = verdict[0]
        out["verdict"] = verdict
    except TimeoutErr:
        out["verdict"] = "TIMEOUT"
        return out
    except Exception as e:
        out["verdict"] = f"ERR:{type(e).__name__}"
        return out
    try:
        dz = with_timeout(lambda: sp.simplify(sp.diff(term, z)), per_case_seconds)
        dzb = with_timeout(lambda: sp.simplify(sp.diff(term, zbar)), per_case_seconds)
        out["d_z_nonzero"] = (dz != 0)
        out["d_zbar_nonzero"] = (dzb != 0)
    except Exception:
        out["d_z_nonzero"] = "?"
        out["d_zbar_nonzero"] = "?"
    return out


def main():
    print("=" * 88)
    print("TRUE Maass weak harmonic shadow term, judged by the 4-label judge (INDICATIVE).")
    print("f- term = Gamma(1-k, -4*pi*n*y) * q^n ;  q^n = e^{2 pi i n z} (holomorphic).")
    print("Gamma argument = y = Im(z), NOT |z|^2.  Question: module-trap (wall) or genuine anti?")
    print("=" * 88)
    n = 1
    for k in [sp.Rational(1, 2), sp.Rational(3, 2), sp.Integer(0), sp.Integer(1), sp.Integer(2)]:
        r = diagnose(k, n, per_case_seconds=30)
        print(f"\n  k={r['k']:<5} n={r['n']}")
        print(f"     verdict        : {r['verdict']}")
        print(f"     d/dz   nonzero : {r.get('d_z_nonzero')}")
        print(f"     d/dzbar nonzero: {r.get('d_zbar_nonzero')}")
    print("\n" + "=" * 88)
    print("READING (INDICATIVE, not bench-certified):")
    print("  module-trapped     -> shadow reducible (WALL, conjecture thickens).")
    print("  anti-holomorphic   -> escapes module-trap (genuine independent anti CANDIDATE, theoretical).")
    print("  real-trapped       -> shadow is real (another wall).")
    print("  TIMEOUT            -> heavy case, needs numeric fallback (not a verdict).")
    print("=" * 88)


if __name__ == "__main__":
    main()
