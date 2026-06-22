#!/usr/bin/env python3
"""Finish the robust CP test: HOLO-ONLY only (full already done: chi2=2.42 both signs).
30 starts x both J signs. If holo reaches low chi2 for either sign => sign was convention
artifact => CP NOT necessary. If high for both => anti-holo needed for CP.
Run on Anthony's machine."""
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
    hc=[log(2),log(5),2*log(2),log(11),2*log(2),log(17),log(5)]
    c2_holo=-6*sqrt(2)*q**(mpf(2)/3)*sum(hc[n]*q**n for n in range(len(hc)))
    if mode=='holo':    return [c1_holo, c2_holo]
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
def jarlskog(U):
    return np.imag(U[0,0]*U[1,1]*np.conj(U[0,1])*np.conj(U[1,0]))
def model(p):
    rt,it,g2r,g2i,beta,gamma=p; tau=mpc(rt,it); g1=mpf(1); gg2=mpc(g2r,g2i)
    Men=m2np(Me_b(tau,mpf(beta),mpf(gamma)),3,3)
    Y4t=Y3_w4(tau); Y1b,Y2b=base_doublet(tau); Yh=[Y1b,Y2b]; Yp=Y2pp(tau,'holo')
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
    return [s12,s13,s23,dmr,me[0]/me[1],me[1]/me[2]], jarlskog(U)
TGT=[(0.308,0.012),(0.02215,0.00056),(0.470,0.015),(0.02981,0.0008),(0.004737,0.0000474),(0.05882,0.00059)]
def chi2f(p,Jtarget):
    rt,it=p[0],p[1]
    if it<=0 or (rt*rt+it*it)<1.0 or abs(rt)>0.5: return 1e6
    try:
        o,J=model(p)
        c=sum(((o[i]-TGT[i][0])/TGT[i][1])**2 for i in range(6))+((J-Jtarget)/0.005)**2
        return c if np.isfinite(c) else 1e7
    except Exception: return 1e7
def scan(Jtarget,n=30):
    rng=np.random.default_rng(11); best=1e9; bp=None
    seeds=[(-0.0378,1.090,0.14,0.0,17.70,284.6),(-0.0378,1.090,0.10,0.10,17.70,284.6),(0.0378,1.090,0.10,-0.10,17.70,284.6)]
    seeds+=[(rng.uniform(-0.5,0.5),rng.uniform(1.0,1.5),rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(5,30),rng.uniform(100,500)) for _ in range(n)]
    for s in seeds:
        r=minimize(chi2f,s,args=(Jtarget,),method='Nelder-Mead',options={'xatol':1e-4,'fatol':1e-3,'maxiter':3500})
        if r.fun<best: best=r.fun; bp=r.x
    return best,bp
cm,pm=scan(-0.028); om,Jm=model(pm)
cp,pp=scan(+0.028); op,Jp=model(pp)
print("HOLO-ONLY robust (full already: chi2=2.42 both signs):")
print(f"  target J=-0.028: chi2={cm:.2f}  J={Jm:+.4f}  tau={pm[0]:.3f}+{pm[1]:.3f}i")
print(f"  target J=+0.028: chi2={cp:.2f}  J={Jp:+.4f}  tau={pp[0]:.3f}+{pp[1]:.3f}i")
print(f"  BEST over both signs: chi2={min(cm,cp):.2f}")
print()
print("LOW (both or either) => CP NOT necessary (holo reaches it). HIGH for both => anti-holo NEEDED for CP.")
