# Corrections and reclassifications

This file records claims in earlier commit messages that overstated results,
with the corrected status. Pushed history is not rewritten; this note is the
authoritative correction.

## EHT M87* visibilities — commit 60d03fc ("certified anti-holomorphic")
RECLASSIFIED to [HEURISTIC], not certified.
- detect_eht_m87_visibility_result.json: Route A MSE = 0.0649, Route B MSE = 0.0831.
- Both MSE >> 1e-3, which invalidates any certification (high-MSE rule).
- No symbolic judge field present (verify_exact.py was never run on it): only the
  PySR marker, which is never authoritative.
- The "anti" verdict is physically expected anyway (Hermitian symmetry
  V(-u,-v) = conj V(u,v) guarantees an anti signature), so a consistent verdict
  with a poor fit is at best a weak indicator, not a detection.
STATUS: [HEURISTIC] indicator only. NOT certified.

## KiDS "end-to-end certified" — commits 4763bc2 / 18c1f80
RECLASSIFIED. The KiDS map-level results (E-pure control, E+B detection, PSF) are
judge-consistent at MSE ~7e-5 and stand as valid SANITY CHECKS on natively-complex
maps. But they are mock/map-level tests, not an "end-to-end certified" detection on
unknown real data. The KiDS PSF negative-control result (real -> holo, shuffled ->
anti, judge OK) is the genuine validated outcome; see RESEARCH_LOG.md (2026-05-22).
STATUS: valid sanity checks / negative control. "end-to-end certified" overstated.

## Per-galaxy E/B-mode mocks
Archived in _archive_invalidated/ (MSE ~0.16, sensitivity-floor probes, not results).
