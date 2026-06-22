#!/usr/bin/env python3
"""patch_blindspot.py -- close the judge_v2 module-trapped blind spot.
Replaces the final return of is_module_trapped to also catch L = pure-imaginary CONSTANT
(the |z|^(is) inverse-square case). Minimal, surgical. Idempotent (refuses if already patched)."""
import re, sys

PATH = "judge_v2.py"
src = open(PATH).read()

OLD = "        prod_only = sp.simplify(L.subs({z: t*z, zbar: zbar/t}) - L) == 0\n        return bool(L_real and prod_only)"
NEW = ("        prod_only = sp.simplify(L.subs({z: t*z, zbar: zbar/t}) - L) == 0\n"
       "        # blind-spot fix (2026-06-22): L = pure-imaginary CONSTANT is also a modulus\n"
       "        # power (imaginary exponent, e.g. |z|^(is) inverse-square). Catch it too.\n"
       "        L_const = (sp.simplify(sp.diff(L, z)) == 0 and sp.simplify(sp.diff(L, zbar)) == 0)\n"
       "        L_pure_imag = (sp.simplify(L + full_conj(L)) == 0)\n"
       "        return bool((L_real or (L_const and L_pure_imag)) and prod_only)")

if "blind-spot fix (2026-06-22)" in src:
    print("ALREADY PATCHED -- no change."); sys.exit(0)
if OLD not in src:
    print("PATTERN NOT FOUND -- aborting (no change). The is_module_trapped return line"); 
    print("does not match the expected text; inspect judge_v2.py manually."); sys.exit(1)
src2 = src.replace(OLD, NEW)
open(PATH, "w").write(src2)
print("PATCH APPLIED: is_module_trapped now also catches L = pure-imaginary constant.")
print("  condition: (L_real OR (L_const AND L_pure_imag)) AND prod_only")
