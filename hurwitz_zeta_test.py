"""
Hurwitz zeta function test with eml★ GP.
Test: can GP rediscover reflection-type relations involving conjugation?
"""
import numpy as np
from mpmath import mp, zeta, mpf, mpc
mp.dps = 30

print("=== Hurwitz Zeta Function Test ===")
print("Tabulating zeta(s, a) for complex s values...\n")

# Hurwitz zeta: zeta(s, a) = sum_{n=0}^{inf} 1/(n+a)^s
# We tabulate zeta(s, 1/4) and zeta(conj(s), 1/4)
# to see if GP finds the reflection relation

a = mpf('0.25')  # a = 1/4

# Complex s values (Re(s) > 1 for convergence)
s_values = [
    1.5 + 0.5j,  2.0 + 0.3j,  2.5 + 0.1j,
    1.8 - 0.4j,  2.2 + 0.7j,  3.0 - 0.2j,
    1.6 + 0.8j,  2.7 - 0.5j,  1.9 + 0.2j,
    2.1 - 0.6j,  2.4 + 0.4j,  3.5 + 0.1j,
    1.7 - 0.3j,  2.8 + 0.6j,  2.3 - 0.1j,
    1.5 + 0.9j,  3.2 - 0.4j,  2.6 + 0.3j,
]

print(f"Computing Hurwitz zeta(s, {a}) for {len(s_values)} values...")

z_arr = []
target_arr = []

for s in s_values:
    sm = mpc(s)
    # zeta(s, a)
    val = complex(zeta(sm, a))
    # zeta(conj(s), a) - involves conjugation
    val_conj = complex(zeta(mpc(s.real, -s.imag), a))
    
    # Target: ratio zeta(s,a) / zeta(conj(s),a)
    # This ratio involves conjugation structurally
    if abs(val_conj) > 1e-10:
        ratio = val / val_conj
    else:
        ratio = 0
    
    z_arr.append(complex(s))
    target_arr.append(ratio)
    print(f"  s={s:.1f}: zeta={val:.6f}, zeta(conj)={val_conj:.6f}, ratio={ratio:.6f}")

z_arr = np.array(z_arr)
target_arr = np.array(target_arr)

# Save data
np.savetxt('data/hurwitz_zeta_data.csv',
    np.column_stack([z_arr.real, z_arr.imag, target_arr.real, target_arr.imag]),
    header='s_real,s_imag,ratio_real,ratio_imag',
    delimiter=',', comments='')

print(f"\nData saved: data/hurwitz_zeta_data.csv")

# Run GP
print("\n=== Running GP on zeta(s,1/4) / zeta(conj(s),1/4) ===")
from discover_gp import run_gp
results = run_gp(z_arr, target_arr, pop=300, gen=50, runs=5)

print("\n=== DONE ===")
