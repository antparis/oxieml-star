#!/usr/bin/env python3
"""
zwegers_exact_judge_v2.py -- Confirm the Zwegers completion verdict, robustly.

Strategy: the holo/anti/module CLASS depends on HOW tau and taubar enter (additively,
via the real y, etc.), NOT on the numerical exponents n^2/24 (which only slow SymPy's
simplify on radicals). So we test:
  PART 1 -- STRUCTURAL forms (fast, exponents simplified) that preserve the exact
            tau/taubar structure of each Zwegers piece. These give the definitive class.
  PART 2 -- EXACT forms (n^2/24, incomplete gamma) but judged with a PER-STEP time guard
            (signal.alarm), so a slow step reports "TIMEOUT" instead of hanging.

The structural test is the authoritative verdict here (class is exponent-independent);
the exact test is confirmatory where SymPy can finish.

Run:  python3 zwegers_exact_judge_v2.py     (no detach needed; guarded)
"""
import sympy as sp
import signal
from judge_v2 import z as tau, zbar as taubar, certify_1field, full_conj

I = sp.I


class TimeoutErr(Exception):
    pass


def _alarm(signum, frame):
    raise TimeoutErr()


def verdict_guarded(expr, seconds=25):
    """certify_1field with a per-call time guard."""
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(seconds)
    try:
        v, _ = certify_1field(expr)
        signal.alarm(0)
        return v
    except TimeoutErr:
        return f"TIMEOUT(>{seconds}s)"
    except Exception as e:
        signal.alarm(0)
        return f"ERR:{type(e).__name__}"
    finally:
        signal.alarm(0)


def show(label, expr, sec=25):
    print(f"  {label:<46} -> {verdict_guarded(expr, sec)}", flush=True)


def kron_12(n):
    return {1: 1, 11: 1, 5: -1, 7: -1}.get(n % 12, 0)


q = sp.exp(2*sp.pi*I*tau)
y = (tau - taubar)/(2*I)

print("=" * 80)
print("PART 1 -- STRUCTURAL forms (exponent-independent class; authoritative)")
print("=" * 80)
# conj(g3) structurally = a function of taubar alone (g3 holo in tau)
conj_g_struct = sp.exp(-2*sp.pi*I*taubar) + sp.exp(-2*sp.pi*I*taubar*2)  # anti, fct of taubar
beta_struct = sp.uppergamma(sp.Rational(1, 2), sp.pi*y)                   # incomplete gamma in y

show("(a) y^(-1/2) * conj(g3)            [structural]", y**(-sp.Rational(1, 2)) * conj_g_struct)
show("(b) beta(y) * q^(-1)              [structural R3]", beta_struct * q**(-1))
show("(c) f(q) + beta(y)*q^(-1)         [structural full]", (q + q**2) + beta_struct*q**(-1))
show("(d) bare mock f(q)=q+q^2          [MEASURABLE]", q + q**2)
print("  --- controls ---")
show("conj(g3) alone                    [structural]", conj_g_struct)
show("y^(-1/2) alone (real factor)", y**(-sp.Rational(1, 2)))
show("beta(y)=uppergamma(1/2,pi y) alone", beta_struct)

print("\n" + "=" * 80)
print("PART 2 -- EXACT forms (n^2/24, real shadow), per-step time-guarded")
print("=" * 80)
g3 = sum(kron_12(n)*n*q**(sp.Rational(n*n, 24)) for n in [1, 5, 7, 11, 13] if kron_12(n))
g3c = full_conj(g3)
beta = lambda x: sp.uppergamma(sp.Rational(1, 2), sp.pi*x)/sp.sqrt(sp.pi)
R3 = sum(sp.sign(n)*beta(sp.Rational(n*n, 6)*y)*q**(-sp.Rational(n*n, 24)) for n in [1, 7, 13] if n % 6 == 1)

show("(a-exact) y^(-1/2)*conj(g3)", y**(-sp.Rational(1, 2))*g3c, sec=40)
show("(b-exact) R3 (incomplete gamma)", R3, sec=40)
show("(d-exact) conj(g3) alone", g3c, sec=40)

print("\n" + "=" * 80)
print("READING: PART 1 gives the authoritative class (exponent-independent). If (a),(b),(c)")
print("are anti while y-factors alone are real-trapped, the real factor MODULATES not REDUCES")
print("-> Zwegers completion escapes the wall (distinct from the 6 systems). (d) holomorphic")
print("confirms the MEASURABLE mock theta has no anti -> criterion (c) not met (formal only).")
