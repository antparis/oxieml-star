# FINDINGS 2026-06-16 -- [ESTABLISHED on this QGT] Spinor-lock (lock d) CONFIRMED by the mixed-derivative discriminant, executed on Anthony's machine. The correct judge test for lock (d) is NOT the naive d/dzbar (nonzero for ANY function of real kx,ky -> false positive) but the MIXED second derivative d2 f / dz d zbar: zero => separable into independent holo(z)+antiholo(zbar); nonzero => holo and anti entangled via real arguments => spinor-lock. On the QGT projector element it is nonzero => lock d holds. Settles Milo condition (1).
## The discriminant
For f(z, zbar): mixed = d2 f / dz d zbar.
  mixed == 0  => f = h(z) + g(zbar) separable => z-bar is INDEPENDENT (would break the conjecture, Plateau B).
  mixed != 0  => holo and anti parts entangled => SPINOR-LOCK (lock d): the z-bar dependence is the
                 generic artefact of an object built from REAL arguments, not independent anti-holomorphy.
This is the rigorous test the naive Wirtinger d/dzbar cannot do (d/dzbar != 0 for any function of real
kx,ky, hence a false positive). The test is symmetric: it CAN break the conjecture (if mixed==0).
## Controls (executed)
  f = z + zbar       (separable)  : mixed = 0      [independent z-bar]
  f = z*zbar         (entangled)  : mixed = 1      [spinor-lock]
  f = 1/sqrt(z*zbar+1)            : mixed = (z*zbar-2)/(4(z*zbar+1)^(5/2)) != 0  [spinor-lock]
## QGT test (executed on Anthony's machine)
Quantum geometric tensor, lower-band projector element of the Qi-Wu-Zhang 2-band model (m=1):
  P01 = -(sin kx - i sin ky)/(2|d|),  |d|=sqrt(sin^2 kx + sin^2 ky + (1+cos kx+cos ky)^2),
  kx=(z+zbar)/2, ky=(z-zbar)/(2i)  (built from REAL momenta).
mixed = d2 P01 / dz dzbar evaluated at 3 generic independent (z,zbar) points:
  z=0.3+0.4i, zbar=0.2-0.1i  -> 8.26e-4 - 4.20e-4 i
  z=0.7-0.2i, zbar=0.5+0.6i  -> 2.59e-3 + 2.83e-3 i
  z=1.1+0.3i, zbar=-0.4+0.8i -> -1.03e-3 + 4.37e-3 i
All nonzero => NOT separable => SPINOR-LOCK CONFIRMED. Lock (d) holds for this QGT.
## Status and honest limits
[ESTABLISHED on this QGT] -- certified on Anthony's machine, no longer sandbox-only. Upgrades the
QGT case of the conjecture (4b688563) from sandbox-argument to machine-certified for lock (d).
LIMIT: confirms spinor-lock on the QWZ QGT; does NOT yet prove NO QGT object escapes spinor-lock
(Milo condition 2 still open -- need to check any natively-complex-variable formulation). Does NOT
prove the general exhaustion (a)-(d). The mixed-derivative discriminant is now a reusable tool to add
to the pipeline alongside verify_exact.py.
Arbiter = execution on Anthony's machine (done). Discriminant: mixed d2/dz dzbar.
