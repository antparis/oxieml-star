#!/usr/bin/env python3
"""
calib_all_eml.py -- Calibrate judge_v2 across ALL three operators + the spin axis.

Covers, in one systematic matrix (holo AND anti columns + walls + orthogonal axis):
  eml   (holomorphic, d/dzbar=0)    : z^2, exp(z), 1/z          -> holomorphic
  eml*  (anti-holomorphic)          : log(zbar), exp(zbar), 1/zbar -> anti-holomorphic
  eml0  (pure phase)                : z/zbar, |z|^(2i)          -> module-trapped
  REAL trap (SPARC)                 : z*zbar                    -> real-trapped
  ORTHOGONAL AXIS (conformal spin)  : spinful log-operator forms, h=1, hbar=1/2
        PAIRED   a+b log|z|^2  (b=bbar)   -> module-trapped  (transcendental but removable)
        UNPAIRED a+ log zbar   (b=0)      -> anti-holomorphic
        ASYMM    a+ log z+2log zbar       -> anti-holomorphic

The point: the tool must be IRREPROACHABLE on holomorphic (never call eml "anti"),
correct on the two walls (eml0 phase and SPARC real are NOT genuine anti), and the
ONLY forms that escape to genuine anti are the UNPAIRED/ASYMMETRIC spinful logs
(b != bbar), which physically requires parity breaking. |z|^(2i) re-confirms the
2026-06-22 module patch survives.

INDEPENDENT ORACLE (not the judge): log-derivative criterion
  L = zbar * d/dzbar(log f);  module-trapped iff L is |z|^2-only (real or pure-imag).
AUTHORITY: judge_v2 on Anthony's machine is the sole arbiter. The oracle is the
expected value of a unit test. No verdict here is valid until RUN on his machine.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field

HOLO, ANTI, REAL, MODULE = "holomorphic", "anti-holomorphic", "real-trapped", "module-trapped"

def normalize(verdict):
    s = str(verdict).strip().lower()
    if "module" in s:                       return MODULE
    if "real" in s:                         return REAL
    if "anti" in s or "mixed" in s:         return ANTI
    if "holo" in s and "anti" not in s:     return HOLO
    return "UNRECOGNIZED:" + str(verdict)

_m = sp.symbols("__mod__", positive=True)

def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False

def _full_conj(e):
    t = sp.Symbol("__conj_tmp__")
    return e.subs(sp.I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -sp.I)

def oracle(f):
    if _isz(sp.diff(f, zbar)):
        return HOLO
    if _isz(sp.simplify(f - _full_conj(f))):
        return REAL
    if _isz(sp.diff(f, z)):
        return ANTI
    L = sp.simplify(zbar * sp.diff(sp.log(f), zbar))
    L_mod = sp.simplify(L.subs(zbar, _m / z))
    if z not in L_mod.free_symbols:          # depends on |z|^2 only -> removable
        return MODULE
    return ANTI

pref = z**(-2) * zbar**(-1)                  # spinful prefactor: h=1, hbar=1/2
CASES = [
    ("eml   HOLO  z^2",                  z**2,                                    HOLO),
    ("eml   HOLO  exp(z)",               sp.exp(z),                               HOLO),
    ("eml   HOLO  1/z",                  1/z,                                     HOLO),
    ("eml*  ANTI  log(zbar)",            sp.log(zbar),                            ANTI),
    ("eml*  ANTI  exp(zbar)",            sp.exp(zbar),                            ANTI),
    ("eml*  ANTI  1/zbar",               1/zbar,                                  ANTI),
    ("eml0  PHASE z/zbar",               z/zbar,                                  MODULE),
    ("eml0  PHASE |z|^(2i)",             (z*zbar)**sp.I,                          MODULE),
    ("REAL  trap  z*zbar",               z*zbar,                                  REAL),
    ("ORTHO PAIRED   log|z|^2 (b=bbar)", pref*(1 + sp.log(z*zbar)),               MODULE),
    ("ORTHO UNPAIRED log zbar (b=0)",    pref*(1 + sp.log(zbar)),                 ANTI),
    ("ORTHO ASYMM    logz+2logzbar",     pref*(1 + sp.log(z) + 2*sp.log(zbar)),   ANTI),
]

def main():
    print("=" * 80)
    print("judge_v2 calibration: eml / eml* / eml0 + orthogonal spin axis")
    print("=" * 80)
    print(f"{'case':36s} {'judge':16s} {'oracle':16s} {'expect':16s} ok")
    print("-" * 80)
    n_ok = 0
    holo_clean = True
    for name, f, expect in CASES:
        try:
            jv = normalize(certify_1field(f))
        except Exception as exc:
            jv = "JUDGE_ERROR:" + type(exc).__name__
        ov = oracle(f)
        ok = (jv == ov == expect)
        n_ok += int(ok)
        if expect == HOLO and jv == ANTI:
            holo_clean = False               # the unforgivable error: holo called anti
        print(f"{name:36s} {jv:16s} {ov:16s} {expect:16s} {'PASS' if ok else 'DIFF'}")
    print("-" * 80)
    print(f"{n_ok}/{len(CASES)} judge==oracle==expected")
    print(f"holomorphic irreproachable (no eml mislabelled anti): {holo_clean}")
    print()
    print("Reading guide:")
    print("  eml  -> holomorphic   : tool must NEVER call these anti (irreproachable on holo).")
    print("  eml* -> anti          : genuine transcendental anti (log/exp/pole in zbar).")
    print("  eml0 -> module-trapped: pure phase carries no independent anti info (removable).")
    print("  REAL -> real-trapped  : the SPARC trap.")
    print("  ORTHO: only UNPAIRED/ASYMM (b!=bbar) escape to anti -> needs parity breaking.")
    print("  DIFF on ORTHO PAIRED  : judge blind spot (log-on-modulus) -> diagnose before IQH.")

if __name__ == "__main__":
    main()
