# CaseFile

CaseFile packages local workflow evidence into structured, reviewable case bundles for handoff, triage, and remediation.

It converts failed commands, imported logs, or manual incident notes into reproducible artifacts with preserved provenance and reproduction notes.

## Quick Links

- [Flags Reference](FLAGS.md)
- [Operator Runbook](HOWTO.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Operational Verification Report](FINAL_REPORT.md)

## Runtime Contract

- Language: Kujo (`.kujo`)
- Entry point: `casefile.kujo`
- Runtime: Kujo CLI
- Recommended execution mode: interpreter (`kujo run --interpreter casefile.kujo -- ...`)

Interpreter mode is the documented default path for this repository context.

Help is available through `help` or `--help`. There is no standalone version command; `--version` is unsupported and exits `2`.

## Quick Start

```bash
export KUJO_BIN="/Users/robertdevore/2026/kujo/target/debug/kujo"

# bootstrap
"$KUJO_BIN" run --interpreter casefile.kujo -- init
"$KUJO_BIN" run --interpreter casefile.kujo -- validate

# capture a failing command
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --name failing-tests -- false

# inspect captured cases
"$KUJO_BIN" run --interpreter casefile.kujo -- list
"$KUJO_BIN" run --interpreter casefile.kujo -- show latest --format markdown
```

## Commands

| Command | Purpose |
|---|---|
| `capture` | Capture command failure, log file, or manual incident case |
| `init` | Create `casefile.toml` with safe defaults |
| `validate` | Validate config shape and path safety constraints |
| `doctor` | Print runtime, repository, and environment diagnostics |
| `list` | List available case bundles |
| `show <id|latest>` | Render case details (`--format markdown|json`) |
| `clean` | Remove old cases (`--older-than`, `--keep`, `--dry-run`) |

## Flags At A Glance

Common capture flags:

- `--name <case-name>`
- `--output-dir <path>`
- `--format human|markdown|json`
- `--from-log <path>`
- `--manual`
- `--notes <text>`
- `--include <glob>`
- `--exclude <glob>`
- `--max-log-bytes <int>`
- `--mirror-exit-code`
- `--no-redact`
- `--force`
- `--command "..."`

Full command-by-command flag details are in [FLAGS.md](FLAGS.md).

## Case Bundle Layout

Default output root: `.casefile/`

Each case directory uses this shape:

- `.casefile/<YYYY-MM-DD-HHMMSS-name>/case.md`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/case.json`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/command.txt`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/stdout.log`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/stderr.log`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/combined.log`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/git-status.txt`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/git-diff-stat.txt`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/environment.json`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/reproduction.md`
- `.casefile/<YYYY-MM-DD-HHMMSS-name>/handoff.md`

Files are mode-aware and only written when applicable.

## Verified Characteristics

- Deterministic local execution (no network dependency)
- Redaction enabled by default
- Path safety checks for output writes and cleanup operations
- Structured machine-readable `case.json` output for automation
- Stable handoff artifacts for human or agent workflows

## Validation

Run the Kujo-native test suite:

```bash
export KUJO_BIN="/Users/robertdevore/2026/kujo/target/debug/kujo"
"$KUJO_BIN" test-run -v tests/casefile_cli_test_v2.kujo
```

## Known Limitations

- `--command` uses simple whitespace splitting. For complex commands, prefer `-- <argv...>`.
- Capture timeout enforcement is not implemented in v1.

## License

MIT. See [LICENSE](LICENSE).
