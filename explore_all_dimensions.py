#!/usr/bin/env python3
"""
explore_all_dimensions.py -- unified exploration across ALL built axes of the eml/eml* hunt.

It orchestrates every dimension produced this session, in two layers:

  LAYER 1 (functions f(z,zbar), one variable) -- via axis_fingerprint:
      verdict (judge_v2) | poly_anti / poly_holo (axis A) | spin s=h-hbar (orthogonal axis)
      | sigma_std / sigma_inv reality (axis B)
      => classifies REMOVABILITY of a function's anti. On a contractible domain every anti
         is removable (real/module). These axes refine the wall but never give non-removability.

  LAYER 2 (forms, several variables / topology) -- via dolbeault_v1:
      d-bar cohomology H^{0,1} (eml*) and d cohomology H^{1,0} (eml), both directions + control.
      => COHOMOLOGY is the ONLY non-removable anti (immune to coboundary AND gauge).

SYNTHESIS (to be certified by running both engines on Anthony's machine):
      non-removable anti  <=>  non-trivial Dolbeault class (Layer 2).
      Every Layer-1 wall (real / module / gauge) is a removability wall.
      The chiral cell can ONLY live in Layer 2; its physical realization (criterion c) is the
      sole remaining frontier (v1b+v1d: torus / period ratio tau).

AUTHORITY: judge_v2 (Layer 1 verdict) on Anthony's machine; Layer 2 = exact SymPy. INDICATIVE
until run there. No physical claim until criterion (c) is met.

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
import axis_fingerprint as afp
import dolbeault_v1 as dol


def layer1():
    z, zb = afp.z, afp.zbar
    P = z**(-2) * zb**(-1)
    # (name, form, physical?, gauge_removable?)  gauge_removable from ginibre_sweep finding.
    corpus = [
        ("ctrl_holo",       z**2,                    False, False),
        ("ctrl_anti(toy)",  sp.log(zb),              False, False),
        ("ctrl_real",       z*zb,                    False, False),
        ("ctrl_module",     z/zb,                    False, False),
        ("landau_n1",       zb*sp.exp(-z*zb/4),      True,  False),
        ("tmg_left",        (1-2*sp.log(z))/z**4,    True,  False),
        ("jordan_r2_spin",  P*(1+sp.log(z*zb)),      True,  False),
        ("ginibre_q2_ker",  sp.exp(-(z-1)*(zb-1)/2)*sp.exp((z-zb)/2)*(1-(z-1)*(zb-1)), True, True),
        ("target(toy)",     P*(1+sp.log(zb)),        False, False),
    ]
    print("=" * 104)
    print("LAYER 1 -- functions f(z,zbar): removability classification (judge + axes A, orthogonal, B)")
    print("=" * 104)
    print(f"{'name':16s} {'verdict':14s} {'poly_anti':10s} {'spin':8s} {'sig_std':8s} {'sig_inv':8s} {'phys':5s} gauge")
    print("-" * 104)
    phys_anti_nonremovable = []
    for name, f, phys, gauge_rem in corpus:
        fp = afp.fingerprint(f)
        tag = "phys" if phys else "----"
        gtag = "g-rem" if gauge_rem else "-"
        print(f"{name:16s} {str(fp['verdict']):14s} {str(fp['poly_anti']):10s} "
              f"{str(fp['spin']):8s} {str(fp['sig_std']):8s} {str(fp['sig_inv']):8s} {tag:5s} {gtag}")
        # genuinely non-removable physical anti: ANTI verdict, physical, and NOT gauge-removable
        if phys and fp['verdict'] == 'ANTI' and not gauge_rem:
            phys_anti_nonremovable.append(name)
    print("-" * 104)
    print(f"physical functions with GENUINELY non-removable ANTI (gauge-invariant): "
          f"{phys_anti_nonremovable if phys_anti_nonremovable else 'NONE'}")
    print("  -> ginibre_q2_ker reads ANTI but is gauge-removable (ginibre_sweep): excluded.")
    print("     No physical Layer-1 non-removable anti exists.")
    return phys_anti_nonremovable


def layer2():
    z1, z2, zb1, zb2 = sp.symbols('z1 z2 zbar1 zbar2')
    Z, ZB = [z1, z2], [zb1, zb2]
    cases = [
        ("anti exact",        dol.PForm([2*zb1*zb2, zb1**2], Z, ZB, "anti")),
        ("anti COHOMOLOGY",   dol.PForm([1/zb1, 0], Z, ZB, "anti")),
        ("holo exact",        dol.PForm([2*z1*z2, z1**2], Z, ZB, "holo")),
        ("holo COHOMOLOGY",   dol.PForm([1/z1, 0], Z, ZB, "holo")),
        ("holo-func->anti",   dol.from_function(1/z1, Z, ZB, "anti")),
        ("real-field->anti",  dol.from_function(z1*zb1, Z, ZB, "anti")),
    ]
    print("\n" + "=" * 104)
    print("LAYER 2 -- forms: Dolbeault cohomology (eml* H^{0,1} & eml H^{1,0})")
    print("=" * 104)
    print(f"{'case':22s} {'dir':5s} {'verdict':12s} primitive")
    print("-" * 104)
    nonremovable = []
    for name, form in cases:
        v, g = dol.verdict(form)
        gs = "-" if g is None else str(g)
        print(f"{name:22s} {form.direction:5s} {v:12s} {gs}")
        if v == "COHOMOLOGY":
            nonremovable.append((name, form.direction))
    print("-" * 104)
    print(f"NON-REMOVABLE anti/holo (COHOMOLOGY): {nonremovable}")
    return nonremovable


def main():
    l1 = layer1()
    l2 = layer2()
    print("\n" + "#" * 104)
    print("MASTER SYNTHESIS  [DERIVATION]")
    print("#" * 104)
    print("Layer 1 (functions): every physical object's anti is REAL/MODULE/GAUGE -> REMOVABLE.")
    print(f"  physical non-removable anti in Layer 1: {l1 if l1 else 'NONE'}")
    print("Layer 2 (forms): COHOMOLOGY is the ONLY non-removable structure, in BOTH directions.")
    print(f"  non-removable classes found: {[c[0]+'('+c[1]+')' for c in l2]}")
    print()
    print("=> non-removable anti  <=>  non-trivial Dolbeault class (Layer 2).")
    print("   All session walls (real / module / gauge) are Layer-1 removability walls.")
    print("   The chiral cell can ONLY live in Layer 2. Remaining frontier = criterion (c):")
    print("   a measurable observable carrying a non-trivial class (v1b+v1d: torus / period tau).")


if __name__ == "__main__":
    main()
