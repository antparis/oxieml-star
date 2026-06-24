#!/usr/bin/env python3
"""
symmetry_harness.py  --  eml / eml(star) project, oxieml-star

A holo/anti SYMMETRY layer ON TOP of judge_v2 (NOT a new judge).
judge_v2.certify_1field / certify_2field remain the sole authority.

WHY
---
Campaign-level fix: the hunt had become anti-only. The detector must read BOTH
sides (holomorphic AND anti-holomorphic) in parallel, plus the negative control,
and be irreproachable on the holomorphic side (never flag anti on a holomorphic
field) BEFORE any claim on the anti side.

WHAT IT ADDS (without touching the authority)
---------------------------------------------
 1. symmetric_reading(f): the judge label (authority) PLUS a 5-way symmetric
    reading -- holo-pure / anti-pure / mixed / real-trapped / module-trapped --
    and both Wirtinger derivatives d/dz, d/dzbar.
 2. mirror_symmetry: judge(f) vs judge(full_conj(f)) must be MIRROR labels.
    This exposes the asymmetry of the bare judge: 'holomorphic' is pure
    (d/dzbar=0) but 'anti-holomorphic' is a CATCH-ALL (pure anti d/dz=0 AND
    mixed). The harness reports it explicitly.
 3. never_false_anti_on_holo: every holomorphic calibration form must judge
    'holomorphic' -- the irreproachable-on-holo condition.
 4. ledger(): two living columns (holo confirmed / anti confirmed) + rejects.

STATUS: [DERIVATION] until run on the M920q. Wirtinger exact. Marker != verdict.
"""
import sympy as sp
from judge_v2 import z, zbar, w, wbar, certify_1field, certify_2field, full_conj

MIRROR_LABEL = {
    "holomorphic": "anti-holomorphic",
    "anti-holomorphic": "holomorphic",
    "real-trapped": "real-trapped",
    "module-trapped": "module-trapped",
}


def symmetric_reading(expr):
    """Judge label (authority) + 5-way symmetric reading + both derivatives."""
    expr = sp.expand(expr)
    dfdz = sp.simplify(sp.diff(expr, z))
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    label, _ = certify_1field(expr)                 # AUTHORITY
    holo_pure = (dfdzbar == 0)
    anti_pure = (dfdz == 0)
    if label in ("real-trapped", "module-trapped"):
        sym = label
    elif holo_pure:
        sym = "holo-pure"
    elif anti_pure:
        sym = "anti-pure"
    else:
        sym = "mixed"
    return dict(judge=label, sym=sym, holo_pure=holo_pure, anti_pure=anti_pure,
                dfdz=dfdz, dfdzbar=dfdzbar)


def mirror_symmetry(expr):
    """judge(f) and judge(full_conj(f)) must be mirror labels."""
    lab_f, _ = certify_1field(sp.expand(expr))
    lab_m, _ = certify_1field(sp.expand(full_conj(expr)))
    expected = MIRROR_LABEL.get(lab_f, lab_f)
    return lab_f, lab_m, (lab_m == expected)


def line(c="=", n=78):
    print(c * n)


# ---------------------------------------------------------------------------
# BALANCED calibration panel: as many holo as anti, plus traps and a genuine mix.
# Each (label, expr, expected_judge, expected_sym).
# ---------------------------------------------------------------------------
HOLO = [
    ("z",            z,              "holomorphic", "holo-pure"),
    ("z**2",         z**2,           "holomorphic", "holo-pure"),
    ("exp(z)",       sp.exp(z),      "holomorphic", "holo-pure"),
    ("log(z)",       sp.log(z),      "holomorphic", "holo-pure"),
    ("z**3 + z",     z**3 + z,       "holomorphic", "holo-pure"),
]
ANTI = [   # exact mirrors of HOLO
    ("zbar",         zbar,           "anti-holomorphic", "anti-pure"),
    ("zbar**2",      zbar**2,        "anti-holomorphic", "anti-pure"),
    ("exp(zbar)",    sp.exp(zbar),   "anti-holomorphic", "anti-pure"),
    ("log(zbar)",    sp.log(zbar),   "anti-holomorphic", "anti-pure"),
    ("zbar**3+zbar", zbar**3 + zbar, "anti-holomorphic", "anti-pure"),
]
TRAPS = [
    ("z + zbar",         z + zbar,                    "real-trapped",   "real-trapped"),
    ("z*zbar (|z|^2)",   z*zbar,                      "real-trapped",   "real-trapped"),
    ("log z + log zbar", sp.log(z) + sp.log(zbar),    "real-trapped",   "real-trapped"),
    ("z/zbar",           z/zbar,                      "module-trapped", "module-trapped"),
    ("z**2 * zbar",      z**2*zbar,                   "module-trapped", "module-trapped"),
]
MIXED = [  # genuine additive anti -> judge 'anti', symmetric reading 'mixed'
    ("z + 0.3*zbar",     z + sp.Rational(3,10)*zbar,  "anti-holomorphic", "mixed"),
    ("zbar + 0.3*z",     zbar + sp.Rational(3,10)*z,  "anti-holomorphic", "mixed"),
]


