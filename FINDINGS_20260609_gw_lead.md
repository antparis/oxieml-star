# FINDINGS — Gravitational-wave lead (rank-1): course correction

**Date:** 2026-06-09 (CEST) · **Owner:** Anthony Monnerot · **Status overall:** [DERIVATION] — literature/maths sound, no eml-star execution yet · **Type:** framing before simulation (anti-reproduction method)

> Arbiter rule reminder: nothing here is [ESTABLISHED] for eml-star. No PySR run, no SymPy judge executed on this lead yet. This file records the FRAMING and a refuted working hypothesis, so the next session does not repeat it.

---

## 1. Context
Rank-1 open lead = gravitational waves. Natively-complex observable: strain h = h_plus - i h_cross, and Weyl scalar psi_4, decomposed on spin-weighted spherical harmonics {}_{-2}Y_lm. Goal (Project A): find anti-holomorphic structure FORCED by physics (not by an analysis/gauge choice), ideally transcendental and CHIRAL (anti part independent, not the mirror conjugate of the holo part).

## 2. Working hypothesis — REFUTED at the basis level [ESTABLISHED math]
Prior hypothesis: for generic azimuthal index m, the zeta-bar dependence of {}_{-2}Y_lm does NOT factorize into (holomorphic) x (real module), collapsing to a module only at the extremes m = ±l.

Refutation: in stereographic coordinate zeta, each term of {}_sY_lm has form zeta^n · zeta-bar^(n-m-s); the exponent difference (power of zeta) - (power of zeta-bar) = m+s is CONSTANT across the whole sum. Therefore one can ALWAYS factor a single phase monomial:
- {}_sY_lm = zeta^(m+s) · R(|zeta|^2) · (1+zeta·zeta-bar)^(-l)  if m+s >= 0
- {}_sY_lm = zeta-bar^(-(m+s)) · R(|zeta|^2) · (1+zeta·zeta-bar)^(-l)  if m+s < 0
with R a REAL polynomial in |zeta|^2. For s=-2: |m|<l is multi-term in zeta AND zeta-bar (so d/d(zeta-bar) != 0), BUT still reducible to zeta-bar^(2-m) · (real function of |zeta|^2). The whole l = |s| = 2 band is a single monomial for all m.
Examples (s=-2): (l=3,m=0) ~ zeta-bar^2·(1-|zeta|^2); (l=4,m=0) ~ zeta-bar^2·[1/96 - |zeta|^2/36 + |zeta|^4/96].

CONSEQUENCE for eml-star: the {}_{-2}Y_lm BASIS is module-trapped for ALL m. Any anti-holomorphic signal coming from the angular basis alone is an ARTEFACT (same module-trapping filter already used for optical vortices and Aharonov-Bohm). Genuine chirality must live in the COEFFICIENTS h_lm(t) (source physics), not in the angular expansion.

Sources: Goldberg-Macfarlane-Newman-Rohrlich-Sudarshan, J. Math. Phys. 8, 2155 (1967); stereographic form with (1+zeta·zeta-bar)^(-l) in Zlochower-Gomez-Husa-Lehner-Winicour, Phys. Rev. D 68, 084014 (2003), arXiv:gr-qc/0306098; convention/frame-phase subtlety in Boyle, J. Math. Phys. 57, 092504 (2016), arXiv:1604.08140.

## 3. eth-bar = Wirtinger on the sphere [ESTABLISHED]
eth-bar·eta = 2·P^(1+s)·d(P^(-s)·eta)/d(zeta-bar), with P=(1+zeta·zeta-bar)/2. So eth-bar IS, up to a conformal weight, the Wirtinger derivative d/d(zeta-bar) — i.e. the eml-star judge, already geometrically present in the Newman-Penrose / Geroch-Held-Penrose formalism. Refs: review arXiv:1801.01714; BMS lectures arXiv:2504.12521.

## 4. Top candidate — precessing-binary mode asymmetry [CONJECTURE for eml-star]
Boyle, Kidder, Ossokine, Pfeiffer, "Gravitational-wave modes from precessing black-hole binaries", 2014, arXiv:1409.4431. Key: "no rotation can eliminate asymmetries in waveforms from precessing systems"; dominant effect is a parity-violating asymmetry (>=3% amplitude modulation, can exceed 50% for massive systems), tied to recoil/kick. The mirror relation h_{l,m} = (-1)^m·conj(h_{l,-m}) (which would make h_cross mirror-locked to h_plus) is BROKEN and not restorable by any instantaneous frame. This matches the "forced by physics, non-reducible" criterion.
Supporting: Ramos-Buades et al. 2025 arXiv:2506.19911 (equatorial-asymmetric modes in SEOBNRv5PHM, dominant error source if omitted); precessing ringdown arXiv:2504.17021 (asymmetry "cannot be eliminated through rotation of the decomposition basis").
Fallback chirality sources: parity-violating propagation birefringence (arXiv:2305.10478; GWTC-3 constraints arXiv:2304.09025) — propagation effect, beyond-GR only; gravitational memory (mostly m=0, E-mode/parity-even, mirror-locked unless combined with precession).

