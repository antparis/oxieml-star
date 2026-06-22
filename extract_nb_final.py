#!/usr/bin/env python3
"""Final extractor: exact normalized q-expansions of wt-2 & wt-4 level-3 triplets
from PHMF_integer.nb (Qu-Ding normalization). Form: prefactor * q^(a/b) * sum c_n q^n.
Sandbox-validated parser by Claude. Writes refs/triplets_qexp.json."""
import re, json
data = open("refs/PHMF_integer.nb", encoding="utf-8", errors="replace").read()
names = ["lv3wt2y3e1","lv3wt2y3e2","lv3wt2y3e3","lv3wt4y3e1","lv3wt4y3e2","lv3wt4y3e3"]
def grab(name):
    for m in re.finditer(re.escape('"'+name+'"'), data):
        if '"="' in data[m.end():m.end()+60]:
            w = data[m.end():m.end()+30000]
            return w[:w.find('ExpressionUUID')] if 'ExpressionUUID' in w else w
    return None
def prefactor(s):
    m = re.search(r'RowBox\[\{"-",\s*"(\d+)"\}\]\s*,\s*"\s*",\s*SuperscriptBox\["q",\s*RowBox\[\{"(\d+)",\s*"/",\s*"(\d+)"\}\]', s)
    if m: return -int(m.group(1)), [int(m.group(2)),int(m.group(3))]
    m = re.search(r'"(\d+)",\s*"\s*",\s*SuperscriptBox\["q",\s*RowBox\[\{"(\d+)",\s*"/",\s*"(\d+)"\}\]', s)
    if m: return int(m.group(1)), [int(m.group(2)),int(m.group(3))]
    return 1,[0,1]
def coeffs(s,maxp=30):
    # fractional-prefactor series (e2,e3): inner series after "(" ; integer series (e1,e4): top-level with signs
    has_frac = re.search(r'SuperscriptBox\["q",\s*RowBox\[\{"\d+",\s*"/"',s) is not None
    t={}
    if has_frac:
        # inner: starts at the inner "(" ; coeffs are positive c*q^n and c*q and leading 1
        inner = s[s.find('"(",'):]
        for m in re.finditer(r'"(\d+)",\s*"\s*",\s*SuperscriptBox\["q",\s*"(\d+)"\]', inner):
            t[int(m.group(2))]=int(m.group(1))
        for m in re.finditer(r'"(\d+)",\s*"\s*",\s*"q"\}', inner):
            t[1]=int(m.group(1))
        t[0]=1
    else:
        # integer series with explicit +/- signs (e1 all +, e4 mostly -)
        for m in re.finditer(r'"([+\-])",\s*RowBox\[\{"(\d+)",\s*"\s*",\s*(?:SuperscriptBox\["q",\s*"(\d+)"\]|"q")', s):
            sign = 1 if m.group(1)=='+' else -1
            p = int(m.group(3)) if m.group(3) else 1
            t[p]=sign*int(m.group(2))
        t[0]=1
    return [t.get(i,0) for i in range(maxp)]
out={}
for nm in names:
    w=grab(nm); pf,fr=prefactor(w); co=coeffs(w)
    out[nm]={"prefactor":pf,"qpow":fr,"coeffs":co}
    print(f"{nm}: pref={pf} q^{fr[0]}/{fr[1]} coeffs[:8]={co[:8]}")
json.dump(out,open("refs/triplets_qexp.json","w"),indent=1)
print("OK -> refs/triplets_qexp.json")