def run_panel(title, panel):
    print(f"\n[{title}]")
    ok = True
    for name, expr, exp_judge, exp_sym in panel:
        r = symmetric_reading(expr)
        good = (r["judge"] == exp_judge and r["sym"] == exp_sym)
        ok = ok and good
        print(f"   {name:<20} judge={r['judge']:<18} sym={r['sym']:<14} "
              f"{'OK' if good else 'FAIL!!'}")
    return ok


def run_mirror(title, panel, expect_mirror):
    """expect_mirror=True : labels MUST be mirror (holo<->anti, traps invariant).
    expect_mirror=False : labels expected NON-mirror -> exposes the judge catch-all."""
    tag = "must be mirror" if expect_mirror else "expected NON-mirror (exposes catch-all)"
    print(f"\n[MIRROR {title}] judge(f) vs judge(full_conj(f)) -- {tag}")
    ok = True
    for name, expr, *_ in panel:
        lab_f, lab_m, is_mirror = mirror_symmetry(expr)
        good = (is_mirror == expect_mirror)
        ok = ok and good
        verdict = "OK" if good else "FAIL!!"
        if not expect_mirror and good:
            verdict = "OK (asymmetry exposed)"
        print(f"   {name:<20} {lab_f:<18} -> conj -> {lab_m:<18} {verdict}")
    return ok


def run_never_false_anti():
    print("\n[NEVER FALSE ANTI ON HOLO] every holomorphic form must judge 'holomorphic'")
    ok = True
    for name, expr, *_ in HOLO:
        lab, _ = certify_1field(sp.expand(expr))
        good = (lab == "holomorphic")
        ok = ok and good
        print(f"   {name:<20} -> {lab:<18} {'OK' if good else 'LEAK!!'}")
    return ok


def ledger(panel_all):
    """Two living columns + rejects, from the symmetric reading."""
    holo_col, anti_col, rejects = [], [], []
    for name, expr, *_ in panel_all:
        r = symmetric_reading(expr)
        if r["sym"] == "holo-pure":
            holo_col.append(name)
        elif r["sym"] in ("anti-pure", "mixed"):
            anti_col.append(name)
        else:
            rejects.append(f"{name} [{r['sym']}]")
    print("\n[LEDGER]")
    print("  HOLO confirmed :", ", ".join(holo_col))
    print("  ANTI confirmed :", ", ".join(anti_col))
    print("  REJECTS (trap) :", ", ".join(rejects))


def run_2field_mixte():
    """Canonical MIXTE eml-star form, two fields: exp(z) - log(wbar)."""
    print("\n[2-FIELD canonical MIXTE]  exp(z) - log(conj y)  ==  exp(z) - log(wbar)")
    expr = sp.exp(z) - sp.log(wbar)
    cls, d = certify_2field(expr)
    ok = "CROSS-CONJUGATE z*conj(w)" in cls
    print(f"   exp(z) - log(wbar) -> {cls[:48]:<48} {'OK' if ok else 'FAIL!!'}")
    print(f"     d_zbar={d['d_zbar']}, d_w={d['d_w']} (both 0 => holo z, anti w)")
    return ok


if __name__ == "__main__":
    line()
    print("symmetry_harness -- holo/anti balanced calibration (layer over judge_v2)")
    line()
    ALL = HOLO + ANTI + TRAPS + MIXED
    r1 = run_panel("HOLO", HOLO)
    r2 = run_panel("ANTI", ANTI)
    r3 = run_panel("TRAPS", TRAPS)
    r4 = run_panel("MIXED (genuine additive anti)", MIXED)
    r5 = run_mirror("pure + traps", HOLO + ANTI + TRAPS, expect_mirror=True)
    r6 = run_mirror("mixed", MIXED, expect_mirror=False)
    r7 = run_never_false_anti()
    r8 = run_2field_mixte()
    ledger(ALL)
    line()
    calib_ok = all([r1, r2, r3, r4, r7, r8])
    mirror_ok = all([r5, r6])
    print("CALIBRATION (panels + never-false-anti + 2field):",
          "PASS" if calib_ok else "FAIL")
    print("MIRROR DIAGNOSTIC (pure/traps symmetric, mixed exposes catch-all):",
          "PASS" if mirror_ok else "FAIL")
    print("Reading: the judge is mirror-symmetric on PURE holo/anti and on traps;")
    print("on MIXED forms it lumps pure-anti + mixed under 'anti-holomorphic'.")
    print("The 5-way 'sym=' reading is the symmetric fix, layered on the authority.")
    line()
    import sys
    sys.exit(0 if (calib_ok and mirror_ok) else 1)
