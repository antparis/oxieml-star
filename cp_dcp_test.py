#!/usr/bin/env python3
"""
cp_dcp_test.py -- delta_CP (Jarlskog J) on the Qu-Lu-Ding T' lepton model.

QUESTION (the only open neutrino door). On the REAL observables (masses/angles)
eml* is DECORATIVE: full_chi2_test.py re-run in-domain gives full chi2=0.91,
holo-only chi2=0.23, nonholo chi2=0.04 (FINDINGS_20260623b). But delta_CP was
never tested: every script keeps a dead placeholder dcp=1.15 and discards the
computed Jarlskog J. delta_CP is the ONLY natively-complex observable -> the one
place the navigation law allows a genuinely forced anti. Does cutting the
anti-holomorphic part (mode='holo') kill CP violation (J -> 0)?

CP-judge (one of the two tribunals): J = Im(U00 U11 conj(U01) conj(U10)) on the
PMNS U the model produces. Validated as a brick: J=0 at delta=0,pi; matches the
closed form c12 s12 c23 s23 c13^2 s13 sin(delta); rephasing-invariant.

DESIGN (self-contained; model functions copied verbatim from full_chi2_test.py
lines 7-64; one in-domain multistart scan per mode):
  full    = eml + eml*    (Y2pp = c_holo + c_nonh)   -> J_full     (each at its own best fit)
  holo    = eml only      (Y2pp = c_holo, eml* off)  -> J_holo
  nonholo = eml* only     (Y2pp = c_nonh, eml off)   -> J_nonholo
  + L2 double comparison at COMMON tau (read U_holo/U_nonholo at the FULL best-fit
    p) to isolate the structural effect of the cut from the tau re-fit.
  + NULL control: Re(tau)=0 (imaginary axis) -> J must -> 0 (CP-reader sanity).
  + ORTHOGONAL AXIS: sweep Re(tau) at the full best-fit (Im,g2,beta,gamma fixed).
    If J is ODD in Re(tau) with J(0)=0, the CP phase lives in Re(tau) i.e. in
    q=exp(2 pi i tau), present in BOTH eml and eml* -> eml* not the sole carrier.

L1 (documented limit, not removed). The charged-lepton matrix Me_b carries a
residual anti-holomorphic piece through the Maass forms Y0 (qb=exp(-2 pi i conj tau)),
which is ALWAYS present regardless of mode. So mode='holo' cuts eml* only in the
neutrino/Dirac sector (Y2pp -> MD), NOT everywhere. The test therefore probes the
necessity of eml* in MD, not a global removal of all anti from the model.

READING (printed conditionally below; NO hardcoded verdict):
  |J_holo| ~ |J_full| (same order, both != 0)  -> eml* DECORATIVE for delta_CP. Door closed.
  J_holo -> 0  while  J_full != 0               -> eml* CARRIES the CP phase. Narrow candidate,
                                                   to be re-tested against the gCP/tau confound.

CAVEAT (sealed). Single model T' -> at best INTERNAL necessity to this model,
never a proof about nature. At the "gCP NO" best fit all couplings are real, so
the only phase source is q=exp(2 pi i tau), present in BOTH eml and eml*: the prior
expectation is J robust to the cut (eml* decorative for CP).

AUTHORITY: this execution on Anthony's machine. No verdict is valid until run here.
Author: Anthony Monnerot, 2026.
"""
import numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp, sqrt, log, gammainc, euler, loggamma
mp.dps=20
def chi2c(m):
    r=m%3; return 1 if r==1 else (-1 if r==2 else 0)
def dchi2(N): return sum(chi2c(d) for d in range(1,N+1) if N%d==0)
def sigm1(N): return sum(mpf(1)/d for d in range(1,N+1) if N%d==0)
def eta(t):
    q=exp(2*pi*I*t); return exp(pi*I*t/12)*qp(q)
