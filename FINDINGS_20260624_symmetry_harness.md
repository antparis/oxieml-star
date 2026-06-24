# FINDINGS 2026-06-24 — Symmetry harness: holo/anti rebalancing over judge_v2

**Status:** [DERIVATION] — Wirtinger-exact, executed on the M920q (imports the
authoritative judge_v2.py). Tooling/method improvement, not a chiral discovery.

## Why

Campaign-level correction: the hunt had drifted anti-only (forcing_filter and the
whole session target ENTANGLED_CHIRAL_ANTI). The detector must read BOTH sides
(holomorphic AND anti-holomorphic) in parallel and be irreproachable on the
holomorphic side (never flag anti on a holomorphic field) before any claim on the
anti side. This is the standing symmetry discipline, previously neglected.

## What was built

`symmetry_harness.py` — a layer ON TOP of judge_v2 (NOT a new judge;
certify_1field / certify_2field stay the sole authority). It adds:
 1. symmetric_reading(f): judge label + a 5-way symmetric reading
    (holo-pure / anti-pure / mixed / real-trapped / module-trapped) + both
    Wirtinger derivatives.
 2. Balanced calibration: 5 holomorphic forms and their 5 exact anti mirrors,
    plus traps and a genuine additive mix.
 3. Mirror test judge(f) vs judge(full_conj(f)).
 4. never_false_anti_on_holo: every holomorphic form must judge 'holomorphic'.
 5. Two-column living ledger (holo confirmed / anti confirmed / rejects).

## Command

    cd ~/Desktop/oxieml-star && python3 symmetry_harness.py

## Raw result

- CALIBRATION (panels + never-false-anti + 2-field MIXTE): PASS.
- MIRROR DIAGNOSTIC: PASS. Pure holo<->anti and traps are mirror-symmetric
  (15/15); MIXED forms are NON-mirror (2/2, by design).
- never-false-anti-on-holo: 5/5 holomorphic forms -> 'holomorphic'. No leak.
- 2-field canonical MIXTE exp(z) - log(wbar) -> CROSS-CONJUGATE z*conj(w)
  (d_zbar=0, d_w=0): holo in field 1, anti in field 2.

## Finding surfaced while building (the concrete asymmetry)

judge_v2's label 'anti-holomorphic' is a CATCH-ALL: it lumps pure anti (d/dz=0,
e.g. zbar, log zbar) AND mixed (both derivatives != 0, e.g. z + 0.3 zbar).
'holomorphic' is a PURE label (d/dzbar=0) but there is no symmetric 'anti-pure'
vs 'mixed' split. The mirror test exposes this: pure forms map holo<->anti, but a
mixed form and its conjugate are BOTH labelled 'anti-holomorphic' (non-mirror).
The 5-way symmetric reading (sym=) is the fix, layered on top WITHOUT touching
the authority: z+0.3 zbar stays 'anti-holomorphic' for the judge but reads
'mixed', distinct from pure anti zbar.

## Consequence for the campaign

The detector now reads both columns. Opportunity to act on (holo data is
abundant; Odrzywolek's original EML is the holomorphic base eml-star extends):
 - calibration: reconstruct a KNOWN holomorphic structure exactly (capability),
 - discovery: search for a hidden anti part inside a holo-reputed field (a real
   find, not a wall).
The harness is the gate that makes the holo side irreproachable first.

## Trace files

- symmetry_harness.py (harness, reproducible; imports judge_v2.py)
- FINDINGS_20260624_symmetry_harness.md (this file)
