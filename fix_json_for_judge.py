#!/usr/bin/env python3
"""
fix_json_for_judge.py
Make a detect_real_data result JSON readable by verify_exact.py.

Two fixes, both idempotent (safe to run repeatedly):
  1. Wrap flat routes under a dataset key:
       runs[route]  ->  runs[dataset_name][route]
     (the judge expects runs[dataset][route]["best_equation"])
  2. Add the "anti_holomorphic" boolean the judge reads (line ~185),
     deduced from the detector's "verdict" field:
       verdict == "anti"  ->  anti_holomorphic = True

Usage:  python3 fix_json_for_judge.py detect_eht_m87_visibility_result.json
"""
import json, os, sys

fn = sys.argv[1]
with open(fn) as f:
    d = json.load(f)

runs = d.get("runs", {})
routes = {"A_emlstar", "B_re"}

# fix 1: wrap flat routes under dataset key
if routes & set(runs.keys()):
    base = os.path.splitext(os.path.basename(d.get("dataset", "dataset")))[0]
    d["runs"] = {base: runs}
    print(f"WRAP: routes wrapped under '{base}'")
else:
    print("WRAP: already nested by dataset; nothing to do.")

# fix 2: add anti_holomorphic from verdict
added = 0
for ds, tbs in d["runs"].items():
    for route, run in tbs.items():
        if isinstance(run, dict) and "best_equation" in run \
           and "anti_holomorphic" not in run:
            run["anti_holomorphic"] = (run.get("verdict") == "anti")
            added += 1
print(f"KEY : added anti_holomorphic to {added} route(s)")

with open(fn, "w") as f:
    json.dump(d, f, indent=2)

for ds, tbs in d["runs"].items():
    for r, run in tbs.items():
        print(f"  {ds}/{r}: verdict={run.get('verdict')} "
              f"anti_holomorphic={run.get('anti_holomorphic')}")
