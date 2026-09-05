# CaseFile

CaseFile is a local Kujo CLI that turns command results, existing logs, and manual notes into plaintext debugging bundles. It does not call models or hosted services.

```sh
kujo run --interpreter casefile.kujo -- help
kujo run --interpreter casefile.kujo -- init
kujo run --interpreter casefile.kujo -- validate
kujo run --interpreter casefile.kujo -- capture --name tests -- false
kujo run --interpreter casefile.kujo -- show latest --format json
```

Run these commands from the repository being investigated, using an absolute path to `casefile.kujo` when it lives elsewhere. Config is loaded from the current directory; output is rooted at the Git top level, or the current directory outside Git. Captured commands inherit the current directory and environment.

Start with `case.md`, `case.json`, and `handoff.md`; consult logs and Git artifacts for details. `case.json` is the completion marker and the machine-readable contract. Capture returns 0 after successfully recording a failed command; use `--mirror-exit-code` to preserve its status.

Requirements: Kujo with `write_file_atomic` and `path_is_symlink` support (verified with the installed `kujo 1.0.0`), Git, and POSIX utilities (`mkdir`, `date`, `head`, `rm`, `uname`). Python 3 is only used for tests and measurements. No package installation or network access is required by CaseFile itself. Tool version probes run installed executables from PATH, which must be trusted.

- [Flags and configuration](FLAGS.md)
- [Workflows](HOWTO.md)
- [Security boundaries](SECURITY.md)
- [Verification and architecture](CONTRIBUTING.md)
- [Hardening audit](docs/audits/repository-hardening.md)
