#!/usr/bin/env python3
"""
ring_field.py -- A field that is holomorphic everywhere EXCEPT on a ring, where
the geometry FORCES anti-holomorphic content. The "two faces in one object" on
NATIVELY-COMPLEX, SPATIAL, TIME-FREE data.

WHY THIS IS THE RIGHT FORM (and not the time trap, not a 1D disguise)
  - Variable z = x + i*y is a SPATIAL position (no time on any axis) -> no Wick/
    SPARC artefact (cf. spacetime_trap.py).
  - The object lives on a 2D region (a disk), not a 1D curve. On a curve, conj(z)
    coincides with a holomorphic Schwarz function (e.g. conj(z)=R^2/z on |z|=R), so
    holo/anti are indistinguishable in 1D. On a 2D band they are NOT: the field is
    non-holomorphic on an open set -> the anti content is GENUINE, not a boundary
    disguise.
  - The anti part is FORCED by geometry (a ring source), not chosen term by term,
    so it is more than a hand-injected calibration: removing the ring removes the
    anti content.

THE FIELD (closed form, so PySR + judge can certify it exactly)
    u = |z|^2 = z*conj(z)
    g(u) = exp( -(u - R^2)^2 / s^2 )            # radial window peaked on |z| = R
    E(z) = z  +  g(u) * conj(z)                 # holo part z + anti part g*conj(z)

  Exact Wirtinger derivative (z, zbar independent):
    dE/d(zbar) = g(u) + u*g'(u)  with  g'(u) = g(u)*(-2(u-R^2)/s^2)
               = g(u) * ( 1 - 2*u*(u-R^2)/s^2 )
  This is a REAL radial function of u=|z|^2:
    * ~0 far from the ring (g -> 0)  -> E is holomorphic there;
    * != 0 on the annular band (g ~ 1) -> anti-holomorphic content, LOCALIZED.

WHAT eml / eml-star DO HERE
  Not "compute physics": they are the OPERATOR BASIS that lets the symbolic-
  regression detector reconstruct E, and the judge verify_exact.py then CERTIFIES
  the two faces: dE/d(zbar) != 0 (there is anti content) and shows WHERE (the ring).

SCOPE / HONESTY
  The mathematics (Wirtinger, dbar/Pompeiu, harmonic h + conj(g)) is CLASSICAL,
  not new. This is a CALIBRATION-grade construction (we chose the form), so the
  result is a VALIDATION that the pipeline reads LOCALIZED anti structure on
  time-free 2D data -- NOT a discovery, NOT cosmology. The link to physical rings
  (Lopez) or CCC is an ANALOGY only, unproven, and out of scope of this script.

ARBITER: the official judge is verify_exact.py (d/d(zbar)). Part 1 here is exact
SymPy on a KNOWN closed form. PySR (Part 3) needs Julia and runs on the machine;
its MSE is only valid when executed there.

Author: Anthony Monnerot, 2026. English only.
"""

import sys
import json
import numpy as np
import sympy as sp

R = 1.0          # ring radius (|z| = R)
R2 = R * R       # R^2
S2 = 0.16        # window width^2 in u (s = 0.4)

OUT_JSON = "ring_field_result.json"
CSV_RING = "ring_field_ring.csv"   # localized-anti field (positive)
CSV_HOLO = "ring_field_holo.csv"   # E = z, no source (negative: pure holo)
CSV_SHUF = "ring_field_shuffled.csv"  # ring with target permuted (negative: noise)