def series(q,c): return sum(mpf(x)*q**n for n,x in enumerate(c))
def Y3_w4(tau):
    q=exp(2*pi*I*tau)
    return [series(q,[1,-84,-756,-2028,-6132,-10584,-18252]),6*q**(mpf(1)/3)*series(q,[1,73,344,1134,2198,4681]),54*q**(mpf(2)/3)*series(q,[1,14,65,148,344,546])]
def base_doublet(tau):
    Y1=-3*sqrt(2)*eta(3*tau)**3/eta(tau); q=exp(2*pi*I*tau); Y2=1+6*sum(dchi2(n)*q**n for n in range(1,35)); return Y1,Y2
a0=euler+log(3)+log(4*pi)-6*loggamma(mpf(1)/3)+6*loggamma(mpf(2)/3)
def Y2pp(tau, mode):
    y=tau.imag; q=exp(2*pi*I*tau)
    c1_holo=-6*(q*log(3)+2*q**2*log(2)+2*q**3*log(3))
    c1_nonh=a0+log(y)-6*(gammainc(0,4*pi*y)/q+gammainc(0,12*pi*y)/q**3+gammainc(0,16*pi*y)/q**4)
    hc=[log(2),log(5),2*log(2),log(11),2*log(2),log(17),log(5)]
    c2_holo=-6*sqrt(2)*q**(mpf(2)/3)*sum(hc[n]*q**n for n in range(len(hc)))
    c2_nonh=-3*sqrt(2)*sum(dchi2(3*n+1)*q**(-(mpf(3*n+1)/3))*gammainc(0,(12*n+4)*pi*y/3) for n in range(8) if dchi2(3*n+1)!=0)
    if mode=='full':    return [c1_holo+c1_nonh, c2_holo+c2_nonh]
    if mode=='holo':    return [c1_holo, c2_holo]
    if mode=='nonholo': return [c1_nonh, c2_nonh]
def m2np(M,r,c): return np.array([[complex(M[i,j]) for j in range(c)] for i in range(r)])
def Me_b(tau,beta,gamma):
    q=exp(2*pi*I*tau)
    Y2t=[series(q,[1,12,36,12,84,72,36,96]),-6*q**(mpf(1)/3)*series(q,[1,7,8,18,14]),-18*q**(mpf(2)/3)*series(q,[1,2,5,4,8])]
    Y4t=Y3_w4(tau); y=tau.imag; qb=exp(-2*pi*I*tau.conjugate())
    Y01=-9*log(3)/(4*pi)+y+(9/pi)*sum((sigm1(n)-sigm1(3*n))*(q**n+qb**n) for n in range(1,18))
    Y02=(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(18))+(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(18))
    Y03=(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(18))+(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(18))
    Y0=[Y01,Y02,Y03]
    return mp.matrix([[Y0[2],Y0[1],Y0[0]],[beta*Y2t[2],beta*Y2t[1],beta*Y2t[0]],[gamma*Y4t[0],gamma*Y4t[2],gamma*Y4t[1]]])
