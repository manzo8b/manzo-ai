"""Write exploratory C-alpha candidates; C-beta remains BLOCKED pending tokenizer and review."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from acr.prompt_study import TASKS,alpha_candidates

if __name__=='__main__':
    out=ROOT/'experiments/experiment_c/drafts'
    out.mkdir(parents=True,exist_ok=True)
    rows=alpha_candidates(TASKS)
    (out/'c_alpha_candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    blocked={'study':'C-beta','status':'NOT_RUN','reason':'Actual model/tokenizer, semantically equivalent dynamic variants, independent blind review, and total budgets not frozen',
     'proposed_ratios':[0.3,0.5,0.62,0.8],'no_fake_padding':True,'generated_variants':0}
    (out/'c_beta_blocked.json').write_text(json.dumps(blocked,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'Prepared {len(rows)} C-alpha candidate prompts (not executed). C-beta blocked until controls are locked.')