# ---------------------------------------------------------------------------
# PART 1 -- exact symbolic proof + localization map
# ---------------------------------------------------------------------------
def part1_symbolic():
    print("=" * 74)
    print("PART 1 -- EXACT SYMBOLIC PROOF (SymPy) + ring localization")
    print("=" * 74)

    z, zbar = sp.symbols("z zbar")
    u = z * zbar
    R2s, S2s = sp.Rational(1, 1), sp.Rational(4, 25)  # 1.0 and 0.16 exactly
    g = sp.exp(-(u - R2s) ** 2 / S2s)
    E = z + g * zbar

    dEdz = sp.simplify(sp.diff(E, z))         # holomorphic-direction derivative
    dEdzbar = sp.simplify(sp.diff(E, zbar))   # the anti content

    # radial closed form g(u) + u g'(u)
    uu = sp.symbols("u", positive=True)
    g_u = sp.exp(-(uu - R2s) ** 2 / S2s)
    radial = sp.simplify(g_u + uu * sp.diff(g_u, uu))

    print()
    print("Field:  E(z) = z + g(|z|^2)*conj(z),  g(u)=exp(-(u-1)^2/0.16),  u=|z|^2")
    print(f"  dE/dz       = {dEdz}")
    print(f"  dE/d(zbar)  = {sp.simplify(dEdzbar)}")
    print(f"  (radial)    dE/d(zbar) as f(u) = {radial}")
    print()
    print("Control:  E_holo(z) = z   ->   dE/d(zbar) = 0  (holomorphic everywhere)")
    print()

    # numeric localization: |dE/dzbar| on a radial scan
    f_radial = sp.lambdify(uu, sp.Abs(radial), "numpy")
    rs = np.linspace(0.0, 1.8, 19)
    print("Localization scan |dE/d(zbar)| vs radius |z|:")
    print("   |z|    u=|z|^2   |dE/dzbar|")
    on_ring_max = 0.0
    far_max = 0.0
    for r in rs:
        val = float(f_radial(r * r))
        tag = ""
        if abs(r - R) < 0.12:
            tag = "  <- ON RING"
            on_ring_max = max(on_ring_max, val)
        if r < 0.4 or r > 1.5:
            far_max = max(far_max, val)
        print(f"  {r:4.2f}   {r*r:6.3f}   {val:10.4f}{tag}")
    print()
    print(f"  max |dE/dzbar| on ring  ~ {on_ring_max:.3f}")
    print(f"  max |dE/dzbar| far away ~ {far_max:.3e}")
    ratio = on_ring_max / far_max if far_max > 0 else float("inf")
    print(f"  ring / far ratio        ~ {ratio:.3e}")
    print()
    print("-" * 74)
    print("READING (exact):")
    print("  * dE/d(zbar) != 0 on a 2D annular BAND (open set) -> genuine anti content,")
    print("    NOT a 1D Schwarz disguise.")
    print("  * dE/d(zbar) ~ 0 far from the ring -> the field is holomorphic there.")
    print("  * One object, two faces, ONE spatial complex variable, NO time axis.")
    print("-" * 74)

    return {
        "field": "E(z) = z + exp(-(|z|^2-1)^2/0.16)*conj(z)",
        "dE_dzbar_radial": str(radial),
        "dE_dz": str(dEdz),
        "on_ring_max_abs_dzbar": float(on_ring_max),
        "far_max_abs_dzbar": float(far_max),
        "ring_over_far_ratio": float(ratio),
    }


# ---------------------------------------------------------------------------
# PART 2 -- data generation (2D spatial, native complex)
# ---------------------------------------------------------------------------
def g_window(u):
    return np.exp(-((u - R2) ** 2) / S2)

def field_E(z):
    u = (z * np.conj(z)).real
    return z + g_window(u) * np.conj(z)

def sample_disk(n, radius, seed):
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        zz = rng.uniform(-radius, radius) + 1j * rng.uniform(-radius, radius)
        if abs(zz) < radius:
            pts.append(zz)
    return np.array(pts[:n])

def export(fname, z, w):
    arr = np.column_stack([z.real, z.imag, w.real, w.imag])
    np.savetxt(fname, arr, delimiter=",", header="z_re,z_im,w_re,w_im", comments="")
    print(f"    wrote {fname}  ({len(z)} rows)")

