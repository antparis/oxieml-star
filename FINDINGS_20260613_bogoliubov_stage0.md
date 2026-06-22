# FINDINGS 2026-06-13 -- Bogoliubov-eml* Stage 0 VALIDATED (executed): neg-freq weight = beta

## What this is
First executed brick of the Bogoliubov/Casimir piste. Tests whether the negative-
frequency spectral weight of a mode equals the Bogoliubov mixing coefficient beta.
Origin: dynamical Casimir effect (moving mirror) transforms the field by a Bogoliubov
transformation b = alpha*a + beta*a-dagger, which MIXES a mode with its conjugate.
beta measures how much conjugate (anti-holomorphic) content is forced.
File: bogoliubov_stage0.py

## Test executed on Anthony's machine (PASS)
On synthetic mode alpha*e^{+iwt} + beta*e^{-iwt} (alpha^2 - beta^2 = 1), omega placed
EXACTLY on an FFT bin (no spectral leakage):
- beta=0 (static mirror): anti-holo weight = 1.53e-31 (machine zero). Negative control PASS.
- beta=0.5 (moving mirror): weight = 0.166667 = exactly beta^2/(alpha^2+beta^2) = 0.25/1.5.
  Detector does not just say "anti-holo present", it RECOVERS the exact value. PASS.
STAGE 0 VALIDATED.

## Status: [ESTABLISHED-userrun] -- but READ the scope carefully
What IS established: on a synthetic Bogoliubov mode, negative-frequency spectral weight
EQUALS beta^2/(alpha^2+beta^2), exactly (1e-31), with clean negative control (beta=0 -> 0).
The Bogoliubov structure is MEASURABLE and the detector recovers the value, not just a verdict.

## What this does NOT yet prove (critical -- do not oversell)
1. This is an FFT detector, NOT verify_exact.py's d/dzbar judge. We showed
   "neg-freq weight = beta". We did NOT show "Wirtinger d/dzbar = beta". The announced
   bridge is d/dzbar = beta; that homonymy test is the NEXT run and is unproven.
2. The mode is a pure exponential (easiest case). A real dynamical-Casimir mode has a
   finite-time envelope (mirror moves over a finite duration) that spreads the spectrum.
   Robustness off the exact-bin case is untested.

## Method notes (for the next session, avoid repeating 3 failed attempts)
- FFT SIGN CONVENTION is the trap: numpy.fft uses e^{+2pi i f t}, so e^{+iwt} lands in
  POSITIVE fftfreq bins. Pick the holo/anti assignment consistently with that.
- omega MUST sit exactly on an FFT bin (omega = 2 pi k / T) or spectral leakage spoils
  exactness. Three naive attempts (Milo: confused holo with real; two windows: sign-
  convention bug) all failed before this. The arbiter was the run, not reasoning.

## NEXT (the test that decides the whole piste)
Pass the SAME mode alpha*e^{+iwt}+beta*e^{-iwt} through verify_exact.py's d/dzbar judge
and check it returns the same beta as the FFT. If yes -> Wirtinger=Bogoliubov is a numeric
identity, not a homonymy, and there is something new. If no -> FFT and Wirtinger measure
different things and the bridge was a resemblance. Both outcomes are valuable. Cold session.

## UPDATE 2026-06-13 -- construction entry point for the NON-CIRCULAR test
Re-reading the deep-research audit of arXiv:2510.21636 (truncated photon) shows the
Hardy bridge is BETTER founded than "an idea to explore" -- though still [CONJECTURE].
The structural chain already exists in the literature:
- Single-photon modes are POSITIVE-FREQUENCY components only = Hardy-space condition
  = boundary values of functions holomorphic in the upper half-plane. Intrinsic U(1)
  phase (Bialynicki-Birula / Riemann-Silberstein photon wavefunction = natively-complex
  analytic signal). This is the principled t->(z,zbar) translation we were missing:
  Hardy/analytic-signal continuation, NOT the ad-hoc z=e^{iwt} that forces the result.
- The truncation paper's Bogoliubov kernels are explicitly C-SYMMETRIC (complex-
  conjugation kernels admitting SVD): the time-dependent boundary INJECTS the conjugate
  (negative-frequency = anti-holomorphic) sector into an initially holomorphic 1-photon
  state. So the physics forces the conjugate content -- it is not placed by hand.
- Non-localizability (Knight 1961; antilocality of Omega = c(-Delta)^{1/2}) is the same
  analytic-continuation obstruction that an anti-holomorphic detector probes.

## WHY this matters for the decisive test
The tautology we hit came from choosing the t->(z,zbar) map so that beta sits in front of
zbar by hand. The Hardy/analytic-signal continuation is an INDEPENDENT translation: it
maps t -> upper-half-plane WITHOUT assuming where beta goes. The real (non-circular) test
is: take the truncation-paper mode, continue it via Hardy (positive-freq projection), and
check whether verify_exact.py's d/dzbar detects the forced negative-frequency content
WITHOUT us having placed it there. Entry points: Knight 1961; Bialynicki-Birula photon
wavefunction; the paper's own C-symmetric Bogoliubov kernels. Status: [CONJECTURE], lead
for a dedicated cold session -- the bridge is theoretically supported but NOT demonstrated.
