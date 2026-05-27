#!/usr/bin/env python3
"""
spacetime_trap.py -- The "pure data" demonstration for the eml / eml-star detector.

THESIS (what we want to show scientists):
  The holomorphic/anti-holomorphic verdict (Wirtinger d/d(zbar)) is RELIABLE ONLY on
  data that is NATIVELY COMPLEX and carries NO REAL TIME/FREQUENCY AXIS. As soon as a
  field measured in space-time is encoded as z = x + i*t, the d/d(zbar) test fabricates
  a FALSE anti-holomorphic verdict -- even for a massless field that has no anti content
  at all. This is the SPARC lesson, made exact and falsifiable.

STRUCTURE
  PART 1 (PROOF, pure SymPy, runs in ~1s, no Julia):
     Exact d/d(zbar) and the correct light-cone observable d/dv for four cases.
       (1) holo   native   : f = z^2            -> d/d(zbar) = 0          (true holo)
       (2) anti   native   : f = conj(z)^2      -> d/d(zbar) = 2*zbar     (true anti, "pure" datum)
       (3) trap   massless : f = cos(x - t), z=x+i*t -> d/d(zbar) != 0    (FALSE anti)
                              but light-cone d/dv = 0                      (no mass: artefact)
       (4) control massive : f = cos(k*x - w*t), w=sqrt(k^2+m^2), z=x+i*t
                              d/d(zbar) != 0  AND  d/dv != 0               (real structure)
     Punchline: on space-time data, d/d(zbar) cannot tell (3) from (4) -- both != 0.
     Only the light-cone d/dv separates them. So an "anti" verdict on time-encoded data
     is meaningless. Cases (1)(2), natively complex with no time axis, are the only ones
     whose d/d(zbar) verdict is trustworthy.

  PART 2 (DATA): write 3 CSVs (z_re,z_im,w_re,w_im) for the holo / anti / trap cases.

  PART 3 (ILLUSTRATION, PySR -> needs Julia, runs on Anthony's machine):
     A NAIVE detector (full standard toolbox, MIXTE eml-star) is run on the 3 datasets.
     Expectation to verify on machine: holo->holo, anti->anti, trap->"anti" with MSE<1e-3.
     => the pipeline's own gate (MSE<1e-3 AND judge d/d(zbar)!=0) CERTIFIES the trap as
     "anti", although Part 1 proves it is a massless field with zero physical anti content.
     This shows MSE + judge are NOT sufficient without a native-complex / no-time guarantee.

  PART 4 (REPORT): summary table + the exact verify_exact.py commands to certify the
     PySR formulas with the OFFICIAL judge (the only authority; Part 1 is exact math,
     Part 3 PySR markers are indicative).

ARBITER: the official judge is verify_exact.py (d/d(zbar)). Part 1 here is exact SymPy
on KNOWN closed forms (same operation the judge performs), so it is authoritative as math.
Part 3's PySR output must be passed to verify_exact.py on the machine; its MSE is only
valid when executed on Anthony's machine.

Author: Anthony Monnerot, 2026. English only.
"""

import sys
import json
import numpy as np
import sympy as sp

OUT_JSON = "spacetime_trap_result.json"
CSV_HOLO = "spacetime_holo.csv"
CSV_ANTI = "spacetime_anti.csv"
CSV_TRAP = "spacetime_trap.csv"

