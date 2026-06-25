#!/usr/bin/env python3
"""
pysr_holo_calib.py -- HOLO calibration of the DISCOVERER (PySR), oxieml-star.

PURPOSE (prerequisite set by FINDINGS_20260624_symmetry_harness):
  the tool must be IRREPROACHABLE on the holomorphic side before any claim on the
  anti side -- it must NEVER introduce a spurious zbar on holomorphic data.

WHY Re AND Im (key audit point):
  PySR works on REAL features (x, y) and fits a real surface. Re alone does NOT
  distinguish holo from anti:  Re(z^2) = x^2 - y^2 = Re(zbar^2)  (identical!).
  Im is what separates them:    Im(z^2) = +2xy  vs  Im(zbar^2) = -2xy.
  So we run PySR on BOTH Re(f) and Im(f), reconstruct f_hat = g_re + i*g_im,
  express it in (z, zbar), and let the judge decide. A reconstruction that
  violates Cauchy-Riemann would inject a spurious zbar -> judge would flag anti.

TEST (irreproachable on holo):
  known holo f -> 2 PySR runs (Re, Im) -> reconstruct -> express in (z,zbar)
  -> certify_1field MUST return 'holomorphic'  AND  MSE < 1e-3 on both runs.

CASES:
  poly : f = z^2 + z      Re = x^2 - y^2 + x,  Im = 2xy + y     (polynomial bricks)
  exp  : f = exp(z)       Re = exp(x)cos(y),   Im = exp(x)sin(y)
         -> cos, sin ADDED to unary operators (else PySR cannot represent it).

MARKER != VERDICT. Result invalid until run on the M920q and judged. [DERIVATION].

Run detached (real PySR fit, ~30 min target per case):
  JULIA_NUM_GC_THREADS=1 setsid nohup python3 -u pysr_holo_calib.py --case poly > pysr_holo_calib_poly.log 2>&1 &
  JULIA_NUM_GC_THREADS=1 setsid nohup python3 -u pysr_holo_calib.py --case exp  > pysr_holo_calib_exp.log  2>&1 &

Validate the pipeline WITHOUT PySR first:
  python3 pysr_holo_calib.py --selftest
"""
import argparse
import json
import sympy as sp
from judge_v2 import z, zbar, certify_1field

# real coordinate symbols used by the reconstruction (match PySR variable_names)
x, y = sp.symbols("x y", real=True)

# ---- reference Re/Im of each known holomorphic case (oracle, NOT the judge) ----
REF = {
    "poly": dict(
        f_true=z**2 + z,
        g_re=x**2 - y**2 + x,
        g_im=2*x*y + y,
        r_lo=0.3, r_hi=2.0,
        unary=["exp", "square", "sqrt_abs(x) = sqrt(abs(x))"],
    ),
    "exp": dict(
        f_true=sp.exp(z),
        g_re=sp.exp(x)*sp.cos(y),
        g_im=sp.exp(x)*sp.sin(y),
        r_lo=0.3, r_hi=1.5,                       # keep exp(x) modest, no overflow
        unary=["exp", "square", "sqrt_abs(x) = sqrt(abs(x))", "cos", "sin"],
    ),
}


def reconstruct_and_judge(g_re_expr, g_im_expr):
    """f_hat = g_re + i g_im  ->  (z, zbar)  ->  judge.  Returns (f_zzbar, label, dfdzbar)."""
    f_hat = g_re_expr + sp.I * g_im_expr
    f_hat = f_hat.rewrite(sp.exp)                 # turn cos/sin into complex exp first
    subs_map = {}
    for s in f_hat.free_symbols:
        if s.name == "x":
            subs_map[s] = (z + zbar) / 2
        elif s.name == "y":
            subs_map[s] = (z - zbar) / (2 * sp.I)
    f_zzbar = sp.simplify(sp.expand(f_hat.subs(subs_map)))
    label, dfdzbar = certify_1field(f_zzbar)
    return f_zzbar, label, dfdzbar


def selftest():
    """Validate generation + reconstruction + judge on the REFERENCE formulas,
    independently of PySR. Each known holo case must reconstruct to f_true and
    judge 'holomorphic'."""
    print("=" * 74)
    print("SELFTEST -- pipeline (reconstruct + judge) on reference formulas, no PySR")
    print("=" * 74)
    ok_all = True
    for case, d in REF.items():
        f_zzbar, label, dfdzbar = reconstruct_and_judge(d["g_re"], d["g_im"])
        matches = sp.simplify(f_zzbar - d["f_true"]) == 0
        is_holo = (label == "holomorphic")
        ok = matches and is_holo
        ok_all = ok_all and ok
        print(f"\n[{case}]  f_true = {d['f_true']}")
        print(f"   reconstructed f_hat(z,zbar) = {f_zzbar}")
        print(f"   matches f_true : {matches}")
        print(f"   judge label    : {label}   (dfdzbar = {dfdzbar})")
        print(f"   => {'OK' if ok else 'FAIL'}")
    print("\n" + "=" * 74)
    print(f"SELFTEST: {'PASS' if ok_all else 'FAIL'}")
    print("Reconstruction is Cauchy-Riemann-clean: holo Re/Im rebuild a holo f,")
    print("the judge sees no spurious zbar. Pipeline ready for the PySR runs.")
    print("=" * 74)
    return ok_all


