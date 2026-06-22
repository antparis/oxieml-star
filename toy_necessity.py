#!/usr/bin/env python3
"""Calibration test: a TOY model where anti-holomorphic structure is GENUINELY NECESSARY.
The observable is a natively complex field value f(z) = a*z + b*conj(z) with b independent of a.
Equal-parameter-count comparison: FULL (a*z+b*conj z) fits exactly; HOLO-ONLY (a*z+c, a*z+d*z^2)
cannot. Proves the pipeline detects necessity (the 'yes' verdict), mirror of the T' decorative
'no' verdict. Also writes a clean CSV (z, f) for the SymPy judge verify_exact.py.
Run on Anthony's machine. Arbiter = this execution + judge."""
import numpy as np
from scipy.optimize import minimize
import csv

rng = np.random.default_rng(1)
N = 40
zs = rng.uniform(-2,2,N) + 1j*rng.uniform(-2,2,N)

# TRUTH: genuinely chiral, anti-holo part independent of holo part
a_true, b_true = (1.3-0.4j), (0.8+0.6j)
def truth(z): return a_true*z + b_true*np.conj(z)
DATA = truth(zs)

def full_pred(p, z):   # a*z + b*conj(z), 4 real params
    a=p[0]+1j*p[1]; b=p[2]+1j*p[3]; return a*z + b*np.conj(z)
def holo_lin(p, z):    # a*z + c, holomorphic, 4 real params
    a=p[0]+1j*p[1]; c=p[2]+1j*p[3]; return a*z + c
def holo_quad(p, z):   # a*z + d*z^2, holomorphic, 4 real params
    a=p[0]+1j*p[1]; d=p[2]+1j*p[3]; return a*z + d*z**2

def chi2(p, fn): o=fn(p,zs); return np.sum(np.abs(o-DATA)**2)
def scan(fn,n=30):
    best=1e18; bp=None
    for _ in range(n):
        s=rng.uniform(-2,2,4)
        r=minimize(chi2,s,args=(fn,),method='Nelder-Mead',options={'maxiter':8000,'xatol':1e-10,'fatol':1e-12})
        if r.fun<best: best=r.fun; bp=r.x
    return best,bp

cf,pf=scan(full_pred); cl,_=scan(holo_lin); cq,_=scan(holo_quad)
print("TOY NECESSITY TEST (natively complex observable f(z)=a*z+b*conj z):")
print(f"  FULL (a*z + b*conj z)   chi2 = {cf:.3e}   recovered a={pf[0]:.3f}+{pf[1]:.3f}i  b={pf[2]:.3f}+{pf[3]:.3f}i")
print(f"  HOLO-ONLY (a*z + c)     chi2 = {cl:.3e}")
print(f"  HOLO-ONLY (a*z + d*z^2) chi2 = {cq:.3e}")
print()
print(f"  truth: a={a_true}  b={b_true}")
verdict = (cl>1e-3 and cq>1e-3 and cf<1e-9)
print("  VERDICT:", "ANTI-HOLO NECESSARY (holo-only fails, full fits)" if verdict else "refittable -- design failed")

# write CSV for the SymPy judge: columns z_re, z_im, f_re, f_im
with open('data/toy_necessity.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['z_re','z_im','f_re','f_im'])
    for z,f in zip(zs,DATA):
        w.writerow([z.real, z.imag, f.real, f.imag])
print()
print("  Wrote data/toy_necessity.csv (z, f=a*z+b*conj z) for the judge.")
print("  Expected judge result on f: df/dzbar = b = 0.8+0.6i != 0  => ANTI-HOLOMORPHIC.")
