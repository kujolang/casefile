"""Deterministic fixture measurement, run from the repository root."""
import json
import statistics
import sys
import time
from pathlib import Path
import test_hardening as harness

harness.SCRIPT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else harness.SCRIPT
results = []
for _ in range(5):
    fixture = harness.Hardening()
    fixture.setUp()
    try:
        source = fixture.ws / 'input.log'
        source.write_text('x' * 1048576)
        start = time.perf_counter()
        data = fixture.capture('--from-log', str(source), '--max-log-bytes', '1024')
        elapsed = (time.perf_counter() - start) * 1000
        probes = fixture.root / 'probes'
        results.append({'elapsed_ms': round(elapsed, 2),
                        'version_probes': len(probes.read_text().splitlines()) if probes.exists() else 0,
                        'combined_log_bytes': (Path(data['case']['path']) / 'combined.log').stat().st_size,
                        'truncated': data['logs']['truncated']})
    finally:
        fixture.doCleanups()
print(json.dumps({'samples': results, 'median_ms': statistics.median(r['elapsed_ms'] for r in results)}, indent=2))
