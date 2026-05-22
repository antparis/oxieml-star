# Invalidated / archived material

## eml_star_galaxy_paper (tex + pdf)
ARCHIVED because its central claim is a known artefact.

The paper claimed that eml-star detects a "non-holomorphic component" in
SPARC / LITTLE THINGS galaxy rotation curves (Spearman rho = -0.27,
p = 0.004). This result is INVALID: it stems from a forced real-to-complex
encoding of intrinsically real data (rotation velocities, radii). The
encoding itself creates an apparent anti-holomorphic structure that is an
artefact, not a physical property of the galaxies.

The detector only yields meaningful results on NATIVELY complex data
(e.g. ellipticities gamma = e1 + i*e2, wavefunctions, impedances). The
galaxy analysis does not meet this condition.

The valid paper (eml_star_paper) and the validated detector pipeline
(double_validation, verify_exact, translate_formula) supersede this work.

## detect_mock_Emode_*_result.json (archived 2026-05-22)
Per-galaxy E/B-mode mock sensitivity tests. INVALIDATED, not results:
- MSE ~0.16 (>> 1e-3 threshold, rule: high MSE invalidates the claim)
- marker/verdict inconsistent; these probe the detection floor when signal
  is buried in noise (sigma ~0.27, no averaging). They "failed usefully"
  (measured the floor); they are NOT detections. Kept for the record only.
