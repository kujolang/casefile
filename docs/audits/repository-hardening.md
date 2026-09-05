# CaseFile repository hardening — 2026-09-04

## Repository

- Repository: `kujolang/casefile`; branch: `main`.
- Starting SHA: `6e8a6ded379a9882b2e48b0a8f0bad57e284c3bf` (clean checkout).
- Ending implementation/documentation SHA: `4df01ffeabd31714f4337d6ff7d2e602a2a9b105`; this audit is a subsequent receipt-only commit. Resolve its final SHA with `git log -1 --format=%H -- docs/audits/repository-hardening.md`.
- Implementation commit: `29dd590`.
- Purpose: local command/log/manual evidence bundles for humans and agents. No model, MCP, HTTP service, database, or hosted integration exists here.
- Dependencies: Kujo interpreter, Git, POSIX utilities, optional installed version probes. Python standard library is test-only. No package manifest, vendored code, dependency tree, release pipeline, or compiled distribution is present. VERSION and CLI version remain 1.0.0.
- Inspected all tracked implementation, tests, spec, placeholder modules, ignore configuration, and GitHub workflow/script. Existing ignored evidence was not modified. README/FLAGS/HOWTO/SECURITY/CONTRIBUTING/AGENTS were absent despite references in the spec and workflow skill; accurate local docs were added.

## Baseline

Installed runtime reports `kujo 1.0.0`. Original CLI suite: **11/11 pass**, 42,375 ms. Help passes with its exact byte contract; the artifact guard passes. Baseline source retained through `git show START:casefile.kujo` for retrospective static checks and identical benchmark fixtures: check passes, lint exits 0 with 81 warnings, formatter check reports `needs formatting` (nonzero). These static checks were performed against the immutable starting source after implementation began.

The first 15 new behavioral tests were run against the original implementation: **13 failed, 2 passed**, 6.613 seconds. Failures reproduced traversal reads, symlink output escape, unrelated-directory deletion, collection flags ignored, unbounded log import, zero-budget command nonexecution, permissive invalid config, PEM body exposure, unredacted Git metadata, and incorrect diagnostic/retention failure semantics. Fixtures use synthetic secrets only.

## Findings

| ID | Priority | Area | Finding | Evidence | Action | Status |
| -- | -------- | ---- | ------- | -------- | ------ | ------ |
| H01 | P0 | Filesystem | `show ..` reads outside bundle root; output follows symlinks | Traversal/symlink regressions failed before | Strict descendant and single-ID validation; reject symlink ancestors/artifacts | Fixed for stable trusted workspaces |
| H02 | P0 | Retention | Every directory was a deletion candidate; output could equal repo root | Unrelated sentinel deleted; root config accepted | Require strict descendant root and timestamped matching manifest; skip incomplete/link cases | Fixed |
| H03 | P1 | Integrity | Nonexclusive mkdir; direct artifact writes; Git write errors discarded | Source and collision/write-failure tests | Exclusive 0700 creation; atomic replacement; propagate all writes; publish manifest last; invalidate forced manifest | Fixed |
| H04 | P1 | Redaction | PEM bodies and Git/environment metadata persisted raw | Synthetic PEM/Git regressions | Full-block redaction and recursive metadata redaction; redact case names | Fixed within documented heuristic scope |
| H05 | P1 | Resources | Imported logs ignore byte budget; zero command budget causes spawn failure | 1 MiB persisted at 1 KiB limit; command returned 127 instead of 7 | Bounded `head` read; truncation reporting; zero-budget execution adapter | Fixed |
| H06 | P1 | Configuration | Collection switches ignored; invalid types/regex accepted | Nine version probes despite all environment switches false | Validate merged config before side effects; honor Git/environment switches | Fixed |
| H07 | P2 | Reliability | Diagnostic missing-key failure, invalid empty retention accepted, cleanup errors return 0 | Source and doctor/retention tests | Controlled failures, early retention validation, nonzero deletion failure | Fixed |
| H08 | P2 | Efficiency | Duplicate default redaction patterns; optional version probes broadly bounded only by runtime | Source and deterministic probe count | Deduplicate regex passes; 2-second/4096-byte optional probes; flags prevent collection | Fixed |
| H09 | P2 | DX | Missing docs, machine-specific Eval paths, no unified behavioral gate | Tracked inventory and Eval fixture | Portable verification with detailed log files/concise receipt; docs; 21 regressions | Fixed |
| H10 | P2 | Concurrency | Ancestor mutation can race checks; forced writers can overlap | Code-supported inference, not exploit reproduction | Explicit trusted-workspace boundary; runtime/serialization follow-up | Open outside supported concurrency contract |

## Changes implemented

All runtime changes live in `casefile.kujo`; regressions live in `tests/test_hardening.py`.

