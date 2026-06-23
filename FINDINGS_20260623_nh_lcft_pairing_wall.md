# FINDINGS 2026-06-23 — Non-Hermitian PT free-fermion LCFT closes on the REAL_TRAPPED wall

Status: tool [ESTABLISHED] (executed here, EXIT=0); physics verdict [DERIVATION] (on inferred (z,zbar) form).

## What was tested
The log cross-correlator G_{-+} ~ Delta*ln|z-w|^2 of the non-Hermitian PT-symmetric
free-fermion LCFT (Io-Huang-Hsieh, arXiv:2602.02649, eq.11) against the
ENTANGLED_CHIRAL_ANTI target, via a pairing/reality judge (full_conj = swap
holo<->anti coordinates + conjugate coefficients only). Fixes a prior bug where
sympy .conjugate() on independent z/zbar mislabeled every wall as "target".

## Command
python3 nh_lcft_pairing_judge.py

## Raw result (this machine, EXIT=0)
paper G_-+  Delta*[ln(z-w)+ln(zb-wb)]  c=cbar  -> PAIRED -> REAL_TRAPPED (wall)
asym sectors  pi*ln(z-w)+phi*ln(zb-wb)  c!=cbar -> UNPAIRED -> ENTANGLED_CHIRAL_ANTI (target)
conj-paired  a*ln(z-w)+conj(a)*ln(zb-wb)       -> PAIRED -> REAL_TRAPPED (wall)
holo control  ln(z-w)                          -> HOL

## Meaning
Non-Hermiticity ALONE does not de-pair the log: with symmetric sectors (c=cbar=-2)
the cross log is paired -> real-trapped -> WALL, same structure as the symplectic
fermion. Irreducible (Delta!=0 not base-removable) but paired. USEFUL FAILURE.
New criterion [DERIVATION]: the chiral cell requires c != cbar (asymmetric sectors
-> unequal log coefficients -> unpaired). Next target: intrinsically asymmetric
non-Hermitian theory (PT-broken Yang-Mills, complex non-conjugate lambda_pm,
arXiv:2603.19006). Caveat: verdict on inferred (z,zbar) form; equal-time slice
ln|x-y| only is published; SM needed to upgrade to [ESTABLISHED] on the paper.
Cell remains EMPTY.
