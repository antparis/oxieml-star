#!/usr/bin/env python3
"""
indefinite_theta_grid.py -- Apply the three-operator grid (eml / eml* / eml0) to the
INDEFINITE theta (mixed-signature) Zwegers completion, to confirm whether the mixed
signature changes the grid class versus the unary case (order-3 f(q)).

Indefinite theta: quadratic form of mixed signature -> raw sum diverges -> Zwegers
regularizes sgn(...) -> erf(sqrt(2y)...) INSIDE the sum (vs unary where the y-term sits
beside). The error factor erf(sqrt(y)) depends on the REAL y = Im(tau). Question: does this
internal real factor change the class, or is the "real factor modulates, not reduces" motif
universal across the whole mock theta family?

Only light forms (the ones that finished in sandbox); the heavy full combination that timed
out is omitted -- not needed for the verdict.

Run from ~/Desktop/oxieml-star/ :  python3 indefinite_theta_grid.py
"""
import sympy as sp
from judge_v2 import z, zbar, certify_1field, full_conj

I = sp.I


def eml(expr):
    return sp.simplify(sp.diff(sp.expand(expr), zbar)) == 0


def eml_star(expr):
    v, _ = certify_1field(expr)
    return v


def eml_zero(expr):
    expr = sp.expand(expr)
    if sp.simplify(sp.diff(expr, z)) == 0 and sp.simplify(sp.diff(expr, zbar)) == 0:
        return "constant"
    mod2 = sp.simplify(expr * full_conj(expr))
    cst = (sp.simplify(sp.diff(mod2, z)) == 0 and sp.simplify(sp.diff(mod2, zbar)) == 0)
    return "pure-phase" if cst else "not-pure-phase"


def grid(name, f):
    e0 = "holo" if eml(f) else "-"
    print(f"  {name:<46} eml:{e0:<6} eml*:{eml_star(f):<18} eml0:{eml_zero(f)}", flush=True)


y = (z - zbar)/(2*I)
q = sp.exp(2*sp.pi*I*z)
erf = sp.erf

print("=" * 92)
print("INDEFINITE THETA (mixed signature) -- three-operator grid")
print("=" * 92)

print("\n[RAW holomorphic, before completion]")
grid("indef raw ~ q + q^3 - q^(-1) (holo in q)", q + q**3 - q**(-1))

print("\n[COMPLETION: sgn -> erf(sqrt(y)...), real erf factor inside the sum]")
grid("indef completed: erf(sqrt y) q + erf(2 sqrt y) q^(-1)", erf(sp.sqrt(y))*q + erf(2*sp.sqrt(y))*q**(-1))

print("\n[CONTROLS]")
grid("erf(sqrt y) alone (regularization factor)", erf(sp.sqrt(y)))
grid("erf(sqrt y) * q^(-1)", erf(sp.sqrt(y))*q**(-1))
grid("erf(sqrt y) * exp(-2pi i zbar) [erf x anti]", erf(sp.sqrt(y))*sp.exp(-2*sp.pi*I*zbar))

print("\n[COMPARISON anchor: unary order-3 Zwegers form]")
grid("unary: y^(-1/2) * conj(g3)", y**(-sp.Rational(1, 2))*sp.exp(-2*sp.pi*I*zbar))

print("\n" + "=" * 92)
print("READING: if the indefinite completion gives the SAME grid class as the unary anchor")
print("(eml* anti, eml0 not-pure-phase) while erf(sqrt y) alone is real-trapped, then the")
print("'real factor modulates not reduces' motif is UNIVERSAL across the mock theta family")
print("(unary AND indefinite). Mixed signature does NOT create a new grid class.")
