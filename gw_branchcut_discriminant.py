#!/usr/bin/env python3
"""
gw_branchcut_discriminant.py -- does the QNM Green-function branch cut give eml* or eml+period?

Adversarial prediction [DERIVATION]: the retarded Green function G(omega) is analytic in the upper
half omega-plane (causality / Titchmarsh). Its poles (QNM) and branch cut (Price tail from
curvature backscattering) are singularities of omega ALONE -> G is HOLOMORPHIC in omega
(dbar_omega G = 0) -> eml + a de Rham/residue PERIOD obstruction, NOT eml*. The measured power
spectrum |G|^2 is REAL -> real-trapped. Genuine eml* (independent log omega-bar) is FORBIDDEN by
causality -- same lock as Kramers-Kronig closed the modular front by reality.

Here z == omega, zbar == omega-bar. Discriminant: judge each closed form holo (eml) vs anti (eml*).
If all causal Green objects read HOL and the spectrum reads REAL, the GW front closes by causality.

AUTHORITY: judge_v2 on Anthony's machine. Oracle = independent unit-test expectation.
Author: Anthony Monnerot, 2026.
"""
import sympy as sp

try:
    from judge_v2 import z, zbar, certify_1field
    HAVE_JUDGE = True
except Exception as e:
    print(f"[WARN] judge_v2 not importable ({e}); ORACLE-ONLY (indicative).")
    z, zbar = sp.symbols('z zbar')
    HAVE_JUDGE = False

HOL, ANTI, REAL, MOD = "HOL", "ANTI", "REAL_TRAPPED", "MODULE_TRAPPED"
_m = sp.symbols('__m__', positive=True)
wc  = 1 - sp.I        # complex QNM frequency omega_c (a constant)
wcb = 1 + sp.I        # its conjugate omega-bar_c


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def _conj(e):
    t = sp.Symbol('__t__')
    return e.subs(sp.I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -sp.I)


def oracle(f):
    if _isz(sp.diff(f, zbar)):
        return HOL
    if _isz(sp.simplify(f - _conj(f))):
        return REAL
    if _isz(sp.diff(f, z)):
        return ANTI
    L = sp.simplify(zbar * sp.diff(sp.log(f), zbar))
    if z not in sp.simplify(L.subs(zbar, _m / z)).free_symbols:
        return MOD
    return ANTI


def normalize(v):
    s = str(v).strip().lower()
    if "module" in s:                   return MOD
    if "real" in s:                     return REAL
    if "anti" in s or "mixed" in s:     return ANTI
    if "hol" in s and "anti" not in s:  return HOL
    return "?:" + str(v)


GRID = [
    ("qnm_pole  1/(w-w_c)",            1/(z - wc),                       HOL,  "QNM resonance pole (omega-singularity)"),
    ("branch_cut_log  log(w-w_c)",     sp.log(z - wc),                   HOL,  "Price-tail branch cut (omega-singularity)"),
    ("branch_power (w-w_c)^(1/2)",     (z - wc)**sp.Rational(1, 2),      HOL,  "fractional branch (omega-singularity)"),
    ("two_pole +-m (Kerr split)",      1/(z-wc) + 1/(z-(2-sp.I)),        HOL,  "spin-split +m/-m poles (still omega-only)"),
    ("power_spectrum |G|^2",           1/((z-wc)*(zbar-wcb)),            REAL, "measured power spectrum (real)"),
    ("ctrl_eml_star  log(w-bar)",      sp.log(zbar - wcb),               ANTI, "eml* signature (forbidden by causality)"),
    ("ctrl_holo  w^2",                 z**2,                             HOL,  "holomorphic control (eml)"),
]


def main():
    print("=" * 100)
    print("GW BRANCH-CUT DISCRIMINANT -- QNM Green function: eml (holo+period) vs eml* (anti)")
    print("=" * 100)
    print(f"{'object':34s} {'oracle':14s} {'judge':14s} {'agree':6s} role")
    print("-" * 100)
    nok = ntot = 0
    diss = []
    for name, f, exp, role in GRID:
        orc = oracle(f)
        assert orc == exp, f"ORACLE MISMATCH {name}: oracle={orc} expected={exp}"
        if HAVE_JUDGE:
            jv = normalize(certify_1field(f))
            agree = "OK" if jv == orc else "XX"
            ntot += 1
            nok += (jv == orc)
            if jv != orc:
                diss.append((name, orc, jv))
        else:
            jv, agree = "--", "--"
        print(f"{name:34s} {orc:14s} {jv:14s} {agree:6s} {role}")
    print("-" * 100)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {nok}/{ntot} agree")
        for name, orc, jv in diss:
            print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("VERDICT [DERIVATION]: GW front closes by CAUSALITY.")
    print("  Every causal Green-function object (poles, branch cut, fractional branch, spin-split")
    print("  poles) is HOLOMORPHIC in omega -> eml + de Rham/residue PERIOD, NOT eml*. The measured")
    print("  power spectrum |G|^2 is REAL_TRAPPED. Genuine eml* (independent log omega-bar) is")
    print("  forbidden by causality (Titchmarsh), the analogue of the reality lock that closed the")
    print("  modular front. Branch cut = holomorphic-period wall, not the chiral cell.")
    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
