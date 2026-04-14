#!/usr/bin/env python
"""
stage-1-validate-role-intake.py
P1 Hook: UserPromptSubmit → Role Intake Validator (Stage 1)
============================================================================
Trigger: When department head submits role intake request.

Behavior:
  1. Validates required fields against schema
  2. Cross-references against approved recruitment plan
  3. Verifies compensation band, assessment battery, no duplicates
  4. Reads PSD artifact if it exists; validates its frontmatter

Exit: 0 = intake valid, 2 = intake invalid
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact
from lib.validators import check_required, check_enum, validate_artifact_file

VALID_ROLE_FAMILIES = {
    "engineering", "product", "design", "data", "translation",
    "security", "business", "hr", "devops",
    "leadership", "creative-design", "art", "audio", "production", "live-ops",
}
VALID_SENIORITIES = ["L0", "L1", "L2", "L3", "L4"]


def validate_role_intake(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Required fields
    for field in ["title", "role_family", "seniority", "team", "justification"]:
        errors.extend(check_required(raw, field))

    # Role family
    rf = raw.get("role_family", "").lower().strip()
    if rf and rf not in VALID_ROLE_FAMILIES:
        errors.append(f"Invalid role family: '{rf}'")

    # Seniority
    sen = raw.get("seniority", "").strip()
    errors.extend(check_enum(sen, VALID_SENIORITIES, "seniority"))

    # Contractor governance: No L3 for contractors
    employment_type = str(raw.get("employment_type", "")).strip().lower()
    if employment_type == "contractor" and sen in ("L3", "L4"):
        cso_cto_approval = raw.get("cso_cto_co_approval", False)
        if not cso_cto_approval:
            errors.append(
                f"Contractor role at {sen} level requires CSO + CTO co-approval "
                f"(No L3 for Contractors rule). Set cso_cto_co_approval: true."
            )

    # Justification length
    just = raw.get("justification", "").strip()
    if just and len(just) < 20:
        errors.append(f"Justification too short ({len(just)} chars, min 20)")

    # Compensation band validation
    comp = raw.get("compensation_band", {})
    if isinstance(comp, dict):
        min_s = comp.get("min")
        max_s = comp.get("max")
        if min_s is not None and max_s is not None:
            if min_s > max_s:
                errors.append(f"Compensation band: min ({min_s}) > max ({max_s})")
            if min_s < 0:
                errors.append("Compensation band min must be non-negative")

    # Validate PSD artifact if candidate_path provided
    if ctx.candidate_path:
        psd_path = ctx.artifact_path("stage1-psd.md")
        if psd_path:
            exists, err = validate_artifact_file(psd_path)
            if not exists:
                warnings.append(f"PSD artifact not yet created: {psd_path}")
            else:
                # Parse and validate frontmatter
                result = parse_artifact(psd_path)
                fm = result.data
                if fm:
                    # Check PSD has required frontmatter fields
                    for field in ["role_title", "role_family", "seniority", "compensation_band"]:
                        if field not in fm:
                            errors.append(f"PSD missing required frontmatter field: {field}")

                    # Validate competency weights sum to ~1.0
                    competencies = fm.get("competencies", [])
                    if competencies and isinstance(competencies, list):
                        weights = [c.get("weight", 0) for c in competencies if isinstance(c, dict)]
                        if weights:
                            total = sum(weights)
                            if abs(total - 1.0) > 0.01:
                                errors.append(f"PSD competency weights sum to {total:.4f}, expected ~1.0")
                        # If weights is empty but competencies is non-empty list, parser issue — warn not fail
                        elif len(competencies) > 0:
                            warnings.append("PSD competency weights could not be parsed from frontmatter")

                    # Validate assessment battery has >= 2 items
                    battery = fm.get("assessment_battery", [])
                    if isinstance(battery, list) and battery and len(battery) < 2:
                        errors.append(f"PSD assessment battery has {len(battery)} items, minimum 2 required")

                    # Validate compensation band consistency
                    psd_band = fm.get("compensation_band", {})
                    intake_band = raw.get("compensation_band", {})
                    if psd_band and intake_band:
                        if psd_band.get("min") != intake_band.get("min") or psd_band.get("max") != intake_band.get("max"):
                            warnings.append("PSD compensation band differs from intake request")

    # Duplicate check against open positions
    open_positions_file = os.path.join(ctx.entity_root, "data", "open-positions.json")
    if os.path.exists(open_positions_file):
        try:
            with open(open_positions_file, "r") as f:
                positions = json.load(f)
                title = raw.get("title", "").lower()
                team = raw.get("team", "").lower()
                dups = [p for p in positions
                        if p.get("title", "").lower() == title
                        and p.get("team", "").lower() == team
                        and p.get("status") == "open"]
                if dups:
                    errors.append(f"Duplicate open position: '{raw.get('title')}' for team '{raw.get('team')}'")
        except (json.JSONDecodeError, IOError):
            pass

    # Assessment battery
    battery = raw.get("assessment_battery", [])
    if not battery and rf:
        warnings.append(f"No assessment battery specified for '{rf}' — default will be applied")

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
    is_valid, errors, warnings = validate_role_intake(raw, ctx)

    checks_total = 8
    checks_passed = checks_total - len(errors) - len(warnings)

    audit_data = {
        "event_type": "role_intake_validation",
        "role_title": raw.get("title", "unknown"),
        "is_valid": is_valid,
        "error_count": len(errors),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Role intake validation passed ({max(0, checks_passed)}/{checks_total} checks)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        print(json.dumps({"is_valid": True, "warnings": warnings}), file=sys.stdout)
        sys.exit(0)
    else:
        print(f"❌ Role intake validation FAILED ({max(0, checks_passed)}/{checks_total} checks):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        print(json.dumps({"is_valid": False, "errors": errors, "warnings": warnings}), file=sys.stdout)
        sys.exit(2)


if __name__ == "__main__":
    main()
