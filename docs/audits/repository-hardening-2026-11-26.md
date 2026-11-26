# CaseFile hardening, 2026-11-26

Baseline `92e1d9b`. Reviewed command and log ingestion, default redaction, forced capture publication, repository metadata, Markdown rendering, manifest selection, retention, and package verification.

- `bbe2425` rejects non-regular log input before changing a bundle, skips the reader at zero budget, and uses a runtime UTC stamp when the local date utility produces unusable output. Three regressions failed on the baseline and passed on published Kujo 1.8.1.
- `ecf79ca` quotes commands and notes in Markdown fences wider than their content and filters terminal control characters in the rendered evidence. A fixture checks the generated case, reproduction, handoff and legacy Markdown view. The raw captured argv and log carry their original post-redaction evidence.
- `722ae8d` avoids reading each listing manifest twice and examines newest candidates first for `show latest`. Five paired samples with 160 complete manifests and one corrupt newest manifest measured median 2514.81 ms before and 952.88 ms after. The selected JSON and complete listing bytes matched exactly.

The full verification gate passed on checksum-verified published Kujo 1.8.1 and local Kujo 1.10.0. Each run included 11 CLI tests, 27 hardening tests, and the byte-stable help contract. Fixture captures and retention ran in disposable workspaces.
