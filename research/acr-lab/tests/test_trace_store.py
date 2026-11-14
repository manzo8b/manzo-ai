import sqlite3
import pytest

from acr.trace_store import TraceStore


def _run(store, run_id='demo'):
    store.start_run(run_id=run_id, task_id='mobile-nav', arm='C2',
                    replicate=1, model_id='mock-model', config_sha256='test-config-hash')


def test_run_and_events_are_append_only(tmp_path):
    with TraceStore(tmp_path / 'lab.db') as store:
        _run(store)
        store.log_event(run_id='demo', revision=0, kind='retrieval',
                        metadata={'selected_ids': [], 'excluded': []})
        with pytest.raises(sqlite3.IntegrityError):
            store.db.execute('DELETE FROM events')
        with pytest.raises(sqlite3.IntegrityError):
            store.db.execute('UPDATE runs SET arm="C3"')


def test_regressions_and_final_pass_rate(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        _run(s)
        for rev, a, b in [(0, 'pass', 'pass'), (1, 'fail', 'pass'),
                           (2, 'pass', 'pass')]:
            s.log_test(run_id='demo', revision=rev, test_id='nav', status=a)
            s.log_test(run_id='demo', revision=rev, test_id='contrast', status=b)
        m=s.regression_metrics('demo')
        assert m['eligible_transitions'] == 3  # rev0: two, rev1: contrast only
        assert m['regressions'] == 1
        assert m['regression_rate'] == pytest.approx(1/3)
        assert m['final_pass_rate'] == 1.0


def test_missing_and_skipped_followups_not_counted_as_success(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        _run(s)
        s.log_test(run_id='demo', revision=0, test_id='nav', status='pass')
        s.log_test(run_id='demo', revision=1, test_id='nav', status='skip')
        m=s.regression_metrics('demo')
        assert m['regression_rate'] is None
        assert m['missing_or_skipped_followups'] == 1


def test_identical_test_version_is_required(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        _run(s)
        s.log_test(run_id='demo', revision=0, test_id='nav', status='pass', test_version='1')
        s.log_test(run_id='demo', revision=1, test_id='nav', status='fail', test_version='2')
        m=s.regression_metrics('demo')
        assert m['eligible_transitions'] == 0
        assert m['missing_or_skipped_followups'] == 1


def test_duplicate_results_rejected(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        _run(s)
        s.log_test(run_id='demo', revision=0, test_id='nav', status='pass')
        with pytest.raises(sqlite3.IntegrityError):
            s.log_test(run_id='demo', revision=0, test_id='nav', status='fail')


def test_unknown_run_invalid_event_and_metadata(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        _run(s)
        with pytest.raises(sqlite3.IntegrityError):
            s.log_event(run_id='unknown', revision=0, kind='note', metadata={})
        with pytest.raises(ValueError):
            s.log_event(run_id='demo', revision=0, kind='not_valid', metadata={})
        with pytest.raises(ValueError):
            s.log_event(run_id='demo', revision=0, kind='note', metadata={'bad':float('nan')})


def test_report_unknown_run(tmp_path):
    with TraceStore(tmp_path/'lab.db') as s:
        with pytest.raises(ValueError):
            s.regression_metrics('unknown')
