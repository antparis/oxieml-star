# FINDINGS 2026-06-02 -- Hasegawa-Mima screened vortex: FORCED transcendental anti DETECTED on a physical system

## Status (two distinct levels)
[ESTABLISHED] DETECTABILITY: pipeline detects anti-holo on the screened
drift-wave vortex (physics forces it via finite rho_s) and NOT on its
unscreened limit (recovers -iGamma/2pi z exactly). Encadrement validated by
EXECUTION, not just analytically. Anti signal is real, not a detector reflex.
[HEURISTIC] FORM: the recovered vortex equation is a numerical overfit
(exp/log pile), NOT a clean closed-form log(zbar). No clean transcendental
reconstruction, and NO chiral imbalance (single vortex is mirror-locked).

## What is tested
Screened Hasegawa-Mima single drift-wave vortex. Anti-holo FORCED by finite
ion-sound Larmor radius rho_s, transcendental (log zbar), proven non-removable
(analytic + SymPy: dw/dzbar = (iG/4pi rho_s^2) K0(|z|/rho_s), vanishes only
rho_s->oo). Raw complex velocity w fed to certified pipeline, NO envelope
division (contrast: optical case was removable by envelope division).
Generator: hasegawa_mima_gen.py. Driver: hm_runs.py. Regime rho_s=0.3 (strong
screening) so anti is dominant, not buried under the holomorphic term.

## Commands (exact)
Config niter=30 pop=300 maxsize=25 parsimony=0.001 precision=64.
  python3 hm_runs.py --only vortex / --only holo / --only shuf
  python3 reality_check.py hm_vortex_result.json
  python3 reality_check.py hm_holo_result.json
  cat hm_shuf_result.json

## Raw results (judge-certified)
  hm_vortex MSE=9.2e-6   ANTI-HOLOMORPHIC  (overfit form, not clean log zbar)
  hm_holo   MSE=2.2e-25  HOLOMORPHIC  -> (-i/2pi)/z = -iG/(2pi z) EXACT, complexity 3
  hm_shuf   MSE=0.155    mse_below_1e-3=false  REJECTED

## Interpretation
- The decisive test is hm_holo: SAME field, screening removed -> detector says
  HOLOMORPHIC with the exact Cauchy kernel. So the ANTI verdict on hm_vortex is
  NOT a detector bias (it does not glue anti everywhere). The vortex/holo
  contrast IS the encadrement, confirmed by execution.
- FIRST physical system where forced transcendental anti is DETECTED by the
  pipeline. Fills the 'forced + transcendental + physical' cell AT THE
  DETECTION LEVEL.
- Limits: (1) form is a numerical overfit, clean log(zbar) NOT reconstructed;
  (2) flag=complex is from parasitic coefficients, NOT physical chirality;
  single real symmetric streamfunction is mirror-locked (b=conj a), as the
  analytic report predicted. (3) This is a THEORETICAL physical field (static
  linear screened response), NOT measured tokamak data.

## Physical meaning of the anti part (Wirtinger identity, not speculation)
dw/dzbar = (1/2)(div v - i omega): its real part is flow compressibility, its
imag part is vorticity. For this vortex it is pure imaginary -> pure vorticity,
concentrated within rho_s, scaling as 1/rho_s^2. The anti-holomorphic lens IS
a vorticity/compressibility diagnostic.

## Next
- Chiral imbalance: screened SOURCE+VORTEX (complex strength Q-iGamma), phase
  fixed by B, to break mirror-locking and seek genuine b != conj(a).
- Cleaner form: add Bessel K to the toolbox, or fit on the analytic short-range
  expansion, to reconstruct log(zbar) in closed form instead of overfit.
- Real data: measured tokamak reflectometry would move this from theoretical
  field to measured signal.
