import numpy as np, csv, os
os.makedirs("data", exist_ok=True)
rng = np.random.default_rng(7)
N = 400
r = rng.uniform(0.3, 2.5, N); th = rng.uniform(-np.pi, np.pi, N)
z = r*np.exp(1j*th)
targets = {
    "loc1_zbar2":      z.conj()**2,
    "loc2_zbar3_zbar": z.conj()**3 + z.conj(),
    "loc3_log_zbar_c": np.log(z.conj() - (0.4-0.2j)),
    "loc4_zbar_logzbar": z.conj()*np.log(z.conj()),
    "loc5_mix_zbar2_z3": z.conj()**2 + z**3,
    "loc6_exp_zbar":   np.exp(z.conj()),
}
for name, t in targets.items():
    with open(f"data/{name}.csv","w",newline="") as f:
        wr=csv.writer(f); wr.writerow(["z_real","z_imag","target_real","target_imag"])
        for zv,wv in zip(z,t): wr.writerow([zv.real,zv.imag,wv.real,wv.imag])
    print(f"{name}: {len(z)} rows, |t| in [{np.abs(t).min():.2f},{np.abs(t).max():.2f}]")
