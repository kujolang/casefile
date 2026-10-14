# Changelog

## [Unreleased]

## [1.0.1] - 2026-10-14

### Fixed

- Redact command arguments, names, notes, Git/environment metadata and complete private-key blocks by default.
- Validate configuration before capture, reject output/show symlinks and constrain retention to completed timestamped bundles.
- Bound imported logs and optional version probes, honor collection switches, and report truncation and write/deletion failures.
- Write artifacts atomically and publish the completion manifest last; invalidate it before forced replacement.
- Preserve exclusive directory creation on Windows with inherited parent ACLs and normalize drive-qualified utility paths.

### Compatibility

- Existing commands and exit codes remain; `case.json` adds security metadata. Consumers must tolerate additional fields.
- Invalid configurations and unsafe output paths that were previously accepted are now rejected. Log limits are 0–16777216 bytes.
- Use a private output root on Windows and serialize forced rewrites with cleanup. Existing completed bundles remain readable; redaction does not rewrite old bundles.
- CaseFile still requires Git and POSIX utilities (available through Git for Windows), and does not provide a hostile-workspace sandbox.

## [1.0.0]

Initial public release. Earlier changes are preserved in Git history.
