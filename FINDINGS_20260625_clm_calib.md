# FINDINGS — CLM exact-profile calibration of the complex-singularity instruments

**Date:** 2026-06-25
**Status:** [ESTABLISHED] (level-2a) — executed on Anthony's machine; both instruments agree
with truth AND with each other (tol 2%).
**Files:** `clm_calib.py` (standalone; does NOT touch the validated `complex_singularity.py`).

## What was tested
The two complex-singularity instruments — (I) radial log-log on `Omega(i s) ~ (delta - s)^(-p)`,
(II) AAA rational approximation of `U'/U` formed from SAMPLES (numerical derivative), poles +
residues — calibrated on a REAL fluid-model PDE solution in closed form, distinct in shape from
the synthetic toys of `complex_singularity.py --toys`.

## Profile (non-circular target)
Exact Constantin-Lax-Majda (CLM) self-similar profile (Elgindi-Jeong) of `omega_t = omega H[omega]`:

    Omega(x) = -2x / (1 + x^2)

Truth, verified by hand (not just cited): nearest complex singularities are SIMPLE POLES at
`x = +-i`  =>  `delta_true = 1.0`, spatial exponent `p_true = 1.0` (pole order 1; `U'/U` residue
`-1`). Checks: `Omega(i s) = -2 i s /(1 - s^2) ~ -i/(1-s)` as `s->1^-`; and
`U'/U = (1 - x^2)/(x (x^2 + 1))` has poles at `x=0` (res `+1`, the REAL ZERO of Omega) and
`x=+-i` (res `-1`, the genuine off-axis singularities).

Why this is not circular: it is a genuine PDE solution, a different functional form from the
power-law toys, and it introduces a REAL-AXIS ZERO at `x=0` (an extra `U'/U` pole, residue `+1`)
that the AAA instrument must discard — a wrinkle the toys did not have.

## Exact command
    cd ~/Desktop/oxieml-star && python3 clm_calib.py

## Raw result (Anthony's machine, 2026-06-25)
    radial   : p = 1.0016   (delta given = 1.0)
    AAA      : delta = 1.0000   p = 0.9998
    AAA off-axis clusters (center, summed_res, n) : [(1j, -1.0, 2), (-1j, -1.0, 2)]
    AAA discarded (real-axis: zero of U / edges)  : [(12.004, -0.0, -0.0), (-11.996, 0.0, 0.0), (-0.0, 0.0, 1.0)]
    VERDICT (tol=0.02): PASS

Both instruments recover (delta=1, p=1); they agree with truth and with each other. The real-axis
zero of Omega (U'/U residue +1 at x=0) is correctly discarded.

## Two bugs found and fixed in sandbox before delivery
1. **Radial window too wide.** `|Omega(i s)|` carries a slowly-varying prefactor `2s/(1+s) -> 1`
   that biases a wide log-log fit (first run gave p=1.073). Fixed: fit on a near-singularity
   log-spaced band `d = delta - s in [1e-5, ~0.05]*delta`, where the prefactor is ~constant.
2. **AAA splits the simple pole.** AAA represented the single pole at `x=i` (residue -1) as a
   DOUBLET (two poles near +-0.02+i, residue -0.5 each), reading p=0.4999. Fixed: greedy-cluster
   nearby poles and SUM residues per cluster before reading `p = -Re(sum residue)`. Generic AAA
   behavior; clustering is the robust fix for the eventual noisy real-data pipeline.

## Framing (settled)
NOT the cube. A real-analytic profile continued to C is forced holomorphic (unique continuation);
the SPARC test passes. The question is location `delta` + exponent `p`, not holo vs anti. The
orthogonal axis is applied on the METHOD (read into the complex plane; extract the closed-form
exponent; cross-check two independent lenses), not on the object.

## Open / not done
- **[OPEN] level-2b — gCLM law `p = -a/(1-a)`** (Lushnikov-Silantyev-Siegel). Blocked until the
  convention map `p_Fourier <-> p_spatial` is pinned (the law's `p` is a Fourier exponent, not the
  spatial pole order the instruments measure — cousin of the lambda != p trap) AND a closed-form
  `a != 0` profile is found to feed the instruments. Not coded, to avoid a calibration that looks
  right while being wrong.
- **[PENDING] real DeepMind/Gomez-Serrano numerical profile** (the unknown) — only after 2a + 2b.
