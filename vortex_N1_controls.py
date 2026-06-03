import json, argparse
import kirsch_stack as ks

# Clone of vortex_stack.py, targeted at the N1 control CSVs, with N1's EXACT
# config as defaults (from vortex_N1_result.json: niter=30, pop=300,
# maxsize=25, parsimony=0.001). Same ks.run_one => same toolbox
# (MIXTE+inv+inv_bar) and same anti-overfit brakes as N1. These are clones
# of the N1 run on control data, nothing else.

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--niter", type=int, default=30)
    ap.add_argument("--pop", type=int, default=300)
    ap.add_argument("--maxsize", type=int, default=25)
    ap.add_argument("--parsimony", type=float, default=0.001)
    ap.add_argument("--only", choices=["all", "holo", "shuf"], default="all")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    datasets = [
        ("vortex_N1_holo", "vortex_N1_holo_control.csv"),
        ("vortex_N1_shuf", "vortex_N1_shuffled.csv"),
    ]
    if args.only == "holo":
        datasets = [d for d in datasets if d[0].endswith("holo")]
    elif args.only == "shuf":
        datasets = [d for d in datasets if d[0].endswith("shuf")]

    for label, csv in datasets:
        r = ks.run_one(csv, label, args.niter, args.pop, args.maxsize,
                       args.parsimony, args.out_dir, verbose=not args.quiet)
        out = f"{label}_result.json"
        with open(out, "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"  [written] {out}")

if __name__ == "__main__":
    main()