- Containment now validates physical-root descendants component by component, rejects dangling links and root equality, and validates `show` IDs/artifacts. Existing absolute in-root paths continue to pass the original suite. Cleanup only considers completed matching manifests, so unrelated/incomplete directories no longer affect retention counts.
- Case creation uses exclusive `mkdir` with private permissions. Individual files use the verified runtime `write_file_atomic` API. Git artifact failures propagate. Forced replacement refreshes empty mode-specific logs/Git artifacts and invalidates the old manifest; the new manifest is written last. Collision, forced symlink replacement, and write-failure tests prove relevant behavior. This is not whole-directory transactional publication.
- Redaction now covers PEM bodies, recursive metadata, and names before persistence. Defaults remain mandatory and custom patterns are validated with the runtime regex engine; identical patterns are deduplicated. Existing command/log/notes tests and explicit opt-out tests pass. Legacy redaction count semantics are preserved, not redefined as a secret count.
- Imported logs read at most the requested source bytes. A zero command limit still executes and retains only enough output internally to determine truncation. Numeric config/flags respect the verified runtime 16 MiB process-output maximum. ASCII size and command status tests cover both boundaries; UTF-8/redaction expansion is documented.
- Git status/diff/untracked/history switches and environment switches govern collection. Schema keys remain present with null/unknown/empty values when disabled. Optional version probes have separate short, bounded process options.
- Diagnostics, invalid regex/types, retention inputs, artifact read errors, and deletion errors now have controlled nonzero exits. `write_file_atomic` prevents symlink/hardlink destination overwrite by replacement, but does not secure mutable ancestors.
- `scripts/verify.sh` preserves full per-check logs and returns a concise receipt, with a bounded failure excerpt. `tests/measure_capture.py` preserves raw representative samples. Eval commands are relative to the checkout. No runtime package or network dependency was added; `head` is an additional POSIX utility used for bounded import.

## Performance and efficiency

Identical five-sample fixtures use a 1 MiB ASCII source log, a 1 KiB requested budget, and all optional collectors disabled. Version tools are deterministic fixture executables. Raw samples: [before](evidence/capture-before.json), [after](evidence/capture-after.json).

| Dimension | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Optional version subprocesses/capture | 9 | 0 | Measured; disabled collectors actually skip work |
| Stored imported log bytes | 1,048,576 | 1,024 | Measured; required budget now enforced |
| Truncation flag | false | true | Correct loss disclosure |
| Median fixture latency | 722.60 ms | 708.65 ms | Nearly unchanged under variable host load; no general speedup claim |

No RSS, CPU, build-size, or token percentage claim is made. Core command output already references separate log artifacts. JSON/handoff schema and content necessary for diagnosis were retained. The handoff limits changed-file detail to eight entries. Notes and Git metadata still rely on runtime bounds. No caches, retry loops, background workers, provider prompts, model schemas, or network requests warranted tuning. Test timing is diagnostic; stable byte/probe/behavior assertions form the ratchet.

## Security

Reviewed argv execution, cwd/config loading, output roots, symlinks, write/publication order, cleanup selection, imported log reading, redaction surfaces, metadata, generated Markdown and command summaries, and failure exits. Captured commands use argv, not an interpolated shell; `--command` remains a simple splitter. PATH, Git config, commands, and workspace ownership remain trusted. Artifacts are plaintext and untrusted evidence; operational paths can expose sensitive location names and heuristic redaction can miss unknown formats. See SECURITY.md.

Static symlink/traversal and exclusive ordinary-creation regressions pass. Hostile ancestor mutation and concurrent forced rewrites are explicitly unsupported. No encryption, sandbox, terminal-control filtering, prompt-injection immunity, or exhaustive security certification is claimed.

## Compatibility

- Public interface: standalone CLI; no exported module API changed. Historical `src/` placeholders retained because downstream expectations are not proven absent.
- CLI commands/flags and byte-stable help unchanged. Safety bugs now return controlled nonzero codes. Zero log budget now executes as intended. Ordinary failed-command capture and mirror exit semantics remain unchanged.
- File format/schema/version unchanged. Empty log/Git artifacts can now exist for modes without those details; valid `case.json` is the completion marker. Damaged/incomplete directories are intentionally omitted from list/latest/clean. Forced recapture no longer retains stale mode-specific evidence.
- Config keys unchanged; documented Boolean/numeric/list types are enforced. Custom invalid regexes fail instead of silently doing nothing. Collection flags now affect the collected context and therefore classification evidence. Runtime output maxima are checked before spawning.
- Environment variables unchanged; command environment inheritance preserved. `KUJO_BIN` remains a verification override.
- External consumers using undocumented traversal, malformed manifests, invalid config types, symlink output roots, or ignored settings may need adjustment. Standard bundle consumers retain field names and ID format. No sibling repository was modified.

## Phase coverage and non-changes

