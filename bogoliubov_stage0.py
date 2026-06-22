#!/usr/bin/env python3
"""Bogoliubov-eml* Stage 0 -- negative control beta=0.
Static mirror -> no photon creation -> pure positive-frequency (holomorphic) mode.
Anti-holomorphic content = spectral power in negative FFT bins (the beta a-dagger term).

CONVENTION: numpy.fft uses e^{+2 pi i f t}, so positive bin = e^{+i w t} = holomorphic;
the forced conjugate (beta) sits on e^{-i w t} = negative bin = anti-holomorphic.
EXACTNESS: choose omega = 2 pi k / T so the mode lands EXACTLY on FFT bin k (no spectral
leakage). Then beta=0 gives anti-holo weight at machine precision, not a tolerance fudge.
"""
import numpy as np

def make_mode(N=4096, T=10.0, k=3, beta=0.0):
    """omega = 2 pi k / T  -> exact bin. f(t)=alpha e^{+i w t}+beta e^{-i w t}.
    Bogoliubov: |alpha|^2-|beta|^2=1."""
    t = np.linspace(0, T, N, endpoint=False)
    omega = 2*np.pi*k/T
    alpha = np.sqrt(1.0 + beta**2)
    holo = alpha * np.exp(+1j*omega*t)
    anti = beta  * np.exp(-1j*omega*t)
    return t, holo + anti, alpha, omega

def anti_holo_weight(t, f):
    F = np.fft.fft(f)
    freqs = np.fft.fftfreq(len(t), d=(t[1]-t[0]))
    P = np.abs(F)**2
    Ppos = P[freqs > 0].sum()
    Pneg = P[freqs < 0].sum()
    return Pneg / (Ppos + Pneg)

if __name__ == "__main__":
    print("="*60)
    print("BOGOLIUBOV-eml* STAGE 0 -- negative control (beta=0), exact-bin")
    print("="*60)
    tc, fc, _, w = make_mode(beta=0.0)
    Fc = np.fft.fft(fc); fr = np.fft.fftfreq(len(tc), d=(tc[1]-tc[0]))
    peak = fr[np.argmax(np.abs(Fc))]
    print(f"omega={w:.4f}, mode freq={w/(2*np.pi):.4f} Hz; FFT peak={peak:+.4f} (expect POSITIVE, on-bin)")
    t, f, alpha, _ = make_mode(beta=0.0)
    w0 = anti_holo_weight(t, f)
    print(f"beta=0 (static): anti-holo weight = {w0:.3e}  (expect ~machine zero)")
    ok0 = w0 < 1e-20
    tb, fb, ab, _ = make_mode(beta=0.5)
    wb = anti_holo_weight(tb, fb)
    expected = 0.5**2 / (ab**2 + 0.5**2)
    print(f"beta=0.5 (moving): anti-holo weight = {wb:.6f}  (expect {expected:.6f})")
    seesb = abs(wb - expected) < 1e-9
    print("-"*60)
    print("  convention (e^{+iwt} -> positive bin)  :", "PASS" if peak > 0 else "FAIL")
    print("  beta=0  -> holomorphic (weight ~0)     :", "PASS" if ok0 else "FAIL")
    print("  beta!=0 -> anti-holo seen, value exact :", "PASS" if seesb else "FAIL")
    print("-"*60)
    print("STAGE 0", "VALIDATED" if (peak>0 and ok0 and seesb) else "FAILED")
