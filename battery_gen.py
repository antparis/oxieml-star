import numpy as np, csv, os
os.makedirs("data/battery", exist_ok=True)
rng = np.random.default_rng(7)
N = 400
r = rng.uniform(0.4, 2.2, N); th = rng.uniform(-np.pi, np.pi, N)
z = r*np.exp(1j*th); zb = z.conj()
T = [
 ("b01_zbar", zb),("b02_zbar2", zb**2),("b03_zbar3", zb**3),("b04_zbar5", zb**5),
 ("b05_z_plus_zbar", z+zb),("b06_z3_zbar2", z**3+zb**2),
 ("b07_z_99holo", z**2+0.01*zb),("b08_z_99anti", zb**2+0.01*z),
 ("b09_logzbar", np.log(zb)),("b10_zbar_logzbar", zb*np.log(zb)),
 ("b11_log_zbar_c", np.log(zb-(0.3-0.2j))),("b12_invzbar", 1/zb),
 ("b13_zbar2_over_z", zb**2/z),("b14_sin_zbar", np.sin(zb)),
 ("b15_TRAP_absz2", z*zb),("b16_TRAP_rezbar", zb.real+0j),
 ("b17_z2_minus_zb2", z**2-zb**2),("b18_half_half", z+zb),
 ("b19_zbar4_z", zb**4+z),("b20_logz_logzbar", np.log(z)+np.log(zb)),
]
for name,vals in T:
    with open(f"data/battery/{name}.csv","w",newline="") as f:
        wr=csv.writer(f); wr.writerow(["z_real","z_imag","target_real","target_imag"])
        for zv,wv in zip(z,vals): wr.writerow([zv.real,zv.imag,wv.real,wv.imag])
print(f"{len(T)} csv written to data/battery/")
