# FINDINGS — singularity_reader.py validated as level-3-ready tool

**Date:** 2026-06-25
**Status:** [ESTABLISHED] (tool level) — reproduced on Anthony's machine, identical to sandbox.
**File:** `singularity_reader.py` (standalone; profile-agnostic array interface).

## What it is
Profile-AGNOSTIC reader: `read(x, u, func=None, true_delta=None)` ingests real-axis arrays
(the level-3 interface). Two lenses (Fourier strip deliberately excluded -- our analyticity-
strip Fourier instrument is documented broken; AAA is its replacement):
  - AAA on U'/U : locator + full spectrum (delta, x_loc), resolves multiple/equidistant
    singularities; gamma = -Re(residue), with clustering of split poles + cut-tail/Froissart
    artifact filter (gamma <= floor discarded).
  - radial : precise exponent, CALIBRATION only (needs func AND exact true_delta).

## Machine result (2026-06-25), 5 cases reproduced
  CLM a=0      : AAA delta=1.0    gamma=0.9999 ; radial 1.0016 ; pole.
  gCLM a=1/2   : AAA delta=1.0001 gamma=1.9998 ; radial 2.0    ; pole.
  branch g=0.7 : AAA delta=0.9683 gamma=0.729  ; radial 0.7035 ; branch ; 8 cut-tail nodes filtered.
  probe B      : two pairs resolved (delta=0.5 & 1.5).
  probe C      : two equidistant resolved (x=+-2, delta=1).

## Branch-exponent accuracy (sandbox, [HEURISTIC], 5 cases)
Three rival methods (local parametric fit, AAA-continuation radial, Domb-Sykes double precision)
were all BEATEN by the clustered AAA-residue. Accuracy of clustered AAA-residue:
  gamma=1 -> 0.0% ; gamma=1.27 -> 0.8% ; gamma=2 -> 0.0% ; gamma=0.7 -> 4.1% ; gamma=0.45 -> 3.5%.
=> <1% for gamma>=1 (the physical collapse regime 0<=a<a_c). For gamma<1 (a<0) it degrades to
~3-4%, blocked by a DOUBLE-PRECISION WALL (Lushnikov used 68-digit arithmetic). <1% everywhere
is unreachable on float64 input -> [DERIVATION/LIMIT].

## Convention (settled, arXiv:2010.01201)
gamma = spatial singularity order = 1/(1-a); Fourier p = 1 - gamma. The instruments measure gamma.

## NOT the cube
Real-analytic profile -> forced holomorphic (unique continuation); question is (delta, gamma),
not holo vs anti. This tool is a singularity reader, orthogonal to the eml* anti-holomorphic hunt.
