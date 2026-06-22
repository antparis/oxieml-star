# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine, TOOLING] Maximal calibration bench re-judged ALL historical candidates and REVEALED a real SPARC-type blind spot in judge_v2, now fixed. The bench is a 'counterfeit-detector calibration': pass known cases of three families and require the right verdict for each, including the traps. FAMILIES: ANTI (must say anti) = vortex log(zbar), loc5 z^3+zbar^2, loc6 exp(zbar), Kirsch, Tricorn; HOLO (must say holo, never anti) = Mandelbrot z^2+c, exp(z), 1/z, z^3+z; REAL-TRAP (must NOT be mistaken for genuine anti -- the SPARC trap) = |z|^2, z+zbar, log|z|^2, Re(z), Im(z), |z|^4, Re(z^2). RESULT on Anthony's machine: 18/18 correct after fix. The bench FOUND that judge_v2 (pre-fix) misclassified z+zbar, log|z|^2, Im(z) as ANTI -- the exact SPARC failure that killed the galaxies. Root cause: judge_v2 had no real-trap test; the naive guesses (rephasing-invariant+entangled) were too narrow, and a first mirror test missed i->-i (so Im(z) slipped through). FIX: a field is REAL-TRAPPED iff f == conj(f) under FULL conjugation (swap z<->zbar AND i->-i). Added to judge_v2.py (backup judge_v2.py.bak_20260618). This DIRECTLY answers Anthony's question 'can the improved tool be trusted to reveal hidden anti in holo-looking data?': not until it could refuse real-traps; now it can.
## Why this matters (Anthony's plasma/virus intuition, made precise)
You cannot extract anti-holomorphic content from data that has none (pure-holo: df/dzbar=0, nothing to
find -- a wall, not a difficulty). But a field BELIEVED holomorphic that is not quite (df/dzbar != 0 and
NOT real-trapped) could hide genuine anti structure -- that would be a real find. The bench guarantees
the tool no longer cries 'anti' on a real field (the SPARC trap), so a future 'anti' verdict on
holo-looking data is now CREDIBLE. First make the detector flawless on the known (the virus signature),
then trust it on the anomaly.
## Tests (executed on Anthony's machine, bench_calibration_maximal.py + judge_v2.py self-test)
 - bench: 18/18 correct (5 ANTI, 4 HOLO, 7 REAL-TRAP, 2 genuine-anti-not-real). [certified]
 - judge_v2 self-test block [0]: |z|^2, z+zbar, log|z|^2, Im(z) -> real-trapped; z+0.3zbar, i*zbar,
   exp(zbar) -> anti-holomorphic; z -> holomorphic. All OK. [certified]
 - blocks [1][2][3] (two-field, rephasing, mixed-derivative) still pass unchanged. [certified]
## Auditor note (three bench iterations, each found a real bug -- the point of a maximal bench)
(1) first criterion 'rephasing-invariant + entangled' too narrow -> missed z+zbar, log|z|^2;
(2) mirror test f==conj(f) but conj as bare z<->zbar swap missed i->-i -> misjudged Im(z) as anti;
(3) FULL conjugation (z<->zbar AND i->-i) -> 18/18. Each failure was a genuine blind spot exposed
BEFORE it could validate a false discovery. This is exactly why the maximal bench was the right call.
## Status
[ESTABLISHED sandbox->machine, TOOLING] judge_v2 now has the REAL-TRAP mirror test (SPARC guard);
18/18 calibration. verify_exact.py unchanged (single-field authority); judge_v2.py updated, backup
judge_v2.py.bak_20260618 kept. Reconnects: SPARC artefact lesson (real fields are mirror-locked);
judge_v2 base (58c61187); real-trapped category long-pending in reality_check.py now realized here.
Files: bench_calibration_maximal.py (new), judge_v2.py (updated), judge_v2.py.bak_20260618 (backup).
Arbiter = Anthony's machine (done).
