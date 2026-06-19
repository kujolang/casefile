# CaseFile Next Session Review

Date: 2026-06-19

## Current Readiness Assessment

CaseFile is a credible local-first v1 evidence-capture CLI. It is deterministic, Kujo-native, documented around interpreter mode, guarded by CLI contract tests, and now stronger around redaction and partial-write handling.

It is not yet universally enterprise grade. The product is ready to keep hardening as a showcase, but it still needs storage, policy, timeout, portability, and scale work before it should be positioned as a complete enterprise incident-evidence platform.

## Completed In This Review

- Hardened default redaction ordering so value-bearing patterns run before generic keyword patterns.
- Added command argv redaction for common sensitive flags and `key=value` style arguments.
- Added embedded command-snippet redaction for shell strings that contain secret-like assignments.
- Applied redaction to report notes before rendering `case.md`.
- Added `security.redaction_enabled` and `security.redaction_count` to `case.json`.
- Made required artifact writes fail capture with exit `4` instead of silently producing incomplete bundles.
- Normalized missing optional runtime detections to `null` instead of storing spawn-error text in `environment.json`.
- Replaced hand-written case-id bubble sort with Kujo's native `sort()` for faster list/show/clean scans.
- Added CLI contract coverage for redaction across command args, logs, notes, `command.txt`, `case.md`, and `case.json`.
- Clarified in docs that `casefile.kujo` remains the active entry point and `src/` contains scaffolds until module import support is stable for this runtime path.

## Root And Source Layout Findings

- No tracked root implementation file should be removed right now.
- `casefile.kujo` is still required as the documented interpreter entry point.
- Tracked `src/*.kujo` files are scaffolds, not migrated implementation copies.
- The untracked `agent/` directory is not part of the tracked release surface and was left untouched.
- The stale README link to `FINAL_REPORT.md` was replaced with this current review document.

## Next Session Worklist

### Security

- Add symlink-aware output-root validation so an in-repo symlink cannot redirect artifacts outside the repository after the lexical path check passes.
- Add redaction tests for bearer headers, AWS-style keys, private-key markers, `--api-key=value`, `--password value`, and imported log paths.
- Consider a `doctor --security` or `validate --strict` mode that warns when `redact = false` or `output_dir` is shared.
- Add optional artifact manifest checksums to detect tampering or incomplete handoff bundles.
- Document the plaintext-at-rest model more prominently in the quick start.

### Functionality

- Implement capture timeout enforcement or remove timeout language from any future-facing roadmap claims until it exists.
- Promote `--include` and `--exclude` from reserved parsing to actual file-context collection, with hard size limits and default excludes.
- Add `show <case-id> --format markdown|json` tests for corrupted or missing `case.json`/`case.md`.
- Add a `clean --format json` mode for CI automation.
- Consider an explicit `casefile.kujo -- help <command>` command-help surface.

### Performance

- Add a large-directory list/show/clean fixture test with hundreds of case directories.
- Avoid reading every `case.json` in `list` when a lightweight index or summary file is available.
- Consider writing a small `index.json` per output root during capture and updating it during clean.
- Benchmark capture overhead from environment and git detection on larger repositories.

### Presentation

- Add a concise architecture note showing why CaseFile is a good Kujo showcase: CLI parsing, subprocess capture, JSON/Markdown rendering, path safety, and tests.
- Add one polished sample `case.md` and `case.json` excerpt to the README without committing generated `.casefile/` output.
- Keep examples copyable and interpreter-first.
- Avoid calling the tool enterprise-ready until encrypted storage, stricter retention controls, and symlink-safe paths are implemented.

### Testing And Release Gates

- Keep `tests/` as CLI contract coverage.
- Add negative tests for partial-write failures if the Kujo test runtime can reliably simulate unwritable directories.
- Add tests for invalid redaction regex patterns to prove deterministic fallback.
- Add smoke commands to release notes: `help`, `validate`, `doctor`, and `test-run -v tests/casefile_cli_test_v2.kujo`.

## Suggested First Actions Next Time

1. Implement symlink-aware output-root validation.
2. Add the expanded redaction matrix tests.
3. Add command-specific help or JSON clean output, whichever better supports the next demo story.
4. Re-run the full interpreter validation suite.
