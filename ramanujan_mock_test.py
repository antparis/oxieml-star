"""
Ramanujan mock theta function tests with eml★ GP.
Test 1: Rediscover known identity between f(q) and phi(q) (order 3).
Test 2: Order 5 relations (f0, f1, phi0, phi1).
Test 3: Cross-order relation.
"""
import numpy as np
from mpmath import mp, mpf, mpc, power, fsum

mp.dps = 50  # 50 decimal places

# === Order 3 mock theta functions ===
def mock_f3(q, N=80):
    """f(q) = 1 + sum q^{n^2} / prod_{k=1}^{n} (1+q^k)"""
    s = mpf(1)
    for n in range(1, N):
        num = power(q, n*n)
        den = fsum([0]) + 1
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 + power(q, k))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

def mock_phi3(q, N=80):
    """phi(q) = 1 + sum q^{n^2} / prod_{k=1}^{n} (1+q^{2k})"""
    s = mpf(1)
    for n in range(1, N):
        num = power(q, n*n)
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 + power(q, 2*k))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

def mock_chi3(q, N=80):
    """chi(q) = 1 + sum q^{n^2} / prod_{k=1}^{n} (1 - q^k + q^{2k})"""
    s = mpf(1)
    for n in range(1, N):
        num = power(q, n*n)
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 - power(q, k) + power(q, 2*k))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

def mock_psi3(q, N=80):
    """psi(q) = sum_{n=1} q^{n^2} / prod_{k=1}^{n} (1 - q^{2k-1})"""
    s = mpf(0)
    for n in range(1, N):
        num = power(q, n*n)
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 - power(q, 2*k - 1))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

# === Order 5 mock theta functions ===
def mock_f0_5(q, N=60):
    """f0(q) = sum q^{n^2} / prod_{k=1}^{n} (1+q^k)  [order 5 version]"""
    s = mpf(0)
    for n in range(0, N):
        num = power(q, n*n)
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 + power(q, k))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

def mock_phi0_5(q, N=60):
    """phi0(q) = sum q^{n*(n+1)/2} / prod_{k=1}^{n} (1+q^k)"""
    s = mpf(0)
    for n in range(0, N):
        num = power(q, n*(n+1)//2)
        prod = mpf(1)
        for k in range(1, n+1):
            prod *= (1 + power(q, k))
        if abs(prod) < 1e-100:
            break
        s += num / prod
    return complex(s)

# === Generate data ===
print("=== Generating mock theta function data ===")
print("(this may take 1-2 minutes at 50 dps)")

# Use q values inside unit disk, real and complex
q_real = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9]
q_complex = [0.5 + 0.1j, 0.3 + 0.2j, 0.4 - 0.1j, 0.6 + 0.05j, 
             0.2 + 0.3j, 0.7 - 0.1j, 0.1 + 0.1j, 0.5 - 0.2j]

q_all = [complex(q) for q in q_real] + q_complex

print(f"\nComputing for {len(q_all)} q values...")

data = {}
for i, q in enumerate(q_all):
    qm = mpc(q)
    f = mock_f3(qm)
    phi = mock_phi3(qm)
    chi = mock_chi3(qm)
    psi = mock_psi3(qm)
    data[q] = {'f': f, 'phi': phi, 'chi': chi, 'psi': psi}
    print(f"  q={q}: f={f:.6f}, phi={phi:.6f}")

# === Test 1: Known relation ===
# Watson (1936): f(q) + 2*psi(q) has a known theta function expression
# Simpler check: verify 2*phi(-q) - f(-q) relation
print("\n=== TEST 1: Relation between f(q) and phi(q) ===")
print("Checking: f(q) - 2*phi(q) + 1 pattern")
for q in q_real[:5]:
    f_val = data[complex(q)]['f']
    phi_val = data[complex(q)]['phi']
    diff = f_val - 2 * phi_val
    print(f"  q={q}: f={f_val:.8f}, phi={phi_val:.8f}, f-2phi={diff:.8f}")

# === GP test on f(q) from q ===
print("\n=== TEST 2: GP discovers f(q) structure ===")
z_arr = np.array(q_all)
f_arr = np.array([data[q]['f'] for q in q_all])

# Save data for GP
np.savetxt('data/ramanujan_f3_data.csv',
           np.column_stack([z_arr.real, z_arr.imag, f_arr.real, f_arr.imag]),
           header='z_real,z_imag,target_real,target_imag',
           delimiter=',', comments='')

# Save phi data
phi_arr = np.array([data[q]['phi'] for q in q_all])
np.savetxt('data/ramanujan_phi3_data.csv',
           np.column_stack([z_arr.real, z_arr.imag, phi_arr.real, phi_arr.imag]),
           header='z_real,z_imag,target_real,target_imag',
           delimiter=',', comments='')

# Save relation data: target = f(q)/phi(q) ratio
ratio = f_arr / phi_arr
np.savetxt('data/ramanujan_f_over_phi_data.csv',
           np.column_stack([z_arr.real, z_arr.imag, ratio.real, ratio.imag]),
           header='z_real,z_imag,target_real,target_imag',
           delimiter=',', comments='')

print(f"\nData saved: {len(q_all)} points")
print("  data/ramanujan_f3_data.csv")
print("  data/ramanujan_phi3_data.csv") 
print("  data/ramanujan_f_over_phi_data.csv")

# Now run GP on the ratio f/phi
print("\n=== Running GP on f(q)/phi(q) ratio ===")
from discover_gp import run_gp
results = run_gp(z_arr, ratio, pop=300, gen=50, runs=5)
print("\n=== DONE ===")
