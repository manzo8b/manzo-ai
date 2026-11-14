import json
from pathlib import Path
import pytest
from acr.design_guard import load_manifest, token_allocation, validate_b, validate_c, summarize_design

ROOT = Path(__file__).resolve().parents[1]


def manifests():
    return (load_manifest(ROOT / 'experiments/experiment_b/manifest.draft.json'),
            load_manifest(ROOT / 'experiments/experiment_c/manifest.draft.json'))


def test_quota_sums_and_example():
    alloc = token_allocation(1500, [0.30,0.50,0.62,0.80])
    assert [(x['scaffold_tokens'], x['dynamic_tokens']) for x in alloc] == [(450,1050),(750,750),(930,570),(1200,300)]
    assert all(x['scaffold_tokens']+x['dynamic_tokens']==1500 for x in alloc)


def test_quota_invalid():
    with pytest.raises(ValueError): token_allocation(0,[0.62])
    with pytest.raises(ValueError): token_allocation(100,[1])


def test_b_within_horizon_and_equal_budget():
    b, _ = manifests()
    assert b['arms']['B-FIB']['checkpoints'] == [1,2,3,5,8]
    assert len(b['arms']['B-UNIF']['checkpoints']) == b['deep_audit_budget_per_arm']
    assert b['max_revisions'] >= 8


def test_b_draft_blocks_frozen_claims():
    b, _ = manifests()
    assert any('cannot yet run' in item for item in validate_b(b))


def test_c_draft_flags_tokenizer():
    _,c = manifests()
    assert any('not frozen' in item for item in validate_c(c))


def test_c_manifest_planned_runs():
    b,c=manifests()
    report=summarize_design(b,c)
    assert report['c_beta_planned_run_count']==480
    assert all(report['experiment_'+x+'_status']=='not_run' for x in ('a','b','c'))
