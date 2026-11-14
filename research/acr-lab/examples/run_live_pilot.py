"""Manual real-model pilot; never invokes an API without --provider openai and a key."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from acr.live_pilot import OpenAIResponsesEditor, run_edit_trial


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--provider', choices=['openai'], required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--fixture',type=Path,default=Path('examples/pilot_cases/navigation_contrast/rev0.html'))
    parser.add_argument('--task-id',default='navigation_contrast')
    parser.add_argument('--objective',default='Improve the mobile UI and preserve previously working checks.')
    parser.add_argument('--out',type=Path,default=Path('experiments/experiment_a/results/live_pilot'))
    parser.add_argument('--revisions',type=int,default=2)
    args=parser.parse_args()
    for arm in ('C2','C3'):
        editor=OpenAIResponsesEditor(args.model)
        trial=run_edit_trial(initial_html=args.fixture,objective=args.objective,
            task_id=args.task_id,arm=arm,model=editor,out_dir=args.out/arm,
            max_revisions=args.revisions)
        print(json.dumps(trial,ensure_ascii=False,indent=2))
    print('Exploratory instrumented pilot only. No statistical claims from this run.')

if __name__=='__main__': main()
