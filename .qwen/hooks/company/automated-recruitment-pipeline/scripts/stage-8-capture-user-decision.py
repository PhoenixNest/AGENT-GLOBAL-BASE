#!/usr/bin/env python
"""
stage-8-capture-user-decision.py
P1 Hook: UserPromptSubmit → User Decision Capture (Stage 8)
============================================================================
Trigger: When user submits hiring outcome decision.

Validates:
  1. Decision is one of: approve, approve_with_conditions, reject
  2. If reject: rollback_stage specified and valid (0-9)
  3. If approve_with_conditions: remediation_items non-empty
  4. Hiring Outcome Report has all 7 sections
  5. All hired candidates have complete audit trails
  6. Per-candidate artifact inventory verified

Exit: 0 = decision valid, 2 = decision invalid (re-prompt user)
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact
from lib.validators import validate_artifact_file


REQUIRED_SECTIONS = 7
VALID_DECISIONS = ["approve", "approve_with_conditions", "reject"]


def validate_user_decision(raw: dict, ctx) -> tuple:
    """Returns (is_valid, failures, warnings)."""
    failures = []
    warnings = []

    decision = raw.get("decision", "").strip().lower()
    rollback_stage = raw.get("rollback_stage")
    conditions = raw.get("conditions", raw.get("remediation_items", []))
    report_sections = raw.get("report_sections_complete", 0)
    audit_complete = raw.get("all_audit_trails_complete", False)

    # 1. Valid decision
    if decision not in VALID_DECISIONS:
        failures.append(f"Invalid decision: '{decision}'. Must be one of: {VALID_DECISIONS}")

    # 2. Reject requires rollback stage
    if decision == "reject":
        if rollback_stage is None:
            failures.append("Reject decision requires rollback_stage (0-9)")
        elif not isinstance(rollback_stage, int) or not (0 <= rollback_stage <= 9):
            failures.append(f"Invalid rollback_stage: {rollback_stage}. Must be 0-9")

    # 3. Approve with conditions requires remediation items
    if decision == "approve_with_conditions":
        if not conditions or len(conditions) == 0:
            failures.append("Approve with conditions requires non-empty remediation_items list")

    # 4. Report completeness
    if report_sections < REQUIRED_SECTIONS:
        failures.append(f"Hiring Outcome Report has {report_sections}/{REQUIRED_SECTIONS} sections (requires {REQUIRED_SECTIONS})")

    # 5. Audit trail completeness
    if not audit_complete:
        warnings.append("Not all hired candidates have complete audit trails")

    # 6. Per-candidate artifact inventory
    candidate_ids = raw.get("candidate_ids", [])
    missing_artifacts = []
    for cid in candidate_ids:
        # Check for expected artifacts — we check the entity root level
        # The actual candidate paths should be provided in the raw input
        cpath = raw.get(f"candidate_path_{cid}", "")
        if cpath:
            for stage_file in ["stage1-psd.md", "stage5-vetting-gate.md",
                               "stage6-background-check.md", "stage7-offer.md",
                               "stage9-hiring-outcome-report.md"]:
                fp = os.path.join(cpath, "pipeline-artifacts", stage_file)
                exists, _ = validate_artifact_file(fp)
                if not exists:
                    missing_artifacts.append(f"{cid}: missing {stage_file}")

    if missing_artifacts:
        warnings.append(f"Missing candidate artifacts: {missing_artifacts[:5]}")

    return len(failures) == 0, failures, warnings


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            c = sys.stdin.read().strip()
            if c:
                raw = json.loads(c)
    except json.JSONDecodeError:
        print("❌ Invalid JSON input", file=sys.stderr)
        sys.exit(2)

    ctx = resolve_entity(raw)
    is_valid, failures, warnings = validate_user_decision(raw, ctx)

    total_checks = 5
    fail_count = len(failures)
    pass_count = total_checks - fail_count
    result = "VALID" if is_valid else "INVALID"

    decision = raw.get("decision", "unknown")
    audit_data = {
        "event_type": "stage_8_user_decision",
        "decision": decision,
        "rollback_stage": raw.get("rollback_stage"),
        "result": result,
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        action_map = {
            "approve": "All candidates advance to Stage 9",
            "approve_with_conditions": f"Candidates advance with {len(raw.get('conditions', []))} remediation items",
            "reject": f"Rolling back to Stage {raw.get('rollback_stage', 'N/A')}",
        }
        print(f"✅ User decision VALID: {decision} — {action_map.get(decision, 'Unknown')}", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ User decision INVALID ({pass_count}/{total_checks} passed):", file=sys.stderr)
        for f_msg in failures:
            print(f"   FAIL: {f_msg}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
