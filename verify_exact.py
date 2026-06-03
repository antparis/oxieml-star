#!/usr/bin/env python3
"""
verify_exact.py
The "exact judge": symbolically certifies whether a PySR-discovered formula
is holomorphic or anti-holomorphic, using exact SymPy algebra (infinite
precision), independently of PySR's numerical verdict.

Rationale
---------
PySR detects structure numerically (~1e-32) but can be fooled by appearances:
e.g. conj(conj(z)^2+c)^2+c LOOKS anti-holomorphic but simplifies to a purely
holomorphic polynomial. A numerical fit cannot prove this; exact symbolic
algebra can.

Certification criterion (Wirtinger derivative)
----------------------------------------------
A function f(z, zbar) is holomorphic if and only if df/d(zbar) = 0.
We treat z and zbar = conj(z) as independent symbols (Wirtinger calculus),
substitute the PySR operators, simplify, and compute df/d(zbar):
  - df/d(zbar) == 0  ->  HOLOMORPHIC   (no irreducible conjugation)
  - df/d(zbar) != 0  ->  ANTI-HOLOMORPHIC (irreducible conjugation present)

This is exact: it sees through apparent conjugations that cancel
(e.g. conj(conj(z)) = z) and through conjugations hidden in real/imag parts.

Usage
-----
    python3 verify_exact.py double_validation_v3_result.json
    python3 verify_exact.py --formula "my_conj(x0)*x0"   # ad-hoc test

Author: Anthony Monnerot, 2026.
"""
import sys
import json
import argparse
import sympy as sp

# Wirtinger setup: z and zbar are INDEPENDENT symbols.
z = sp.Symbol("z")
zbar = sp.Symbol("zbar")


# ------------------------------------------------------------------
# Operator definitions in the Wirtinger picture.
# x0 in PySR is the complex input. We map x0 -> z, and conj(x0) -> zbar.
# This is the key: instead of sympy.conjugate(z) (which sympy may not
# differentiate cleanly), we use the independent symbol zbar.
# ------------------------------------------------------------------
def op_conj(expr):
    """conj of an expression: swap z<->zbar throughout."""
    return expr.subs({z: zbar, zbar: z}, simultaneous=True)


def op_my_real(expr):
    """Re(u) = (u + conj(u)) / 2."""
    return (expr + op_conj(expr)) / 2


def op_my_imag(expr):
    """Im(u) = (u - conj(u)) / (2i)."""
    return (expr - op_conj(expr)) / (2 * sp.I)


def op_my_abs2(expr):
    """|u|^2 = u * conj(u)."""
    return expr * op_conj(expr)


def op_eml(x, y):
    """eml(x, y) = exp(x) - log(y). Holomorphic."""
    return sp.exp(x) - sp.log(y)


def op_emlstar(x, y):
    """emlstar(x, y) = exp(x) - log(conj(y)). Canonical MIXTE (conj on 2nd arg only)."""
    return sp.exp(x) - sp.log(op_conj(y))


def op_my_conj(expr):
    return op_conj(expr)
def op_inv(expr):
    """inv(z) = 1/z. Holomorphic."""
    return 1 / expr
def op_inv_bar(expr):
    """inv_bar(z) = 1/conj(z). Anti-holomorphic."""
    return 1 / op_conj(expr)


# Namespace for sympify: maps PySR tokens to our Wirtinger-aware functions.
LOCALS = {
    "x0": z,
    "I": sp.I,
    "j": sp.I,  # PySR prints complex constants with 'j'
    "my_real": op_my_real,
    "my_imag": op_my_imag,
    "my_abs2": op_my_abs2,
    "my_conj": op_my_conj,
    "inv": op_inv,
    "inv_bar": op_inv_bar,
    "eml": op_eml,
    "emlstar": op_emlstar,
    "exp": sp.exp,
    "log": sp.log,
    "sin": sp.sin,
    "cos": sp.cos,
}


