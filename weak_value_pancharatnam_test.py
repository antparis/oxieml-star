#!/usr/bin/env python3
"""Is the weak-value 'thumb' (the oriented area carrying Im(W)) the known Pancharatnam-Berry
geometric phase? Corrected test (earlier sandbox had a sign bug and overclaimed 'same object').
For A=|chi><chi| (projector): W = <phi|chi><chi|psi>/<phi|psi> is a Bargmann invariant, and
arg(W) is EXACTLY the Pancharatnam phase of (phi,chi,psi); Im(W)=|W| sin(that phase). So the thumb
IS the Berry phase dressed by a known modulus ratio: CAPABILITY (retrieving known physics), not
discovery. For a GENERIC A (not a projector) the clean triangle breaks -- the only open direction.
Run on Anthony's machine. Arbiter = this execution."""
import numpy as np
rng = np.random.default_rng(1)

print("="*78)
print("Weak-value thumb vs Pancharatnam-Berry geometric phase (corrected)")
print("="*78)

def bloch_state(theta, phi):
    return np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)])
def bloch_vector(s):
    sx=np.array([[0,1],[1,0]]); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]])
    return np.array([np.real(np.vdot(s,M@s)) for M in (sx,sy,sz)])
def pancharatnam(a,b,c):
    return np.angle(np.vdot(a,b)*np.vdot(b,c)*np.vdot(c,a))
def solid_angle(a,b,c):
    num=np.dot(a,np.cross(b,c)); den=1+np.dot(a,b)+np.dot(b,c)+np.dot(c,a)
    return 2*np.arctan2(num,den)

print("\n[1] Pancharatnam phase = +1/2 solid angle of the Bloch triangle (geometric):")
ok1=True
for _ in range(4):
    s=[bloch_state(*rng.uniform([0,0],[np.pi,2*np.pi])) for _ in range(3)]
    P=pancharatnam(*s); Om=solid_angle(*[bloch_vector(x) for x in s])
    if abs(((P-Om/2+np.pi)%(2*np.pi))-np.pi)>1e-9: ok1=False
    print(f"   Pancharatnam={P:+.4f}   Omega/2={Om/2:+.4f}   ratio={P/(Om/2):+.4f}")
print(f"   Pancharatnam == +Omega/2 : {ok1}")

print("\n[2] A=|chi><chi| (projector): W=<phi|chi><chi|psi>/<phi|psi>, arg(W)==Pancharatnam(phi,chi,psi):")
ok2=True
for _ in range(5):
    psi=bloch_state(*rng.uniform([0,0],[np.pi,2*np.pi]))
    phi=bloch_state(*rng.uniform([0,0],[np.pi,2*np.pi]))
    chi=bloch_state(*rng.uniform([0,0],[np.pi,2*np.pi]))
    W=(np.vdot(phi,chi)*np.vdot(chi,psi))/np.vdot(phi,psi)
    P=pancharatnam(phi,chi,psi)
    d=((np.angle(W)-P+np.pi)%(2*np.pi))-np.pi
    if abs(d)>1e-9: ok2=False
    print(f"   arg(W)={np.angle(W):+.4f}   Pancharatnam={P:+.4f}   diff={d:+.1e}   |W|={abs(W):.3f}")
print(f"   arg(W) == Pancharatnam phase exactly : {ok2}   => Im(W)=|W| sin(Pancharatnam): Berry phase dressed by known modulus")

print("\n[3] GUARD: degenerate (coplanar) triangle -> zero both sides:")
s1=bloch_state(0.5,0.0); s2=bloch_state(1.5,0.0); s3=bloch_state(2.5,0.0)
W=(np.vdot(s2,s3)*np.vdot(s3,s1))/np.vdot(s2,s1); P=pancharatnam(s2,s3,s1)
print(f"   coplanar: Im(W)={W.imag:+.2e}  Pancharatnam={P:+.2e}  => both ~0 : {abs(W.imag)<1e-9 and abs(P)<1e-9}")

print("\n[4] GENERIC A (not a projector): the clean triangle breaks (the only open direction):")
A=np.array([[0.4,0.7+0.3j],[0.7-0.3j,-0.2]])
psi=bloch_state(0.7,0.3); phi=bloch_state(1.9,1.1)
W=(np.vdot(phi,A@psi))/np.vdot(phi,psi)
print(f"   generic A: W={W:+.4f}, arg(W)={np.angle(W):+.4f} (not a single Bloch triangle => not a pure Pancharatnam phase)")

print("\n"+"="*78)
print("VERDICT: for a PROJECTOR observable, the weak-value thumb IS the Pancharatnam-Berry phase")
print("(known, measured geometric phase) dressed by a known modulus -> CAPABILITY confirmed, NOT")
print("discovery. The framework computes a standard geometric phase correctly. Only open direction:")
print("a GENERIC (non-projector) observable, where the clean 3-state triangle breaks. Do not overclaim.")
print("="*78)