Phases 0–1: complete tracked inventory, immutable starting revision, executable baseline. Phases 2–4: monolithic implementation/placeholders reviewed, duplicate regex work removed, collection and import bounded; no speculative module rewrite/cache. Phases 5–6: no model tools or provider context; preserve structured artifact references and concise verification output. Phases 7–9: error paths, static containment, retention, atomic publication, collision regression, and remaining concurrent mutation boundary reviewed. Phases 10–11: CLI/config/JSON compatibility, runtime/native utilities, pinned checkout action and read-only workflow permissions reviewed. Phases 12–15: behavior regressions, portable verification/Eval ratchets, docs and compact agent entrypoint added. Phase 16: placeholders retained; no evidence justified removing them. Phases 17–18: high-confidence local fixes implemented and complete relevant verification rerun.

No separate build, package install, typecheck command, browser E2E, hosted API, or release artifact exists. `kujo check` provides parse/compile validation and interpreter tests exercise runtime contracts. Hosted CI currently runs artifact hygiene only; no unverified Kujo download was introduced.

## Cross-repository follow-ups

**Kujo runtime / filesystem contract (P2, conditional):** CaseFile checks ancestors before separate filesystem calls. Descriptor-relative no-follow write/delete/publication primitives plus a verified runtime version contract are needed before claiming containment against concurrent hostile ancestor changes. Existing runtime source has some related read/publication APIs, but complete mutation compatibility was not established. Impact is restricted to expanding beyond trusted stable workspaces; current supported use does not require a sibling change. Preserve existing atomic-write behavior and error contracts when adding capability. Evidence: `safe_descendant`, `safe_write`, `clean_command_handler`, SECURITY.md.

## Remaining work

- **P0/P1:** none known within the documented trusted-local scope after this pass.
- **P2:** stronger concurrent/hostile filesystem semantics; define forced-writer locking and stale-lock recovery before changing its established behavior. Hosted full verification needs a reproducible supported Kujo provisioning contract.
- **Needs more evidence:** downstream consumers of placeholder modules; behavior on other Kujo builds advertising the same version; Linux execution (this pass ran on macOS). Version 1.0.0 alone is not a verified minimum native-API guarantee.
- **Not worth changing in this pass:** wholesale module split, removing placeholder files, rewriting byte-stable help, inventing caching, or imposing flaky timing gates. Formatter drift predates this work; bulk style churn was avoided.
- **P3:** command-specific help and machine-readable retention output remain optional future UX work, not blockers.

## Verification receipt

Commands ran from the repository unless noted:

| Exact command | Result |
| --- | --- |
| `KUJO_BIN=$(command -v kujo) kujo test-run -v tests/casefile_cli_test_v2.kujo` | Baseline 11/11; final 11/11 (39,890 ms) |
| `python3 -m unittest discover -s tests -p 'test_hardening.py'` | Initial 15: 13 failures reproduced; final expanded 21/21 (10.385 s) |
| `kujo run --interpreter casefile.kujo -- help` | Pass; original suite verifies exact bytes |
| `kujo run --interpreter casefile.kujo -- validate` | Pass; isolated init/validate exercised by original suite |
| `kujo check /tmp/casefile-baseline.kujo` / `kujo check casefile.kujo` | Both pass |
| `kujo lint /tmp/casefile-baseline.kujo` / `kujo lint casefile.kujo` | Both exit 0 with warnings; see below |
| `kujo format --check /tmp/casefile-baseline.kujo` / `kujo format --check casefile.kujo` | Both report pre-existing formatting drift, exit nonzero |
| `bash .github/scripts/check-kujo-tool-artifacts.sh` | Pass |
| `git diff --check` / `bash -n scripts/verify.sh` | Pass |
| `python3 tests/measure_capture.py /tmp/casefile-baseline.kujo` / `python3 tests/measure_capture.py` | Five samples each; linked JSON evidence |
| `bash scripts/verify.sh` | All checks pass; complete logs preserved in its reported temp directory |

Lint before: 78 `unreachable-code` and 3 `missing-error-handling-pattern` warnings. Final: 82 `unreachable-code` and 1 `missing-error-handling-pattern`. The line-oriented unreachable warnings flag dictionary entries following multiline `return {` expressions; tested execution produces those values. The remaining fallible-call warning is listing `list_dir`; general filesystem I/O can still fail outside supported stable-workspace assumptions. Warning-free lint/format is not claimed.

One intermediate run encountered host-wide process exhaustion (`Errno 35`, with over 2,000 processes observed). No retry/sleep/timeout workaround was added; rerunning after host capacity recovered passed. Full raw command logs were retained in temporary evidence, not committed as potentially sensitive generated bundles.

## Durable record

SignalBox admitted one unresolved trust-boundary finding: Capture `cap_84fe8cd4-cd9a-4f49-aa3b-9aefa9901e1e`, Signal `sig_f4f6a681-8961-4fdb-9a9e-7a12370106d0`; exact-ID and concept retrieval passed. No duplicates skipped. Completed fixes, routine verification and session recaps were rejected as capture candidates. Strata consolidation stores the session handoff/current state with this audit and commit provenance; prior June notes point to a now-absent NEXT_SESSION_REVIEW.md and must not override this verified current state.
