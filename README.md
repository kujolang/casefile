# CaseFile

[![Version](https://img.shields.io/badge/version-1.0.2-black)](https://github.com/kujolang/casefile)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![built with Kujo](https://img.shields.io/badge/built%20with-Kujo-white.svg)](https://github.com/kujolang/kujo)

CaseFile is a local Kujo CLI that turns command results, existing logs, and manual notes into plaintext debugging bundles. It does not call models or hosted services.

```sh
kujo run casefile.kujo -- help
kujo run casefile.kujo -- init
kujo run casefile.kujo -- validate
kujo run casefile.kujo -- capture --name tests -- false
kujo run casefile.kujo -- show latest --format json
```

Run these commands from the repository being investigated, using an absolute path to `casefile.kujo` when it lives elsewhere. Config is loaded from the current directory; output is rooted at the Git top level, or the current directory outside Git. Captured commands inherit the current directory and environment.

Start with `case.md`, `case.json`, and `handoff.md`; consult logs and Git artifacts for details. `case.json` is the completion marker and the machine-readable contract. Capture returns 0 after successfully recording a failed command; use `--mirror-exit-code` to preserve its status.

Requirements: Kujo 1.8.1 or newer with `write_file_atomic` and `path_is_symlink` support, Git, and POSIX utilities (`mkdir`, `date`, `head`, `rm`, `uname`). Python 3 is only used for tests and measurements. No package installation or network access is required by CaseFile itself. Tool version probes run installed executables from PATH, which must be trusted.

`kennel.toml` declares the official package metadata, CLI entry point, runtime requirement, and verification scripts. `casefile.toml` configures evidence capture in the workspace being investigated. Normal use runs on Kujo's default VM; `--interpreter` is an optional runtime override.

- [Flags and configuration](FLAGS.md)
- [Workflows](HOWTO.md)
- [Security boundaries](SECURITY.md)
- [Verification and architecture](CONTRIBUTING.md)
- [Hardening audit](docs/audits/repository-hardening.md)

Drive-qualified and extended-length paths passed to file utilities use forward slashes for Git
for Windows compatibility. Directory-creation failures include the utility error.
Exclusive creation is preserved. POSIX uses mode 0700; drive-qualified Windows
paths inherit their parent ACL and require a private parent directory.
