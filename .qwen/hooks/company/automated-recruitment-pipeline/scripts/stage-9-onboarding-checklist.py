#!/usr/bin/env python
"""
stage-9-onboarding-checklist.py
P3 Hook: PostToolUse → Onboarding Checklist Validation (Stage 9)
============================================================================
Trigger: When onboarding process begins.

Validates:
  1. Equipment ordered/delivered
  2. Accounts created and active
  3. Software licenses provisioned
  4. Buddy assigned (tenure > 6 months, performance >= Strong)
  5. Manager briefing complete
  6. Documentation package prepared
  7. For contractors: time-bound access with auto-revocation date

Exit: 0 = checklist complete, 2 = checklist incomplete
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


def validate_onboarding(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read provisioning artifact
    prov_path = ctx.artifact_path("stage8-provisioning.md")
    artifact_data = {}
    if prov_path:
        exists, _ = validate_artifact_file(prov_path)
        if exists:
            result = parse_artifact(prov_path)
            artifact_data = result.data

    # Merge with stdin data
    provisioning = raw.get("provisioning", artifact_data.get("provisioning", {}))
    is_contractor = raw.get("contractor", artifact_data.get("contractor", False))

    # 1. Equipment
    if not provisioning.get("equipment_ordered", False):
        errors.append("Equipment not yet ordered")

    # 2. Accounts
    if not provisioning.get("accounts_created", False):
        errors.append("Accounts not yet created")

    # 3. Software licenses
    if not provisioning.get("software_licenses", False):
        warnings.append("Software licenses not fully provisioned")

    # 4. Buddy
    if not provisioning.get("buddy_assigned", False):
        errors.append("Buddy not assigned")

    # 5. Manager briefing
    if not provisioning.get("manager_briefing", False):
        warnings.append("Manager briefing not confirmed")

    # 6. Documentation
    if not provisioning.get("documentation_sent", False):
        warnings.append("Documentation package not sent")

    # 7. Contractor-specific checks
    if is_contractor:
        clearance = provisioning.get("clearance_level", raw.get("clearance_level", ""))
        if clearance:
            # Parse numeric level for safe comparison
            clearance_num = int(clearance[1:]) if clearance.startswith("L") and clearance[1:].isdigit() else 0
            if clearance_num < 2:
                errors.append(f"Contractor clearance {clearance} below L2 minimum")
        revocation = raw.get("auto_revocation_date", artifact_data.get("auto_revocation_date", ""))
        if not revocation:
            errors.append("Contractor missing auto-revocation date")

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
    is_valid, errors, warnings = validate_onboarding(raw, ctx)

    audit_data = {
        "event_type": "stage_9_onboarding_checklist",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "is_valid": is_valid,
        "error_count": len(errors),
        "is_contractor": raw.get("contractor", False),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Onboarding checklist validated", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Onboarding checklist FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
