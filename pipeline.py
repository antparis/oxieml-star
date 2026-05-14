#!/usr/bin/env python3
"""
Pipeline: Python GP -> Rust Adam optimizer
1. Run GP to find best formula structures
2. Convert to EML-only format
3. Send to Rust for constant optimization
"""
import subprocess
import sys
import re
import os

def extract_eml_subtrees(formula):
    """Extract eml/eml_star subtrees from a GP formula."""
    trees = []
    # Find all eml(...) and eml_star(...) with balanced parens
    for match in re.finditer(r'(eml_star|eml)\(', formula):
        start = match.start()
        depth = 0
        for i in range(start, len(formula)):
            if formula[i] == '(':
                depth += 1
            elif formula[i] == ')':
                depth -= 1
                if depth == 0:
                    trees.append(formula[start:i+1])
                    break
    return trees

def gp_to_eml(formula):
    """Convert GP formula to pure EML format for Rust."""
    # Replace named constants with one/zero
    s = formula
    s = re.sub(r'\bhalf\b', 'one', s)
    s = re.sub(r'\bfive\b', 'one', s)
    s = re.sub(r'\btwo\b', 'one', s)
    s = re.sub(r'\btwentyfive\b', 'one', s)
    s = re.sub(r'\bln10\b', 'one', s)
    s = re.sub(r'\bpi\b', 'one', s)
    s = re.sub(r'\bimag_i\b', 'one', s)
    s = re.sub(r'\([0-9.-]+\+0j\)', 'one', s)
    
    # Extract deepest eml/eml_star subtree
    trees = extract_eml_subtrees(s)
    if trees:
        # Return the longest (deepest) one
        return max(trees, key=len)
    
    # If no eml/eml_star found, wrap in eml
    return f"eml(z, one)"

def run_pipeline(csv_path, pop=500, gen=80, runs=5):
    """Full pipeline: GP -> extract EML -> Rust optimize."""
    
    print("=" * 60)
    print("  Pipeline: Python GP -> Rust Adam")
    print("=" * 60)
    
    # Step 1: Run GP
    print("\n[Step 1] Running Python GP...")
    result = subprocess.run(
        ["python3", "discover_gp.py", "--csv", csv_path,
         "--pop", str(pop), "--gen", str(gen), "--runs", str(runs)],
        capture_output=True, text=True
    )
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    
    # Extract best formula from results
    results_path = csv_path.replace(".csv", "_results.txt")
    if not os.path.exists(results_path):
        print("No results file found")
        return
    
    with open(results_path) as f:
        lines = f.readlines()
    
    if not lines:
        print("Empty results")
        return
    
    # Parse best formulas
    formulas = []
    for line in lines[:10]:
        m = re.search(r'MSE=(\S+)\s+eml_star=\S+\s+(.*)', line)
        if m:
            mse = float(m.group(1))
            formula = m.group(2).strip()
            formulas.append((mse, formula))
    
    if not formulas:
        print("Could not parse formulas")
        return
    
    formulas.sort()
    print(f"\n[Step 2] Top {min(5, len(formulas))} GP formulas:")
    for mse, f in formulas[:5]:
        print(f"  MSE={mse:.4e}  {f[:80]}")
    
    # Step 3: Convert to EML and optimize in Rust
    # Create data file in Rust format
    rust_data = csv_path.replace("_python.csv", "_rust.txt").replace(".csv", "_rust.txt")
    if not os.path.exists(rust_data):
        # Convert CSV to space-separated
        with open(csv_path) as f:
            next(f)  # skip header
            with open(rust_data, "w") as out:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 4:
                        out.write(f"{parts[0]} {parts[2]}\n")
    
    print(f"\n[Step 3] Optimizing in Rust...")
    for mse, formula in formulas[:3]:
        eml_formula = gp_to_eml(formula)
        print(f"\n  GP: {formula[:60]}...")
        print(f"  EML: {eml_formula}")
        
        result = subprocess.run(
            ["./target/release/oxieml", "--optimize-formula", eml_formula,
             "--vars", "1", "--file", rust_data],
            capture_output=True, text=True
        )
        
        # Extract final MSE
        for line in result.stderr.split("\n"):
            if "Optimized" in line or "Early" in line:
                print(f"  Rust: {line.strip()}")
        for line in result.stdout.split("\n"):
            if "Optimized" in line or "Params" in line:
                print(f"  Rust: {line.strip()}")
    
    print(f"\n{'=' * 60}")
    print("  Pipeline complete")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline.py data.csv [--pop 500] [--gen 80] [--runs 5]")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    pop = 500
    gen = 80
    runs = 5
    
    i = 2
    while i < len(sys.argv) - 1:
        if sys.argv[i] == "--pop": pop = int(sys.argv[i+1])
        elif sys.argv[i] == "--gen": gen = int(sys.argv[i+1])
        elif sys.argv[i] == "--runs": runs = int(sys.argv[i+1])
        i += 2
    
    run_pipeline(csv_path, pop, gen, runs)
