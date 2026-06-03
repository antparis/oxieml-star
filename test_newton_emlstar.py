#!/usr/bin/env python3
# Standalone Newton-fractal test for the eml-star ablation.
# Does NOT modify pysr_stacking.py. Reuses the SAME operators.
#
# THE NON-DECORATIVE TEST (Anthony's criterion):
#   - Fit the HOLOMORPHIC Newton map N(z)=(2z^3+1)/(3z^2) -> should work WITH or
#     WITHOUT eml-star (holomorphic ops suffice).
#   - Fit the ANTI-HOLOMORPHIC target conj(N(z)) -> should work WITH eml-star,
#     and FAIL (high MSE) WITHOUT eml-star.
#   => If removing eml-star breaks ONLY the anti-holomorphic fit, eml-star earns
#      its role. This is regression (generating a formula), not measurement.
#
# Run on Anthony's machine (has PySR + Julia). Generates its own data.

import numpy as np
import pandas as pd
import os

# ----- 1. Generate Newton-fractal data (pure math, natively complex) -----
def newton_cubic(z):
    return (2*z**3 + 1) / (3*z**2)        # N(z) for p(z)=z^3-1

rng = np.random.default_rng(42)
pts = []
while len(pts) < 3000:
    z = rng.uniform(-2,2) + 1j*rng.uniform(-2,2)
    if abs(z) > 0.15:            # stay well away from the pole at z=0
        pts.append(z)
z = np.array(pts[:3000], dtype=np.complex128)
w_holo = newton_cubic(z)              # holomorphic target
w_anti = np.conj(newton_cubic(z))     # anti-holomorphic target (negative control)

# Save in the column order pysr_stacking.load_dataset expects:
# col0=z_real, col1=z_imag, col2=target_real, col3=target_imag
os.makedirs("data", exist_ok=True)
pd.DataFrame({"z_real":z.real,"z_imag":z.imag,
              "target_real":w_holo.real,"target_imag":w_holo.imag}
             ).to_csv("data/newton_holo.csv", index=False)
pd.DataFrame({"z_real":z.real,"z_imag":z.imag,
              "target_real":w_anti.real,"target_imag":w_anti.imag}
             ).to_csv("data/newton_anti.csv", index=False)
print("Wrote data/newton_holo.csv and data/newton_anti.csv (3000 rows each)")

# ----- 2. Operator sets: WITH and WITHOUT eml-star -----
# (identical to pysr_stacking.build_operators, base set only, no discovered bricks)
def operators(with_emlstar):
    binary = ["+","-","*","/",
              "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"]
    unary  = ["cos","sin","exp","log"]
    sym = {"eml": lambda x,y: __import__('sympy').exp(x) - __import__('sympy').log(y)}
    if with_emlstar:
        binary.append("emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))")
        unary += ["my_conj(z) = conj(z)",
                  "my_real(z) = complex(real(z))",
                  "my_imag(z) = complex(imag(z))",
                  "my_abs2(z) = z * conj(z)"]
        import sympy
        sym.update({
            "emlstar": lambda x,y: sympy.exp(x) - sympy.log(sympy.conjugate(y)),
            "my_conj": lambda z: sympy.conjugate(z),
            "my_real": lambda z: sympy.re(z),
            "my_imag": lambda z: sympy.im(z),
            "my_abs2": lambda z: z*sympy.conjugate(z),
        })
    return binary, unary, sym

# ----- 3. Run PySR (only on Anthony's machine; guarded import) -----
def fit(csv, with_emlstar, label):
    try:
        from pysr import PySRRegressor
    except Exception as e:
        print(f"  [{label}] PySR not available here ({e}). Run on your machine.")
        return None
    df = pd.read_csv(csv)
    z = (df.iloc[:,0].values + 1j*df.iloc[:,1].values).astype(np.complex128)
    y = (df.iloc[:,2].values + 1j*df.iloc[:,3].values).astype(np.complex128)
    binary, unary, sym = operators(with_emlstar)
    model = PySRRegressor(
        niterations=200, population_size=500, precision=64,
        elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
        verbosity=0, deterministic=False, parallelism="multithreading",
        maxsize=30, maxdepth=8,
        binary_operators=binary, unary_operators=unary,
        extra_sympy_mappings=sym,
    )
    model.fit(z.reshape(-1,1), y)
    pred = model.predict(z.reshape(-1,1))
    mse = float(np.mean(np.abs(y-pred)**2))
    eq = str(model.get_best()["equation"])
    print(f"  [{label}] MSE={mse:.3e}  eq={eq[:60]}")
    return mse

if __name__ == "__main__":
    print("\n=== eml-star ABLATION on Newton fractal ===")
    print("Expectation: holo fits both ways; anti fits ONLY with eml-star.\n")
    print("HOLOMORPHIC target  N(z)=(2z^3+1)/(3z^2):")
    fit("data/newton_holo.csv", True,  "holo  WITH emlstar ")
    fit("data/newton_holo.csv", False, "holo  WITHOUT       ")
    print("\nANTI-HOLOMORPHIC target  conj(N(z)):")
    fit("data/newton_anti.csv", True,  "anti  WITH emlstar ")
    fit("data/newton_anti.csv", False, "anti  WITHOUT       ")
    print("\nVERDICT RULE:")
    print("  If 'anti WITHOUT' MSE >> 1e-3 while 'anti WITH' is tiny,")
    print("  and 'holo' is tiny BOTH ways -> eml-star is NON-DECORATIVE here.")
    print("  Then pass the WITH-emlstar equations to verify_exact.py for the real verdict.")
