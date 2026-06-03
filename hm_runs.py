import json, argparse
import kirsch_stack as ks

# Clone of optical_runs.py, targeted at the Hasegawa-Mima screened vortex CSVs.
# Same ks.run_one (precision=64, MIXTE+inv+inv_bar, anti-overfit brakes).
# vortex = screened (rho_s=0.3, expect ANTI log zbar)
# holo   = unscreened limit (rho_s=1e6, expect HOLO -iG/2pi z) [encadrement control]
# shuf   = shuffled vortex (negative control)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--niter", type=int, default=30)
    ap.add_argument("--pop", type=int, default=300)
    ap.add_argument("--maxsize", type=int, default=25)
    ap.add_argument("--parsimony", type=float, default=0.001)
    ap.add_argument("--only", choices=["all", "vortex", "holo", "shuf"], default="all")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    datasets = [
        ("hm_vortex", "hm_vortex.csv"),
        ("hm_holo", "hm_holo.csv"),
        ("hm_shuf", "hm_shuf.csv"),
    ]
    if args.only != "all":
        datasets = [(l, c) for (l, c) in datasets if l.endswith(args.only)]

    for label, csv in datasets:
        r = ks.run_one(csv, label, args.niter, args.pop, args.maxsize,
                       args.parsimony, args.out_dir, verbose=not args.quiet)
        out = f"{label}_result.json"
        with open(out, "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"  [written] {out}")

if __name__ == "__main__":
    main()
