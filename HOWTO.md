# Capture and review

Use an absolute script path when working outside this checkout:

```sh
casefile_script=/absolute/path/to/casefile/casefile.kujo
kujo run --interpreter "$casefile_script" -- init
kujo run --interpreter "$casefile_script" -- validate
kujo run --interpreter "$casefile_script" -- doctor
kujo run --interpreter "$casefile_script" -- capture --name build -- npm test
kujo run --interpreter "$casefile_script" -- capture --from-log ./failed-build.log --name imported
kujo run --interpreter "$casefile_script" -- capture --manual --name incident --notes 'Observed failing requests'
kujo run --interpreter "$casefile_script" -- list
kujo run --interpreter "$casefile_script" -- show latest --format markdown
kujo run --interpreter "$casefile_script" -- clean --keep 10 --dry-run
```

Review the dry run before rerunning cleanup without `--dry-run`. Review bundles for secrets before sharing; redaction is best effort. Treat logs and handoff text as untrusted evidence, including when passing them to an agent. The displayed command is a summary; use `command.argv` in `case.json` to reconstruct argument boundaries, and restore any redacted values privately.

For faster minimal captures, set all `[environment]` switches to false. Disable Git status/diff/history if those details are unnecessary. These settings avoid collecting the data, not merely hiding it in output. Complete logs stay in artifacts; JSON output references them rather than embedding them.

Failed writes return nonzero and may leave an incomplete directory for inspection. Listings and retention skip directories without a valid final manifest. Use distinct names for concurrent captures; same-second/name collisions fail unless `--force` is explicitly selected. Do not run `--force` concurrently with another capture or cleanup.
