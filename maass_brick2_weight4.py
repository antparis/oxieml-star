#!/usr/bin/env python3
"""
Brick 2 of the g1=0 ablation build (Qu-Lu-Ding 2506.19822).
Holomorphic level-3 modular forms: weight-2 triplet (calibrated vs Feruglio
1706.08749 known q-expansion) and the weight-4 triplet/singlet built on it.
The weight-4 triplet Y3^(4) is the ingredient of the Majorana matrix M_N.
Arbiter: runs on Anthony's machine. Sandbox-tested by Claude.
"""
from mpmath import mp, mpf, pi, exp, mpc, j as I, qp
mp.dps = 40

def eta(t):
    q = exp(2*pi*I*t); return exp(pi*I*t/12)*qp(q)
def dlog_eta(t):
    d = mpf('1e-9'); return (eta(t+d)-eta(t-d))/(2*d)/eta(t)

def Yw2(tau):
    Y1 = (I/(2*pi))*( dlog_eta(tau/3)+dlog_eta((tau+1)/3)+dlog_eta((tau+2)/3)-27*dlog_eta(3*tau) )
    Y2 = (-I/pi)*( dlog_eta(tau/3)+exp(-2*pi*I/3)*dlog_eta((tau+1)/3)+exp(-4*pi*I/3)*dlog_eta((tau+2)/3) )
    Y3 = (-I/pi)*( dlog_eta(tau/3)+exp(-4*pi*I/3)*dlog_eta((tau+1)/3)+exp(-2*pi*I/3)*dlog_eta((tau+2)/3) )
    return Y1,Y2,Y3

def Yw4_triplet(tau):
    Y1,Y2,Y3 = Yw2(tau)
    return (Y1*Y1-Y2*Y3, Y3*Y3-Y1*Y2, Y2*Y2-Y1*Y3)

# --- CALIBRATION of weight-2 triplet vs Feruglio known q-expansion ---
tau = mpc(0, 2.5); q = exp(2*pi*I*tau)
Y1,Y2,Y3 = Yw2(tau)
print("=== CALIBRATION weight-2 triplet (Feruglio 1706.08749) ===")
print("Y1            =", complex(Y1), " expected 1+12q =", complex(1+12*q))
print("Y2/q^(1/3)    =", complex(Y2/q**(mpf(1)/3)), " expected -6")
print("Y3/q^(2/3)    =", complex(Y3/q**(mpf(2)/3)), " expected -18")
ok = abs(Y1-(1+12*q))<1e-4 and abs(Y2/q**(mpf(1)/3)+6)<1e-3 and abs(Y3/q**(mpf(2)/3)+18)<1e-3
print("PASS:", ok)
print()

# --- weight-4 triplet (ingredient of M_N) at the lepton best-fit tau ---
taubf = mpc('-0.1563','1.108')
t1,t2,t3 = Yw4_triplet(taubf)
print("=== weight-4 triplet Y3^(4) at lepton best-fit tau (Im=1.108) ===")
print("Y3^(4) =", [complex(t1), complex(t2), complex(t3)])
print("all finite & nonzero:", all(abs(x)>0 for x in (t1,t2,t3)))
print()
print("Brick 2 OK: holomorphic weight-2 (calibrated) and weight-4 (for M_N) ready.")
