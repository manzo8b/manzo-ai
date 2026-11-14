"""MANZO AI ACR v0.4 — deterministic memory lifecycle/retrieval proof of concept.

No LLM API, no write persistence or identity provider: integration must provide
trusted test registry, authenticated human operations, tokenizer and ACID storage.
This module does NOT establish an AI performance advantage.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from json import dumps
from pathlib import Path
from typing import Callable, Mapping
import json
from jsonschema import Draft202012Validator, FormatChecker

_SCHEMA = json.loads(Path(__file__).with_name('acr_memory.schema.json').read_text(encoding='utf-8'))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
_ALLOWED = {
    ('candidate', 'verified'): {'controller'},
    ('verified', 'approved'): {'human'},
    ('candidate', 'rejected'): {'controller', 'human'},
    ('verified', 'rejected'): {'controller', 'human'},
    ('approved', 'rejected'): {'human'},
    ('approved', 'superseded'): {'human'},
    ('candidate', 'under_review'): {'scheduler'},
    ('verified', 'under_review'): {'scheduler'},
    ('approved', 'under_review'): {'scheduler'},
    ('under_review', 'candidate'): {'human'},
}

class MemoryErrorACR(ValueError):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _dt(s: str | None) -> datetime | None:
    if s is None:
        return None
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    if d.tzinfo is None:
        raise MemoryErrorACR('Date-time must carry a timezone offset')
    return d


def validate(mem: dict) -> None:
    errors = sorted(_VALIDATOR.iter_errors(mem), key=lambda e: str(e.path))
    if errors:
        raise MemoryErrorACR('; '.join(f'{list(e.path)}: {e.message}' for e in errors))
    if mem['id'] == mem.get('supersedes') or mem['id'] == mem.get('superseded_by'):
        raise MemoryErrorACR('Memory cannot supersede itself')
    if mem['history'][-1]['to'] != mem['status']:
        raise MemoryErrorACR('Latest history status does not match memory status')


def create(record: dict, *, actor: str, reason: str, now: datetime | None = None) -> dict:
    """Controller creates candidates; human creates normative rules already approved.

    All callers must authenticate actor outside this library.
    """
    m = deepcopy(record)
    t = now or utcnow()
    if not reason or len(reason) < 3:
        raise MemoryErrorACR('Creation reason required')
    is_norm = m['type'] == 'M0_normative'
    expected = 'approved' if is_norm else 'candidate'
    allowed_actor = 'human' if is_norm else 'controller'
    if actor != allowed_actor or m.get('status') != expected:
        raise MemoryErrorACR(f'Creation requires {allowed_actor} and status {expected}')
    if is_norm and (m['source']['kind'] != 'human' or m['source']['proposed_by'] != 'human'):
        raise MemoryErrorACR('Normative records must be sourced to the human decision')
    if m.get('history'):
        raise MemoryErrorACR('Creation accepts no pre-existing history')
    m['history'] = [{'from': None, 'to': expected, 'by': actor, 'at': t.isoformat(), 'reason': reason}]
    validate(m)
    return m


def verify_evidence(mem: dict, registry: Mapping[tuple[str, str], dict], *, require_generalization: bool = True) -> None:
    """Registry is a TEST-HARNESS-OWNED lookup, never a copy of the candidate memory.

    Expect records containing: result=pass, project, context_id,
    deterministic=True, kind=(regression|generalization), date=YYYY-MM-DD.
    """
    valid = []
    for item in mem['evidence']:
        trusted = registry.get((item['run'], item['test_id']))
        if not trusted:
            continue
        same = (item['result'] == 'pass' and trusted.get('result') == 'pass'
                and trusted.get('project') == mem['scope']['project']
                and trusted.get('context_id') == item['context_id']
                and trusted.get('date') == item['date']
                and trusted.get('deterministic') is True)
        if same:
            valid.append((item, trusted))
    if not valid:
        raise MemoryErrorACR('No independently trusted, matching deterministic PASS evidence')
    if mem['type'] == 'M3_procedural':
        contexts = {t['context_id'] for _, t in valid}
        if len(contexts) < 2:
            raise MemoryErrorACR('M3 requires two independently tested contexts')
        if require_generalization and not any(t.get('kind') == 'generalization' for _, t in valid):
            raise MemoryErrorACR('M3 requires a generalization test')


def transition(mem: dict, to: str, *, actor: str, reason: str,
               registry: Mapping[tuple[str, str], dict] | None = None,
               replacement: dict | None = None,
               now: datetime | None = None) -> dict:
    """Pure return-new-record transition; persistence must be atomic outside this module."""
    validate(mem)
    if (mem['status'], to) not in _ALLOWED or actor not in _ALLOWED[(mem['status'], to)]:
        raise MemoryErrorACR(f'Transition denied: {mem["status"]} -> {to} by {actor}')
    if not reason or len(reason) < 3:
        raise MemoryErrorACR('Reason required')
    if to == 'verified':
        if registry is None:
            raise MemoryErrorACR('Trusted test registry required for verification')
        verify_evidence(mem, registry)
    if to == 'superseded':
        if replacement is None:
            raise MemoryErrorACR('Replacement required')
        validate(replacement)
        if (replacement['supersedes'] != mem['id'] or replacement['id'] == mem['id']
                or replacement['scope']['project'] != mem['scope']['project']
                or replacement['status'] != 'approved'):
            raise MemoryErrorACR('Replacement must be a distinct approved record from the same project')
    t = now or utcnow()
    if to == 'under_review' and not any(d is not None and d <= t for d in
                                        (_dt(mem.get('expires_at')), _dt(mem.get('review_after')))):
        raise MemoryErrorACR('Review cannot be scheduled before its due date')
    m = deepcopy(mem)
    if to == 'superseded':
        m['superseded_by'] = replacement['id']
    m['history'].append({'from': mem['status'], 'to': to, 'by': actor, 'at': t.isoformat(), 'reason': reason})
    m['status'] = to
    validate(m)
    return m


def _eligible(mem: dict, *, project: str, situation: set[str], now: datetime,
              current_revision: int | None, order_two: bool) -> tuple[bool, str]:
    validate(mem)
    if mem['scope']['project'] != project:
        return False, 'wrong_project'
    if mem['status'] not in {'approved', 'verified'}:
        return False, 'inactive_status'
    if any(d is not None and d <= now for d in (_dt(mem['expires_at']), _dt(mem['review_after']))):
        return False, 'review_or_expiry_due'
    if not set(mem['scope']['applies_when']).issubset(situation):
        return False, 'scope_not_applicable'
    if set(mem['scope']['excludes']) & situation:
        return False, 'scope_excluded'
    if order_two and mem['type'] != 'M0_normative':
        r = mem['source']['revision']
        if current_revision is None or r is None or not current_revision - 2 <= r < current_revision:
            return False, 'outside_two_revision_window'
    return True, 'eligible'


def retrieve(records: list[dict], *, project: str, situation: list[str],
             now: datetime, current_revision: int | None, order_two: bool,
             max_tokens: int, token_count: Callable[[str], int]) -> dict:
    """Conjunctive scope; fail-closed for unresolved conflict keys; exact token count supplied by caller.

    Source and claim are untrusted data even after retrieval. Caller must place
    JSON in a lower-trust data slot, never in system/developer instructions.
    """
    if max_tokens < 1:
        raise MemoryErrorACR('Positive memory budget required')
    eligible, excluded = [], []
    for m in records:
        yes, why = _eligible(m, project=project, situation=set(situation),
                             now=now, current_revision=current_revision, order_two=order_two)
        (eligible if yes else excluded).append(m if yes else {'id': m['id'], 'reason': why})
    by_key = {}
    for m in eligible:
        if m['conflict_key'] is not None:
            by_key.setdefault(m['conflict_key'], []).append(m)
    conflicted = set()
    for key, group in by_key.items():
        if len({m['claim'] for m in group}) > 1:
            conflicted.update(m['id'] for m in group)
    eligible = [m for m in eligible if m['id'] not in conflicted]
    excluded.extend({'id': mid, 'reason': 'unresolved_conflict'} for mid in sorted(conflicted))
    ranked = sorted(eligible, key=lambda m: (
        -(3 if m['type'] == 'M0_normative' and m['status'] == 'approved' else
           2 if m['status'] == 'approved' else 1),
        -len(m['scope']['applies_when']),
        -_dt(m['created_at']).timestamp(), m['id']))
    selected = []
    for m in ranked:
        item = {'id': m['id'], 'type': m['type'], 'claim': m['claim'],
                'status': m['status'], 'scope': m['scope'], 'source_ref': m['source']['ref']}
        trial = selected + [item]
        payload = dumps({'memory_data_untrusted': trial}, ensure_ascii=False, separators=(',', ':'))
        if token_count(payload) <= max_tokens:
            selected = trial
        else:
            excluded.append({'id': m['id'], 'reason': 'token_budget'})
    serialized = dumps({'memory_data_untrusted': selected}, ensure_ascii=False, separators=(',', ':'))
    return {'payload_json': serialized, 'selected_ids': [m['id'] for m in selected],
            'excluded': excluded, 'conflicts_for_human': sorted(conflicted),
            'memory_tokens': token_count(serialized)}
