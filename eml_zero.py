#!/usr/bin/env python3
"""eml_zero.py -- standalone pure-phase detector (eml-zero), the third operator of the eml family.

The eml family (Anthony Monnerot), three complementary local detectors on a complex field f(z,zbar):
  eml   (holomorphic)  : df/dzbar == 0  -> f depends on z alone
  eml*  (anti-holo)    : judge_v2.certify_1field -> holo / real-trapped / module-trapped / anti
  eml0  (pure phase)   : |f|^2 = f*conj(f) is CONSTANT while f varies -> f is a pure winding phase

eml0 gives a POSITIVE characterization of the pure-phase sub-class of the module-trapped walls
(|z|^(is), winding (z/zbar)^n): objects that rotate without changing amplitude. It complements
eml* (which tests df/dzbar) by testing the MODULUS instead.

Calibrated & established on machine 2026-06-22 (FINDINGS_20260622j). Reuses judge_v2.full_conj
for the FULL conjugation (z<->zbar AND i->-i).

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
from judge_v2 import z, zbar, full_conj


def eml_zero(expr):
    """Pure-phase detector. Returns one of: 'constant', 'pure-phase', 'not-pure-phase'.
    'pure-phase' iff f is non-constant AND |f|^2 = f*full_conj(f) has zero derivative in both
    z and zbar (modulus is constant while f winds)."""
    expr = sp.expand(expr)
    if sp.simplify(sp.diff(expr, z)) == 0 and sp.simplify(sp.diff(expr, zbar)) == 0:
        return "constant"
    mod2 = sp.simplify(expr * full_conj(expr))
    cst = (sp.simplify(sp.diff(mod2, z)) == 0 and sp.simplify(sp.diff(mod2, zbar)) == 0)
    return "pure-phase" if cst else "not-pure-phase"


def is_pure_phase(expr):
    """Boolean convenience wrapper: True iff eml_zero(expr) == 'pure-phase'."""
    return eml_zero(expr) == "pure-phase"


if __name__ == "__main__":
    I = sp.I
    print("=" * 72)
    print("eml_zero self-validation (each line must say OK)")
    print("=" * 72)
    cases = [
        ("z/|z| = e^(i theta)        PURE PHASE", z/sp.sqrt(z*zbar), "pure-phase"),
        ("(z/zbar)^(1/2) winding     PURE PHASE", (z/zbar)**sp.Rational(1, 2), "pure-phase"),
        ("|z|^(is)                   PURE PHASE", (z*zbar)**(I*sp.Rational(1, 2)), "pure-phase"),
        ("(z/|z|)^3 = e^(3i theta)   PURE PHASE", (z/sp.sqrt(z*zbar))**3, "pure-phase"),
        ("z         (module varies)  NOT",        z, "not-pure-phase"),
        ("zbar      (module varies)  NOT",        zbar, "not-pure-phase"),
        ("z+zbar    (real)           NOT",        z + zbar, "not-pure-phase"),
        ("log(zbar)                  NOT",        sp.log(zbar), "not-pure-phase"),
        ("z*zbar = |z|^2 (real)      NOT",        z*zbar, "not-pure-phase"),
        ("1/zbar (Kirsch anti)       NOT",        1/zbar, "not-pure-phase"),
        ("5 (constant)               CONST",      sp.Integer(5), "constant"),
    ]
    allok = True
    for label, expr, expected in cases:
        v = eml_zero(expr)
        ok = (v == expected)
        if not ok:
            allok = False
        print(f"   {label:<40} -> {v:<16} {'OK' if ok else 'FAIL!!'}")
    print("-" * 72)
    print(f"All OK => eml_zero sound: detects pure phase (|f|=const), the 3rd eml operator. {'PASS' if allok else 'FAIL'}")
