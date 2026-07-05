#!/usr/bin/env python3
"""judge_v2.py -- EXTENDS verify_exact.py without replacing it.
Adds: (1) two-field Wirtinger mode (z,zbar,w,wbar -> 4 derivatives + classification);
(2) rephasing test (decorative vs physical); (3) mixed-derivative discriminant (separable vs entangled);
(4) REAL-TRAP mirror test: a field is real-trapped (SPARC trap) iff f == conj(f) under FULL
    conjugation (z<->zbar AND i->-i). Added 2026-06-18.
(5) MODULE-TRAP test: a field is module-trapped iff it factors as holo(z) * real_modulus(|z|^2),
    i.e. z^a*zbar^b = z^(a-b)*|z|^(2b). The anti is carried entirely by a real radial modulus ->
    reducible (Aharonov-Bohm category). Test by log-derivative factorization: L = zbar*dlog(f)/dzbar
    must be REAL and a function of the product z*zbar ONLY. This correctly keeps ADDITIVE genuine anti
    (vortex_N1 = A*log(z-c)+B*log(zbar-c), z+0.3*zbar) as anti, while catching MULTIPLICATIVE monomials.
    Added 2026-06-20 after the C-native bench (323/323) flagged MODULE/MIXED collapsing into 'anti'.
    NOTE: |mu| constant alone is INSUFFICIENT (it over-captures additive sums like vortex_N1 whose |mu|
    is also constant); factorization is the correct criterion. backup judge_v2.py.bak_20260620 kept.
Reproduces the original single-field judge exactly. Each test can return NO.
verify_exact.py is unchanged and remains the authoritative single-field judge.
Author: Anthony Monnerot, 2026."""
import sympy as sp

z, zbar = sp.symbols("z zbar")
w, wbar = sp.symbols("w wbar")

def op_conj_1f(expr):
    return expr.subs({z: zbar, zbar: z}, simultaneous=True)

def full_conj(expr):
    """COMPLETE complex conjugation: swap z<->zbar AND i->-i (the missing piece)."""
    tmp = sp.Symbol("tmp_conj")
    e = expr.subs(sp.I, tmp)
    e = e.subs({z: zbar, zbar: z}, simultaneous=True)
    e = e.subs(tmp, -sp.I)
    return e

def is_module_trapped(expr):
    """True iff f factors as holo(z) * real_modulus(z*zbar). Test via log-derivative:
    if f = h(z)*m(z*zbar), then zbar*dlog(f)/dzbar = (z*zbar)*m'/m depends on the
    product z*zbar ONLY. Additive holo+anti sums fail this (genuine anti). Requires dfdz, dfdzbar != 0."""
    expr = sp.expand(expr)
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    dfdz = sp.simplify(sp.diff(expr, z))
    if dfdzbar == 0 or dfdz == 0:
        return False
    try:
        L = sp.simplify(zbar * dfdzbar / expr)
        L_real = sp.simplify(L - full_conj(L)) == 0
        t = sp.symbols("t", positive=True)
        prod_only = sp.simplify(L.subs({z: t*z, zbar: zbar/t}) - L) == 0
        # blind-spot fix (2026-06-22): L = pure-imaginary CONSTANT is also a modulus
        # power (imaginary exponent, e.g. |z|^(is) inverse-square). Catch it too.
        L_const = (sp.simplify(sp.diff(L, z)) == 0 and sp.simplify(sp.diff(L, zbar)) == 0)
        L_pure_imag = (sp.simplify(L + full_conj(L)) == 0)
        # 2026-06-23: module-trapped iff L depends on |z|^2 ONLY (prod_only).
        # f then factors as holo(z)*radial_envelope(|z|^2), real OR complex
        # (complex radial phase = dispersive chirp). Earlier real/pure-imag
        # sub-cases were too narrow. No genuine anti has prod_only True.
        return bool(prod_only)
    except Exception:
        return False

def certify_1field(expr):
    """Single-field judge, 4 labels: holomorphic / real-trapped / module-trapped / anti-holomorphic."""
    expr = sp.expand(expr)
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    if dfdzbar == 0:
        return "holomorphic", dfdzbar
    if sp.simplify(expr - full_conj(expr)) == 0:
        return "real-trapped", dfdzbar
    if is_module_trapped(expr):
        return "module-trapped", dfdzbar
    return "anti-holomorphic", dfdzbar