def part2_data(n=1500, seed=42):
    print()
    print("=" * 74)
    print("PART 2 -- DATA GENERATION (2D spatial disk, native complex, no time)")
    print("=" * 74)
    z = sample_disk(n, 1.8, seed)
    w_ring = field_E(z)
    w_holo = z.copy()
    export(CSV_RING, z, w_ring)   # positive: localized anti
    export(CSV_HOLO, z, w_holo)   # negative control: pure holo
    # negative control: shuffle the ring target (destroy structure)
    rng = np.random.default_rng(seed + 7)
    perm = rng.permutation(len(z))
    export(CSV_SHUF, z, w_ring[perm])
    corr = np.corrcoef(z.real, z.imag)[0, 1]
    print(f"    disk input corr(Re,Im) = {corr:+.3f}  (near 0 = genuine 2D, spatial)")
    # self-check: target equals the closed form exactly
    err = np.max(np.abs(w_ring - field_E(z)))
    print(f"    max|target - closed form| = {err:.3e}  (must be ~0)")


# ---------------------------------------------------------------------------
# PART 3 -- PySR illustration (needs Julia; runs on Anthony's machine)
# ---------------------------------------------------------------------------
def build_toolbox():
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
        "my_conj": lambda v: sp.conjugate(v),
        "my_real": lambda v: sp.re(v),
        "my_imag": lambda v: sp.im(v),
        "my_abs2": lambda v: v * sp.conjugate(v),
    }
    return binary_operators, unary_operators, extra_sympy

def run_one(csv_path, label):
    from pysr import PySRRegressor
    import pandas as pd
    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    X = z.reshape(-1, 1)
    binops, unops, smap = build_toolbox()
    model = PySRRegressor(
        niterations=60,
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
    return {"dataset": label, "csv": csv_path, "best_equation": eq,
            "best_mse": mse, "mse_below_1e-3": bool(mse < 1e-3)}

def part3_pysr():
    print()
    print("=" * 74)
    print("PART 3 -- DETECTOR (PySR; needs Julia; runs on your machine)")
    print("=" * 74)
    try:
        import pysr  # noqa: F401
    except Exception as e:
        print(f"    [skipped here] PySR not importable ({e.__class__.__name__}).")
        print("    Run on your Linux machine to produce the detector illustration.")
        return None
    results = {}
    for csv_path, label in [(CSV_RING, "ring"), (CSV_HOLO, "holo"), (CSV_SHUF, "shuffled")]:
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
        print("    ring     -> judge ANTI-HOLOMORPHIC, MSE < 1e-3  (localized anti, true)")
        print("    holo     -> judge HOLOMORPHIC,      MSE < 1e-3  (no source, true negative)")
        print("    shuffled -> REJECTED (MSE >> 1e-3)              (noise, no structure)")
        return
    print("  PySR best formulas (markers INDICATIVE -- certify with the judge):")
    for label, r in pysr_results.items():
        if "error" in r:
            print(f"    {label}: ERROR {r['error']}")
            continue
        print(f"    {label}: MSE={r['best_mse']:.3e}  below_1e-3={r['mse_below_1e-3']}")
        print(f"          eq = {r['best_equation']}")
    print()
    print("  OFFICIAL certification -- paste each (the judge is the only authority):")
    for label, r in pysr_results.items():
        if "error" in r:
            continue
        eq = r["best_equation"].replace('"', '\\"')
        print(f'    python3 verify_exact.py --formula "{eq}"   # {label}')
    print()
    print("  Reading: ring -> anti (and Part 1 shows the anti is LOCALIZED on |z|=1);")
    print("  holo -> holomorphic (no source); shuffled -> rejected. The two faces of")
    print("  one spatial object, certified, with NO time axis involved.")


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    bundle = {"script": "ring_field.py", "R": R, "s2": S2}

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
    print("  2026-05-27 [ESTABLISHED if symbolic part executed] ring_field.py: built a 2D "
          "spatial (time-free) field E(z)=z+g(|z|^2)conj(z), g a ring window. Exact: "
          "dE/dzbar=g(u)+u g'(u) is real-radial, !=0 on the annular band (genuine 2D anti, "
          "not a 1D Schwarz disguise) and ~0 far away (holomorphic). Two faces in one object. "
          "CALIBRATION-grade validation that the pipeline reads LOCALIZED anti on spatial data; "
          "NOT a discovery, NOT cosmology (Lopez/CCC link = analogy only). trace: ring_field.py")


if __name__ == "__main__":
    main()