# 7 observables (value, sigma); charged ratios at 1%. order: s12,s13,s23,dmr,dcp,me/mmu,mmu/mtau
TGT=[(0.308,0.012),(0.02215,0.00056),(0.470,0.015),(0.02981,0.0008),(1.15,0.20),(0.004737,0.0000474),(0.05882,0.00059)]
def observables(p,mode):
    rt,it,g2,beta,gamma=p; tau=mpc(rt,it); g1=mpf(1); gg2=mpf(g2)
    Men=m2np(Me_b(tau,mpf(beta),mpf(gamma)),3,3)
    Y4t=Y3_w4(tau); Y1b,Y2b=base_doublet(tau); Yh=[Y1b,Y2b]; Yp=Y2pp(tau,mode)
    MN=mp.matrix([[-Y4t[1],Y4t[2]/sqrt(2)],[Y4t[2]/sqrt(2),Y4t[0]]])
    MD=mp.matrix([[g1*Yp[1],sqrt(2)*gg2*Yh[0],-sqrt(2)*g1*Yp[0]-gg2*Yh[1]],[g1*Yp[0]-sqrt(2)*gg2*Yh[1],sqrt(2)*g1*Yp[1],-gg2*Yh[0]]])
    Mnu=m2np(-(MD.T*(MN**-1)*MD),3,3)
    we,Ue=np.linalg.eigh(Men.conj().T@Men); me=np.sqrt(np.abs(np.sort(we))); Ue=Ue[:,np.argsort(we)]
    wn,Vn=np.linalg.eigh(Mnu@Mnu.conj().T); Vn=Vn[:,np.argsort(wn)]
    U=Ue.conj().T@Vn; mn=np.sqrt(np.abs(np.sort(wn)))
    s12=np.sin(np.arctan2(abs(U[0,1]),abs(U[0,0])))**2
    s13=np.sin(np.arcsin(min(abs(U[0,2]),1)))**2
    s23=np.sin(np.arctan2(abs(U[1,2]),abs(U[2,2])))**2
    dmr=(mn[1]**2-mn[0]**2)/(mn[2]**2-mn[0]**2)
    dcp=1.15  # placeholder kept for the chi2 (J read separately, not fitted)
    return [s12,s13,s23,dmr,dcp,me[0]/me[1],me[1]/me[2]]
def chi2f(p,mode):
    rt,it=p[0],p[1]
    if it<=0 or (rt*rt+it*it)<1.0 or abs(rt)>0.5:
        return 1e6+1e4*((1.0-(rt*rt+it*it)) if (rt*rt+it*it)<1 else 0)+1e4*(max(0,abs(rt)-0.5))+1e4*max(0,-it)
    try:
        o=observables(p,mode)
        c=sum(((o[i]-TGT[i][0])/TGT[i][1])**2 for i in range(7))
        return c if np.isfinite(c) else 1e7
    except Exception: return 1e7
def scan(mode,n=20):
    rng=np.random.default_rng(3); best=1e9; bp=None
    seeds=[(-0.0378,1.090,0.149,17.70,284.6)]+[(rng.uniform(-0.5,0.5),rng.uniform(1.0,1.5),rng.uniform(-3,3),rng.uniform(5,30),rng.uniform(100,500)) for _ in range(n)]
    for s in seeds:
        r=minimize(chi2f,s,args=(mode,),method='Nelder-Mead',options={'xatol':1e-4,'fatol':1e-3,'maxiter':4000})
        if r.fun<best: best=r.fun; bp=r.x
    return best,bp

# ---- CP-reader: extract PMNS U (verbatim from observables) + Jarlskog J ----
def get_U(p,mode):
    rt,it,g2,beta,gamma=p; tau=mpc(rt,it); g1=mpf(1); gg2=mpf(g2)
    Men=m2np(Me_b(tau,mpf(beta),mpf(gamma)),3,3)
    Y4t=Y3_w4(tau); Y1b,Y2b=base_doublet(tau); Yh=[Y1b,Y2b]; Yp=Y2pp(tau,mode)
    MN=mp.matrix([[-Y4t[1],Y4t[2]/sqrt(2)],[Y4t[2]/sqrt(2),Y4t[0]]])
    MD=mp.matrix([[g1*Yp[1],sqrt(2)*gg2*Yh[0],-sqrt(2)*g1*Yp[0]-gg2*Yh[1]],[g1*Yp[0]-sqrt(2)*gg2*Yh[1],sqrt(2)*g1*Yp[1],-gg2*Yh[0]]])
    Mnu=m2np(-(MD.T*(MN**-1)*MD),3,3)
    we,Ue=np.linalg.eigh(Men.conj().T@Men); Ue=Ue[:,np.argsort(we)]
    wn,Vn=np.linalg.eigh(Mnu@Mnu.conj().T); Vn=Vn[:,np.argsort(wn)]
    U=Ue.conj().T@Vn; mn=np.sqrt(np.abs(np.sort(wn)))
    return U,mn
