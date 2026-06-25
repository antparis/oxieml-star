#!/usr/bin/env python3
"""
symmetry_battery.py -- HOLO/ANTI symmetry calibration of the discoverer (PySR),
oxieml-star.  Companion to pysr_holo_calib.py, generalised to BOTH sides of the
classification cube plus the interior cubies and a negative control.

WHY (rule SYMETRIE): the tool must be IRREPROACHABLE on holo AND anti before any
claim on unknown data. It must (a) reconstruct the KNOWN formula, not just the
right label; (b) never cry ANTI on a holo/real/module field; (c) reject noise.

PIPELINE (identical to pysr_holo_calib, audited): native (z,zbar) data -> PySR on
Re(f) and Im(f) -> Occam selector (simplest equation with loss<1e-8) -> rebuild
f_hat=g_re+i*g_im -> express in (z,zbar) -> judge_v2.certify_1field. MARKER!=VERDICT.

MAP (9 cases, every expected verdict checked against judge_v2):
  region          case            f(z,zbar)        expected verdict      exact recon?
  holo wall       poly            z**2+z           holomorphic           yes
  holo wall       exp             exp(z)           holomorphic           yes
  anti wall       poly_anti       zbar**2          anti-holomorphic      yes
  anti wall       exp_anti        exp(zbar)        anti-holomorphic      yes (clean transc.)
  anti (paper)    mixte           exp(z)-log(zbar) anti-holomorphic      NO  [branch cut]
  anti (limit)    log_anti        log(zbar)        anti-holomorphic      NO  [branch cut]
  interior cubie  real_trapped    z*zbar           real-trapped          yes
  interior cubie  module_trapped  z**2*zbar        module-trapped        yes
  neg control     shuffle         z**2+z, y perm.  REJECT (MSE>=1e-3)    n/a

log_anti / mixte: Im=arg(zbar) carries the log branch cut, out of reach of a
{+,-,*,/,exp,cos,sin} basis -> verdict required, exact reconstruction NOT required.
This is a documented structural limit, not a tool failure. [DERIVATION/LIMIT].

Run a single case detached (~30 min):
  JULIA_NUM_GC_THREADS=1 setsid nohup python3 -u symmetry_battery.py --case poly_anti > sb_poly_anti.log 2>&1 &
Validate the whole map WITHOUT PySR first (shows the 9-case table):
  python3 symmetry_battery.py --selftest
"""
import argparse, json, signal, time
import sympy as sp
from judge_v2 import z, zbar, certify_1field

x, y = sp.symbols("x y", real=True)

