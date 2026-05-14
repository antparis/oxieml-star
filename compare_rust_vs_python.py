import numpy as np
import os
os.makedirs("data", exist_ok=True)

def generate_data(name, func, x_range, n_points=500):
    x = np.linspace(*x_range, n_points)
    y = func(x)
    with open(f"data/{name}_rust.txt", "w") as f:
        for xi, yi in zip(x, y):
            f.write(f"{xi} {yi}\n")
    with open(f"data/{name}_python.csv", "w") as f:
        f.write("z_real,z_imag,target_real,target_imag\n")
        for xi, yi in zip(x, y):
            f.write(f"{xi},0.0,{yi},0.0\n")
    print(f"Done: {name}")

generate_data("exp", lambda x: np.exp(x), (-3, 3))
generate_data("ln1px", lambda x: np.log(1 + x), (0.01, 5))
generate_data("sinc", lambda x: np.sin(x) / (x + 1e-12), (-10, 10))
print("\nData ready. Now run the tests.")
