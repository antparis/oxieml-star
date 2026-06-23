#!/usr/bin/env python3
"""
certify_schrodinger.py -- CERTIFIER run: map the closed-form wavefunctions of
the Schrodinger equation onto judge_v2 (holo / anti / module / real).

FRAMING (decided in this session, see history)
-----------------------------------------------
Hermitian scalar Schrodinger is already closed piece by piece: LLL, higher
Landau levels, Aharonov-Bohm, Laughlin, vortices, real bound states -- all fall
on established walls (module-trapped, real-trapped, holomorphic, or finite-order
removable anti). The half-conjecture 20260622o (hermiticity <-> anti-irreducibility
mutually exclusive) explains WHY: a Hermitian H gives unitary evolution -> the
anti part of psi is reducible. So the orthogonal axis for Schrodinger is NOT the
magnetic field or angular momentum (done) but HERMITICITY ITSELF: only a
NON-Hermitian setting (complex potential / PT-symmetry / resonance) could carry
an irreducible anti. This script certifies that map and re-confirms the tool is
irreproachable on holomorphic.

Status: [ESTABLISHED] for the verdicts once run on machine (capability / calibration,
known textbook forms -- NOT a discovery). The DISPERSIVE PACKET is a frontier case:
oracle predicts anti for a HERMITIAN free solution -> either a new blind spot
(complex quadratic radial phase, cf |z|^(is) patch 20260622d/e) or a subtlety;
the judge on the machine decides. The TARGET (exp(zbar)*gaussian) is the genuine
transcendental-anti form that Hermitian Schrodinger does NOT produce, shown for
contrast.

AUTHORITY: judge_v2 on Anthony's machine is the sole arbiter. The in-script oracle
(L = zbar*d/dzbar(log f); module iff prod_only AND (L_real OR (L_const AND
L_pure_imag))) reproduces judge_v2's criterion and is the expected value only.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field

HOLO, ANTI, REAL, MODULE = "holomorphic", "anti-holomorphic", "real-trapped", "module-trapped"
I = sp.I
_t = sp.symbols("__scale__", positive=True)

def normalize(verdict):
    s = str(verdict).strip().lower()
    if "module" in s:                   return MODULE
    if "real" in s:                     return REAL
    if "anti" in s or "mixed" in s:     return ANTI
    if "holo" in s and "anti" not in s: return HOLO
    return "UNRECOGNIZED:" + str(verdict)

def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False

def _fconj(e):
    s = sp.Symbol("__conj_tmp__")
    return e.subs(I, s).subs({z: zbar, zbar: z}, simultaneous=True).subs(s, -I)

def oracle(f):
    if _isz(sp.diff(f, zbar)):
        return HOLO
    if _isz(sp.simplify(f - _fconj(f))):
        return REAL
    if _isz(sp.diff(f, z)):
        return ANTI
    L = sp.simplify(zbar * sp.diff(sp.log(f), zbar))
    prod_only = _isz(sp.simplify(L.subs({z: _t*z, zbar: zbar/_t}) - L))
    L_real = _isz(sp.simplify(L - _fconj(L)))
    L_const = _isz(sp.diff(L, z)) and _isz(sp.diff(L, zbar))
    L_pure_imag = _isz(sp.simplify(L + _fconj(L)))
    if prod_only and (L_real or (L_const and L_pure_imag)):
        return MODULE
    return ANTI

CASES = [
    ("HOLO  control z^2",                        z**2,                                          HOLO,   "tool must never call holo anti"),
    ("HOLO  control exp(z)",                     sp.exp(z),                                     HOLO,   ""),
    ("ANTI  control exp(zbar)",                  sp.exp(zbar),                                  ANTI,   "genuine transcendental anti"),
    ("ANTI  control log(zbar)",                  sp.log(zbar),                                  ANTI,   ""),
    ("SCHRO real bound state exp(-|z|^2/2)",     sp.exp(-z*zbar/2),                             REAL,   "real wavefunction -> real-trapped"),
    ("SCHRO LLL m=2  z^2 exp(-|z|^2/2)",         z**2*sp.exp(-z*zbar/2),                        MODULE, "holo x gaussian -> module"),
    ("SCHRO Landau n=1  zbar exp(-|z|^2/2)",     zbar*sp.exp(-z*zbar/2),                        MODULE, "finite-order anti, removable"),
    ("SCHRO Aharonov-Bohm z^1.5 zbar^-0.5 gauss", z**sp.Rational(3,2)*zbar**sp.Rational(-1,2)*sp.exp(-z*zbar/4), MODULE, "real exponents -> module"),
    ("SCHRO dispersive packet exp(-|z|^2/(2(1+i)))", sp.exp(-z*zbar/(2*(1+I))),                 ANTI,   "FRONTIER: hermitian but oracle=anti -> blind spot? diagnose"),
    ("TARGET nonherm exp(zbar)exp(-|z|^2/2)",    sp.exp(zbar)*sp.exp(-z*zbar/2),                ANTI,   "transcendental z-bar alone: NOT produced by hermitian Schrodinger"),
]

def main():
    print("=" * 88)
    print("CERTIFIER: Schrodinger closed-form wavefunctions vs judge_v2")
    print("=" * 88)
    print(f"{'case':46s} {'judge':16s} {'oracle':16s} ok")
    print("-" * 88)
    n_ok = 0
    holo_clean = True
    for name, f, expect, _note in CASES:
        try:
            jv = normalize(certify_1field(f))
        except Exception as exc:
            jv = "JUDGE_ERROR:" + type(exc).__name__
        ov = oracle(f)
        ok = (jv == ov == expect)
        n_ok += int(ok)
        if expect == HOLO and jv == ANTI:
            holo_clean = False
        print(f"{name:46s} {jv:16s} {ov:16s} {'PASS' if ok else 'DIFF'}")
    print("-" * 88)
    print(f"{n_ok}/{len(CASES)} judge==oracle==expected")
    print(f"holomorphic irreproachable (no holo mislabelled anti): {holo_clean}")
    print()
    print("Reading guide:")
    print("  All HERMITIAN Schrodinger forms (LLL/Landau/AB/bound state) -> walls")
    print("  (module/real). Confirms hermiticity->reducibility (20260622o). Capability,")
    print("  NOT discovery (textbook forms).")
    print("  DISPERSIVE PACKET: if judge=anti for this hermitian solution, it is a")
    print("  candidate blind spot (complex quadratic radial phase) -> diagnose, do NOT")
    print("  claim a chiral discovery. If judge=module, the criterion already covers it.")
    print("  TARGET: the transcendental z-bar-alone form hermitian Schrodinger cannot")
    print("  produce -> only a NON-Hermitian setting could. That is the open axis.")

if __name__ == "__main__":
    main()
