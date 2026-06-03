import numpy as np
import csv
rng = np.random.default_rng(42)
Nvort = 5
centers   = rng.uniform(-2, 2, Nvort) + 1j*rng.uniform(-2, 2, Nvort)
a_weights = rng.uniform(-1, 1, Nvort) + 1j*rng.uniform(-1, 1, Nvort)
b_weights = rng.uniform(-1, 1, Nvort) + 1j*rng.uniform(-1, 1, Nvort)
def field(zv):
    zc = np.conj(zv)
    out = 0+0j
    for k in range(Nvort):
        out += a_weights[k]*np.log(zv - centers[k]) + b_weights[k]*np.log(zc - np.conj(centers[k]))
    return out
def field_holo(zv):
    out = 0+0j
    for k in range(Nvort):
        out += a_weights[k]*np.log(zv - centers[k])
    return out
xs = np.linspace(-3, 3, 60)
ys = np.linspace(-3, 3, 60)
Z, W = [], []
for x in xs:
    for y in ys:
        zv = x + 1j*y
        if all(abs(zv - c) > 0.3 for c in centers):
            Z.append(zv); W.append(field(zv))
Z = np.array(Z); W = np.array(W)
def dump(fname, zs, ws):
    with open(fname, 'w', newline='') as f:
        wr = csv.writer(f); wr.writerow(['z_re','z_im','w_re','w_im'])
        for zv, wv in zip(zs, ws):
            wr.writerow([zv.real, zv.imag, wv.real, wv.imag])
dump('vortex_gas.csv', Z, W)
dump('vortex_holo_control.csv', Z, [field_holo(zv) for zv in Z])
idx = rng.permutation(len(Z))
dump('vortex_shuffled.csv', Z, [W[idx[i]] for i in range(len(Z))])
print("rows:", len(Z), "| |w| range [%.2f, %.2f]" % (np.abs(W).min(), np.abs(W).max()))
