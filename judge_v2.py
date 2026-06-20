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
    if f = h(z)*m(z*zbar), then zbar*dlog(f)/dzbar = (z*zbar)*m'/m is REAL and depends on the
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
        return bool(L_real and prod_only)
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
