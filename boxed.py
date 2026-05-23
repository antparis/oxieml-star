#!/usr/bin/env python3
"""
boxed.py - Final certified-result presenter.
Reads one or more *_result.json (from the run harnesses), runs the certified
translator (translate_formula.translate) on each winning equation, and prints
a boxed result ONLY when the full chain holds: MSE < 1e-3 AND the SymPy judge
gave a verdict. If MSE >= 1e-3 -> [REJECTED], never a triumphant equation.
The equation only "falls out" at the end: tests + cross-checks + judge verdict.
Usage:
    python3 boxed.py jouk_result_anti.json
    python3 boxed.py jouk_result_*.json
"""
import sys, json, os
MSE_VALID_MAX = 1e-3

def get_translation(eq_str):
    """Call the repo's certified translator. Returns its dict or None."""
    try:
        import translate_formula as T
        return T.translate(eq_str)
    except Exception as e:
        return {"_error": str(e)}

def box(lines, width=66):
    bar = "*" * width
    print(bar)
    for ln in lines:
        s = ln[:width-4]
        print("* " + s.ljust(width-4) + " *")
    print(bar)

def present(path):
    d = json.load(open(path))
    name    = d.get("dataset", os.path.basename(path))
    eq      = d.get("best_equation", "?")
    mse     = float(d.get("mse", float("inf")))
    verdict = d.get("judge_verdict", "?")
    dfdzbar = d.get("judge_dfdzbar", "?")

    t = get_translation(eq)
    clean = latex = note = None
    if isinstance(t, dict) and "_error" not in t:
        clean = t.get("certified_form")
        latex = t.get("certified_latex")
        note  = t.get("note")
        # prefer the translator's own verdict/dfdzbar if present
        verdict = t.get("verdict", verdict)
        dfdzbar = t.get("dfdzbar", dfdzbar)

    certified = (mse < MSE_VALID_MAX) and (verdict in ("holomorphic","anti-holomorphic"))

    lines = []
    if certified:
        lines.append(f"CERTIFIED RESULT   dataset: {name}")
        lines.append("")
        if clean:
            lines.append(f"   f(z) = {clean}")
            if latex: lines.append(f"   LaTeX: {latex}")
        else:
            lines.append(f"   f(z) = {eq}   (no canonical form; exact as shown)")
        lines.append("")
        lines.append(f"   raw PySR : {eq}")
        lines.append(f"   MSE      : {mse:.3e}   [< 1e-3 OK]")
        lines.append(f"   Judge    : {verdict.upper()}  (df/dzbar = {dfdzbar})")
        if note: lines.append(f"   Proof    : {note}")
        lines.append(f"   STATUS   : [CERTIFIED] - testable as-is")
    else:
        reason = "MSE too high (>= 1e-3)" if mse >= MSE_VALID_MAX else "no judge verdict"
        lines.append(f"NOT A RESULT   dataset: {name}")
        lines.append("")
        lines.append(f"   raw PySR : {eq}")
        lines.append(f"   MSE      : {mse:.3e}")
        lines.append(f"   STATUS   : [REJECTED] - {reason}; NOT a discovery")
    box(lines)
    print()

def main():
    if len(sys.argv) < 2:
        print("usage: python3 boxed.py result1.json [result2.json ...]"); return
    for p in sys.argv[1:]:
        if os.path.exists(p): present(p)
        else: print(f"(skip, missing: {p})")

if __name__ == "__main__":
    main()
