"""Public CLI regressions; Python is a test-only dependency."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(os.environ.get('CASEFILE_SCRIPT', Path(__file__).resolve().parents[1] / 'casefile.kujo'))
KUJO = shutil.which(os.environ.get('KUJO_BIN', 'kujo'))
QUIET = '''[environment]
include_os = false
include_runtime_versions = false
include_package_manager = false
include_ci_context = false
[git]
include_status = false
include_diff_stat = false
include_recent_commits = 0
include_untracked = false
'''

class Hardening(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='casefile-hardening-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.ws = self.root / 'workspace'
        self.ws.mkdir()
        self.env = os.environ.copy()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        # Make tool discovery deterministic and observable, without user toolchains.
        for tool in ('node', 'npm', 'pnpm', 'yarn', 'python3', 'pytest', 'php', 'composer', 'go'):
            p = self.bin / tool
            p.write_text('#!/bin/sh\nprintf "probe\\n" >> "$PROBE_LOG"\nprintf "fixture 1.0\\n"\n')
            p.chmod(0o755)
        self.env['PATH'] = str(self.bin) + os.pathsep + self.env['PATH']
        self.env['PROBE_LOG'] = str(self.root / 'probes')
        self.config()

    def config(self, extra=''):
        (self.ws / 'casefile.toml').write_text(extra + QUIET)

    def run_cli(self, *args):
        return subprocess.run([KUJO, 'run', '--interpreter', str(SCRIPT), '--', *args],
                              cwd=self.ws, env=self.env, text=True, capture_output=True, timeout=30)

    def capture(self, *args):
        result = self.run_cli('capture', '--name', 'fixture', '--format', 'json', *args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_show_rejects_traversal(self):
        (self.ws / 'case.md').write_text('OUTSIDE SENTINEL')
        r = self.run_cli('show', '..')
        self.assertEqual(r.returncode, 2)
        self.assertNotIn('OUTSIDE SENTINEL', r.stdout)

    def test_output_symlink_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.ws / '.casefile').symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_cli('capture', '--manual').returncode, 4)
        self.assertEqual(list(outside.iterdir()), [])

    def test_nested_and_dangling_symlinks_rejected(self):
        (self.ws / 'alias').symlink_to(self.root / 'absent', target_is_directory=True)
        self.config('output_dir = "alias/nested"\n')
        self.assertEqual(self.run_cli('validate').returncode, 2)

    def test_output_cannot_be_repository_root(self):
        self.config('output_dir = "."\n')
        self.assertEqual(self.run_cli('validate').returncode, 2)

    def test_clean_preserves_unrelated_directories(self):
        unrelated = self.ws / '.casefile' / 'precious'
        unrelated.mkdir(parents=True)
        sentinel = unrelated / 'keep.txt'
        sentinel.write_text('keep')
        self.assertEqual(self.run_cli('clean', '--keep', '0').returncode, 0)
        self.assertTrue(sentinel.exists())

    def test_show_rejects_symlink_artifact(self):
        case = self.ws / '.casefile' / '2026-01-01-000000-fixture'
        case.mkdir(parents=True)
        outside = self.root / 'outside.md'
        outside.write_text('OUTSIDE SENTINEL')
        (case / 'case.md').symlink_to(outside)
        r = self.run_cli('show', case.name)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn('OUTSIDE SENTINEL', r.stdout)

    def test_environment_collection_flags(self):
        data = self.capture('--manual')
        self.assertIsNone(data['environment']['node'])
        self.assertIsNone(data['environment']['ci'])
        self.assertFalse((self.root / 'probes').exists())

    def test_log_bound_and_truncation(self):
        log = self.ws / 'input.log'
        log.write_text('x' * 4096)
        data = self.capture('--from-log', str(log), '--max-log-bytes', '64')
        self.assertTrue(data['logs']['truncated'])
        self.assertEqual((Path(data['case']['path']) / 'combined.log').stat().st_size, 64)

    def test_zero_log_limit_still_executes_command(self):
        data = self.capture('--max-log-bytes', '0', '--', 'sh', '-c', 'printf hello; exit 7')
        self.assertEqual(data['command']['exit_code'], 7)
        self.assertEqual((Path(data['case']['path']) / 'stdout.log').read_text(), '')
        self.assertTrue(data['logs']['truncated'])

    def test_invalid_config_and_regex_rejected(self):
        for extra in ('redact = "false"\n', 'max_log_bytes = -1\n', '[redaction]\npatterns = ["["]\n'):
            self.config(extra)
            self.assertEqual(self.run_cli('validate').returncode, 2, extra)
            self.assertEqual(self.run_cli('capture', '--manual').returncode, 2, extra)

    def test_private_key_body_redacted(self):
        data = self.capture('--manual', '--notes', '-----BEGIN PRIVATE KEY-----\nSYNTHETICKEYBODY\n-----END PRIVATE KEY-----')
        contents = (Path(data['case']['path']) / 'case.md').read_text()
        self.assertNotIn('SYNTHETICKEYBODY', contents)

    def test_git_metadata_redacted(self):
        subprocess.run(['git', 'init', '-q', str(self.ws)], check=True)
        (self.ws / 'token=SYNTHETICSECRET').write_text('fixture')
        (self.ws / 'casefile.toml').write_text(QUIET.replace('include_status = false', 'include_status = true').replace('include_untracked = false', 'include_untracked = true'))
        data = self.capture('--manual')
        for artifact in Path(data['case']['path']).iterdir():
            self.assertNotIn('SYNTHETICSECRET', artifact.read_text(), artifact.name)

    def test_doctor_invalid_path_has_controlled_exit(self):
        self.config('output_dir = "../outside"\n')
        r = self.run_cli('doctor')
        self.assertEqual(r.returncode, 2)
        self.assertNotIn('KeyError', r.stdout + r.stderr)

    def test_invalid_retention_rejected_even_empty(self):
        self.assertEqual(self.run_cli('clean', '--older-than', 'oops').returncode, 2)

    def test_capture_and_clean_real_case(self):
        data = self.capture('--manual')
        path = Path(data['case']['path'])
        self.assertEqual(self.run_cli('clean', '--keep', '0', '--dry-run').returncode, 0)
        self.assertTrue(path.exists())
        self.assertEqual(self.run_cli('clean', '--keep', '0').returncode, 0)
        self.assertFalse(path.exists())

    def fixed_date(self):
        p = self.bin / 'date'
        p.write_text('#!/bin/sh\nprintf "2026-01-01-000000\\n"\n')
        p.chmod(0o755)

    def test_collision_is_exclusive(self):
        self.fixed_date()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.run_cli('capture', '--name', 'fixture', '--manual'), range(2)))
        self.assertEqual(sorted(r.returncode for r in results), [0, 4])

    def test_force_replaces_symlink_without_writing_target(self):
        self.fixed_date()
        data = self.capture('--manual')
        artifact = Path(data['case']['path']) / 'command.txt'
        artifact.unlink()
        outside = self.root / 'sentinel'
        outside.write_text('keep')
        artifact.symlink_to(outside)
        self.capture('--manual', '--force')
        self.assertEqual(outside.read_text(), 'keep')
        self.assertFalse(artifact.is_symlink())

    def test_git_artifact_write_failure_is_reported(self):
        self.fixed_date()
        data = self.capture('--manual')
        artifact = Path(data['case']['path']) / 'git-status.txt'
        artifact.unlink()
        artifact.mkdir()
        r = self.run_cli('capture', '--name', 'fixture', '--manual', '--force')
        self.assertEqual(r.returncode, 4)
        self.assertFalse((artifact.parent / 'case.json').exists())

    def test_case_name_redaction(self):
        r = self.run_cli('capture', '--name', 'password=SYNTHETICNAME', '--manual', '--format', 'json')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('SYNTHETICNAME', r.stdout)

    def test_unreadable_artifact_has_controlled_exit(self):
        data = self.capture('--manual')
        (Path(data['case']['path']) / 'case.md').write_bytes(b'\xff')
        self.assertEqual(self.run_cli('show', data['case']['id']).returncode, 4)

    def test_no_redact_remains_explicit_opt_out(self):
        data = self.capture('--manual', '--no-redact', '--notes', 'token=SYNTHETICRAW')
        self.assertFalse(data['security']['redaction_enabled'])
        self.assertIn('SYNTHETICRAW', (Path(data['case']['path']) / 'case.md').read_text())

if __name__ == '__main__':
    unittest.main()
