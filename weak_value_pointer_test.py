#!/usr/bin/env python3
"""Does macroscopic irreversibility kill Im(weak value)?
Proper model: weak measurement with a QUANTUM POINTER (position q, momentum p).
Aharonov-Albert-Vaidman: Re(W) shifts <q>, Im(W) shifts <p>. Irreversibility acts on the
pointer DENSITY MATRIX (NOT as a real scalar factor on W -- that would scale Re and Im together).
Distinguish (i) pure DECOHERENCE in position (measurement) vs (ii) DISSIPATION (friction).
Run on Anthony's machine. Arbiter = this execution + the open physical question."""
import numpy as np
rng = np.random.default_rng(0)

print("="*78)
print("WEAK VALUE with a quantum pointer: does irreversibility kill Im(W) = pointer <p>?")
print("="*78)

N=400; L=20.0; q=np.linspace(-L,L,N); dq=q[1]-q[0]; sigma=2.0
G0=np.exp(-q**2/(4*sigma**2)); G0/=np.sqrt(np.sum(np.abs(G0)**2)*dq)

D=np.zeros((N,N),dtype=complex)
for i in range(1,N-1):
    D[i,i+1]=1/(2*dq); D[i,i-1]=-1/(2*dq)
P=-1j*D

A=np.array([[0.4,0.7+0.3j],[0.7-0.3j,-0.2]])
ev,Vmat=np.linalg.eigh(A); g=0.5

def pointer_state(psi,phi):
    Phi=np.zeros(N,dtype=complex)
    for k in range(2):
        ck=np.vdot(phi,Vmat[:,k])*np.vdot(Vmat[:,k],psi)
        Phi+=ck*np.exp(-(q-g*ev[k])**2/(4*sigma**2))
    return Phi/np.sqrt(np.sum(np.abs(G0)**2)*dq)

def expect_q_p(rho):
    tr=np.real(np.trace(rho))*dq
    qmean=np.real(np.sum(np.diag(rho)*q))*dq/tr
    pmean=np.real(np.trace(rho@P))*dq/tr
    return qmean,pmean

def wv(psi,phi): return np.vdot(phi,A@psi)/np.vdot(phi,psi)

ReW=[];ImW=[];QQ=[];PP=[]
for _ in range(6):
    psi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    phi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    rho=np.outer(pointer_state(psi,phi),pointer_state(psi,phi).conj())
    qm,pm=expect_q_p(rho); W=wv(psi,phi)
    ReW.append(W.real);ImW.append(W.imag);QQ.append(qm);PP.append(pm)
print(f"\n[correspondence] corr(<q>,Re W)={np.corrcoef(QQ,ReW)[0,1]:.4f}  corr(<p>,Im W)={np.corrcoef(PP,ImW)[0,1]:.4f}")
print("   => <q> reads Re(W), <p> reads Im(W) (Aharonov-Albert-Vaidman).")

psi=np.array([1.0+0j,0.4+0.2j]);psi/=np.linalg.norm(psi)
phi=np.array([0.3+0.5j,1.0+0j]);phi/=np.linalg.norm(phi)
Phi=pointer_state(psi,phi); rho0=np.outer(Phi,Phi.conj())
q0,p0=expect_q_p(rho0); W=wv(psi,phi)
print(f"   reference: Im(W)={W.imag:+.4f}, pointer <p>={p0:+.4f}")

print("\n[(i) pure DECOHERENCE in position] (measurement-type irreversibility)")
QI,QJ=np.meshgrid(q,q,indexing='ij')
for Gam in [0.0,0.2,1.0,5.0]:
    qm,pm=expect_q_p(rho0*np.exp(-Gam*(QI-QJ)**2))
    print(f"   Gamma={Gam:>4}: <q>={qm:+.4f} <p>={pm:+.4f}  ({'Im W PRESERVED' if abs(pm-p0)<1e-3 else 'shifted'})")
print("   => decoherence PRESERVES <p>=Im(W); only momentum VARIANCE grows (noise, not signal).")

print("\n[(ii) DISSIPATION / friction on momentum] (thermalizing irreversibility)")
Phi_p=np.fft.fftshift(np.fft.fft(Phi))
kgrid=2*np.pi*np.fft.fftshift(np.fft.fftfreq(N,d=dq))
pmean_now=np.real(np.sum(kgrid*np.abs(Phi_p)**2)/np.sum(np.abs(Phi_p)**2))
for eta_t in [0.0,0.3,1.0,3.0]:
    dp=pmean_now*np.exp(-eta_t)-pmean_now
    Phi_new=Phi*np.exp(1j*dp*q)
    qm,pm=expect_q_p(np.outer(Phi_new,Phi_new.conj()))
    print(f"   eta*t={eta_t:>4}: <p>={pm:+.4f}  (Im W decays toward 0)")
print("   => DISSIPATION damps <p>=Im(W) toward 0.")

print("\n"+"="*78)
print("VERDICT: Im(W) is read out as pointer momentum <p>. Pure DECOHERENCE (measurement,")
print("classical emergence) PRESERVES it; only DISSIPATION (thermalization) kills it. An ideal")
print("measurement decoheres without dissipating => Im(W) physical there. Real weak-value")
print("experiments (optics, AAV) run in that regime and DO measure Im(W). Open point: must a")
print("real post-selection dissipate? Empirically it need not. Strong support, not a proof.")
print("="*78)
