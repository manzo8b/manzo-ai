"""Real-browser smoke demo with intentionally seeded UI regressions.

Usage: python examples/run_browser_smoke.py --out experiments/experiment_a/results/browser_smoke
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

# Running the script from a source checkout does not require pip install.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from acr.browser_runner import CATALOG_VERSION, VIEWPORT, as_json, browser_version, run_browser_checks
from acr.trace_store import TraceStore


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(out: Path) -> dict:
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    fixtures = ROOT / 'examples' / 'browser_fixture'
    db = out / 'browser_traces.sqlite3'
    if db.exists():
        raise FileExistsError(f'Database already exists, choose a new --out: {db}')
    config = {
        'catalog_version': CATALOG_VERSION,
        'viewport': VIEWPORT,
        'fixtures': {f'rev{i}': digest(fixtures / f'rev{i}.html') for i in range(4)},
        'python': platform.python_version(),
        'playwright': importlib.metadata.version('playwright'),
        'chromium': browser_version(),
        'no_llm': True,
        'fixture_is_synthetic': True,
    }
    config_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode('utf8')).hexdigest()
    rows = []
    with TraceStore(db) as store:
        store.start_run(run_id='fixture-browser-smoke', task_id='mobile-web-demo', arm='C2',
                        replicate=1, model_id='NO_LLM__REAL_BROWSER', config_sha256=config_hash)
        for rev in range(4):
            document = fixtures / f'rev{rev}.html'
            results, version = run_browser_checks(document, screenshots=out / 'failures')
            if version != config['chromium']:
                raise RuntimeError('Browser version changed during smoke run')
            store.log_event(run_id='fixture-browser-smoke', revision=rev, kind='revision',
                            metadata={'html_sha256': digest(document), 'catalog': CATALOG_VERSION,
                                      'fixture': document.name, 'chromium': version})
            for item in results:
                store.log_test(run_id='fixture-browser-smoke', revision=rev,
                               test_id=item.test_id, status=item.status,
                               test_version=CATALOG_VERSION)
                if item.status == 'fail':
                    store.log_event(run_id='fixture-browser-smoke', revision=rev, kind='feedback',
                                    metadata={'test_id': item.test_id, 'reason': item.detail})
            rows.append({'revision': rev, 'document': document.name,
                         'document_sha256': digest(document),
                         'tests': as_json(results),
                         'passes': sum(r.status == 'pass' for r in results),
                         'fails': sum(r.status == 'fail' for r in results)})
        metrics = store.regression_metrics('fixture-browser-smoke')
    summary = {
        'title': 'ACR Lab local browser instrumentation smoke test',
        'disclaimer': 'Synthetic fixed UI changes, real Chromium/Playwright tests, no LLM. NOT ACR efficacy.',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'configuration': config,
        'configuration_sha256': config_hash,
        'revisions': rows, 'metrics': metrics,
        'environment_note': 'HTML injected with Playwright page.set_content; external services not used',
    }
    (out/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(out), 'passes_by_revision': [r['passes'] for r in rows],
                      'regressions': metrics['regressions'],
                      'eligible_transitions': metrics['eligible_transitions'],
                      'regression_rate': metrics['regression_rate']}, ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'experiments/experiment_a/results/browser_smoke')
    run(parser.parse_args().out)
