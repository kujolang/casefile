# Agent Notes for CaseFile

Read `README.md` and `CONTRIBUTING.md` before changing code or examples.

Use interpreter mode for repository workflows:

```bash
kujo run --interpreter casefile.kujo -- <command>
```

Canonical copyable examples live in:

- `README.md` for quick start and product overview
- `HOWTO.md` for operational workflows
- `FLAGS.md` for the command and flag contract

Treat `tests/` as CLI contract coverage, not as the first source for user-facing examples. There are no generated examples, legacy demos, or expected-fail examples in the tracked repository today; label any future additions clearly.

Exclude generated and bulk paths during broad sweeps unless explicitly targeted:

```bash
rg --files -g '!target/**' -g '!.casefile/**' -g '!node_modules/**' -g '!vendor/**'
```
