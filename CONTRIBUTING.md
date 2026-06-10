# Contributing to CaseFile

CaseFile is maintained as a Kujo-native project with deterministic, local-first behavior.

## Engineering Standards

- Keep behavior deterministic and reproducible.
- Do not add network calls to core CaseFile command paths.
- Preserve redaction-by-default behavior.
- Preserve output path safety and guarded cleanup semantics.
- Prefer explicit, test-backed changes over speculative refactors.

## Local Development

Primary runtime used in this repository:

```bash
/path/to/kujo/target/debug/kujo
```

Primary script:

```text
casefile.kujo
```

## Core Validation Commands

```bash
# Usage and command surface
/path/to/kujo/target/debug/kujo run --interpreter casefile.kujo -- help

# Config lifecycle
/path/to/kujo/target/debug/kujo run --interpreter casefile.kujo -- init
/path/to/kujo/target/debug/kujo run --interpreter casefile.kujo -- validate

# Tests
/path/to/kujo/target/debug/kujo test-run -v tests/casefile_cli_test_v2.kujo
```

## Pull Request Expectations

Each PR should include:

- Problem statement and intended behavioral change
- User-visible impact summary
- Test evidence (`test-run` output)
- Documentation updates when command surface or semantics change

## Documentation Rules

When you change CLI behavior, update:

- `README.md` for product-level usage and positioning
- `FLAGS.md` for authoritative command/flag details
- `HOWTO.md` for operational runbooks
- `SECURITY.md` if behavior affects trust boundaries or risk model

## Release Readiness Checklist

- Kujo-native tests pass
- No Rust/cargo dependency assumptions introduced
- No network behavior added in core command flows
- Flags and examples match parser behavior
- Security and operational docs remain accurate

## Non-Goals (v1)

- Automatic LLM root-cause or auto-fix actions
- Remote uploads or issue tracker side effects
- SARIF output and dashboard/daemon operation
