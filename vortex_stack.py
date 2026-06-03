import json, argparse
import kirsch_stack as ks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--niter", type=int, default=120)
    ap.add_argument("--pop", type=int, default=500)
    ap.add_argument("--maxsize", type=int, default=40)
    ap.add_argument("--parsimony", type=float, default=0.001)
    ap.add_argument("--only", choices=["all","vortex","holo","shuf"], default="all")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    datasets = [
        ("vortex", "vortex_gas.csv"),
        ("holo",   "vortex_holo_control.csv"),
        ("shuf",   "vortex_shuffled.csv"),
    ]
    if args.only != "all":
        datasets = [(l,c) for (l,c) in datasets if l == args.only]
    for label, csv in datasets:
        r = ks.run_one(csv, label, args.niter, args.pop, args.maxsize,
                       args.parsimony, args.out_dir, verbose=not args.quiet)
        with open(f"vortex_stack_{label}_result.json", "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"  [written] vortex_stack_{label}_result.json")

if __name__ == "__main__":
    main()
