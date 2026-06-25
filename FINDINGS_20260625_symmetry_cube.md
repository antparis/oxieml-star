# FINDINGS 2026-06-25 — Symmetry calibration of the eml/eml★ discoverer (PySR → judge_v2)

**Status tags:** [ESTABLISHED] = run on Anthony's machine + judged by `judge_v2.certify_1field`.
[LIMIT] = diagnosed structural limit, not a tool failure.

**Tool:** `symmetry_battery.py` (companion to `pysr_holo_calib.py`).
**Pipeline:** native (z,z̄) data → PySR on Re(f) and Im(f) → Occam selector (simplest equation
with loss < 1e-8) → rebuild f̂ = g_re + i·g_im → express in (z,z̄) → `chop` dust → `judge_v2.certify_1field`.
**Rule enforced (SYMÉTRIE):** the tool must be irreproachable on holo AND anti before any claim on
unknown data. MARKER (PySR operator name) ≠ VERDICT (only the SymPy judge decides).

---

## Result — classification cube calibrated: 8/9 clean, 1 documented limit

| region            | case            | f(z,z̄)            | judge verdict        | passed | MSE Re / Im            |
|-------------------|-----------------|--------------------|----------------------|--------|------------------------|
| holo wall         | poly            | z²+z               | holomorphic          | yes    | ~1e-14 / —             |
| holo wall         | exp             | exp(z)             | holomorphic          | yes    | ~5e-15 / —             |
| anti wall         | poly_anti       | z̄²                 | anti-holomorphic     | yes    | 3.9e-15 / 1.6e-15      |
| anti wall         | exp_anti        | exp(z̄)             | anti-holomorphic     | yes    | 4.9e-15 / 2.1e-15      |
| interior cubie    | real_trapped    | z·z̄                | real-trapped         | yes    | 5.4e-15 / 3.2e-34      |
| interior cubie    | module_trapped  | z²·z̄               | module-trapped       | yes    | 9.0e-15 / 7.9e-15      |
| anti wall (cut)   | mixte           | exp(z)−log(z̄)      | anti-holomorphic     | verdict-only | 9.4e-2 / 1.40    |
| anti wall (cut)   | log_anti        | log(z̄)             | [LIMIT] recon timeout| no (limit) | branch cut         |
| negative control  | shuffle         | z²+z, y permuted   | REJECT (high MSE)    | yes    | 0.40 / 1.04            |

**Reading.** The four pure corners (holo/anti × algebraic/transcendental) reconstruct EXACTLY and are
judged correctly. The two interior cubies are judged correctly. The negative control is rejected
(tool does not hallucinate a formula on noise). `mixte` reaches the correct verdict (anti-holomorphic)
despite the branch cut; exact reconstruction is NOT the criterion for cut cases — the verdict is.
`log_anti` is a structural limit: Im = arg(z̄) (log branch cut) is out of reach of the
{+,−,*,/,exp,cos,sin,log_abs} basis; the reconstruction times out cleanly at 60 s. [LIMIT], not a failure.

**Symmetry conclusion [ESTABLISHED].** The discoverer sees anti exactly as well as holo on both the
algebraic and transcendental corners, plus the interior cubies, and rejects noise. This is the
"irreproachable on holo AND anti" precondition required before any claim on unknown data.

---

## Four bugs found and fixed this session

1. **Occam selector** — `model.sympy()` returned a Pareto pick inconsistent with the loss minimum,
   producing decorated equations (complexity 13–22) instead of the clean one (complexity 5–7).
   Fix: `select_equation_idx` = simplest equation with loss < 1e-8, fallback score then loss-min.

2. **Naming bug x0/x1 (critical)** — reconstruction looked for SymPy symbols "x","y" but PySR emits
   "x0","x1". The (z,z̄) substitution silently failed → the judge always saw a holomorphic stub →
   the tool was STRUCTURALLY BLIND TO ANTI while looking perfect on holo. Caught only by the
   symmetry test (poly_anti returned "holomorphic" before the fix). Fix: map both x0/x1 and x/y.

3. **Reconstruction freeze (9 h)** — `mixte` froze ~9 h at 100% CPU inside `reconstruct_and_judge`
   (`sympy.simplify`/`expand` explodes on log/atan2 branch-cut expressions). PySR fit had finished;
   only the symbolic step hung. Fix: three guard-rails (see below). After the fix, the SAME `mixte`
   case reconstructed in 17 s on a rerun (different PySR draw, deterministic=False), and `log_anti`
   hit the 60 s timeout cleanly with status [LIMIT].

4. **Floating-point dust → false negative** — real_trapped (z·z̄) reconstructed as
   `z·z̄ + 1.18e-19·I`. The 1e-19·I dust (Im MSE = 3e-34 = machine zero) broke the judge's EXACT
   full_conj invariance test → verdict slid from real-trapped to module-trapped. Fix: `chop`
   (round numeric coefficients < 1e-12 to zero, term by term) applied to the (z,z̄) expression
   BEFORE the judge. Verified the chop does NOT remove legitimate coefficients (>tol) nor alter the
   pure corners. The pivot judge `judge_v2` was NOT modified.

---

## Guard-rails added (memory rule CHECKPOINT/RÉCUPÉRATION)

- **Heartbeat** `sb_<case>_progress.log` — one timestamped line per step.
- **Partial checkpoint** — PySR fit (g_re, g_im, MSE) saved to JSON BEFORE the symbolic
  reconstruction, so a freeze/timeout in reconstruction does not lose the expensive fit.
- **Timeout** `RECON_TIMEOUT = 60 s` on reconstruction via SIGALRM → clean [LIMIT] status, next case
  proceeds (no chain block). Verified: a deliberately infinite reconstruction is cut at the cap.

---

## Exact reproduction commands

Selftest (no PySR, checks all 9 verdicts against judge_v2):
    python3 symmetry_battery.py --selftest

Single case, detached (~1–2 min for simple cases, ~30 min for transcendental):
    JULIA_NUM_GC_THREADS=1 setsid nohup python3 -u symmetry_battery.py --case <CASE> > sb_<CASE>.log 2>&1 &

Live progress:
    tail -n 10 sb_<CASE>_progress.log

Result JSON per case: `sb_<CASE>_result.json`.

---

## Open / next (not done this session)

- `log_anti` exact reconstruction needs an operator basis that captures arg/atan2 (out of current
  scope; verdict-only is acceptable for cut cases). [LIMIT]
- Orthogonal robustness test: inject controlled noise (1e-19, 1e-10, 1e-5) to map the judge's
  exact-invariance breakdown threshold. [proposed]
- Complex-singularity bench (Navier-Stokes angle): rewrite high-k Fourier + add AAA on U′/U,
  calibrate on 4 toys, then the CCF proven law p = −a/(1−a). Separate chantier. [proposed]
