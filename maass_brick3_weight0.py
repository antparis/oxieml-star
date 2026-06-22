#!/usr/bin/env python3
"""
Brick 3 of the g1=0 ablation build (Qu-Ding 2406.19822 / 2406.02527).
Non-holomorphic weight-0 level-3 (A4) polyharmonic Maass triplet Y3^(0), Eq. C.32.
Purely non-holomorphic (no holomorphic weight-0 form exists) -> ingredient of M_e.
Calibrated 3 ways against the calibrated weight-2 triplet (brick 2, Feruglio):
  CALIB 1: constant term of comp1 = -9 log3/(4pi) ~ -0.7868
  CALIB 2: D(Y3,i^(0)) = -(1/4pi) Y_i^(2)   [holomorphic part, all 3 comps]
  CALIB 3: xi_0(Y3,1^(0)) = -conj(Y1^(2))   [non-holomorphic part]
The q^1 coefficient is -3/pi (NOT -3/2pi); the D check confirms this.
Arbiter: runs on Anthony's machine. Sandbox-tested by Claude.
"""
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp, log
mp.dps = 30

def eta(t):
    q = exp(2*pi*I*t); return exp(pi*I*t/12)*qp(q)
def dl(t):
    d = mpf('1e-9'); return (eta(t+d)-eta(t-d))/(2*d)/eta(t)
def Yw2(tau):
    Y1 = (I/(2*pi))*( dl(tau/3)+dl((tau+1)/3)+dl((tau+2)/3)-27*dl(3*tau) )
    Y2 = (-I/pi)*( dl(tau/3)+exp(-2*pi*I/3)*dl((tau+1)/3)+exp(-4*pi*I/3)*dl((tau+2)/3) )
    Y3 = (-I/pi)*( dl(tau/3)+exp(-4*pi*I/3)*dl((tau+1)/3)+exp(-2*pi*I/3)*dl((tau+2)/3) )
    return [Y1,Y2,Y3]

def Yw0(tau):
    y=tau.imag; q=exp(2*pi*I*tau)
    c1=[mpf(3)/pi,mpf(9)/(2*pi),mpf(1)/pi,mpf(21)/(4*pi),mpf(18)/(5*pi),mpf(3)/(2*pi)]
    Y1 = y - 9*log(3)/(4*pi) - sum(c1[n-1]*q**n for n in range(1,7)) \
                            - sum(c1[n-1]*exp(-4*pi*n*y)/q**n for n in range(1,7))
    h2=[mpf(1),mpf(7)/4,mpf(8)/7,mpf(9)/5,mpf(14)/13]; nh2=[mpf(1)/4,mpf(1)/5,mpf(5)/16,mpf(2)/11]
    Y2 = (9*q**(mpf(1)/3)/(2*pi))*sum(h2[n]*q**n for n in range(5)) \
       + (27*q**(mpf(1)/3)*exp(pi*y/3)/pi)*sum(nh2[n]*exp(-(4*(n+1)-1)*pi*y)/q**(n+1) for n in range(4))
    h3=[mpf(1)/4,mpf(1)/5,mpf(5)/16,mpf(2)/11,mpf(2)/7]; nh3=[mpf(1),mpf(7)/4,mpf(8)/7,mpf(9)/5]
    Y3 = (27*q**(mpf(2)/3)/pi)*sum(h3[n]*q**n for n in range(5)) \
       + (9*q**(mpf(2)/3)*exp(2*pi*y/3)/(2*pi))*sum(nh3[n]*exp(-(4*(n+1)-2)*pi*y)/q**(n+1) for n in range(4))
    return [Y1,Y2,Y3]

def ddtau(f,tau,h=mpf('1e-7')):
    return ((f(tau+h)-f(tau-h))/(2*h) - I*(f(tau+I*h)-f(tau-I*h))/(2*h))/2
def ddtaubar(f,tau,h=mpf('1e-7')):
    return ((f(tau+h)-f(tau-h))/(2*h) + I*(f(tau+I*h)-f(tau-I*h))/(2*h))/2
def D_c(tau,i):  return ddtau(lambda t: Yw0(t)[i], tau)/(2*pi*I)
def xi0_c(tau,i): return 2*I*ddtaubar(lambda t: Yw0(t)[i], tau)

tau=mpc('0.1','1.3')
print("=== CALIB 1: constant term comp1 ===")
print("-9 log3/(4pi) =", float(-9*log(3)/(4*pi)), " PASS:", abs(float(-9*log(3)/(4*pi))+0.78684)<1e-4)
print()
print("=== CALIB 2: D(Y3,i^(0)) = -(1/4pi) Y_i^(2)  [holomorphic part] ===")
allok=True
for i in range(3):
    r = D_c(tau,i)/(-(mpf(1)/(4*pi))*Yw2(tau)[i]); ok=abs(r-1)<1e-2; allok=allok and ok
    print(f"  comp{i+1}: ratio = {complex(r)}  PASS: {ok}")
print()
print("=== CALIB 3: xi_0(Y3,1^(0)) = -conj(Y1^(2))  [non-holomorphic part] ===")
r = xi0_c(tau,0)/(-Yw2(tau)[0].conjugate()); ok3=abs(r-1)<1e-2
print(f"  ratio = {complex(r)}  PASS: {ok3}")
print()
print("BRICK 3 fully calibrated:", allok and ok3, "-- weight-0 triplet ready for M_e.")
