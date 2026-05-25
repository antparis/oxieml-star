# FINDINGS 2026-05-24 — First real-data test: VLA radio-interferometer visibilities

## Goal
Run the eml-star detection pipeline on REAL natively-complex data (not real re-encoded as complex).
Dataset: VLA tutorial UVFITS day2_TDEM0003_10s_norx_1src_1spw.uvfits (4.06 MB, 348160 vis points).
Light path: pyuvdata (pip, no CASA, no casacore) on Mac. Genuinely complex (imag part nonzero).

## Protocol [ÉTABLI]
1. Fix ONE channel (CH=32) + ONE polarization (POL=0) -> z->f(z) is a well-defined function.
2. z = u + i*v ; f = complex visibility at (CH,POL).
3. CUT to v >= 0 to break Hermitian symmetry V(-u,-v)=conj(V(u,v)) (anti-SPARC guard). 864 points after cut.
4. Normalize z and f. Save real + a seed-42 shuffled negative control.
5. PySR toolbox INCLUDING conjugation (my_conj): we SEARCH whether conj is needed.
   niterations=120, population=400, maxsize=30, parsimony=0.001, precision=64.

## Result [ÉTABLI] — NULL (correct scientific outcome)
REAL     : best_mse 0.0608 , complexity 30 (formula contains my_conj terms)
SHUFFLED : best_mse 0.0623 , complexity 30
Two MSE essentially identical, BOTH ~60x above the 1e-3 threshold.

## Verdict
NEGATIVE CONTROL MATCHES REAL DATA -> the real fit captures NO genuine structure.
The my_conj terms in the real Pareto are a MARKER, not a verdict, and are meaningless here.
MSE alone (0.06 >> 1e-3) invalidates any claim; no SymPy judge step needed.
Conclusion: eml-star finds NO exploitable holomorphic/anti-holomorphic structure in VLA
visibilities at this channel/pol after the v>=0 cut. This matches the prior conclusion that
radio-interferometer visibilities are an "oracle" case (EHT M87), not a discovery terrain.

## Methodological gains [ÉTABLI]
- Light pipeline (pyuvdata, no CASA) works on real public data, reproducible by anyone.
- The shuffle negative control did its job: it caught a potential false positive (the my_conj marker).
- The protocol correctly says "nothing here" instead of fabricating a SPARC-style artefact.

## Data on disk
Mac: /Users/ant/Library/Caches/pyuvdata/.../day2_TDEM0003_10s_norx_1src_1spw.uvfits
     /tmp/vla_real.npz, /tmp/vla_shuffled.npz (note: /tmp cleared on Mac reboot)
     /tmp/vla_real_result.json, /tmp/vla_shuffled_result.json
