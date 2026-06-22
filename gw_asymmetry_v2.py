#!/usr/bin/env python3
"""GW mirror-asymmetry test, factor (-1)^l (Boyle et al. 1409.4431).
Surviving violation of h_{l,-m}=(-1)^l conj(h_{l,m}) in co-precessing frame.
Global norm by |h22|, threshold on weak modes. Precessing triplet vs aligned."""
import sxs, numpy as np
MODES = [(2,2),(2,1),(3,3),(3,2),(4,4),(4,3),(5,5),(5,4)]
THRESH = 1e-4
def asym_table(sid):
    sim = sxs.load(sid)
    w = sim.h.to_coprecessing_frame()
    idx = {tuple(lm): i for i, lm in enumerate(w.LM.tolist())}
    h = w.data
    scale = np.median(np.abs(h[:, idx[(2,2)]])) + 1e-30
    out = {}
    for (l,m) in MODES:
        if (l,m) not in idx or (l,-m) not in idx:
            out[(l,m)] = ('NA', None); continue
        a = h[:, idx[(l,m)]]; b = h[:, idx[(l,-m)]]
        amp = np.median(np.abs(a))/scale
        if amp < THRESH:
            out[(l,m)] = ('skip', amp)
        else:
            A = a - ((-1)**l)*np.conj(b)
            out[(l,m)] = (np.median(np.abs(A))/scale, amp)
    return out
targets = {
    'BBH:0161 prec': 'SXS:BBH:0161',
    'BBH:0163 prec': 'SXS:BBH:0163',
    'BBH:0164 prec': 'SXS:BBH:0164',
    'BBH:0109 alig': 'SXS:BBH:0109',
}
results = {name: asym_table(sid) for name, sid in targets.items()}
print("="*78)
print("ASYMMETRY |A_lm|/|h22| in CO-PRECESSING frame, factor (-1)^l, thresh=%.0e" % THRESH)
print("="*78)
print("mode  | " + " | ".join(f"{n:14s}" for n in results))
for (l,m) in MODES:
    cells = []
    for name in results:
        val, amp = results[name][(l,m)]
        if val == 'skip': cells.append(f"{'skip':14s}")
        elif val == 'NA': cells.append(f"{'NA':14s}")
        else: cells.append(f"{val:<14.3e}")
    print(f"({l},{m}) | " + " | ".join(cells))
print()
print("READ: chiral signal = precessing >> aligned on SAME measurable mode.")
print("If precessing ~ aligned everywhere -> no chiral asymmetry (negative, honest).")
