#!/usr/bin/env python3
"""
reality_check.py  --  ADD-ON to verify_exact.py. Does NOT modify it.

Adds the SPARC reality discriminator ON TOP of the exact judge. The judge
(certify) keeps its two-verdict contract untouched; this script imports it
and prints an extra flag, so no existing harness breaks.

  judge = 'anti-holomorphic'  AND  field is REAL (f == conj f)
      -> the anti-holomorphic part is the conjugate mirror of the
         holomorphic part: a SPARC-type trap (conj(x)=x degeneracy),
         NOT a genuine independent anti structure.
  judge = 'anti-holomorphic'  AND  field is COMPLEX (f != conj f)
      -> genuine, chiral-asymmetric anti structure (the eml* target):
         e.g. unequal holo/anti log weights -> nonzero conformal spin.
  judge = 'holomorphic'
      -> reality flag is irrelevant (df/dzbar == 0).

CAVEAT (non-negotiable): this test is EXACT and is only valid on an exact
symbolic formula. On real / noisy data it is as fragile as df/dzbar==0
(a tiny parasitic term flips it). On real data the arbiter remains the
NEGATIVE CONTROL (shuffle) plus an exploitable MSE -- never this flag alone.

Acceptance gate for a genuine (e.g. transcendental) anti detection:
    judge == 'anti-holomorphic'  AND  reality == 'complex'
    AND  MSE < 1e-3              AND  negative control rejected.

Usage:
    python3 reality_check.py --formula "log(x0) + 0.3333*log(my_conj(x0))"
    python3 reality_check.py result.json        # JSON with a best_equation field

Author: Anthony Monnerot, 2026.
"""
import argparse
import json
import os

import sympy as sp

from verify_exact import certify   # the single arbiter, imported UNCHANGED

z = sp.Symbol("z")
zbar = sp.Symbol("zbar")


def _conj(expr):
    return expr.subs({z: zbar, zbar: z}, simultaneous=True)


def reality_flag(expr):
    e = sp.expand(expr)
    return "real" if sp.simplify(e - _conj(e)) == 0 else "complex"


def assess(eq_str):
    verdict, expr, dfdzbar = certify(eq_str)
    if verdict == "holomorphic":
        flag = "n/a"
        label = "HOLOMORPHIC"
    else:
        flag = reality_flag(expr)
        if flag == "real":
            label = ("REAL-TRAPPED (SPARC-type: anti = conjugate mirror "
                     "of holo, NOT a genuine independent structure)")
        else:
            label = "GENUINE ANTI-HOLOMORPHIC (chiral / complex)"
    return verdict, expr, dfdzbar, flag, label


def _print(eq_str):
    verdict, expr, dfdzbar, flag, label = assess(eq_str)
    print(f"Formula      : {eq_str}")
    print(f"Simplified   : {expr}")
    print(f"df/d(zbar)   : {dfdzbar}")
    print(f"Judge verdict: {verdict.upper()}    (certify, UNCHANGED)")
    print(f"Reality flag : {flag}")
    print(f"=> CLASS     : {label}")


def main():
    p = argparse.ArgumentParser(
        description="Reality discriminator on top of the exact judge "
                    "(verify_exact.certify). Does not modify the judge.")
    p.add_argument("json_file", nargs="?",
                   help="JSON result file containing a 'best_equation' field")
    p.add_argument("--formula", help="assess a single ad-hoc formula")
    args = p.parse_args()

    if args.formula:
        _print(args.formula)
        return

    if not args.json_file:
        p.error("provide a JSON file (with best_equation) or --formula")

    if not os.path.exists(args.json_file):
        p.error(f"missing file: {args.json_file}")

    with open(args.json_file) as fh:
        data = json.load(fh)

    eq = data.get("best_equation")
    if eq is None:
        p.error(f"{args.json_file} has no top-level 'best_equation' field")
    _print(eq)


if __name__ == "__main__":
    main()
