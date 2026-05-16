"""
Joukowski transform test — holomorphic vs non-holomorphic.
Test 1: w = z + 1/z (Joukowski, holomorphic — used in aerodynamics)
Test 2: w = z + 1/conj(z) (non-holomorphic version)
If eml★ works: Test 1 = 0/5, Test 2 = 5/5
"""
import numpy as np
from discover_gp import run_gp

# Points on a circle-ish region, avoid z=0
np.random.seed(42)
r = 1.2 + 0.3 * np.random.randn(25)
theta = np.linspace(0.1, 2*np.pi - 0.1, 25)
z = r * np.exp(1j * theta)

# === TEST 1: Joukowski (holomorphic) ===
print("=" * 60)
print("TEST 1: Joukowski transform w = z + 1/z")
print("EXPECT: eml★ = 0/5 (holomorphic)")
print("=" * 60)
target1 = z + 1.0/z
results1 = run_gp(z, target1, pop=300, gen=40, runs=5)

# === TEST 2: Non-holomorphic Joukowski ===
print("\n" + "=" * 60)
print("TEST 2: w = z + 1/conj(z)")
print("EXPECT: eml★ = 5/5 (non-holomorphic)")
print("=" * 60)
target2 = z + 1.0/np.conj(z)
results2 = run_gp(z, target2, pop=300, gen=40, runs=5)

# === TEST 3: Bonus — mixed ===
print("\n" + "=" * 60)
print("TEST 3: w = exp(z) + exp(conj(z)) = 2*exp(Re(z))*cos(Im(z))")
print("EXPECT: eml★ active (mixed holomorphic/anti-holomorphic)")
print("=" * 60)
target3 = np.exp(z) + np.exp(np.conj(z))
results3 = run_gp(z, target3, pop=300, gen=40, runs=5)

print("\n=== SUMMARY ===")
print("Test 1 (z + 1/z, holomorphic):       expect eml★ = 0")
print("Test 2 (z + 1/conj(z), non-holo):    expect eml★ = 5")
print("Test 3 (exp(z)+exp(conj(z)), mixed): expect eml★ > 0")
print("=== DONE ===")
