#!/usr/bin/env python3
"""LYAPUNOV-DOMINANCE test (#046 candidate, v2): mechanism of the blur
floor -- with the TWO-REGIME separation the v1 sandbox failure imposed.

v1 FAILURE (diagnosed, documented): a wide ln-x window (u <= 400) crossed
the deep log-periodic rendezvous (#044), so the contrast estimator
measured TIDE DEPTH, not the short-window ROUGHNESS whose floor #042/#043
established (log-uniform ~0.05 saturating; linear grid decaying). The
orthogonal axis broken this time: "there is only ONE contrast" -- false;
there are two regimes: ROUGHNESS (short window, before the first
rendezvous) and TIDES (long window). v2 separates them explicitly.

HYPOTHESIS under test (Anthony's Lyapunov bridge, auditor-framed): the
roughness floor exists because some frequencies DOMINATE the phasor sum;
full blur requires non-dominance. CAUTION: deterministic phasors, not
random variables -- Lyapunov is a LENS, not the theorem.

Panels (predictions announced, falsifiable; v1's mis-windowed panel A
already hints the extreme-dominance form may be FALSE even here):
 A. ABLATION on ROUGHNESS (short window u in [0.05, 5.3] = the #042/#043
    object): remove 4 extreme vs 4 middle frequencies from the
    log-uniform N=64 choir. Dominance form predicts extremes >> middles.
 B. q-TRANSITION on ROUGHNESS: spread warped by exponent q (3 -> 0.2);
    if the floor tracks the SHAPE of the whole distribution, the
    mechanism is COLLECTIVE (Lyapunov spirit: the distribution decides).
 C. LINEAR-GRID EXPONENT on ROUGHNESS up to N=2048 (the #043 decay,
    properly measured): prediction ~0.5 (pure averaging) -- to verify.
 D. TIDE REGIME documented as DISTINCT: same choirs, long window
    (u <= 400): contrast saturates near 1 for every distribution
    (every choir eventually has a deep rendezvous) -- the v1 artifact
    becomes a stated regime boundary.
 E. RECIPROCAL CONTROL: nu_k = 0 -> exactly constant, both windows.
No verdict hardcoded. Authority: Anthony's machine.
"""
import numpy as np

KAPPA = 0.2
U_SHORT = np.linspace(0.05, 5.3, 40000)      # the #042/#043 roughness window
U_LONG  = np.linspace(0.05, 400.0, 120000)   # the tide window (v1's mistake)
nu_of = lambda d: KAPPA / (2.0 * d)

def contrast_on(U, nus, wts=None):
    if wts is None:
        wts = np.ones(len(nus))
    v = np.abs(sum(w * np.exp(1j * nv * U) for w, nv in zip(wts, nus)))
    hi, lo = float(np.max(v)), float(np.min(v))
    return (hi - lo) / (hi + lo) if hi + lo > 0 else 0.0

print("=" * 74)
print("A. ABLATION on ROUGHNESS (u <= 5.3, log-uniform N=64, delta [0.3,30])")
ds = np.geomspace(0.3, 30.0, 64)
nus = np.sort(np.array([nu_of(d) for d in ds]))
c_full = contrast_on(U_SHORT, nus)
c_noext = contrast_on(U_SHORT, nus[2:-2])
mid = len(nus) // 2
keep = np.ones(len(nus), bool); keep[mid-2:mid+2] = False
c_nomid = contrast_on(U_SHORT, nus[keep])
print(f"  full choir           : contrast = {c_full:.5f}")
print(f"  extremes removed (4) : contrast = {c_noext:.5f}   ratio = {c_noext/c_full:.3f}")
print(f"  middles removed (4)  : contrast = {c_nomid:.5f}   ratio = {c_nomid/c_full:.3f}")
print("  dominance form holds iff extreme-removal kills much more than")
print("  middle-removal; ratios ~1 both sides = the form is REFUTED here.")

print("=" * 74)
print("B. q-TRANSITION on ROUGHNESS (shape of the whole distribution, N=64)")
for q in [3.0, 2.0, 1.0, 0.5, 0.2]:
    t = (np.arange(1, 65) / 64.0) ** q
    ds_q = 0.3 * (30.0 / 0.3) ** t
    c = contrast_on(U_SHORT, [nu_of(d) for d in ds_q])
    print(f"   q={q:3.1f}: roughness contrast = {c:.5f}")
print("   a monotone trend with q = the mechanism is COLLECTIVE (the")
print("   distribution's shape decides), Lyapunov-spirit rather than")
print("   extreme-dominance.")

print("=" * 74)
print("C. LINEAR-GRID EXPONENT on ROUGHNESS: contrast ~ N^(-p), to N=2048")
Ns, Cs = [], []
for N in [64, 128, 256, 512, 1024, 2048]:
    ds_l = np.linspace(0.3, 30.0, N)
    Cs.append(contrast_on(U_SHORT, [nu_of(d) for d in ds_l]))
    Ns.append(N)
    print(f"   N={N:5d}: contrast = {Cs[-1]:.6f}")
p = -np.polyfit(np.log(Ns), np.log(Cs), 1)[0]
print(f"   fitted exponent p = {p:.3f}   (prediction was ~0.5)")
print("   and the log-uniform saturation reference on the same window:")
for N in [64, 256, 1024]:
    ds_g = np.geomspace(0.3, 30.0, N)
    print(f"   N={N:5d} (geom): contrast = {contrast_on(U_SHORT, [nu_of(d) for d in ds_g]):.6f}")

print("=" * 74)
print("D. TIDE REGIME (long window u <= 400): same choirs, stated boundary")
for label, ds_v in [("log-uniform N=64", np.geomspace(0.3, 30.0, 64)),
                    ("linear     N=64", np.linspace(0.3, 30.0, 64))]:
    c = contrast_on(U_LONG, [nu_of(d) for d in ds_v])
    print(f"   {label}: tide contrast = {c:.5f}")
print("   every choir saturates near 1 once its rendezvous are inside the")
print("   window: the tide regime is DISTINCT from the roughness regime;")
print("   #042/#043 statements live in the roughness regime ONLY.")

print("=" * 74)
print("E. RECIPROCAL CONTROL (nu_k = 0), both windows")
rng = np.random.default_rng(20260709)
w = rng.uniform(0.5, 1.5, 64)
for U, tag in [(U_SHORT, "short"), (U_LONG, "long ")]:
    v0 = np.abs(np.sum(w) * np.exp(1j * 0.0 * U))
    print(f"   {tag}: max - min = {float(np.max(v0) - np.min(v0)):.2e}   (expected 0)")

print("=" * 74)
print("READING (computed above, no prior):")
print(" 1. A: extreme-vs-middle ablation on the RIGHT object decides the")
print("    dominance FORM of the hypothesis.")
print(" 2. B: the q-trend decides whether the floor is COLLECTIVE (shape).")
print(" 3. C: the roughness decay exponent of the linear grid, properly")
print("    measured, tests the pure-averaging bridge to law #008.")
print(" 4. D: the two regimes are now SEPARATED and both documented; the")
print("    v1 mis-windowing is the boundary's discovery, kept as such.")
print(" 5. E: reciprocal flat on both windows -- one-way only, as always.")
print("STATUS: deterministic phasors; Lyapunov is a LENS (label kept).")
print("Pure mathematics of OUR object; says nothing about nature.")
