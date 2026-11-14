"""Independently audit browser smoke fixtures, SQLite trace, and JSON output.

It checks trace integrity against shipped fixtures and recomputes primary regression
counts independently of TraceStore.regression_metrics. Not tamper-proof.

Usage: python examples/audit_browser_smoke.py --dir experiments/experiment_a/results/browser_smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(result_dir: Path) -> dict:
    result_dir = Path(result_dir).resolve()
    summary = json.loads((result_dir / 'summary.json').read_text(encoding='utf-8'))
    data_path = result_dir / 'browser_traces.sqlite3'
    if not data_path.exists():
        raise FileNotFoundError(data_path)
    db = sqlite3.connect(f'file:{data_path}?mode=ro', uri=True)
    try:
        run = db.execute('SELECT run_id,arm,model_id,config_sha256 FROM runs').fetchall()
        if run != [('fixture-browser-smoke','C2','NO_LLM__REAL_BROWSER',summary.get('configuration_sha256'))]:
            raise ValueError('Unexpected demo run metadata')
        rows = db.execute('SELECT revision,test_id,test_version,status FROM test_results ORDER BY revision,test_id').fetchall()
        events = db.execute('SELECT revision,metadata_json FROM events WHERE kind=? ORDER BY revision', ('revision',)).fetchall()
    finally:
        db.close()
    catalog = summary['configuration']['catalog_version']
    actual_config_hash = hashlib.sha256(json.dumps(summary['configuration'], sort_keys=True).encode('utf8')).hexdigest()
    if summary.get('configuration_sha256') != actual_config_hash:
        raise ValueError('Configuration hash mismatch')
    revisions = summary['revisions']
    if len(events) != 4 or len(revisions) != 4 or len(rows) != 24:
        raise ValueError('Wrong snapshot/event/test count')
    for index in range(4):
        eventrev, eventjson = events[index]
        evt = json.loads(eventjson)
        fixture = ROOT / 'examples' / 'browser_fixture' / f'rev{index}.html'
        digest = sha(fixture)
        if eventrev != index or evt['html_sha256'] != digest or revisions[index]['document_sha256'] != digest:
            raise ValueError(f'Fixture SHA mismatch for revision {index}')
        fixture_hashes = summary['configuration']['fixtures']
        if fixture_hashes[f'rev{index}'] != digest:
            raise ValueError(f'Configuration SHA mismatch for revision {index}')

    by_revision = {i: {} for i in range(4)}
    for rev, test, version, status in rows:
        if rev not in by_revision or version != catalog or test in by_revision[rev] or status not in ('pass','fail'):
            raise ValueError('Unexpected revision, duplicate test, version, or status')
        by_revision[rev][test] = status
    keys = set(by_revision[0])
    if len(keys) != 6 or any(set(t) != keys for t in by_revision.values()):
        raise ValueError('Test catalog changed across revisions')
    for rev in revisions:
        recorded = {r['test_id']: r['status'] for r in rev['tests']}
        if recorded != by_revision[rev['revision']]:
            raise ValueError('Summary does not match SQLite test results')
    eligible = 0
    regressions = 0
    for before, after in zip(range(3), range(1, 4)):
        for test in keys:
            if by_revision[before][test] == 'pass':
                eligible += 1
                regressions += (by_revision[after][test] == 'fail')
    if (eligible, regressions) != (summary['metrics']['eligible_transitions'], summary['metrics']['regressions']):
        raise ValueError('Summary regression metrics disagree with independent audit')
    return {
        'audit': 'PASS',
        'test_catalog': catalog,
        'snapshot_passes': [sum(s == 'pass' for s in by_revision[rev].values()) for rev in range(4)],
        'eligible_transitions': eligible,
        'regressions': regressions,
        'rate': regressions / eligible if eligible else None,
        'limitations': 'Checks consistency and SHA against repository fixture copies; not tamper-proof or an ACR efficacy study.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, required=True)
    print(json.dumps(audit(parser.parse_args().dir), ensure_ascii=False, indent=2))
