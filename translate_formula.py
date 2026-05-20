#!/usr/bin/env python3
"""
translate_formula.py
Certified formula translator: turns a raw PySR equation into clean,
human-readable mathematics (and LaTeX) -- but ONLY when SymPy can PROVE the
proposed clean form is exactly equal to the PySR formula.

Why "certified"
---------------
A translator that GUESSES a nice-looking form is dangerous: it could display
a beautiful but wrong formula and make us believe a result that isn't there
(the SPARC lesson). This translator never guesses. For each candidate clean
form, it asks SymPy: "is the PySR formula EXACTLY equal to this?" It outputs
a translation only if the symbolic difference simplifies to zero. Otherwise
it honestly reports the raw simplified expression and "form not certified".

Pipeline
--------
1. Parse the PySR string into a SymPy expression in (z, zbar)  [reuses the
   judge's operator semantics: my_real, emlstar, my_conj, eml, ...].
2. Simplify exactly.
3. Try to match a library of canonical anti-/holomorphic forms by PROVING
   equality (expr - candidate == 0 after simplification).
4. Emit: plain notation, LaTeX, and the holo/anti verdict (Wirtinger).

Usage
-----
    python3 translate_formula.py --formula "exp(my_real(log(x0) + log(x0)))"
    python3 translate_formula.py double_validation_v5_kids_result.json

Author: Anthony Monnerot, 2026.
"""
import sys
import json
import argparse
import sympy as sp

# Wirtinger setup: z and zbar are INDEPENDENT symbols.
z = sp.Symbol("z")
zbar = sp.Symbol("zbar")
# A free complex constant placeholder used in some canonical forms.
c = sp.Symbol("c")


# ------------------------------------------------------------------
# Operator semantics (identical to verify_exact.py).
# ------------------------------------------------------------------
def op_conj(expr):
    return expr.subs({z: zbar, zbar: z}, simultaneous=True)


def op_my_real(expr):
    return (expr + op_conj(expr)) / 2


def op_my_imag(expr):
    return (expr - op_conj(expr)) / (2 * sp.I)


def op_my_abs2(expr):
    return expr * op_conj(expr)


def op_eml(x, y):
    return sp.exp(x) - sp.log(y)


def op_emlstar(x, y):
    return sp.exp(op_conj(x)) - sp.log(op_conj(y))


LOCALS = {
    "x0": z, "I": sp.I, "j": sp.I,
    "my_real": op_my_real, "my_imag": op_my_imag, "my_abs2": op_my_abs2,
    "my_conj": op_conj, "eml": op_eml, "emlstar": op_emlstar,
    "exp": sp.exp, "log": sp.log, "sin": sp.sin, "cos": sp.cos,
}


def normalize_pysr_string(s):
    import re
    num = r"(?<![A-Za-z_0-9.])(\d+\.?\d*(?:[eE][+-]?\d+)?)j"
    return re.sub(num, r"(\1*I)", s)


def parse_formula(eq_str):
    return sp.sympify(normalize_pysr_string(eq_str), locals=LOCALS)


# ------------------------------------------------------------------
# Library of canonical forms. Each entry: (name, plain, latex, builder).
# The builder produces a SymPy expression in z, zbar (and possibly a fitted
# constant). We PROVE equality, we do not assume it.
# ------------------------------------------------------------------
def canonical_library():
    return [
        ("conjugate",            "conj(z)",       r"\overline{z}",        zbar),
        ("modulus_squared",      "|z|^2",         r"|z|^2",               z * zbar),
        ("modulus",              "|z|",           r"|z|",                 sp.sqrt(z * zbar)),
        ("real_part",            "Re(z)",         r"\operatorname{Re}(z)",(z + zbar) / 2),
        ("imag_part",            "Im(z)",         r"\operatorname{Im}(z)",(z - zbar) / (2 * sp.I)),
        ("conj_squared",         "conj(z)^2",     r"\overline{z}^{2}",    zbar**2),
        ("z_squared",            "z^2",           r"z^{2}",               z**2),
        ("z_times_conj_sq",      "z*conj(z)^2",   r"z\,\overline{z}^{2}", z * zbar**2),
        ("identity",             "z",             r"z",                   z),
    ]


