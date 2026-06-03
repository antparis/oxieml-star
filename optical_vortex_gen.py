"""
optical_vortex_gen.py -- physically-honest anti-holomorphic test case.

A Laguerre-Gauss optical vortex of topological charge l:
    u_l(z) ~ z^l  * exp(-|z|^2 / w^2)   for l > 0   (phase winds one way)
    u_l(z) ~ conj(z)^|l| * exp(-|z|^2/w^2) for l < 0 (phase winds the OTHER way)

The SIGN of l (the chirality / handedness of the phase winding) is exactly the
holomorphic vs anti-holomorphic distinction. This is REAL physics: optical
vortices are routinely generated (spiral phase plates, SLMs) and measured
(interferometric 'fork' fringes). The Gaussian envelope exp(-z*conj(z)/w^2)
is common to both signs and itself carries z_bar -- so the RAW beam is never
purely holomorphic. Dividing out the (known) envelope is an ANALYSIS CHOICE
that reveals the underlying chirality. This demonstrates the user's thesis:
how you treat the data decides whether you see the anti-holomorphic structure.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from antiholo_probe import probe_scattered, interpret

w = 2.0
xs = np.linspace(-3, 3, 80)
ys = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(xs, ys, indexing='ij')
Z = (X + 1j * Y).ravel()
env = np.exp(-(np.abs(Z) ** 2) / w ** 2)

def beam(l):
    if l >= 0:
        return (Z ** l) * env
    else:
        return (np.conj(Z) ** abs(l)) * env

print("=== Optical vortex: chirality = holomorphic vs anti-holomorphic ===\n")
for l in [+3, -3]:
    u = beam(l)
    # RAW beam (envelope included, as physically measured)
    A_raw, dz_raw, dzb_raw = probe_scattered(Z, u, n=70)
    # After dividing the KNOWN Gaussian envelope (analysis choice)
    u_clean = u / env
    A_cln, dz_cln, dzb_cln = probe_scattered(Z, u_clean, n=70)
    print(f"charge l = {l:+d}")
    print(f"  RAW beam      : anti-fraction A = {A_raw:5.3f}   -> {interpret(A_raw)}")
    print(f"  envelope-out  : anti-fraction A = {A_cln:5.3f}   -> {interpret(A_cln)}")
    print()

# Negative control: shuffle the field values (destroy spatial structure)
print("=== Negative control (shuffled charge +3 beam) ===")
u = beam(+3) / env
idx = np.random.default_rng(0).permutation(len(u))
A_shuf, _, _ = probe_scattered(Z, u[idx], n=70)
print(f"  shuffled      : anti-fraction A = {A_shuf:5.3f}   -> {interpret(A_shuf)}")
print("  (a structureless field gives A near 0.5: no clean holo/anti signal)")
