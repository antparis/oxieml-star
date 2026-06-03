"""
Generate a single-vortex chiral field (Nvort=1) for PySR detection test.
Target:  w(z) = a * log(z - c) + b * log(conj(z) - conj(c))
with a != conj(b) to ensure genuine anti-holomorphic content.
"""
import numpy as np
import csv

rng = np.random.default_rng(42)

Nvort = 1
centers   = rng.uniform(-2, 2, Nvort) + 1j * rng.uniform(-2, 2, Nvort)
a_weights = rng.uniform(-1, 1, Nvort) + 1j * rng.uniform(-1, 1, Nvort)
b_weights = rng.uniform(-1, 1, Nvort) + 1j * rng.uniform(-1, 1, Nvort)

assert abs(a_weights[0] - np.conj(b_weights[0])) > 0.1, \
    "a ~ conj(b): degenerate case, change seed"

print(f"center  c = {centers[0]}")
print(f"weight  a = {a_weights[0]}")
print(f"weight  b = {b_weights[0]}")
print(f"|a - conj(b)| = {abs(a_weights[0] - np.conj(b_weights[0])):.4f}")

def field(zv):
    zc = np.conj(zv)
    return a_weights[0] * np.log(zv - centers[0]) + \
           b_weights[0] * np.log(zc - np.conj(centers[0]))

def field_holo(zv):
    return a_weights[0] * np.log(zv - centers[0])

xs = np.linspace(-3, 3, 60)
ys = np.linspace(-3, 3, 60)
Z, W = [], []
for x in xs:
    for y in ys:
        zv = x + 1j * y
        if abs(zv - centers[0]) > 0.3:
            Z.append(zv)
            W.append(field(zv))

Z = np.array(Z)
W = np.array(W)

def dump(fname, zs, ws):
    with open(fname, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['z_re', 'z_im', 'w_re', 'w_im'])
        for zv, wv in zip(zs, ws):
            wr.writerow([zv.real, zv.imag, wv.real, wv.imag])

dump('vortex_N1.csv', Z, W)
dump('vortex_N1_holo_control.csv', Z, [field_holo(zv) for zv in Z])

idx = rng.permutation(len(Z))
dump('vortex_N1_shuffled.csv', Z, [W[idx[i]] for i in range(len(Z))])

print(f"\nrows: {len(Z)}")
print(f"|w| range [{np.abs(W).min():.4f}, {np.abs(W).max():.4f}]")
print(f"var(w) = {np.var(W):.4f}")

h = 1e-6
dzbar_num, dz_num = [], []
for zv in Z[:200]:
    wx = (field(zv + h) - field(zv - h)) / (2 * h)
    wy = (field(zv + 1j*h) - field(zv - 1j*h)) / (2 * h)
    dz_num.append(0.5 * (wx - 1j * wy))
    dzbar_num.append(0.5 * (wx + 1j * wy))
dzbar_num = np.array(dzbar_num)
dz_num = np.array(dz_num)
viol = np.abs(dzbar_num - np.conj(dz_num))
print(f"\nSPARC check (first 200 pts):")
print(f"  median|d/dzbar - conj(d/dz)| = {np.median(viol):.4f}")
print(f"  median|d/dz|    = {np.median(np.abs(dz_num)):.4f}")
print(f"  median|d/dzbar| = {np.median(np.abs(dzbar_num)):.4f}")
print("  => GENUINE" if np.median(viol) > 0.01 else "  => WARNING: SPARC-degenerate!")
