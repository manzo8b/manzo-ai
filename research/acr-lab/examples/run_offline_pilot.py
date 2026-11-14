"""Exercise C2/C3 isolation and trace infrastructure, NO LLM or ACR effect."""
import argparse
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from acr.pilot_replay import run_replay

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=ROOT/'experiments/experiment_a/results/offline_pilot')
    args=ap.parse_args()
    cases={'navigation_contrast':ROOT/'examples/pilot_cases/navigation_contrast',
           'form_layout':ROOT/'examples/pilot_cases/form_layout'}
    result=run_replay(cases=cases,out=args.out)
    print(json.dumps({'status':result['status'],'comparisons':result['comparisons'],
                      'llm_requests':result['llm_requests']},indent=2,ensure_ascii=False))
