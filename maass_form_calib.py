#!/usr/bin/env python3
"""
maass_form_calib.py -- Brick 1 of the g1=0 ablation simulation (Qu-Lu-Ding 2506.19822).
Calibrates the weight-1 level-3 non-holomorphic polyharmonic Maass form Y2hat''^(1)
against the paper's published constant a0, and measures its holomorphic vs
non-holomorphic content at the best-fit modulus.
Arbiter: this runs on Anthony's machine. Sandbox-tested by Claude beforehand.
"""
from mpmath import mp, mpf, euler, log, pi, loggamma, gammainc, exp, mpc, j as I
mp.dps = 30

# --- Calibration 1: the constant a0 (Qu-Lu-Ding eq. 3.26) ---
a0 = euler + log(3) + log(4*pi) - 6*loggamma(mpf(1)/3) + 6*loggamma(mpf(2)/3)
print("=== CALIBRATION: a0 (published ~ 0.1132) ===")
print("a0 =", a0)
print("PASS:", abs(float(a0) - 0.1132) < 1e-3)
print()

# --- Best-fit modulus (NO, no gCP), Qu-Lu-Ding Table 2 ---
Retau, Imtau = mpf('-0.1563'), mpf('1.108')
tau = mpc(Retau, Imtau); y = Imtau
q = exp(2*pi*I*tau)
print("=== Y2hat''_1^(1) decomposition at best-fit tau (Im tau=1.108) ===")
print("|q| =", abs(q), "(q-series converges fast)")

# Classify by Wirtinger d/dtaubar:
#   HOLOMORPHIC (d/dtaubar=0): a0 + mock q-series
#   NON-HOLOMORPHIC: log(y) + incomplete-Gamma terms
holo = a0 - 6*(q*log(3) + 2*q**2*log(2) + 2*q**3*log(3))
nh_logy = log(y)
nh_gamma = -6*(gammainc(0,4*pi*y)/q + gammainc(0,12*pi*y)/q**3 + gammainc(0,16*pi*y)/q**4)
nonholo = nh_logy + nh_gamma
full = holo + nonholo

print("HOLOMORPHIC part |.|   =", float(abs(holo)))
print("NON-HOLO log(y)        =", float(nh_logy))
print("NON-HOLO Gamma |.|     =", float(abs(nh_gamma)))
print("NON-HOLO total |.|     =", float(abs(nonholo)))
print("FULL form |.|          =", float(abs(full)))
print()
print("non-holo fraction =", float(100*abs(nonholo)/abs(full)), "%")
print("  (of which Gamma/mock part =", float(100*abs(nh_gamma)/abs(nonholo)), "% -- exponentially suppressed)")
print()
print("KEY: the non-holomorphic content (~48%) is dominated by log y, NOT the mock-Gamma part.")
print("The genuinely 'deep' non-holomorphic (anti-holo) mock structure is <0.5% at the physical tau.")
print("xi_1(log y) = -1 exactly: this non-holo content lifts to a trivial O(1) holomorphic shadow.")
