#!/usr/bin/env python3
"""
verify_decomposition.py

Independent numerical verification of the decomposition found by PySR
in Phase 1 of eml_star_decomposition.py.

Tested identity (no conj used):

  emlstar(z, w) = my_real(2*exp(z) - log(w**2)) + log(w) - exp(z)

where emlstar is taken from pysr_stacking.py line 135:

  emlstar(x, y) = exp(conj(x)) - log(conj(y) + 1e-30)

Test conditions:
- N=10000 points (5x larger than training set)
- Seed=123 (different from training seed=42)
- Same domain guards: |Re|, |Im| <= pi - 0.05 ; |w| >= 0.1
"""

import numpy as np

N = 10000
DOMAIN_HALF_WIDTH = np.pi - 0.05
W_MIN_MODULUS = 0.1
EMLSTAR_LOG_EPS = 1e-30

SEED = 123  # different from training seed=42


def emlstar_ground_truth(z, w):
    """Reference emlstar from pysr_stacking.py line 135."""
    return np.exp(np.conj(z)) - np.log(np.conj(w) + EMLSTAR_LOG_EPS)


def emlstar_decomposition(z, w):
    """Decomposition discovered by PySR (no conj used)."""
    return np.real(2 * np.exp(z) - np.log(w ** 2)) + np.log(w) - np.exp(z)


def main():
    rng = np.random.default_rng(SEED)

    re_z = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=N)
    im_z = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=N)
    z = re_z + 1j * im_z

    re_w = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=N)
    im_w = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=N)
    w = re_w + 1j * im_w
    bad = np.abs(w) < W_MIN_MODULUS
    while np.any(bad):
        k = int(bad.sum())
        re_new = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=k)
        im_new = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=k)
        w[bad] = re_new + 1j * im_new
        bad = np.abs(w) < W_MIN_MODULUS

    y_truth = emlstar_ground_truth(z, w)
    y_decomp = emlstar_decomposition(z, w)

    diff = y_truth - y_decomp
    mse = np.mean(np.abs(diff) ** 2)
    max_abs_err = np.max(np.abs(diff))

    print(f"[verify] N={N} samples, seed={SEED}")
    print(f"[verify] MSE (truth vs decomposition): {mse:.6e}")
    print(f"[verify] Max absolute error: {max_abs_err:.6e}")
    print(f"[verify] First 3 truth values: {y_truth[:3]}")
    print(f"[verify] First 3 decomp values: {y_decomp[:3]}")
    print(f"[verify] First 3 diffs: {diff[:3]}")

    if mse < 1e-25:
        print("VERIFICATION_STATUS: OK — decomposition is exact at machine precision")
    elif mse < 1e-10:
        print("VERIFICATION_STATUS: PARTIAL — small numerical drift, formal proof needed")
    else:
        print("VERIFICATION_STATUS: FAIL — decomposition is not exact")


if __name__ == "__main__":
    main()
