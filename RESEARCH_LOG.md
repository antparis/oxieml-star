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
