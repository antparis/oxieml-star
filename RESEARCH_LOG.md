# Research Log (append-only)

One line per finding: date — status — short description — trace file.
Status: [ESTABLISHED] executed+certified · [DERIVATION] sound, unproven ·
[CONJECTURE] untested idea · [HEURISTIC] numerical hint, not a proof.

2026-05-22 — [ESTABLISHED] — EML family classification: 100 ops, 20 holo / 20 anti / 50 hybrid / 1 const — classify_eml_family.py / FINDINGS_20260522.md §1
2026-05-22 — [ESTABLISHED] — {eml,eml★,Re} reconstructs all f(a)-g(b) candidates at machine precision — test_generative_power.py / FINDINGS_20260522.md §2
2026-05-22 — [DERIVATION] — sqrt, powers, 1/z, arctan/asin/acos, tan, sinh all reduce to exp/log (explicit forms) — sieve_phase2.py / FINDINGS_20260522.md §3
2026-05-22 — [ESTABLISHED] — Infinity wall: Gamma NOT reconstructible (MSE 1.97e-3 vs control 7.64e-30, same budget) — test_gamma_full.py / FINDINGS_20260522.md §4
2026-05-22 — [DERIVATION] — Two orthogonal walls: phase/monodromy (finite, eml⁰ crosses part) vs infinite-process (Gamma, no finite operator) — FINDINGS_20260522.md §5
2026-05-22 — [ESTABLISHED] — KiDS PSF detector: real field -> holo, shuffled control -> anti, both routes + SymPy judge agree (negative control success) — double_validation_v6_result.json (verify_exact.py judges OK)
2026-05-22 [ESTABLISHED-groundtruth/PENDING-detector] Penning-trap sanity check: 3 natively-complex maps (cyclotron=holo, mirror=anti, squeezing=hybrid) + shuffle control; exact SymPy classes set; detector run pending. trace: simulate_penning_maps.py, FINDINGS_20260522_penning.md
2026-05-22 [CONJECTURE] Optical phase-problem zero-flipping = conjugation; possible eml-star link via exp/log algebra. Unproven, possibly not novel (optics 1975-85). Hard question logged. trace: FINDINGS_20260522_optics.md
2026-05-23 [ESTABLISHED] B2 Clunie-Sheil-Small shear calibration: holo->holomorphic (dzbar=0), shear->anti-holomorphic (dzbar!=0), both MSE<1e-3, judge-certified, --report PASS. Calibration NOT discovery; light config (pop100/niter80/maxsize18). -> FINDINGS_20260523_b2_shear.md
2026-05-23 [DECISION] eml-star canonical = MIXTE exp(x)-log(conj(y)), per paper. Direction: align CODE to paper (2 active files verify_exact.py + pysr_stacking.py + re-certify Penning), do NOT touch the publication. Provisional-strong pending Theorem 4.3 proof reading. -> FINDINGS_20260523_emlstar_definition.md
2026-05-23 [ESTABLISHED] MIXTE correction applied (verify_exact.py + pysr_stacking.py, backups kept). Penning re-certified under MIXTE: all dataset verdicts hold (holo/anti via route B/hybrid/rejected). Route-A formula for penning_anti was a PURE-bug artefact, unmasked by the fix; dual-route design saved the verdict. -> FINDINGS_20260523_mixte_recert.md
2026-05-23 [ESTABLISHED] MIXTE tool calibrated end-to-end (PySR->judge): holo->z^2 (MSE 1e-32), anti->conj(z^2) (MSE 1e-32, anti-holomorphic), shuffle rejected (MSE 0.61). --report PASS. Anti captured via my_conj not emlstar (expected under MIXTE). -> FINDINGS_20260523_mixte_calib.md
2026-05-23 [PRINCIPLE] Calibration discipline: re-certify at EVERY tool change AND at every result to validate. Calibration proves reliability on known cases, NOT absolute perfection. Do not re-test the known in a loop without a change. The real guard is a negative control on each NEW test, not repetition of the known.
2026-05-23 [ESTABLISHED] Joukowski test on MIXTE tool: holo->z+1/z, anti->z+1/conj(z), mixed->2Re(exp z), shuffle rejected (MSE 4.33). --report PASS. Level-1 capability demo, NOT a discovery. translate_formula.py corrected to MIXTE (backup kept); new boxed.py certified presenter (equation shown only if MSE<1e-3 AND judge verdict). TODO: enrich translator library + widen box. -> FINDINGS_20260523_joukowski.md
