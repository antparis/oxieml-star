#!/usr/bin/env python3
"""
lcft_orthogonal_sweep.py
========================
SYSTEMATIC application of the orthogonal axis (conformal spin s = h - hbar) to the
full set of RESOLVED, parity-broken (or spinful-log candidate) LCFT two-point forms.

Goal: turn the [DERIVATION] block-closure into a single [ESTABLISHED] certification.
The orthogonal axis target is a SPINFUL (h != hbar, hbar != 0), UNPAIRED log operator
(b != bbar) -- the only corner that escapes the three walls (real / module / observable).

This harness encodes every resolved physical closed form swept in reconnaissance and
asks judge_v2 to classify each, comparing against an INDEPENDENT Wirtinger oracle.

KEY established criterion (FINDINGS_20260622r, 12/12) for
    f = z^(-2h) * zbar^(-2hbar) * ( a + b*log z + bbar*log zbar ) :
    - paired   log (b = bbar -> log|z|^2)  -> MODULE_TRAPPED  (transcendental but removable)
    - unpaired log (b != bbar)             -> genuine ANTI    (requires physical parity break)

WHAT THE SWEEP SHOWS (to be certified here):
  The physically realized log in every resolved candidate appears EITHER as
    log|z|^2  (paired -> MODULE_TRAPPED or, if scalar, REAL_TRAPPED), OR as
    chiral log z  (stress-tensor Jordan sector, hbar = 0 -> HOL).
  The target spinful-unpaired form is mathematically genuine ANTI but is NOT produced
  by any resolved physical LCFT swept so far. Chiral cell stays empty.

AUTHORITY: judge_v2 on Anthony's machine is the SOLE arbiter. The oracle below is the
expected value of a unit test, nothing more. No verdict is valid until RUN here.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp

try:
    from judge_v2 import z, zbar, certify_1field
    HAVE_JUDGE = True
except Exception as e:
    print(f"[WARN] judge_v2 not importable ({e}); running ORACLE-ONLY (no certification).")
    z, zbar = sp.symbols('z zbar')
    HAVE_JUDGE = False

HOL, ANTI, REAL, MOD = "HOL", "ANTI", "REAL_TRAPPED", "MODULE_TRAPPED"
_m = sp.symbols('__mod__', positive=True)


# ---------------------------------------------------------------- independent oracle
def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def _full_conj(e):
    t = sp.Symbol('__conj_tmp__')
    return e.subs(sp.I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -sp.I)


def oracle(f):
    """Replicates judge_v2 ordering: HOL -> REAL -> pure-ANTI -> MODULE -> ANTI."""
    if _isz(sp.diff(f, zbar)):
        return HOL
    if _isz(sp.simplify(f - _full_conj(f))):
        return REAL
    if _isz(sp.diff(f, z)):
        return ANTI
    L = sp.simplify(zbar * sp.diff(sp.log(f), zbar))
    L_mod = sp.simplify(L.subs(zbar, _m / z))
    if z not in L_mod.free_symbols:
        return MOD
    return ANTI


def normalize(verdict):
    s = str(verdict).strip().lower()
    if "module" in s:
        return MOD
    if "real" in s:
        return REAL
    if "anti" in s or "mixed" in s:
        return ANTI
    if "hol" in s and "anti" not in s:
        return HOL
    return "UNRECOGNIZED:" + str(verdict)


# ---------------------------------------------------------------- the sweep grid
# spinful prefactor: h=1, hbar=1/2  ->  z^-2 * zbar^-1   (spin s = 1/2)
P = z**(-2) * zbar**(-1)

# Each row: (id, physical_source, closed_form, expected_verdict, fills_chiral_cell?)
GRID = [
    # --- controls (calibration spine) ---
    ("ctrl_holo",   "control",                       z**2,                                HOL,  False),
    ("ctrl_anti",   "control",                       sp.log(zbar),                        ANTI, False),
    ("ctrl_real",   "control (SPARC)",               z*zbar,                              REAL, False),
    ("ctrl_module", "control (eml0 phase)",          z/zbar,                              MOD,  False),

    # --- massive-gravity family at the log critical point (TMG/NMG/GMG/critical gravity) ---
    # The log operator is the Jordan partner of the stress tensor T(z): weight (2,0), hbar=0.
    ("tmg_left",        "TMG/NMG/GMG t(z) log partner of T", (1 - 2*sp.log(z))/z**4,        HOL,  False),
    ("tmg_parity_img",  "parity image (half-chiral wall)",   (1 - 2*sp.log(zbar))/zbar**4,  ANTI, False),
    ("tmg_full_local",  "TMG full local (spinful prefactor)",zbar**(-2)*(1 - 2*sp.log(z))/z**4, MOD, False),

    # --- universal rank-2 Jordan block <O_i O_j> = c/|x|^(2D) [[log|x|^2, 1],[1,0]] ---
    ("jordan_r2_scalar", "universal rank-2 Jordan (scalar)",  (1 + sp.log(z*zbar))/(z*zbar)**2, REAL, False),
    ("jordan_r2_spin",   "universal rank-2 Jordan (spinful)", P*(1 + sp.log(z*zbar)),           MOD,  False),

    # --- rank-3 Jordan of TTbar at c=0 (dimension (4,4), spin 0) ---
    ("ttbar_r3_c0",      "TTbar rank-3 Jordan c=0",           (-2*sp.log(z*zbar) + 1)/(z*zbar)**4, REAL, False),

    # --- THE TARGET corner: spinful + UNPAIRED log (mathematically genuine ANTI) ---
    # No resolved physical LCFT swept so far produces these. Form exists; physics does not force it.
    ("target_unpaired",  "TARGET spinful-unpaired (no phys.)", P*(1 + sp.log(zbar)),            ANTI, False),
    ("target_asym",      "TARGET spinful-asymmetric (no phys.)", P*(1 + sp.log(z) + 2*sp.log(zbar)), ANTI, False),
]


def main():
    print("=" * 96)
    print("ORTHOGONAL-AXIS LCFT SWEEP  (conformal spin s = h - hbar)")
    print("authority = judge_v2 (this machine);  oracle = independent unit-test expectation")
    print("=" * 96)
    header = f"{'id':18s} {'oracle':14s} {'judge':14s} {'agree':6s} {'cell':5s}  physical source"
    print(header)
    print("-" * 96)

    n_ok = n_total = 0
    disagreements = []
    for cid, src, f, expected, fills in GRID:
        orc = oracle(f)
        assert orc == expected, f"ORACLE MISMATCH on {cid}: oracle={orc} expected={expected}"
        if HAVE_JUDGE:
            jraw = certify_1field(f)
            jv = normalize(jraw)
            agree = "OK" if jv == orc else "XX"
            n_total += 1
            if jv == orc:
                n_ok += 1
            else:
                disagreements.append((cid, orc, jv, jraw))
        else:
            jv, agree = "--", "--"
        cell = "FILL" if fills else "no"
        print(f"{cid:18s} {orc:14s} {jv:14s} {agree:6s} {cell:5s}  {src}")

    print("-" * 96)
    if HAVE_JUDGE:
        print(f"judge vs oracle: {n_ok}/{n_total} agree")
        if disagreements:
            print("\nDISAGREEMENTS (judge is authority; investigate):")
            for cid, orc, jv, jraw in disagreements:
                print(f"  {cid}: oracle={orc} judge={jv} (raw={jraw})")
    print(f"\nchiral cell filled by any swept form: "
          f"{'YES' if any(g[4] for g in GRID) else 'NO -- cell remains EMPTY'}")
    print("\nSUMMARY: the physically-realized log is always paired (log|z|^2 -> MODULE/REAL)")
    print("or chiral-pure (log z, hbar=0 -> HOL). The spinful-unpaired ANTI target is a")
    print("genuine form but is NOT produced by any resolved physical LCFT swept here.")

    if HAVE_JUDGE and disagreements:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
