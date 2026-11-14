"""Summarize static feasibility of experimental drafts (not experimental outcomes)."""
import json
from pathlib import Path
from acr.design_guard import load_manifest, summarize_design

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    b = load_manifest(root / "experiments/experiment_b/manifest.draft.json")
    c = load_manifest(root / "experiments/experiment_c/manifest.draft.json")
    print(json.dumps(summarize_design(b, c), indent=2, ensure_ascii=False))
