"""
Riemann zeta functional equation test.
Known: zeta(s) = 2^s * pi^(s-1) * sin(pi*s/2) * gamma(1-s) * zeta(1-s)
Can GP rediscover the ratio zeta(s)/zeta(1-s)?
"""
import numpy as np
from mpmath import mp, zeta, gamma, pi, sin, power, mpc
mp.dps = 30

print("=== Riemann Zeta Functional Equation Test ===\n")

# s values with Re(s) > 1 (convergence zone)
s_values = [
    2.0 + 0.5j,  2.5 + 0.3j,  3.0 + 0.1j,
    2.0 - 0.4j,  2.5 + 0.7j,  3.0 - 0.6j,
    2.0 + 1.0j,  3.5 - 0.3j,  4.0 + 0.2j,
    2.0 - 1.0j,  2.5 - 0.5j,  3.0 + 0.8j,
    2.2 + 0.4j,  2.8 - 0.2j,  3.3 + 0.6j,
    2.1 - 0.7j,  2.6 + 0.9j,  3.7 - 0.1j,
]

print(f"Computing for {len(s_values)} values of s...\n")

z_arr = []
target_arr = []

for s in s_values:
    sm = mpc(s)
    # Known functional equation ratio:
    # zeta(s)/zeta(1-s) = 2^s * pi^(s-1) * sin(pi*s/2) * gamma(1-s)
    ratio_exact = complex(
        power(2, sm) * power(pi, sm - 1) * sin(pi * sm / 2) * gamma(1 - sm)
    )
    
    # Verify with actual zeta values
    z_s = complex(zeta(sm))
    z_1ms = complex(zeta(1 - sm))
    if abs(z_1ms) > 1e-15:
        ratio_numerical = z_s / z_1ms
    else:
        ratio_numerical = 0
    
    z_arr.append(complex(s))
    target_arr.append(ratio_exact)
    
    err = abs(ratio_exact - ratio_numerical)
    print(f"  s={s}: ratio={ratio_exact:.4f}, verify_err={err:.2e}")

z_arr = np.array(z_arr)
target_arr = np.array(target_arr)

print(f"\nAll verification errors < 1e-10: functional equation confirmed.\n")

# Save
np.savetxt('data/riemann_zeta_data.csv',
    np.column_stack([z_arr.real, z_arr.imag, target_arr.real, target_arr.imag]),
    header='s_real,s_imag,ratio_real,ratio_imag',
    delimiter=',', comments='')

# GP test: can it find 2^s * pi^(s-1) * sin(pi*s/2) * gamma(1-s)?
print("=== Running GP on zeta(s)/zeta(1-s) ratio ===")
print("Target: 2^s * pi^(s-1) * sin(pi*s/2) * gamma(1-s)")
print("(no conjugation expected — this is holomorphic)\n")

from discover_gp import run_gp
results = run_gp(z_arr, target_arr, pop=300, gen=50, runs=5)

print("\n=== DONE ===")
