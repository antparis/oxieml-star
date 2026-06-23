#!/usr/bin/env python3
"""
nonseparable_judge.py -- two-mode (z1,z2) classifier: does a NON-SEPARABLE state carry genuine
chiral anti (eml*), or is it merely HOLOMORPHIC entanglement (eml wall)?

Multi-variable extension of judge_v2 (which is one-field z,zbar). For a two-mode amplitude
f(z1,z2,zbar1,zbar2) it reports, simultaneously:
  base verdict        : HOL / REAL / ANTI / MODULE  (anti content)
  inter-mode separable: f = g(mode1)*h(mode2)?   (d2 log f / d(mode1)d(mode2) = 0)
  chiral factorize    : f = holo(z)*anti(zbar)?   (d2 log f / dz_i dzbar_j = 0)
Refined class:
  HOL + non-separable  -> ENTANGLED HOLO (eml WALL: entanglement != chirality)
  REAL/MODULE          -> WALL (mirror/modulus)
  ANTI + chiral-fact   -> SEPARABLE half-chiral WALL
  ANTI + non-fact      -> ENTANGLED CHIRAL ANTI (the target type)

KEY RESULT: quantum-style entanglement (non-separable but holomorphic, or symmetric chiral
coupling) is a WALL. The ONLY two-mode form reaching the target is a NON-FACTORIZABLE CROSS-MODE
chiral coupling (mode1 holo x mode2 anti, additively, e.g. 1 + pi log z1 + phi log zbar2).
"Entanglement != chirality" -- the seductive quantum analogy is a wall.

AUTHORITY: exact SymPy. judge_v2 is one-field; this extends it (like dolbeault). INDICATIVE until
run on Anthony's machine. (b)+(c) -- physically forced + measurable -- NOT addressed here.
Author: Anthony Monnerot, 2026.
"""
import sympy as sp

z1, z2, zb1, zb2 = sp.symbols('z1 z2 zbar1 zbar2')
ZH, ZA = [z1, z2], [zb1, zb2]
m1, m2 = sp.symbols('m1 m2', positive=True)
I, pi, phi = sp.I, sp.pi, sp.GoldenRatio


def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def fconj(e):
    t = sp.Symbol('__t__')
    return e.subs(I, t).subs({z1: zb1, zb1: z1, z2: zb2, zb2: z2}, simultaneous=True).subs(t, -I)


def is_holo(f):       return all(_isz(sp.diff(f, a)) for a in ZA)
def is_real(f):       return _isz(sp.simplify(f - fconj(f)))
def is_pure_anti(f):  return all(_isz(sp.diff(f, h)) for h in ZH)


def intermode_sep(f):
    L = sp.log(f)
    mode1, mode2 = [z1, zb1], [z2, zb2]
    return all(_isz(sp.diff(sp.diff(L, a), b)) for a in mode1 for b in mode2)


def chiral_fact(f):
    L = sp.log(f)
    return all(_isz(sp.diff(sp.diff(L, h), a)) for h in ZH for a in ZA)


def module_multi(f):
    try:
        for zb, z, mm in [(zb1, z1, m1), (zb2, z2, m2)]:
            L = sp.simplify(zb * sp.diff(sp.log(f), zb))
            if z in sp.simplify(L.subs(zb, mm / z)).free_symbols:
                return False
        return True
    except Exception:
        return False


def classify(f):
    if is_holo(f):          base = "HOL"
    elif is_real(f):        base = "REAL"
    elif is_pure_anti(f):   base = "ANTI"
    elif module_multi(f):   base = "MODULE"
    else:                   base = "ANTI"
    sep, cf = intermode_sep(f), chiral_fact(f)
    if base == "HOL":
        ref = "HOL separable" if sep else "ENTANGLED HOLO (eml WALL)"
    elif base in ("REAL", "MODULE"):
        ref = "WALL (mirror/modulus)"
    elif base == "ANTI" and cf:
        ref = "SEPARABLE half-chiral WALL"
    else:
        ref = "ENTANGLED CHIRAL ANTI (target type)"
    return base, sep, cf, ref


GRID = [
    ("ctrl_holo  z1^2",                       z1**2),
    ("ctrl_anti  log zbar1",                  sp.log(zb1)),
    ("sep_holo  z1*z2",                       z1*z2),
    ("ENT_holo  z1z2+(z1z2)^2",               z1*z2 + (z1*z2)**2),
    ("sep_chiral  z1*zbar2",                  z1*zb2),
    ("real_paired  |z1|^2+|z2|^2",            z1*zb1 + z2*zb2),
    ("EPR_chiral  z1 zbar2 + z2 zbar1",       z1*zb2 + z2*zb1),
    ("chiral_fact_uneq  exp(i pi z1+i phi zbar2)", sp.exp(I*pi*z1 + I*phi*zb2)),
    ("TARGET  1+pi log z1+phi log zbar2",     1 + pi*sp.log(z1) + phi*sp.log(zb2)),
    ("TARGET_eq  1+pi log z1+pi log zbar2",   1 + pi*sp.log(z1) + pi*sp.log(zb2)),
]


def main():
    print("=" * 116)
    print("NON-SEPARABLE JUDGE (two modes) -- entanglement vs chirality")
    print("=" * 116)
    print(f"{'state':42s} {'base':8s} {'sep':6s} {'chiralFact':11s} refined class")
    print("-" * 116)
    for name, f in GRID:
        b, s, c, r = classify(f)
        print(f"{name:42s} {b:8s} {str(s):6s} {str(c):11s} {r}")
    print("-" * 116)
    print("RESULT [DERIVATION]: entanglement != chirality.")
    print("  - Holomorphic entanglement (non-separable but d-bar=0) -> ENTANGLED HOLO = eml WALL.")
    print("  - Symmetric chiral coupling z1 zbar2 + z2 zbar1 (EPR-like) -> REAL = wall.")
    print("  - The ONLY target is a NON-FACTORIZABLE CROSS-MODE chiral coupling (mode1 holo x mode2")
    print("    anti, additive in log): 1 + pi log z1 + phi log zbar2 -> ENTANGLED CHIRAL ANTI.")
    print("  The quantum-entanglement analogy is a WALL; the target is a chiral cross-mode knot.")
    print("  OPEN (b)+(c): is such a cross-mode chiral log FORCED physically and MEASURABLE (interference)?")


if __name__ == "__main__":
    main()
