#!/usr/bin/env python3
"""
axis_fingerprint.py
===================
META-TOOL for the eml / eml* hunt.

The "orthogonal axis" was ONE instance of a general method: take the invariant that
every past attempt silently held FIXED, and vary it. The spin s = h - hbar was that
invariant. This tool makes the whole stack of silently-fixed invariants EXPLICIT and
MEASURABLE, so that new "orthogonal-axis-like" techniques can be found by reading off
which cells of the multi-axis grid are still EMPTY.

Each closed form f(z, zbar) gets a fingerprint VECTOR over several axes:

  axis 0  verdict        : judge_v2 classification        (HOL / ANTI / REAL_TRAPPED / MODULE_TRAPPED)
  axis 1  poly_anti      : smallest q with (d/dzbar)^q f = 0, else oo   [poly-analytic / "branch" axis]
  axis 2  poly_holo      : smallest p with (d/dz)^p f = 0, else oo      [mirror of axis 1]
  axis 3  spin           : eigenvalue of R = z d/dz - zbar d/dzbar, if eigenstate, else n/a  [orthogonal axis]
  axis 4  sigma_std_real : is f real under standard conjugation z<->zbar           [reality axis, lambda=std]
  axis 5  sigma_inv_real : is f real under inversion-conjugation z->1/zbar         [reality axis, lambda=inv]

Adding a NEW technique = adding one function to AXES below (e.g. a different involution,
an integrability test once J-input is supported, a multi-variable Dolbeault test).

The occupancy report flags TARGET cells that are mathematically possible but never yet
observed in a physically-realized form -- those empty cells are the next hunting grounds.

NOTE on weighted states: for Gaussian-weighted Fock states (Landau levels), the raw
poly_anti order reads oo because of exp(-|z|^2/4); the judge's MODULE_TRAPPED verdict is
the correct reading there. A weight-stripped poly order is a planned refinement.

AUTHORITY: judge_v2 on Anthony's machine is the sole arbiter for axis 0. Axes 1-5 are
exact SymPy structural diagnostics (no fitting), but remain INDICATIVE until run here.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp

try:
    from judge_v2 import z, zbar, certify_1field
    HAVE_JUDGE = True
except Exception as e:
    print(f"[WARN] judge_v2 not importable ({e}); axis 0 uses the internal oracle (INDICATIVE).")
    z, zbar = sp.symbols('z zbar')
    HAVE_JUDGE = False

HOL, ANTI, REAL, MOD = "HOL", "ANTI", "REAL_TRAPPED", "MODULE_TRAPPED"
MAXP = 8
_m = sp.symbols('__mod__', positive=True)


# ----------------------------------------------------------------- helpers
def _isz(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def _full_conj(e):
    t = sp.Symbol('__t__')
    return e.subs(sp.I, t).subs({z: zbar, zbar: z}, simultaneous=True).subs(t, -sp.I)


def _sigma_inv(e):
    t = sp.Symbol('__t__')
    a, b = sp.Symbol('__a__'), sp.Symbol('__b__')
    e2 = e.subs(sp.I, t).subs({z: a, zbar: b}, simultaneous=True)
    e2 = e2.subs({a: 1/zbar, b: 1/z}, simultaneous=True).subs(t, -sp.I)
    return e2


def _oracle(f):
    """Internal fallback for axis 0 (replicates judge_v2 ordering)."""
    if _isz(sp.diff(f, zbar)):
        return HOL
    if _isz(sp.simplify(f - _full_conj(f))):
        return REAL
    if _isz(sp.diff(f, z)):
        return ANTI
    L = sp.simplify(zbar * sp.diff(sp.log(f), zbar))
    if z not in sp.simplify(L.subs(zbar, _m / z)).free_symbols:
        return MOD
    return ANTI


def _normalize(v):
    s = str(v).strip().lower()
    if "module" in s:                    return MOD
    if "real" in s:                      return REAL
    if "anti" in s or "mixed" in s:      return ANTI
    if "hol" in s and "anti" not in s:   return HOL
    return "?:" + str(v)


# ----------------------------------------------------------------- axes
def axis_verdict(f):
    return _normalize(certify_1field(f)) if HAVE_JUDGE else _oracle(f)


def _poly_order(f, wrt):
    g = f
    for k in range(1, MAXP + 1):
        g = sp.diff(g, wrt)
        if _isz(g):
            return k
    return sp.oo


def axis_poly_anti(f): return _poly_order(f, zbar)
def axis_poly_holo(f): return _poly_order(f, z)


def axis_spin(f):
    if _isz(f):
        return None
    R = sp.simplify(z * sp.diff(f, z) - zbar * sp.diff(f, zbar))
    s = sp.simplify(R / f)
    return s if not s.free_symbols else "n/a"


def axis_sigma_std(f):
    return _isz(sp.simplify(f - _full_conj(f)))


def axis_sigma_inv(f):
    try:
        return _isz(sp.simplify(sp.together(f - _sigma_inv(f))))
    except Exception:
        return False


AXES = [
    ("verdict",  axis_verdict),
    ("poly_anti", axis_poly_anti),
    ("poly_holo", axis_poly_holo),
    ("spin",     axis_spin),
    ("sig_std",  axis_sigma_std),
    ("sig_inv",  axis_sigma_inv),
]


def fingerprint(f):
    return {name: fn(f) for name, fn in AXES}


# ----------------------------------------------------------------- corpus
def _poly_class(n):
    if n == 1:        return "N1(holo)"
    if n == sp.oo:    return "Ntransc"
    return f"N{n}fin"


P = z**(-2) * zbar**(-1)  # spinful prefactor h=1, hbar=1/2
# (name, form, physical?)  physical=True only for physically-realized closed forms;
# controls, bare monomials and hypothetical targets are physical=False.
CORPUS = [
    ("ctrl_holo",        z**2,                            False),
    ("ctrl_anti",        sp.log(zbar),                    False),
    ("ctrl_real",        z*zbar,                          False),
    ("ctrl_module",      z/zbar,                          False),
    ("zbar_affine",      zbar,                            False),
    ("zbar_quad",        zbar**2,                         False),
    ("landau_n1",        zbar*sp.exp(-z*zbar/4),          True),
    ("tmg_left",         (1 - 2*sp.log(z))/z**4,          True),
    ("jordan_r2_spin",   P*(1 + sp.log(z*zbar)),          True),
    ("target_unpaired",  P*(1 + sp.log(zbar)),            False),
    ("inv_real_probe",   1/(z*zbar),                      False),
]


def main():
    print("=" * 104)
    print("AXIS FINGERPRINT  -- multi-axis structural map of the eml/eml* hunt")
    print("authority: judge_v2 (axis 0, this machine);  axes 1-5: exact SymPy structural diagnostics")
    print("=" * 104)
    hdr = f"{'form':18s} {'verdict':14s} {'poly_anti':10s} {'poly_holo':10s} {'spin':8s} {'sig_std':8s} {'sig_inv':8s}"
    print(hdr)
    print("-" * 104)

    rows = []
    for name, f, phys in CORPUS:
        fp = fingerprint(f)
        rows.append((name, fp, phys))
        tag = "phys" if phys else "----"
        print(f"{name:18s} {str(fp['verdict']):14s} {str(fp['poly_anti']):10s} "
              f"{str(fp['poly_holo']):10s} {str(fp['spin']):8s} "
              f"{str(fp['sig_std']):8s} {str(fp['sig_inv']):8s} {tag}")

    print("-" * 104)
    print("OCCUPANCY  (verdict x poly_anti_class x spin_class) -- [P]=physically-realized occupant")
    occ = {}
    for name, fp, phys in rows:
        sp_cls = "s=0" if fp["spin"] == 0 else ("s!=0" if fp["spin"] not in ("n/a", None) else "s=n/a")
        key = (fp["verdict"], _poly_class(fp["poly_anti"]), sp_cls)
        occ.setdefault(key, []).append(name + ("[P]" if phys else ""))
    for key in sorted(occ, key=lambda k: (str(k[0]), str(k[1]), str(k[2]))):
        print(f"  {str(key):46s} : {', '.join(occ[key])}")

    # physically-occupied cells only
    phys_occ = set()
    for name, fp, phys in rows:
        if not phys:
            continue
        sp_cls = "s=0" if fp["spin"] == 0 else ("s!=0" if fp["spin"] not in ("n/a", None) else "s=n/a")
        phys_occ.add((fp["verdict"], _poly_class(fp["poly_anti"]), sp_cls))

    print("-" * 104)
    print("EMPTY TARGET CELLS  (mathematically possible; EMPTY = no PHYSICALLY-realized form there):")
    target_cells = [
        (ANTI, "N2fin",   "s!=0", "finite-order (poly-analytic N=2) GENUINE anti, nonzero spin -> Ginibre/Bergman kernel?"),
        (ANTI, "N3fin",   "s!=0", "finite-order (N=3) genuine anti, nonzero spin"),
        (ANTI, "Ntransc", "s!=0", "transcendental genuine anti, nonzero spin (the spinful-unpaired log target)"),
        (ANTI, "Ntransc", "s=0",  "transcendental genuine anti, spin 0"),
    ]
    for v, pc, sc, desc in target_cells:
        flag = "FILLED-P" if (v, pc, sc) in phys_occ else "EMPTY"
        print(f"  [{flag:8s}] verdict={v}, poly={pc}, spin={sc}")
        print(f"             {desc}")

    print("-" * 104)
    print("REALITY-AXIS FLIPS  (chiral under sigma_std but REAL under sigma_inv = new reality structure):")
    flips = [name for name, fp, phys in rows
             if fp["sig_std"] is False and fp["sig_inv"] is True and fp["verdict"] in (MOD, ANTI)]
    print("  " + (", ".join(flips) if flips else "(none in corpus)"))
    print("  -> these forms are mirror w.r.t. an alternative real structure; 'chirality' is")
    print("     sigma-relative. A physical system that FORCES sigma_inv as its reality condition")
    print("     would turn an apparent module/anti object into a wall, or vice-versa.")


if __name__ == "__main__":
    main()
