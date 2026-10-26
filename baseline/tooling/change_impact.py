#!/usr/bin/env python3
"""Prospective change-impact report: structural deltas versus measured maintenance work.

Reports remain evidence, not automated architectural decisions. No benchmark feedback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from maintenance_sensor import compare as compare_snapshots

VERSION = 1
METRICS = ("attempts", "rework", "regressions", "coordinated_semantic_edit_sites",
           "elapsed_seconds", "tool_wait_seconds", "tokens", "tool_and_investigation_cost")


def load(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("expected JSON object: " + str(path))
    return obj


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def evidence_item(path: Path) -> dict[str, Any]:
    return {"path": str(path), "sha256": digest(path.read_bytes())}


def numeric(value: Any, name: str) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number or null")
    return value


def assess_trial(data: dict[str, Any] | None) -> dict[str, Any]:
    if data is None:
        return {"status": "NOT_MEASURED", "data": None}
    if data.get("record_status") == "TEMPLATE_NOT_AN_EXECUTED_TRIAL":
        return {"status": "NOT_MEASURED_TEMPLATE_ONLY", "data": None}
    if data.get("record_status") != "OBSERVED_TRIAL":
        raise ValueError("trial must declare OBSERVED_TRIAL or TEMPLATE_NOT_AN_EXECUTED_TRIAL")
    task = data.get("task")
    cond = data.get("conditions")
    obs = data.get("task_observations")
    checks = data.get("verification")
    if not all(isinstance(v, dict) for v in (task, cond, obs, checks)):
        raise ValueError("observed trial needs task, conditions, task_observations, verification")
    for field in ("id", "family", "released_requirement", "external_acceptance_criterion"):
        if not isinstance(task.get(field), str) or not task[field].strip():
            raise ValueError(f"observed trial task missing {field}")
    if not isinstance(cond.get("source_commit"), str) or not cond["source_commit"]:
        raise ValueError("observed trial needs a source_commit")
    for metric in METRICS:
        numeric(obs.get(metric), metric)
    if (obs.get("elapsed_seconds") is not None and obs.get("tool_wait_seconds") is not None and
            obs["tool_wait_seconds"] > obs["elapsed_seconds"]):
        raise ValueError("tool wait exceeds elapsed time")
    if not isinstance(obs.get("responsibilities_touched"), list):
        raise ValueError("responsibilities_touched must be a list")
    if not isinstance(obs.get("evidence"), list) or not obs["evidence"]:
        raise ValueError("observed work needs explicit evidence references")
    if not isinstance(checks.get("contract_checks"), list) or not checks["contract_checks"]:
        raise ValueError("observed trial needs contract checks, including NOT_RUN when appropriate")
    outcome = checks.get("acceptance_status", "NOT_VERIFIED")
    if outcome not in {"PASS", "FAIL", "NOT_RUN", "NOT_VERIFIED"}:
        raise ValueError("invalid independent acceptance_status")
    return {"status": "OBSERVED_SINGLE_TASK_NOT_CAUSAL", "task": {k: task[k] for k in
            ("id", "family", "external_acceptance_criterion")},
            "conditions": {"source_commit": cond["source_commit"],
                           "agent_model": cond.get("agent_model"),
                           "prior_exposure": cond.get("prior_exposure")},
            "measurements": {k: obs.get(k) for k in METRICS},
            "responsibilities_touched": obs["responsibilities_touched"],
            "evidence": obs["evidence"], "acceptance_status": outcome,
            "independent_acceptance_evidence": checks.get("independent_evidence", []),
            "interpretation": "Observed work on one task; no claim that an architectural change improved maintainability."}


def trial_pair(a: dict[str, Any] | None, b: dict[str, Any] | None) -> dict[str, Any]:
    old, new = assess_trial(a), assess_trial(b)
    if old["status"] != "OBSERVED_SINGLE_TASK_NOT_CAUSAL" or new["status"] != "OBSERVED_SINGLE_TASK_NOT_CAUSAL":
        return {"status": "NOT_COMPARABLE", "reason": "both trials need observed measurements"}
    shared_family = old["task"]["family"] == new["task"]["family"]
    shared_acceptance = old["task"]["external_acceptance_criterion"] == new["task"]["external_acceptance_criterion"]
    if not shared_family or not shared_acceptance:
        return {"status": "NOT_COMPARABLE", "same_family": shared_family,
                "same_acceptance_criterion": shared_acceptance}
    changes = {k: new["measurements"][k] - old["measurements"][k] if
               old["measurements"][k] is not None and new["measurements"][k] is not None else None
               for k in METRICS}
    return {"status": "DESCRIPTIVE_MATCHED_FAMILY_ONLY", "deltas": changes,
            "before_acceptance": old["acceptance_status"], "after_acceptance": new["acceptance_status"],
            "causal_improvement_established": False,
            "limitation": "Same task family and criterion are necessary but insufficient for causal comparison. Check task difficulty, repeated exposure, agent/model, budgets, and independent acceptance."}


def analyze(before: dict[str, Any], after: dict[str, Any],
            trial: dict[str, Any] | None = None,
            baseline_trial: dict[str, Any] | None = None) -> dict[str, Any]:
    structural = compare_snapshots(before, after)
    b, a = before["summary"], after["summary"]
    if b["threshold"] != a["threshold"] or before["scope"]["requested_sources"] != after["scope"]["requested_sources"]:
        comparable = False
    else:
        comparable = structural["coverage_complete"]
    deltas = {k: (a[k] - b[k]) if isinstance(a.get(k), (int, float)) and not isinstance(a.get(k), bool)
              and isinstance(b.get(k), (int, float)) and not isinstance(b.get(k), bool) else None
              for k in ("functions", "total_mass_proxy", "high_mass_proxy", "high_mass_fraction_proxy", "high_cc_functions", "max_cc_proxy")}
    if not comparable:
        deltas = {k: None for k in deltas}
    funcs = structural["functions"]
    changed = [f for f in funcs if f["status"] != "UNCHANGED"]
    new_low = deltas.get("high_mass_fraction_proxy")
    absolute = deltas.get("high_mass_proxy")
    dilution = comparable and new_low is not None and absolute is not None and new_low < 0 and absolute >= 0
    return {"schema_version": VERSION, "structural": {
                "status": "COMPARABLE_PROXY" if comparable else "INCOMPARABLE_SCOPE_COVERAGE_OR_THRESHOLD",
                "before_label": before["label"], "after_label": after["label"],
                "before_scope": before["scope"], "after_scope": after["scope"],
                "before_summary": b, "after_summary": a, "deltas": deltas,
                "changed_or_unmatched_functions": changed,
                "function_identity_limit": structural["matching"],
                "ratio_dilution_candidate": dilution,
                "complexity_is_maintainability": False},
            "work": assess_trial(trial),
            "matched_work": trial_pair(baseline_trial, trial) if baseline_trial is not None else
            {"status": "NOT_MEASURED", "reason": "no comparable baseline task trial supplied"},
            "overall_maintenance_conclusion": "UNESTABLISHED",
            "decision": "INVESTIGATE_IF_RELEVANT_NOT_AUTOMATIC_REFACTOR",
            "limits": ["Static metrics are Python AST proxies, not the benchmark scorer.",
                       "A changed source cannot prove a maintenance improvement without a concrete task.",
                       "A matched task-family comparison is descriptive and may be confounded.",
                       "Parse failures, coverage changes and definition-identity uncertainty require review."]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--before", type=Path, required=True)
    ap.add_argument("--after", type=Path, required=True)
    ap.add_argument("--trial", type=Path)
    ap.add_argument("--baseline-trial", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.baseline_trial and not args.trial:
        ap.error("--baseline-trial requires --trial")
    try:
        paths = [args.before, args.after] + ([args.trial] if args.trial else []) + (
            [args.baseline_trial] if args.baseline_trial else [])
        inputs = [load(p) for p in paths]
        value = analyze(inputs[0], inputs[1], inputs[2] if args.trial else None,
                        inputs[3] if args.baseline_trial else None)
        value["input_evidence_sha256"] = [evidence_item(p) for p in paths]
        serialized = json.dumps(value, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
        return 0 if value["structural"]["status"] == "COMPARABLE_PROXY" else 2
    except (ValueError, KeyError, TypeError, OSError) as exc:
        ap.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