## 5. Best data entry point [ESTABLISHED]
SXS third catalog, Scheel et al. 2025, arXiv:2505.13378 (3756 simulations), via Python package `sxs` (sxs.readthedocs.io, github.com/sxs-collaboration/sxs). Provides h_lm as NATIVE COMPLEX time series (real+imag per mode, s=-2, l=2..8), HDF5, extrapolated to scri+, CoM-corrected; memory included since v3.0.0 (h.remove_memory() available). Complement: MAYA catalog-2 arXiv:2309.00262 for rare eccentric+precessing configs. AVOID GWOSC/LVK strain h(t): real detector projection only -> SPARC trap if complexified after the fact.

## 6. Reducibility test (run BEFORE any simulation)
Anti-holo signature is an ARTEFACT if it vanishes under any of: (a) tetrad/null-frame change; (b) polarization-basis rotation (h_+ <-> h_x); (c) co-precessing / maximum-radiation frame (via `scri`); (d) h_cross -> 0. It is FORCED if it survives all.
CRITICAL trap: since the basis is always reducible, a naive d/d(zeta-bar) != 0 test on the full sum ALWAYS fires (trivial, gauge-removable). The discriminant is NOT "d/d(zeta-bar) != 0" but "does the chiral structure survive the co-precessing frame AND fail to factor into (global holomorphic)x(module) once the basis is normalized".
Protocol: 1) load a precessing SXS sim, extract complex h_lm(t); 2) compute mode asymmetry A_lm(t)=h_{l,m}-(-1)^m·conj(h_{l,-m}) (≈0 for aligned/non-precessing control; !=0 for precessing); 3) rotate to co-precessing frame (scri), recompute A_lm — if it survives (> ~3% and >> numerical noise ~1e-4 inter-resolution), inherent; 4) apply SymPy Wirtinger judge to the coefficient-borne factor after analytically factoring the reducible basis; target precessing (2,1),(3,2),(3,3),(2,0).
Decision threshold: if A_lm drops below ~1e-4 (noise) after co-precessing rotation, abandon that configuration; pivot to precessing ringdown (arXiv:2504.17021) or propagation birefringence (arXiv:2305.10478).

## 7. Novelty vs reproduction
Prior art closest: Tiglio & Villanueva 2021, arXiv:1911.00644 (free-form symbolic regression MODELS the (2,2) waveform, min overlap 99%) — but no holomorphic/anti-holomorphic analysis, no Wirtinger judge. PySR: Cranmer 2023 arXiv:2305.01582. No published PySR + exact Wirtinger judge (d/d(zeta-bar) via SymPy) on GW modes found (absence of evidence, not evidence of absence — reconfirm at write-up). eml-star value-added = NOT a waveform model but a detector of NON-REDUCIBLE chirality in precessing coefficients. Open niche.

## 8. ESTABLISHED vs CONJECTURE (summary)
[ESTABLISHED]: basis {}_{-2}Y_lm reducible for all m (m+s constant); eth-bar = d/d(zeta-bar); precessing mode asymmetry physical and frame-irreducible (arXiv:1409.4431, 2504.17021, 2506.19911); SXS = native complex h_lm; GWOSC = real strain (trap).
[CONJECTURE / open]: that precessing h_lm(t) coefficients carry a transcendental, chiral (mirror-independent) anti-holomorphic structure in the eml-star sense once basis is factored and co-precessing frame imposed. Asymmetry A_lm is established; its translation into an exploitable, non-reducible Wirtinger signature is NOT proven — this is the new work.

## 9. Next session (NOT done tonight)
- pip install sxs (PC Linux), download 2-3 strongly-precessing BBH + 1 aligned control.
- write mirror-asymmetry script A_lm(t) + co-precessing rotation (scri).
- only then: PySR + verify_exact.py on the coefficient factor.
No simulation launched on 2026-06-09; this file is framing only.
