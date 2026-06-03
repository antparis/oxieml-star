# FINDINGS 2026-05-30 -- Time-reversal, chirality, and where anti-holomorphic data really is

## Origin
Late-night reasoning thread (Anthony Monnerot) linking the arrow of time to the
holomorphic / anti-holomorphic split of eml / eml*. Goal of this trace: keep the
SOUND parts, mark the speculative parts, and connect them to a concrete test.

## What is mathematically ESTABLISHED
- Wirtinger operators: d/dz = 1/2(dx - i dy), d/dz_bar = 1/2(dx + i dy).
  Holomorphic <=> d/dz_bar f = 0 ; anti-holomorphic <=> d/dz f = 0.       [ESTABLISHED]
- Rotation sense = holo/anti distinction: multiply by e^{i t} (one sense) is
  holomorphic, conjugation / e^{-i t} (other sense) is anti-holomorphic.   [ESTABLISHED]
- Time reversal t -> -t, after Wick rotation, acts as z <-> z_bar, i.e. it
  SWAPS holomorphic and anti-holomorphic. The user's "if time flips, anti
  becomes holo" is exact.                                                  [ESTABLISHED]
- Optical vortex of topological charge l: amplitude ~ z^l * exp(-|z|^2/w^2)
  for l>0 (holomorphic phase part) and ~ conj(z)^|l| * exp(-|z|^2/w^2) for
  l<0 (anti-holomorphic). The SIGN of the charge IS the chirality and IS the
  holo/anti distinction. Verified numerically (antiholo_probe):
    l=+3, envelope removed -> anti-fraction A = 0.031 (holomorphic z^3)
    l=-3, envelope removed -> anti-fraction A = 0.969 (anti-holomorphic z_bar^3)
    raw beams (envelope in) -> A ~ 0.5 for BOTH (structure masked)
    shuffled control        -> A ~ 0.5 (no false positive)                 [ESTABLISHED, numeric]

## The user's thesis, now demonstrated
"Science flattens natively-complex data and loses the anti-holomorphic part."
DEMONSTRATED on the optical vortex: the anti-holomorphic signature is invisible
in the raw beam and only appears after an analysis choice (dividing the known
Gaussian envelope). How the data is treated decides whether the structure is seen.

## What is NOT established (speculation, kept as such)
- "Our universe is holomorphic, there is a hidden anti-holomorphic universe":
  NOT supported. In a single complex field, holo and anti parts both live in the
  SAME measurable world simultaneously; they are components, not two universes. [CONJECTURE / metaphysical]
- "Mass <-> holomorphic, time <-> holomorphic, no mass/no time -> anti-holomorphic":
  NOT a theorem. Mass is a positive scalar, not a field with a 'mirror'. The
  question "mirror of mass" is not well posed yet.                          [CONJECTURE]
- Universe rotation: observationally constrained to be extremely small /
  consistent with zero (CMB bounds). Not a usable mechanism.                [HEURISTIC, against]
- "Great Attractor pulls / sets the arrow of time": FALSE premise. The Great
  Attractor is an ordinary gravitational mass overdensity, fully conventional,
  unrelated to the arrow of time.                                          [ESTABLISHED FALSE]

## Where genuinely anti-holomorphic, MEASURABLE data is (the 'fuel' map)
Honest ranking. Key correction: anti-holomorphic data is NOT unmeasurable; it is
measurable but usually projected away. The strong, unambiguous signal is in
systems with intrinsic chirality, NOT in lensing.
  (A) Cosmic shear epsilon = e1 + i e2 (KiDS, in hand): spin-2, native complex.
      E/B decomposition ~ holo/anti split. BUT published B-mode null tests on
      KiDS-1000 are consistent with ZERO (p 0.04-0.68). Lensing is holomorphic
      to leading order; anti part (B-mode) is a faint correction. Detector
      per-galaxy floor ~0.02 at sigma=0.27 -> MUST average on a pixel grid.   [ESTABLISHED]
  (B) CMB polarization P = Q + i U: spin-2, real data. Primordial B-modes NOT
      yet detected (the cosmological holy grail).                            [ESTABLISHED]
  (C) Optical vortices / OAM beams: chirality = holo/anti, lab-measurable
      (interferometric fork fringes). Charge < 0 = real anti-holomorphic data. [ESTABLISHED]
  (D) Chiral condensed matter: superfluid/BEC vortices, quantum-Hall edge
      states, topological insulators. Chirality built in.                    [ESTABLISHED]

## Tools produced
- antiholo_probe.py : cheap Wirtinger 'fuel gauge' (no PySR). Anti-fraction
  A = median|d/dz_bar| / (median|d/dz| + median|d/dz_bar|). Pre-filter for real
  data before any expensive symbolic-regression run.
- optical_vortex_gen.py : physically-honest test case (LG beams +l vs -l),
  demonstrating chirality <-> holo/anti and the envelope-removal analysis effect.

## Next gate
- No new heavy run until Linux cooling is fixed (heatwave, room ~28C, thermal
  cutoff). All work above is CPU-cheap and already done.
- When cool: (1) finish vortex_N1 detector test (level-1 capability check), then
  (2) run antiholo_probe on KiDS pixel-averaged shear as a real-data fuel gauge.
- Reminder: level-1 = known target = capability demo, NOT a discovery.

## RESULT 2026-05-31 [ESTABLISHED] -- vortex_N1 detector + judge
Single-vortex chiral field, target a*log(z-c) + b*log(zbar-cbar).
- Run: kirsch_stack.run_one, niter=30 pop=300 maxsize=25 (corrected toolbox, anti-monster brakes).
- best_mse = 2.69e-18  (mse_below_1e-3 = TRUE, 15 orders below threshold)
- complexity = 21; center c recovered exactly: log(z - 1.0958 + 0.2445i).
- PySR encoded the anti term via my_imag (Im hides conj); NOT directly visible as emlstar.
- JUDGE verify_exact.py --formula: df/d(zbar) = (-1.1842 - 0.4015i)/(zbar - cbar) != 0
  VERDICT: ANTI-HOLOMORPHIC (exact SymPy, infinite precision).
- All three guard-rail conditions met: on-machine + MSE exploitable + SymPy judge certified.
STATUS: [ESTABLISHED]. Detector capability on REACHABLE chiral target proven end-to-end.
CAVEAT: level-1 (known generated target) = capability demo, NOT a discovery.
Confirms intuition: chirality (privileged rotation) => detectable z-bar signature.
