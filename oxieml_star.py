"""
oxieml_star — Pure Python wrapper for eml★ symbolic regression.

No Rust compilation needed. Just numpy.

Usage:
    from oxieml_star import eml, eml_star, conj_eml, mod_squared, real_part
    from oxieml_star import discover_formula

    # Basic operators
    z = 1.0 + 0.5j
    print(eml(z, 1.0))         # exp(z) - ln(1) = exp(z)
    print(eml_star(z, z))      # exp(z) - ln(conj(z))
    print(conj_eml(z))         # conj(z) via Theorem 3.1
    print(mod_squared(z))      # |z|^2 via eml_star

    # Discover formulas from data
    import numpy as np
    z_data = np.array([1+0.5j, 2-1j, 0.5+0.3j, -1+2j])
    targets = np.conj(z_data)  # unknown to the engine
    results = discover_formula(z_data, targets, max_depth=2)
    for r in results[:5]:
        print(r)
"""

import numpy as np
import warnings
from typing import List, Tuple, Optional
import itertools
import time


# ============================================================
# Core Operators
# ============================================================

def eml(x, y):
    """EML operator: eml(x, y) = exp(x) - ln(y)
    
    Odrzywołek (2026). The continuous Sheffer operator.
    """
    x = np.asarray(x, dtype=complex)
    y = np.asarray(y, dtype=complex)
    y_safe = np.where(np.abs(y) < 1e-30, 1e-30 + 0j, y)
    x_clamped = np.clip(x.real, -709, 709) + 1j * x.imag
    return np.exp(x_clamped) - np.log(y_safe)


def eml_star(x, y):
    """EML-star operator: eml★(x, y) = exp(x) - ln(conj(y))
    
    Monnerot (2026). Anti-holomorphic companion operator.
    The ONLY difference from eml is the conjugation of y before ln.
    """
    x = np.asarray(x, dtype=complex)
    y = np.asarray(y, dtype=complex)
    y_conj = np.conj(y)
    y_safe = np.where(np.abs(y_conj) < 1e-30, 1e-30 + 0j, y_conj)
    x_clamped = np.clip(x.real, -709, 709) + 1j * x.imag
    return np.exp(x_clamped) - np.log(y_safe)


def conj_eml(z):
    """Complex conjugation via Theorem 3.1 (Monnerot 2026).
    
    conj(z) = 1 - eml★(0, eml(z, 1))
    Valid for Im(z) in [-pi, pi).
    """
    z = np.asarray(z, dtype=complex)
    if np.any(np.abs(z.imag) >= np.pi):
        warnings.warn("conj_eml: some Im(z) outside [-pi, pi). Results unreliable there.")
    zero = np.zeros_like(z)
    one = np.ones_like(z)
    inner = eml(z, one)          # eml(z, 1) = exp(z)
    star = eml_star(zero, inner) # eml★(0, exp(z)) = 1 - conj(z)
    return one - star


def mod_squared(z):
    """|z|^2 = z * conj(z) via eml★.
    
    Monnerot (2026), Corollary of Theorem 3.1.
    """
    return z * conj_eml(z)


def real_part(z):
    """Re(z) = (z + conj(z)) / 2 via eml★."""
    return (z + conj_eml(z)) / 2


def imag_part(z):
    """Im(z) = (z - conj(z)) / (2i) via eml★."""
    return (z - conj_eml(z)) / 2j


# ============================================================
# Tree Representation
# ============================================================

class EmlTree:
    """Symbolic EML/EML-star tree."""
    
    def __init__(self, kind, left=None, right=None, var_idx=None):
        self.kind = kind  # 'one', 'var', 'eml', 'eml_star'
        self.left = left
        self.right = right
        self.var_idx = var_idx
    
    def eval(self, vars):
        """Evaluate tree on complex variable array."""
        if self.kind == 'one':
            return np.ones_like(vars[0]) if len(vars) > 0 else 1.0+0j
        elif self.kind == 'zero':
            return np.zeros_like(vars[0]) if len(vars) > 0 else 0.0+0j
        elif self.kind == 'var':
            return vars[self.var_idx]
        elif self.kind == 'eml':
            l = self.left.eval(vars)
            r = self.right.eval(vars)
            return eml(l, r)
        elif self.kind == 'eml_star':
            l = self.left.eval(vars)
            r = self.right.eval(vars)
            return eml_star(l, r)
    
    def depth(self):
        if self.kind in ('one', 'zero', 'var'):
            return 0
        return 1 + max(self.left.depth(), self.right.depth())
    
    def size(self):
        if self.kind in ('one', 'zero', 'var'):
            return 1
        return 1 + self.left.size() + self.right.size()
    
    def has_eml_star(self):
        if self.kind == 'eml_star':
            return True
        if self.kind in ('one', 'zero', 'var'):
            return False
        return self.left.has_eml_star() or self.right.has_eml_star()
    
    def __str__(self):
        if self.kind == 'one':
            return '1'
        elif self.kind == 'zero':
            return '0'
        elif self.kind == 'var':
            return f'x{self.var_idx}'
        elif self.kind == 'eml':
            return f'eml({self.left}, {self.right})'
        elif self.kind == 'eml_star':
            return f'eml_star({self.left}, {self.right})'
    
    def __repr__(self):
        return self.__str__()


# ============================================================
# Topology Enumeration
# ============================================================