# ---------------------------------------------------------------------------
# PART 1 -- exact symbolic proof
# ---------------------------------------------------------------------------
def part1_symbolic():
    print("=" * 74)
    print("PART 1 -- EXACT SYMBOLIC PROOF (SymPy, no Julia)")
    print("=" * 74)

    rows = []  # (label, encoding, dzbar, verdict_naive, dv, verdict_phys, artefact)

    # --- native-complex frame: z and zbar are INDEPENDENT symbols ---
    z, zbar = sp.symbols("z zbar")

    # (1) holo native: f = z^2
    f1 = z**2
    d1 = sp.simplify(sp.diff(f1, zbar))
    rows.append(("(1) holo native   f=z^2",
                 "native complex (no time)",
                 d1, "HOLOMORPHIC" if d1 == 0 else "non-holo",
                 None, "holomorphic (true)", "no"))

    # (2) anti native: f = conj(z)^2 = zbar^2
    f2 = zbar**2
    d2 = sp.simplify(sp.diff(f2, zbar))
    rows.append(("(2) anti native   f=conj(z)^2",
                 "native complex (no time)",
                 d2, "HOLOMORPHIC" if d2 == 0 else "ANTI/non-holo",
                 None, "anti-holomorphic (true)", "no"))

    # --- space-time frame: real x, t ; z = x + i*t (the trap) ---
    x, t = sp.symbols("x t", real=True)
    I = sp.I

    def dzbar_xt(g):
        # z = x + i t  =>  d/dzbar = (d/dx + i d/dt)/2
        return sp.simplify((sp.diff(g, x) + I * sp.diff(g, t)) / 2)

    def dv_xt(g):
        # light-cone observable: d_x + d_t = 2 d_v  (verified in wick_diag.py)
        # d/dv = (d/dx + d/dt)/2 ; annihilates every right-mover f(x - t)
        return sp.simplify((sp.diff(g, x) + sp.diff(g, t)) / 2)

    # (3) massless field cos(x - t)
    g3 = sp.cos(x - t)
    d3_zbar = dzbar_xt(g3)
    d3_v = dv_xt(g3)
    rows.append(("(3) trap massless f=cos(x-t)",
                 "space-time  z=x+i*t",
                 d3_zbar, "ANTI (naive)" if d3_zbar != 0 else "holo",
                 d3_v, "NO mass (d/dv=0)" if d3_v == 0 else "structure",
                 "YES (false anti)"))

    # (4) massive field cos(k x - w t), w = sqrt(k^2 + m^2)
    k, m = sp.symbols("k m", positive=True)
    w = sp.sqrt(k**2 + m**2)
    g4 = sp.cos(k * x - w * t)
    d4_zbar = sp.simplify(dzbar_xt(g4))
    d4_v = sp.simplify(dv_xt(g4))
    rows.append(("(4) control massive cos(kx-wt)",
                 "space-time  z=x+i*t",
                 d4_zbar, "ANTI (naive)" if d4_zbar != 0 else "holo",
                 d4_v, "HAS structure (d/dv!=0)" if d4_v != 0 else "none",
                 "n/a (genuine, but naive can't tell from (3))"))

    # print
    for (label, enc, dzb, vn, dv, vp, art) in rows:
        print()
        print(f"{label}")
        print(f"    encoding        : {enc}")
        print(f"    d/d(zbar)       : {dzb}")
        print(f"    naive verdict   : {vn}")
        if dv is not None:
            print(f"    light-cone d/dv : {dv}")
            print(f"    physical verdict: {vp}")
        else:
            print(f"    physical verdict: {vp}")
        print(f"    artefact?       : {art}")

    print()
    print("-" * 74)
    print("CONCLUSION (exact):")
    print("  * Cases (3) and (4) BOTH give d/d(zbar) != 0 -> the naive test labels BOTH")
    print("    'anti', yet (3) is massless (no anti content) and (4) is genuinely")
    print("    structured. d/d(zbar) on time-encoded data CANNOT separate them.")
    print("  * The light-cone d/dv = 0 exactly for the massless field (3) and != 0 for")
    print("    the massive one (4): the correct observable, not d/d(zbar).")
    print("  * Only the NATIVELY-COMPLEX, time-free data (1)(2) have a trustworthy")
    print("    d/d(zbar) verdict. => anti-holomorphic claims require pure (no-time) data.")
    print("-" * 74)

    # machine-readable
    return {
        "holo_native_dzbar": str(rows[0][2]),
        "anti_native_dzbar": str(rows[1][2]),
        "trap_massless_dzbar": str(rows[2][2]),
        "trap_massless_dv": str(rows[2][4]),
        "massive_dzbar": str(rows[3][2]),
        "massive_dv": str(rows[3][4]),
    }