def select_equation_idx(eqs, tol=1e-8):
    """Pick the SIMPLEST equation whose loss is essentially perfect (< tol), so the
    discoverer returns the canonical clean formula -- not an over-decorated Pareto
    neighbour with a negligibly smaller loss. Fallback: PySR score (best loss-per-
    complexity tradeoff), then raw min loss (e.g. noisy/shuffle cases)."""
    good = eqs[eqs["loss"] < tol]
    if len(good) > 0:
        return good["complexity"].idxmin()
    if "score" in eqs.columns:
        return eqs["score"].idxmax()
    return eqs["loss"].idxmin()


def run_pysr(case):
    """Real calibration: generate data for the known holo case, run PySR on Re and
    Im, reconstruct, judge. Needs numpy + pysr (run on the M920q, detached)."""
    import numpy as np
    from pysr import PySRRegressor

    d = REF[case]
    rng = np.random.default_rng(42)
    N = 2000
    r = rng.uniform(d["r_lo"], d["r_hi"], N)
    theta = rng.uniform(-np.pi, np.pi, N)
    zz = r * np.exp(1j * theta)
    xx, yy = zz.real, zz.imag
    if case == "poly":
        fv = zz**2 + zz
    elif case == "exp":
        fv = np.exp(zz)
    else:
        raise ValueError(case)
    X = np.column_stack([xx, yy])
    tgt_re, tgt_im = fv.real, fv.imag
    print(f"[data] case={case} N={N} Re range[{tgt_re.min():.3f},{tgt_re.max():.3f}] "
          f"Im range[{tgt_im.min():.3f},{tgt_im.max():.3f}]")

    def fit(target, tag):
        model = PySRRegressor(
            niterations=60,
            populations=15,
            population_size=33,
            maxsize=30,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=d["unary"],
            extra_sympy_mappings={"sqrt_abs": lambda a: sp.sqrt(sp.Abs(a))},
            elementwise_loss="loss(prediction, target) = (prediction - target)^2",
            variable_names=["x", "y"],
            deterministic=False,
            parallelism="multithreading",
            random_state=0,
            verbosity=1,
        )
        print(f"[pysr] fitting {tag} ...")
        model.fit(X, target)
        eqs = model.equations_
        idx = select_equation_idx(eqs)
        best = eqs.loc[idx]
        print(f"[pysr] {tag} loss={best['loss']:.3e}  complexity={best['complexity']}  eq={best['equation']}")
        return model.sympy(index=idx), float(best["loss"])

    g_re, mse_re = fit(tgt_re, "Re(f)")
    g_im, mse_im = fit(tgt_im, "Im(f)")

    f_zzbar, label, dfdzbar = reconstruct_and_judge(sp.sympify(g_re), sp.sympify(g_im))
    holo_ok = (label == "holomorphic")
    mse_ok = (mse_re < 1e-3) and (mse_im < 1e-3)
    irreproachable = holo_ok and mse_ok

    print("\n" + "=" * 74)
    print(f"CASE {case}: reconstructed f_hat(z,zbar) = {f_zzbar}")
    print(f"  judge label : {label}   (dfdzbar = {dfdzbar})")
    print(f"  MSE Re={mse_re:.3e}  Im={mse_im:.3e}  (both < 1e-3 ? {mse_ok})")
    print(f"  IRREPROACHABLE ON HOLO (holomorphic AND MSE<1e-3): {irreproachable}")
    print("=" * 74)
    out = {
        "case": case, "judge_label": label, "f_hat": str(f_zzbar),
        "mse_re": mse_re, "mse_im": mse_im, "mse_below_1e-3": bool(mse_ok),
        "holomorphic": bool(holo_ok), "irreproachable": bool(irreproachable),
        "note": "MARKER != VERDICT. Re alone is holo/anti-ambiguous; Re+Im reconstruct + judge.",
    }
    json.dump(out, open(f"pysr_holo_calib_{case}_result.json", "w"), indent=2)
    print(f"[saved] pysr_holo_calib_{case}_result.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=["poly", "exp"], default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest or args.case is None:
        selftest()
    else:
        run_pysr(args.case)
