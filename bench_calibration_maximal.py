#!/usr/bin/env python3
"""Maximal calibration bench: every historical candidate re-judged, with the CORRECTED real-trap
test. A field is REAL-TRAPPED (the SPARC trap) iff f == conj(f) under FULL conjugation (z<->zbar
AND i->-i). Three families with required verdicts. This bench REVEALED that judge_v2 lacked the
mirror test and mis-flagged z+zbar, log|z|^2, Im(z) as ANTI -- a real SPARC-type blind spot now fixed.
Run on Anthony's machine. Arbiter = this execution."""
import sympy as sp
z, zbar = sp.symbols("z zbar")

def full_conj(expr):
    tmp = sp.Symbol("__tmp__")
    e = expr.subs(sp.I, tmp)
    e = e.subs({z: zbar, zbar: z}, simultaneous=True)
    e = e.subs(tmp, -sp.I)
    return e

def classify(expr):
    expr = sp.expand(expr)
    d = sp.simplify(sp.diff(expr, zbar))
    if d == 0:
        return "HOLO"
    is_real = sp.simplify(expr - full_conj(expr)) == 0
    return "REAL-TRAP" if is_real else "ANTI"

cases = [
    ("vortex_N1  log(zbar)",        sp.log(zbar),                          "ANTI"),
    ("loc5_mix   z^3 + zbar^2",     z**3 + zbar**2,                        "ANTI"),
    ("loc6_exp   exp(zbar)",        sp.exp(zbar),                          "ANTI"),
    ("Kirsch     z/zbar^2 + 1/zbar",sp.Rational(13,10)*z/zbar**2 + sp.Rational(65,100)/zbar, "ANTI"),
    ("Tricorn    conj(z)^2 + c",    zbar**2 + sp.Rational(1,4),            "ANTI"),
    ("Mandelbrot z^2 + c",          z**2 + sp.Rational(1,4),               "HOLO"),
    ("holo ctrl  exp(z)",           sp.exp(z),                             "HOLO"),
    ("holo ctrl  1/z",              1/z,                                   "HOLO"),
    ("holo ctrl  z^3+z",            z**3 + z,                              "HOLO"),
    ("trap |z|^2 = z*zbar",         z*zbar,                                "REAL-TRAP"),
    ("trap z + zbar",               z + zbar,                              "REAL-TRAP"),
    ("trap log|z|^2",               sp.log(z)+sp.log(zbar),                "REAL-TRAP"),
    ("trap Re=(z+zbar)/2",          (z+zbar)/2,                            "REAL-TRAP"),
    ("trap Im=(z-zbar)/2i",         (z-zbar)/(2*sp.I),                     "REAL-TRAP"),
    ("trap |z|^4",                  (z*zbar)**2,                           "REAL-TRAP"),
    ("trap Re(z^2)",                (z**2+zbar**2)/2,                      "REAL-TRAP"),
    ("anti chiral z + 0.3*zbar",    z + sp.Rational(3,10)*zbar,            "ANTI"),
    ("anti i*zbar (not real)",      sp.I*zbar,                             "ANTI"),
]
print("="*84)
print("MAXIMAL CALIBRATION BENCH (corrected: full conjugation z<->zbar AND i->-i)")
print("="*84)
print(f"\n{'case':<32}{'-> classified':<16}{'required':<12}{'OK?'}")
print("-"*72)
allok=True
for name, expr, req in cases:
    cls = classify(expr); ok = (cls==req); allok = allok and ok
    print(f"{name:<32}{cls:<16}{req:<12}{'OK' if ok else 'FAIL!!'}")
print("\n"+"="*84)
print(f"ALL CORRECT: {allok}")
print("If True: judge_v2 needs the mirror test (full_conj + REAL-TRAP) added -- the bench found it missing.")
print("="*84)
