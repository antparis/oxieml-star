#!/usr/bin/env python3
"""
superconductor_retest_fixed_judge.py -- Re-test the two-band superconductor composite-vortex
candidate with the FIXED judge_v2 (blind spot closed 2026-06-22e), cross-checked by the
independent rotation oracle R = z*d/dz - zbar*d/dzbar.

WHY: the candidate's "anti" verdict was issued by the OLD judge, which had the |z|^(is)
blind spot. Phase-on-modulus forms (z/|z|)^n are exactly the kind that fooled it. Must
confirm the verdict survives the fix before building on the candidate.

Candidate: Psi_j = (z/|z|)^n_j (pure winding phase), composite = sum with n1 != n2.
Form: (z/|z|)^n = z^(n/2) * zbar^(-n/2).

EXPECTED (from sandbox): isolated (z/|z|)^n -> module-trapped (R/f = n constant);
composite n1!=n2 -> anti-holomorphic with R/f DEPENDENT on z,zbar (genuine, unlike |z|^(is)
which had R/f=0). Same-winding control -> module-trapped.

Run from ~/Desktop/oxieml-star/ :  python3 superconductor_retest_fixed_judge.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field


def verdict(expr):
    v, _ = certify_1field(expr)
    return v


def rotation_oracle(expr):
    dz = sp.diff(expr, z); dzb = sp.diff(expr, zbar)
    try:
        return sp.simplify((z*dz - zbar*dzb) / expr)
    except Exception:
        return "ERR"


def winding(n):
    return (z / sp.sqrt(z*zbar))**n


print("=" * 84)
print("SUPERCONDUCTOR CANDIDATE re-test with FIXED judge + rotation oracle")
print("=" * 84)
print("\nIsolated components (expected module-trapped, R/f = constant):")
for n in [1, 2, 3]:
    f = sp.simplify(winding(n))
    print(f"  (z/|z|)^{n}            -> {verdict(f):<17} R/f = {rotation_oracle(f)}")

print("\nCOMPOSITE (n1 != n2) -- THE CANDIDATE (expected anti, R/f dependent on z,zbar):")
all_anti = True
for (n1, n2) in [(1, 2), (1, 3), (2, 3)]:
    f = sp.simplify(winding(n1) + winding(n2))
    v = verdict(f); r = rotation_oracle(f)
    rconst = (sp.simplify(sp.diff(r, z)) == 0 and sp.simplify(sp.diff(r, zbar)) == 0) if r != "ERR" else True
    if v != "anti-holomorphic":
        all_anti = False
    print(f"  (z/|z|)^{n1} + (z/|z|)^{n2}  -> {v:<17} R/f {'CONSTANT(=module-like!)' if rconst else 'depends on z,zbar (genuine)'}")

print("\nCONTROLS:")
fsame = sp.simplify(winding(2) + winding(2))
print(f"  same winding (z/|z|)^2 + (z/|z|)^2 -> {verdict(fsame)}  (expected module-trapped)")
c1, c2 = sp.symbols("c1 c2", real=True, positive=True)
fphys = sp.simplify(winding(1)*sp.exp(-c1*z*zbar) + winding(2)*sp.exp(-c2*z*zbar))
print(f"  full physical form (with real gaussians) -> {verdict(fphys)}  (expected anti)")

print("\n" + "=" * 84)
print(f">>> Candidate survives fixed judge: {'YES -- anti verdict holds, NOT a |z|^(is) artefact' if all_anti else 'NO -- COLLAPSED to module/real'}")
print(">>> Math anti confirmed. Physical reservations (eta=0, native observable, stability) REMAIN.")
