#!/usr/bin/env python3
"""
kerr_psi4_calibration.py -- CALIBRATION FIRST for the Kerr / Psi4 gravitational-wave front.

Per the navigation law (v1d): genuine chiral anti needs a NATIVELY COMPLEX measurable. The GW
Weyl scalar Psi4 is spin-weight -2 (graviton helicity +-2), so the complex strain h = h+ - i hx
is natively complex (helicity-forced, not an h+,hx encoding). Complex variable z = stereographic
coordinate on the celestial sphere (real conformal geometry of S^2 -> z natively complex). SPARC-pass.

CALIBRATE on KNOWN GW objects before any discovery claim. Adversarial prediction [DERIVATION]:
the "obvious" chiral GW objects are WALLS, not genuine eml*:
  - linear polarization (real strain)         -> REAL_TRAPPED (non-chiral real field)
  - circular polarization (pure helicity phase)-> MODULE_TRAPPED (eml0 phase; |h|=const)
  - pure spin-weight -2 structure              -> MODULE_TRAPPED (orthogonal-axis spin wall)
The genuine eml* target is the FORCED TRANSCENDENTAL structure: the branch cut of the QNM Green
function in complex frequency (Price tail from curvature backscattering) -> log-type ANTI.
Here we (a) confirm the walls on known objects, (b) confirm the tool catches the log target as ANTI.

AUTHORITY: judge_v2 on Anthony's machine. Oracle = independent unit-test expectation.
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


GRID = [
    # controls / reference signatures
    ("ctrl_holo  z^2 (eml)",            z**2,                        HOL,  "holomorphic reference"),
    ("target_sig  log zbar (eml*)",     sp.log(zbar),                ANTI, "the eml* signature we hunt (branch cut)"),
    # known GW objects (calibration baseline)
    ("gw_linear_pol  z+zbar",           z + zbar,                    REAL, "linear polarization, real strain (non-chiral)"),
    ("gw_circular_phase  z/zbar",       z/zbar,                      MOD,  "circular polarization, helicity phase (eml0)"),
    ("gw_spinweight2  zbar^2/(1+|z|^2)^2", zbar**2/(1+z*zbar)**2,    MOD,  "pure spin-weight -2 (orthogonal-axis spin wall)"),
    ("gw_intensity  |Psi|^2  z*zbar",   z*zbar,                      REAL, "measured intensity (real) -> mirror"),
]


def main():
    print("=" * 100)
    print("KERR / PSI4 CALIBRATION -- known GW objects (calibrate before discovery)")
    print("=" * 100)
    print(f"{'object':38s} {'oracle':14s} {'judge':14s} {'agree':6s} role")
    print("-" * 100)
    nok = ntot = 0
    diss = []
    for name, f, exp, role in GRID:
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
        print(f"{name:38s} {orc:14s} {jv:14s} {agree:6s} {role}")
    print("-" * 100)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {nok}/{ntot} agree")
        for name, orc, jv in diss:
            print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("CALIBRATION VERDICT [DERIVATION]:")
    print("  Known chiral GW objects are WALLS: linear pol -> real; circular pol (helicity phase) ->")
    print("  module (eml0); pure spin-weight -2 -> module; measured intensity -> real. None is genuine eml*.")
    print("  The tool DOES catch the target signature log(zbar) -> ANTI (eml*).")
    print("  => DISCOVERY TARGET (next, not now): the branch cut of the QNM Green function in complex")
    print("     frequency (Price tail, forced by curvature) -> log-type ANTI, natively complex, measurable.")
    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