def try_prove_equal(expr, candidate):
    """Return True iff expr == candidate exactly (difference simplifies to 0)."""
    try:
        diff = sp.simplify(expr - candidate)
        return diff == 0
    except Exception:
        return False


def try_prove_equal_up_to_constant(expr, candidate_builder_with_c):
    """Try expr == candidate + c for a complex constant c (additive offset).

    Returns (True, fitted_c) if expr - candidate is a constant (no z, zbar).
    """
    try:
        diff = sp.simplify(expr - candidate_builder_with_c)
        free = diff.free_symbols
        if z not in free and zbar not in free:
            # diff is a constant offset
            return True, diff
    except Exception:
        pass
    return False, None


def wirtinger_verdict(expr):
    try:
        d = sp.simplify(sp.diff(expr, zbar))
        return "holomorphic" if d == 0 else "anti-holomorphic", d
    except Exception:
        return "unknown", None


def translate(eq_str):
    """Return a dict describing the certified translation (or lack thereof)."""
    expr = sp.expand(parse_formula(eq_str))
    simplified = sp.simplify(expr)
    verdict, dzbar = wirtinger_verdict(expr)

    result = {
        "pysr": eq_str,
        "simplified": str(simplified),
        "verdict": verdict,
        "dfdzbar": str(dzbar),
        "certified_form": None,
        "certified_latex": None,
        "note": None,
    }

    # 1) exact match against the library
    for name, plain, latex, cand in canonical_library():
        if try_prove_equal(simplified, cand):
            result["certified_form"] = plain
            result["certified_latex"] = latex
            result["note"] = f"proved exactly equal to {name}"
            return result

    # 2) match up to an additive complex constant (e.g. conj(z)+c)
    for name, plain, latex, cand in canonical_library():
        ok, fitted = try_prove_equal_up_to_constant(simplified, cand)
        if ok and fitted != 0:
            result["certified_form"] = f"{plain} + const"
            result["certified_latex"] = f"{latex} + c"
            result["note"] = (f"proved equal to {name} + constant "
                              f"(c = {sp.nsimplify(fitted, rational=False)})")
            return result

    # 3) no certified canonical form
    result["note"] = ("no canonical form certified; showing exact simplified "
                      "expression only")
    return result


def print_translation(t):
    print(f"PySR formula     : {t['pysr']}")
    print(f"Exact simplified : {t['simplified']}")
    print(f"Verdict          : {t['verdict'].upper()}  (df/d(zbar) = {t['dfdzbar']})")
    if t["certified_form"]:
        print(f"CERTIFIED form   : {t['certified_form']}")
        print(f"CERTIFIED LaTeX  : {t['certified_latex']}")
        print(f"  -> {t['note']}")
    else:
        print(f"Certified form   : (none)")
        print(f"  -> {t['note']}")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Certified PySR formula translator.")
    parser.add_argument("json_file", nargs="?", help="PySR result JSON")
    parser.add_argument("--formula", help="translate a single ad-hoc formula")
    args = parser.parse_args()

    if args.formula:
        print_translation(translate(args.formula))
        return

    if not args.json_file:
        parser.error("provide a JSON file or --formula")

    with open(args.json_file) as f:
        data = json.load(f)

    print(f"{'='*72}")
    print(f"CERTIFIED TRANSLATION of {args.json_file}")
    print(f"{'='*72}")
    for ds_name, tbs in data.get("runs", {}).items():
        print(f"\n### {ds_name}")
        for tb_name in ("A_emlstar", "B_re"):
            run = tbs.get(tb_name)
            if run is None:
                continue
            print(f"\n[{tb_name}]")
            try:
                print_translation(translate(run["best_equation"]))
            except Exception as e:
                print(f"  ERROR translating: {e}")


if __name__ == "__main__":
    main()
