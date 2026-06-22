# FINDINGS 2026-06-10 -- GW first hands-on run: infrastructure works, signal dissolved under control

## Origin
First execution session on the gravitational-wave lead (rank-1 from
FINDINGS_20260609_gw_lead.md). Goal: install sxs, load a precessing waveform,
measure mirror asymmetry A_lm, apply co-precessing-frame discriminant. Setup +
first probe, NOT a discovery attempt.

## What WORKS (infrastructure established)
- sxs 2025.0.27 in isolated venv_gw. Activate: source venv_gw/bin/activate
- Catalogue v3.0.0: 4170 sims. 2272 precessing (chi1_perp>0.3, ecc<0.01), 654 aligned.
- Waveform via sim.h (new v3 API; old 'Lev/rhOverM' dead, now 'LevN:Strain_N2.h5').
  WaveformModes, l_max=8, 77 modes.
- sxs native frames work: to_coprecessing_frame(), frame_type. Transform clean.

## What is a TRAP (method pitfalls, traced so we do not repeat them)
- Per-mode normalisation |A_lm|/|h_lm| is FRAGILE: weak mode -> noise/noise ->
  unstable, hits 2.000 exactly (sign + small-denominator artefact, NOT physics).
  Use GLOBAL normalisation by |h_22|.
- Mirror-factor sign NOT trivial. Tried (-1)^m (wrong), (-1)^l (wrong),
  (-1)^(l+m) (works for m-EVEN, still wrong for m-ODD). Exact SXS convention for
  the m-odd sign must be read from docs BEFORE next run. m-EVEN (2,2),(4,4) clean.
- A 2.000 EXACT value = sign-bug signature. Three sign errors this session, all
  caught by this tell-tale + the negative control.

## RESULT (honest, mostly NEGATIVE)
- Clean m-EVEN modes (2,2),(4,4): BOTH precessing SXS:BBH:0161 and aligned
  control SXS:BBH:0109 are mirror-SYMMETRIC in co-precessing frame (1e-7 to 1e-9).
  No chiral asymmetry where measurement is reliable.
- Initially promising (2,1)=1.68e-3 on 0161 (per-mode norm) DISSOLVED to 7.7e-8
  under robust global norm => normalisation artefact, NOT physics. Auditor
  over-eagerness corrected by the control. Useful failure.
- m-ODD modes: not exploitable yet (sign convention unresolved).

## Status: [DERIVATION/LIMIT]
GW infrastructure ESTABLISHED and reusable. First asymmetry probe gives NO chiral
signal on reliable (m-even) modes for SXS:BBH:0161; apparent (2,1) signal was an
artefact removed by the negative control. m-odd sign convention must be fixed
before any A_lm claim. eml* (PySR+judge) NOT yet involved -- correctly gated
behind a clean, control-validated asymmetry we do not have yet.

## Next session (cold, with the doc)
1. Read exact SXS mirror convention for h_{l,-m} vs conj(h_{l,m}); verify on a
   pure aligned non-spinning case where ALL modes must be exactly symmetric.
2. Re-run A_lm on m-even AND m-odd with correct sign, precessing vs aligned.
3. ONLY if a control-validated asymmetry survives co-precessing frame: feed the
   residual to PySR + verify_exact.py (the eml* stage).
Candidate triplet: SXS:BBH:0161/0163/0164 (q=1, chi1_perp~0.51).

## Pointer
Builds on FINDINGS_20260609_gw_lead.md (lead + protocol). Records the FIRST
hands-on run and its method lessons.

## SIGN CONVENTION RESOLVED (web research, 3 concordant sources)
Correct mirror relation for NON-PRECESSING binaries (inertial frame):
  h_{l,-m} = (-1)^l conj(h_{l,m})   [factor is (-1)^l, NOT (-1)^(l+m) nor (-1)^m]
Sources: Boyle et al. arXiv:1409.4431 (THE precession paper) eq.23; Mills &
Fairhurst arXiv:2007.04313 ("h_{l-m}=(-1)^l h_{lm}^*"); spin-weighted SH identity
2Y_{l-m}=(-1)^(l+m) ... resolves to (-1)^l for the strain.
WHY (-1)^l gave 2.000 on m-odd this session: NOT a wrong factor. The relation is
exact only (a) for non-precessing and (b) where the mode is non-negligible.
m-odd modes of an ALIGNED binary are physically ~0 -> |A|/|h_lm| = eps/eps blows
up. Fix: (1) use factor (-1)^l, (2) normalise GLOBALLY by |h_22|, (3) THRESHOLD:
skip modes with |h_lm| below ~1e-4 |h_22| (measuring noise otherwise).
KEY (Boyle): the relation h_{l,m}=(-1)^l conj(h_{l,-m}) is NOT essential -- it is
a property of non-precessing systems. The CHIRAL ASYMMETRY we seek = the SURVIVING
violation of this relation in the co-precessing frame. That violation IS the signal.
