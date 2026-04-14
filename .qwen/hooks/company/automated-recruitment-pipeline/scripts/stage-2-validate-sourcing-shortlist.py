#!/usr/bin/env python
"""
stage-2-validate-sourcing-shortlist.py
P2 Hook: PostToolUse → Sourcing Shortlist Validation (Stage 2)
============================================================================
Trigger: After sourcing aggregation completes.

Validates:
  1. Shortlist has ≤ 50 candidates (top-50 constraint)
  2. Dedup index integrity (unique_after_dedup ≤ total_raw)
  3. Each candidate has complete profile (name, email, experience, skills)
  4. Sourcing scores are in valid range (0-100)
  5. No duplicate emails in shortlist
  6. Sourcing channels used ≥ 1
  7. Reads sourcing results artifact for structured validation

Exit: 0 = shortlist valid, 2 = shortlist invalid
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

MAX_SHORTLIST = 50


def validate_sourcing_shortlist(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read sourcing artifact
    sourcing_path = ctx.artifact_path("stage2-sourcing-shortlist.md")
    artifact_data = {}
    if sourcing_path:
        exists, _ = validate_artifact_file(sourcing_path)
        if exists:
            result = parse_artifact(sourcing_path)
            artifact_data = result.data

    # Merge stdin with artifact data
    total_raw = raw.get("total_raw", artifact_data.get("total_raw", 0))
    unique_after_dedup = raw.get("unique_after_dedup", artifact_data.get("unique_after_dedup", 0))
    shortlist = raw.get("shortlist", artifact_data.get("shortlist", []))
    channels = raw.get("channels_used", artifact_data.get("channels_used", []))

    # 1. Shortlist ≤ 50
    shortlist_count = len(shortlist) if shortlist else (raw.get("shortlist_count", 0))
    if shortlist_count > MAX_SHORTLIST:
        errors.append(f"Shortlist has {shortlist_count} candidates (max {MAX_SHORTLIST})")

    # 2. Dedup integrity
    if total_raw > 0 and unique_after_dedup > total_raw:
        errors.append(f"unique_after_dedup ({unique_after_dedup}) > total_raw ({total_raw})")

    if shortlist_count > 0 and unique_after_dedup > 0 and shortlist_count > unique_after_dedup:
        warnings.append(f"Shortlist count ({shortlist_count}) > unique_after_dedup ({unique_after_dedup})")

    # 3. Candidate profile completeness
    if shortlist:
        for i, c in enumerate(shortlist):
            missing = []
            for field in ["full_name", "email", "experience_years", "skills"]:
                if not c.get(field):
                    missing.append(field)
            if missing:
                errors.append(f"Candidate {i+1} ({c.get('candidate_id', '?')}) missing: {missing}")

            # 4. Sourcing score in range
            score = c.get("sourcing_score")
            if score is not None:
                try:
                    s = float(score)
                    if s < 0 or s > 100:
                        errors.append(f"Candidate {i} sourcing_score {s} out of range [0, 100]")
                except (TypeError, ValueError):
                    errors.append(f"Candidate {i} has non-numeric sourcing_score")

            # 5. No duplicate emails
            # (checked separately below)

    # 5. Duplicate email check
    if shortlist:
        emails = [c.get("email", "").lower() for c in shortlist if c.get("email")]
        seen = set()
        for email in emails:
            if email in seen:
                errors.append(f"Duplicate email in shortlist: {email}")
            seen.add(email)

    # 6. At least 1 sourcing channel
    channel_count = len(channels) if isinstance(channels, list) else 0
    if channel_count < 1:
        errors.append("No sourcing channels specified")

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
    is_valid, errors, warnings = validate_sourcing_shortlist(raw, ctx)

    checks_total = 6
    checks_passed = checks_total - len(errors) - len(warnings)

    audit_data = {
        "event_type": "stage_2_sourcing_shortlist_validation",
        "role_id": ctx.role_id or raw.get("role_id", "N/A"),
        "is_valid": is_valid,
        "total_raw": raw.get("total_raw", 0),
        "unique_after_dedup": raw.get("unique_after_dedup", 0),
        "shortlist_count": len(raw.get("shortlist", [])),
        "error_count": len(errors),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Sourcing shortlist validated ({max(0, checks_passed)}/{checks_total} checks)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Sourcing shortlist validation FAILED ({max(0, checks_passed)}/{checks_total} checks):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
