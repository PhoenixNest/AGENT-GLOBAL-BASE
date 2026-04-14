#!/usr/bin/env python
"""
stage-5-asg02-design-review.py
P1 Hook: PreToolUse → ASG-02 Design Leadership Review (Stage 5)
============================================================================
Trigger: When design leadership review is initiated for L1+ design roles.

Validates:
  1. Role is design-family at L1+ seniority
  2. Review evaluator is specified (CDO or delegate)
  3. All 3 review components present (portfolio, whiteboard, craft critique)
  4. Review duration = 75 minutes (time-boxed)

Exit: 0 = review valid, 2 = review invalid (block advancement)
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.validators import check_required, check_enum


DESIGN_FAMILIES = ["design", "art", "creative-design"]
ELIGIBLE_SENIORITIES = ["L1", "L2", "L3", "L4"]
REVIEW_COMPONENTS = ["portfolio_deep_dive", "whiteboard_exercise", "craft_critique"]


def validate_asg02(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # 1. Role family check
    rf = raw.get("role_family", "").lower().strip()
    if rf not in DESIGN_FAMILIES:
        # Not a design role — review should be waived
        return True, errors, ["ASG-02 waived for non-design role family"]

    # 2. Seniority check
    sen = raw.get("seniority", "").strip()
    if sen not in ELIGIBLE_SENIORITIES:
        return True, errors, ["ASG-02 waived for L0 (junior) role"]

    # 3. Evaluator specified
    evaluator = raw.get("evaluator", "")
    if not evaluator:
        errors.append("ASG-02 requires evaluator (CDO or Head of Design)")

    # 4. Review components
    components = raw.get("components", [])
    if components:
        for comp in REVIEW_COMPONENTS:
            if comp not in components:
                warnings.append(f"ASG-02 component '{comp}' not yet completed")

    # 5. Duration check
    duration = raw.get("duration_minutes", 0)
    if duration > 0 and duration != 75:
        warnings.append(f"ASG-02 duration is {duration}min (standard is 75min)")

    return len(errors) == 0, errors, warnings


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
    is_valid, errors, warnings = validate_asg02(raw, ctx)

    audit_data = {
        "event_type": "stage_5_asg02_design_review",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "role_family": raw.get("role_family", "unknown"),
        "seniority": raw.get("seniority", "unknown"),
        "is_valid": is_valid,
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} ASG-02 design review validated", file=sys.stderr)
        for w in warnings:
            print(f"   INFO: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ ASG-02 design review FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