def enumerate_topologies(max_depth, num_vars=1):
    """Enumerate all EML/EML-star tree topologies up to max_depth."""
    leaves = [EmlTree('one'), EmlTree('zero')]
    for i in range(num_vars):
        leaves.append(EmlTree('var', var_idx=i))
    
    by_depth = {0: list(leaves)}
    
    for d in range(1, max_depth + 1):
        trees = []
        # Collect all trees at depth < d
        below = []
        for dd in range(d - 1):
            below.extend(by_depth[dd])
        
        at_prev = by_depth[d - 1]
        
        # Case 1: both children at depth d-1
        for l in at_prev:
            for r in at_prev:
                trees.append(EmlTree('eml', l, r))
                trees.append(EmlTree('eml_star', l, r))
        
        # Case 2: left at d-1, right below
        for l in at_prev:
            for r in below:
                trees.append(EmlTree('eml', l, r))
                trees.append(EmlTree('eml_star', l, r))
        
        # Case 3: left below, right at d-1
        for l in below:
            for r in at_prev:
                trees.append(EmlTree('eml', l, r))
                trees.append(EmlTree('eml_star', l, r))
        
        by_depth[d] = trees
    
    all_trees = []
    for d in range(max_depth + 1):
        all_trees.extend(by_depth[d])
    
    return all_trees


# ============================================================
# Complex Symbolic Regression
# ============================================================

def complex_mse(tree, z_data, targets):
    z_data = np.asarray(z_data, dtype=complex)
    """Compute MSE = mean(|pred - target|^2) for complex data."""
    try:
        if isinstance(z_data, np.ndarray) and z_data.ndim == 1:
            vars = [z_data]
        else:
            vars = [z_data[:, i] for i in range(z_data.shape[1])]
        
        pred = tree.eval(vars)
        err = pred - targets
        mse = np.mean(np.abs(err) ** 2)
        
        if np.isfinite(mse):
            return float(mse)
        return float('inf')
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return float('inf')


def discover_formula(z_data, targets, max_depth=2, num_vars=1, top_k=10):
    """Discover symbolic formulas from complex-valued data.
    
    Parameters
    ----------
    z_data : np.ndarray, shape (n,) or (n, num_vars), dtype complex
        Input complex data.
    targets : np.ndarray, shape (n,), dtype complex
        Target complex values.
    max_depth : int
        Maximum tree depth to search.
    num_vars : int
        Number of input variables.
    top_k : int
        Number of top formulas to return.
    
    Returns
    -------
    list of dict with keys: 'formula', 'mse', 'size', 'has_eml_star'
    """
    z_data = np.asarray(z_data, dtype=complex)
    targets = np.asarray(targets, dtype=complex)
    
    print(f"Enumerating topologies (depth <= {max_depth}, {num_vars} var(s))...")
    topologies = enumerate_topologies(max_depth, num_vars)
    print(f"Topologies: {len(topologies)}")
    
    print("Evaluating...")
    start = time.time()
    
    results = []
    for tree in topologies:
        mse = complex_mse(tree, z_data, targets)
        if np.isfinite(mse):
            results.append({
                'formula': str(tree),
                'mse': mse,
                'size': tree.size(),
                'has_eml_star': tree.has_eml_star(),
            })
    
    results.sort(key=lambda r: r['mse'])
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s. Valid: {len(results)}/{len(topologies)}")
    
    return results[:top_k]


def verify_theorem_31(z_data):
    """Verify Theorem 3.1: conj(z) = 1 - eml★(0, eml(z, 1)) on given data.
    
    Returns MSE between eml★-computed conj and native np.conj.
    """
    z_data = np.asarray(z_data, dtype=complex)
    conj_native = np.conj(z_data)
    conj_eml_result = conj_eml(z_data)
    mse = float(np.mean(np.abs(conj_eml_result - conj_native) ** 2))
    status = "EXACT" if mse < 1e-20 else "APPROX"
    print(f"Theorem 3.1 verification: MSE = {mse:.2e} [{status}] on {len(z_data)} points")
    return mse


# ============================================================
# Quick Demo
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  OxiEML-Star — Python Wrapper")
    print("  eml★(x, y) = exp(x) - ln(conj(y))")
    print("  Monnerot (2026)")
    print("=" * 60)
    
    # Demo 1: Basic operators
    z = 1.0 + 0.5j
    print(f"\nz = {z}")
    print(f"eml(z, 1)     = {eml(z, 1.0):.6f}  (= exp(z))")
    print(f"eml_star(z,z) = {eml_star(z, z):.6f}")
    print(f"conj_eml(z)   = {conj_eml(z):.6f}  (expected: {np.conj(z)})")
    print(f"|z|^2 via eml★ = {mod_squared(z):.6f}  (expected: {abs(z)**2:.6f})")
    print(f"Re(z) via eml★ = {real_part(z):.6f}  (expected: {z.real})")
    
    # Demo 2: Verify Theorem 3.1
    print()
    grid = np.linspace(-2, 2, 20)
    re, im = np.meshgrid(grid, grid)
    z_grid = (re + 1j * im).ravel()
    mask = (np.abs(z_grid.imag) < np.pi - 0.1) & (np.abs(z_grid) > 0.1)
    z_test = z_grid[mask]
    verify_theorem_31(z_test)
    
    # Demo 3: Discover formula
    print()
    targets = np.conj(z_test)
    results = discover_formula(z_test, targets, max_depth=2)
    print(f"\nTop 5 discovered formulas for conj(z):")
    for i, r in enumerate(results[:5]):
        star = "YES" if r['has_eml_star'] else "no"
        exact = " <<<< EXACT" if r['mse'] < 1e-20 else ""
        print(f"  {i+1}. MSE={r['mse']:.4e}  eml★={star}  {r['formula']}{exact}")