# ---------------------------------------------------------------------------
# PART 2 -- data generation
# ---------------------------------------------------------------------------
def sample_annulus(n, r_in, r_out, seed):
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        zz = rng.uniform(-r_out, r_out) + 1j * rng.uniform(-r_out, r_out)
        if r_in < abs(zz) < r_out:
            pts.append(zz)
    return np.array(pts[:n])

def export(fname, z, w):
    arr = np.column_stack([z.real, z.imag, w.real, w.imag])
    np.savetxt(fname, arr, delimiter=",", header="z_re,z_im,w_re,w_im", comments="")
    print(f"    wrote {fname}  ({len(z)} rows)")

def part2_data(n=1500, seed=42):
    print()
    print("=" * 74)
    print("PART 2 -- DATA GENERATION (native holo, native anti, space-time trap)")
    print("=" * 74)

    # native complex, no time axis
    z = sample_annulus(n, 0.3, 2.0, seed)
    export(CSV_HOLO, z, z**2)                 # holo target
    export(CSV_ANTI, z, np.conj(z)**2)        # anti target (the "pure" datum we want)

    # space-time trap: z = x + i t, field cos(x - t)
    rng = np.random.default_rng(seed + 1)
    x = rng.uniform(-2.0, 2.0, n)
    tt = rng.uniform(-2.0, 2.0, n)
    z_st = x + 1j * tt
    w_st = np.cos(x - tt) + 0j
    export(CSV_TRAP, z_st, w_st)              # massless field, time-encoded -> false anti

    # quick self-check: confirm anti = conj of a holo map, trap input is genuinely complex
    corr = np.corrcoef(z_st.real, z_st.imag)[0, 1]
    print(f"    trap input corr(Re,Im) = {corr:+.3f}  (near 0 = genuinely 2D, time on Im axis)")


# ---------------------------------------------------------------------------
# PART 3 -- PySR illustration (needs Julia; runs on Anthony's machine)
# ---------------------------------------------------------------------------
def build_naive_toolbox():
    """Standard MIXTE toolbox of pysr_stacking.py -- the 'naive researcher' setup."""
    binary_operators = [
        "+", "-", "*", "/",
        "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))",
        "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))",
    ]
    unary_operators = [
        "sin", "cos", "exp", "log",
        "my_conj(z) = conj(z)",
        "my_real(z) = complex(real(z))",
        "my_imag(z) = complex(imag(z))",
        "my_abs2(z) = z * conj(z)",
    ]
    extra_sympy = {
        "eml": lambda a, b: sp.exp(a) - sp.log(b),
        "emlstar": lambda a, b: sp.exp(a) - sp.log(sp.conjugate(b)),  # MIXTE
        "my_conj": lambda u: sp.conjugate(u),
        "my_real": lambda u: sp.re(u),
        "my_imag": lambda u: sp.im(u),
        "my_abs2": lambda u: u * sp.conjugate(u),
    }
    return binary_operators, unary_operators, extra_sympy

def run_one(csv_path, label):
    from pysr import PySRRegressor  # imported lazily: only needed on the machine
    import pandas as pd
    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    X = z.reshape(-1, 1)
    binops, unops, smap = build_naive_toolbox()
    model = PySRRegressor(
        niterations=80,
        population_size=300,
        maxsize=30,
        binary_operators=binops,
        unary_operators=unops,
        extra_sympy_mappings=smap,
        precision=64,
        parsimony=0.001,
        parallelism="multithreading",
        deterministic=False,
        verbosity=1,
        progress=False,
    )
    print(f"    [PySR] fitting {label} from {csv_path} (X.shape={X.shape}, complex)...", flush=True)
    model.fit(X, y)
    best = model.get_best()
    eq = str(best["equation"])
    mse = float(best["loss"])
    print(f"    [PySR] {label}: best_mse={mse:.3e}  eq={eq}")
    return {"dataset": label, "csv": csv_path, "best_equation": eq, "best_mse": mse,
            "mse_below_1e-3": bool(mse < 1e-3)}

