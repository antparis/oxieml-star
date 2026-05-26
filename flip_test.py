#!/usr/bin/env python3
# Flip test: chirality mixing phi<->chi in the 1+1D Dirac-like system.
#   d_t phi + d_x phi = -mu chi      (right-mover, "left chirality" phi)
#   d_t chi - d_x chi = -mu phi      (left-mover,  "right chirality" chi)
#
# QUESTION (Anthony's intuition vs the machine): as the mass mu grows,
# is the onset of phi<->chi mixing a THRESHOLD (nothing, then sudden flip)
# or PROGRESSIVE from mu=0 ? We do NOT presuppose the answer.
#
# Method: solve EXACTLY in Fourier space (no numerical PDE error).
# For a single mode k, the 2x2 system has eigenfrequencies; we evolve a
# Gaussian wavepacket initially in phi only (chi=0) and measure mixing.
#
# Mixing observable (L2, gauge-clean): fraction of energy that has flowed
# from phi into chi:   M(t) = ||chi||^2 / (||phi||^2 + ||chi||^2).
#
# This is a HEURISTIC numerical indicator, NOT a judge-certified result.

import numpy as np

# ----- spatial grid (periodic box) -----
N  = 2048
L  = 50.0
x  = np.linspace(-L/2, L/2, N, endpoint=False)
dx = x[1] - x[0]
k  = 2*np.pi*np.fft.fftfreq(N, d=dx)          # wavenumbers

# ----- initial condition: Gaussian packet in phi only, chi = 0 -----
x0, sigma, k0 = 0.0, 3.0, 1.0
phi0 = np.exp(-(x-x0)**2/(2*sigma**2)) * np.cos(k0*x)
chi0 = np.zeros_like(x)

phi0_k = np.fft.fft(phi0)
chi0_k = np.fft.fft(chi0)

def evolve(mu, t):
    """Exact time evolution in Fourier space for each mode k.
       System per mode:  d_t [phi_k; chi_k] = M_k [phi_k; chi_k]
       with  d_t phi = -i k phi - mu chi      (from d_t phi = -d_x phi - mu chi)
             d_t chi = +i k chi - mu phi      (from d_t chi = +d_x chi - mu phi)
       M_k = [[-i k, -mu], [-mu, +i k]].
    """
    phout = np.zeros(N, dtype=complex)
    chout = np.zeros(N, dtype=complex)
    for j in range(N):
        kk = k[j]
        M = np.array([[-1j*kk, -mu],
                      [-mu,    +1j*kk]], dtype=complex)
        from scipy.linalg import expm
        U = expm(M*t)
        v0 = np.array([phi0_k[j], chi0_k[j]], dtype=complex)
        v  = U @ v0
        phout[j], chout[j] = v[0], v[1]
    phi = np.fft.ifft(phout)
    chi = np.fft.ifft(chout)
    return phi, chi

def mixing_at(mu, t):
    phi, chi = evolve(mu, t)
    np_ = np.sum(np.abs(phi)**2)
    nc_ = np.sum(np.abs(chi)**2)
    return nc_/(np_+nc_)

# The per-mode expm loop over 2048 modes is slow; use the closed form instead.
# Eigenvalues of M_k are +/- sqrt(-(k^2+mu^2)) = +/- i*omega, omega=sqrt(k^2+mu^2).
# Closed-form propagator (standard 2x2 exp):
def evolve_fast(mu, t):
    om = np.sqrt(k**2 + mu**2)
    # handle om=0 (k=0,mu=0) safely
    cos = np.cos(om*t)
    # sinc-like term sin(om t)/om, limit t at om->0
    with np.errstate(divide='ignore', invalid='ignore'):
        sinc = np.where(om>1e-14, np.sin(om*t)/om, t)
    # U = cos(om t) I + sinc * M   (since M^2 = -(k^2+mu^2) I = -om^2 I)
    a = -1j*k        # M11
    b = -mu          # M12 = M21
    d =  1j*k        # M22
    U11 = cos + sinc*a
    U12 =        sinc*b
    U21 =        sinc*b
    U22 = cos + sinc*d
    phout = U11*phi0_k + U12*chi0_k
    chout = U21*phi0_k + U22*chi0_k
    phi = np.fft.ifft(phout)
    chi = np.fft.ifft(chout)
    return phi, chi

def mixing_fast(mu, t):
    phi, chi = evolve_fast(mu, t)
    np_ = np.sum(np.abs(phi)**2); nc_ = np.sum(np.abs(chi)**2)
    return nc_/(np_+nc_)

print("="*64)
print("FLIP TEST: chirality mixing phi<->chi vs mass mu")
print("system: d_t phi + d_x phi = -mu chi ; d_t chi - d_x chi = -mu phi")
print("Mixing M = ||chi||^2 / (||phi||^2+||chi||^2), packet starts in phi only")
print("="*64)

T = 10.0
print(f"\n--- Mixing at fixed time t={T}, scanning mu ---")
print(f"{'mu':>8} | {'Mixing M(t=10)':>16}")
print("-"*30)
mus = [0.0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
for mu in mus:
    M = mixing_fast(mu, T)
    print(f"{mu:8.3f} | {M:16.6e}")

print("\n--- Small-mu behaviour (is onset a threshold or smooth?) ---")
print(f"{'mu':>8} | {'M(t=10)':>14} | {'M/mu^2':>12}")
print("-"*40)
for mu in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05]:
    M = mixing_fast(mu, T)
    print(f"{mu:8.3f} | {M:14.6e} | {M/mu**2:12.4f}")

print("\nReading guide:")
print("  - If M jumps from 0 to finite only past some mu*, that's a THRESHOLD.")
print("  - If M -> 0 smoothly as mu->0 (and M/mu^2 ~ const), that's PROGRESSIVE")
print("    with leading behaviour M ~ (const)*mu^2.")
print("  (The machine decides; this script does not presuppose.)")
