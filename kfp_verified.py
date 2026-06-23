# KFP nu=2/3 edge, VERIFIED from the primary action (Kane-Fisher-Polchinski PRL 72, 4129 (1994)):
#   S0 ~ d_x phi1 (d_t + v1 d_x) phi1 + 3 d_x phi2 (-d_t + v2 d_x) phi2 + 2 v12 d_x phi1 d_x phi2
#   S1 ~ xi(x) e^{i(phi1 + 3 phi2)} + c.c.    (disorder coupling = electron-like vertex operator)
# phi1 = right-mover (holomorphic z = x - v1 t);  phi2 = left-mover (anti-holomorphic zbar = x + v2 t).
# Vertex correlator <e^{i(phi1+3phi2)}(1) e^{-i(...)}(0)> = exp(sum coeff * <phi phi>), <phi phi> ~ -log.
#   -> G ~ z^{-1} * zbar^{-3}  (charge z^-1 x neutral zbar^-3) : MULTIPLICATIVE = product of powers.
import sympy as sp
z1,z2,zb1,zb2 = sp.symbols('z1 z2 zbar1 zbar2')
ZH,ZA=[z1,z2],[zb1,zb2]; m1,m2=sp.symbols('m1 m2',positive=True); I=sp.I
def _isz(e):
    e=sp.simplify(e)
    if e==0: return True
    try: return bool(e.equals(0))
    except: return False
def fconj(e):
    t=sp.Symbol('__t__')
    return e.subs(I,t).subs({z1:zb1,zb1:z1,z2:zb2,zb2:z2},simultaneous=True).subs(t,-I)
def is_holo(f): return all(_isz(sp.diff(f,a)) for a in ZA)
def is_real(f): return _isz(sp.simplify(f-fconj(f)))
def is_pure_anti(f): return all(_isz(sp.diff(f,h)) for h in ZH)
def intermode_sep(f):
    L=sp.log(f); return all(_isz(sp.diff(sp.diff(L,a),b)) for a in [z1,zb1] for b in [z2,zb2])
def chiral_fact(f):
    L=sp.log(f); return all(_isz(sp.diff(sp.diff(L,h),a)) for h in ZH for a in ZA)
def module_multi(f):
    try:
        for zb,z,mm in [(zb1,z1,m1),(zb2,z2,m2)]:
            L=sp.simplify(zb*sp.diff(sp.log(f),zb))
            if z in sp.simplify(L.subs(zb,mm/z)).free_symbols: return False
        return True
    except: return False
def classify(f):
    if is_holo(f): b="HOL"
    elif is_real(f): b="REAL"
    elif is_pure_anti(f): b="ANTI"
    elif module_multi(f): b="MODULE"
    else: b="ANTI"
    s=intermode_sep(f); c=chiral_fact(f)
    if b=="HOL": r=("HOL sep (eml WALL)" if s else "ENTANGLED HOLO (eml WALL)")
    elif b in("REAL","MODULE"): r="WALL paired"
    elif b=="ANTI" and c: r="SEPARABLE half-chiral WALL"
    else: r="ENTANGLED CHIRAL ANTI (target)"
    return b,s,c,r
forms=[
 ("KFP electron e^{i(phi1+3phi2)}  G~z^-1 zbar^-3 [VERIFIED]", z1**(-1)*zb2**(-3)),
 ("KFP disorder op (same vertex)             z^-1 zbar^-3", z1**(-1)*zb2**(-3)),
 ("clean chiral charge vertex                z^-1",        z1**(-1)),
 ("note's claim (UNSUPPORTED) z^-2 ln z  holomorphic",     z1**(-2)*sp.log(z1)),
 ("CONTRAST target (NOT realized by KFP) z^-1 zbar^-3(1+log z1+log zbar2)", z1**(-1)*zb2**(-3)*(1+sp.log(z1)+sp.log(zb2))),
 ("ctrl_real |z1|^2", z1*zb1),
]
print("KFP nu=2/3 VERIFIED  (charge=z holo, neutral=zbar anti)")
print("-"*100)
for n,f in forms:
    b,s,c,r=classify(f)
    print(f"{n:60s} base={b:7s} cf={str(c):5s} -> {r}")

print()
print("--- NOTE #2 form: G = z^-2hc zbar^-2hn (A + B ln zbar)  (cross-chiral factorizable) ---")
hc,hn=sp.Rational(1,2),sp.Rational(3,2)
note2 = z1**(-2*hc)*zb2**(-2*hn)*(2 + sp.log(zb2))      # A=2,B=1, hc=1/2,hn=3/2 -> z^-1 zbar^-3(2+ln zbar2)
b,s,c,r = classify(note2)
print(f"G_KFP_note2 = z^-1 zbar^-3 (2+ln zbar2)   base={b} chiral_fact={c} -> {r}")
print(f"   cross 2nd deriv  d_z d_zbar log G = {sp.simplify(sp.diff(sp.diff(sp.log(note2),z1),zb2))}  (0 => factorizes => WALL)")
print()
print("--- the note's other 'target' ln(z zbar): already a KNOWN WALL (paired log) ---")
paired = z1**(-1)*zb2**(-1)*(2 + sp.log(z1*zb2))
b2,s2,c2,r2 = classify(paired)
print(f"ln(z zbar) paired form   base={b2} chiral_fact={c2} -> {r2}")
