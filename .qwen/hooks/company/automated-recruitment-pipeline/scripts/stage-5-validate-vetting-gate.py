#!/usr/bin/env python
"""
stage-5-validate-vetting-gate.py
P0 Hook: SessionEnd → Elite Vetting Gate Validation (Stage 5)
============================================================================
Trigger: After elite vetting gate evaluation.

Validates:
  1. Impact at Scale score >= 4
  2. Craft Depth score >= 4
  3. Leadership Signal >= 4 (supervisor) or >= 3 (IC)
  4. Standards Signal >= 4
  5. Red Flag Scan = PASS (zero flags)
  6. >= 4 on at least 4 of 5 dimensions
  7. Tenure stability >= 18 months average (flagged if not)
  8. L1+ design roles: ASG-02 review present and passed

Reads vetting artifact from candidate_path for structured validation.

Exit: 0 = pass, 2 = fail (auto-reject)
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


def validate_vetting_gate(raw: dict, ctx) -> tuple:
    """Returns (is_valid, failures, warnings)."""
    failures = []
    warnings = []

    # Try reading vetting artifact first
    vetting_path = ctx.artifact_path("stage5-vetting-gate.md")
    artifact_data = {}
    if vetting_path:
        exists, _ = validate_artifact_file(vetting_path)
        if exists:
            result = parse_artifact(vetting_path)
            artifact_data = result.data

    # Merge stdin data (higher priority) with artifact data
    scores_raw = raw.get("scores", artifact_data.get("scores", {}))

    candidate_id = raw.get("candidate_id", ctx.candidate_id or "N/A")
    is_supervisor = raw.get("is_supervisor", False)
    seniority = raw.get("seniority", artifact_data.get("seniority", ctx.seniority or ""))

    # If seniority-based supervisor detection
    if not is_supervisor and seniority:
        is_supervisor = seniority in ("L3", "L4")

    # Extract scores
    impact = scores_raw.get("impact_at_scale", 0)
    craft = scores_raw.get("craft_depth", 0)
    leadership = scores_raw.get("leadership_signal", 0)
    standards = scores_raw.get("standards_signal", 0)
    red_flags = scores_raw.get("red_flag_scan", "FAIL")
    avg_tenure = scores_raw.get("avg_tenure_months", 0)

    # 1. Impact at Scale >= 4
    if impact < 4:
        failures.append(f"Impact at Scale: {impact}/5 (requires >= 4)")

    # 2. Craft Depth >= 4
    if craft < 4:
        failures.append(f"Craft Depth: {craft}/5 (requires >= 4)")

    # 3. Leadership Signal
    threshold = 4 if is_supervisor else 3
    if leadership < threshold:
        failures.append(f"Leadership Signal: {leadership}/5 (requires >= {threshold} for {'supervisor' if is_supervisor else 'IC'})")

    # 4. Standards Signal >= 4
    if standards < 4:
        failures.append(f"Standards Signal: {standards}/5 (requires >= 4)")

    # 5. Red Flag Scan = PASS
    if red_flags != "PASS":
        failures.append(f"Red Flag Scan: {red_flags} (requires PASS)")

    # 6. >= 4 on at least 4 of 5 dimensions (4 scored dims + red_flag_scan PASS)
    dims_at_4 = sum(1 for s in [impact, craft, leadership, standards] if s >= 4)
    if red_flags == "PASS":
        dims_at_4 += 1  # Red flag PASS counts as 5th dimension
    if dims_at_4 < 4:
        failures.append(f"Only {dims_at_4}/5 dimensions at threshold (requires >= 4)")

    # 7. Tenure stability
    if avg_tenure > 0 and avg_tenure < 18:
        warnings.append(f"Average tenure: {avg_tenure} months (recommended >= 18)")

    # 8. ASG-02 design review for L1+ design roles
    role_family = raw.get("role_family", "").lower()
    if role_family in ("design", "art", "creative-design") and seniority in ("L1", "L2", "L3", "L4"):
        asg02 = raw.get("asg02_design_review", artifact_data.get("asg02_design_review", ""))
        if asg02 == "FAIL":
            failures.append("ASG-02 Design Leadership Review: FAIL")
        elif not asg02 and seniority in ("L3", "L4"):
            warnings.append(f"ASG-02 review not yet completed for {seniority} {role_family} role")

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
    is_valid, failures, warnings = validate_vetting_gate(raw, ctx)

    total_checks = 7
    fail_count = len(failures)
    pass_count = total_checks - fail_count
    result = "PASS" if is_valid else "FAIL"

    audit_data = {
        "event_type": "stage_5_vetting_gate",
        "result": result,
        "scores": raw.get("scores", {}),
        "dimensions_at_threshold": sum(1 for s in [
            raw.get("scores", {}).get("impact_at_scale", 0),
            raw.get("scores", {}).get("craft_depth", 0),
            raw.get("scores", {}).get("leadership_signal", 0),
            raw.get("scores", {}).get("standards_signal", 0),
        ] if s >= 4),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        dims = sum(1 for s in [
            raw.get("scores", {}).get("impact_at_scale", 0),
            raw.get("scores", {}).get("craft_depth", 0),
            raw.get("scores", {}).get("leadership_signal", 0),
            raw.get("scores", {}).get("standards_signal", 0),
        ] if s >= 4)
        print(f"✅ Vetting gate PASSED for {ctx.candidate_id} ({pass_count}/{total_checks} checks, {dims}/4 scored dims at threshold)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Vetting gate FAILED for {ctx.candidate_id}:", file=sys.stderr)
        for f_msg in failures:
            print(f"   FAIL: {f_msg}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
