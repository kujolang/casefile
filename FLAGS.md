# CLI contract

Invoke `kujo run --interpreter /path/to/casefile.kujo -- COMMAND`.

| Command | Arguments |
| --- | --- |
| `help`, `--help`, `-h` | Stable command overview |
| `init` | Create `casefile.toml` unless it already exists |
| `validate` | Check configuration and output containment |
| `doctor` | Environment and output diagnostics; invalid configuration/path exits 2 |
| `capture` | Flags below, followed optionally by `-- executable arg...` |
| `list` | Completed, timestamped bundles in ascending ID order |
| `show` | `<case-id\|latest> [--format markdown\|json]`; IDs must be a single directory name |
| `clean` | `[--keep N] [--older-than Nd] [--dry-run]` |

Capture flags: `--name TEXT`, `--output-dir PATH`, `--format human|markdown|json`, `--from-log FILE`, `--notes TEXT`, `--include GLOB`, `--exclude GLOB`, `--max-log-bytes N`, `--mirror-exit-code`, `--no-redact`, `--force`, `--manual`, `--command TEXT`.

`--command` splits on spaces; it is not a shell parser. Prefer argv after `--` for quoting-sensitive commands. `--manual` selects manual capture; `--from-log` selects log import unless manual capture is selected. Avoid combining capture modes. With no command or log, capture defaults to manual mode. `--include`/`--exclude` and config path globs are reserved metadata settings; CaseFile does not collect arbitrary file contents.

`--force` permits replacing an existing same-second/name bundle. It invalidates the previous manifest, refreshes mode-specific logs, and atomically replaces individual artifacts. Serialize forced captures and cleanup. It is not a multi-file transaction or a concurrency lock.

`--max-log-bytes` and `max_log_bytes` accept 0–16777216. Command capture bounds each stream; `combined.log` joins stdout then stderr, not chronological interleaving. Log import bounds source bytes. UTF-8 decoding and redaction may change the stored byte length. A zero limit still executes the command and records whether output was discarded. Truncation is explicit in `logs.truncated`.

Cleanup combines `--keep` and `--older-than` with **union** semantics: either criterion selects a case. No criteria means no deletion. Invalid, incomplete, unrelated, or symlinked case directories are skipped. Failed deletions return 4. Age comparisons use timestamped local-time IDs.

Exit codes: 0 for successful processing, 2 for usage/configuration errors, 4 for capture/write/cleanup failures, or the command status with `--mirror-exit-code`. `--version` remains unsupported and exits 2.

## Configuration

`init` emits the defaults. `output_dir` defaults to `.casefile`, must be strictly inside the root, and cannot traverse symlinks beneath it. `redact` defaults to true; `max_log_bytes` to 250000. `default_format` is validated for compatibility but capture defaults to human output and show to Markdown; explicit `--format` selects output.

`[git]`: `include_status`, `include_diff_stat`, `include_untracked` (true); `include_recent_commits` (5; non-negative integer). Zero skips history collection. Disabling status also omits changed-file classification signals.

`[environment]`: `include_os`, `include_runtime_versions`, `include_package_manager`, `include_ci_context` (all true). False skips the corresponding collection and leaves schema fields at null/unknown. Version probes have a 2-second timeout and a 4096-byte output bound each. Captured commands retain the runtime's default process timeout; CaseFile has no timeout flag.

`[redaction].patterns` is an array of valid regex strings extending mandatory defaults; duplicates are removed. Patterns cannot disable default protection. `[paths].include_globs`/`exclude_globs` are string arrays reserved for compatibility. Boolean and numeric fields are type checked before capture writes anything.
