# FINDINGS 2026-06-23a -- judge_v2 module criterion unified (radial chirp blind spot fixed)

Status: [ESTABLISHED] -- patch executed + bench-certified on machine (38/38), no regression.

## Trigger
certify_schrodinger.py: the FREE dispersive wave packet exp(-|z|^2/(2(1+it))) -- a
HERMITIAN Schrodinger solution -- was judged ANTI by judge_v2. It factors as
real_gaussian x radial_chirp exp(i|z|^2/4): everything depends on |z|^2, so it is
radial, NOT chiral. Judging it anti was a blind spot (same family as the |z|^(is)
patch 2026-06-22d/e, one level up: pure-imaginary L that is |z|^2-dependent, not
constant; and here L is fully complex = real gaussian part + imag chirp part).

## Root cause
is_module_trapped accepted module only if  prod_only AND (L_real OR (L_const AND
L_pure_imag)), where L = zbar*dlog(f)/dzbar. These real / pure-imag-constant
sub-cases were too narrow: a COMPLEX radial envelope (gaussian x chirp) gives L
that is |z|^2-only but neither real nor pure-imaginary -> missed.

## Fix (one line)
    OLD: return bool((L_real or (L_const and L_pure_imag)) and prod_only)
    NEW: return bool(prod_only)
Rationale: L = zbar*dlog(f)/dzbar depends on |z|^2 ONLY  <=>  f = holo(z) *
radial_envelope(|z|^2) (real OR complex)  <=>  reducible to holomorphic by radial
division  <=>  not genuinely chiral. The earlier real/pure-imag conditions were
special cases now subsumed.

## Exact commands + raw result (on machine)
    cp judge_v2.py judge_v2_BACKUP_20260623_023558.py   # backup first (pivot rule)
    # one-line patch applied to is_module_trapped
    python3 cnative_bench.py --no-random
        -> generated/scored 38/38, errors 0, PASS 38/38, FAIL 0, No failures.
    python3 certify_schrodinger.py
        -> dispersive packet judge: anti-holomorphic -> module-trapped (FIXED);
           LLL/Landau-n1/AB -> module; real bound state -> real; holo irreproachable True.

## Adversarial check (sandbox, pre-patch)
prod_only-only criterion catches dispersive packet, pure chirp exp(i|z|^2/4),
|z|^(is), LLL; and leaks NO genuine anti (log(zbar), exp(zbar), zbar^2 exp(zbar),
mixed z^3+conj z^2, exp(zbar)*gaussian all stay anti). LEAK INTO MODULE: False.

## Caveat (tooling only, not a discovery)
This is a CERTIFIER refinement: it improves how the tool classifies a known
hermitian wavefunction. It is NOT a chiral discovery. The chiral cell stays EMPTY.
The certify_schrodinger.py in-script ORACLE still encodes the old criterion and now
prints DIFF/9-of-10 on the dispersive packet (oracle stale, judge correct); to be
realigned to prod_only in a follow-up (cosmetic; the judge verdict is authoritative).

## Files
judge_v2.py (patched), judge_v2_BACKUP_20260623_023558.py (backup), certify_schrodinger.py.
