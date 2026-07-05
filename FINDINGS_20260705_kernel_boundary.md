# FINDINGS 2026-07-05 — The one-way kernel has an intrinsic, dimensionless, FORCED boundary at |x|=1, EMERGENT from the infinite mode choir

## What
Anthony's "iceberg" question (is there a limit of the computable with structure
beyond, built from OUR tools, not grafted?) + his N-bubble question (what do
many bubbles do at that limit?). Framed as five panels on the published one-way
kernel K(x) = sum_{m>=1} k x^m / lambda_m^2, lambda_m = -kappa/2 - i m delta,
x = zbar*wbar (closed form: Lerch). Bears directly on OPEN QUESTION 3 of the
published paper (boundary behaviour of the closed form).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-05)
```
cd ~/Desktop/oxieml-star && timeout 200 python3 kernel_boundary_test.py
```

## Raw result (machine output, identical to sandbox)
A. INSIDE |x|<1: mode sum (N=6000) = closed form to 1.1e-16 / 1.8e-15 /
   1.1e-14 at x = 0.5 / 0.9 / 0.99. The choir sings; the identity holds.
B. BEYOND |x|>1: the SUM diverges (x=1.5: 8.4e5 -> 1.3e14 -> 1.3e31 at
   N=50/100/200) while the FUNCTION continues FINITE (|K|=2.53 at x=1.5,
   3.02 at x=2.0). The wall is a boundary of the SERIES, not of the object:
   the iceberg has a submerged part (analytic continuation).
C. N-EMERGENCE: every finite-N choir is wall-free (|K_N(1.5)| finite for all
   N up to 1000, reaching 3.7e170 yet finite). Effective wall x*(N) (1%
   truncation error): 0.904 at N=10, 0.9906 at N=30; beyond N=100 the wall
   sits closer to 1 than 1e-6 -- PROBE-SATURATED (bisection ceiling), noted
   honestly. The wall exists only at N=infinity and sharpens monotonically:
   it is an EMERGENT property of the infinite choir, contained in no bubble.
   (Domain-level instance of the sum-emergence law #004.)
D. N-ROBUST STAIRCASE: 4 anti-bubbles of orders 3,5,8,12 + holo z^2 give a
   5-step INTEGER winding staircase {+2,-3,-5,-8,-12}, deviation from
   integers 0.00e+00 at every radius. More bubbles = more steps, smallest
   move stays 1: the #037 integer-vs-continuum protection is N-robust.
E. THE TEAR (monodromy), validated route: dilogarithm control --
   disc Li_2(x) measured vs theory 2*pi*i*ln(x): 2.547612 vs 2.547612
   (x=1.5, diff 9.2e-9), exact at x=2.0, 4.6e-9 at x=3.0. [ESTABLISHED
   machine] for the dilog control. The kernel's own leading tear is quoted
   through the Lerch->dilog reduction at integer offset: status
   [DERIVATION] for the kernel-specific jump (mpmath's lerchphi was found
   branch-smooth on x>1 -- a library continuation choice -- so the direct
   eps-probe does not apply; the exact-reduction route is the honest one).

## Verdict
The certified anti-holomorphic object possesses an intrinsic boundary of
computability at the pure number |x| = 1:
  - DIMENSIONLESS: the only kind of wall a scale-free formalism admits
    (consistent with #038: no hbar/G/c, walls only at ratios);
  - FORCED: it comes from the mode-ladder geometry, not from a hand-inserted
    cutoff (#038 panel D showed grafted walls appear where the hand puts
    them; this one nobody put anywhere);
  - EMERGENT: absent from every finite choir, present only at N=infinity --
    the bubbles' true victory mode (the choir, never the pressure, cf #019);
  - STRUCTURED BEYOND: analytic continuation finite past the wall, with a
    discrete branch tear across x>1.
POSITIVE structural result (not a closure): first candidate material for the
paper's open question 3, i.e., for a possible boundary section of a future
one-way-kernel v3.

## Status
- Panels A-D + dilog control of E: [ESTABLISHED machine] (run 2026-07-05,
  identical to sandbox, no hardcoded verdict).
- Kernel-specific tear magnitude: [DERIVATION] (Lerch->dilog reduction).
- Scope: mathematics of OUR object. Says nothing about nature, nothing
  about the physical Planck scale. Resemblance to "wall + beyond" pictures
  is a shared FORM, not an identity.

## Traces
- kernel_boundary_test.py (harness, sandbox-tested, timeout-guarded)
- FINDINGS_20260705_planck_scale_closure.md (#038, the scale-free premise)
- FINDINGS_20260705_clock_dilation_closure.md (#037, protected by panel D)
- This file: FINDINGS_20260705_kernel_boundary.md
- Paper link: oneway-kernel Discussion, open question 3 (boundary behaviour)
