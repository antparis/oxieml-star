# FINDINGS 2026-07-10 — Inverse problem (#051): the theorem becomes an INSTRUMENT — one-way spectroscopy reads the hidden choir from its relief, and ships with its limits proven on day one: exactly mirror-blind, aperture set by the window (u ~ 1/speed), mute on the reciprocal by design

## What
The #050 dictionary read backwards (Anthony's pick, idea-list #053):
a hidden finite choir generates a measured relief; the inverter fits the
three closed forms and must name the family and recover [a, b]. Five
panels: blind identification, the reflection ambiguity (hand identity),
noise, the reciprocal guard, and the window-aperture resolution born
from the orthogonal pass on this test's own failures.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-10)
```
cd ~/Desktop/oxieml-star && timeout 500 python3 kernel_inverse_test.py
```

## Raw result (machine output, identical to sandbox)
A. BLIND IDENTIFICATION (clean, hidden N=64, truth [1/300, 1/3]):
   hidden logu  -> WINNER logu CORRECT (a 1.34%, b 0.11%).
   hidden invsq -> WINNER logu INCORRECT: the degenerate logu fit
     (a -> 0, residual 3.50e-09) mimics the inverse-square (6.93e-08).
     [Auditor prediction "the right family wins every time" PARTIALLY
     REFUTED — near-edge degeneracy: as a -> 0 the log-uniform measure
     concentrates at the slow edge and impersonates 1/nu^2.]
   hidden unif  -> WINNER unif CORRECT (b 0.21%; a 20.23% — the slow
     edge already fragile on clean data).
B. REFLECTION AMBIGUITY: max |relief - mirrored relief| = 5.66e-15 —
   machine zero, confirming the hand identity mu_hat_mirror =
   e^{i(a+b)u} conj(mu_hat). MODULUS-ONLY DATA CANNOT DISTINGUISH A
   CHOIR FROM ITS MIRROR: an exact, proven bound of the spectroscopy,
   graved instead of hidden.
C. NOISE (hidden logu, short window): b robust (1.35% / 5.74% at 1%/5%
   noise), a FRAGILE (29.42% / 75.74%). The slow edge barely writes.
D. RECIPROCAL GUARD: flat relief -> contrast 0.00e+00 < protocol floor
   1e-4 -> INVERSION REFUSED. No structure, no reading; the reciprocal
   is unreadable BY DESIGN, and the instrument knows it.
E. THE WINDOW IS THE APERTURE (orthogonal axis on A/C: the parameter
   held fixed was the WINDOW; information about a winding speed lives
   at u ~ 1/speed — slow needles rotate ~0.02 rad on the short window
   and write nothing, hence unreadable a AND family confusion at the
   slow edge):
   E1. hidden invsq, N=1024, window [0.05, 300] (validity u << N):
       WINNER invsq CORRECT — residual 9.87e-04 vs logu 3.08e-02 (30x
       separation); a 0.10%, b 2.23%. The family confusion RESOLVED.
   E2. hidden logu, 1% noise, long window: a 0.02% (vs 29.42% short),
       b 0.04%. The slow edge becomes readable.

## Verdict — the instrument and its notice
ONE-WAY SPECTROSCOPY EXISTS AND WORKS: the composition of an invisible
choir is read from its relief alone, noise included. It ships with its
limits PROVEN on day one:
 (1) exactly MIRROR-BLIND (reflection identity, machine zero);
 (2) APERTURE = THE WINDOW: u ~ 1/speed per voice; short windows read
     only the fast edge (the partial-rotation regime of #048, now an
     instrument law); extending the window opens the aperture;
 (3) MUTE ON THE RECIPROCAL by design (the guard refuses).
Sixth full methodological cycle of the arc: prediction announced ->
machine-refuted -> orthogonally diagnosed -> diagnosis promoted to law
-> law machine-confirmed.

## Status
- Panels A-E: [ESTABLISHED machine] (run 2026-07-10, identical to
  sandbox; failures reported verbatim, no verdict hardcoded).
- Mirror identity and window-aperture law: [DERIVATION] hand arguments,
  machine-faced by panels B and E.
- Fit machinery: grid + Nelder-Mead over (log a, log(b/a)); modulus-only
  objective; scipy sici.
- Says nothing about nature or real spectroscopy. Shared FORM, never
  identity.

## Opens (traced, not started)
- Multi-window inversion (combine short + long windows: full-range
  reading with finite data; the practical instrument).
- Degeneracy penalty or model-selection criterion (AIC-style) for
  near-edge impersonation on short windows (E resolves it physically;
  a statistical guard would be belt-and-braces).
- Weighted-measure inversion (recover w(nu), not only [a, b]): the full
  spectroscopy, ill-posedness to frame.
- Carried: DSI prior-art FINDINGS before v3; q-family closed forms.

## Traces
- kernel_inverse_test.py (harness; the partial refutation and its
  resolution documented inside)
- kernel_closed_floors_test.py (#050, the dictionary)
- PROOF_20260710_fourier_floor_theorem.md (#049, validity clause u << N
  used by panel E)
- This file: FINDINGS_20260710_inverse_problem.md
