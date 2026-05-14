#!/usr/bin/env python3
"""Batch test all SPARC galaxies in data/ folder."""
import subprocess, re, time, os, numpy as np

csvs = sorted([f for f in os.listdir("data") if f.startswith("sparc_") and f.endswith(".csv")])
print(f"Found {len(csvs)} galaxies")
print("=" * 70)

results = []
for idx, csv in enumerate(csvs):
    path = f"data/{csv}"
    name = csv.replace("sparc_", "").replace(".csv", "").upper()
    pts = sum(1 for _ in open(path)) - 1
    
    start = time.time()
    r = subprocess.run(
        ["python3", "discover_gp.py", "--csv", path, "--pop", "200", "--gen", "40", "--runs", "1"],
        capture_output=True, text=True, timeout=120)
    elapsed = time.time() - start
    
    mse, formula, star = None, "?", False
    for line in r.stdout.split("\n"):
        m = re.search(r'Best MSE:\s+(\S+)', line)
        if m: mse = float(m.group(1))
        m = re.search(r'Formula:\s+(.*)', line)
        if m:
            formula = m.group(1).strip()[:60]
            star = "eml_star" in formula or "conj_eml" in formula
    
    if mse is not None:
        results.append((name, pts, mse, star, formula, elapsed))
        s = " [eml*]" if star else ""
        print(f"[{idx+1:3d}/{len(csvs)}] {name:14s} {pts:3d}pts MSE={mse:.2e}{s} ({elapsed:.1f}s)")

results.sort(key=lambda x: x[2])
print(f"\n{'='*70}")
print(f"  RESULTS: {len(results)} galaxies")
print(f"{'='*70}")
mses = [r[2] for r in results]
print(f"Median MSE: {np.median(mses):.4e}")
print(f"Best: {results[0][0]} MSE={results[0][2]:.4e}")
print(f"MSE < 1e-3: {sum(1 for m in mses if m<1e-3)}/{len(results)}")
print(f"MSE < 1e-2: {sum(1 for m in mses if m<1e-2)}/{len(results)}")
print(f"eml*: {sum(1 for r in results if r[3])}/{len(results)}")
