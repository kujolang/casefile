# Development

`casefile.kujo` is the implementation. Files under `src/` are historical module placeholders; no imports use them. Preserve them until module consumers and migration expectations are known. `tests/casefile_cli_test_v2.kujo` covers existing CLI contracts; `tests/test_hardening.py` covers security and failure regressions using isolated temporary workspaces and synthetic tool versions.

Run from the checkout with Kujo and Python 3 on PATH:

```sh
bash scripts/verify.sh
python3 tests/measure_capture.py
```

Verification prints a concise receipt and preserves each check’s complete output in the reported temporary evidence directory. A failed check returns its exit status and the last 40 log lines.

`KUJO_BIN` can point to another compatible runtime. The measurement command uses five deterministic 1 MiB imported-log fixtures with optional collectors disabled and reports raw samples, probe counts, output size, and median latency. Pass an alternate script path to measure an older revision with the identical fixture. Timing is diagnostic, not a flaky CI threshold. Stable regression assertions cover collection counts and bounded output.

The existing GitHub workflow verifies generated-artifact hygiene with a pinned checkout action and read-only permissions. Full runtime verification is available through `scripts/verify.sh` and the portable Eval fixture; hosted execution requires a separately verified Kujo installation. No unverified runtime download was added to CI.

Preserve help output, argv execution, exit codes, redaction defaults, JSON field names, and supported configuration. Update FLAGS.md for behavior changes and SECURITY.md for boundary changes. Use local fixtures, never real credentials. Do not read or modify generated `.casefile/` evidence as source.
