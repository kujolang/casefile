# CaseFile Operations Runbook

This runbook provides operational workflows for common incident capture and triage operations.

Use `help` or `--help` to inspect the command surface. There is no standalone version command; `--version` is unsupported and exits `2`.

Set the Kujo binary once before running the workflows below:

```bash
export KUJO_BIN="kujo"
```

## 1. Bootstrap a New Repository

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- init
"$KUJO_BIN" run --interpreter casefile.kujo -- validate
"$KUJO_BIN" run --interpreter casefile.kujo -- doctor
```

Expected outcome:
- Valid `casefile.toml`
- Safe output root resolution
- Environment diagnostics available for triage

## 2. Capture a Failing Command (Primary Workflow)

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --name auth-regression -- false
```

For complex commands, pass argv after `--`.

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --name api-test -- npm test -- --runInBand
```

## 3. Preserve Exit Codes in CI

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --mirror-exit-code -- false
```

Use this mode when upstream automation must fail if the captured command fails.

## 4. Capture from Existing Logs

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --from-log /tmp/failed-build.log --name ci-log-capture
```

Best when command rerun is expensive or impossible in current environment.

## 5. Manual Incident Record

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --manual --name prod-note --notes "Observed elevated 500 rates after deploy window"
```

Use manual mode for operational notes, postmortem context, or external incident data.

## 6. Review and Handoff

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- list
"$KUJO_BIN" run --interpreter casefile.kujo -- show latest --format markdown
"$KUJO_BIN" run --interpreter casefile.kujo -- show latest --format json
```

Share these artifacts first:
- `case.md`
- `case.json`
- `handoff.md`

## 7. Retention and Cleanup

Preview only:

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- clean --keep 20 --dry-run
```

Execute retention:

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- clean --keep 20
```

Age-based cleanup:

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- clean --older-than 30d --dry-run
```

## 8. Troubleshooting

- If VM-first path fails, continue with `--interpreter` execution.
- Missing optional runtime tools (for example `pnpm`) are non-fatal in diagnostics.
- If output path validation fails, keep `output_dir` inside repository root.
- Prefer explicit argv mode (`--`) over `--command` for shell-heavy commands.

## 9. Governance Checklist

Before sharing an incident packet:
- Confirm redaction status is appropriate
- Check `case.json` for `security.redaction_enabled` and `security.redaction_count`
- Verify included notes are accurate and non-sensitive
- Confirm case reflects reproducible command or clear manual/log context
- Attach both markdown and JSON outputs for mixed consumer workflows
