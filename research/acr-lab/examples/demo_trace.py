"""Small trace logging demo; does NOT call a language model."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from acr.trace_store import TraceStore

with TemporaryDirectory() as work:
    with TraceStore(Path(work) / 'lab.sqlite') as store:
        store.start_run(run_id='demo-001', task_id='navigation-mobile', arm='C2',
                        replicate=1, model_id='none-demo', config_sha256='demo-config')
        store.log_event(run_id='demo-001', revision=0, kind='prompt_ref',
                        metadata={'prompt_sha256': 'demonstration-only', 'stored_raw_prompt': False})
        for rev, states in enumerate((('pass','pass'), ('pass','fail'))):
            store.log_test(run_id='demo-001', revision=rev, test_id='mobile-menu', status=states[0])
            store.log_test(run_id='demo-001', revision=rev, test_id='contrast', status=states[1])
        print(json.dumps(store.regression_metrics('demo-001'), indent=2))
