"""No API calls; deterministic double proves instrumentation, not causal benefit."""
from pathlib import Path
from acr.live_pilot import GeneratedEdit, checked_html, run_edit_trial

class EchoEditor:
    model_id='test-double'
    def edit(self, *, system, prompt, max_output_tokens):
        assert 'CURRENT_HTML_DATA' in prompt
        document=prompt.split('CURRENT_HTML_DATA:\n',1)[1].split('\nTASK_OUTPUT_CONTRACT:',1)[0]
        return GeneratedEdit(document,'No modification; neutral echo',None,None,'test-double')

FIX=Path(__file__).resolve().parents[1]/'examples/browser_fixture/rev0.html'

def test_document_boundaries():
    try:
        checked_html('<html></html>')
        assert False,'Incomplete HTML should be rejected'
    except ValueError:
        pass

def test_untrusted_iframe_rejected():
    try:
        checked_html('<!doctype html><html><iframe src="x"></iframe></html>')
        assert False
    except ValueError:
        pass

def test_two_arm_runs_are_separate_and_neutral(tmp_path):
    for arm in ('C2','C3'):
        result=run_edit_trial(initial_html=FIX,objective='Preserve the existing working UI',
            task_id='fixture',arm=arm,model=EchoEditor(),out_dir=tmp_path/arm,
            max_revisions=1,count_tokens=lambda s:len(s)//3+1)
        assert result['llm_used'] is False
        assert result['metrics']['regressions']==0
        assert result['metrics']['final_pass_rate']==1.0
        assert (tmp_path/arm/'traces.sqlite').is_file()

class RepairThenEcho:
    model_id='test-double'
    def __init__(self):
        self.prompts=[]
    def edit(self, *, system, prompt, max_output_tokens):
        self.prompts.append(prompt)
        if len(self.prompts)==1:
            # First revision repairs a deliberately broken menu fixture.
            good=FIX.read_text(encoding='utf8')
            return GeneratedEdit(good,'Repair mobile menu',None,None,'test-double')
        document=prompt.split('CURRENT_HTML_DATA:\n',1)[1].split('\nTASK_OUTPUT_CONTRACT:',1)[0]
        return GeneratedEdit(document,'Preserve the repaired menu',None,None,'test-double')


def test_verified_memory_is_retrieved_only_in_c3(tmp_path):
    broken=FIX.parent/'rev1.html'
    for arm in ('C2','C3'):
        editor=RepairThenEcho()
        result=run_edit_trial(initial_html=broken,objective='Repair menu while keeping all other checks passing',
            task_id='menu-repair',arm=arm,model=editor,out_dir=tmp_path/arm,
            max_revisions=2,count_tokens=lambda s:len(s)//3+1)
        assert result['llm_used'] is False
        assert result['snapshots'][0]['fails']==1
        assert result['snapshots'][1]['fails']==0
        assert result['snapshots'][2]['fails']==0
        assert len(editor.prompts)==2
        payload=editor.prompts[1].split('CURRENT_HTML_DATA:',1)[0]
        if arm=='C3':
            assert 'mem_1000' in payload
            assert 'mobile_menu' in payload
        else:
            assert 'mem_1000' not in payload
