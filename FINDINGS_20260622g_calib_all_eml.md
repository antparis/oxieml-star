# FINDINGS 2026-06-22g -- judge_v2 calibration across eml / eml* / eml0 + spin axis

Status: [ESTABLISHED] for the classification criterion (executed + certified on machine).
        [DERIVATION] for the physical (parity-broken LCFT / IQH) realization.

## What was tested
calib_all_eml.py runs judge_v2.certify_1field on 12 closed forms spanning the three
operators (eml / eml* / eml0), the two reducibility walls (real-trapped, module-trapped),
and the orthogonal conformal-spin axis. Each verdict is compared against an INDEPENDENT
log-derivative oracle  L = zbar * d/dzbar(log f)  (module-trapped iff L is |z|^2-only,
real or pure-imaginary). The oracle is the expected value of a unit test, NOT the judge.

## Exact command
    cd ~/Desktop/oxieml-star && python3 calib_all_eml.py
sha256(calib_all_eml.py) = 6e0187074fcc6a5b581c7dd955be94ab76b014422119f3dc59786e6e0248cc30

## Raw result
12/12 judge == oracle == expected.  holomorphic irreproachable (no eml mislabelled anti) = True.
  eml   z^2, exp(z), 1/z                            -> holomorphic       PASS
  eml*  log(zbar), exp(zbar), 1/zbar                -> anti-holomorphic  PASS
  eml0  z/zbar, |z|^(2i)                            -> module-trapped    PASS  (re-confirms 2026-06-22 patch)
  REAL  z*zbar                                      -> real-trapped      PASS
  ORTHO z^-2 zbar^-1 (1 + log|z|^2)   (b=bbar)      -> module-trapped    PASS
  ORTHO z^-2 zbar^-1 (1 + log zbar)   (b=0)         -> anti-holomorphic  PASS
  ORTHO z^-2 zbar^-1 (1 + log z + 2 log zbar)       -> anti-holomorphic  PASS

## Established criterion (orthogonal / conformal-spin axis)
For a spinful logarithmic-operator 2-point form
  f = z^(-2h) * zbar^(-2hbar) * (a + b*log z + bbar*log zbar),  with h != hbar:
  PAIRED  (b = bbar -> log|z|^2)    : module-trapped (transcendental but removable;
                                      same wall as Aharonov-Bohm).
  UNPAIRED / ASYMMETRIC (b != bbar) : genuine anti-holomorphic.
The transcendental log does NOT escape the module wall unless the left/right log
couplings are asymmetric (b != bbar).

## Consequence (navigation) -- [DERIVATION]
b != bbar requires parity breaking in the physical theory. Parity-invariant LCFTs
(generic percolation / polymers / time-reversal-invariant disorder) give b = bbar
-> module-trapped. The structurally-correct candidate is a parity-broken LCFT
(integer quantum Hall plateau transition: c=0, spin operators, measured multifractality).
No closed form for that correlator is established literature; the chiral cell remains
EMPTY. This finding SHARPENS the wall, it does not fill the cell.

## Files
calib_all_eml.py (this repo).
