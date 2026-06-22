#!/usr/bin/env python3
"""
cnative_bench.py -- C-native calibration bench for the single-field Wirtinger judge.

Tests judge_v2.certify_1field on complex symbolic functions whose holomorphic
class is known by an INDEPENDENT exact reference (5 classes), then projects onto
the judge's 3 labels and asserts judge == expected. The reference oracle is NOT
the judge: it is the expected value of a unit test. Author: Anthony Monnerot, 2026.
"""
import argparse
import json
import random
from datetime import datetime, timezone

import sympy as sp

from judge_v2 import z, zbar, certify_1field

HOL, ANTI, MIXED, MODULE_TRAPPED, REAL_TRAPPED = (
    "HOL", "ANTI", "MIXED", "MODULE_TRAPPED", "REAL_TRAPPED")

PROJECT = {
    HOL: "holomorphic",
    REAL_TRAPPED: "real-trapped",
    ANTI: "anti-holomorphic",
    MIXED: "anti-holomorphic",
    MODULE_TRAPPED: "module-trapped",
}

MODULE_K_MAX = 3


def _full_conj(expr):
    tmp = sp.Symbol("__ref_tmp_conj__")
    e = expr.subs(sp.I, tmp)
    e = e.subs({z: zbar, zbar: z}, simultaneous=True)
    e = e.subs(tmp, -sp.I)
    return e


