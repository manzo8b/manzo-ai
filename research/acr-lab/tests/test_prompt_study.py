import pytest
from acr.prompt_study import TASKS,Task,alpha_candidates

def test_alpha_dynamic_hash_invariant_across_all_scaffolds():
    rows=alpha_candidates(TASKS)
    assert len(rows)==12
    for task in TASKS:
        group=[x for x in rows if x['task_id']==task.task_id]
        assert len({x['dynamic_sha256'] for x in group})==1
        assert len({x['utf8_bytes'] for x in group})==4
        assert all(x['exact_tokens'] is None for x in group)

def test_missing_invariant_is_rejected():
    with pytest.raises(ValueError):
        alpha_candidates([Task('bad','No heading preserved',('WCAG contrast',))])
