"""Conservative *static* research-design checks. Never runs an LLM or an experiment."""
from __future__ import annotations
import json
from pathlib import Path


def load_manifest(path: Path | str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def token_allocation(total: int, ratios: list[float]) -> list[dict]:
    """Illustrate quotas; DOES NOT create meaning-preserving prompts."""
    if total <= 0:
        raise ValueError("positive total required")
    results = []
    for r in ratios:
        if not 0 < r < 1:
            raise ValueError("ratio must be between 0 and 1")
        s = round(total * r)
        results.append({"ratio": r, "scaffold_tokens": s, "dynamic_tokens": total - s})
    return results


def validate_b(manifest: dict) -> list[str]:
    issues = []
    horizon = manifest["max_revisions"]
    audit_budget = manifest["deep_audit_budget_per_arm"]
    if not manifest.get("critical_tests_each_revision"):
        issues.append("Critical tests must run at every revision")
    for arm in ("B-FIB", "B-UNIF"):
        points = manifest["arms"][arm]["checkpoints"]
        if sorted(set(points)) != points or not all(1 <= p <= horizon for p in points):
            issues.append(f"{arm}: invalid, unordered, or out-of-horizon checkpoints")
        if len(points) != audit_budget:
            issues.append(f"{arm}: deep audit count differs from budget")
    if manifest["arms"]["B-EVENT"]["max_deep_audits"] != audit_budget:
        issues.append("Event arm must have the same maximum audit budget")
    if "TO BE LOCKED" in manifest["arms"]["B-EVENT"]["trigger"]:
        issues.append("B-EVENT threshold not frozen — protocol cannot yet run")
    return issues


def validate_c(manifest: dict) -> list[str]:
    issues = []
    beta = manifest["studies"]["C-beta"]
    for total in beta["nominal_total_token_budgets"]:
        for alloc in token_allocation(total, beta["scaffold_ratios"]):
            if alloc["dynamic_tokens"] < 250:
                issues.append(f"C-beta {total} tokens @ {alloc['ratio']:.2f}: dynamic span <250 tokens; feasibility review required")
    if beta.get("actual_tokenizer") == "TO_BE_LOCKED":
        issues.append("Actual tokenizer not frozen — ratio cannot be measured exactly")
    if beta.get("task_semantics") != "blind_review_required":
        issues.append("Missing semantic-equivalence audit")
    return issues


def summarize_design(b: dict, c: dict) -> dict:
    beta = c["studies"]["C-beta"]
    counts = beta["arm_count"] * len(beta["nominal_total_token_budgets"]) * beta["tasks_planned"] * beta["repetitions"]
    return {
        "category": "static_design_check_not_empirical_evidence",
        "experiment_a_status": "not_run",
        "experiment_b_status": "not_run",
        "experiment_c_status": "not_run",
        "b_horizon": b["max_revisions"],
        "b_checkpoints": {arm:b["arms"][arm].get("checkpoints") for arm in ("B-FIB", "B-UNIF")},
        "c_beta_planned_run_count": counts,
        "c_allocations": {str(n):token_allocation(n, beta["scaffold_ratios"]) for n in beta["nominal_total_token_budgets"]},
        "b_open_items": validate_b(b),
        "c_open_items": validate_c(c),
    }
