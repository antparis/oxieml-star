"""
antiholo_probe.py  --  CHEAP anti-holomorphic 'fuel gauge' for complex fields.

Given a natively-complex field f sampled on points z = x + i*y, estimate the
Wirtinger derivatives by finite differences on a regular grid and report the
ANTI-HOLOMORPHIC FRACTION:

    A = median|df/dz_bar| / (median|df/dz| + median|df/dz_bar|)

    A ~ 0   -> holomorphic   (depends on z only)        [EML branch]
    A ~ 1   -> anti-holomorphic (depends on z_bar only)  [EML* branch]
    A ~ 0.5 -> mixed

No PySR, no symbolic regression. Runs in milliseconds. Intended as a PRE-FILTER
on real data (KiDS pixel grid, optical-vortex measurement, CMB Q+iU) before any
expensive symbolic-regression run. It is a NUMERICAL INDICATOR, not a proof:
certification still requires the SymPy judge on a fitted closed form.
"""
import numpy as np


def wirtinger_grid(xs, ys, G):
    """Central-difference Wirtinger derivatives on a regular grid.
    G[i,j] = f(xs[i], ys[j]), complex. NaN allowed for masked points."""
    hx = xs[1] - xs[0]
    hy = ys[1] - ys[0]
    dGx = np.full_like(G, np.nan, dtype=complex)
    dGy = np.full_like(G, np.nan, dtype=complex)
    dGx[1:-1, :] = (G[2:, :] - G[:-2, :]) / (2 * hx)
    dGy[:, 1:-1] = (G[:, 2:] - G[:, :-2]) / (2 * hy)
    dz    = 0.5 * (dGx - 1j * dGy)
    dzbar = 0.5 * (dGx + 1j * dGy)
    return dz, dzbar


def anti_fraction_from_grid(xs, ys, G):
    dz, dzbar = wirtinger_grid(xs, ys, G)
    m = np.isfinite(dz) & np.isfinite(dzbar)
    adz = np.nanmedian(np.abs(dz[m]))
    adzbar = np.nanmedian(np.abs(dzbar[m]))
    A = adzbar / (adz + adzbar + 1e-300)
    return A, adz, adzbar


def probe_scattered(z, f, n=60):
    """Bin scattered (z, f) onto an n x n grid, then probe. Returns A, |dz|, |dzbar|."""
    x, y = z.real, z.imag
    xs = np.linspace(x.min(), x.max(), n)
    ys = np.linspace(y.min(), y.max(), n)
    G = np.full((n, n), np.nan, dtype=complex)
    ix = np.clip(np.searchsorted(xs, x) - 1, 0, n - 1)
    iy = np.clip(np.searchsorted(ys, y) - 1, 0, n - 1)
    # average duplicates per cell
    acc = {}
    for a, b, val in zip(ix, iy, f):
        acc.setdefault((a, b), []).append(val)
    for (a, b), vals in acc.items():
        G[a, b] = np.mean(vals)
    return anti_fraction_from_grid(xs, ys, G)


def interpret(A):
    if A < 0.15:
        return "HOLOMORPHIC  (z only)  -> EML branch"
    if A > 0.85:
        return "ANTI-HOLOMORPHIC (z_bar only) -> EML* branch"
    return "MIXED (both z and z_bar present)"
