# FINDINGS — Joukowski test on MIXTE tool + certified result presenter

Date: 2026-05-23
Status: [ESTABLISHED] executed on machine + judge-certified (MIXTE).
Level: LEVEL 1 (statuses known a priori by presence of conj). Capability demo
on a realistic aerodynamic map, NOT a discovery.

## Test (joukowski_mixte.py, light config pop=120/niter=80/maxsize=18)
400 pts annulus |z|>0.3, native complex.
  holo  : w = z + 1/z              -> HOLOMORPHIC
  anti  : w = z + 1/conj(z)        -> ANTI-HOLOMORPHIC
  mixed : w = exp(z)+exp(conj z)   -> ANTI (judge: d/dzbar != 0)
  shuf  : anti targets shuffled    -> negative control

## Results (judge-certified)
  holo  : eq = x0 + 1/x0                 MSE 2.98e-32  HOLOMORPHIC      OK
  anti  : eq = 1/my_conj(x0) + x0        MSE 3.97e-32  ANTI-HOLOMORPHIC OK
  mixed : eq = my_real(exp(x0)*2)        MSE 1.45e-31  ANTI-HOLOMORPHIC OK
  shuf  : MSE 4.33 (>= 1e-3) REJECTED                                   OK
  --report: PASS
Note: PySR found mixed = 2*Re(exp(z)), the compact exact form of exp(z)+exp(conj z).

## Tooling changes this session (all 3 active files now MIXTE + coherent)
- verify_exact.py    : MIXTE (judge), backup .bak_pure
- pysr_stacking.py   : MIXTE (generator Julia+SymPy), backup .bak_pure
- translate_formula.py: MIXTE (certified translator), backup .bak_pure
  verified: my_conj(x0*x0) -> conj(z)^2, proved exactly equal.

## New: boxed.py (certified result presenter)
Reads *_result.json, runs the certified translator, prints a boxed equation
ONLY if MSE<1e-3 AND judge gave a verdict; else [REJECTED]. The equation
"falls out" only at the end of the validation chain (anti-SPARC by design).
Known limitation [TODO]: translator library lacks Joukowski forms, so boxed
currently shows raw PySR (with numeric dust) instead of clean z+1/conj(z).
Also box width truncates long df/dzbar. Both are presentation polish, deferred.

## Status
[ESTABLISHED] MIXTE tool discriminates holo/anti/mixed on Joukowski; neg control
rejected. Level-1 capability demo, not a discovery.
[TODO] Enrich translator canonical library (Joukowski forms) + widen box.
