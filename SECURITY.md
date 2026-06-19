# Security Policy

## Security Posture

CaseFile is a local incident-capture CLI focused on deterministic artifact generation with default redaction and strict path controls.

## Trust Boundaries

- Input boundary: CLI args, optional log files, local command execution
- Storage boundary: repository-local output directory (default `.casefile`)
- Process boundary: local subprocess execution for captured commands and diagnostics
- Network boundary: no outbound network activity in core CaseFile workflows

## Security Controls

### 1) Redaction by Default

CaseFile redacts common secret-like patterns in generated logs, reports, command metadata, and notes.

Typical categories:
- API keys
- bearer tokens
- password-like assignments
- authorization headers
- private key markers

Redaction is applied before writing generated artifacts such as `case.md`, `case.json`, `command.txt`, `combined.log`, `reproduction.md`, and `handoff.md`. `case.json` includes a `security.redaction_enabled` boolean and `security.redaction_count` counter so automation can verify whether redaction was active and whether any patterns matched.

`--no-redact` is explicit and should only be used in trusted workflows.

### 2) Path Safety

- Output directories are validated against repository-root constraints.
- Path traversal escapes are blocked.
- Cleanup actions are restricted to the configured output root.

### 3) Controlled Deletion

- `clean` can be previewed with `--dry-run`.
- Unsafe delete targets are skipped.
- Retention policies are explicit (`--keep`, `--older-than`).

### 4) Deterministic Evidence

Case packets include command metadata, environment context, and git context to improve traceability and reduce ambiguity during incident review.

## Known Security Limitations

- Redaction is pattern-based, not a full DLP/secret-scanning engine.
- Sensitive command output may transiently exist in process memory before write.
- Artifacts are plaintext at rest; apply host-level controls as required.
- Shell snippets are redacted conservatively when they contain embedded assignment-like secret patterns; this may reduce reproduction command fidelity in exchange for safer handoff artifacts.

## Recommended Hardening

- Restrict filesystem permissions for repository and artifact directories.
- Enable disk encryption on developer and CI hosts.
- Use dedicated service accounts for automation that invokes CaseFile.
- Avoid `--no-redact` in shared or regulated environments.

## Reporting Vulnerabilities

Report privately to maintainers with:

- impact summary
- reproduction steps
- affected command path
- expected vs actual behavior
- environment details (OS, Kujo version, command used)

Please avoid public disclosure until maintainers complete triage and remediation.
