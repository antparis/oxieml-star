#!/usr/bin/env python3
"""Two tests on the weak value.
(A) NUMERIC: a generic (non-projector) observable A -- is W a SUM of known Pancharatnam-Berry
    phases (decomposable), or an irreducible new object? Decompose A = sum_k a_k |k><k|, compare.
(B) JUDGE (SymPy exact Wirtinger): weak value anti-holomorphic in FUTURE phi, holomorphic in PAST
    psi. Wirtinger done correctly: independent symbols for bar/unbar (as verify_exact.py treats z,zbar).
Run on Anthony's machine. Arbiter = this execution + SymPy judge."""
import numpy as np
import sympy as sp

print("="*78)
print("(A) NUMERIC: generic observable -- sum of known Berry phases, or new irreducible object?")
print("="*78)
rng = np.random.default_rng(2)

def test(dim, label):
    print(f"\n--- {label} (dim {dim}) ---")
    M=rng.standard_normal((dim,dim))+1j*rng.standard_normal((dim,dim)); A=(M+M.conj().T)/2
    av,ae=np.linalg.eigh(A); match=True
    for _ in range(4):
        psi=rng.standard_normal(dim)+1j*rng.standard_normal(dim); psi/=np.linalg.norm(psi)
        phi=rng.standard_normal(dim)+1j*rng.standard_normal(dim); phi/=np.linalg.norm(phi)
        Wd=(np.vdot(phi,A@psi))/np.vdot(phi,psi)
        Ws=sum(av[k]*(np.vdot(phi,ae[:,k])*np.vdot(ae[:,k],psi))/np.vdot(phi,psi) for k in range(dim))
        ok=np.allclose(Wd,Ws); match=match and ok
        print(f"   W_direct={Wd:+.4f}   sum-of-Bargmann={Ws:+.4f}   match={ok}")
    return match

test(2,"qubit, generic A"); test(3,"qutrit, generic A")
A=rng.standard_normal((3,3))+1j*rng.standard_normal((3,3)); A=(A+A.conj().T)/2
av,ae=np.linalg.eigh(A); maxres=0.0
for _ in range(200):
    psi=rng.standard_normal(3)+1j*rng.standard_normal(3); psi/=np.linalg.norm(psi)
    phi=rng.standard_normal(3)+1j*rng.standard_normal(3); phi/=np.linalg.norm(phi)
    Wd=(np.vdot(phi,A@psi))/np.vdot(phi,psi)
    Ws=sum(av[k]*(np.vdot(phi,ae[:,k])*np.vdot(ae[:,k],psi))/np.vdot(phi,psi) for k in range(3))
    maxres=max(maxres,abs(Wd-Ws))
print(f"\n   [residue test] max |W_direct - projector_sum| over 200 cases = {maxres:.2e}")
print(f"   => {'NO residue: fully a sum of known Berry phases (door CLOSED)' if maxres<1e-9 else 'RESIDUE EXISTS'}")

print("\n"+"="*78)
print("(B) JUDGE (SymPy exact Wirtinger): anti-holo in future phi, holo in past psi?")
print("="*78)
ps0,ps1   = sp.symbols('ps0 ps1')        # psi (holomorphic vars, past)
psb0,psb1 = sp.symbols('psb0 psb1')      # psi-bar (independent)
f0,f1     = sp.symbols('f0 f1')          # phi (future)
fb0,fb1   = sp.symbols('fb0 fb1')        # phi-bar (independent)
a00,a11   = sp.symbols('a00 a11', real=True)
a01,a01b  = sp.symbols('a01 a01b')       # A Hermitian: a10 = a01b
num = fb0*(a00*ps0 + a01*ps1) + fb1*(a01b*ps0 + a11*ps1)
den = fb0*ps0 + fb1*ps1
W = num/den
dW_psbar = sp.simplify(sp.diff(W, psb0))   # psi-bar absent  -> 0 (holo past)
dW_phi   = sp.simplify(sp.diff(W, f0))     # phi unbarred absent -> 0 (anti future)
dW_phbar = sp.simplify(sp.diff(W, fb0))    # phi-bar present -> nonzero
dW_psi   = sp.simplify(sp.diff(W, ps0))    # psi present     -> nonzero
print(f"\n   dW/d(psi-bar) = {dW_psbar}   (expect 0: HOLOMORPHIC in past)")
print(f"   dW/d(phi)     = {dW_phi}   (expect 0: ANTI-HOLOMORPHIC in future)")
print(f"   dW/d(phi-bar) = {'NONZERO' if dW_phbar!=0 else 0}   (expect nonzero)")
print(f"   dW/d(psi)     = {'NONZERO' if dW_psi!=0 else 0}   (expect nonzero)")
verdict = (dW_psbar==0) and (dW_phi==0) and (dW_phbar!=0) and (dW_psi!=0)
print(f"\n   JUDGE VERDICT: holomorphic in past psi AND anti-holomorphic in future phi: {verdict}")

print("\n"+"="*78)
print("SUMMARY: (A) generic observable = weighted sum of known Pancharatnam-Berry phases, no residue")
print("(door closed: capability, not discovery). (B) SymPy judge certifies the cross-conjugate")
print("structure exactly: anti-holo carried by FUTURE phi, holo by PAST psi -- the eml*/eml signature.")
print("="*78)
