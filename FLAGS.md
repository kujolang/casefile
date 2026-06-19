# CaseFile Flag Reference

This file is the authoritative command and flag surface for CaseFile v1.0.0.

## Invocation Pattern

Examples assume `KUJO_BIN` points to the local Kujo executable.

```bash
"$KUJO_BIN" run --interpreter casefile.kujo -- <command> [flags] [-- command argv...]
```

## Global

| Flag | Meaning |
|---|---|
| `-h`, `--help`, `help` | Show command usage |

There is no standalone version command. `--version` is unsupported and exits `2`.

## capture

### Syntax

```bash
... casefile.kujo -- capture [capture flags] [-- command argv...]
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--name <name>` | string | auto timestamped | Case name suffix |
| `--output-dir <path>` | string | from config | Override output root |
| `--format <human|markdown|json>` | enum | `human` | Output mode |
| `--from-log <path>` | string | none | Build case from existing log file |
| `--manual` | bool | `false` | Manual mode (no command execution) |
| `--notes <text>` | string | empty | Notes included in report |
| `--include <glob>` | repeatable string | none | Parsed for future file-context filtering |
| `--exclude <glob>` | repeatable string | none | Parsed for future file-context filtering |
| `--max-log-bytes <int>` | integer | config value | Log truncation threshold |
| `--mirror-exit-code` | bool | `false` | Exit with captured command status |
| `--no-redact` | bool | `false` | Disable redaction for this run |
| `--force` | bool | `false` | Reserved for future overwrite behavior |
| `--command <string>` | string | none | Simple whitespace-split command input |

### Capture Modes

- Command mode: provide command argv after `--`
- String command mode: use `--command "..."`
- Log mode: use `--from-log <path>`
- Manual mode: use `--manual`

## init

### Syntax

```bash
... casefile.kujo -- init
```

Creates `casefile.toml` if it does not already exist.

## validate

### Syntax

```bash
... casefile.kujo -- validate
```

Validates config parsing, output path safety, and core settings.

## doctor

### Syntax

```bash
... casefile.kujo -- doctor
```

Prints runtime and repository diagnostics.

## list

### Syntax

```bash
... casefile.kujo -- list
```

Lists known cases in table format.

## show

### Syntax

```bash
... casefile.kujo -- show <case-id|latest> [--format markdown|json]
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--format <markdown|json>` | enum | `markdown` | Output format for case display |

## clean

### Syntax

```bash
... casefile.kujo -- clean [clean flags]
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--older-than <Nd>` | duration-like string | none | Delete cases older than cutoff, e.g. `30d` |
| `--keep <N>` | integer | none | Keep newest N, delete older remainder |
| `--dry-run` | bool | `false` | Preview deletions without removing files |

## Exit Behavior

- Successful command processing: exit `0`
- Argument/config/usage errors: exit `2`
- Capture execution errors: non-zero
- With `capture --mirror-exit-code`: returns captured command exit code
- Unsupported leading flags such as `--version` also exit `2`

## Notes

- Prefer `-- <argv...>` for reliable command parsing.
- `--include`, `--exclude`, and `--force` are accepted today and reserved for expanded behavior.
- Redaction applies to generated logs, command metadata, report notes, and rendered handoff artifacts unless `--no-redact` is set.
- `case.json` includes `security.redaction_enabled` and `security.redaction_count` for automation checks.
