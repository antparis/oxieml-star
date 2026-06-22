#!/usr/bin/env python3
"""
superconductor_vortex_probe.py -- Multi-field anti-coupling test on the two-band
superconductor composite vortex, eta=0 (U(1)xU(1), independent phases).

CONTEXT: in the standard type-1.5 regime the Josephson coupling -eta|Psi1||Psi2|cos(t2-t1)
LOCKS the phases (t1=t2), collapsing to a single common phase -> module-trapped (WALL,
Hecke-type). The ONLY escape is eta=0 (independent phases). We test there.

MODEL: near a vortex core, Psi_j = (z/|z|)^{n_j} * exp(-c_j*|z|^2)
  (z/|z|)^n = winding-n pure phase; exp(-c|z|^2) = real recovery profile, scale ~1/sqrt(c).

CRITERION (multi-field, calibrated 2026-06-21d): a combination Psi1+Psi2 is anti-
irreducible iff neither holo/real/module, confirmed by BOTH judge_v2 AND the
independent rotation oracle (R=z*d/dz - zbar*d/dzbar; module iff R(f)/f is z-only).

SANDBOX RESULT (to confirm here): the flip to anti is driven by DIFFERENT WINDINGS
(n1 != n2), NOT by different scales. Different scale alone stays module.

RESERVATIONS (SPARC, NOT yet lifted -- this is a candidate, not a discovery):
  (1) eta=0 is an idealization (real two-band SC usually has residual Josephson eta!=0);
  (2) is the sum Psi1+Psi2 a NATIVE observable, or posed? (total density |Psi1|^2+|Psi2|^2
      is real; the complex sum is not obviously measured);
  (3) co-located different windings n1!=n2 may be energetically unstable.
Only if all three are answered by physics (forced, not posed) is this Project-A.

Run from ~/Desktop/oxieml-star/ :  python3 superconductor_vortex_probe.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def _verdict(expr):
    out = certify_1field(expr)
    return out[0] if isinstance(out, (tuple, list)) else out


def rot_oracle(f):
    f = sp.expand(f); dz = sp.diff(f, z); dzb = sp.diff(f, zbar)
    if sp.simplify(dzb) == 0:
        return "holomorphic"
    Rf = sp.simplify(z*dz - zbar*dzb)
    try:
        r = sp.simplify(Rf/f)
        return "module" if sp.simplify(sp.diff(r, zbar)) == 0 else "NOT-module"
    except Exception:
        return "ERR"


def psi(n, c):
    return (z/sp.sqrt(z*zbar))**n * sp.exp(-c*z*zbar)


def test(name, f):
    j = _verdict(f); o = rot_oracle(f)
    agree = ((j == "anti-holomorphic" and o == "NOT-module") or
             (j == "module-trapped" and o == "module") or
             (j == "holomorphic" and o == "holomorphic") or
             (j == "real-trapped"))
    print(f"  [{name}] judge={j}  oracle={o}  {'(agree)' if agree else '<-- DISAGREE'}")
    return j, o, agree


print("=" * 80)
print("TWO-BAND SC COMPOSITE VORTEX, eta=0 (independent phases) -- judge_v2 + oracle")
print("=" * 80)
print("\n-- isolated fields (expect module: pure phase x real modulus) --")
test("Psi1 n=1 c=1", psi(1, 1))
test("Psi2 n=2 c=2", psi(2, 2))
print("\n-- same winding, different scale (expect module: scale alone insufficient) --")
test("Psi(1,c=1)+Psi(1,c=2)", psi(1, 1) + psi(1, 2))
print("\n-- DIFFERENT winding, same scale (expect anti: winding drives the flip) --")
test("Psi(n=1,1)+Psi(n=2,1)", psi(1, 1) + psi(2, 1))
print("\n-- different winding AND scale (full type-1.5 config) --")
test("Psi(1,1)+Psi(2,2)", psi(1, 1) + psi(2, 2))
test("Psi(1,1)+Psi(3,2)", psi(1, 1) + psi(3, 2))
print("\n" + "=" * 80)
print("If different-winding combos are anti by BOTH criteria: irreducible anti coupling")
print("in eta=0 regime. STILL a candidate -- 3 SPARC reservations above remain to lift")
print("against real physics (eta=0 forced? sum native? n1!=n2 stable?). NOT a discovery.")
print("=" * 80)
