# FINDINGS — DEIMOS complex-shear residual: WALL [LIMITE budget]

## What was tested
Broken parameter vs May Test C: the observable. Test C used the REAL tangential
projection gamma_t(r) (mirror-locked by construction). Here: the FULL complex
shear gamma = e1 + i*e2, unprojected, residual after subtracting the standard
stacked pattern gamma = -A e^{2i phi}/r, around 268 GAMA lenses.

## Pipeline (machine-run)
build_shear_residual.py (stage 1): 195,513 -> 152,076 sources after cuts
(SN>10, flag=0, MASK=0); |e| mean 0.2369 (matches May ref ~0.25); pairing
radius 20 arcmin -> 11,092 pairs. shear_residual_stage2.py (stage 2):
self-pairs excluded (r>0.2 arcmin), polar binning 5x6 on the complex
Delta_z plane, 24 bins filled, ~162 pairs/bin.

## Gates and results (exact numbers, machine)
- Noise-floor MSE = 7.87e-04 < 1e-3 threshold: measurement VALID.
- Standard-pattern fit: A = -0.00544; SHUFFLE control: A_shuffled = 0.01117.
  |A| < |A_shuffle| => even the STANDARD lensing pattern is not detectable
  at this budget (268 lenses, DEIMOS depth). May's 1/r detection required
  the 21M-source SOM-gold catalog.
- Residual reduced chi2 = 1.29: consistent with pure noise. No structure.
- PSF control: |corr(residual, PSF stack)| = 0.159: not instrumental.

## Verdict
WALL [LIMITE budget], NOT structural. No PySR stage 3 (gates forbid it:
running the discoverer on pure noise manufactures ghost formulas). DEIMOS is
now closed on the CORRECT object (full complex field), unlike May's closure
on the real projection. The same test on SOM-gold 21M remains open in
principle. Anti-holomorphic content in DEIMOS weak lensing: none measurable.

## Traces
build_shear_residual.py, shear_residual_stage2.py,
data/shear_residual_pairs.csv (11,092 rows),
data/shear_residual_binned.csv (24 bins).
