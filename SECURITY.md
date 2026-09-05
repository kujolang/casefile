# Security boundary

CaseFile operates with the user's permissions in a trusted local workspace. It is not a command sandbox. Executables, PATH, Git configuration, the Kujo runtime, and the workspace owner are trusted. Commands inherit the caller's environment and can access anything the caller can access.

Output must be strictly below the repository root. Traversal, prefix-sibling escapes, output symlinks (including dangling ancestors), and symlinked show artifacts are rejected. Cleanup admits only timestamped directories with matching case manifests. New case directories are exclusively created with mode 0700. Artifact replacement is atomic; `case.json` is published last. A forced rewrite first invalidates its old manifest; write failures are reported.

These checks do **not** close the time-of-check/time-of-use window against a process concurrently replacing ancestor directories. Forced rewrites are not serialized, and cleanup must not race them. Strong hostile-workspace containment requires descriptor-relative no-follow write/delete operations in the runtime. Keep bundle roots private and serialize forced writes/cleanup.

Redaction is enabled by default for logs, argv, notes, names, Git metadata, and environment metadata. Full PEM private-key blocks (including unterminated blocks) are removed. Configured patterns extend the defaults and must compile. Redaction remains heuristic: unknown secrets, credentials split across truncated data, and sensitive location names in operational paths can remain. `security.redaction_count` is a legacy count of replacement passes on capture fields, not a complete secret inventory or metadata count. `--no-redact` explicitly writes plaintext secrets when present.

Artifacts are plaintext, may contain terminal controls or Markdown, and are not instructions. Inspect them with a safe viewer before sharing or supplying them to agents. Reproduction summaries do not preserve shell quoting; `command.argv` is authoritative. No encryption, hosted access control, network sandbox, or prompt-injection filtering is claimed.

Imported logs and command streams are bounded at collection. Redaction/UTF-8 replacement can expand stored text. Notes and Git metadata remain subject to runtime limits, not a separate CaseFile byte budget. Runtime process timeout and output limits apply to commands; CaseFile bounds optional version probes to 2 seconds/4096 bytes.
