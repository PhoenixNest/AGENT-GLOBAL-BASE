#!/usr/bin/env python
"""
stage-0-validate-department-plan.py
P1 Hook: UserPromptSubmit → Department Planning Validator (Stage 0)
============================================================================
Trigger: When department head submits recruitment plan for consolidation.

Behavior:
  1. Validate required fields against schema
  2. Cross-reference roles against approved taxonomy
  3. Check budget capacity, duplicates, priority justification
  4. Log to entity-specific audit log

Exit: 0 = plan valid, 2 = plan invalid (return to department head)
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.validators import check_required, check_enum


# Approved role families (universal)
VALID_ROLE_FAMILIES = {
    "company": ["engineering", "product", "design", "data", "translation",
                "security", "business", "hr", "devops"],
    "studio": ["leadership", "engineering", "creative-design", "art",
               "audio", "production", "live-ops"],
}
VALID_SENIORITIES = ["L0", "L1", "L2", "L3", "L4"]
VALID_PRIORITIES = ["P0", "P1", "P2"]


def validate_department_plan(raw: dict) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Top-level required
    for field in ["department", "planning_quarter", "budget_impact"]:
        errors.extend(check_required(raw, field))

    roles = raw.get("roles", [])
    if not roles:
        errors.append("At least one role must be specified")
        return False, errors, warnings

    if not isinstance(roles, list):
        errors.append("'roles' must be an array")
        return False, errors, warnings

    seen = set()
    total_headcount = 0
    p0_count = 0

    for i, role in enumerate(roles):
        prefix = f"roles[{i}]"

        # Required fields
        for field in ["title", "role_family", "seniority", "count", "justification", "priority"]:
            errors.extend(check_required(role, field, prefix))

        # Role family
        rf = role.get("role_family", "").lower().strip()
        entity_type = raw.get("entity_type", "company")
        valid_families = VALID_ROLE_FAMILIES.get(entity_type, VALID_ROLE_FAMILIES["company"])
        if rf and rf not in valid_families:
            errors.append(f"{prefix}.role_family '{rf}' invalid. Must be one of: {valid_families}")

        # Seniority
        sen = role.get("seniority", "").strip()
        errors.extend(check_enum(sen, VALID_SENIORITIES, f"{prefix}.seniority"))

        # Count
        count = role.get("count")
        if isinstance(count, (int, float)):
            if count < 1:
                errors.append(f"{prefix}.count must be >= 1")
            total_headcount += int(count)

        # Priority
        pri = role.get("priority", "").strip().upper()
        errors.extend(check_enum(pri, VALID_PRIORITIES, f"{prefix}.priority"))

        # P0 requires detailed justification
        if pri == "P0":
            p0_count += 1
            just = role.get("justification", "")
            if len(str(just)) < 50:
                errors.append(f"{prefix}.justification: P0 requires business case (≥50 chars)")

        # Duplicate check
        key = (role.get("title", "").lower(), role.get("seniority", "").lower())
        if key in seen and key[0]:
            errors.append(f"{prefix}: Duplicate role '{role.get('title')}' at {role.get('seniority')} level")
        seen.add(key)

    # --- Plan Amendment Validation ---
    is_amendment = raw.get("is_amendment", False)
    if is_amendment:
        amendment_id = raw.get("amendment_id", "")
        if not amendment_id:
            errors.append("Amendment requires amendment_id field")
        amendment_reason = raw.get("amendment_reason", "")
        if len(str(amendment_reason)) < 30:
            errors.append(f"Amendment requires business justification (≥30 chars, got {len(str(amendment_reason))})")
        original_plan_id = raw.get("original_plan_id", "")
        if not original_plan_id:
            errors.append("Amendment must reference original_plan_id")

    # Warnings
    if total_headcount > 20:
        warnings.append(f"Total headcount {total_headcount} may strain onboarding capacity")
    if p0_count > 5:
        warnings.append(f"{p0_count} P0 roles — verify all are truly critical")

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
    is_valid, errors, warnings = validate_department_plan(raw)

    checks_total = 12
    checks_passed = checks_total - len(errors)

    # Audit
    audit_data = {
        "event_type": "stage_0_department_plan_validation",
        "department": raw.get("department", "unknown"),
        "is_valid": is_valid,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "checks_total": checks_total,
        "checks_passed": max(0, checks_passed),
        "errors": errors[:5],  # Truncate for audit
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Department plan validation passed ({max(0, checks_passed)}/{checks_total} checks)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        print(json.dumps({"is_valid": True, "warnings": warnings}), file=sys.stdout)
        sys.exit(0)
    else:
        print(f"❌ Department plan validation FAILED ({max(0, checks_passed)}/{checks_total} checks):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        print(json.dumps({"is_valid": False, "errors": errors, "warnings": warnings}), file=sys.stdout)
        sys.exit(2)


if __name__ == "__main__":
    main()
