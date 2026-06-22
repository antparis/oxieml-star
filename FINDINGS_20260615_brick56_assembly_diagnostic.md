# FINDINGS 2026-06-15 -- [DERIVATION/LIMITE] Brick 5+6 assembly of the Qu-Lu-Ding T' lepton model: neutrino sector reproduced to 0.4%, charged-lepton sector blocked on triplet relative normalization. Next action = authors' reference notebook.

## What this is
Assembly of the full lepton model (M_e 3x3, M_D 2x3, M_N 2x2) of Qu-Lu-Ding 2506.19822 eq. 4.3,
seesaw m_nu = -M_D^T M_N^{-1} M_D, diagonalization, PMNS extraction, calibrated against Table 2
"Without gCP NO" best-fit (tau=-0.1563+1.108i, beta/alpha=4.896, gamma/alpha=3.267e-3,
|g2/g1|=0.2946 arg=1.888pi). This is the step BEFORE the g1=0 ablation test. NOT an ablation result.

## What WORKS (established by execution on Anthony's machine)
- All 4 form bricks calibrated independently (a0=0.1132; Feruglio; harmonic Delta1; shadows xi0/xi1).
- Seesaw STRUCTURE correct: Delta m21^2 / Delta m31^2 = 0.02991 vs target 0.02981 (0.4%), and the
  lightest neutrino mass m1 = 0 (NO, 2 RH neutrinos) -- exactly the Table 2 prediction.
  => M_D (bricks 4), M_N (weight-4 triplet), seesaw are correct.
- PMNS extraction routine VALIDATED on a known controlled case (built U, diagonal M_e):
  recovers sin2_12=0.308, sin2_13=0.022, sin2_23=0.470 exactly. The method is sound.

## What is BLOCKED (charged-lepton / mixing sector)
At the published best-fit the model gives (validated Takagi convention Mnu Mnu^dag):
  sin2_th12 = 0.240 (target 0.308), sin2_th13 = 0.031 (target 0.02215), sin2_th23 = 0.458 (0.470),
  m_e/m_mu = 0.00534 (target 0.004737), m_mu/m_tau = 0.0633 (target 0.05882).
Angles are right order of magnitude (th23 within 3%) but do not match Table 2.

## Causes ELIMINATED (each tested, not assumed)
- Row permutations of M_e: scanned all, m_mu/m_tau insensitive -> not it.
- Component indexing of triplets in M_e: scanned all 6^3, m_e/m_mu converges to <1% (0.004765 vs
  0.004737) but m_mu/m_tau stays 0.0633 regardless -> not the cause of the residual.
- q-series truncation of weight-0 form: stable at NT=8 (NT=20,50 identical) -> not it.
- PMNS extraction method: validated on known case -> not it.
- Takagi convention: corrected to Mnu Mnu^dag (left rotation), improved angles -> applied.

## Causes FIXED (real errors found and corrected)
- Weight-0 form: was using eq. C.32 of 2406.02527 (older paper, with nonholo e^{-4pi n y}/q^n terms);
  the MODEL uses eq. 3.21 of 2506.19822, where Y3,2 and Y3,3 are PURELY holomorphic (q only) and
  only Y3,1 carries the nonholo y + (q+qbar) part. Corrected; changed values, did not fully converge.
- All triplets must derive from the SINGLE weight-1 holomorphic doublet (Y1,Y2) via T' tensor
  products (eq. D.22 Y3^(2)=(Y2^2, sqrt2 Y1Y2, -Y1^2); eq. D.24 Y3^(4)). Confirmed structure.

## Localized remaining cause [DERIVATION]
m_mu/m_tau (and hence the mixing angles via M_e diagonalization) is fixed by the RELATIVE
NORMALIZATION between the weight-2 and weight-4 triplets. The bare tensor products (D.22/D.24)
carry the right STRUCTURE but not Qu-Ding's normalization convention (Fourier coeff of y^{1-k}
set to 1/(1-k)). The published gamma/alpha=3.267e-3 assumes THEIR normalization. Eq. 3.18 gives
the normalized prefactors but has apparent 0/0 singularities at physical even weights (k=1: 3-3^{2k-1}=0;
k=2: zeta(2-2k)=zeta(-2)=0), so it is not directly evaluable term-by-term -- needs limits.

## Decision / next action
The reliable source for the exact normalized q-expansions is the authors' reference Mathematica
notebook PHMF_integer.nb (ref [84], http://staff.ustc.edu.cn/~dinggj/supplementary_materials/PHMF_integer.nb).
It is the arbiter for normalization, as verify_exact.py is for formulas. NEXT: obtain the notebook,
read the normalized weight-2 and weight-4 triplet q-expansions, apply their relative normalization,
re-test M_e and the angles against Table 2. Only after the full model reproduces Table 2 do we run
the g1=0 ablation. A correctly diagnosed limit is a result, not a failure.

## Status
[DERIVATION/LIMITE]. Neutrino sector reproduced (0.4%); charged-lepton/mixing sector blocked on
relative normalization, cause localized. 4 form bricks remain [DERIVATION/CALIBRATED] and sealed.
Files: brick56 assembly draft (Claude sandbox), maass_brick1-4 (calibrated, on machine).
Arbiter = Anthony's machine + Qu-Ding reference notebook + Table 2.
