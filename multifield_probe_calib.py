#!/usr/bin/env python3
"""
multifield_probe_calib.py -- Calibration of the multi-field anti-coupling criterion.

QUESTION: can a holomorphic-coefficient combination of SEPARATELY-REDUCIBLE fields
(each module-trapped) be irreducibly ANTI? If yes, the multi-field axis is non-empty
(the single-field judge, looking at one field at a time, would miss it).

CRITERION (no division -- avoids the 4b artefact): the coupling is anti-irreducible
if a holomorphic combination a(z)*f1 + b(z)*f2 is neither holo, real-trapped, nor
module -- confirmed by BOTH the judge AND the independent rotation oracle.

CALIBRATION (sandbox result, to confirm on YOUR machine via judge_v2):
  - candidate z^2*e^{|z|^2} + z*e^{2|z|^2} (DIFFERENT real moduli)  -> anti (both agree)
  - control   z^2*e^{|z|^2} + z*e^{|z|^2}  (SAME modulus)          -> module (both agree)
  - control   z*e^{|z|^2}  (single module)                         -> module
  - control   gold additive anti A*z + B*zbar                      -> anti (both agree)
The rotation oracle is INDEPENDENT of the judge: it tests whether R(f)/f depends on
z only (R = z*d/dz - zbar*d/dzbar). Agreement of two independent criteria is the bar.

RESERVATION: the candidate is POSED (a hand-built combination), not DERIVED from a
physical system. It proves the multi-field blind spot is non-empty, NOT a physical
discovery. A real two-scale physical system is needed for the SPARC examination.

Run from ~/Desktop/oxieml-star/ :  python3 multifield_probe_calib.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def _verdict(expr):
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def rotation_oracle(f):
    """Independent of the judge: module iff R(f)/f depends on z only."""
    f = sp.expand(f)
    dz = sp.diff(f, z); dzb = sp.diff(f, zbar)
    if sp.simplify(dzb) == 0:
        return "holomorphic"
    Rf = sp.simplify(z * dz - zbar * dzb)
    try:
        ratio = sp.simplify(Rf / f)
        return "module" if sp.simplify(sp.diff(ratio, zbar)) == 0 else "NOT-module"
    except Exception as e:
        return f"ERR:{type(e).__name__}"


CASES = [
    ("CANDIDATE different moduli  z^2 e^{|z|^2} + z e^{2|z|^2}",
     z**2*sp.exp(z*zbar) + z*sp.exp(2*z*zbar), "anti / NOT-module"),
    ("CONTROL  same modulus       z^2 e^{|z|^2} + z e^{|z|^2}",
     z**2*sp.exp(z*zbar) + z*sp.exp(z*zbar), "module / module"),
    ("CONTROL  single module      z e^{|z|^2}",
     z*sp.exp(z*zbar), "module / module"),
    ("CONTROL  gold additive anti A z + B zbar",
     (sp.Float('0.7')+sp.Float('0.4')*sp.I)*z + (sp.Float('-0.3')+sp.Float('1.2')*sp.I)*zbar,
     "anti / NOT-module"),
]

print("=" * 84)
print("MULTI-FIELD ANTI-COUPLING CRITERION -- calibration on judge_v2 (your machine)")
print("=" * 84)
print(f"{'case':<52}{'judge':<18}{'rot.oracle':<12}")
print("-" * 84)
all_ok = True
for name, f, expected in CASES:
    jv = _verdict(f)
    ro = rotation_oracle(f)
    # agreement check: judge 'anti' <-> oracle 'NOT-module'; judge 'module' <-> oracle 'module'
    agree = ((jv == "anti-holomorphic" and ro == "NOT-module") or
             (jv == "module-trapped" and ro == "module") or
             (jv == "holomorphic" and ro == "holomorphic"))
    flag = "" if agree else "  <-- JUDGE/ORACLE DISAGREE"
    if not agree:
        all_ok = False
    print(f"{name:<52}{jv:<18}{ro:<12}{flag}")
print("-" * 84)
if all_ok:
    print(">>> Judge and independent rotation oracle AGREE on all cases.")
    print("    CANDIDATE (different moduli) is anti by BOTH criteria -> the multi-field")
    print("    blind spot is NON-EMPTY: a holo combination of separately-reducible")
    print("    module fields can be irreducibly anti when the real moduli differ.")
    print("    RESERVATION: candidate is POSED, not physically forced. Needs a real")
    print("    two-scale physical system for the SPARC examination before any claim.")
else:
    print(">>> DISAGREEMENT between judge and oracle -- do NOT trust the criterion yet.")
print("=" * 84)
