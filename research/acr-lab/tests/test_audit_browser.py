import json
import sqlite3
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
from audit_browser_smoke import audit
from acr.trace_store import TraceStore


def make_result(tmp_path):
    p=tmp_path/'results'
    p.mkdir()
    fixtures=ROOT/'examples'/'browser_fixture'
    import hashlib
    sha=lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    config={'catalog_version':'v1','fixtures':{f'rev{rev}':sha(fixtures/f'rev{rev}.html') for rev in range(4)}}
    config_hash=hashlib.sha256(json.dumps(config,sort_keys=True).encode('utf8')).hexdigest()
    with TraceStore(p/'browser_traces.sqlite3') as s:
        s.start_run(run_id='fixture-browser-smoke',task_id='mobile-web-demo',arm='C2',replicate=1,model_id='NO_LLM__REAL_BROWSER',config_sha256=config_hash)
        for rev in range(4):
            s.log_event(run_id='fixture-browser-smoke',revision=rev,kind='revision',metadata={'html_sha256':sha(fixtures/f'rev{rev}.html')})
            for t in ['a','b','c','d','e','f']:
                fail=(rev==1 and t=='a') or (rev==2 and t=='b')
                s.log_test(run_id='fixture-browser-smoke',revision=rev,test_id=t,status='fail' if fail else 'pass',test_version='v1')
        metrics=s.regression_metrics('fixture-browser-smoke')
    data={'configuration':config, 'configuration_sha256':config_hash,
          'revisions':[{'revision':rev,'document_sha256':sha(fixtures/f'rev{rev}.html'),
                        'tests':[{'test_id':t,'status':'fail' if ((rev==1 and t=='a') or (rev==2 and t=='b')) else 'pass'} for t in ['a','b','c','d','e','f']]} for rev in range(4)],
          'metrics':metrics}
    (p/'summary.json').write_text(json.dumps(data))
    return p


def test_audit_recomputes_two_regressions(tmp_path):
    p=make_result(tmp_path)
    a=audit(p)
    assert (a['eligible_transitions'],a['regressions'])==(16,2)


def test_audit_rejects_changed_summary(tmp_path):
    p=make_result(tmp_path)
    path=p/'summary.json'
    data=json.loads(path.read_text())
    data['metrics']['regressions']=0
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError,match='disagree'):
        audit(p)