def normalize_pysr_string(s):
    """Convert a PySR equation string into something sympify can parse.

    PySR prints complex literals like '1.94 + 0.53j' or '... - 0.27j)'.
    Python/sympy use 'j' suffix on a number for imaginary, but sympify does
    not. We convert a trailing 'j' on a numeric literal into '*I'.
    """
    import re
    # Replace <number>j  ->  (<number>*I). Handles 0.53j, 9.4e91j, 27015j etc.
    # A numeric literal: digits, optional decimal, optional exponent.
    num = r"(?<![A-Za-z_0-9.])(\d+\.?\d*(?:[eE][+-]?\d+)?)j"
    s = re.sub(num, r"(\1*I)", s)
    return s


def parse_formula(eq_str):
    """Parse a PySR formula string into a SymPy expression in (z, zbar)."""
    norm = normalize_pysr_string(eq_str)
    expr = sp.sympify(norm, locals=LOCALS)
    return expr


def certify(eq_str):
    """Return ('holomorphic'|'anti-holomorphic', simplified_expr, dfdzbar)."""
    expr = parse_formula(eq_str)
    expr = sp.expand(expr)
    # Wirtinger derivative w.r.t. zbar
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    is_holo = (dfdzbar == 0)
    verdict = "holomorphic" if is_holo else "anti-holomorphic"
    return verdict, expr, dfdzbar


def verdict_short(v):
    return "holo" if v == "holomorphic" else "anti"


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Exact SymPy certification of PySR formulas.")
    parser.add_argument("json_file", nargs="?",
                        help="PySR result JSON to certify")
    parser.add_argument("--formula", help="certify a single ad-hoc formula")
    args = parser.parse_args()

    if args.formula:
        print(f"Formula : {args.formula}")
        try:
            verdict, expr, dfdzbar = certify(args.formula)
            print(f"Simplified : {expr}")
            print(f"df/d(zbar) : {dfdzbar}")
            print(f"VERDICT    : {verdict.upper()}")
        except Exception as e:
            print(f"ERROR parsing/certifying: {e}")
        return

    if not args.json_file:
        parser.error("provide a JSON file or --formula")

    with open(args.json_file) as f:
        data = json.load(f)

    print(f"{'='*78}")
    print(f"EXACT SYMBOLIC CERTIFICATION of {args.json_file}")
    print(f"(criterion: df/d(zbar) == 0  =>  holomorphic)")
    print(f"{'='*78}\n")

    header = "{:<16}{:<10}{:<14}{:<14}{:<14}".format(
        "Dataset", "PySR_num", "Judge_A", "Judge_B", "Agreement")
    print(header)
    print("-" * 78)

    runs = data.get("runs", {})
    for ds_name, tbs in runs.items():
        cells = {}
        for tb_name in ("A_emlstar", "B_re"):
            run = tbs.get(tb_name)
            if run is None:
                cells[tb_name] = ("--", "n/a")
                continue
            eq = run["best_equation"]
            pysr_anti = run["anti_holomorphic"]
            try:
                verdict, _, _ = certify(eq)
                cells[tb_name] = (verdict_short(verdict),
                                  "anti" if pysr_anti else "holo")
            except Exception as e:
                cells[tb_name] = ("ERR", "anti" if pysr_anti else "holo")

        judge_a = cells["A_emlstar"][0]
        judge_b = cells["B_re"][0]
        pysr_a = cells["A_emlstar"][1]
        # agreement: do the two judges agree, and do they match PySR?
        judges_agree = (judge_a == judge_b)
        match_pysr = (judge_a == pysr_a) if judge_a not in ("ERR", "--") else None
        agree_str = "judges OK" if judges_agree else "JUDGES DIFFER"
        if match_pysr is False:
            agree_str += " / vs PySR !"

        print("{:<16}{:<10}{:<14}{:<14}{:<14}".format(
            ds_name, pysr_a, judge_a, judge_b, agree_str))

    print("\nNote: 'Judge' is the exact SymPy verdict (infinite precision).")
    print("'PySR_num' is the numerical detector verdict (Route A).")
    print("When they disagree, the exact judge is authoritative.")


if __name__ == "__main__":
    main()
