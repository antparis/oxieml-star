#!/usr/bin/env python3
"""CP-judge Stage 1: rephasing-invariant CP detector (Jarlskog + commutator).
Validates on known cases before any Delta(54) claim. This is the CALIBRATION
of the CP layer -- distinct from the Wirtinger judge verify_exact.py.
Routing rule: CP physicality is decided here (rephasing-invariant), NOT by d/dzbar.
"""
import sympy as sp
import numpy as np

def trig_reduce(expr, pairs):
    for c, s in pairs:
        expr = expr.subs(c**2, 1 - s**2)
    return sp.simplify(expr)

# --- standard PMNS/CKM parametrization (PDG) ---
s12,s13,s23,c12,c13,c23,delta = sp.symbols('s12 s13 s23 c12 c13 c23 delta', real=True)
U = sp.Matrix([
 [ c12*c13, s12*c13, s13*sp.exp(-sp.I*delta)],
 [-s12*c23 - c12*s23*s13*sp.exp(sp.I*delta), c12*c23 - s12*s23*s13*sp.exp(sp.I*delta), s23*c13],
 [ s12*s23 - c12*c23*s13*sp.exp(sp.I*delta), -c12*s23 - s12*c23*s13*sp.exp(sp.I*delta), c23*c13],
])
PAIRS = [(c12,s12),(c13,s13),(c23,s23)]

def test1_jarlskog():
    J = sp.im(U[0,0]*U[1,1]*sp.conjugate(U[0,1])*sp.conjugate(U[1,0]))
    J = trig_reduce(J, PAIRS)
    J0 = sp.simplify(J.subs(delta, 0))
    print("TEST 1 Jarlskog J =", J)
    print("        J(delta=0) =", J0, "(expect 0 = CP conserved)")
    return J0 == 0

def test2_two_generations():
    th, ph = sp.symbols('theta phi', real=True)
    U2 = sp.Matrix([[sp.cos(th), sp.sin(th)*sp.exp(sp.I*ph)],
                    [-sp.sin(th)*sp.exp(-sp.I*ph), sp.cos(th)]])
    m1,m2,n1,n2 = sp.symbols('m1 m2 n1 n2', positive=True)
    Mu = sp.diag(m1, m2)
    Md = U2 * sp.diag(n1, n2) * U2.conjugate().T
    Hu = Mu*Mu.conjugate().T; Hd = Md*Md.conjugate().T
    C = Hu*Hd - Hd*Hu
    tr = sp.simplify((C**3).trace())
    print("TEST 2 two-gen Tr[Hu,Hd]^3 =", tr, "(expect 0 = phase removable)")
    return tr == 0

def test3_commutator_3gen():
    vals = {s12:0.55, c12:sp.sqrt(1-0.55**2), s13:0.15, c13:sp.sqrt(1-0.15**2),
            s23:0.64, c23:sp.sqrt(1-0.64**2)}
    mu_,mc_,mt_,md_,ms_,mb_ = 0.002,1.27,173.0,0.005,0.1,4.18
    def im_comm(dv):
        Un = U.subs(vals).subs(delta, dv)
        Un = np.array([[complex(x) for x in row] for row in Un.tolist()], dtype=complex)
        Mu = np.diag([mu_,mc_,mt_]).astype(complex)
        Md = Un @ np.diag([md_,ms_,mb_]).astype(complex) @ Un.conj().T
        Hu = Mu@Mu.conj().T; Hd = Md@Md.conj().T
        C = Hu@Hd - Hd@Hu
        return float(np.trace(C@C@C).imag)
    a, b = im_comm(1.0), im_comm(0.0)
    print("TEST 3 Im Tr[Hu,Hd]^3: d=1.0 ->", f"{a:.3e}", "(!=0);  d=0 ->", f"{b:.3e}", "(0)")
    return abs(a) > 1e3 and abs(b) < 1e-6

if __name__ == "__main__":
    print("="*60)
    print("CP-JUDGE STAGE 1 -- calibration on known cases")
    print("="*60)
    r1 = test1_jarlskog()
    r2 = test2_two_generations()
    r3 = test3_commutator_3gen()
    print("-"*60)
    print("RESULTS:")
    print("  Test 1 (Jarlskog J->0 at delta=0)   :", "PASS" if r1 else "FAIL")
    print("  Test 2 (2-gen always removable)      :", "PASS" if r2 else "FAIL")
    print("  Test 3 (commutator forced iff delta) :", "PASS" if r3 else "FAIL")
    print("-"*60)
    print("STAGE 1", "VALIDATED" if (r1 and r2 and r3) else "FAILED -- fix before Stage 2")
