#!/usr/bin/env python3
"""Gravitational time dilation vs chimera intrinsic clock -- correspondence test.

Question (framed 2026-07-06): can the certified intrinsic local clock of the
two-needle chimera (position-dependent winding rate, FINDINGS_20260629) serve
as the MECHANISM of gravitational time dilation (ground vs ISS clock offset)?

Honest protocol: calibrate the chimera ONCE (free choices: one radial scale =
switch-radius placement via the anti-needle coefficient), then PREDICT the
ground-vs-ISS fractional rate difference with no further tuning, and compare
to the general-relativity value. Controls: (i) fine radial sweep to expose the
functional FORM of each clock profile; (ii) adversarial calibration scan (the
step placed anywhere); (iii) mechanism-dependence test (two different needle
orders) against clock universality (equivalence principle).

No verdict is hardcoded: every comparison below is computed and printed.
Authority: THIS execution on Anthony's machine.
"""
import numpy as np

# ---------------------------------------------------------------- winding
def winding(f, R, n=8192):
    """Winding number of f around the circle |z| = R (closed loop)."""
    th = np.linspace(0.0, 2.0 * np.pi, n + 1)
    z = R * np.exp(1j * th)
    ang = np.unwrap(np.angle(f(z)))
    return (ang[-1] - ang[0]) / (2.0 * np.pi)

def chimera(p, q, a):
    """f(z) = z^p + a * conj(z)^q  (two needles of different order)."""
    return lambda z: z**p + a * np.conj(z)**q

# ---------------------------------------------------------------- GR side
G  = 6.67430e-11        # m^3 kg^-1 s^-2
M  = 5.9722e24          # kg (Earth)
c  = 2.99792458e8       # m/s
Re = 6.371e6            # m   (ground clock radius)
h_iss = 4.20e5          # m   (ISS altitude)
Ri = Re + h_iss
v_iss = 7.66e3          # m/s (ISS orbital speed)

grav_term = (G * M / c**2) * (1.0 / Re - 1.0 / Ri)   # ISS faster (gravity)
vel_term  = -v_iss**2 / (2.0 * c**2)                  # ISS slower (velocity)
d_net     = grav_term + vel_term                      # net fractional offset

print("=" * 74)
print("GR target: fractional rate difference (ISS relative to ground)")
print(f"  gravitational term : {grav_term:+.3e}")
print(f"  velocity term      : {vel_term:+.3e}")
print(f"  net                : {d_net:+.3e}   (~{d_net*86400*1e6:+.1f} us/day)")

# ---------------------------------------------------------- chimera side
print("=" * 74)
print("Chimera clock profile: winding of z^2 + a*conj(z)^5 vs radius (a=1)")
f25 = chimera(2, 5, 1.0)
grid = np.geomspace(0.05, 20.0, 25)
vals = np.array([winding(f25, R) for R in grid])
ints = np.round(vals)
print(f"  radii  : {np.array2string(grid, precision=2, max_line_width=74)}")
print(f"  winding: {np.array2string(ints.astype(int), max_line_width=74)}")
print(f"  max |winding - nearest integer| over sweep: {np.max(np.abs(vals - ints)):.2e}")
achieved = sorted(set(int(v) for v in ints))
print(f"  achieved values: {achieved}  (a step function; switch near R=1)")
sign_change = (min(achieved) < 0) and (max(achieved) > 0)
print(f"  sign inversion across the sweep: {sign_change}")

# GR profile over the SAME kind of sweep (ground -> 1000 km altitude)
alts = np.linspace(0.0, 1.0e6, 25)
gr_prof = (G * M / c**2) * (1.0 / Re - 1.0 / (Re + alts))
print("GR clock profile: fractional offset vs altitude (0 -> 1000 km)")
print(f"  range     : [{gr_prof.min():.3e}, {gr_prof.max():.3e}]")
print(f"  monotone  : {bool(np.all(np.diff(gr_prof) > 0))}")
print(f"  continuous: max step between adjacent altitudes = {np.max(np.diff(gr_prof)):.3e}")
print(f"  sign inversion: {bool(gr_prof.min() < 0 < gr_prof.max())}")

# ------------------------------------------- honest calibration + predict
print("=" * 74)
print("Honest protocol: calibrate switch radius anywhere, predict ground-vs-ISS")
# Map physical radius r -> plane radius R = r / Re (one allowed scale).
Rg, RiP = 1.0, Ri / Re
# Adversarial scan: place the switch radius s anywhere (via a = s^-3 for p=2,q=5)
preds = []
for s in np.geomspace(0.2, 5.0, 401):
    fa = chimera(2, 5, s ** (-3.0))
    dw = winding(fa, RiP) - winding(fa, Rg)
    preds.append(round(dw))
preds = sorted(set(preds))
print(f"  achievable predicted differences (all step placements): {preds}")
best = min(preds, key=lambda p: abs(p - d_net))
print(f"  GR requires: {d_net:+.3e}")
print(f"  nearest achievable: {best}  ->  residual {abs(best - d_net):.3e}")
if best == 0:
    print(f"  -> predicting 0 misses the ENTIRE measured effect (100% of it)")
nz = [abs(p) for p in preds if p != 0]
if nz:
    print(f"  smallest NONZERO prediction: {min(nz)}  vs required {abs(d_net):.1e}"
          f"  -> overshoot factor {min(nz)/abs(d_net):.1e}")

# ------------------------------------------------- universality control
print("=" * 74)
print("Universality (equivalence-principle) control: change the mechanism")
for (p, q) in [(2, 5), (3, 1), (1, 4)]:
    fa = chimera(p, q, 1.0)
    lo, hi = int(round(winding(fa, 0.3))), int(round(winding(fa, 3.0)))
    print(f"  needles (p={p}, q={q}): plateau values {lo} -> {hi}"
          f"   step size {abs(hi-lo)}")
print("  GR: ALL clock mechanisms show the SAME fractional offset (measured).")

# -------------------------------------------------------------- reading
print("=" * 74)
print("READING (computed above, no prior):")
print(f" 1. chimera profile = integer STEP function {achieved},"
      f" sign-inverting: {sign_change}")
print(f" 2. GR profile = continuous, monotone, tiny (max {gr_prof.max():.1e}),"
      f" never sign-inverting")
print(f" 3. achievable set is integers; required offset {d_net:+.1e} is not"
      f" integer-reachable except by 0, which predicts NO effect")
print(" 4. step size depends on needle orders (mechanism-dependent),"
      " violating clock universality")
print("STATUS: correspondence test between two established objects;"
      " this run certifies the comparison, not any physics claim.")
