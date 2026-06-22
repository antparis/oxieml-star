#!/usr/bin/env python3
"""v3: bound each definition to the NEXT lv3wt name so windows don't bleed.
Exact normalized q-expansions of wt-2/wt-4 level-3 triplets from PHMF_integer.nb."""
import re, json
data = open("refs/PHMF_integer.nb", encoding="utf-8", errors="replace").read()
names = ["lv3wt2y3e1","lv3wt2y3e2","lv3wt2y3e3","lv3wt4y3e1","lv3wt4y3e2","lv3wt4y3e3"]
def grab(name):
    # find the ASSIGNMENT occurrence: "name", " ", "=", RowBox  (definition cell, not the Text label)
    for m in re.finditer(re.escape('"'+name+'"')+r'\s*,\s*"\s*"\s*,\s*"="', data):
        start = m.start()
        # bound: next lv3wt assignment, or +25000
        nxt = re.search(r'"lv3wt\w+"\s*,\s*"\s*"\s*,\s*"="', data[m.end():])
        end = m.end()+nxt.start() if nxt else m.end()+25000
        return data[start:end]
    return None
def prefactor(s):
    m = re.search(r'RowBox\[\{"-",\s*"(\d+)"\}\]\s*,\s*"\s*",\s*SuperscriptBox\["q",\s*RowBox\[\{"(\d+)",\s*"/",\s*"(\d+)"\}\]', s)
    if m: return -int(m.group(1)), [int(m.group(2)),int(m.group(3))]
    m = re.search(r'"(\d+)",\s*"\s*",\s*SuperscriptBox\["q",\s*RowBox\[\{"(\d+)",\s*"/",\s*"(\d+)"\}\]', s)
    if m: return int(m.group(1)), [int(m.group(2)),int(m.group(3))]
    return 1,[0,1]
def coeffs(s,maxp=22):
    has_frac = re.search(r'SuperscriptBox\["q",\s*RowBox\[\{"\d+",\s*"/"',s) is not None
    t={}
    if has_frac:
        inner = s[s.find('"(",'):]
        for m in re.finditer(r'"(\d+)",\s*"\s*",\s*SuperscriptBox\["q",\s*"(\d+)"\]', inner):
            t[int(m.group(2))]=int(m.group(1))
        for m in re.finditer(r'"(\d+)",\s*"\s*",\s*"q"\}', inner): t[1]=int(m.group(1))
        t[0]=1
    else:
        for m in re.finditer(r'"([+\-])",\s*RowBox\[\{"(\d+)",\s*"\s*",\s*(?:SuperscriptBox\["q",\s*"(\d+)"\]|"q")', s):
            sign=1 if m.group(1)=='+' else -1; p=int(m.group(3)) if m.group(3) else 1; t[p]=sign*int(m.group(2))
        t[0]=1
    return [t.get(i,0) for i in range(maxp)]
out={}
for nm in names:
    w=grab(nm)
    if not w: print(nm,"NOT FOUND"); continue
    pf,fr=prefactor(w); co=coeffs(w)
    out[nm]={"prefactor":pf,"qpow":fr,"coeffs":co}
    print(f"{nm}: pref={pf} q^{fr[0]}/{fr[1]} coeffs={co[:10]}")
json.dump(out,open("refs/triplets_qexp.json","w"),indent=1)
print("OK -> refs/triplets_qexp.json")
