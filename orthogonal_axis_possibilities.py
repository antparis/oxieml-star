#!/usr/bin/env python3
"""
orthogonal_axis_possibilities.py -- run the orthogonal axis (conformal spin s = h - hbar)
on EACH image discussed (pi/the winding, phi/phase, phi/irrational spin, single helix,
double helix as real linking, double helix as amplitudes).

Orthogonal-axis criterion [ESTABLISHED, FINDINGS_20260622r]: for a spinful form
  f = z^(-2h) z^bar^(-2hbar) (a + b log z + bbar log zbar):
    spin alone (powers, even irrational)         -> MODULE_TRAPPED (z^a zbar^b rule)
    paired   log (b=bbar -> log|z|^2)            -> MODULE_TRAPPED
    unpaired log (b!=bbar)                       -> genuine ANTI  (the only escape)
Question tested here: does any phi/pi/helix image escape, or do they all hit known walls?

z = natural complex variable. spin = eigenvalue of R = z d/dz - zbar d/dzbar (if eigenstate).
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
phi = sp.GoldenRatio


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


def spin(f):
    if _isz(f):
        return None
    R = sp.simplify(z*sp.diff(f, z) - zbar*sp.diff(f, zbar))
    s = sp.simplify(R/f)
    return s if not s.free_symbols else "n/a"


def normalize(v):
    s = str(v).strip().lower()
    if "module" in s:                   return MOD
    if "real" in s:                     return REAL
    if "anti" in s or "mixed" in s:     return ANTI
    if "hol" in s and "anti" not in s:  return HOL
    return "?:" + str(v)


P = z**(-2) * zbar**(-1)   # spinful prefactor (h=1, hbar=1/2)

GRID = [
    # (image, closed form, expected, which wall / escape)
    ("single_helix_real    z+zbar",        z + zbar,                    REAL, "real space curve -> mirror (real-trapped)"),
    ("helix_phase_eml0     z/zbar",        z/zbar,                      MOD,  "pure phase (spinning disk) -> module/eml0"),
    ("single_helix_holo    z^2",           z**2,                        HOL,  "one-sided winding -> holomorphic (eml)"),
    ("phi_irrational_spin  z*zbar^phi",    z*zbar**phi,                 MOD,  "irrational spin s=1-phi, NO log -> still module"),
    ("phi_irrational_holo  z^phi",         z**phi,                      HOL,  "one-sided irrational helix -> holomorphic"),
    ("pi_winding_paired    P(1+log|z|^2)", P*(1+sp.log(z*zbar)),        MOD,  "the tour, PAIRED log -> module (removable)"),
    ("pi_winding_unpaired  P(1+log zbar)", P*(1+sp.log(zbar)),          ANTI, "the tour, UNPAIRED log -> genuine ANTI (target)"),
    ("double_helix_real    z*zbar",        z*zbar,                      REAL, "linking number (real, integer) -> mirror"),
    ("double_helix_ampl    z*zbar (prod)", z**2/zbar,                   MOD,  "two-amplitude product (1 field) -> module"),
    ("eml_star_ref         log zbar",      sp.log(zbar),                ANTI, "eml* reference signature"),
]


def main():
    print("=" * 104)
    print("ORTHOGONAL AXIS on EACH possibility (pi / phi / helix) -- spin reading + judge verdict")
    print("=" * 104)
    print(f"{'image':36s} {'spin':10s} {'oracle':14s} {'judge':14s} {'agree':6s} maps to")
    print("-" * 104)
    nok = ntot = 0
    diss = []
    for name, f, exp, note in GRID:
        orc = oracle(f)
        assert orc == exp, f"ORACLE MISMATCH {name}: oracle={orc} expected={exp}"
        sp_val = spin(f)
        if HAVE_JUDGE:
            jv = normalize(certify_1field(f))
            agree = "OK" if jv == orc else "XX"
            ntot += 1
            nok += (jv == orc)
            if jv != orc:
                diss.append((name, orc, jv))
        else:
            jv, agree = "--", "--"
        print(f"{name:36s} {str(sp_val):10s} {orc:14s} {jv:14s} {agree:6s} {note}")
    print("-" * 104)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {nok}/{ntot} agree")
        for name, orc, jv in diss:
            print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("VERDICT [DERIVATION]: under the orthogonal axis, EVERY phi/pi/helix image is a known WALL:")
    print("  real curve -> real-trapped ; phase -> module(eml0) ; one-sided -> holo ; irrational spin")
    print("  (phi) -> STILL module ; linking number -> real ; two-amplitude product -> module.")
    print("  The ONLY escape is the UNPAIRED transcendental log (pi_winding_unpaired -> ANTI), which")
    print("  is the known orthogonal-axis target -- but NO phi/pi/helix object physically forces it.")
    print("  Spin alone (even the golden ratio) never escapes; only an unpaired forced log would.")
    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
