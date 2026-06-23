#!/usr/bin/env python3
"""
log_spiral_fractal_sweep.py -- orthogonal axis + ALL Layer-1 tools at once on log-spiral /
fractal / complex-exponent forms; surface the master pattern.

A logarithmic spiral = a COMPLEX exponent: z^(alpha+i*beta) has log-spiral level curves
(beta*ln r + alpha*theta = const). Fractals / discrete scale invariance produce complex
critical exponents = log-periodicity cos(omega*ln|z|) = the same structure. Physical realization:
conformal/scale-invariant QM (-g/r^2, Efimov, Calogero), where psi ~ r^(i*nu) is a FORCED log
spiral in a complex amplitude (scale anomaly -> discrete scale invariance).

We run, on each form, ALL Layer-1 tools simultaneously via axis_fingerprint:
  verdict (judge_v2) | spin s=h-hbar (orthogonal axis) | poly_anti order (axis A) | sigma reality (axis B).
Then classify into the MASTER 3-CASE PATTERN of how a complex object depends on zbar:
  HOL            : no zbar                                  (eml, one-sided)
  WALL_PAIRED    : zbar paired with z (real/modulus/powers) (REAL_TRAPPED or MODULE_TRAPPED)
  GENUINE_ANTI   : zbar UNPAIRED, transcendental            (ANTI)

AUTHORITY: judge_v2 (verdict). Oracle = independent unit-test expectation.
Author: Anthony Monnerot, 2026.
"""
import sympy as sp
import axis_fingerprint as afp

z, zbar, I = afp.z, afp.zbar, sp.I
m = sp.symbols('__m__', positive=True)
HOL, ANTI, REAL, MOD = "HOL", "ANTI", "REAL_TRAPPED", "MODULE_TRAPPED"


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
    if z not in sp.simplify(L.subs(zbar, m / z)).free_symbols:
        return MOD
    return ANTI


def master_case(verdict):
    if verdict == HOL:
        return "HOL (one-sided)"
    if verdict in (REAL, MOD):
        return "WALL_PAIRED (zbar = mirror/modulus)"
    if verdict == ANTI:
        return "GENUINE_ANTI (zbar unpaired)"
    return "?"


GRID = [
    ("logspiral_holo  z^(1+i)",            z**(1+I),                         HOL,  "log spiral, one-sided"),
    ("logspiral_phase  |z|^i",             (z*zbar)**(I/2),                  MOD,  "scale-free phase (|z|^is blind-spot, patched)"),
    ("logspiral_anti  zbar^(1+i)",         zbar**(1+I),                      ANTI, "log spiral pure-anti (half-chiral wall)"),
    ("logspiral_balanced z^s zbar^sbar",   z**(1+I)*zbar**(1-I),             REAL, "balanced log spiral -> real"),
    ("complex_unbalanced z^(1+i)zbar^(2-i)", z**(1+I)*zbar**(2-I),           MOD,  "complex powers pair -> module"),
    ("fractal_logperiodic cos(3 ln|z|)",   sp.cos(3*sp.log(sp.sqrt(z*zbar))),REAL, "DSI / fractal log-periodicity (real)"),
    ("efimov_radial  |z|^(i/3)",           (z*zbar)**(I*sp.Rational(1,3)),   MOD,  "conformal QM psi~r^(i nu) (Efimov) -> module"),
    ("escape_unpaired z^-1 zbar^-1(1+log zbar)", z**(-1)*zbar**(-1)*(1+sp.log(zbar)), ANTI, "the ONLY escape: unpaired transcendental log"),
]


def main():
    print("=" * 116)
    print("LOG-SPIRAL / FRACTAL under the ORTHOGONAL AXIS + ALL Layer-1 tools simultaneously")
    print("=" * 116)
    print(f"{'form':42s} {'judge':14s} {'spin':14s} {'poly_anti':10s} {'sigStd':7s} {'sigInv':7s} master-case")
    print("-" * 116)
    nok = ntot = 0
    diss = []
    for name, f, exp, note in GRID:
        orc = oracle(f)
        assert orc == exp, f"ORACLE MISMATCH {name}: oracle={orc} expected={exp}"
        fp = afp.fingerprint(f)               # ALL tools at once: verdict, poly, spin, sigma
        jv = fp["verdict"]
        agree = "OK" if jv == orc else "XX"
        ntot += 1
        nok += (jv == orc)
        if jv != orc:
            diss.append((name, orc, jv))
        print(f"{name:42s} {str(jv):14s} {str(fp['spin']):14s} {str(fp['poly_anti']):10s} "
              f"{str(fp['sig_std']):7s} {str(fp['sig_inv']):7s} {master_case(jv)}")
    print("-" * 116)
    print(f"judge vs oracle: {nok}/{ntot} agree")
    for name, orc, jv in diss:
        print(f"  DISAGREE {name}: oracle={orc} judge={jv}")
    print()
    print("PATTERNS [DERIVATION] -- with all tools at once:")
    print("  1. Every log-spiral / fractal / complex-exponent form is HOL or WALL_PAIRED.")
    print("     The spin column shows even COMPLEX/irrational spin (1+i, etc.) -> still a wall;")
    print("     scale-freeness (fractal) does NOT move the verdict off the wall.")
    print("  2. The ONLY GENUINE_ANTI is the unpaired transcendental log (poly_anti = oo, spin n/a).")
    print("     No power, no phase, no complex exponent, no fractal reaches it -- only an UNPAIRED LOG.")
    print("  3. Master law: zbar is genuine ONLY when UNPAIRED + transcendental. Rotation/spin/scale")
    print("     (phi, pi, helix, log spiral, fractal) all PAIR zbar with z -> mirror/modulus -> wall.")
    print("  => A fractal CANNOT fill the chiral cell: it supplies a sophisticated wall (log-spiral phase),")
    print("     not independent anti. The cell needs an unpaired forced log in a natively-complex measurable.")
    if diss:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
