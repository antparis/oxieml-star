# FINDINGS 2026-06-02 -- Hall double-Beltrami chiral target: a CONJECTURE that passes the d_i->0 encadrement

## Status
[CONJECTURE] structurally motivated, NOT derived line-by-line from Hall-MHD.
[ESTABLISHED, narrow] SymPy: the SPECIFIC form F = 1/z + i*d_i/zbar has an
anti part dF/dzbar = -i*d_i/zbar^2 that is proportional to d_i (Hall) and
VANISHES exactly as d_i->0. So IF the physics produces this form, the
encadrement holds. What is NOT proven: that Hall-MHD forces exactly this form.

## Path so far (two rejected, one surviving)
1. REJECTED: diamagnetic tilt on source+vortex. SymPy showed the streamfunction
   stays REAL -> reality theorem forces mirror-lock (b=conj a), NO chirality,
   tilt or not. conj(df/dz)-df/dzbar = 0 verified. Real psi cannot be chiral.
2. REJECTED: double-Beltrami eigenmode weights posited as mode+->1/z, mode-->1/zbar.
   Encadrement FAILED: b-conj(a) -> -1 (not 0) as d_i->0, and the mode->(z/zbar)
   map was hand-posited, not derived. Discarded as hand-picking.
3. SURVIVING [CONJECTURE]: complexify in-plane velocity + i*(out-of-plane Hall
   flow v_z). Shivamoggi (arXiv:1112.3953) 2D Hall-MHD reduction: in-plane field
   from a REAL flux psi (b_x=psi_y, b_y=-psi_x), PLUS a Hall-peculiar out-of-plane
   flow v_z (eq 23c) that has NO MHD analog and vanishes without Hall.
   Model: F = w_inplane + i*v_z, with v_z ~ d_i/zbar (opposite handedness,
   amplitude ∝ Hall). SymPy: F = 1/z + i*d_i/zbar.

## SymPy results (for the conjectured form)
  F = 1/z + i*d_i/zbar
  holomorphic weight a = 1 (real), anti weight b = i*d_i (imaginary) -> NOT conjugate
  dF/dzbar = -i*d_i/zbar^2  (anti present, ALGEBRAIC 1/zbar^2, proportional to d_i)
  ENCADREMENT d_i->0: dF/dzbar -> 0, F -> 1/z (holomorphic). Anti vanishes with Hall. OK.

## What is forced vs assumed
- FORCED (Shivamoggi): out-of-plane v_z exists only in Hall-MHD, vanishes as Hall->0.
- ASSUMED (not derived): that v_z couples to 1/zbar with amplitude exactly ∝ d_i.
  This handedness/coupling is physically motivated (opposite-sign Beltrami modes)
  but NOT proven from the equations. => CONJECTURE.

## Caveats
- The naive metric b-conj(a) is misleading here (a=1 always present). The correct
  chirality statement: anti weight b=i*d_i exists, is non-conjugate to a, forced
  by Hall, vanishes at d_i=0. The chirality is in the FORCED anti, not in b-conj(a).
- This anti is ALGEBRAIC (1/zbar^2), NOT transcendental log zbar. Weaker than the
  Hasegawa-Mima transcendental target on that axis.

## Next to upgrade CONJECTURE -> DERIVATION
- Derive the out-of-plane v_z coupling to z/zbar rigorously from the 2D Hall-MHD
  double-Beltrami eigenfunctions (the missing step). Without it, no generator.
- Only AFTER a clean derivation: build generator + run pipeline + judge.
