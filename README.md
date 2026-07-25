# CaseFile

[![Version](https://img.shields.io/badge/version-1.0.0-black)](https://github.com/kujolang/casefile)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![built with Kujo](https://img.shields.io/badge/built%20with-Kujo-white.svg)](https://github.com/kujolang/kujo)

CaseFile packages local workflow evidence into structured, reviewable case bundles for handoff, triage, and remediation.

It converts failed commands, imported logs, or manual incident notes into reproducible artifacts with preserved provenance and reproduction notes.

## Quick Links

- [Flags Reference](FLAGS.md)
- [Operator Runbook](HOWTO.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Next Session Review](NEXT_SESSION_REVIEW.md)

## Runtime Contract

- Language: Kujo (`.kujo`)
- Entry point: `casefile.kujo`
- Runtime: Kujo CLI
- Recommended execution mode: interpreter (`kujo run --interpreter casefile.kujo -- ...`)

Interpreter mode is the documented default path for this repository context.

Help is available through `help` or `--help`. There is no standalone version command; `--version` is unsupported and exits `2`.

## Production Readiness Posture

CaseFile is a strong local-first v1 CLI for deterministic evidence capture, review, and handoff. It is suitable for developer workstations and CI-style local capture flows where plaintext artifacts are acceptable inside a controlled repository workspace.

It should not be described as universally enterprise grade yet. The remaining enterprise hardening work is around encrypted artifact storage, richer retention policy controls, shell-accurate command rendering, configurable timeout enforcement, and broader compatibility proof across large case directories and operating systems. The current next-step list is tracked in [NEXT_SESSION_REVIEW.md](NEXT_SESSION_REVIEW.md).

## Repository Layout

`casefile.kujo` is the active CLI entry point and implementation file. The tracked `src/` files are module scaffolds kept for the planned source split once Kujo module import behavior is stable for this repository runtime path; they are not stale duplicates of migrated code.

## Quick Start

```bash
export KUJO_BIN="kujo"

# bootstrap
"$KUJO_BIN" run --interpreter casefile.kujo -- init
"$KUJO_BIN" run --interpreter casefile.kujo -- validate

# capture a failing command
"$KUJO_BIN" run --interpreter casefile.kujo -- capture --name failing-tests -- false

# inspect captured cases
"$KUJO_BIN" run --interpreter casefile.kujo -- list
"$KUJO_BIN" run --interpreter casefile.kujo -- show latest --format markdown
```

Expected bootstrap output includes:

```text
Created casefile.toml
Config validation passed
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

```text
.casefile/<YYYY-MM-DD-HHMMSS-name>/
  case.md
  case.json
  command.txt
  stdout.log
  stderr.log
  combined.log
  git-status.txt
  git-diff-stat.txt
  environment.json
  reproduction.md
  handoff.md
```

Files are mode-aware and only written when applicable.

## Verified Characteristics

- Deterministic local execution (no network dependency)
- Redaction enabled by default
- Command arguments, embedded command snippets, imported logs, and notes are redacted before being written to generated artifacts
- `case.json` includes a `security` block with redaction status and count metadata
- Required artifact writes fail the capture instead of silently producing incomplete bundles
- Path safety checks for output writes and cleanup operations
- Structured machine-readable `case.json` output for automation
- Stable handoff artifacts for human or agent workflows
- Native case-id sorting for list/show/clean scans

## Validation

Run the Kujo-native test suite:

```bash
export KUJO_BIN="kujo"
"$KUJO_BIN" test-run -v tests/casefile_cli_test_v2.kujo
```

## Known Limitations

- `--command` uses simple whitespace splitting. For complex commands, prefer `-- <argv...>`.
- Capture timeout enforcement is not implemented in v1.

## License

MIT. See [LICENSE](LICENSE).
