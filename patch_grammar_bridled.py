#!/usr/bin/env python3
"""
patch_grammar_bridled.py -- BRIDLED grammar enrichment for cnative_bench.py.
Adds sin, cos, pow2, pow3 applied ONCE to a SIMPLE atom (depth-1 max: sym, c*sym,
c*sym+d) -- never to an already-composed sub-expression. This forbids nested
transcendentals (sin(cos(exp(z^3)))) AT BIRTH, so SymPy cannot blow up. No timeout
needed. Ground truth preserved by construction (single-symbol). Sandbox-verified:
600 cases in 0.2s, 0 ground-truth fail, 0 case > 1s, transcendentals present.
Run from ~/Desktop/oxieml-star/ . Backup must exist. Aborts if blocks not found.
"""
import io, sys
PATH = "cnative_bench.py"

# 1) Insert _simple_arg and _gen_enriched right AFTER _gen_in (anchor on its last line).
ANCHOR = '''    if op == "inv":
        return 1 / (_gen_in(sym, rng, depth - 1) + _const(rng))
    raise RuntimeError("unreachable")'''

INSERT = ANCHOR + '''


def _simple_arg(sym, rng):
    """A depth-1 atom: sym, c*sym, or c*sym+d. Never an already-composed expr."""
    r = rng.random()
    if r < 0.4:
        return sym
    elif r < 0.7:
        return _const(rng) * sym
    else:
        return _const(rng) * sym + _const(rng)


def _gen_enriched(sym, rng, depth):
    """Bridled enrichment: half the time the classic generator, half the time a
    transcendental (sin/cos/pow) applied ONCE to a simple atom. No nesting of
    transcendentals -> SymPy cannot explode. Single-symbol -> ground truth kept."""
    if rng.random() < 0.5:
        return _gen_in(sym, rng, depth)
    fn = rng.choice(["sin", "cos", "pow2", "pow3"])
    arg = _simple_arg(sym, rng)
    if fn == "sin":
        return sp.sin(arg)
    if fn == "cos":
        return sp.cos(arg)
    if fn == "pow2":
        return arg ** 2
    return arg ** 3'''

# 2) Point gen_holo and gen_anti at _gen_enriched.
OLD_HOLO = "def gen_holo(rng, depth):\n    return _ensure_has(_gen_in, z, rng, depth)"
NEW_HOLO = "def gen_holo(rng, depth):\n    return _ensure_has(_gen_enriched, z, rng, depth)"
OLD_ANTI = "def gen_anti(rng, depth):\n    return _ensure_has(_gen_in, zbar, rng, depth)"
NEW_ANTI = "def gen_anti(rng, depth):\n    return _ensure_has(_gen_enriched, zbar, rng, depth)"

with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

if "_gen_enriched" in src:
    print("ALREADY PATCHED -- nothing to do."); sys.exit(0)

for label, old in [("_gen_in anchor", ANCHOR), ("gen_holo", OLD_HOLO), ("gen_anti", OLD_ANTI)]:
    if old not in src:
        print(f"ERROR: '{label}' block not found. Aborting (no write)."); sys.exit(1)
    if src.count(old) != 1:
        print(f"ERROR: '{label}' found {src.count(old)} times, expected 1. Aborting."); sys.exit(1)

src = src.replace(ANCHOR, INSERT)
src = src.replace(OLD_HOLO, NEW_HOLO)
src = src.replace(OLD_ANTI, NEW_ANTI)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("PATCH APPLIED (bridled enrichment).")
print("  added: _simple_arg, _gen_enriched (sin/cos/pow2/pow3 on simple atoms only)")
print("  gen_holo and gen_anti now use _gen_enriched")
print("  NO timeout, NO nested transcendentals possible.")
print("  next: re-run the bench (should stay fast + 100% pass + transcendentals in random gens).")
