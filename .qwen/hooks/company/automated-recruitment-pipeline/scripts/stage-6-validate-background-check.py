#!/usr/bin/env python
"""
stage-6-validate-background-check.py
P1 Hook: PostToolUse → Background Check Validation (Stage 6)
============================================================================
Trigger: After background check completes.

Validates:
  1. All 5 checks present (employment, education, criminal, references, COI)
  2. Overall status consistent with individual check results
  3. FAIL or DISQUALIFYING on any check → overall_status = FAIL
  4. All CLEAR → overall_status = CLEAR
  5. Contractor COI included
  6. Reads background check artifact for structured validation

Exit: 0 = background check valid, 2 = check failed or data inconsistent
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact
from lib.validators import validate_artifact_file, check_required

REQUIRED_CHECKS = [
    "employment_verification",
    "education_verification",
    "criminal_background",
    "reference_checks",
    "conflict_of_interest",
]
FAIL_VALUES = {"FAIL", "DISQUALIFYING"}
CLEAR_VALUE = "CLEAR"


def validate_background_check(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read background check artifact
    bg_path = ctx.artifact_path("stage6-background-check.md")
    artifact_data = {}
    if bg_path:
        exists, _ = validate_artifact_file(bg_path)
        if exists:
            result = parse_artifact(bg_path)
            artifact_data = result.data

    # Merge stdin with artifact data
    checks = raw.get("checks", artifact_data.get("checks", {}))
    overall = raw.get("overall_status", artifact_data.get("overall_status", ""))
    is_contractor = raw.get("contractor", artifact_data.get("contractor", False))
    flags = raw.get("flags", artifact_data.get("flags", []))

    # 1. All 5 checks present
    for check_name in REQUIRED_CHECKS:
        if check_name not in checks:
            errors.append(f"Missing required check: {check_name}")

    # If any check is missing, we can't validate further
    if any(c not in checks for c in REQUIRED_CHECKS):
        return False, errors, warnings

    # 2. Overall status consistency
    any_fail = any(checks.get(c) in FAIL_VALUES for c in REQUIRED_CHECKS)
    all_clear = all(checks.get(c) == CLEAR_VALUE for c in REQUIRED_CHECKS)

    if all_clear and overall != CLEAR_VALUE:
        errors.append(
            f"All checks CLEAR but overall_status = '{overall}' (expected 'CLEAR')"
        )

    if any_fail:
        # Determine which check(s) failed
        failed_checks = [c for c in REQUIRED_CHECKS if checks.get(c) in FAIL_VALUES]
        if overall != "FAIL":
            errors.append(
                f"Failed checks: {failed_checks}, but overall_status = '{overall}' (expected 'FAIL')"
            )

    # 3. Specific check validation
    employment = checks.get("employment_verification", "")
    if employment not in (CLEAR_VALUE, "FLAGGED", "FAIL"):
        errors.append(f"Invalid employment_verification value: '{employment}'")

    education = checks.get("education_verification", "")
    if education not in (CLEAR_VALUE, "FLAGGED", "FAIL"):
        errors.append(f"Invalid education_verification value: '{education}'")

    criminal = checks.get("criminal_background", "")
    if criminal not in (CLEAR_VALUE, "FLAGGED", "FAIL"):
        errors.append(f"Invalid criminal_background value: '{criminal}'")

    references = checks.get("reference_checks", "")
    if references not in (CLEAR_VALUE, "FLAGGED", "FAIL"):
        errors.append(f"Invalid reference_checks value: '{references}'")

    coi = checks.get("conflict_of_interest", "")
    valid_coi = (CLEAR_VALUE, "FLAGGED", "DISQUALIFYING", "ACCEPTABLE_WITH_MITIGATIONS")
    if coi not in valid_coi:
        errors.append(f"Invalid conflict_of_interest value: '{coi}'. Must be one of: {valid_coi}")

    # 4. COI disqualifying check (redundant with any_fail check above, kept for clarity)
    if coi == "DISQUALIFYING" and overall != "FAIL":
        errors.append("COI is DISQUALIFYING but overall_status != 'FAIL'")

    # 5. Contractor-specific COI
    if is_contractor and not coi:
        errors.append("Contractor missing conflict_of_interest check")

    # 6. Flag consistency
    if flags and isinstance(flags, list):
        unresolved = [f for f in flags if not f.get("resolved", False)]
        if unresolved and overall == CLEAR_VALUE:
            warnings.append(
                f"Has {len(unresolved)} unresolved flag(s) but overall_status is CLEAR"
            )

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
    is_valid, errors, warnings = validate_background_check(raw, ctx)

    checks_total = 5
    checks_present = sum(1 for c in REQUIRED_CHECKS if c in raw.get("checks", {}))

    audit_data = {
        "event_type": "stage_6_background_check_validation",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "is_valid": is_valid,
        "checks_present": checks_present,
        "overall_status": raw.get("overall_status", "unknown"),
        "error_count": len(errors),
        "is_contractor": raw.get("contractor", False),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Background check validated ({checks_present}/{checks_total} checks present)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Background check validation FAILED ({checks_present}/{checks_total} checks present):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
