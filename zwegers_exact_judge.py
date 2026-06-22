#!/usr/bin/env python3
"""
zwegers_exact_judge.py -- Test the EXACT Zwegers completion of Ramanujan's 3rd-order
mock theta f(q) at the corrected judge, to confirm the anti-holomorphic verdict survives
on the exact object (not an artefact of the sandbox simplification with integer exponents).

EXACT forms (from the Zwegers/Zagier research, FINDINGS context):
  shadow      g3(tau) = sum_{n} (-12/n) n q^(n^2/24)   [weight 3/2 unary theta]
  derivative  d hat/d taubar  ~  y^(-1/2) * conj(g3)    [k=1/2, y=Im(tau) REAL]
  completion  R3(tau) = sum_{n≡1(6)} sgn(n) beta(n^2 y/6) q^(-n^2/24)
              beta(x) = uppergamma(1/2, pi x)/sqrt(pi)   [erfc form]
  full        f_hat = q^(-1/24) f(q) + R3

KEY QUESTION: does the REAL factor y = Im(tau) = (tau-taubar)/2i reduce the anti to a wall
(module/real, like the 6 previous systems) or does the anti survive (genuine transcendental
irreducible, living in the FORMAL completion -- criterion (c) measurability NOT met since
the completion is a mathematical object, not the measurable mock theta f(q) which is holomorphic)?

Controls show: y^(-1/2) alone and uppergamma(1/2,pi*y) alone are real-trapped; the test is
whether multiplying conj(g3) by them keeps anti (modulation, not reduction).

Each step has its own try/except so a slow step does not block the others.
Run detached (no global timeout):
  setsid nohup python3 -u zwegers_exact_judge.py > zwegers_exact_judge.log 2>&1 &
"""
import sympy as sp
from judge_v2 import z as tau, zbar as taubar, certify_1field, full_conj

I = sp.I


def verdict(expr):
    v, _ = certify_1field(expr)
    return v


def step(label, expr, expected_note=""):
    print(f"\n[{label}]  {expected_note}", flush=True)
    try:
        v = verdict(expr)
        print(f"    juge -> {v}", flush=True)
        return v
    except Exception as e:
        print(f"    ERREUR {type(e).__name__}: {e}", flush=True)
        return None


def kron_12(n):
    """Kronecker symbol (-12/n): +1 if n≡1,11 mod12 ; -1 if n≡5,7 mod12 ; else 0."""
    return {1: 1, 11: 1, 5: -1, 7: -1}.get(n % 12, 0)


q = sp.exp(2*sp.pi*I*tau)
y = (tau - taubar)/(2*I)   # Im(tau), REAL
NMAX = 13                  # truncation: n = 1,5,7,11,13

print("=" * 76)
print("ZWEGERS EXACT COMPLETION at corrected judge -- f(q) order 3")
print("=" * 76)
print(f"y = Im(tau) real? y - conj(y) = {sp.simplify(y - full_conj(y))}", flush=True)

# exact shadow g3 (weight 3/2)
g3 = sum(kron_12(n)*n*q**(sp.Rational(n*n, 24)) for n in range(1, NMAX+1) if kron_12(n) != 0)
g3_conj = full_conj(g3)

# (a) the derivative y^(-1/2) * conj(g3)
step("a) derivative y^(-1/2)*conj(g3)", y**(-sp.Rational(1, 2)) * g3_conj,
     "EXPECT: anti if real factor only modulates")

# (b) R3 completion term (exact, with incomplete gamma in y)
beta = lambda x: sp.uppergamma(sp.Rational(1, 2), sp.pi*x)/sp.sqrt(sp.pi)
R3 = sum(sp.sign(n)*beta(sp.Rational(n*n, 6)*y)*q**(-sp.Rational(n*n, 24))
         for n in range(1, NMAX+1) if (n % 6) == 1)
step("b) R3 = sum beta(n^2 y/6) q^(-n^2/24)", R3, "EXPECT: anti (the non-holo completion term)")

# (c) full completion f_hat = q^(-1/24) f(q) + R3
f_mock = q**(-sp.Rational(1, 24)) * (1 + q + q**2 - q**5 + q**7)  # truncated holomorphic mock part
f_hat = f_mock + R3
step("c) full f_hat = q^(-1/24)f(q) + R3", f_hat, "EXPECT: anti (completion carries it)")

# (d) the bare mock theta f(q) itself -- MEASURABLE object, must be holomorphic
step("d) bare f(q) (measurable, holomorphic)", f_mock, "EXPECT: holomorphic (criterion c)")

# controls
print("\n--- CONTROLS ---", flush=True)
step("conj(g3) alone", g3_conj, "EXPECT: anti (function of taubar)")
step("y^(-1/2) alone (real factor)", y**(-sp.Rational(1, 2)), "EXPECT: real-trapped")
step("uppergamma(1/2,pi*y) alone", sp.uppergamma(sp.Rational(1, 2), sp.pi*y), "EXPECT: real-trapped")

print("\n" + "=" * 76)
print("READING: if (a),(b),(c) anti while y-factors alone are real -> the real factor")
print("MODULATES but does NOT reduce the anti. Distinct from the 6 walls. BUT the anti")
print("lives in the COMPLETION (formal); bare f(q) in (d) is holomorphic (measurable).")
print("=> confirms half-1 (anti exists in formal), not half-2 (not in measurable).")
