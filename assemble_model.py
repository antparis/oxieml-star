#!/usr/bin/env python3
"""Assemble Qu-Lu-Ding 2506.19822 T' lepton model (bricks 5+6) with EXACT Qu-Ding
normalized triplets from reference notebook PHMF_integer.nb, calibrate vs Table 2.
Run on Anthony's machine. Arbiter = this execution. NOT an ablation result yet."""
import numpy as np
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp, sqrt, log, gammainc, euler, loggamma
mp.dps=30
def chi2(m):
    r=m%3; return 1 if r==1 else (-1 if r==2 else 0)
def dchi2(N): return sum(chi2(d) for d in range(1,N+1) if N%d==0)
def sigm1(N): return sum(mpf(1)/d for d in range(1,N+1) if N%d==0)
def eta(t):
    q=exp(2*pi*I*t); return exp(pi*I*t/12)*qp(q)
def series(q,c): return sum(mpf(x)*q**n for n,x in enumerate(c))
# EXACT Qu-Ding normalized triplets (from notebook PHMF_integer.nb)
def Y3_w2(tau):
    q=exp(2*pi*I*tau)
    return [series(q,[1,12,36,12,84,72,36,96]),
            -6*q**(mpf(1)/3)*series(q,[1,7,8,18,14]),
            -18*q**(mpf(2)/3)*series(q,[1,2,5,4,8])]
def Y3_w4(tau):
    q=exp(2*pi*I*tau)
    return [series(q,[1,-84,-756,-2028,-6132,-10584,-18252]),
            6*q**(mpf(1)/3)*series(q,[1,73,344,1134,2198,4681]),
            54*q**(mpf(2)/3)*series(q,[1,14,65,148,344,546])]
def Y3_w0(tau):  # eq 3.21, model weight-0 form
    y=tau.imag; q=exp(2*pi*I*tau); qb=exp(-2*pi*I*tau.conjugate())
    Y1=-9*log(3)/(4*pi)+y+(9/pi)*sum((sigm1(n)-sigm1(3*n))*(q**n+qb**n) for n in range(1,30))
    Y2=(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(30))+(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(30))
    Y3=(27/(4*pi))*q**(mpf(2)/3)*sum(sigm1(3*n+2)*q**n for n in range(30))+(9/(2*pi))*q**(mpf(1)/3)*sum(sigm1(3*n+1)*q**n for n in range(30))
    return [Y1,Y2,Y3]
def base_doublet(tau):
    Y1=-3*sqrt(2)*eta(3*tau)**3/eta(tau); q=exp(2*pi*I*tau)
    Y2=1+6*sum(dchi2(n)*q**n for n in range(1,40)); return Y1,Y2
a0=euler+log(3)+log(4*pi)-6*loggamma(mpf(1)/3)+6*loggamma(mpf(2)/3)
def Y2pp(tau):  # brick4 non-holo weight-1 doublet
    y=tau.imag; q=exp(2*pi*I*tau)
    c1=a0+log(y)-6*(q*log(3)+2*q**2*log(2)+2*q**3*log(3))-6*(gammainc(0,4*pi*y)/q+gammainc(0,12*pi*y)/q**3+gammainc(0,16*pi*y)/q**4)
    hc=[log(2),log(5),2*log(2),log(11),2*log(2),log(17),log(5)]
    holo=-6*sqrt(2)*q**(mpf(2)/3)*sum(hc[n]*q**n for n in range(len(hc)))
    nh=sum(dchi2(3*n+1)*q**(-(mpf(3*n+1)/3))*gammainc(0,(12*n+4)*pi*y/3) for n in range(8) if dchi2(3*n+1)!=0)
    return [c1, holo-3*sqrt(2)*nh]
def m2np(M,r,c): return np.array([[complex(M[i,j]) for j in range(c)] for i in range(r)])

def run(label, tau, beta, gamma, g2, tgt):
    g1=mpf(1)
    Y0=Y3_w0(tau); Y2t=Y3_w2(tau); Y4t=Y3_w4(tau)
    Y1b,Y2b=base_doublet(tau); Yh=[Y1b,Y2b]; Yp=Y2pp(tau)
    Me=mp.matrix([[Y0[2],Y0[1],Y0[0]],[beta*Y2t[2],beta*Y2t[1],beta*Y2t[0]],[gamma*Y4t[0],gamma*Y4t[2],gamma*Y4t[1]]])
    MN=mp.matrix([[-Y4t[1],Y4t[2]/sqrt(2)],[Y4t[2]/sqrt(2),Y4t[0]]])
    MD=mp.matrix([[g1*Yp[1],sqrt(2)*g2*Yh[0],-sqrt(2)*g1*Yp[0]-g2*Yh[1]],[g1*Yp[0]-sqrt(2)*g2*Yh[1],sqrt(2)*g1*Yp[1],-g2*Yh[0]]])
    Mnu=-(MD.T*(MN**-1)*MD)
    Me_n=m2np(Me,3,3); Mnu_n=m2np(Mnu,3,3)
    ev,_=np.linalg.eigh(Me_n.conj().T@Me_n); me=np.sqrt(np.abs(np.sort(ev.real)))
    we,Ue=np.linalg.eigh(Me_n.conj().T@Me_n); Ue=Ue[:,np.argsort(we)]
    wn,Vn=np.linalg.eigh(Mnu_n@Mnu_n.conj().T); Vn=Vn[:,np.argsort(wn)]
    U=Ue.conj().T@Vn
    th13=np.arcsin(min(abs(U[0,2]),1)); th12=np.arctan2(abs(U[0,1]),abs(U[0,0])); th23=np.arctan2(abs(U[1,2]),abs(U[2,2]))
    print("=== %s ==="%label)
    print("  m_e/m_mu   = %.6f  target %.6f"%(me[0]/me[1], tgt['eu']))
    print("  m_mu/m_tau = %.6f  target %.5f"%(me[1]/me[2], tgt['ut']))
    print("  sin2_th12  = %.4f  target %.3f"%(np.sin(th12)**2, tgt['s12']))
    print("  sin2_th13  = %.5f  target %.5f"%(np.sin(th13)**2, tgt['s13']))
    print("  sin2_th23  = %.4f  target %.3f"%(np.sin(th23)**2, tgt['s23']))

# With gCP NO: all real couplings (cleanest calibration target)
run("With gCP NO", mpc('-0.03777','1.090'), mpf('17.70'), mpf('284.6'), mpf('0.1490'),
    {'eu':0.004737,'ut':0.05882,'s12':0.308,'s13':0.02215,'s23':0.459})
