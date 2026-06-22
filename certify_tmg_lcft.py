#!/usr/bin/env python3
"""
certify_tmg_lcft.py -- CERTIFIER run: pass closed-form correlators of the
topologically-massive-gravity (TMG) logarithmic CFT to judge_v2.

CONTEXT
-------
TMG at the chiral point (mu*l=1) is dual to a c=0 LCFT with c_L=0, c_R=3l/G,
b=-3l/G (Skenderis-Taylor-van Rees 0906.4926). It is the cleanest SOLVED
PARITY-BROKEN LCFT (c_L != c_R). The stress-tensor log partner t has weight
(h,hbar)=(2,0): the Jordan cell sits in ONE chiral sector. Standard c=0 LCFT
2-point function:  <t(z)t(0)> ~ (theta - 2b log z)/z^4  -> function of z only.

QUESTION (the live frontier): does this parity-broken solved LCFT realize the
escape form (spinful prefactor h!=hbar both nonzero x UNPAIRED log zbar) that
this session's calibration certified as genuine anti? Prediction: NO -- the log
sits on a weight-(2,0) sector, so the chiral correlator is holomorphic (eml),
its parity image is pure-anti (a chiral half), and the full local correlator is
module-trapped. The qualifying spinful-unpaired form is NOT produced by TMG.

This script CERTIFIES that statement on closed forms (CERTIFIER mode, not PySR).

AUTHORITY: judge_v2 on Anthony's machine is the sole arbiter. The in-script
oracle (log-derivative criterion L = zbar*d/dzbar(log f), |z|^2-only -> module)
is the expected value of a unit test, indicative only.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field

HOLO, ANTI, REAL, MODULE = "holomorphic", "anti-holomorphic", "real-trapped", "module-trapped"

def normalize(verdict):
    s = str(verdict).strip().lower()
    if "module" in s:                   return MODULE
    if "real" in s:                     return REAL
    if "anti" in s or "mixed" in s:     return ANTI
    if "holo" in s and "anti" not in s: return HOLO
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
    if z not in L_mod.free_symbols:
        return MODULE
    return ANTI

# theta=1, b=1 (constants irrelevant to the holomorphy class); hbar=1 for full-local
CASES = [
    ("TMG chiral-left  (1-2logz)/z^4         (h,hbar)=(2,0)", (1 - 2*sp.log(z))/z**4,            HOLO,
     "log sits on holomorphic sector -> eml, NOT eml*"),
    ("TMG parity-image (1-2logzbar)/zbar^4    (h,hbar)=(0,2)", (1 - 2*sp.log(zbar))/zbar**4,      ANTI,
     "pure anti, but a CHIRAL HALF -> observable wall"),
    ("TMG full-local   zbar^-2*(1-2logz)/z^4  (h!=hbar)",      zbar**(-2)*(1 - 2*sp.log(z))/z**4, MODULE,
     "holo log x spinful power -> removable -> module"),
    ("TARGET unpaired  z^-2 zbar^-1 (1+logzbar)  (NOT in TMG)", z**(-2)*zbar**(-1)*(1 + sp.log(zbar)), ANTI,
     "the escape form TMG does NOT realize"),
]

def main():
    print("=" * 84)
    print("CERTIFIER: TMG / chiral-gravity LCFT closed forms (parity-broken, c_L!=c_R)")
    print("=" * 84)
    print(f"{'case':54s} {'judge':16s} {'oracle':16s} ok")
    print("-" * 84)
    n_ok = 0
    for name, f, expect, _note in CASES:
        try:
            jv = normalize(certify_1field(f))
        except Exception as exc:
            jv = "JUDGE_ERROR:" + type(exc).__name__
        ov = oracle(f)
        ok = (jv == ov == expect)
        n_ok += int(ok)
        print(f"{name:54s} {jv:16s} {ov:16s} {'PASS' if ok else 'DIFF'}")
    print("-" * 84)
    print(f"{n_ok}/{len(CASES)} judge==oracle==expected")
    print()
    print("VERDICT if all PASS:")
    print("  TMG's parity breaking puts the transcendental log in ONE chiral sector")
    print("  (weight (2,0)): chiral correlator = HOLO (eml); parity image = pure-anti")
    print("  chiral half; full local correlator = MODULE-trapped. The spinful-unpaired")
    print("  anti form (TARGET) is real and judge-anti, but is NOT produced by TMG.")
    print("  => The solved parity-broken LCFT does NOT fill the chiral cell.")
    print("     Reason: 'spinful' (both weights nonzero) and 'unpaired log' (parity")
    print("     broken) are in structural tension in solved LCFTs. Cell stays EMPTY.")

if __name__ == "__main__":
    main()
