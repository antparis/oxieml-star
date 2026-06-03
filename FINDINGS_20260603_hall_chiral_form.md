# FINDINGS 2026-06-03 -- Hall chiral field: the CORRECT mathematical form [DERIVATION]

## Status
[DERIVATION] sound reasoning + coherent closed form + double encadrement verified
in SymPy, BUT one motivated step not formally proven (handedness->z/zbar assignment).
Upgrades the earlier [CONJECTURE] (algebraic 1/z + i d_i/zbar) which is now SUPERSEDED.

## The correct form (replaces the conjecture)
  F(z,zbar) = |z|*K1(|z|)/z  +  |z|*K1(|z|/d_i)/zbar
  - holomorphic part: MHD long mode, screened at scale 1, carried on 1/z
  - anti-holomorphic part: Hall short mode, screened at scale d_i, carried on 1/zbar
  - TRANSCENDENTAL (Bessel K1), NOT algebraic 1/zbar. Consistent with Hasegawa-Mima.

## Derived from (not posited)
Double-Beltrami eigenvalues (Yoshida-Mahajan-Ohsaki): roots of
  lambda^2 - (1/eps)(b-1/a) lambda + (1-b/a)/eps^2 = 0, eps=d_i/L.
  product lambda_+ lambda_- = (a-b)/(a eps^2) < 0 when b>a => OPPOSITE handedness.
Localized decaying curl-eigenfield => modified Helmholtz => Bessel K screening.
Hall short mode screened at kappa ~ 1/d_i; MHD long mode at kappa ~ 1.

## Chirality test (SymPy, executed)
  F - conj(F) != 0  => genuinely complex, NOT mirror-locked.
  Reason: anti = |z| K1(|z|/d_i)/zbar  vs  conj(holo) = |z| K1(|z|)/zbar.
  These differ UNLESS the two screening scales coincide.
  => b != conj(a) is FORCED by d_i != 1 (Hall scale != MHD scale).
  CHIRALITY IS THE SCALE SEPARATION.

## Double encadrement (two independent vanishings)
  (1) d_i -> 0: anti part |z| K1(|z|/d_i)/zbar -> 0 (exponential screening,
      SINGULAR limit, verified both at fixed r and inside the shrinking layer).
  (2) d_i = 1: anti - conj(holo) = 0 exactly => mirror-locked (no scale
      separation => no chirality). Verified in SymPy.
  Both confirm: chirality is physics-forced by Hall scale separation, removable
  only by killing the Hall scale (d_i->0) or merging it with MHD (d_i->1).

## What remains NOT formally derived (honest)
The assignment "negative-handedness (Hall) mode -> 1/zbar, positive-handedness
(MHD) mode -> 1/z" is PHYSICALLY MOTIVATED (opposite-sign curl eigenvalues =
opposite handedness, research-supported) but NOT proven line-by-line from
curl v = lambda v in the complex-velocity representation. This is the single
remaining gap between [DERIVATION] and [ESTABLISHED].

## Next
- Close the gap: derive handedness->(z or zbar) carrying from curl v = lambda v
  in complex-velocity form. THEN generator + pipeline + judge.
- Generator target: F above, with d_i a free parameter; controls d_i->0 (anti
  vanishes) and d_i=1 (mirror). Add Bessel K to PySR toolbox for clean recovery.

## CORRECTION (2026-06-03, same day) -- the handedness justification was WRONG
Derivation from curl v = lambda v in complex form (SymPy, executed) shows:
 - v_z obeys Helmholtz ∇²v_z = -lambda^2 v_z : depends on lambda^2, SIGN-BLIND.
 - in-plane complex velocity w = (2i/lambda) dv_z/dz.
 - m=0 radial mode: w ∝ zbar; sign(lambda) only flips the SIGN of w, does NOT
   swap z<->zbar. => a mode is NOT made chiral by the sign of lambda. MIRROR.
 - => the earlier claim "opposite-sign curl eigenvalues -> one mode on z, other
   on zbar" is FALSE. The sign of lambda does not carry chirality.
 - TRUE carrier of chirality: opposite ANGULAR WINDING m=+1 vs m=-1 (verified:
   a field from m=+1 and m=-1 screened modes has F-conj(F)!=0, anti present,
   and the Hall m=-1 part vanishes as d_i->0, encadrement OK).

## Re-localized open question (the real remaining gap)
NOT "why does sign(lambda) carry z/zbar" (answered: it does not), BUT:
  "what forces the Hall mode to have angular winding m OPPOSITE to the MHD mode?"
Until that is derived from Hall-MHD, the opposite-winding pair is POSITED, not
derived -- the same kind of unproven step as before, moved from sign(lambda) to
sign(m). Status stays [DERIVATION] with the gap now precisely identified.

## Net result of this session's gap-closing attempt
Did NOT close the gap. BUT eliminated a false lead (sign of lambda) and
identified the true seat of 2D chirality: the angular winding number m. The
superseded algebraic conjecture AND the sign(lambda) justification are both
retired. The screened transcendental form stands, but its chirality must come
from opposite m, whose physical origin is the next thing to derive.
