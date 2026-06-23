# FINDINGS 2026-06-23 — Multi-axis fingerprint tool (meta-method of the orthogonal axis)

**Status:** [ESTABLISHED] tool calibration (axis 0 == judge on 11 forms) · [DERIVATION] occupancy reading.

## What was built and tested

`axis_fingerprint.py` — a META-TOOL operationalizing the general method behind the orthogonal
axis: take the invariant every past attempt held FIXED and vary it. The tool makes the stack of
silently-fixed invariants EXPLICIT and MEASURABLE as a coordinate system, and reports which cells
of the multi-axis grid are EMPTY of a physically-realized form (= new hunting grounds).

Fingerprint axes per closed form f(z, zbar):
- axis 0  verdict       : judge_v2 (HOL / ANTI / REAL_TRAPPED / MODULE_TRAPPED) — AUTHORITY
- axis 1  poly_anti     : smallest q with (d/dzbar)^q f = 0, else oo   (poly-analytic / "branch" axis)
- axis 2  poly_holo     : smallest p with (d/dz)^p f = 0, else oo
- axis 3  spin          : eigenvalue of R = z d/dz - zbar d/dzbar (if eigenstate)  (orthogonal axis)
- axis 4  sigma_std_real: real under standard conjugation z<->zbar
- axis 5  sigma_inv_real: real under inversion-conjugation z->1/zbar  (generalized reality axis)

Extensible by design: a new technique = one new function in AXES.

## Exact command

cd ~/Desktop/oxieml-star && python3 axis_fingerprint.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine)

axis 0 (real judge_v2) is IDENTICAL to the internal oracle on all 11 corpus forms. EXIT=0.

form               verdict        poly_anti  poly_holo  spin   sig_std  sig_inv  phys
ctrl_holo          HOL            1          3          2      False    False
ctrl_anti          ANTI           oo         1          n/a    False    False
ctrl_real          REAL_TRAPPED   2          2          0      True     False
ctrl_module        MODULE_TRAPPED oo         2          2      False    True
zbar_affine        ANTI           2          1          -1     False    False
zbar_quad          ANTI           3          1          -2     False    False
landau_n1          MODULE_TRAPPED oo         oo         -1     False    False    phys
tmg_left           HOL            1          oo         n/a    False    False    phys
jordan_r2_spin     MODULE_TRAPPED oo         oo         -1     False    False    phys
target_unpaired    ANTI           oo         oo         n/a    False    False
inv_real_probe     REAL_TRAPPED   oo         oo         0      True     False

Tool calibrated: axis 0 == judge. [ESTABLISHED]

## Occupancy reading — [DERIVATION]

1. All physically-realized forms cluster in HOL and MODULE_TRAPPED. No physical form
   occupies any ANTI cell. The chiral cell emptiness, seen geometrically on the grid.
2. All four genuine-ANTI target cells are EMPTY of physical occupants:
   - ANTI x poly_anti=N2(finite) x spin!=0   (candidate: polyanalytic Ginibre/Bergman kernel)
   - ANTI x poly_anti=N3(finite) x spin!=0
   - ANTI x poly_anti=transcendental x spin!=0   (the spinful-unpaired log target)
   - ANTI x poly_anti=transcendental x spin=0
   Only toy monomials (zbar, zbar^2) and the hypothetical target occupy ANTI cells.
3. Reality-axis flip: z/zbar is MODULE_TRAPPED under sigma_std but REAL under sigma_inv.
   Chirality is sigma-relative; a system forcing sigma_inv as its reality condition would
   reclassify the object. New testable axis (B).

## New techniques imagined (meta-method = break a silently-fixed invariant)

- A  poly-analytic order N   : CODED. Open door: physically-FORCED finite-N>=2 anti
                               (non-harmonic; Landau Fock states are module walls). [CONJECTURE]
- B  generalized reality sigma : CODED. Chirality is sigma-relative. [CONJECTURE]
- C  integrability (Newlander-Nirenberg) : non-integrable almost-complex J (Nijenhuis != 0) forces
                               non-removable d-bar != 0. Strongest SPARC-pass. Needs J-input. [CONJECTURE, separate build]
- D  several complex variables / Dolbeault cohomology : anti as H^{0,q>=1} class = topologically
                               forced, non-removable by construction. Highest potential. [CONJECTURE, biggest build]
- E  analytic continuation in a complex parameter : causality -> Kramers-Kronig = mirror relation.
                               Likely a WALL (real-trapped-like). [CONJECTURE/probable wall]

## Holo / anti ledger update (systematic)

- HOL confirmed (physical): tmg_left (stress-tensor log sector). Earlier: Landau n=0, Kirsch holo side.
- ANTI confirmed (physical, measurable observable): still ZERO.
- Walls reconfirmed (physical): MODULE_TRAPPED = landau_n1, jordan_r2_spin; HOL = tmg_left.
- New structural fact: reality is sigma-relative (z/zbar flips std<->inv).

## Next concrete lead (CERTIFIER mode, frame-before-simulate)

Apply axis A to the polyanalytic Ginibre kernel (non-Hermitian random-matrix physics, natively
complex, forced): candidate for the EMPTY cell ANTI x finite-N x spin!=0. Closed form -> judge.

## Files

- axis_fingerprint.py (meta-tool, calibrated)
- this trace
