#!/usr/bin/env python3
"""Extract weight-2 and weight-4 level-3 triplet q-expansions from Qu-Ding's
reference notebook PHMF_integer.nb (their exact normalization)."""
import re
NB = "refs/PHMF_integer.nb"
data = open(NB, encoding="utf-8", errors="replace").read()
names = ["lv3wt2y3e1","lv3wt2y3e2","lv3wt2y3e3",
         "lv3wt4y3e1","lv3wt4y3e2","lv3wt4y3e3"]
def extract_def(name):
    for m in re.finditer(re.escape('"'+name+'"'), data):
        tail = data[m.end():m.end()+60]
        if '"="' in tail or '" ", "="' in tail or '"=' in tail:
            return data[m.end():m.end()+8000]
    return None
def parse_qseries(s):
    terms = {}
    for m in re.finditer(r'"(\-?\d+)",\s*"\s*",\s*SuperscriptBox\["q",\s*"(\d+)"\]', s):
        terms[int(m.group(2))] = terms.get(int(m.group(2)),0)+int(m.group(1))
    for m in re.finditer(r'"(\-?\d+)",\s*"\s*",\s*"q"\}', s):
        terms[1]=terms.get(1,0)+int(m.group(1))
    return dict(sorted(terms.items()))
for nm in names:
    w = extract_def(nm)
    print("="*60); print(nm)
    if w is None:
        print("  NOT FOUND as assignment"); continue
    head = re.sub(r'\s+',' ', w[:400])
    print("  RAW HEAD:", head)
    print("  integer-power terms:", parse_qseries(w[:6000]))
    print("  has FractionBox:", "FractionBox" in w[:2000], " has SqrtBox:", "SqrtBox" in w[:2000])
