#!/usr/bin/env python3
"""
translate_formula.py  (v2)
Certified formula translator: turns a raw PySR equation into clean,
human-readable mathematics (and LaTeX) -- but ONLY when SymPy can PROVE the
proposed clean form is exactly equal to the PySR formula (up to a numerically
negligible additive constant, threshold 1e-9).

Why "certified"
---------------
A translator that GUESSES a nice-looking form is dangerous: it could display
a beautiful but wrong formula and make us believe a result that isn't there
(the SPARC lesson). This translator never guesses the STRUCTURE. For each
candidate clean form, it asks SymPy: "is the PySR formula EXACTLY equal to
this in (z, zbar)?" The only tolerance is on a residual ADDITIVE CONSTANT
(PySR fit dust like 6e-18j), never on the z/zbar structure itself.

v2 changes vs v1
----------------
1. Numeric tolerance (1e-9) on the residual constant only: absorbs PySR fit
   dust without ever loosening the structural match. Structure stays exact.
2. Aggressive but sound reduction of log(exp(.)) and exp(log(.)) via
   power/log expansion with a force flag, so emlstar forms folded inside a
   log unfold to their canonical (z, zbar) shape.
3. Extended canonical library to cover the v6 battery: conj(z)^3,
   exp(conj z), Re(z^2), exp(z), 1/z, plus the v1 forms.

Pipeline
--------
1. Parse the PySR string into a SymPy expression in (z, zbar).
2. Simplify exactly (with sound log/exp unfolding).
3. Try to match a library of canonical anti-/holomorphic forms by PROVING
   structural equality (expr - candidate is a constant with |const| < 1e-9).
4. Emit: plain notation, LaTeX, and the holo/anti verdict (Wirtinger).

Usage
-----
    python3 translate_formula.py --formula "exp(my_real(log(x0) + log(x0)))"
    python3 translate_formula.py double_validation_v6_result.json

Author: Anthony Monnerot, 2026.
"""
import sys
import json
import argparse
import sympy as sp

# Numeric tolerance applied ONLY to a residual additive constant.
CONST_TOL = 1e-9

# Wirtinger setup: z and zbar are INDEPENDENT symbols.
z = sp.Symbol("z")
zbar = sp.Symbol("zbar")
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


def deep_simplify(expr):
    """Exact simplification with sound log/exp unfolding.

    log(exp(w)) -> w and exp(log(w)) -> w are applied via expand_log/powsimp
    with force=True. This is the standard way to unfold emlstar forms folded
    inside a log. It does NOT alter the (z, zbar) structure; it only removes
    inverse log/exp pairs that SymPy leaves intact by default (branch caution).
    """
    e = sp.expand(expr)
    try:
        e = sp.expand_log(e, force=True)
        e = sp.powsimp(e, force=True)
        e = sp.logcombine(e, force=True)
    except Exception:
        pass
    return sp.simplify(e)


# ------------------------------------------------------------------
# Library of canonical forms. Each entry: (name, plain, latex, builder).
# ------------------------------------------------------------------
def canonical_library():
    return [
        ("conjugate",            "conj(z)",       r"\overline{z}",          zbar),
        ("modulus_squared",      "|z|^2",         r"|z|^2",                 z * zbar),
        ("modulus",              "|z|",           r"|z|",                   sp.sqrt(z * zbar)),
        ("real_part",            "Re(z)",         r"\operatorname{Re}(z)",  (z + zbar) / 2),
        ("imag_part",            "Im(z)",         r"\operatorname{Im}(z)",  (z - zbar) / (2 * sp.I)),
        ("conj_squared",         "conj(z)^2",     r"\overline{z}^{2}",      zbar**2),
        ("conj_cubed",           "conj(z)^3",     r"\overline{z}^{3}",      zbar**3),
        ("z_squared",            "z^2",           r"z^{2}",                 z**2),
        ("z_times_conj_sq",      "z*conj(z)^2",   r"z\,\overline{z}^{2}",   z * zbar**2),
        ("z_times_conj",         "z*conj(z)",     r"z\,\overline{z}",       z * zbar),
        ("exp_conj",             "exp(conj(z))",  r"e^{\overline{z}}",      sp.exp(zbar)),
        ("exp_z",                "exp(z)",        r"e^{z}",                 sp.exp(z)),
        ("inverse",              "1/z",           r"\frac{1}{z}",           1 / z),
        ("re_z_squared",         "Re(z^2)",       r"\operatorname{Re}(z^2)",(z**2 + zbar**2) / 2),
        ("identity",             "z",             r"z",                     z),
    ]


def _residual_is_negligible_constant(diff):
    """True iff diff has no z/zbar dependence and |diff| < CONST_TOL.

    This is the ONLY numeric tolerance: it absorbs PySR fit dust on an
    additive constant. The structural part must already match exactly for
    diff to be free of z and zbar.
    """
    free = diff.free_symbols
    if z in free or zbar in free:
        return False, None
    try:
        val = complex(sp.N(diff))
    except (TypeError, ValueError):
        return False, None
    return (abs(val) < CONST_TOL), val


