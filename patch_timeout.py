#!/usr/bin/env python3
"""
patch_timeout.py -- Add a per-case timeout to cnative_bench.py's evaluate().
Wraps the whole evaluate body (ref_classify + simplify + certify) in a
signal.alarm timeout. A case exceeding the limit is marked SKIPPED_TIMEOUT,
EXCLUDED from the pass count, and reported separately -- never counted as OK.
This preserves honesty: a timeout is a non-judged case, not a success.

Default timeout: 8 seconds per case. Adjustable via env CNATIVE_TIMEOUT.
Run from ~/Desktop/oxieml-star/ . A dated backup must already exist.
"""
import io, sys

PATH = "cnative_bench.py"

# 1) Insert the timeout helper after the imports (anchor on 'z, zbar = ' line).
ANCHOR_IMPORT = "z, zbar = sp.symbols"
HELPER = '''import signal as _signal
import os as _os

class _TimeoutErr(Exception):
    pass

def _timeout_handler(signum, frame):
    raise _TimeoutErr()

_CASE_TIMEOUT = int(_os.environ.get("CNATIVE_TIMEOUT", "8"))

def _with_timeout(fn, seconds):
    old = _signal.signal(_signal.SIGALRM, _timeout_handler)
    _signal.alarm(seconds)
    try:
        return fn()
    finally:
        _signal.alarm(0)
        _signal.signal(_signal.SIGALRM, old)

'''

# 2) Replace the evaluate() function with a timeout-wrapped version.
OLD_EVAL = '''def evaluate(name, expr):
    try:
        truth = ref_classify(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "status": "REF_ERROR",
                "detail": str(e)}
    se = sp.simplify(expr)
    if se.is_number:
        return None
    expected = PROJECT[truth]
    try:
        judge, _ = certify_1field(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "truth": truth,
                "expected": expected, "status": "JUDGE_ERROR", "detail": str(e)}'''

NEW_EVAL = '''def _evaluate_core(name, expr):
    try:
        truth = ref_classify(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "status": "REF_ERROR",
                "detail": str(e)}
    se = sp.simplify(expr)
    if se.is_number:
        return None
    expected = PROJECT[truth]
    try:
        judge, _ = certify_1field(expr)
    except Exception as e:
        return {"name": name, "expr": str(expr), "truth": truth,
                "expected": expected, "status": "JUDGE_ERROR", "detail": str(e)}'''

# 3) Add the timeout wrapper function right before run().
OLD_RUN = "def run(n_per_class, seed, depth, do_random):"
NEW_RUN = '''def evaluate(name, expr):
    """Timeout-guarded wrapper. A case exceeding _CASE_TIMEOUT seconds is
    marked SKIPPED_TIMEOUT and never counted as a pass."""
    try:
        return _with_timeout(lambda: _evaluate_core(name, expr), _CASE_TIMEOUT)
    except _TimeoutErr:
        return {"name": name, "expr": str(expr), "status": "SKIPPED_TIMEOUT",
                "detail": f">{_CASE_TIMEOUT}s"}


def run(n_per_class, seed, depth, do_random):'''

with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

if "_CASE_TIMEOUT" in src:
    print("ALREADY PATCHED (timeout present) -- nothing to do.")
    sys.exit(0)

changes = 0

# helper insertion
idx = src.find(ANCHOR_IMPORT)
if idx == -1:
    print("ERROR: import anchor not found. Aborting."); sys.exit(1)
line_end = src.find("\n", idx) + 1
src = src[:line_end] + "\n" + HELPER + src[line_end:]
changes += 1

# evaluate -> _evaluate_core
if OLD_EVAL not in src:
    print("ERROR: evaluate() block not found as expected. Aborting (no write)."); sys.exit(1)
if src.count(OLD_EVAL) != 1:
    print(f"ERROR: evaluate() found {src.count(OLD_EVAL)} times, expected 1. Aborting."); sys.exit(1)
src = src.replace(OLD_EVAL, NEW_EVAL)
changes += 1

# add wrapper before run()
if OLD_RUN not in src:
    print("ERROR: run() definition not found. Aborting."); sys.exit(1)
if src.count(OLD_RUN) != 1:
    print(f"ERROR: run() found {src.count(OLD_RUN)} times, expected 1. Aborting."); sys.exit(1)
src = src.replace(OLD_RUN, NEW_RUN)
changes += 1

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print(f"PATCH APPLIED ({changes} edits).")
print(f"  per-case timeout: 8s (env CNATIVE_TIMEOUT to change)")
print(f"  timeout cases -> status SKIPPED_TIMEOUT, excluded from pass count.")
print(f"  NOTE: summarize() still needs to report SKIPPED_TIMEOUT separately --")
print(f"        check the final output for any timeouts and tell Claude the count.")
