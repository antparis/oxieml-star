#!/usr/bin/env python3
"""
ginibre_sweep.py
================
CERTIFIER-mode test of axis A (poly-analytic order) on the Ginibre / polyanalytic
random-matrix ensemble -- a NATIVELY COMPLEX physical object (non-Hermitian RMT
eigenvalues; passes SPARC at criterion (a)).

Question: does the polyanalytic (higher-Landau-level) Ginibre kernel fill the EMPTY
cell "genuine ANTI at finite poly-analytic order" in a way that survives SPARC and is
carried by a MEASURABLE observable?

Bulk kernel of the q-polyanalytic ensemble (w0 = 1 fixed second point):
    K_q(z,w) = e^{z w0bar - (|z|^2+|w0|^2)/2} * L_{q-1}(|z-w0|^2)
             = e^{-|z-w0|^2/2} * e^{i Im(z w0bar)} * L_{q-1}(|z-w0|^2)
    with L_0 = 1 (ordinary Ginibre), L_1(x) = 1 - x (q=2).

Structural split (exact):
    radial   = e^{-|z-w0|^2/2}            -> measurable envelope (real)
    cocycle  = e^{(z w0bar - zbar w0)/2}  -> GAUGE factor (magnetic translation)
    Laguerre = L_{q-1}(|z-w0|^2)          -> polyanalytic prefactor

DECISIVE SPARC CONTROL: strip the gauge cocycle (a gauge choice). If the kernel's ANTI
verdict disappears (-> REAL/MODULE), the anti was a GAUGE ARTEFACT and FAILS SPARC.

Predicted [DERIVATION]: the full q=2 kernel reads ANTI (finite poly order) but its anti is
entirely gauge -> gauge-stripped reads REAL; the measurable correlation |K|^2 reads REAL.
=> Ginibre does NOT fill the chiral cell. It is a GAUGE wall (a sub-type of observable wall).

AUTHORITY: judge_v2 on Anthony's machine is the sole arbiter. Oracle = unit-test expectation.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp

try:
    from judge_v2 import z, zbar, certify_1field
    HAVE_JUDGE = True
except Exception as e:
    print(f"[WARN] judge_v2 not importable ({e}); ORACLE-ONLY (no certification).")
    z, zbar = sp.symbols('z zbar')
    HAVE_JUDGE = False

HOL, ANTI, REAL, MOD = "HOL", "ANTI", "REAL_TRAPPED", "MODULE_TRAPPED"
_m = sp.symbols('__mod__', positive=True)


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def _full_conj(e):
    t = sp.Symbol('__t__')
    return e.subs(sp.I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -sp.I)


def oracle(f):
    if _isz(sp.diff(f, zbar)):
        return HOL
    if _isz(sp.simplify(f - _full_conj(f))):
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


# ----- forms (w0 = 1) -----
w, wb = sp.Integer(1), sp.Integer(1)
zmw, zbmwb = (z - w), (zbar - wb)
L0 = sp.Integer(1)
L1 = 1 - zmw * zbmwb

cocycle  = sp.exp((z*wb - zbar*w) / 2)
radial   = sp.exp(-(zmw * zbmwb) / 2)
Kq1      = radial * cocycle * L0
Kq2      = radial * cocycle * L1
Kq1_str  = radial * L0                      # gauge-stripped q1
Kq2_str  = radial * L1                      # gauge-stripped q2  (DECISIVE control)
corr2    = sp.exp(-(zmw * zbmwb)) * (L1**2)  # |K_q2|^2 envelope (measurable)

# (id, form, expected, role)
GRID = [
    ("ctrl_anti",            sp.log(zbar),  ANTI, "control"),
    ("ctrl_real",            z*zbar,        REAL, "control"),
    ("cocycle_1pt",          cocycle,       ANTI, "gauge factor alone (non-observable)"),
    ("radial_envelope",      radial,        REAL, "measurable modulus"),
    ("ginibre_q1_kernel",    Kq1,           MOD,  "ordinary Ginibre kernel, 1-pt"),
    ("ginibre_q1_gaugestrip",Kq1_str,       REAL, "q1 kernel minus gauge -> real"),
    ("ginibre_q2_kernel",    Kq2,           ANTI, "q=2 polyanalytic kernel, 1-pt (finite-order ANTI)"),
    ("ginibre_q2_gaugestrip",Kq2_str,       REAL, "DECISIVE SPARC: q2 minus gauge -> REAL = anti was gauge"),
    ("ginibre_corr_modsq_q2",corr2,         REAL, "measurable correlation |K|^2 (observable)"),
]


def main():
    print("=" * 100)
    print("GINIBRE / POLYANALYTIC SWEEP  (axis A: poly-analytic order, CERTIFIER mode)")
    print("authority = judge_v2 (this machine);  oracle = independent unit-test expectation")
    print("=" * 100)
    print(f"{'id':24s} {'oracle':14s} {'judge':14s} {'agree':6s} role")
    print("-" * 100)

    n_ok = n_tot = 0
    diss = []
    for cid, f, exp, role in GRID:
        orc = oracle(f)
        assert orc == exp, f"ORACLE MISMATCH {cid}: oracle={orc} expected={exp}"
        if HAVE_JUDGE:
            jv = normalize(certify_1field(f))
            agree = "OK" if jv == orc else "XX"
            n_tot += 1
            n_ok += (jv == orc)
            if jv != orc:
                diss.append((cid, orc, jv))
        else:
            jv, agree = "--", "--"
        print(f"{cid:24s} {orc:14s} {jv:14s} {agree:6s} {role}")

    print("-" * 100)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {n_ok}/{n_tot} agree")
        for cid, orc, jv in diss:
            print(f"  DISAGREE {cid}: oracle={orc} judge={jv}")

    print("\nSPARC verdict on Ginibre (axis A):")
    print("  - ginibre_q2_kernel reads ANTI at FINITE poly-analytic order (fills the math cell), BUT")
    print("  - ginibre_q2_gaugestrip reads REAL: the anti is ENTIRELY in the gauge cocycle,")
    print("    removable by a gauge choice -> FAILS SPARC -> artefact.")
    print("  - ginibre_corr_modsq_q2 (the MEASURABLE observable) reads REAL.")
    print("  => Ginibre does NOT fill the chiral cell. GAUGE WALL (sub-type of observable wall).")

    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
