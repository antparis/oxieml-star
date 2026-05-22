#!/usr/bin/env python3
"""
classify_eml_family.py
Systematic enumeration and classification of EML-type operators,
certified by exact Wirtinger derivatives (SymPy), with correct
equivalence grouping.

Operator shape:  op(x, y) = f(a) - g(b)
  - f, g in {id, exp, log, sin, cos}
  - a in {x, conj(x)},  b in {y, conj(y)}
Probed as a single complex variable (x = y = z), so each operator is a
function of z and conj(z).

Classification (same Wirtinger engine as verify_exact.py: z and zbar are
INDEPENDENT symbols):
  - holomorphic       : df/dzbar == 0
  - anti-holomorphic  : df/dz    == 0
  - hybrid            : both nonzero (the eml* class)
  - constant          : both zero

Equivalence grouping: two operators are the SAME function iff they agree
numerically on a grid of (z, zbar) points sampled INDEPENDENTLY (zbar is
NOT the conjugate of z here, it is a free second variable). Sampling them
independently is what makes the fingerprint a true functional identity
test in the Wirtinger sense: two expressions match iff they are identical
as functions of the two independent variables z and zbar. This collapses
the raw list to GENUINELY DISTINCT operators per class.

Outputs:
  - prints a summary table
  - writes eml_family_classification.csv (one row per operator)

Author: Anthony Monnerot, 2026.
"""
import sympy as sp
import itertools
import csv
from collections import Counter, defaultdict

z = sp.Symbol("z")
zbar = sp.Symbol("zbar")

def conj(expr):
    return expr.subs({z: zbar, zbar: z}, simultaneous=True)

BASE = {
    "id":  lambda u: u,
    "exp": lambda u: sp.exp(u),
    "log": lambda u: sp.log(u),
    "sin": lambda u: sp.sin(u),
    "cos": lambda u: sp.cos(u),
}

def classify(expr):
    dfdz    = sp.simplify(sp.diff(expr, z))
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    hz, hzb = (dfdz == 0), (dfdzbar == 0)
    if hz and hzb: return "constant"
    if hzb:        return "holomorphic"
    if hz:         return "anti-holomorphic"
    return "hybrid"

# grid of INDEPENDENT (z, zbar) points -- key fix: zbar is a free variable,
# sampled independently of z, so the fingerprint is a true 2-variable
# functional identity test.
GRID = [(0.7+0.3j, 1.1-0.2j), (1.2-0.5j, 0.4+0.8j),
        (-0.4+0.9j, 0.6+0.1j), (0.5+1.1j, -0.3-0.7j),
        (1.5+0.2j, 0.9+1.3j), (0.8-0.6j, 1.4-0.4j)]

def fingerprint(expr):
    out = []
    for zv, zbv in GRID:
        try:
            val = complex(expr.subs({z: zv, zbar: zbv}))
            out.append((round(val.real, 5), round(val.imag, 5)))
        except Exception:
            out.append(("nan", "nan"))
    return tuple(out)

def generates(cls):
    """What the class can build, in plain terms."""
    return {
        "holomorphic":      "holomorphic functions only (no conj/Re/Im)",
        "anti-holomorphic": "anti-holomorphic functions (conj-only world)",
        "hybrid":           "BOTH: gives access to conj(z), hence Re, Im, |z|^2",
        "constant":         "constant / degenerate",
    }[cls]

def main():
    arg_choices = [("z", z), ("conj(z)", zbar)]
    rows = []
    for fname, f in BASE.items():
        for gname, g in BASE.items():
            for (a_lbl, a), (b_lbl, b) in itertools.product(arg_choices, arg_choices):
                expr = sp.expand(f(a) - g(b))
                cls = classify(expr)
                fp = fingerprint(expr)
                rows.append(dict(label=f"{fname}({a_lbl}) - {gname}({b_lbl})",
                                 f=fname, g=gname, a=a_lbl, b=b_lbl,
                                 cls=cls, fp=fp))

    counts = Counter(r["cls"] for r in rows)
    # distinct = unique fingerprints per class
    fps_by_class = defaultdict(set)
    for r in rows:
        fps_by_class[r["cls"]].add(r["fp"])
    distinct = {c: len(s) for c, s in fps_by_class.items()}

    print(f"Total operators enumerated: {len(rows)}")
    print("Raw class counts      :", dict(counts))
    print("DISTINCT per class    :", distinct)
    print()
    print("=== Named operators ===")
    def cls_of(fl, al, gl, bl):
        for r in rows:
            if r["f"]==fl and r["a"]==al and r["g"]==gl and r["b"]==bl:
                return r["cls"]
        return "?"
    print(f"  eml       = exp(z) - log(z)           -> {cls_of('exp','z','log','z')}")
    print(f"  eml*      = exp(z) - log(conj z)      -> {cls_of('exp','z','log','conj(z)')}  (your operator)")
    print(f"  eml*_pure = exp(conj z) - log(conj z) -> {cls_of('exp','conj(z)','log','conj(z)')}  (= conj(eml))")
    print(f"  eml_mir   = exp(conj z) - log(z)      -> {cls_of('exp','conj(z)','log','z')}  (UNNAMED mirror)")
    print()

    # one representative per distinct class+fingerprint
    for target in ("hybrid", "anti-holomorphic"):
        print(f"=== DISTINCT {target.upper()} operators (one representative each) ===")
        seen = set()
        for r in rows:
            if r["cls"] != target: continue
            if r["fp"] in seen: continue
            seen.add(r["fp"])
            print("  ", r["label"])
        print()

    # CSV export
    with open("eml_family_classification.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["operator", "f", "arg1", "g", "arg2", "class", "generates"])
        for r in rows:
            w.writerow([r["label"], r["f"], r["a"], r["g"], r["b"],
                        r["cls"], generates(r["cls"])])
    print("Wrote eml_family_classification.csv  (%d rows)" % len(rows))

if __name__ == "__main__":
    main()
