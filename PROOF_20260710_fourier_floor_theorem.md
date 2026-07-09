# PROOF 2026-07-10 — The Fourier floor theorem (hand proof, #049)

Status: [DERIVATION -> THEOREM candidate]. All ingredients are classical
elementary analysis (equicontinuity, discrepancy bounds, Bohr almost
periodicity, Riemann-Lebesgue); the contribution is the exact assembly
fitted to the one-way tear relief, with each clause machine-faced by the
companion test (kernel_theorem_companion_test.py). No novelty is claimed
for the ingredients. Says nothing about nature.

## Setting

Fix a window I = [u_min, u_max] subset (0, infinity) (FIXED-WINDOW
CLAUSE: mandatory — growing windows change regime, cf. the
roughness/tide boundary, #046-D). A choir is a finite family of
frequencies nu_k in [a, b] subset [0, infinity) with weights w_k > 0
(complex weights: Corollary 3). Its normalized profile is

    P_N(u) / W_N = | mu_hat_N(u) |,    mu_hat_N(u) = int e^{i nu u} dmu_N,

where mu_N = (1/W_N) sum_k w_k delta_{nu_k}, W_N = sum_k w_k, is the
weighted winding measure. The contrast functional on C(I, R_{>=0}) is
K(f) = (max f - min f) / (max f + min f).

## Theorem 1 (Fourier floor law, fixed window)

Let mu be a probability measure on [a, b] and (mu_N) probability
measures on [a, b] converging weakly to mu. Then:
 (i)  mu_hat_N -> mu_hat uniformly on I;
 (ii) K(|mu_hat_N|) -> K(|mu_hat|), the denominator being protected:
      max_I |mu_hat| > 0 always.

Proof. (i) Pointwise convergence: for fixed u, nu -> e^{i nu u} is
continuous and bounded on [a, b]; weak convergence gives
mu_hat_N(u) -> mu_hat(u). Equicontinuity: for all N and u, u' in I,
|mu_hat_N(u) - mu_hat_N(u')| <= sup_nu |e^{i nu u} - e^{i nu u'}|
<= b |u - u'|, a uniform Lipschitz bound. A pointwise-convergent,
uniformly Lipschitz sequence on a compact interval converges uniformly
(cover I by finitely many delta-balls; standard 3-epsilon argument).
(ii) f -> K(f) is continuous in sup norm at every f with
max f + min f > 0. Protection of the denominator: mu_hat extends to an
entire function of u (Fourier transform of a compactly supported finite
measure, Paley-Wiener elementary half); mu_hat(0) = 1, so mu_hat is not
identically zero; an entire function not identically zero cannot vanish
on a set with an accumulation point, hence |mu_hat| > 0 somewhere on I,
so max_I |mu_hat| > 0. Then K(|mu_hat_N|) -> K(|mu_hat|) by (i). QED.

Remark (what the theorem says for the registry). The roughness floor of
a large choir IS the window-contrast of the Fourier transform of its
weighted winding measure: #046-B ("the shape decides") is definitional;
#047-D (foam asymmetry) is the reweighting of mu; there is no universal
convergence exponent (#046-C), only a distance to the limit (Lemma 2).

## Lemma 2 (rate: quantile sampling converges like 1/N)

Let mu have CDF F and let mu_N put mass 1/N at quantile nodes
nu_k in F^{-1}([(k-1)/N, k/N]). Then the Kolmogorov discrepancy is
D_N <= 1/N, and for every u in I, since nu -> e^{i nu u} has total
variation <= u(b - a) + 2 on [a, b] (real and imaginary parts are
monotone-by-pieces with |g'| <= u), a Koksma-style bound gives

    | mu_hat_N(u) - mu_hat(u) | <= C(I) / N,   C(I) ~ u_max (b - a).

Hence |K_N - K_infinity| = O(1/N) as a GENERAL BOUND.
REFINEMENT (machine-taught, sandbox 2026-07-10): the bound is not
tight for midpoint quantile nodes t_k = (k - 1/2)/N -- for a smooth
density the midpoint rule is second order, O(1/N^2), observed slope
-2.00; endpoint nodes t_k = k/N keep a boundary term of true order
1/N (predicted slope -1). The approach speed belongs to HOW the
choir samples its measure, not to the measure alone. The constant
C blows up with u_max and with the measure's concentration (peaked
densities have large effective variation once reweighted) — which is
why the linear grid, whose nu-density is concentrated like 1/nu^2 near
a, is still a factor ~2 from its limit at N = 64 (#048-F). The dead
exponent p = 0.188 of #046-C was a chord of this 1/N approach read over
a short N-range; it never was a law. [Machine-faced: companion panel A.]

## Theorem 3 (fate of the tides: the atomic/continuous dichotomy)

 (a) ATOMIC (finite choir): mu_hat is a finite trigonometric sum, hence
     Bohr almost periodic; every value configuration recurs within
     epsilon infinitely often. In particular the deep rendezvous of
     #044 recur forever: THE TIDES ARE ETERNAL for any finite choir.
     (Classical Bohr theory; no novelty claimed.)
 (b) ABSOLUTELY CONTINUOUS mu (the true continuum): by the
     Riemann-Lebesgue lemma, mu_hat(u) -> 0 as u -> infinity. On far
     windows the whole profile dies: THE TIDES ARE MORTAL in the
     continuum; the tear heals at large scale. For a density smooth on
     [a, b] with a > 0, integration by parts gives the rate
     |mu_hat(u)| = O(1/(u a)).
Consequence: the log-periodic rendezvous of #044 are a DISCRETENESS
phenomenon of the choir. A finite ladder keeps its calendar forever; a
continuum of windings forgets it. [Machine-faced: companion panel B —
a genuinely new, falsifiable prediction produced by the orthogonal pass
on the theorem itself.]

## Corollaries

 C1 (Reciprocal as theorem). All nu_k = 0 means mu = delta_0, so
    mu_hat = 1 identically: zero relief on every window. The one-way
    differential follows from the law; the empirical controls of
    #040-#048 were instances of this line.
 C2 (Estimator robustness). Uniform convergence (Thm 1.i) transfers to
    ANY estimator continuous in sup norm (contrast, RMS ripple over
    mean, etc.): the law does not depend on our choice of contrast.
    [Machine-faced: companion panel C.]
 C3 (Complex weights). For complex w_k, mu_N is a finite complex
    measure; Theorem 1 holds verbatim with W_N = sum |w_k| and weak
    convergence of complex measures; the phase switches of #042 are
    reweightings of a complex mu. The denominator protection now needs
    mu_hat not identically zero, i.e. mu != 0 as a measure.

## Perimeter and honesty

- Fixed window mandatory (clause of Thm 1); growing windows leave the
  theorem's scope and enter the tide regime.
- N = infinity proxies in machine tests (quantile choirs) are valid
  while u << N (discrepancy bound of Lemma 2 at the far window's u).
- The ingredients are textbook; the assembled statement, its fit to the
  one-way tear, and the dichotomy's consequence for #044 are what is
  registered. Status upon machine-facing of panels A-D:
  Theorem 1 + Lemma 2 + Theorem 3 = [THEOREM (elementary), machine-faced].

## Traces
- kernel_theorem_companion_test.py (the falsifiable face: slope -1,
  death of the tides in the continuum, estimator robustness)
- FINDINGS_20260710_fourier_floor_law.md (#048, the law proven here)
- This file: PROOF_20260710_fourier_floor_theorem.md
