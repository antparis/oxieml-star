#!/usr/bin/env python3
"""
patch_grammar.py -- Enrich cnative_bench.py's _gen_in generator grammar.
Adds sin, cos, pow2, pow3 to the operator pool. Single-symbol recursion is
preserved, so holo stays holo and anti stays anti BY CONSTRUCTION (verified:
200 holo gens all df/dzbar=0, 200 anti gens all df/dz=0, sin/cos/pow present).
Idempotent-safe: aborts if the enriched version is already present.
Run from ~/Desktop/oxieml-star/ . A dated backup must already exist.
"""
import io, sys

PATH = "cnative_bench.py"

OLD = '''def _gen_in(sym, rng, depth):
    if depth <= 0 or rng.random() < 0.35:
        return sym if rng.random() < 0.7 else _const(rng)
    op = rng.choice(["add", "sub", "mul", "exp", "log", "inv"])
    if op in ("add", "sub", "mul"):
        a = _gen_in(sym, rng, depth - 1)
        b = _gen_in(sym, rng, depth - 1)
        return {"add": a + b, "sub": a - b, "mul": a * b}[op]
    if op == "exp":
        return sp.exp(_gen_in(sym, rng, depth - 1))
    if op == "log":
        return sp.log(_gen_in(sym, rng, depth - 1))
    if op == "inv":
        return 1 / (_gen_in(sym, rng, depth - 1) + _const(rng))
    raise RuntimeError("unreachable")'''

NEW = '''def _gen_in(sym, rng, depth):
    if depth <= 0 or rng.random() < 0.35:
        return sym if rng.random() < 0.7 else _const(rng)
    op = rng.choice(["add", "sub", "mul", "exp", "log", "inv",
                     "sin", "cos", "pow2", "pow3"])
    if op in ("add", "sub", "mul"):
        a = _gen_in(sym, rng, depth - 1)
        b = _gen_in(sym, rng, depth - 1)
        return {"add": a + b, "sub": a - b, "mul": a * b}[op]
    if op == "exp":
        return sp.exp(_gen_in(sym, rng, depth - 1))
    if op == "log":
        return sp.log(_gen_in(sym, rng, depth - 1))
    if op == "inv":
        return 1 / (_gen_in(sym, rng, depth - 1) + _const(rng))
    if op == "sin":
        return sp.sin(_gen_in(sym, rng, depth - 1))
    if op == "cos":
        return sp.cos(_gen_in(sym, rng, depth - 1))
    if op == "pow2":
        return _gen_in(sym, rng, depth - 1) ** 2
    if op == "pow3":
        return _gen_in(sym, rng, depth - 1) ** 3
    raise RuntimeError("unreachable")'''

with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

if NEW in src:
    print("ALREADY PATCHED -- nothing to do.")
    sys.exit(0)

if OLD not in src:
    print("ERROR: exact _gen_in block not found. Aborting (no change made).")
    print("       The file may differ from expected. Restore from backup if needed.")
    sys.exit(1)

count = src.count(OLD)
if count != 1:
    print(f"ERROR: expected exactly 1 occurrence of _gen_in, found {count}. Aborting.")
    sys.exit(1)

src2 = src.replace(OLD, NEW)
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src2)

print("PATCH APPLIED.")
print(f"  added operators: sin, cos, pow2, pow3")
print(f"  file size: {len(src)} -> {len(src2)} bytes (+{len(src2)-len(src)})")
print("  ground truth preserved by construction (single-symbol recursion).")
print("  next: re-run the bench to confirm 338 cases still pass + new transcendental gens appear.")