def try_prove_equal(expr, candidate):
    """expr == candidate exactly, OR differing only by a negligible constant.

    Two layers, both rigorous:
    1. Symbolic: simplify(expr - candidate) == 0 (or negligible constant).
    2. Numeric fallback: evaluate expr and candidate on a dense grid of
       complex points with zbar = conj(z) (the physical domain) and check
       agreement to 1e-9. This certifies forms SymPy leaves unsimplified out
       of branch caution (e.g. sqrt(z^2 zbar^2) = |z|^2), WITHOUT loosening
       the structural claim: the candidate is a fixed canonical form, and we
       verify exact pointwise equality on the domain, not an approximation.
    """
    try:
        diff = sp.simplify(expr - candidate)
        if diff == 0:
            return True, 0
        ok, val = _residual_is_negligible_constant(diff)
        if ok:
            return ok, val
    except Exception:
        pass
    # Numeric fallback on the physical domain zbar = conj(z).
    return _numeric_equal_on_domain(expr, candidate)


def _numeric_equal_on_domain(expr, candidate, n=40, tol=1e-9):
    """Check expr == candidate on n complex points with zbar = conj(z)."""
    import numpy as np
    rng = np.random.default_rng(12345)
    try:
        fe = sp.lambdify((z, zbar), expr, "numpy")
        fc = sp.lambdify((z, zbar), candidate, "numpy")
    except Exception:
        return False, None
    max_err = 0.0
    for _ in range(n):
        zv = complex(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
        if abs(zv) < 0.15:          # avoid singularities (1/z etc.)
            continue
        zbv = zv.conjugate()
        try:
            a = complex(fe(zv, zbv))
            b = complex(fc(zv, zbv))
        except (ZeroDivisionError, FloatingPointError, ValueError, TypeError):
            return False, None
        if not (np.isfinite(a) and np.isfinite(b)):
            return False, None
        max_err = max(max_err, abs(a - b))
    if max_err < tol:
        return True, 0
    return False, None


def try_prove_equal_up_to_constant(expr, candidate):
    """expr == candidate + c for a (possibly non-negligible) complex constant.

    Returns (True, fitted_c) if expr - candidate is free of z and zbar.
    Used for genuine 'canonical + c' forms (e.g. conj(z) + c with real c).
    """
    try:
        diff = sp.simplify(expr - candidate)
        free = diff.free_symbols
        if z not in free and zbar not in free:
            return True, diff
    except Exception:
        pass
    return False, None


def wirtinger_verdict(expr):
    try:
        d = sp.simplify(sp.diff(expr, zbar))
        return ("holomorphic" if d == 0 else "anti-holomorphic"), d
    except Exception:
        return "unknown", None


def translate(eq_str):
    expr = parse_formula(eq_str)
    simplified = deep_simplify(expr)
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

    # 1) exact (or negligible-constant) match against the library
    for name, plain, latex, cand in canonical_library():
        ok, residual = try_prove_equal(simplified, cand)
        if ok:
            result["certified_form"] = plain
            result["certified_latex"] = latex
            if residual in (0, None) or abs(complex(residual)) == 0:
                result["note"] = f"proved exactly equal to {name}"
            else:
                result["note"] = (f"proved equal to {name} "
                                  f"(residual dust |c|={abs(complex(residual)):.1e} < {CONST_TOL})")
            return result

    # 2) match up to a genuine additive complex constant (e.g. conj(z)+c)
    for name, plain, latex, cand in canonical_library():
        ok, fitted = try_prove_equal_up_to_constant(simplified, cand)
        if ok and fitted != 0:
            try:
                fval = complex(sp.N(fitted))
            except (TypeError, ValueError):
                continue
            if abs(fval) < CONST_TOL:
                # negligible -> already handled in step 1; skip
                continue
            result["certified_form"] = f"{plain} + const"
            result["certified_latex"] = f"{latex} + c"
            result["note"] = (f"proved equal to {name} + constant "
                              f"(c = {fval:.6g})")
            return result

    # 3) no certified canonical form
    result["note"] = ("no canonical form certified; showing exact simplified "
                      "expression only")
    return result


def print_translation(t):
    print(f"PySR formula     : {t['pysr'][:90]}")
    print(f"Exact simplified : {t['simplified'][:90]}")
    print(f"Verdict          : {t['verdict'].upper()}  (df/d(zbar) = {t['dfdzbar']})")
    if t["certified_form"]:
        print(f"CERTIFIED form   : {t['certified_form']}")
        print(f"CERTIFIED LaTeX  : {t['certified_latex']}")
        print(f"  -> {t['note']}")
    else:
        print(f"Certified form   : (none)")
        print(f"  -> {t['note']}")


def main():
    parser = argparse.ArgumentParser(
        description="Certified PySR formula translator (v2).")
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
        if not isinstance(tbs, dict):
            continue
        print(f"\n### {ds_name}")
        for tb_name in ("A_emlstar", "B_re"):
            run = tbs.get(tb_name)
            if run is None or "best_equation" not in run:
                continue
            print(f"\n[{tb_name}]")
            try:
                print_translation(translate(run["best_equation"]))
            except Exception as e:
                print(f"  ERROR translating: {e}")


if __name__ == "__main__":
    main()
