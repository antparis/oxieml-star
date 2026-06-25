#!/usr/bin/env python3
"""
winding_lens.py -- GLOBAL chirality lens (winding) for the eml* hunt, applied SYSTEMATICALLY:
orthogonal axis on every held-fixed parameter (scale AND loop centre), full cube placement.

It COMPLEMENTS the local Wirtinger / factorization judge; it does not replace it.

CORE LAW (sandbox-validated, [HEURISTIC]): genuine non-removable holo+anti mix
   <=>  ( D = d_z d_zbar log f != 0 )  AND  ( winding is SCALE-DEPENDENT ).
Each test alone has a false positive (D!=0 for real-trapped z+zbar; winding-moves for the
factorizable z*(zbar+1)); the conjunction removes both. Verified 9/9.

SYSTEMATIC ORTHOGONAL AXIS (this version):
  - scale axis: winding swept over MANY decades (not a few fixed radii).
  - loop-centre axis (the previously held-fixed assumption): centres scanned over the plane ->
    a DEFECT CENSUS. This exposes the deep cube distinction:
       real-trapped  -> zeros lie on a CURVE (no isolated winding) -> winding 0 everywhere
       holo/anti/module/mix -> zeros are ISOLATED POINTS with signed winding (+ holo / - anti)
CUBE PLACEMENT (2x2x2): factorizable? (D) x transcendental? (non-polynomial) x
  point-vs-line zeros (chiral vs real-trapped), with the signed defect census.

Caveat: integer windings only; fractional branch monodromy stays the singularity_reader's job.
On real noisy data: survives to noise/signal ~ 1; blizzard needs scale-bin averaging N>=(n/s)^2.
"""
import numpy as np
import sympy as sp

def winding(fvals):
    a = np.unwrap(np.angle(fvals)); return (a[-1] - a[0]) / (2 * np.pi)
def _loop(c, R, n=400):
    th = np.linspace(0, 2 * np.pi, n, endpoint=True); return c + R * np.exp(1j * th)

# ---- orthogonal axis 1: SCALE swept over many decades ----
def scale_behavior(f_np, decades=(-2.0, 2.5), npts=40):
    Rs = np.logspace(decades[0], decades[1], npts)
    ws = [round(winding(f_np(_loop(0j, R)))) for R in Rs]
    if all(w == 0 for w in ws): return "const0", ws
    if len(set(ws)) == 1:       return f"const{ws[0]:+d}", ws
    return "scale-dependent", ws

# ---- orthogonal axis 2: LOOP CENTRE scanned over the plane -> defect census ----
def defect_census(f_np, extent=3.0, ngrid=41, r=0.10):
    xs = np.linspace(-extent, extent, ngrid)
    found = []
    vanishes = False
    for cx in xs:
        for cy in xs:
            c = cx + 1j * cy
            vals = f_np(_loop(c, r, 120))
            if np.min(np.abs(vals)) < 1e-6:
                vanishes = True
            w = winding(vals)
            if abs(w) > 0.5 and abs(w - round(w)) < 0.3 and round(w) != 0:
                found.append((round(cx, 2), round(cy, 2), int(round(w))))
    # cluster nearby same-sign cells
    clusters = []
    for cx, cy, w in found:
        hit = next((k for k, (px, py, pw, n) in enumerate(clusters)
                    if abs(px - cx) < 0.4 and abs(py - cy) < 0.4 and pw == w), None)
        if hit is None: clusters.append([cx, cy, w, 1])
        else:
            clusters[hit][0] = (clusters[hit][0] * clusters[hit][3] + cx) / (clusters[hit][3] + 1)
            clusters[hit][1] = (clusters[hit][1] * clusters[hit][3] + cy) / (clusters[hit][3] + 1)
            clusters[hit][3] += 1
    pts = [(round(c[0], 2) + round(c[1], 2) * 1j, c[2]) for c in clusters]
    return pts, vanishes

# ---- local lens ----
_z, _zb = sp.symbols('z zb')
def disc(f_sym): return sp.simplify(sp.diff(sp.diff(sp.log(f_sym), _zb), _z))
def is_transcendental(f_sym):
    return any(f_sym.has(fn) for fn in (sp.exp, sp.log, sp.sin, sp.cos))

# ---- full systematic classify (cube + both orthogonal axes + conjunction gate) ----
def classify(f_sym, f_np):
    D = disc(f_sym); nonfact = (D != 0)
    trans = is_transcendental(f_sym)
    beh, _ = scale_behavior(f_np)
    sdep = (beh == "scale-dependent")
    pts, vanishes = defect_census(f_np)
    isolated = len(pts) > 0
    real_trapped = vanishes and not isolated
    # cube corner
    cube = (("non-factoriz" if nonfact else "factoriz") + " x " +
            ("transcendent" if trans else "algebraic") + " x " +
            ("point-zeros(chiral)" if isolated else ("line-zeros(real-trapped)" if real_trapped else "no-zero")))
    if nonfact and sdep:
        verdict = "GENUINE-MIX CANDIDATE (disc!=0 AND scale-dependent)"
    elif real_trapped or beh == "const0":
        verdict = "WALL: real-trapped / no isolated chirality"
    elif not sdep:
        verdict = f"WALL: single-chirality/module (winding {beh})"
    else:
        verdict = "WALL: factorizable w/ off-centre zero (winding moves but disc=0)"
    return dict(disc_nonzero=nonfact, scale=beh, defects=pts, real_trapped=real_trapped,
                cube=cube, verdict=verdict)

def _battery():
    z, zb = _z, _zb
    B = [("z^2","wall",z**2,lambda Z:Z**2),
         ("conj^2","wall",zb**2,lambda Z:np.conj(Z)**2),
         ("z*conj","wall",z*zb,lambda Z:Z*np.conj(Z)),
         ("z^2*conj","wall",z**2*zb,lambda Z:Z**2*np.conj(Z)),
         ("z+conj","wall",z+zb,lambda Z:Z+np.conj(Z)),
         ("z^2+conj","MIX",z**2+zb,lambda Z:Z**2+np.conj(Z)),
         ("z+conj^2","MIX",z+zb**2,lambda Z:Z+np.conj(Z)**2),
         ("z*(conj+1)","wall",z*(zb+1),lambda Z:Z*(np.conj(Z)+1)),
         ("exp(z)+conj","MIX",sp.exp(z)+zb,lambda Z:np.exp(Z)+np.conj(Z))]
    ok = 0
    for name, truth, fs, fn in B:
        r = classify(fs, fn)
        is_mix = "GENUINE-MIX" in r["verdict"]
        correct = (is_mix == (truth == "MIX")); ok += correct
        print(f"{name:12s}| cube=[{r['cube']:54s}]")
        print(f"             scale={r['scale']:16s} defects={r['defects']}")
        print(f"             -> {r['verdict']}  [{'ok' if correct else 'WRONG'}]")
    print(f"\nself-test: {ok}/9 correct  ({'PASS' if ok == 9 else 'FAIL'})")
    return ok == 9

if __name__ == "__main__":
    _battery()
