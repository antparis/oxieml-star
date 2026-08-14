#!/usr/bin/env bash
# Machine-side runner for the #063 complex-domain recertification candidate.
# This script records a two-seal run. It never commits, pushes or promotes.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${SCRIPT_DIR}/$(basename "${BASH_SOURCE[0]}")"
JUDGE="${SCRIPT_DIR}/wc_covariant_test_v2_candidate.py"
EXPECTED_JUDGE_SHA256="8c432b074dff7b8d6ee9acf4f7275dc9140a61fd9ccab48cdd8e152a86214d0c"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="${SCRIPT_DIR}/runs/wc_covariant_v2/${RUN_ID}"

if [ ! -s "$JUDGE" ]; then
  printf '[FAIL] Missing candidate judge: %s\n' "$JUDGE" >&2
  exit 1
fi

ACTUAL_JUDGE_SHA256="$(sha256sum "$JUDGE" | awk '{print $1}')"
if [ "$ACTUAL_JUDGE_SHA256" != "$EXPECTED_JUDGE_SHA256" ]; then
  printf '[FAIL] Candidate judge hash mismatch.\n' >&2
  printf 'Expected: %s\n' "$EXPECTED_JUDGE_SHA256" >&2
  printf 'Actual:   %s\n' "$ACTUAL_JUDGE_SHA256" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '[FAIL] python3 is not available.\n' >&2
  exit 1
fi

if ! python3 -c 'import sympy' >/dev/null 2>&1; then
  printf '[FAIL] SymPy is not available in the selected python3 environment.\n' >&2
  exit 1
fi

if ! mkdir -p "$(dirname "$RUN_DIR")" || ! mkdir "$RUN_DIR"; then
  printf '[FAIL] Cannot create a fresh run directory: %s\n' "$RUN_DIR" >&2
  exit 1
fi

{
  printf 'run_id=%s\n' "$RUN_ID"
  printf 'runner=%s\n' "$RUNNER"
  printf 'judge=%s\n' "$JUDGE"
  printf 'expected_judge_sha256=%s\n' "$EXPECTED_JUDGE_SHA256"
  printf 'started_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "${RUN_DIR}/manifest_before.txt"

python3 -c 'import platform, sys, sympy; print("python=" + sys.version.replace("\n", " ")); print("platform=" + platform.platform()); print("sympy=" + sympy.__version__)' \
  > "${RUN_DIR}/environment.txt"

sha256sum "$RUNNER" "$JUDGE" > "${RUN_DIR}/input_hashes.txt"

set +e
python3 "$JUDGE" > "${RUN_DIR}/judge_output.txt" 2> "${RUN_DIR}/judge_error.txt"
RC=$?
set -e

printf '%s\n' "$RC" > "${RUN_DIR}/exit_code.txt"
printf 'finished_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  > "${RUN_DIR}/manifest_after.txt"

sha256sum \
  "$RUNNER" \
  "$JUDGE" \
  "${RUN_DIR}/manifest_before.txt" \
  "${RUN_DIR}/environment.txt" \
  "${RUN_DIR}/input_hashes.txt" \
  "${RUN_DIR}/judge_output.txt" \
  "${RUN_DIR}/judge_error.txt" \
  "${RUN_DIR}/exit_code.txt" \
  "${RUN_DIR}/manifest_after.txt" \
  > "${RUN_DIR}/final_hashes.txt"

printf 'Run directory: %s\n' "$RUN_DIR"
printf 'Judge exit code: %s\n' "$RC"
printf '[PENDING REVIEW] No claim is promoted automatically.\n'

if [ "$RC" -ne 0 ]; then
  printf '[FAIL] Recertification candidate failed.\n' >&2
  exit "$RC"
fi
