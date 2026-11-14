from datetime import datetime,timezone
from acr.pilot_replay import candidate_from_browser_fix
from acr.engine import transition, retrieve

def test_verified_memory_requires_registry_and_window():
    now=datetime(2026,11,14,tzinfo=timezone.utc)
    m=candidate_from_browser_fix(memory_id='mem_1099',project='form_layout',revision=2,
      run_id='test_C3',test_id='email_form_validation',date='2026-11-14',now=now)
    reg={('test_C3_rev_2','email_form_validation'):{'result':'pass','project':'form_layout',
       'context_id':'form_layout_rev_2','deterministic':True,'kind':'regression','date':'2026-11-14'}}
    m=transition(m,'verified',actor='controller',reason='browser evidence',registry=reg,now=now)
    selected=retrieve([m],project='form_layout',situation=['web_review'],now=now,
       current_revision=3,order_two=True,max_tokens=4000,token_count=lambda s:len(s.encode()))
    assert selected['selected_ids']==['mem_1099']
    old=retrieve([m],project='form_layout',situation=['web_review'],now=now,
       current_revision=5,order_two=True,max_tokens=4000,token_count=lambda s:len(s.encode()))
    assert old['selected_ids']==[]
