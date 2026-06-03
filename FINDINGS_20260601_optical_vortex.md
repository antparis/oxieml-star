# FINDINGS 2026-06-01 -- Optical vortex: pipeline calibrated on a PHYSICAL system (ALGEBRAIC anti)

## Status
[ESTABLISHED] executed on machine + judge-certified + both controls passed.
NATURE: CALIBRATION on a physical (optical) system. NOT a Projet-A discovery.

## What is tested
Laguerre-Gauss optical vortex (real lab physics, charge sign = chirality =
holo/anti). Envelope-divided targets fed to the certified pipeline
(PySR MIXTE+inv+inv_bar -> verify_exact.certify -> reality_check.py), like N1.
Adapter: optical_vortex_to_csv.py (reuses only beam(l) physics).

## Commands (exact)
Config: niter=30 pop=300 maxsize=25 parsimony=0.001 precision=64.
  python3 optical_runs.py --only anti / --only holo / --only shuf
  python3 reality_check.py optical_anti_result.json
  python3 reality_check.py optical_holo_result.json
  cat optical_shuf_result.json

## Raw results (judge-certified)
  optical_anti  MSE=1.71e-29  my_conj(x0^3)=zbar^3  ANTI  flag=complex  OK
  optical_holo  MSE=1.71e-29  x0^3=z^3              HOLO  df/dzbar=0     OK
  optical_shuf  MSE=538.7     mse_below_1e-3=false  REJECTED            OK

## Interpretation / limits
- FIRST pipeline success on a PHYSICAL measurable system (LG beam, lab-made).
- BUT anti = zbar^3 = MONOMIAL = ALGEBRAIC finite-order anti (like Kirsch),
  NOT the transcendental log(zbar) of vortex_N1.
- AND the anti depends on the analysis choice of dividing the Gaussian
  envelope, NOT forced by a physical constraint (unlike Kirsch traction-free).
- => CALIBRATION, not a discovery. The "forced + transcendental + physical"
  case remains EMPTY. flag=complex here only means zbar^3 is not a real field,
  NOT a deep chiral imbalance (b != conj a) as in N1.

## Next
- Plasma candidates (see research report): screened drift-wave / Hasegawa-Mima
  vortex (transcendental Bessel/log zbar, forced by screening length rho_s),
  Hall-MHD double-Beltrami (genuine chiral imbalance forced by B). These are
  the real Projet-A targets: forced by physics, not by an analysis choice.
