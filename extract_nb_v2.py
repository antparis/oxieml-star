#!/usr/bin/env python3
"""Extract exact normalized q-expansions of wt-2 and wt-4 level-3 triplets from
PHMF_integer.nb. Handles structure: prefactor * q^(a/b) * (1 + c1 q + c2 q^2 + ...).
Outputs Python-ready coefficient lists. Sandbox-validated parser logic by Claude."""
import re, json
data = open("refs/PHMF_integer.nb", encoding="utf-8", errors="replace").read()
names = ["lv3wt2y3e1","lv3wt2y3e2","lv3wt2y3e3","lv3wt4y3e1","lv3wt4y3e2","lv3wt4y3e3"]

def grab(name):
    for m in re.finditer(re.escape('"'+name+'"'), data):
        tail = data[m.end():m.end()+60]
        if '"="' in tail:
            return data[m.end():m.end()+20000]
    return None

def flatten(s):
    # strip Mathematica box wrappers to a flat infix-ish string
    s = s.split('"=",',1)[1] if '"=",' in s else s
    # cut at end of this definition: first occurrence of "}], "Text" or ExpressionUUID after balanced
    s = s[:s.find('ExpressionUUID')] if 'ExpressionUUID' in s else s
    s = s.replace('RowBox[{','(').replace('}]',')')
    s = s.replace('SuperscriptBox[','POW(').replace('FractionBox[','FRAC(').replace('SqrtBox[','SQRT(')
    s = re.sub(r'"\s*"','',s)
    s = s.replace('"','').replace(' ','')
    return s

for nm in names:
    w = grab(nm)
    print("="*50); print(nm)
    if not w: print(" not found"); continue
    f = flatten(w)
    print(" FLAT:", f[:300])