def part3_pysr():
    print()
    print("=" * 74)
    print("PART 3 -- NAIVE PySR DETECTOR (needs Julia; expected to run on your machine)")
    print("=" * 74)
    try:
        import pysr  # noqa: F401
    except Exception as e:
        print(f"    [skipped here] PySR not importable in this environment ({e.__class__.__name__}).")
        print("    Run this script on your Linux machine to produce the PySR illustration.")
        return None
    results = {}
    for csv_path, label in [(CSV_HOLO, "holo"), (CSV_ANTI, "anti"), (CSV_TRAP, "trap")]:
        try:
            results[label] = run_one(csv_path, label)
        except Exception as e:
            print(f"    [error] {label}: {e}")
            results[label] = {"dataset": label, "error": str(e)}
    return results


# ---------------------------------------------------------------------------
# PART 4 -- report + official-judge commands
# ---------------------------------------------------------------------------
def part4_report(pysr_results):
    print()
    print("=" * 74)
    print("PART 4 -- REPORT")
    print("=" * 74)
    if not pysr_results:
        print("  PySR not run here. After running on your machine, certify each formula")
        print("  with the OFFICIAL judge:")
        print('    python3 verify_exact.py --formula "<best_equation from %s>"' % OUT_JSON)
        print()
        print("  Expected (TO VERIFY on machine):")
        print("    holo -> judge HOLOMORPHIC,      MSE < 1e-3   (true negative)")
        print("    anti -> judge ANTI-HOLOMORPHIC, MSE < 1e-3   (true positive = pure datum)")
        print("    trap -> judge ANTI-HOLOMORPHIC, MSE < 1e-3   (FALSE positive: massless field)")
        print("    => MSE+judge certify the trap as 'anti' although Part 1 proves no mass.")
        return
    print("  PySR best formulas (markers are INDICATIVE -- certify with the judge):")
    for label, r in pysr_results.items():
        if "error" in r:
            print(f"    {label}: ERROR {r['error']}")
            continue
        print(f"    {label}: MSE={r['best_mse']:.3e}  below_1e-3={r['mse_below_1e-3']}")
        print(f"          eq = {r['best_equation']}")
    print()
    print("  OFFICIAL certification -- paste each command (the judge is the only authority):")
    for label, r in pysr_results.items():
        if "error" in r:
            continue
        eq = r["best_equation"].replace('"', '\\"')
        print(f'    python3 verify_exact.py --formula "{eq}"   # {label}')
    print()
    print("  Reading: 'anti' on holo would be a detector bug; 'anti' on trap is the")
    print("  POINT -- a massless field faking anti content purely because t was put on")
    print("  the imaginary axis. The light-cone d/dv in Part 1 is the honest verdict.")


# ---------------------------------------------------------------------------
def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    bundle = {"script": "spacetime_trap.py"}

    if only in ("all", "symbolic"):
        bundle["symbolic"] = part1_symbolic()
    if only in ("all", "gen", "pysr"):
        part2_data()
    pysr_results = None
    if only in ("all", "pysr"):
        pysr_results = part3_pysr()
        if pysr_results:
            bundle["pysr"] = pysr_results
    if only in ("all", "pysr"):
        part4_report(pysr_results)

    with open(OUT_JSON, "w") as fh:
        json.dump(bundle, fh, indent=2)
    print()
    print(f"[written] {OUT_JSON}")
    print()
    print("RESEARCH_LOG.md line to append AFTER you run it (set status from the run):")
    print("  2026-05-27 [ESTABLISHED if symbolic part executed] spacetime_trap.py: "
          "d/d(zbar) verdict is encoding-dependent; massless cos(x-t) under z=x+it is "
          "FALSELY flagged anti (d/dzbar!=0) while light-cone d/dv=0; d/dzbar cannot "
          "separate massless from massive on time-encoded data. Only native-complex "
          "no-time data give a reliable verdict. eml-star = operator basis, not a sensor. "
          "trace: spacetime_trap.py")


if __name__ == "__main__":
    main()
