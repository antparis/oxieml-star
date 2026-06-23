#!/usr/bin/env python3
"""
v1d_modular.py -- CERTIFIER test of the forced tau-bar dependence of modular completions.

Front: "forced anti in the moduli variable tau" (here tau == z, taub == zbar for judge_v2).
Adversarial result: the modular front SPLITS into two walls, neither filling the chiral cell.

  (W1) quasi-modular / holomorphic-anomaly: completion of E2 is
         E2*(z,zbar) = E2(z) - 3/(pi*Im z),  Im z = (z-zbar)/(2i).
       The forced part -3/(pi*Im z) is REAL-valued -> mirror -> REAL_TRAPPED.
       dbar E2* != 0 (anti EXISTS, forced by modularity) BUT it is the forced reflection of a real
       correction, NOT independent. FAILS criterion (b). "forced != chiral".

  (W2) mock modular (Zwegers): completion's non-holomorphic Eichler integral is genuinely COMPLEX
       -> ANTI (passes (b)) but not a measured observable -> FAILS (c). (project-known, reconfirmed.)

Deep reason (navigation law, reinforced): physical observables here (free energies, couplings,
partition functions) are REAL-valued -> forced tau-bar part is the mirror (real-trapped). Genuine
chiral anti needs a NATIVELY COMPLEX measurable (amplitude/phase), not a real free energy.

AUTHORITY: judge_v2 on Anthony's machine (z,zbar). Oracle = independent unit-test expectation.
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


y = (z - zbar) / (2*sp.I)
E2_star_nh = -3/(sp.pi*y)
mock_schem = sp.exp(2*sp.I*sp.pi*zbar)/(z - zbar)
E4 = sp.Function('E4')(z)
E6 = sp.Function('E6')(z)

GRID = [
    ("E2star_completion -3/(pi Im z)", E2_star_nh, REAL, "W1: forced but REAL -> fails (b)"),
    ("mock_completion_schematic",      mock_schem, ANTI, "W2: complex anti -> passes (b), fails (c)"),
    ("E4(z) holomorphic",              E4,         HOL,  "holomorphic control (eml)"),
    ("E6(z) holomorphic",              E6,         HOL,  "holomorphic control (eml)"),
    ("y = Im z (real control)",        y,          REAL, "real control"),
    ("z^2 (holo control)",             z**2,       HOL,  "holo control"),
    ("z/zbar (module control)",        z/zbar,     MOD,  "module control (eml0)"),
]


def main():
    print("=" * 100)
    print("v1d MODULAR (CERTIFIER) -- forced tau-bar dependence of modular completions")
    print("=" * 100)
    print(f"{'object':36s} {'oracle':14s} {'judge':14s} {'agree':6s} note")
    print("-" * 100)
    nok = ntot = 0
    diss = []
    for name, f, exp, note in GRID:
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
        print(f"{name:36s} {orc:14s} {jv:14s} {agree:6s} {note}")
    print("-" * 100)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {nok}/{ntot} agree")
        for name, orc, jv in diss:
            print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("dbar E2* =", sp.simplify(sp.diff(E2_star_nh, zbar)),
          "  (anti EXISTS, forced; but E2* completion is REAL -> mirror)")
    print()
    print("VERDICT [DERIVATION]: modular/tau front is a DOUBLE WALL.")
    print("  W1 E2*/holomorphic-anomaly: forced anti is REAL -> real-trapped -> fails (b).")
    print("  W2 mock modular: complex anti -> passes (b) but not measured -> fails (c).")
    print("  Real observables (free energy/coupling/partition fn) -> mirror. Chiral anti needs a")
    print("  NATIVELY COMPLEX measurable (amplitude/phase), not a real free energy.")
    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
