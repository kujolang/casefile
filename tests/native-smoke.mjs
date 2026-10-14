import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const script = resolve('casefile.kujo');
const root = mkdtempSync(join(tmpdir(), 'casefile native space-'));
function run(...args) {
  const result = spawnSync(process.env.KUJO_BIN || 'kujo', ['run', '--interpreter', script, '--', ...args], { cwd: root, encoding: 'utf8', timeout: 30000 });
  assert.equal(result.status, 0, result.stderr + result.stdout);
  return result.stdout;
}
try {
  run('init');
  const config = join(root, 'casefile.toml');
  writeFileSync(config, readFileSync(config, 'utf8').replace(/include_[a-z_]+ = true/g, value => value.replace('true', 'false')).replace('include_recent_commits = 5', 'include_recent_commits = 0'));
  run('validate');
  writeFileSync(join(root, 'input log.txt'), 'failure password=synthetic-private-value\n');
  const imported = JSON.parse(run('capture', '--name', 'imported', '--from-log', join(root, 'input log.txt'), '--format', 'json'));
  assert.equal(imported.logs.truncated, false);
  const shown = run('show', 'latest', '--format', 'json');
  assert.equal(JSON.parse(shown).version, '1.0.1');
  assert.ok(!shown.includes('synthetic-private-value'));
  run('capture', '--manual', '--name', 'manual');
  run('capture', '--name', 'command', '--', process.execPath, '-e', 'process.exit(1)');
  assert.match(run('list'), /imported/);
  assert.match(run('clean', '--keep', '0', '--dry-run'), /would delete/);
  console.log('PASS: native paths, log import, manual and command capture, show, list, cleanup preview');
} finally {
  rmSync(root, { recursive: true, force: true });
}
