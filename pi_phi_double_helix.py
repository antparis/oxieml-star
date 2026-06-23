#!/usr/bin/env python3
"""
pi_phi_double_helix.py -- pi and phi as a DOUBLE HELIX under the orthogonal axis.

A double helix = two strands with two pitches: pi on one, phi on the other. The decisive question
under the orthogonal axis is NOT pi/phi themselves but PAIRING: are the holo and anti strands
paired (anti coeff = conj of holo coeff -> mirror/modulus -> wall) or unpaired (different coeffs)?
Since pi != phi (both irrational, incommensurate), unequal strand coefficients are UNPAIRED.

But "ANTI in the judge" splits further. A finer diagnostic separates two regimes:
  FACTORIZES (d_z d_zbar log f = 0)  =>  f = holo(z) * anti(zbar) = SEPARABLE
        => the anti is a dressed PURE-ANTI factor = HALF-CHIRAL WALL (mirror), not the cell.
  DOES NOT FACTORIZE                 =>  genuinely ENTANGLED unpaired anti = the orthogonal-axis
        target type (like the spinful unpaired log).

Verdict columns: judge_v2 verdict | spin | factorizes? | refined class.
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
I, pi, phi = sp.I, sp.pi, sp.GoldenRatio


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
    return e.subs(I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -I)


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


def factorizes(f):
    """f = holo(z)*anti(zbar)  <=>  d_z d_zbar (log f) = 0."""
    try:
        return _isz(sp.diff(sp.diff(sp.log(f), z), zbar))
    except Exception:
        return False


def spin(f):
    if _isz(f):
        return None
    R = sp.simplify(z*sp.diff(f, z) - zbar*sp.diff(f, zbar))
    s = sp.simplify(R/f)
    return s if not s.free_symbols else "n/a"


def refined_class(verdict, fact):
    if verdict == HOL:
        return "HOL (one-sided)"
    if verdict in (REAL, MOD):
        return "WALL_PAIRED (mirror/modulus)"
    # verdict == ANTI
    return "SEPARABLE half-chiral WALL" if fact else "ENTANGLED unpaired ANTI (target type)"


P = z**(-1)*zbar**(-1)

GRID = [
    ("dh_powers_pitch  z^(i pi) zbar^(i phi)",   z**(I*pi)*zbar**(I*phi),                          MOD),
    ("dh_plane_mult    exp(i pi z + i phi zbar)", sp.exp(I*pi*z + I*phi*zbar),                      ANTI),
    ("dh_plane_paired  exp(i pi z - i pi zbar)",  sp.exp(I*pi*z - I*pi*zbar),                       REAL),
    ("dh_plane_neqpair exp(i pi z - i phi zbar)", sp.exp(I*pi*z - I*phi*zbar),                      ANTI),
    ("dh_log_unpaired  P(1+pi log z+phi log zbar)", P*(1 + pi*sp.log(z) + phi*sp.log(zbar)),        ANTI),
    ("dh_log_paired    P(1+pi log z+pi log zbar)",  P*(1 + pi*sp.log(z) + pi*sp.log(zbar)),         REAL),
    ("dh_ratio_holo    z^(i phi/pi)",            z**(I*phi/pi),                                     HOL),
    ("ctrl_real  z+zbar",                        z + zbar,                                          REAL),
    ("ctrl_anti  log zbar (pure)",               sp.log(zbar),                                      ANTI),
]


def main():
    print("=" * 116)
    print("PI and PHI as a DOUBLE HELIX under the orthogonal axis (+ factorization diagnostic)")
    print("=" * 116)
    print(f"{'form':44s} {'judge':14s} {'spin':10s} {'fact?':6s} {'agree':6s} refined class")
    print("-" * 116)
    nok = ntot = 0
    diss = []
    for name, f, exp in GRID:
        orc = oracle(f)
        assert orc == exp, f"ORACLE MISMATCH {name}: oracle={orc} expected={exp}"
        fact = factorizes(f)
        sp_val = spin(f)
        if HAVE_JUDGE:
            jv = normalize(certify_1field(f))
            agree = "OK" if jv == orc else "XX"
            ntot += 1
            nok += (jv == orc)
            if jv != orc:
                diss.append((name, orc, jv))
        else:
            jv, agree = orc, "--"
        print(f"{name:44s} {str(jv):14s} {str(sp_val):10s} {str(fact):6s} {agree:6s} {refined_class(jv, fact)}")
    print("-" * 116)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {nok}/{ntot} agree")
        for name, orc, jv in diss:
            print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("VERDICT [DERIVATION]: the double-helix verdict is governed by PAIRING; pi != phi breaks it.")
    print("  - As EXPONENTS (spiral pitches): always module -> wall (powers pair regardless of pitch).")
    print("  - As MULTIPLICATIVE strands exp(i pi z)*exp(i phi zbar): FACTORIZES -> separable half-chiral")
    print("    WALL (a pure-anti factor dressed by a holo factor; not entangled).")
    print("  - As ADDITIVE unequal log coefficients (pi != phi): does NOT factorize -> ENTANGLED unpaired")
    print("    ANTI = the orthogonal-axis target type. Incommensurability pi != phi forces the unpairing.")
    print("  => FIRST intuition of the session to reach the genuine-target side -- but only as a FORM.")
    print("     OPEN: is the unequal-coefficient unpairing FORCED by a physical system (SPARC) and carried")
    print("     by a MEASURABLE natively-complex observable (interference)? [CONJECTURE] -- the verrou.")
    if HAVE_JUDGE and diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