def jarlskog(U):
    return float(np.imag(U[0,0]*U[1,1]*np.conj(U[0,1])*np.conj(U[1,0])))

if __name__=='__main__':
    print("="*78)
    print("delta_CP / Jarlskog test on the T' lepton model -- two tribunals (CP-judge)")
    print("Authority: THIS execution. No verdict valid until run here.")
    print("="*78)

    # 1) one in-domain scan per mode; read J at each mode's OWN best fit
    res={}
    for mode in ['full','holo','nonholo']:
        c,p=scan(mode)
        U,mn=get_U(p,mode); J=jarlskog(U)
        res[mode]=(c,p,J,U)
        print(f"--- {mode:8s} chi2={c:7.2f}  tau={p[0]:+.4f}{p[1]:+.4f}i  J={J:+.6e}")
    Jf=res['full'][2]; Jh=res['holo'][2]; Jn=res['nonholo'][2]

    # 2) L2 double comparison at COMMON tau = full best-fit (isolate cut from tau re-fit)
    pfull=res['full'][1]
    print("\n[L2] same tau (full best-fit), modes swapped on Y2pp:")
    for mode in ['full','holo','nonholo']:
        U,_=get_U(pfull,mode); print(f"     {mode:8s} J={jarlskog(U):+.6e}")

    # 3) NULL control: Re(tau)=0 -> J must -> 0
    print("\n[NULL] Re(tau)=0 (imaginary axis), full best-fit otherwise -> J must -> 0:")
    p0=(0.0,pfull[1],pfull[2],pfull[3],pfull[4])
    U0,_=get_U(p0,'full'); print(f"     J(Re tau=0)={jarlskog(U0):+.3e}")

    # 4) ORTHOGONAL AXIS: sweep Re(tau) at full best-fit; expect ODD in Re(tau), J(0)=0
    print("\n[ORTHOGONAL AXIS] sweep Re(tau) at fixed Im/g2/beta/gamma (full best-fit):")
    rts=[-0.40,-0.30,-0.15,-0.05,0.0,0.05,0.15,0.30,0.40]; Js={}
    for rt in rts:
        U,_=get_U((rt,pfull[1],pfull[2],pfull[3],pfull[4]),'full'); Js[rt]=jarlskog(U)
        print(f"     Re(tau)={rt:+.2f}  J={Js[rt]:+.6e}")
    odd=all(np.isclose(Js[rt],-Js[-rt],atol=1e-9,rtol=1e-3) for rt in [0.05,0.15,0.30,0.40])
    print(f"     ODD in Re(tau) and J(0)~0 ? {odd and abs(Js[0.0])<1e-9}")

    # 5) READING (conditional, no hardcoded verdict)
    print("\n"+"-"*78)
    same_order = (Jh!=0) and (abs(Jh)>=0.1*abs(Jf)) and (abs(Jh)<=10*abs(Jf))
    holo_kills = (abs(Jf)>1e-6) and (abs(Jh)<0.05*abs(Jf))
    print(f"READING: J_full={Jf:+.3e}  J_holo={Jh:+.3e}  J_nonholo={Jn:+.3e}")
    if holo_kills:
        print("  -> cutting eml* drives J->0 while J_full!=0: eml* CARRIES the CP phase.")
        print("     NARROW CANDIDATE -- re-test against gCP/tau confound before any claim.")
    elif same_order:
        print("  -> |J_holo| ~ |J_full|: cutting eml* does NOT kill J. eml* DECORATIVE for delta_CP.")
        print("     Consistent with the navigation law and the prior auditor expectation.")
    else:
        print("  -> intermediate: J changes but does not vanish. Inspect L2 / orthogonal-axis output.")
    print("  STATUS: [HEURISTIC] from this single model; not a statement about nature.")
    print("-"*78)
