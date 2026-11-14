"""Reproducible C2/C3 offline replay over identical fixed HTML revisions.

No editor, no LLM; equality of outputs is deliberate and NOT evidence of ACR
benefit. Traces and prompt compilation are the subject of this integration test.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import importlib.metadata
import platform
from acr.browser_runner import CATALOG_VERSION, VIEWPORT, run_browser_checks, browser_version
from acr.prompt_compiler import RevisionRequest, build_revision_prompt
from acr.trace_store import TraceStore
from acr.engine import create, retrieve, transition


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_from_browser_fix(*, memory_id: str, project: str, revision: int,
                               run_id: str, test_id: str, date: str, now: datetime) -> dict:
    record={'id':memory_id,'type':'M2_episodic',
            'claim':f'Test {test_id} passed at revision {revision} after failing in the preceding revision.',
            'scope': {'project':project,'applies_when':['web_review'],'excludes':[]},
            'source':{'kind':'trace','ref':f'{run_id}/rev_{revision}','proposed_by':'controller','revision':revision},
            'status':'candidate','evidence':[{'test_id':test_id,'result':'pass',
                'run':f'{run_id}_rev_{revision}','context_id':f'{project}_rev_{revision}','date':date}],
            'created_at':now.isoformat(),'expires_at':None,'review_after':None,
            'supersedes':None,'superseded_by':None,'conflict_key':None,'history':[]}
    return create(record,actor='controller',reason='Recorded a browser-verified fix',now=now)


def run_replay(*, cases: dict[str,Path], out: Path) -> dict:
    out=Path(out).resolve()
    if out.exists():
        raise FileExistsError(f'Choose a new output directory: {out}')
    out.mkdir(parents=True)
    case_paths={k:[v/f'rev{i}.html' for i in range(4)] for k,v in cases.items()}
    for files in case_paths.values():
        if any(not p.exists() for p in files):
            raise FileNotFoundError('A case must have rev0..rev3.html')
    config={'test_catalog':CATALOG_VERSION,'viewport':VIEWPORT,'chromium':browser_version(),
            'playwright':importlib.metadata.version('playwright'),
            'python':platform.python_version(),'model':'NONE_OFFLINE_REPLAY',
            'cases':{k:[digest(p) for p in v] for k,v in case_paths.items()},
            'max_revisions':3,'arms':['C2','C3'],
            'budget_note':'Counts are UTF-8 bytes, NOT LLM tokens; no efficacy claims.',
            'browser_observations_shared_per_immutable_snapshot':True}
    config_hash=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    with (out/'config.json').open('w',encoding='utf8') as f: json.dump(config,f,indent=2,ensure_ascii=False)
    # A replay observes immutable snapshots. Compute each browser snapshot once and
    # reuse its frozen observations in both arms; actual live experiments must not cache edits.
    browser_cache={}
    for task, files in case_paths.items():
        for revision, path in enumerate(files):
            observations, version=run_browser_checks(path)
            if version != config['chromium']:
                raise RuntimeError('Browser version changed during snapshot testing')
            browser_cache[(task,revision)]=([{'test_id':x.test_id,'status':x.status,'detail':x.detail} for x in observations],version)
    runs=[]
    with TraceStore(out/'traces.sqlite3') as store:
        for case,files in case_paths.items():
            for arm in ('C2','C3'):
                run_id=f'replay_{case}_{arm}'
                store.start_run(run_id=run_id,task_id=case,arm=arm,replicate=1,
                                model_id='NONE_OFFLINE_REPLAY',config_sha256=config_hash)
                memories=[]; previous=None; prompt_hashes=[]; selections=[]; result_rows=[]
                # Per-run memory state is freshly reset: no cross-arm contamination.
                for revision,path in enumerate(files):
                    now=datetime.now(timezone.utc)
                    active=None
                    if arm=='C3':
                        active=retrieve(memories,project=case,situation=['web_review'],
                            now=now,current_revision=revision,order_two=True,
                            max_tokens=4000,
                            token_count=lambda s:len(s.encode('utf-8')))
                    # C2 has the same last-checklist feedback, no memory.
                    prompt=build_revision_prompt(RevisionRequest(
                        task_id=case,objective=f'Improve the {case} interface while preserving passed checks',
                        revision=revision,current_html_sha256=digest(path),
                        feedback=tuple((i['test_id'],i['status']) for i in (previous or []))),
                        arm=arm,memory_json=active['payload_json'] if active else None,
                        token_count=lambda s:len(s.encode('utf-8')),
                        cap=16000)
                    prompt_hashes.append(prompt['sha256'])
                    selection=active['selected_ids'] if active else []
                    selections.append(selection)
                    store.log_event(run_id=run_id,revision=revision,kind='prompt_ref',
                        metadata={'sha256':prompt['sha256'],'size_utf8_bytes':prompt['count'],
                                  'actual_llm_tokens':None,'no_model_invocation':True})
                    store.log_event(run_id=run_id,revision=revision,kind='retrieval',
                        metadata={'selected_ids':selection,'excluded':active['excluded'] if active else [],
                                  'memory_budget_unit':'utf8_bytes_not_tokens'})
                    raw,version=browser_cache[(case,revision)]
                    for item in raw:
                        store.log_test(run_id=run_id,revision=revision,test_id=item['test_id'],
                            status=item['status'],test_version=CATALOG_VERSION)
                    store.log_event(run_id=run_id,revision=revision,kind='revision',
                        metadata={'snapshot_sha256':digest(path),'snapshot':str(path.name),
                                  'browser_version':version,'snapshot_results_reused_between_arms':True})
                    # Candidate memories are strictly test-observation claims from this arm.
                    if arm=='C3' and previous is not None:
                        prior={i['test_id']:i['status'] for i in previous}
                        for i in raw:
                            if prior.get(i['test_id'])=='fail' and i['status']=='pass':
                                mid=f'mem_{len(memories)+1001:04d}'
                                r=candidate_from_browser_fix(memory_id=mid,project=case,
                                    revision=revision,run_id=run_id,test_id=i['test_id'],
                                    date=now.date().isoformat(),now=now)
                                registry={(f'{run_id}_rev_{revision}',i['test_id']):{
                                    'result':'pass','project':case,
                                    'context_id':f'{case}_rev_{revision}',
                                    'deterministic':True,'kind':'regression','date':now.date().isoformat()}}
                                r=transition(r,'verified',actor='controller',
                                    reason='Matched independently obtained browser PASS',
                                    registry=registry,now=now)
                                memories.append(r)
                                store.log_event(run_id=run_id,revision=revision,
                                    kind='memory_decision',metadata={'id':mid,
                                        'status':'verified','test_id':i['test_id'],
                                        'run_scope':run_id})
                    previous=raw
                    result_rows.append({'revision':revision,'sha256':digest(path),'checks':raw})
                metrics=store.regression_metrics(run_id)
                runs.append({'run_id':run_id,'task':case,'arm':arm,'metrics':metrics,
                             'memory_selections':selections,'prompt_hashes':prompt_hashes,
                             'snapshots':result_rows})
    comparison=[]
    for case in cases:
        c2=next(x for x in runs if x['task']==case and x['arm']=='C2')
        c3=next(x for x in runs if x['task']==case and x['arm']=='C3')
        comparison.append({'task':case,'c2_regressions':c2['metrics']['regressions'],
                           'c3_regressions':c3['metrics']['regressions'],
                           'same_snapshots':all(a['sha256']==b['sha256'] for a,b in zip(c2['snapshots'],c3['snapshots'])),
                           'c3_memory_selected':any(c3['memory_selections']),
                           'this_is_not_an_efficacy_comparison':True})
    report={'status':'offline_replay_only_NOT_EXPERIMENT_A',
            'warning':'C2 and C3 replay identical predetermined snapshots; no AI-generated edits, no measured treatment effect.',
            'config_sha256':config_hash,'comparisons':comparison,'runs':runs,
            'cost_usd':0.0,'llm_requests':0,'token_counts_available':False}
    (out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    return report