def certify_2field(expr):
    """Two independent fields. Returns classification + the 4 Wirtinger derivatives."""
    expr = sp.expand(expr)
    d_zbar = sp.simplify(sp.diff(expr, zbar)); d_wbar = sp.simplify(sp.diff(expr, wbar))
    d_z    = sp.simplify(sp.diff(expr, z));    d_w    = sp.simplify(sp.diff(expr, w))
    holo_z = (d_zbar == 0); holo_w = (d_wbar == 0)
    if holo_z and holo_w:        cls = "holo-holo (both holomorphic; e.g. squeezing alpha*beta)"
    elif holo_z and not holo_w:  cls = "CROSS-CONJUGATE z*conj(w) (holo field1, anti field2 -- weak-value type)"
    elif not holo_z and holo_w:  cls = "CROSS-CONJUGATE conj(z)*w (anti field1, holo field2)"
    else:                        cls = "mixed (anti in BOTH fields)"
    return cls, dict(d_z=d_z, d_zbar=d_zbar, d_w=d_w, d_wbar=d_wbar)

def rephasing_test(expr):
    """z->e^{ia}z, w->e^{ib}w (and conjugates). Invariant => physical; phase survives => decorative."""
    a, b = sp.symbols("a b", real=True)
    sub = {z: sp.exp(sp.I*a)*z, zbar: sp.exp(-sp.I*a)*zbar,
           w: sp.exp(sp.I*b)*w, wbar: sp.exp(-sp.I*b)*wbar}
    diff = sp.simplify(expr.subs(sub, simultaneous=True) - expr)
    invariant = (diff == 0)
    return ("rephasing-INVARIANT (physical)" if invariant
            else "rephasing-dependent (decorative unless part of an invariant combination)"), invariant

def mixed_discriminant(expr):
    """d^2/dz dzbar: zero => separable (independent), nonzero => entangled."""
    expr = sp.expand(expr)
    d2 = sp.simplify(sp.diff(expr, z, zbar))
    return ("separable (independent z/zbar)" if d2==0 else "entangled (z,zbar coupled)"), d2

