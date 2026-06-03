#!/usr/bin/env python3
"""
beltrami_check.py  --  Beltrami dilatation add-on for the eml* detector.

Standalone, does NOT modify verify_exact.py or reality_check.py.
Reports the Beltrami coefficient  mu_f = (df/dzbar)/(df/dz).

Usage:
  python3 beltrami_check.py "z + zbar/2"           # direct sympy expr
  python3 beltrami_check.py hm_vortex_result.json  # PySR best_equation

JSON path reuses verify_exact.parse_formula (same operator dictionary as the
judge), so emlstar / inv_bar / my_conj / my_abs2 / eml are parsed identically.

Classification by the VALUE of |mu| (sampled), with the structure of mu used
only as a secondary note (v2 refinement, 2026-06-03: value-based, not
complexity-based, so a negligible-anti residue is no longer mislabeled):
   |mu| = 0                 -> HOLOMORPHIC
   0 < median|mu| < 0.05    -> HOLO-DOMINANT (negligible anti residue)
   0.05 <= |mu| < 1         -> MIXED / ANTI-MINOR (real independent anti)
   |mu| ~ 1 (all samples)   -> REAL-TRAPPED (mirror-locked, SPARC-type)
   |mu| > 1 (all samples)   -> ANTI-DOMINANT
   |mu| crosses 1           -> MIXED (spatially varying anti weight)
   df/dz = 0                -> PURE ANTI-HOLOMORPHIC

REDUCIBILITY NOTE (secondary): a twist is a mere frame change only if
count_ops(mu) < count_ops(f) AND |mu|<1 everywhere. Reported as a note, no
longer the primary label (it was too coarse: flagged |mu|~0.7 and |mu|~0.002
alike). The VALUE of |mu| is now the primary discriminant.

CAVEAT: exact only on symbolic closed-form f. On noisy real data the arbiter
stays the negative control + exploitable MSE, never this coefficient alone.

Author: Anthony Monnerot, 2026.
"""
import sys, json
import sympy as sp

z, zbar = sp.symbols('z zbar')

SAMPLE_PTS = [1+0.5j, 0.7-0.3j, -0.4+0.9j, 1.3+0.2j, -0.6-0.6j]
HOLO_DOM_THR = 0.05   # median |mu| below this = holo-dominant negligible anti

def beltrami_report(f, n_samples=5):
    f = sp.sympify(f)
    fz   = sp.diff(f, z)
    fzbar = sp.diff(f, zbar)
    print(f"f         = {f}")
    print(f"df/dz     = {sp.simplify(fz)}")
    print(f"df/dzbar  = {sp.simplify(fzbar)}")

    if fzbar == 0:
        print("|mu|      = 0")
        print("CLASS     : HOLOMORPHIC")
        return "HOLOMORPHIC"
    if fz == 0:
        print("|mu|      = infinite (df/dz = 0)")
        print("CLASS     : PURE ANTI-HOLOMORPHIC")
        return "PURE_ANTI"

    mu = sp.simplify(fzbar / fz)
    is_const = (sp.diff(mu, z) == 0 and sp.diff(mu, zbar) == 0)
    cf, cmu = sp.count_ops(f), sp.count_ops(mu)

    mods = []
    for p in SAMPLE_PTS[:n_samples]:
        try:
            val = complex(mu.subs({z: p, zbar: complex(p).conjugate()}))
            mods.append(abs(val))
        except Exception:
            pass
    if not mods:
        print(f"mu_f      = {mu}")
        print("CLASS     : UNDETERMINED (could not sample mu)")
        return "UNDETERMINED"

    mods.sort()
    mmin, mmax = mods[0], mods[-1]
    mmed = mods[len(mods)//2]
    print(f"mu_f      = {mu}")
    print(f"mu const? = {is_const}   complexity f={cf}, mu={cmu}")
    print(f"|mu|      = median {mmed:.4f}, range [{mmin:.4f}, {mmax:.4f}] over {len(mods)} samples")

    near1 = all(abs(m-1) < 1e-6 for m in mods)
    alllt1 = all(m < 1-1e-9 for m in mods)
    allgt1 = all(m > 1+1e-9 for m in mods)

    reducible = (is_const or cmu < cf)
    note = ""
    if alllt1:
        note = ("  [note: mu simpler than f -> reducible twist (frame change)]"
                if reducible else
                "  [note: mu not simpler than f -> non-reducible (genuine structure)]")

    if near1:
        cls = "REAL-TRAPPED (|mu|=1, mirror-locked, SPARC-type)"
    elif allgt1:
        cls = "ANTI-DOMINANT (|mu|>1)"
    elif alllt1:
        if mmed < HOLO_DOM_THR:
            cls = f"HOLO-DOMINANT (median|mu|<{HOLO_DOM_THR}, negligible anti residue)"
        else:
            cls = "MIXED / ANTI-MINOR (|mu|<1, real independent anti)"
        cls += note
    else:
        cls = "MIXED (|mu| crosses 1 across domain => spatially varying anti weight)"
    print(f"CLASS     : {cls}")
    return cls

def report_json(path):
    from verify_exact import parse_formula
    with open(path) as fh:
        d = json.load(fh)
    eq = d.get("best_equation")
    if eq is None:
        raise SystemExit(f"No 'best_equation' field in {path}")
    print(f"[{d.get('label','?')}]  MSE={d.get('best_mse','?')}")
    f = parse_formula(eq)
    beltrami_report(f)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        report_json(sys.argv[1])
    elif len(sys.argv) == 2:
        beltrami_report(sys.argv[1])
    else:
        print("Usage: python3 beltrami_check.py '<sympy expr in z, zbar>'")
        print("   or: python3 beltrami_check.py <result.json>")
