#!/usr/bin/env python3
"""Extract z=h22 and A33 (co-precessing frame), resample to regular grid,
save .npz for PySR run in the MAIN env. Precessing triplet + aligned control."""
import sxs, numpy as np
TARGETS = {'p0161':'SXS:BBH:0161','p0163':'SXS:BBH:0163',
           'p0164':'SXS:BBH:0164','a0109':'SXS:BBH:0109'}
N_RESAMPLE = 4000  # regular grid points
def extract(sid):
    sim = sxs.load(sid)
    w = sim.h.to_coprecessing_frame()
    idx = {tuple(lm): i for i, lm in enumerate(w.LM.tolist())}
    h = w.data
    t = np.asarray(w.t, dtype=float)
    z   = h[:, idx[(2,2)]]
    A33 = h[:, idx[(3,3)]] - ((-1)**3)*np.conj(h[:, idx[(3,-3)]])
    # regular time grid (skip first/last 5% to avoid junk radiation + ringdown tail)
    t0, t1 = t[0] + 0.05*(t[-1]-t[0]), t[-1] - 0.05*(t[-1]-t[0])
    tg = np.linspace(t0, t1, N_RESAMPLE)
    zr   = np.interp(tg, t, z.real)   + 1j*np.interp(tg, t, z.imag)
    A33r = np.interp(tg, t, A33.real) + 1j*np.interp(tg, t, A33.imag)
    return tg, zr, A33r
data = {}
for tag, sid in TARGETS.items():
    print('extracting', sid, '...')
    tg, zr, A33r = extract(sid)
    data[tag+'_t']   = tg
    data[tag+'_z']   = zr
    data[tag+'_A33'] = A33r
np.savez('gw_pysr_data.npz', **data)
print()
print('=== saved gw_pysr_data.npz ===')
print('keys:', list(data.keys()))
for tag in TARGETS:
    z = data[tag+'_z']; A = data[tag+'_A33']
    print('%s: N=%d  |z|med=%.3e  |A33|med=%.3e  NaN=%s' % (
        tag, len(z), np.median(np.abs(z)), np.median(np.abs(A)),
        np.isnan(z).any() or np.isnan(A).any()))
