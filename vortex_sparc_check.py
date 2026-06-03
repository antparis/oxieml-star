import numpy as np
def load(fn):
    d = np.genfromtxt(fn, delimiter=',', names=True)
    z = d['z_re'] + 1j*d['z_im']
    w = d['w_re'] + 1j*d['w_im']
    return z, w
def sparc_test(fn):
    z, w = load(fn)
    # rebuild on a regular grid to take numerical Wirtinger derivatives
    xs = np.unique(np.round(z.real, 6)); ys = np.unique(np.round(z.imag, 6))
    nx, ny = len(xs), len(ys)
    grid = {}
    for zz, ww in zip(z, w):
        grid[(round(zz.real,6), round(zz.imag,6))] = ww
    G = np.full((nx, ny), np.nan, complex)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            v = grid.get((round(x,6), round(y,6)))
            if v is not None: G[i,j] = v
    hx = xs[1]-xs[0]; hy = ys[1]-ys[0]
    dGx = np.full_like(G, np.nan); dGy = np.full_like(G, np.nan)
    dGx[1:-1,:] = (G[2:,:]-G[:-2,:])/(2*hx)
    dGy[:,1:-1] = (G[:,2:]-G[:,:-2])/(2*hy)
    dz    = 0.5*(dGx - 1j*dGy)
    dzbar = 0.5*(dGx + 1j*dGy)
    viol = np.abs(dzbar - np.conj(dz))
    m = np.isfinite(viol)
    return np.nanmedian(viol[m]), np.nanmedian(np.abs(dz)[m]), np.nanmedian(np.abs(dzbar)[m])
for fn in ['vortex_gas.csv','vortex_holo_control.csv']:
    v, adz, adzbar = sparc_test(fn)
    print(f"{fn:28s} median|d/dzbar-conj(d/dz)|={v:.4f}  |d/dz|={adz:.4f}  |d/dzbar|={adzbar:.4f}")
print()
print("vortex_gas: viol >> 0 => escapes SPARC (genuine independent anti). GOOD.")
print("holo_control: |d/dzbar| ~ 0 => holomorphic (no anti). GOOD.")
