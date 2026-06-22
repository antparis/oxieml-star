#!/usr/bin/env python3
"""Sequential weak values: prepare |psi>, weakly measure A (first) then B (second), post-select <phi|.
W_seq = <phi|B A|psi>/<phi|psi>. Question: is the geometric structure still a SUM of known 3-state
Pancharatnam-Berry phases, or an irreducible higher-order (4-point / non-abelian / order-dependent)
object? Guard: a polygon ALWAYS splits into triangles, so only an irreducible RESIDUE would be new.
NOTE: a first sandbox run reported match=False in the decomposition -- that was an OPERATOR-ORDER BUG
in the bra-ket chain (B A = sum_ij b_j a_i |j><j|i><i|), not a residue. Fixed here.
Run on Anthony's machine. Arbiter = this execution."""
import numpy as np
rng = np.random.default_rng(3)
dim=2
def rstate():
    s=rng.standard_normal(dim)+1j*rng.standard_normal(dim); return s/np.linalg.norm(s)
def rherm():
    M=rng.standard_normal((dim,dim))+1j*rng.standard_normal((dim,dim)); return (M+M.conj().T)/2
def seqwv(psi,phi,A,B):   # <phi| B A |psi> : A acts first, then B
    return (np.vdot(phi,B@A@psi))/(np.vdot(phi,psi))

print("="*78)
print("Sequential weak values: known sum of Berry phases, or irreducible higher-order object?")
print("="*78)

print("\n[1] order dependence (non-commutativity): W(A then B) vs W(B then A) when [A,B]!=0:")
for _ in range(4):
    psi,phi=rstate(),rstate(); A,B=rherm(),rherm()
    Wab=seqwv(psi,phi,A,B); Wba=seqwv(psi,phi,B,A)
    comm=np.linalg.norm(A@B-B@A)
    print(f"   W(A then B)={Wab:+.3f}   W(B then A)={Wba:+.3f}   |[A,B]|={comm:.2f}   order matters={not np.allclose(Wab,Wba)}")

print("\n[2] decomposition: W_seq = sum_ij b_j a_i <phi|j><j|i><i|psi>/<phi|psi> (4-state Bargmann terms):")
psi,phi=rstate(),rstate(); A,B=rherm(),rherm()
aval,avec=np.linalg.eigh(A); bval,bvec=np.linalg.eigh(B)
W_direct=seqwv(psi,phi,A,B)
W_decomp=sum(bval[j]*aval[i]*(np.vdot(phi,bvec[:,j])*np.vdot(bvec[:,j],avec[:,i])*np.vdot(avec[:,i],psi))/np.vdot(phi,psi)
             for j in range(dim) for i in range(dim))
print(f"   W_direct={W_direct:+.4f}   W_decomp={W_decomp:+.4f}   match={np.allclose(W_direct,W_decomp)}")
maxres=0.0
for _ in range(200):
    psi,phi=rstate(),rstate(); A,B=rherm(),rherm()
    aval,avec=np.linalg.eigh(A); bval,bvec=np.linalg.eigh(B)
    Wd=seqwv(psi,phi,A,B)
    Ws=sum(bval[j]*aval[i]*(np.vdot(phi,bvec[:,j])*np.vdot(bvec[:,j],avec[:,i])*np.vdot(avec[:,i],psi))/np.vdot(phi,psi)
           for j in range(dim) for i in range(dim))
    maxres=max(maxres,abs(Wd-Ws))
print(f"   residue over 200 cases: max|W_direct - 4-state decomp| = {maxres:.2e}")
print(f"   => {'NO residue: sequential WV IS a sum of 4-state Bargmann terms' if maxres<1e-9 else 'RESIDUE beyond the 4-state decomposition'}")

print("\n[3] is each 4-point geometric phase reducible to a sum of triangle (3-state) phases?")
def b4(a,b,c,d): return np.vdot(a,b)*np.vdot(b,c)*np.vdot(c,d)*np.vdot(d,a)
def b3(a,b,c): return np.vdot(a,b)*np.vdot(b,c)*np.vdot(c,a)
maxd=0.0
for _ in range(200):
    a,b,c,d=rstate(),rstate(),rstate(),rstate()
    D4=np.angle(b4(a,b,c,d)); tri=np.angle(b3(a,b,c))+np.angle(b3(a,c,d))
    maxd=max(maxd,abs(((D4-tri+np.pi)%(2*np.pi))-np.pi))
print(f"   max diff (4-point phase vs triangulation) over 200 cases = {maxd:.2e}")
print(f"   => {'4-point phase = sum of triangle phases (reducible, KNOWN)' if maxd<1e-9 else 'irreducible 4-point phase (NEW)'}")

print("\n"+"="*78)
print("VERDICT: order-dependence (non-commutativity) is REAL, but the sequential weak value is")
print("EXACTLY a sum of 4-state Bargmann terms (no residue), and each 4-point phase reduces to a")
print("sum of triangle (3-state Pancharatnam-Berry) phases. So sequential WV adds NO irreducible")
print("geometric object: still a sum of KNOWN Berry phases. Door CLOSED: capability, not discovery.")
print("Do not overclaim non-commutativity as 'new geometry'. (Earlier match=False was an operator-")
print("order bug, now fixed -- not a residue.)")
print("="*78)