def _is_zero(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    try:
        return bool(e.equals(0))
    except Exception:
        return False


def _is_module_rotation(e):
    """Independent module-trap test (rotation generator R = z*d/dz - zbar*d/dzbar).
    For f = holo(z)*M(z*zbar): R(M)=0 (modulus rotation-invariant), so R(f)/f = z*holo'/holo
    depends on z ONLY. Holds for ANY holomorphic factor (monomial or not). This is independent
    of the judge's L = zbar*dlog/dzbar criterion (different operator/direction)."""
    try:
        Rf = sp.simplify(z * sp.diff(e, z) - zbar * sp.diff(e, zbar))
        ratio = sp.simplify(Rf / e)
        return _is_zero(sp.simplify(sp.diff(ratio, zbar)))
    except Exception:
        return False


def ref_classify(expr):
    e = sp.expand(expr)
    dzbar = sp.simplify(sp.diff(e, zbar))
    if _is_zero(dzbar):
        return HOL
    if _is_zero(e - _full_conj(e)):
        return REAL_TRAPPED
    dz = sp.simplify(sp.diff(e, z))
    if _is_zero(dz):
        return ANTI
    if _is_module_rotation(e):
        return MODULE_TRAPPED
    return MIXED


def _const(rng):
    return rng.choice([sp.Integer(2), sp.Integer(-3), sp.Rational(1, 2),
                       sp.I, 1 + sp.I, 1 - sp.I, -sp.I])


def _gen_in(sym, rng, depth):
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
    raise RuntimeError("unreachable")


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
    return arg ** 3


def _ensure_has(expr_fn, sym, rng, depth):
    for _ in range(8):
        e = expr_fn(sym, rng, depth)
        if e.has(sym) and not e.is_number:
            return e
    return sym


def gen_holo(rng, depth):
    return _ensure_has(_gen_enriched, z, rng, depth)


def gen_anti(rng, depth):
    return _ensure_has(_gen_enriched, zbar, rng, depth)


def gen_mixed(rng, depth):
    H = gen_holo(rng, depth)
    A = gen_anti(rng, depth)
    return H + A if rng.random() < 0.5 else H * A


def gen_real_trapped(rng, depth):
    H = gen_holo(rng, depth)
    form = rng.choice(["sum", "abs2", "im", "logabs2"])
    if form == "sum":
        return H + _full_conj(H)
    if form == "abs2":
        return H * _full_conj(H)
    if form == "im":
        return (H - _full_conj(H)) / (2 * sp.I)
    return sp.log(H) + sp.log(_full_conj(H))


def gen_module(rng, depth):
    H = gen_holo(rng, depth)
    k = rng.choice([1, 2])
    return H * (z * zbar) ** k


GENERATORS = {
    HOL: gen_holo,
    ANTI: gen_anti,
    MIXED: gen_mixed,
    REAL_TRAPPED: gen_real_trapped,
    MODULE_TRAPPED: gen_module,
}


def gold_controls():
    y_im = (z - zbar) / (2 * sp.I)
    return [
        ("z", z),
        ("zbar", zbar),
        ("z**2 + (1+I)", z ** 2 + (1 + sp.I)),
        ("exp(z)", sp.exp(z)),
        ("log(z)", sp.log(z)),
        ("1/z", 1 / z),
        ("conj(conj(z)) = z (fake-anti -> HOL)", _full_conj(_full_conj(z))),
        ("(z+zbar)-zbar = z (cancel -> HOL)", (z + zbar) - zbar),
        ("(2*z+zbar)-zbar = 2z (cancel -> HOL)", (2 * z + zbar) - zbar),
        ("exp(zbar)", sp.exp(zbar)),
        ("1/zbar", 1 / zbar),
        ("i*zbar (genuine anti, not real)", sp.I * zbar),
        ("|z|^2 = z*zbar (REAL-TRAP)", z * zbar),
        ("z+zbar (REAL-TRAP)", z + zbar),
        ("Im(z)=(z-zbar)/2i (REAL-TRAP)", y_im),
        ("log|z|^2 (REAL-TRAP)", sp.log(z) + sp.log(zbar)),
        ("z + 0.3*zbar (MIXED)", z + sp.Rational(3, 10) * zbar),
        ("exp(z)+exp(zbar) (REAL-TRAP: it is real!)", sp.exp(z) + sp.exp(zbar)),
        ("exp(z)+I*exp(zbar) (MIXED, not real)", sp.exp(z) + sp.I * sp.exp(zbar)),
        ("Eb2-type: z + 1/Im(z) (additive real anti)", z + 1 / y_im),
        ("z^2 * zbar = z*|z|^2 (MODULE-TRAP)", z ** 2 * zbar),
        ("(z+1)*|z|^2 (MODULE-TRAP)", (z + 1) * z * zbar),
        ("z * zbar^2 = |z|^4 / z (MODULE-TRAP)", z * zbar ** 2),
        # --- transcendental controls (added 2026-06-20, lift the SymPy reservation on the Maass shadow) ---
        ("z*exp(|z|^2) (MODULE-TRAP transc.)", z * sp.exp(z * zbar)),
        ("z^2*besselj(0,|z|^2) (MODULE-TRAP transc.)", z ** 2 * sp.besselj(0, z * zbar)),
        ("z*Gamma(1/2,|z|^2) (MODULE-TRAP transc.)", z * sp.uppergamma(sp.Rational(1, 2), z * zbar)),
        ("z^3*log(|z|^2) (MODULE-TRAP transc.)", z ** 3 * sp.log(z * zbar)),
        ("(1/z)*exp(|z|^2) (MODULE-TRAP transc.)", sp.exp(z * zbar) / z),
        ("z*erf(|z|^2) (MODULE-TRAP transc.)", z * sp.erf(z * zbar)),
        ("exp(|z|^2) (REAL-TRAP transc.)", sp.exp(z * zbar)),
        ("besselj(0,|z|^2) (REAL-TRAP transc.)", sp.besselj(0, z * zbar)),
        ("Gamma(1/2,|z|^2) (REAL-TRAP transc.)", sp.uppergamma(sp.Rational(1, 2), z * zbar)),
        ("exp(zbar) (ANTI transc.)", sp.exp(zbar)),
        ("z+exp(zbar) (MIXED transc.)", z + sp.exp(zbar)),
        ("besselj(0,zbar) (ANTI transc.)", sp.besselj(0, zbar)),
        ("Gamma(1/2,zbar) (ANTI transc.)", sp.uppergamma(sp.Rational(1, 2), zbar)),
        ("exp(z) (HOL transc.)", sp.exp(z)),
        ("besselj(0,z) (HOL transc.)", sp.besselj(0, z)),
    ]


def evaluate(name, expr):
    try:
        truth = ref_classify(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "status": "REF_ERROR",
                "detail": str(e)}
    se = sp.simplify(expr)
    if se.is_number:
        return None
    expected = PROJECT[truth]
    try:
        judge, _ = certify_1field(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "truth": truth,
                "expected": expected, "status": "JUDGE_ERROR", "detail": str(e)}
    ok = (judge == expected)
    severity = "OK"
    if not ok:
        if truth == HOL and judge != "holomorphic":
            severity = "FALSE_ANTI_ON_HOLO"
        elif truth in (ANTI, MIXED, MODULE_TRAPPED) and judge == "holomorphic":
            severity = "FALSE_HOLO_ON_NONHOLO"
        else:
            severity = "MISMATCH"
    return {"name": name, "expr": str(expr), "truth": truth,
            "expected": expected, "judge": judge,
            "status": "OK" if ok else severity}


def run(n_per_class, seed, depth, do_random):
    rng = random.Random(seed)
    results = []
    for name, expr in gold_controls():
        r = evaluate(name, expr)
        if r is not None:
            r["source"] = "gold"
            results.append(r)
    if do_random:
        for truth_intent, gen in GENERATORS.items():
            made = 0
            attempts = 0
            while made < n_per_class and attempts < n_per_class * 20:
                attempts += 1
                try:
                    expr = gen(rng, depth)
                except Exception:
                    continue
                r = evaluate(f"rand[{truth_intent}]#{made}", expr)
                if r is None:
                    continue
                r["source"] = "random"
                r["intent"] = truth_intent
                results.append(r)
                made += 1
    return results


def summarize(results):
    judge_labels = ["holomorphic", "anti-holomorphic", "module-trapped", "real-trapped"]
    truth_labels = [HOL, ANTI, MIXED, MODULE_TRAPPED, REAL_TRAPPED]
    total = len(results)
    errors = [r for r in results if r["status"] in ("REF_ERROR", "JUDGE_ERROR")]
    scored = [r for r in results if r["status"] not in ("REF_ERROR", "JUDGE_ERROR")]
    fails = [r for r in scored if r["status"] != "OK"]
    passed = len(scored) - len(fails)
    print("=" * 78)
    print("C-NATIVE CALIBRATION BENCH  (judge tested against independent reference)")
    print("=" * 78)
    print(f"generated/scored : {total} / {len(scored)}    errors: {len(errors)}")
    print(f"PASS             : {passed}/{len(scored)}    FAIL: {len(fails)}")
    print()
    print("Cross-tab  ground-truth (rows)  x  judge label (cols)")
    print("-" * 78)
    hdr = "{:<16}".format("truth\\judge")
    for jl in judge_labels:
        hdr += "{:>16}".format(jl)
    print(hdr)
    counts = {t: {j: 0 for j in judge_labels} for t in truth_labels}
    for r in scored:
        if r["truth"] in counts and r.get("judge") in counts[r["truth"]]:
            counts[r["truth"]][r["judge"]] += 1
    for t in truth_labels:
        row = "{:<16}".format(t)
        for jl in judge_labels:
            row += "{:>16}".format(counts[t][jl])
        print(row)
    print("-" * 78)
    print("Reading: MODULE_TRAPPED lands under 'module-trapped'; MIXED lands under 'anti-holomorphic' by")
    print("design (single-field judge has MODULE_TRAPPED but no separate MIXED label). REAL_TRAPPED must")
    print("sit only under 'real-trapped'; HOL only under 'holomorphic'.")
    print()
    if fails:
        print("FAILURES (judge != expected):")
        print("-" * 78)
        for r in fails:
            print(f"  [{r['status']}] {r['name']}")
            print(f"      expr     : {r['expr']}")
            print(f"      truth    : {r.get('truth')}  -> expected {r.get('expected')}")
            print(f"      judge    : {r.get('judge')}")
    else:
        print("No failures: judge == expected on every scored case.")
    if errors:
        print()
        print("ERRORS (expression skipped by ref or judge):")
        for r in errors:
            print(f"  [{r['status']}] {r['name']}: {r.get('detail','')[:80]}")
    return {"total": total, "scored": len(scored), "passed": passed,
            "failed": len(fails), "errors": len(errors), "crosstab": counts}


def main():
    ap = argparse.ArgumentParser(description="C-native Wirtinger judge bench.")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--no-random", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    results = run(args.n, args.seed, args.depth, not args.no_random)
    summary = summarize(results)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.out or f"cnative_bench_report_{stamp}.json"
    with open(out, "w") as f:
        json.dump({"generated_utc": stamp, "seed": args.seed,
                   "n_per_class": args.n, "depth": args.depth,
                   "summary": summary, "results": results},
                  f, indent=2, default=str)
    print()
    print(f"Full report written to {out}")
    critical = any(r["status"] in ("FALSE_ANTI_ON_HOLO", "FALSE_HOLO_ON_NONHOLO")
                   for r in results)
    raise SystemExit(2 if critical else 0)


if __name__ == "__main__":
    main()
