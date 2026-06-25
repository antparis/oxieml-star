# FINDINGS — a=1/2 gCLM exact-profile calibration + exponent-convention lock resolved

**Date:** 2026-06-25
**Status:** [ESTABLISHED] (level-2b) — executed on Anthony's machine; both instruments agree
with truth AND with each other (tol 2%).
**Files:** `clm_calib_ahalf.py` (standalone; does NOT touch the validated `clm_calib.py`).
**Source:** Lushnikov, Silantyev, Siegel, "Collapse vs. blow up and global existence in the
generalized Constantin-Lax-Majda equation", arXiv:2010.01201.

## Central result: the exponent-convention lock (resolved from the primary source)
Three exponents were being conflated; this is the resolution, verified against the paper:
- **gamma = SPATIAL singularity order**: `omega ~ (x - i v_c)^(-gamma)` (their Eq. 13/17).
  **Theorem 1 (Eq. 21): gamma = 1/(1-a).**
- **p = FOURIER exponent**: `|omega_hat_k| ~ C e^(-delta|k|)/|k|^p` (Eq. 62). Their Eq. 63 gives
  `delta = q_c` and **`p = 1 - gamma`**, hence `p = -a/(1-a)`.
- **OUR INSTRUMENTS MEASURE gamma (the spatial order), NOT the Fourier p.**
  - radial fits `Omega(i s) ~ (delta - s)^(-gamma)` -> slope = -gamma.
  - AAA on `U'/U` (= `Omega'/Omega`): a pole/branch of ANY order gamma gives `U'/U ~ -gamma/(x-x0)`,
    a SIMPLE pole of residue `-gamma`. So `gamma = -Re(residue)`, independent of pole order.
- **Consequence:** the quantity the sister file `clm_calib.py` prints as "p" is in fact `gamma`.
  No numerical error in level-2a (the instrument correctly measured the spatial order = 1), only
  an ambiguous label. The paper's "p" is a different object (`= 1 - gamma = 0` for the CLM simple
  pole). This file prints `gamma` explicitly and cross-prints `p_Fourier = 1 - gamma` only for
  traceability.

Sanity table (spatial order our instruments should return):
  a = 0    -> gamma = 1  (simple pole)   ; Fourier p = 0
  a = 1/2  -> gamma = 2  (double pole)   ; Fourier p = -1
  a = 2/3  -> gamma = 3  (triple pole)   ; Fourier p = -2
  a = (n-1)/n -> gamma = n (order-n pole); other a in (0,1) -> branch point of order gamma.

## Profile tested (non-circular)
Exact a=1/2 self-similar solution (their Eq. 38, v_c = 1):

    Omega(xi) = (16/3) * xi / (xi^2 + 1)^2

Truth (verified by hand): DOUBLE poles at `xi = +-i` => `gamma_true = 2`, `delta_true = 1`.
`U'/U = (1 - 3 xi^2)/( xi (xi^2 + 1) )`: off-axis residue `-2` (=> gamma=2) at `xi=+-i`, and
residue `+1` at the REAL ZERO `xi=0` (discarded). By Theorem 3 of the paper, a=0 and a=1/2 are
the ONLY values with a pure closed-form leading-order singularity, so a=1/2 is the only
non-trivial closed-form `a != 0` calibration available; other a require the numerical profile
(the level-3 unknown). This test exercises a singularity ORDER (gamma=2) different from level-2a
(gamma=1), on a genuine `a != 0` PDE solution.

## Exact command
    cd ~/Desktop/oxieml-star && python3 clm_calib_ahalf.py

## Raw result (Anthony's machine, 2026-06-25)
    radial   : gamma = 2.0000   (delta given = 1.0)
    AAA      : delta = 1.0002   gamma = 1.9997
    AAA off-axis clusters (center, summed_res, n) : [(1j, -2.0, 3), (-1j, -2.0, 3)]
    AAA discarded (real-axis: zero of U / edges)  : [(-13.997, 0.0, 0.0), (14.003, 0.0, -0.0), (0.0, 0.0, 0.999)]
    VERDICT (tol=0.02): PASS

Both instruments recover (delta=1, gamma=2); they agree with truth and with each other. The
AAA split the simple `U'/U` pole into 3 nodes per side, re-summed by clustering to residue -2
(=> gamma=2). The real-axis zero (residue +1) is correctly discarded.

## NOT the cube (framing, settled)
A real-analytic profile continued to C is forced holomorphic (unique continuation); the SPARC
test passes. The question is location `delta` + order `gamma`, not holo vs anti. The orthogonal
axis is applied on the METHOD (read into the complex plane; extract the closed-form order;
cross-check two independent lenses).

## Open / not done
- **[PENDING] level-3 — real DeepMind/Gomez-Serrano numerical profile** (the unknown). For
  `a != 0, 1/2` there is no closed form (Theorem 3), so any further a is itself a numerical
  target and belongs to level 3, not calibration.
- Optional later refactor: merge `clm_calib.py` + `clm_calib_ahalf.py` into one `--a {0,0.5}`
  parametrized bench (separate, backup-first step; both standalone files are validated as-is).
