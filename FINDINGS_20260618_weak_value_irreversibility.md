# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine] Refinement of the weak-value candidate (232398dd): the Project-A caveat is much narrower than 'gauge vs physical'. Three results this session sharpen the node. (1) Im(W) is T-ODD: under time reversal (swap preparation<->postselection) W -> conj(W), so Re(W) is T-even and Im(W) flips sign -> Im(W) is the physical time-oriented component, NOT a gauge (a gauge would be T-even/removable). (2) Irreversibility (arrow of time) enters ONLY via tracing the measurement apparatus: an isolated qubit + apparatus stays pure and reversible (S_total=0); entropy appears only on tracing the apparatus (S~1 bit). The node is localized in the macroscopic readout, not in the system. (3) With a proper QUANTUM POINTER (Re(W) shifts <q>, Im(W) shifts <p>, Aharonov-Albert-Vaidman), pure DECOHERENCE in position PRESERVES <p>=Im(W) exactly (only momentum variance/noise grows) while DISSIPATION (friction/thermalization) damps Im(W) to 0. An ideal measurement decoheres WITHOUT dissipating, so Im(W) is physical there; real weak-value experiments (optics, AAV) run in that regime and DO measure Im(W).
## Auditor correction of an earlier-too-soft statement
The prior FINDINGS said the caveat was 'not decidable by calculation, depends on interpretation'.
That was too soft. The rephasing-invariance ALREADY showed Im(W) is not removable by convention,
and the T-ODD result confirms it is a time-oriented physical component, not a gauge. The genuine
residual point is a precise physical one, not a matter of taste.
## Tests (executed on Anthony's machine)
 - T-reversal: W_rev = wv(phi,psi) == conj(W) for all sampled (psi,phi). [certified] Re T-even, Im T-odd.
 - Reversibility/entropy: isolated qubit S=0; qubit+apparatus closed S_total=0 (reversible); tracing the
   apparatus gives reduced S~0.999 bits (irreversible). Arrow of time = the trace, not the system. [certified]
 - Quantum pointer: corr(<q>,Re W)=0.9998, corr(<p>,Im W)=0.9998 (AAV correspondence). [certified]
 - Decoherence exp(-Gamma (q-q')^2) on the pointer density matrix: <p>=Im(W) preserved for Gamma=0..5
   (reference Im(W)=-0.206, <p> stays -0.0124..-0.0118); only momentum variance grows. Analytic reason:
   the off-diagonal damping vanishes on the diagonal, so d/dq rho|_{q=q} is unchanged. [certified]
 - Dissipation (friction damping mean momentum by e^{-eta t}): <p>=Im(W) decays -0.0124 -> -0.0006. [certified]
## Audit of Milo's proposed scripts (REJECTED)
Milo proposed weak_value_macro_pointer.py / weak_value_pointer (real scalar factor on W). REJECTED:
multiplying W by a REAL factor scales Re and Im together, so it can never test selective survival of
Im(W). The physics of irreversibility lives in the pointer density matrix, not in a scalar on W.
The intuition (introduce irreversibility) was right; the implementation was physically void.
## The remaining open point (now very narrow)
Im(W) survives everything that DEFINES a measurement (decoherence, recording); it dies only under
thermalizing DISSIPATION, which is avoidable, not mandatory. So Project-A reduces to: 'must a real
post-selection dissipate?' Empirically (AAV, optical weak-value experiments) it need NOT -- Im(W) is
measured. Strong, convergent support that Im(W) is a genuine independent anti-holomorphic quantity.
## Status
[ESTABLISHED sandbox->machine] for the three structural facts (T-odd, trace-localized irreversibility,
decoherence-preserves vs dissipation-kills). The Plateau-B claim itself remains [CONJECTURE, strong]:
support is now serious and convergent, but a full proof needs the physical argument that ideal
(non-dissipative) post-selection is legitimate. Do NOT overclaim: strong candidate, not a proof.
Files: weak_value_pointer_test.py (this), weak_value_test.py (232398dd). Arbiter = Anthony's machine + open point.