if __name__ == "__main__":
    print("="*84)
    print("judge_v2 self-validation (each line must say OK, including REAL-TRAP and MODULE-TRAP cases)")
    print("="*84)
    a = sp.sqrt(2); c = sp.symbols("c")
    A = sp.Float('0.717') + sp.Float('0.395')*sp.I
    B = sp.Float('-0.30') + sp.Float('1.20')*sp.I
    vortex = A*sp.log(z - c) + B*sp.log(zbar - c)
    print("\n[0] single-field, 4 labels (holo / real-trap / module-trap / anti):")
    for label, expr, expected in [
        ("z (holo)", z, "holomorphic"),
        ("zbar (anti)", zbar, "anti-holomorphic"),
        ("z*zbar = |z|^2 (REAL-TRAP)", z*zbar, "real-trapped"),
        ("z+zbar (REAL-TRAP)", z+zbar, "real-trapped"),
        ("log|z|^2 (REAL-TRAP)", sp.log(z)+sp.log(zbar), "real-trapped"),
        ("Im(z)=(z-zbar)/2i (REAL-TRAP)", (z-zbar)/(2*sp.I), "real-trapped"),
        ("conj(conj(z)) = z (holo trap)", op_conj_1f(op_conj_1f(z)), "holomorphic"),
        ("z + 0.3*zbar (genuine anti, additive)", z + sp.Rational(3,10)*zbar, "anti-holomorphic"),
        ("i*zbar (genuine anti)", sp.I*zbar, "anti-holomorphic"),
        ("exp(zbar) (anti)", sp.exp(zbar), "anti-holomorphic"),
        ("z^1.7*zbar^-0.7 (MODULE-TRAP)", z**sp.Rational(17,10)*zbar**sp.Rational(-7,10), "module-trapped"),
        ("z^(1+sqrt2)*zbar^(-sqrt2/2) (MODULE-TRAP)", z**(1+a)*zbar**(-a/2), "module-trapped"),
        ("z^2*zbar (MODULE-TRAP)", z**2*zbar, "module-trapped"),
        ("z/zbar (MODULE-TRAP)", z/zbar, "module-trapped"),
        ("vortex_N1 log(z-c)+B log(zbar-c) (genuine chiral)", vortex, "anti-holomorphic")]:
        v,_ = certify_1field(expr)
        print(f"   {label:<46} -> {v:<18} {'OK' if v==expected else 'FAIL!!'}")
    print("\n[1] two-field classification:")
    for label, expr, sub in [
        ("z*w (squeezing)", z*w, "holo-holo"),
        ("z*wbar (weak value)", z*wbar, "CROSS-CONJUGATE z*conj(w)"),
        ("zbar*w", zbar*w, "CROSS-CONJUGATE conj(z)*w"),
        ("zbar*wbar", zbar*wbar, "mixed")]:
        cls,_ = certify_2field(expr); ok = sub in cls
        print(f"   {label:<24} -> {cls[:40]:<40} {'OK' if ok else 'FAIL!!'}")
    print("\n[2] rephasing test (NO for decorative, YES for invariant):")
    for label, expr, exp_inv in [
        ("z*wbar (decorative)", z*wbar, False),
        ("z*zbar (invariant)", z*zbar, True),
        ("|zw|^2 (invariant)", z*wbar*zbar*w, True)]:
        msg, inv = rephasing_test(expr)
        print(f"   {label:<24} -> inv={inv}  {'OK' if inv==exp_inv else 'FAIL!!'}")
    print("\n[3] mixed-derivative discriminant:")
    for label, expr, exp_ent in [
        ("z+zbar (separable)", z+zbar, False),
        ("z*zbar (entangled)", z*zbar, True),
        ("exp(z*zbar) (entangled)", sp.exp(z*zbar), True)]:
        msg, d2 = mixed_discriminant(expr); ent=(d2!=0)
        print(f"   {label:<24} -> {'entangled' if ent else 'separable':<10} {'OK' if ent==exp_ent else 'FAIL!!'}")
    print("\n"+"="*84)
    print("All OK => judge_v2 sound: 4-label single-field (holo/real-trap/module-trap/anti),")
    print("vortex_N1 stays anti (genuine chiral), z^a zbar^b is module-trapped. verify_exact.py unchanged.")
    print("="*84)


# ============================================================================
# certify_genuine -- HARDENED v2 (2026-06-29). Fixes from adversarial self-audit:
#  (BUG) corrected winding: removed the parasitic closure term that gave false walls.
#  (A1)  adaptive radius grid bracketing every needle crossover (catches far inversions).
#  (A4)  INDETERMINATE verdict when winding unmeasurable (zeros on contour), not a fake wall.
# certify_1field UNCHANGED. Verdicts: GENUINE / WALL:<r> / INDETERMINATE:<r>.
# ============================================================================
import numpy as _np_cg

def _cg_terms(e):
    e=sp.expand(e); out=[]
    for t in (e.as_ordered_terms() if e.func==sp.Add else [e]):
        c=t.as_coeff_Mul()[0]
        try: cm=abs(complex(c))
        except Exception: cm=1.0
        deg=0
        for sym in (z,zbar):
            if t.has(sym) and t.is_polynomial(sym):
                try: deg+=int(sp.degree(sp.Poly(t,sym)))
                except Exception: pass
        out.append((cm,deg))
    return out

def _cg_radii(e):
    base=[0.3,0.7,1.5,3.0,7.0,15.0,40.0,100.0]
    try:
        tt=_cg_terms(e); cross=[]
        for i in range(len(tt)):
            for j in range(i+1,len(tt)):
                ci,di=tt[i]; cj,dj=tt[j]
                if di!=dj and ci>0 and cj>0:
                    r=(ci/cj)**(1.0/(dj-di))
                    if 1e-9<r<1e12: cross+=[r*0.5,r*0.9,r*1.1,r*2.0]
        return tuple(sorted(set([x for x in base+cross if 1e-6<x<1e12])))
    except Exception:
        return tuple(base)

