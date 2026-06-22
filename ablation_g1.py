#!/usr/bin/env python3
"""g1=0 ablation test on Qu-Lu-Ding T' lepton model. Kill the non-holomorphic
Y_2hat'' Dirac term (g1=0), re-minimize chi2 over neutrino-sector params vs NuFIT.
chi2 stays bad => non-holo NECESSARY; recovers => decorative. Multi-start.
Run on Anthony's machine. Arbiter = this execution."""
import numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp, sqrt, log, gammainc, euler, loggamma
mp.dps=25
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
    Y1=-3*sqrt(2)*eta(3*tau)**3/eta(tau); q=exp(2*pi*I*tau); Y2=1+6*sum(dchi2(n)*q**n for n in range(1,40)); return Y1,Y2
a0=euler+log(3)+log(4*pi)-6*loggamma(mpf(1)/3)+6*loggamma(mpf(2)/3)
def Y2pp(tau):
    y=tau.imag; q=exp(2*pi*I*tau)
    c1=a0+log(y)-6*(q*log(3)+2*q**2*log(2)+2*q**3*log(3))-6*(gammainc(0,4*pi*y)/q+gammainc(0,12*pi*y)/q**3+gammainc(0,16*pi*y)/q**4)
    hc=[log(2),log(5),2*log(2),log(11),2*log(2),log(17),log(5)]
    holo=-6*sqrt(2)*q**(mpf(2)/3)*sum(hc[n]*q**n for n in range(len(hc)))
    nh=sum(dchi2(3*n+1)*q**(-(mpf(3*n+1)/3))*gammainc(0,(12*n+4)*pi*y/3) for n in range(8) if dchi2(3*n+1)!=0)
    return [c1, holo-3*sqrt(2)*nh]
def m2np(M,r,c): return np.array([[complex(M[i,j]) for j in range(c)] for i in range(r)])

# neutrino-sector observables (g1-sensitive), NuFIT NO from Table 1
TGT = {'s12':(0.308,0.012),'s13':(0.02215,0.00056),'s23':(0.470,0.015),'dmr':(7.49e-5/2.513e-3,0.19e-5/2.513e-3)}

def neutrino_obs(tau, g1, g2):
    Y4t=Y3_w4(tau); Y1b,Y2b=base_doublet(tau); Yh=[Y1b,Y2b]; Yp=Y2pp(tau)
    MN=mp.matrix([[-Y4t[1],Y4t[2]/sqrt(2)],[Y4t[2]/sqrt(2),Y4t[0]]])
    MD=mp.matrix([[g1*Yp[1],sqrt(2)*g2*Yh[0],-sqrt(2)*g1*Yp[0]-g2*Yh[1]],[g1*Yp[0]-sqrt(2)*g2*Yh[1],sqrt(2)*g1*Yp[1],-g2*Yh[0]]])
    Mnu=-(MD.T*(MN**-1)*MD); Mnu_n=m2np(Mnu,3,3)
    # charged-lepton basis: use the identity-equivalent? No -- mixing needs M_e. Use M_e from full model (fixed, g1-independent).
    return Mnu_n

# M_e is g1-independent; build once at a fixed (good) charged-lepton point
def Me_fixed(tau, beta, gamma):
    q=exp(2*pi*I*tau)
    Y2t=[series(q,[1,12,36,12,84,72,36,96]),-6*q**(mpf(1)/3)*series(q,[1,7,8,18,14]),-18*q**(mpf(2)/3)*series(q,[1,2,5,4,8])]
    Y4t=Y3_w4(tau)
    y=tau.imag; qb=exp(-2*pi*I*tau.conjugate())
    Y0_1=-9*log(3)/(4*pi)+y+(9/pi)*sum((sigm1(n)-sigm1(3*n))*(q**n+qb**n) for n in range(1,25))
    Y0_2=(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(25))+(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(25))
    Y0_3=(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(25))+(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(25))
    Y0=[Y0_1,Y0_2,Y0_3]
    return mp.matrix([[Y0[2],Y0[1],Y0[0]],[beta*Y2t[2],beta*Y2t[1],beta*Y2t[0]],[gamma*Y4t[0],gamma*Y4t[2],gamma*Y4t[1]]])

def chi2_neutrino(p, g1fixed):
    rt,it,g2 = p
    tau=mpc(rt,it)
    try:
        beta=mpf('17.70'); gamma=mpf('284.6')
        Men=m2np(Me_fixed(tau,beta,gamma),3,3)
        Mnu_n=neutrino_obs(tau, mpf(g1fixed), mpf(g2))
        we,Ue=np.linalg.eigh(Men.conj().T@Men); Ue=Ue[:,np.argsort(we)]
        wn,Vn=np.linalg.eigh(Mnu_n@Mnu_n.conj().T); Vn=Vn[:,np.argsort(wn)]
        U=Ue.conj().T@Vn; mnu=np.sqrt(np.sort(np.abs(wn)))
        s12=np.sin(np.arctan2(abs(U[0,1]),abs(U[0,0])))**2
        s13=np.sin(np.arcsin(min(abs(U[0,2]),1)))**2
        s23=np.sin(np.arctan2(abs(U[1,2]),abs(U[2,2])))**2
        dmr=(mnu[1]**2-mnu[0]**2)/(mnu[2]**2-mnu[0]**2)
        c=0
        for v,(cc,ss) in [(s12,TGT['s12']),(s13,TGT['s13']),(s23,TGT['s23']),(dmr,TGT['dmr'])]:
            c+=((v-cc)/ss)**2
        return c if np.isfinite(c) else 1e6
    except Exception:
        return 1e6

def best_chi2(g1fixed, ntries=12):
    best=1e9; bp=None
    rng=np.random.default_rng(0)
    starts=[(-0.03777,1.090,0.1490)]+[(rng.uniform(-0.5,0.5),rng.uniform(0.9,1.3),rng.uniform(0.01,0.6)) for _ in range(ntries)]
    for s in starts:
        r=minimize(chi2_neutrino,s,args=(g1fixed,),method='Nelder-Mead',options={'xatol':1e-4,'fatol':1e-3,'maxiter':2000})
        if r.fun<best: best=r.fun; bp=r.x
    return best,bp

print("=== FULL MODEL (g1=1) ===")
c_full,p_full=best_chi2(1.0)
print("  best chi2_neutrino =",round(c_full,3)," at tau=%.4f+%.4fi g2=%.4f"%(p_full[0],p_full[1],p_full[2]))
print()
print("=== ABLATION (g1=0, non-holo term OFF), re-minimized ===")
c_abl,p_abl=best_chi2(0.0)
print("  best chi2_neutrino =",round(c_abl,3)," at tau=%.4f+%.4fi g2=%.4f"%(p_abl[0],p_abl[1],p_abl[2]))
print()
print("VERDICT:")
print("  chi2 full   =",round(c_full,2))
print("  chi2 g1=0   =",round(c_abl,2))
if c_abl > 25:
    print("  => g1=0 cannot fit: NON-HOLOMORPHIC TERM NECESSARY (chi2 stays bad after refit)")
elif c_abl < 3*max(c_full,1):
    print("  => g1=0 refit recovers: non-holo term DECORATIVE")
else:
    print("  => intermediate: degraded but not collapsed -- needs interpretation")
