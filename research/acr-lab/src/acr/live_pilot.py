"""Instrumented C2/C3 editing runner; not evidence of ACR superiority.

Security: run only against trusted local fixtures in a dedicated isolated host.
Generations may contain JS; browser_runner blocks outgoing requests, but this
is not a complete security boundary. No production files are touched.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Protocol

from .browser_runner import CHECKS, CATALOG_VERSION, run_browser_checks
from .engine import create, retrieve, transition
from .prompt_compiler import RevisionRequest, build_revision_prompt
from .trace_store import TraceStore

MAX_HTML_BYTES = 160_000
PROMPT_INSTRUCTION = (
    'Return exactly one JSON object with fields "html" (complete revised HTML) '
    'and "summary" (a short description). Use valid HTML, preserve existing '
    'functional behavior, fix failed checks and do not regress passed checks. '
    'Do not use external assets, URLs, or scripts. Do not include markdown fences.'
)


@dataclass(frozen=True)
class GeneratedEdit:
    html: str
    summary: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    model_id: str = 'test-double'


class EditingModel(Protocol):
    model_id: str
    def edit(self, *, system: str, prompt: str, max_output_tokens: int) -> GeneratedEdit: ...


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def checked_html(html: str) -> str:
    if not isinstance(html, str) or not html.lstrip().lower().startswith('<!doctype html'):
        raise ValueError('Model must produce a complete HTML5 document')
    if len(html.encode('utf-8')) > MAX_HTML_BYTES:
        raise ValueError('Generated HTML exceeds size limit')
    if any(token in html.lower() for token in ('<iframe', '<object', '<embed', '<base ', '<meta http-equiv="refresh"')):
        raise ValueError('Unsafe/unsupported HTML construct')
    return html


def _count(text: str) -> int:
    try:
        import tiktoken
    except ImportError as exc:
        raise RuntimeError('Install the llm extra for token-aware live comparison') from exc
    return len(tiktoken.get_encoding('o200k_base').encode(text))


def make_test_memory(*, run_id: str, project: str, revision: int, test_id: str,
                     registry: dict, memory_id: str, when: datetime) -> dict:
    """Create a verified observation ONLY from a real passing deterministic check.

    This is an episodic memory; it is NOT an automatically promoted general rule.
    """
    day = when.date().isoformat()
    evidence = {'test_id':test_id, 'result':'pass', 'run':run_id,
                'context_id':f'{run_id}/revision-{revision}', 'date':day}
    registry[(run_id,test_id)] = {'result':'pass', 'project':project,
                                 'context_id':evidence['context_id'],'date':day,
                                 'deterministic':True,'kind':'regression'}
    record = {
        'id': memory_id, 'type':'M2_episodic',
        'claim': f'At revision {revision}, deterministic browser check {test_id} passed; preserve its behavior.',
        'scope':{'project':project,'applies_when':['web-revision'],'excludes':[]},
        'source':{'kind':'test','ref':f'{run_id}/{revision}/{test_id}',
                  'proposed_by':'controller','revision':revision},
        'status':'candidate','evidence':[evidence], 'created_at':when.isoformat(),
        'expires_at':None,'review_after':None,'supersedes':None,
        'superseded_by':None,'conflict_key':None,'history':[],
    }
    record = create(record, actor='controller', reason='Deterministic test observation', now=when)
    return transition(record,'verified',actor='controller',reason='Trusted test registry pass',registry=registry,now=when)


def run_edit_trial(*, initial_html: Path, objective: str, task_id: str,
                   arm: str, model: EditingModel, out_dir: Path,
                   max_revisions: int = 2, max_prompt_tokens: int = 12000,
                   max_memory_tokens: int = 800, max_output_tokens: int = 4000,
                   count_tokens=_count, run_id: str | None = None,
                   replicate: int = 1) -> dict:
    if arm not in {'C2','C3'}:
        raise ValueError('Only preregistered C2 and C3 supported')
    if not 1 <= max_revisions <= 6:
        raise ValueError('Pilot revision cap must be 1..6')
    if not initial_html.is_file():
        raise FileNotFoundError(initial_html)
    if not objective.strip():
        raise ValueError('Objective required')
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = run_id or (task_id+'-'+arm+'-'+str(replicate))
    trace_db = out_dir/'traces.sqlite'
    registry, memories = {}, []
    html = checked_html(initial_html.read_text(encoding='utf8'))
    config = {'task_id':task_id,'arm':arm,'model':model.model_id,
              'max_revisions':max_revisions, 'max_prompt_tokens':max_prompt_tokens,
              'max_memory_tokens':max_memory_tokens,'max_output_tokens':max_output_tokens,
              'test_catalog':CATALOG_VERSION}
    snapshots=[]
    total_in=total_out=0
    with TraceStore(trace_db) as store:
        store.start_run(run_id=run_id,task_id=task_id,arm=arm,replicate=replicate,
                        model_id=model.model_id,config_sha256=hash_text(json.dumps(config,sort_keys=True)))
        for revision in range(max_revisions+1):
            path=out_dir / f'{run_id}-rev{revision}.html'
            path.write_text(html,encoding='utf8')
            check_results, version = run_browser_checks(path)
            result_map={r.test_id:r.status for r in check_results}
            for r in check_results:
                store.log_test(run_id=run_id,revision=revision,test_id=r.test_id,status=r.status,
                               test_version=CATALOG_VERSION)
            snapshots.append({'revision':revision,'passes':sum(v=='pass' for v in result_map.values()),
                              'fails':sum(v=='fail' for v in result_map.values()),'html_sha256':hash_text(html)})
            store.log_event(run_id=run_id,revision=revision,kind='revision',
                            metadata={'html_sha256':hash_text(html),'browser_version':version})
            if revision == max_revisions:
                break
            # Only strictly newly passing checks from this run are promoted to M2.
            if arm == 'C3' and revision > 0:
                previous = last_results
                now=datetime.now(timezone.utc)
                for test_id,status in result_map.items():
                    if status=='pass' and previous.get(test_id)=='fail':
                        mid=f'mem_{len(memories)+1000:04d}'
                        memories.append(make_test_memory(run_id=run_id,project=task_id,
                            revision=revision,test_id=test_id,registry=registry,
                            memory_id=mid,when=now))
            last_results=result_map.copy()
            ret={'payload_json':'{"memory_data_untrusted":[]}', 'selected_ids':[],
                 'excluded':[], 'memory_tokens':0}
            if arm=='C3':
                ret=retrieve(memories,project=task_id,situation=['web-revision'],
                             now=datetime.now(timezone.utc),current_revision=revision+1,
                             order_two=True,max_tokens=max_memory_tokens,token_count=count_tokens)
            store.log_event(run_id=run_id,revision=revision,kind='retrieval',
                            metadata={'selected_ids':ret['selected_ids'],
                                      'excluded':ret['excluded'],'memory_tokens':ret['memory_tokens']})
            request=RevisionRequest(task_id=task_id,objective=objective,revision=revision+1,
                 current_html_sha256=hash_text(html),feedback=tuple(sorted(result_map.items())))
            compiled=build_revision_prompt(request,arm=arm,
                memory_json=ret['payload_json'] if arm=='C3' else None)
            # Each arm receives the exact same instructions and input format.
            prompt=compiled['user_payload_json']+'\nCURRENT_HTML_DATA:\n'+html+'\nTASK_OUTPUT_CONTRACT:\n'+PROMPT_INSTRUCTION
            tokens=count_tokens(compiled['system_policy']+'\n'+prompt)
            if tokens > max_prompt_tokens:
                raise ValueError(f'Prompt token budget exceeded: {tokens} > {max_prompt_tokens}')
            store.log_event(run_id=run_id,revision=revision,kind='prompt_ref',
                            metadata={'prompt_sha256':hash_text(prompt),'count_tokens':tokens})
            output=model.edit(system=compiled['system_policy'],prompt=prompt,max_output_tokens=max_output_tokens)
            html=checked_html(output.html)
            total_in += output.input_tokens or 0
            total_out += output.output_tokens or 0
            store.log_event(run_id=run_id,revision=revision,kind='output_ref',
                            metadata={'html_sha256':hash_text(html),'summary':output.summary[:150]})
            store.log_event(run_id=run_id,revision=revision,kind='usage',
                            metadata={'input_tokens':output.input_tokens,'output_tokens':output.output_tokens,
                                      'model_id':output.model_id})
        metrics=store.regression_metrics(run_id)
    return {'run_id':run_id,'arm':arm,'model_id':model.model_id,'metrics':metrics,
            'snapshots':snapshots,'input_tokens':total_in if total_in else None,
            'output_tokens':total_out if total_out else None,'llm_used': model.model_id!='test-double',
            'status':'instrumented_pilot_not_confirmatory'}


class OpenAIResponsesEditor:
    """Optional live provider. Requires explicit API key, never embeds credentials."""
    def __init__(self, model_id: str):
        import os
        if not os.environ.get('OPENAI_API_KEY'):
            raise RuntimeError('OPENAI_API_KEY missing; no live provider calls attempted')
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install: pip install -e '.[llm]'") from exc
        self.model_id=model_id
        self.client=OpenAI()

    def edit(self, *, system: str, prompt: str, max_output_tokens: int) -> GeneratedEdit:
        response=self.client.responses.create(model=self.model_id,
                      instructions=system,input=prompt,
                      max_output_tokens=max_output_tokens,store=False)
        raw=response.output_text
        try:
            parsed=json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError('Model did not return a JSON edit; run stopped') from exc
        if not isinstance(parsed,dict) or set(parsed)!={'html','summary'}:
            raise RuntimeError('Provider response did not match edit contract')
        html=checked_html(parsed['html'])
        if not isinstance(parsed['summary'],str):
            raise RuntimeError('Invalid summary')
        usage=response.usage
        return GeneratedEdit(html,parsed['summary'],
                input_tokens=getattr(usage,'input_tokens',None),
                output_tokens=getattr(usage,'output_tokens',None),model_id=self.model_id)
