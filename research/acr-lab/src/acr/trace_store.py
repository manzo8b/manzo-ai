"""SQLite experimental trace ledger (metadata-only by default).

This database is append-only at the application level, NOT tamper-proof.
Do not store secrets or identifiable user content in event metadata.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARMS = frozenset({'C0', 'C1', 'C2', 'C3', 'C4', 'C5'})
EVENT_TYPES = frozenset({
    'prompt_ref', 'retrieval', 'output_ref', 'feedback', 'memory_proposal',
    'memory_decision', 'usage', 'revision', 'note',
})
TEST_STATUSES = frozenset({'pass', 'fail', 'skip'})


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(payload: dict[str, Any]) -> str:
    if not isinstance(payload, dict):
        raise ValueError('Event metadata must be a dict')
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, allow_nan=False)


class TraceStore:
    """Minimal reproducibility layer, not an evidence-authority service."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(self.path))
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA busy_timeout=3000')
        self._initialize()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.db.close()

    def _initialize(self):
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            arm TEXT NOT NULL CHECK(arm IN ('C0','C1','C2','C3','C4','C5')),
            replicate INTEGER NOT NULL CHECK(replicate >= 1),
            model_id TEXT NOT NULL,
            config_sha256 TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL REFERENCES runs(run_id),
            revision INTEGER NOT NULL CHECK(revision >= 0),
            kind TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            recorded_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS test_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL REFERENCES runs(run_id),
            revision INTEGER NOT NULL CHECK(revision >= 0),
            test_id TEXT NOT NULL,
            test_version TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pass','fail','skip')),
            recorded_at TEXT NOT NULL,
            UNIQUE(run_id,revision,test_id,test_version)
        );
        CREATE TRIGGER IF NOT EXISTS protect_event_update
        BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
        CREATE TRIGGER IF NOT EXISTS protect_event_delete
        BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
        CREATE TRIGGER IF NOT EXISTS protect_result_update
        BEFORE UPDATE ON test_results BEGIN SELECT RAISE(ABORT, 'results are append-only'); END;
        CREATE TRIGGER IF NOT EXISTS protect_result_delete
        BEFORE DELETE ON test_results BEGIN SELECT RAISE(ABORT, 'results are append-only'); END;
        CREATE TRIGGER IF NOT EXISTS protect_run_update
        BEFORE UPDATE ON runs BEGIN SELECT RAISE(ABORT, 'runs are immutable'); END;
        CREATE TRIGGER IF NOT EXISTS protect_run_delete
        BEFORE DELETE ON runs BEGIN SELECT RAISE(ABORT, 'runs are immutable'); END;
        ''')
        self.db.commit()

    def start_run(self, *, run_id: str, task_id: str, arm: str,
                  replicate: int, model_id: str, config_sha256: str) -> None:
        if arm not in ARMS:
            raise ValueError('Unknown experimental arm')
        if replicate < 1 or not all((run_id, task_id, model_id, config_sha256)):
            raise ValueError('Run metadata must be complete')
        with self.db:
            self.db.execute('''INSERT INTO runs
                (run_id,task_id,arm,replicate,model_id,config_sha256,created_at)
                VALUES (?,?,?,?,?,?,?)''',
                (run_id, task_id, arm, replicate, model_id, config_sha256, _utcnow()))

    def log_event(self, *, run_id: str, revision: int, kind: str,
                  metadata: dict[str, Any]) -> None:
        if revision < 0 or kind not in EVENT_TYPES:
            raise ValueError('Invalid revision or event type')
        payload = _json(metadata)
        with self.db:
            self.db.execute('''INSERT INTO events
                (run_id,revision,kind,metadata_json,recorded_at)
                VALUES (?,?,?,?,?)''', (run_id, revision, kind, payload, _utcnow()))

    def log_test(self, *, run_id: str, revision: int, test_id: str,
                 status: str, test_version: str = '1') -> None:
        if revision < 0 or status not in TEST_STATUSES or not test_id or not test_version:
            raise ValueError('Invalid test result')
        with self.db:
            self.db.execute('''INSERT INTO test_results
                (run_id,revision,test_id,test_version,status,recorded_at)
                VALUES (?,?,?,?,?,?)''',
                (run_id,revision,test_id,test_version,status,_utcnow()))

    def regression_metrics(self, run_id: str) -> dict:
        """Compare identical test IDs/versions at consecutive revision numbers.

        Missing or skipped follow-up is flagged, never counted as a successful test.
        Treat results as descriptive, not statistically significant on their own.
        """
        if not self.db.execute('SELECT 1 FROM runs WHERE run_id=?', (run_id,)).fetchone():
            raise ValueError('Unknown run')
        rows = self.db.execute('''SELECT revision,test_id,test_version,status
            FROM test_results WHERE run_id=? ORDER BY revision''', (run_id,)).fetchall()
        snapshots = {}
        for rev, test_id, version, status in rows:
            snapshots.setdefault(rev, {})[(test_id, version)] = status
        eligible = regressions = missing = 0
        for rev in range(max(snapshots, default=0)):
            previous = snapshots.get(rev, {})
            current = snapshots.get(rev + 1, {})
            for key, status in previous.items():
                if status != 'pass':
                    continue
                next_status = current.get(key)
                if next_status in {'pass', 'fail'}:
                    eligible += 1
                    regressions += next_status == 'fail'
                else:
                    missing += 1
        last_rev = max(snapshots, default=None)
        latest = snapshots.get(last_rev, {}) if last_rev is not None else {}
        final_count = sum(v in {'pass','fail'} for v in latest.values())
        final_pass = sum(v == 'pass' for v in latest.values())
        return {
            'run_id': run_id,
            'revisions_observed': len(snapshots),
            'eligible_transitions': eligible,
            'regressions': regressions,
            'regression_rate': regressions / eligible if eligible else None,
            'missing_or_skipped_followups': missing,
            'final_tests_evaluated': final_count,
            'final_pass_rate': final_pass / final_count if final_count else None,
        }