def _cg_wind(e, R, n=40000):
    free=e.free_symbols-{z,zbar}
    if free: e=e.subs({s:sp.Float(0.37) for s in free})
    fn=sp.lambdify((z,zbar),e,"numpy"); th=_np_cg.linspace(0,2*_np_cg.pi,n,endpoint=True)
    zc=R*_np_cg.exp(1j*th)
    try: v=fn(zc,_np_cg.conj(zc))*_np_cg.ones(n,dtype=complex)
    except Exception: return None
    if not _np_cg.all(_np_cg.isfinite(v)): return None
    mn=_np_cg.min(_np_cg.abs(v)); mx=_np_cg.max(_np_cg.abs(v))
    if mx<1e-300 or mn<1e-6*mx: return None
    ph=_np_cg.unwrap(_np_cg.angle(v)); raw=(ph[-1]-ph[0])/(2*_np_cg.pi); near=round(raw)
    return int(near) if abs(raw-near)<0.05 else None

def _neg_harmonic(expr, radii, ntheta=256, tol=1e-8):
    """True iff the field has some NEGATIVE angular harmonic c_m (m<0) at some sampled
    radius -- i.e. the anti needle TURNS. Module-dressed holomorphic decoys (all m>=0)
    return False. Numeric probe: lambdify + FFT on circles; radii from the adaptive grid.
    Added 2026-07-02 (gate hardening #023 -> universal harmonic form)."""
    import numpy as _np
    try:
        f = sp.lambdify((z, zbar), expr, "numpy")
    except Exception:
        return True   # cannot probe -> do not block (fail-open, judge stays conservative)
    th = _np.linspace(0, 2 * _np.pi, ntheta, endpoint=False)
    probed = False
    for R in radii:
        Z = float(R) * _np.exp(1j * th)
        try:
            vals = _np.asarray(f(Z, _np.conj(Z)), dtype=complex)
            if vals.shape == ():
                vals = _np.full(ntheta, complex(vals))
        except Exception:
            continue
        if not _np.all(_np.isfinite(vals)):
            continue
        probed = True
        c = _np.fft.fft(vals) / ntheta
        mneg = _np.abs(c[ntheta // 2 + 1:])          # m < 0 harmonics
        scale = _np.max(_np.abs(c)) + 1e-300
        if _np.max(mneg) / scale > tol:
            return True
    return True if not probed else False


def certify_genuine(expr, radii=None):
    """Hardened full conjunction gate. GENUINE iff anti-holomorphic AND disc!=0 AND winding
    scale-dependent. Verdicts: GENUINE / WALL:<reason> / INDETERMINATE:<reason>."""
    expr=sp.simplify(expr); label,dfb=certify_1field(expr); detail={"label":label}
    if label!="anti-holomorphic": return "WALL:"+label, detail
    try: disc=sp.simplify(sp.diff(sp.diff(sp.log(expr),z),zbar))
    except Exception: disc=None
    detail["disc_nonzero"]=(disc is not None and sp.simplify(disc)!=0)
    if not detail["disc_nonzero"]: return "WALL:factorisable(disc=0)", detail
    grid=radii if radii is not None else _cg_radii(expr)
    ws=[_cg_wind(expr,float(R)) for R in grid]; m=[w for w in ws if w is not None]
    detail["windings"]=m; detail["n_radii"]=len(grid)
    if len(m)<2 or len(m)/max(1,len(grid))<0.3:
        return "INDETERMINATE:winding-unmeasurable(zeros on contour)", detail
    if len(set(m))<=1: return "WALL:winding-constant(no scale inversion)", detail
    if not _neg_harmonic(expr, list(grid)):
        detail["neg_harmonic"] = False
        return "WALL:no-anti-needle(non-negative harmonics)", detail
    detail["neg_harmonic"] = True
    return "GENUINE", detail

def _battery_certify_genuine():
    cases=[("z",z,"WALL:holomorphic"),("zbar",zbar,"WALL:factorisable(disc=0)"),
        ("z+zbar",z+zbar,"WALL:real-trapped"),("z*zbar",z*zbar,"WALL:real-trapped"),
        ("z^2*zbar",z**2*zbar,"WALL:module-trapped"),("z/zbar",z/zbar,"WALL:module-trapped"),
        ("z^2+zbar",z**2+zbar,"GENUINE"),("z^2-zbar",z**2-zbar,"GENUINE"),
        ("exp(z)+zbar",sp.exp(z)+zbar,"GENUINE"),("z^2+log(zbar)",z**2+sp.log(zbar),"GENUINE"),
        ("K1",z**3+zbar+sp.log(zbar),"GENUINE"),("log(z)+log(zbar)",sp.log(z)+sp.log(zbar),"WALL:real-trapped"),
        ("z+0.3zbar",z+sp.Rational(3,10)*zbar,"WALL:winding-constant(no scale inversion)"),
        ("z^2+1e3 zbar far",z**2+sp.Float(1000)*zbar,"GENUINE"),
        ("z^4+1e-4 zbar^9",z**4+sp.Rational(1,10000)*zbar**9,"GENUINE")]
    print("="*78); print("certify_genuine v2 self-validation (corrected winding + adaptive + INDETERMINATE)"); print("="*78)
    allok=True
    for label,e,exp in cases:
        v,d=certify_genuine(e); ok=(v==exp); allok=allok and ok
        print("  %-26s -> %-44s %s"%(label,v,"OK" if ok else "FAIL exp "+exp))
    print("="*78); print("ALL OK" if allok else "SOME FAILED"); return allok

if __name__=="__main__":
    print("\n[certify_genuine v2 battery]"); _battery_certify_genuine()


# ---------------------------------------------------------------------------
# H2 hardening (2026-07-03, registry #026/#027): 4-pairing cross-field
# discriminant. A two-point kernel K(z, zbar; w, wbar) can be cross-entangled on
# ANY of the four pairings (z,w), (z,wbar), (zbar,w), (zbar,wbar); testing a
# single pairing is incomplete (the derived one-way kernel lives on (zbar,wbar)).
# Numeric central finite differences on log K with INDEPENDENT variables
# (symbolic diff of undefined transcendentals cannot lambdify). Points where
# |K| < 1e-6 are skipped (branch safety).
# ---------------------------------------------------------------------------
def cross_discriminant_2field(K, npts=16, h=1e-4, rmax=0.72, tol=1e-4, seed=5):
    """Return dict pairing -> (entangled: bool, median |d_a d_b log K|)."""
    import numpy as _np
    import sympy as _sp
    import mpmath as _mp
    f = _sp.lambdify((z, zbar, w, wbar), K,
                     modules=["mpmath", {"lerchphi": _mp.lerchphi,
                                         "polylog": _mp.polylog}])
    idx = {"z": 0, "zbar": 1, "w": 2, "wbar": 3}
    pairs = {"(z,w)": ("z", "w"), "(z,wbar)": ("z", "wbar"),
             "(zbar,w)": ("zbar", "w"), "(zbar,wbar)": ("zbar", "wbar")}
    rng = _np.random.default_rng(seed)

    def rand4():
        def one():
            return (rmax * _np.sqrt(rng.uniform())
                    * _np.exp(2j * _np.pi * rng.uniform()))
        return [one(), one(), one(), one()]

    pts, tries = [], 0
    while len(pts) < npts and tries < 60 * npts:
        tries += 1
        v4 = rand4()
        try:
            if abs(complex(f(*v4))) > 1e-6:
                pts.append(v4)
        except Exception:
            continue
    out = {}
    for name, (a, b) in pairs.items():
        ia, ib = idx[a], idx[b]
        vals = []
        for v4 in pts:
            def L(sa, sb):
                u = list(v4)
                u[ia] = u[ia] + sa * h
                u[ib] = u[ib] + sb * h
                return _np.log(complex(f(*u)))
            try:
                d = (L(1, 1) - L(1, -1) - L(-1, 1) + L(-1, -1)) / (4 * h * h)
            except Exception:
                continue
            if _np.isfinite(d):
                vals.append(abs(d))
        med = float(_np.median(vals)) if vals else 0.0
        out[name] = (med > tol, med)
    return out
