#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export KUJO_BIN="${KUJO_BIN:-$(command -v kujo)}"
export PYTHONDONTWRITEBYTECODE=1
receipt_dir="$(mktemp -d "${TMPDIR:-/tmp}/casefile-verification.XXXXXX")"
run_check() {
  local label="$1"
  shift
  if "$@" >"$receipt_dir/$label.log" 2>&1; then
    return 0
  else
    local status=$?
    printf 'FAIL: %s (exit %s). Evidence: %s\n' "$label" "$status" "$receipt_dir" >&2
    tail -40 "$receipt_dir/$label.log" >&2
    return "$status"
  fi
}
run_check help "$KUJO_BIN" run --interpreter casefile.kujo -- help
run_check check "$KUJO_BIN" check casefile.kujo
run_check lint "$KUJO_BIN" lint casefile.kujo
run_check cli "$KUJO_BIN" test-run -v tests/casefile_cli_test_v2.kujo
run_check hardening python3 -m unittest discover -s tests -p 'test_hardening.py'
run_check artifacts bash .github/scripts/check-kujo-tool-artifacts.sh
run_check whitespace git diff --check
printf 'PASS: help, check, lint, CLI, hardening, artifacts, whitespace. Evidence: %s\n' "$receipt_dir"
