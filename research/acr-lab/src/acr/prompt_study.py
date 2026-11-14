"""Experiment C template preparation: lexical control only, no golden-ratio efficacy claim."""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    task_id: str
    dynamic_text: str
    invariants: tuple[str,...]

SCAFFOLDS = {
  'S0': '',
  'S1': 'Return a patch plan with a precise list of the changed elements. Preserve every explicit invariant.',
  'S2': 'Return a patch plan with a precise list of changed elements. Preserve every explicit invariant. Verify changes against the supplied deterministic checklist and identify any untested requirement.',
  'S3': 'Return a patch plan with a precise list of changed elements. Preserve every explicit invariant. Verify changes against the supplied deterministic checklist and identify any untested requirement. Distinguish observations from hypotheses. Do not alter unrelated UI components. State which requested checks require an external test runner.',
}

def alpha_candidates(tasks: list[Task]) -> list[dict]:
    """C-alpha keeps D byte-identical while S changes; total length varies."""
    rows=[]
    for task in tasks:
        dyn=task.dynamic_text
        dynhash=hashlib.sha256(dyn.encode('utf-8')).hexdigest()
        if not all(fragment.lower() in dyn.lower() for fragment in task.invariants):
            raise ValueError('Invariant absent from dynamic task text')
        for level,scaffold in SCAFFOLDS.items():
            payload={'scaffold':scaffold,'dynamic_task':dyn}
            serialized=json.dumps(payload,ensure_ascii=False,sort_keys=True)
            rows.append({'task_id':task.task_id,'level':level,'payload':payload,
                         'dynamic_sha256':dynhash,'utf8_bytes':len(serialized.encode('utf-8')),
                         'exact_tokens':None,'status':'PENDING_LOCKED_TOKENIZER_AND_BLIND_REVIEW'})
    return rows

TASKS = [
 Task('web_mobile_nav','Revise a responsive webpage. Keep the navigation accessible and opening on mobile. Maintain the visible menu button and correct aria-expanded state.',
      ('navigation accessible','aria-expanded')),
 Task('web_form_validation','Revise a form without changing required email validation. Preserve clear error feedback and a success confirmation when the input is valid.',
      ('email validation','success confirmation')),
 Task('web_contrast','Revise the homepage typography while maintaining sufficient text contrast. Preserve semantic headings and support a 390px mobile viewport.',
      ('text contrast','semantic headings','390px')),
]
