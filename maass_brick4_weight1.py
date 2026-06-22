#!/usr/bin/env python3
"""
Brick 4 of the g1=0 ablation build (Qu-Lu-Ding 2506.19822).
The TWO weight-1 level-3 (T') doublets for the Dirac matrix M_D (eq. 4.3):
  Y2hat^(1)   (rep 2-hat)   : HOLOMORPHIC     -> coupling g2
  Y2hat''^(1) (rep 2-hat'')  : NON-HOLOMORPHIC -> coupling g1  (the term to ablate)
Each doublet has 2 components. Sources: eq. 3.11 (holo), eq. 3.25 (non-holo).
TWO paper typos corrected (forced by eq. 3.22, verified by the harmonic + shadow tests):
  - Y2hat''_2 non-holo prefactor is q^{-1/3} (NOT q^{2/3} as printed)
  - 3rd gamma arg is (12n+4)*pi*y/3 = 28*pi*y/3 at n=2 (NOT 2*pi*y/3)
Calibrations (all on Anthony's machine):
  CALIB H      : holo doublet vs published q-expansion eq. 3.11 + eta closed form
  CALIB Delta1 : both non-holo components satisfy the weight-1 harmonic condition Delta_1=0
  CALIB xi1    : xi_1 maps the non-holo doublet to (conj of) the holo doublet (Maass shadow);
                 this discriminated variant A (3n+1) from variant C (3n+2, shadow=0)
Arbiter: runs on Anthony's machine. Sandbox-tested by Claude.
"""
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp, sqrt, log, gammainc, euler, loggamma
mp.dps = 40

def eta(t):
    q = exp(2*pi*I*t); return exp(pi*I*t/12)*qp(q)
def chi2(m):
    r = m % 3; return 1 if r == 1 else (-1 if r == 2 else 0)
def divsum_chi2(N):
    return sum(chi2(d) for d in range(1, N+1) if N % d == 0)

a0 = euler + log(3) + log(4*pi) - 6*loggamma(mpf(1)/3) + 6*loggamma(mpf(2)/3)

def Y2hat_holo(tau):
    Y1 = -3*sqrt(2)*eta(3*tau)**3/eta(tau)
    q = exp(2*pi*I*tau)
    Y2 = 1 + 6*sum(divsum_chi2(n)*q**n for n in range(1, 40))
    return [Y1, Y2]

def Y2pp_c1(tau):
    y = tau.imag; q = exp(2*pi*I*tau)
    return a0 + log(y) - 6*(q*log(3) + 2*q**2*log(2) + 2*q**3*log(3)) \
              - 6*(gammainc(0,4*pi*y)/q + gammainc(0,12*pi*y)/q**3 + gammainc(0,16*pi*y)/q**4)
def Y2pp_c2(tau):
    y = tau.imag; q = exp(2*pi*I*tau)
    hc = [log(2), log(5), 2*log(2), log(11), 2*log(2), log(17), log(5)]
    holo = -6*sqrt(2)*q**(mpf(2)/3)*sum(hc[n]*q**n for n in range(len(hc)))
    nh = sum(divsum_chi2(3*n+1)*q**(-(mpf(3*n+1)/3))*gammainc(0,(12*n+4)*pi*y/3)
             for n in range(8) if divsum_chi2(3*n+1) != 0)
    return holo - 3*sqrt(2)*nh
def Y2hat_nonholo(tau):
    return [Y2pp_c1(tau), Y2pp_c2(tau)]

def Delta1(f, tau, h=mpf('1e-4')):
    x = tau.real; y = tau.imag
    fxx = (f(mpc(x+h,y)) - 2*f(mpc(x,y)) + f(mpc(x-h,y)))/h**2
    fyy = (f(mpc(x,y+h)) - 2*f(mpc(x,y)) + f(mpc(x,y-h)))/h**2
    fx  = (f(mpc(x+h,y)) - f(mpc(x-h,y)))/(2*h)
    fy  = (f(mpc(x,y+h)) - f(mpc(x,y-h)))/(2*h)
    return -y**2*(fxx+fyy) + I*y*(fx + I*fy)
def ddtaubar(f, tau, h=mpf('1e-6')):
    return ((f(tau+h)-f(tau-h))/(2*h) + I*(f(tau+I*h)-f(tau-I*h))/(2*h))/2
def xi1(f, tau): return 2*I*tau.imag*ddtaubar(f, tau)

tau = mpc('0.07', '1.5'); q = exp(2*pi*I*tau)
print("=== CALIB H: holomorphic doublet Y2hat^(1) vs eq. 3.11 ===")
Y1,Y2 = Y2hat_holo(tau)
r1 = Y1/(-3*sqrt(2)*q**(mpf(1)/3)); ref1 = 1+q+2*q**2+2*q**4+q**5+2*q**6
okH1 = abs(r1-ref1) < 1e-2
print("  Y1/(-3sqrt2 q^1/3) =", complex(r1), " vs 1+q+2q^2+... PASS:", okH1)
okH2 = abs(Y2-(1+6*q+6*q**2)) < 0.05
print("  Y2 =", complex(Y2), " vs 1+6q+6q^2 PASS:", okH2)
print()
print("=== CALIB Delta1: non-holo components are weight-1 harmonic ===")
d1 = abs(Delta1(Y2pp_c1, tau)); d2 = abs(Delta1(Y2pp_c2, tau))
print("  Delta_1(Y2hat''_1) =", float(d1), " PASS:", d1 < 1e-2)
print("  Delta_1(Y2hat''_2) =", float(d2), " PASS:", d2 < 1e-2)
print()
print("=== CALIB xi1: Maass shadow reboucle sur le doublet holomorphe (conj) ===")
s1 = xi1(Y2pp_c1, tau); s2 = xi1(Y2pp_c2, tau)
r_s1 = s1/(-Y2.conjugate()); r_s2 = s2/(Y1.conjugate())
print("  xi_1(Y2hat''_1)/(-conj Y_holo2) =", complex(r_s1), " PASS:", abs(r_s1-1) < 1e-2)
print("  xi_1(Y2hat''_2)/( conj Y_holo1) =", complex(r_s2), " PASS:", abs(r_s2-1) < 1e-2)
print()
allok = okH1 and okH2 and d1<1e-2 and d2<1e-2 and abs(r_s1-1)<1e-2 and abs(r_s2-1)<1e-2
print("BRICK 4 fully calibrated:", allok, "-- weight-1 doublets ready for M_D.")