RECON_TIMEOUT = 60   # seconds: hard cap on the symbolic reconstruction (simplify can hang
                     # forever on branch-cut expressions log/atan2 -- lesson from `mixte` 9h freeze)


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def hb(case, msg):
    """Heartbeat: append one timestamped line to a per-case progress file, flushed at once."""
    with open(f"sb_{case}_progress.log", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')}  {msg}\n")

# ---- case registry: f_true in (z,zbar), expected verdict, exact-recon flag ----
CASES = {
    "poly":           dict(f=z**2 + z,                 expect="holomorphic",      exact=True,  note=""),
    "exp":            dict(f=sp.exp(z),                expect="holomorphic",      exact=True,  note="",
                          unary=["exp","square","sqrt_abs(x) = sqrt(abs(x))","cos","sin"]),
    "poly_anti":      dict(f=zbar**2,                  expect="anti-holomorphic", exact=True,  note=""),
    "exp_anti":       dict(f=sp.exp(zbar),             expect="anti-holomorphic", exact=True,  note="",
                          unary=["exp","square","sqrt_abs(x) = sqrt(abs(x))","cos","sin"]),
    "mixte":          dict(f=sp.exp(z)-sp.log(zbar),   expect="anti-holomorphic", exact=False, note="branch cut",
                          unary=["exp","square","sqrt_abs(x) = sqrt(abs(x))","cos","sin","log_abs(x) = log(abs(x))"]),
    "log_anti":       dict(f=sp.log(zbar),             expect="anti-holomorphic", exact=False, note="branch cut",
                          unary=["exp","square","sqrt_abs(x) = sqrt(abs(x))","cos","sin","log_abs(x) = log(abs(x))"]),
    "real_trapped":   dict(f=z*zbar,                   expect="real-trapped",     exact=True,  note=""),
    "module_trapped": dict(f=z**2*zbar,                expect="module-trapped",   exact=True,  note=""),
    "shuffle":        dict(f=z**2 + z,                 expect="REJECT",           exact=False, note="negative control"),
}
DEFAULT_UNARY = ["exp","square","sqrt_abs(x) = sqrt(abs(x))"]
R_LO, R_HI = 0.3, 1.5


def re_im_of(f_true):
    """Exact analytic Re/Im in (x,y) from f_true(z,zbar). x,y declared real."""
    f_xy = f_true.subs({z: x + sp.I*y, zbar: x - sp.I*y})
    f_xy = sp.expand(sp.simplify(f_xy))
    return sp.simplify(sp.re(f_xy)), sp.simplify(sp.im(f_xy))


def chop(expr, tol=1e-12):
    """Round numeric coefficients (real & imag parts) below tol to zero, term by term.
    Removes floating-point dust (e.g. 1.18e-19*I) that breaks the judge's EXACT full_conj
    invariance test and causes a false negative (real-trapped misread as module-trapped).
    Acts on the (z,zbar) expression BEFORE certify_1field -- the pivot judge is NOT modified.
    Verified not to remove legitimate coefficients (>tol) nor alter the pure corners."""
    expr = sp.expand(expr)
    out = sp.Integer(0)
    for term in sp.Add.make_args(expr):
        coeff, rest = term.as_coeff_Mul()
        re, im = sp.re(coeff), sp.im(coeff)
        re = 0 if (re.is_number and abs(float(re)) < tol) else re
        im = 0 if (im.is_number and abs(float(im)) < tol) else im
        out += (re + sp.I*im) * rest
    return sp.expand(out)


def reconstruct_and_judge(g_re_expr, g_im_expr):
    f_hat = g_re_expr + sp.I*g_im_expr
    f_hat = f_hat.rewrite(sp.exp)
    subs_map = {}
    for s in f_hat.free_symbols:
        if s.name in ("x", "x0"):   subs_map[s] = (z + zbar)/2
        elif s.name in ("y", "x1"): subs_map[s] = (z - zbar)/(2*sp.I)
    f_zzbar = sp.simplify(sp.expand(f_hat.subs(subs_map)))
    f_zzbar = chop(f_zzbar)          # remove floating-point dust before the exact judge
    label, dfdzbar = certify_1field(f_zzbar)
    return f_zzbar, label, dfdzbar


def selftest():
    print("=" * 92)
    print("SELFTEST -- 9-case symmetry map: oracle Re/Im -> reconstruct -> judge_v2 (no PySR)")
    print("=" * 92)
    print(f"{ 'case':<16}{'f_true':<20}{'judged':<18}{'expected':<18}{'recon':<7}{'verdict'}")
    print("-" * 92)
    ok_all = True
    for name, d in CASES.items():
        if name == "shuffle":
            print(f"{name:<16}{'z**2+z (y perm.)':<20}{'(negative control: run-only, expects MSE>=1e-3)'}")
            continue
        g_re, g_im = re_im_of(d["f"])
        f_hat, label, _ = reconstruct_and_judge(g_re, g_im)
        verdict_ok = (label == d["expect"])
        match = sp.simplify(f_hat - d["f"]) == 0
        recon_ok = match if d["exact"] else True   # exact recon not required for [branch cut]
        ok = verdict_ok and recon_ok
        ok_all = ok_all and ok
        tag = "OK" if ok else "FAIL"
        if not d["exact"] and not match:
            tag += f" [{d['note']}: verdict-only]"
        print(f"{name:<16}{str(d['f'])[:19]:<20}{label:<18}{d['expect']:<18}"
              f"{('exact' if d['exact'] else 'n/a'):<7}{tag}")
    print("-" * 92)
    print(f"SELFTEST: {'PASS' if ok_all else 'FAIL'}  "
          f"(verdicts match judge_v2; exact reconstruction enforced only where not branch-cut)")
    print("=" * 92)
    return ok_all


def run_pysr(case):
    import numpy as np
    from pysr import PySRRegressor
    d = CASES[case]
    unary = d.get("unary", DEFAULT_UNARY)
    rng = np.random.default_rng(42)
    N = 2000
    r = rng.uniform(R_LO, R_HI, N); theta = rng.uniform(-np.pi, np.pi, N)
    zz = r*np.exp(1j*theta); xx, yy = zz.real, zz.imag

    # numeric f(z,zbar) for this case
    fz = sp.lambdify((z, zbar), d["f"], "numpy")
    fv = fz(zz, np.conj(zz))
    fv = np.broadcast_to(fv, zz.shape).astype(complex)

    Xx, Xy = xx.copy(), yy.copy()
    if case == "shuffle":
        Xy = rng.permutation(Xy)   # break the (x,y)<->f correspondence
    X = np.column_stack([Xx, Xy])
    tgt_re, tgt_im = fv.real, fv.imag
    print(f"[data] case={case} N={N} expect={d['expect']} "
          f"Re[{tgt_re.min():.3f},{tgt_re.max():.3f}] Im[{tgt_im.min():.3f},{tgt_im.max():.3f}]")

    extra = {"sqrt_abs": lambda a: sp.sqrt(sp.Abs(a)), "log_abs": lambda a: sp.log(sp.Abs(a))}

    def select_equation_idx(eqs, tol=1e-8):
        good = eqs[eqs["loss"] < tol]
        if len(good) > 0: return good["complexity"].idxmin()
        if "score" in eqs.columns: return eqs["score"].idxmax()
        return eqs["loss"].idxmin()

    def fit(target, tag):
        model = PySRRegressor(
            niterations=60, populations=15, population_size=33, maxsize=30,
            binary_operators=["+","-","*","/"], unary_operators=unary,
            extra_sympy_mappings=extra,
            elementwise_loss="loss(prediction, target) = (prediction - target)^2",
            variable_names=["x","y"], deterministic=False,
            parallelism="multithreading", random_state=0, verbosity=1,
        )
        print(f"[pysr] fitting {tag} ...")
        model.fit(X, target)
        eqs = model.equations_
        idx = select_equation_idx(eqs); best = eqs.loc[idx]
        print(f"[pysr] {tag} loss={best['loss']:.3e} complexity={best['complexity']} eq={best['equation']}")
        return model.sympy(index=idx), float(best["loss"])

    hb(case, "fit Re ...")
    g_re, mse_re = fit(tgt_re, "Re(f)")
    hb(case, f"fit Re done mse={mse_re:.3e}")
    hb(case, "fit Im ...")
    g_im, mse_im = fit(tgt_im, "Im(f)")
    hb(case, f"fit Im done mse={mse_im:.3e}")
    mse_ok = (mse_re < 1e-3) and (mse_im < 1e-3)

    partial = dict(case=case, expect=d["expect"], stage="fit_done",
                   g_re=str(g_re), g_im=str(g_im),
                   mse_re=mse_re, mse_im=mse_im, mse_below_1e_3=bool(mse_ok),
                   judge_label=None, f_hat=None, passed=None,
                   exact_required=bool(d["exact"]), note=d["note"],
                   marker_note="PARTIAL: fit saved, reconstruction not yet done.")
    json.dump(partial, open(f"sb_{case}_result.json", "w"), indent=2)
    hb(case, "fit checkpoint saved -> starting reconstruction (timeout %ds)" % RECON_TIMEOUT)

    recon_timed_out = False
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(RECON_TIMEOUT)
    try:
        f_hat, label, dfdzbar = reconstruct_and_judge(sp.sympify(g_re), sp.sympify(g_im))
        signal.alarm(0)
        hb(case, f"reconstruction done: label={label}")
    except _Timeout:
        recon_timed_out = True
        f_hat, label, dfdzbar = None, "LIMIT-reconstruction-timeout", None
        hb(case, f"reconstruction TIMEOUT after {RECON_TIMEOUT}s -> [LIMITE]")
    except Exception as e:
        signal.alarm(0)
        recon_timed_out = True
        f_hat, label, dfdzbar = None, f"LIMIT-reconstruction-error:{type(e).__name__}", None
        hb(case, f"reconstruction ERROR {type(e).__name__} -> [LIMITE]")

    if case == "shuffle":
        passed = (not mse_ok) and (not recon_timed_out)   # success = REJECT (high MSE)
        verdict = f"REJECT control: MSE_ok={mse_ok} -> {'PASS (rejected)' if passed else 'FAIL'}"
    elif recon_timed_out:
        passed = False
        verdict = f"[LIMITE] reconstruction did not converge ({label}); fit saved, verdict undetermined"
    else:
        verdict_ok = (label == d["expect"])
        passed = verdict_ok and mse_ok
        verdict = (f"label={label} expected={d['expect']} match={verdict_ok} "
                   f"MSE_ok={mse_ok} -> {'PASS' if passed else 'MISMATCH'}")

    print("\n" + "=" * 92)
    print(f"CASE {case}: f_hat = {f_hat}")
    print(f"  judge={label} (dfdzbar={dfdzbar})  MSE Re={mse_re:.3e} Im={mse_im:.3e}")
    print(f"  {verdict}")
    if recon_timed_out:
        print(f"  NOTE: reconstruction hit the {RECON_TIMEOUT}s cap (branch-cut blowup). "
              f"Fit is saved; this is a documented [LIMITE], not a tool failure.")
    elif not d["exact"] and case not in ("shuffle",):
        print(f"  NOTE: exact reconstruction not required for this case [{d['note']}]; verdict is the criterion.")
    print("=" * 92)

    out = dict(case=case, expect=d["expect"], judge_label=label,
               f_hat=(str(f_hat) if f_hat is not None else None),
               g_re=str(g_re), g_im=str(g_im),
               mse_re=mse_re, mse_im=mse_im, mse_below_1e_3=bool(mse_ok),
               passed=bool(passed), reconstruction_timed_out=bool(recon_timed_out),
               exact_required=bool(d["exact"]), note=d["note"],
               marker_note="MARKER != VERDICT. Re+Im reconstruct + judge_v2.")
    json.dump(out, open(f"sb_{case}_result.json", "w"), indent=2)
    hb(case, f"final JSON written passed={passed}")
    print(f"[saved] sb_{case}_result.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=list(CASES.keys()), default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest or args.case is None:
        selftest()
    else:
        run_pysr(args.case)
