#!/usr/bin/env python
"""
stage-7-validate-offer-generation.py
P1 Hook: PostToolUse → Offer Generation Validation (Stage 7)
============================================================================
Trigger: After offer package is generated.

Validates:
  1. Base salary within compensation band [min, max]
  2. All required offer fields present
  3. Multi-candidate handling (only one active offer per role)
  4. Offer status is valid

Exit: 0 = offer valid, 2 = offer invalid
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact
from lib.validators import check_required, validate_artifact_file


def validate_offer(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read offer artifact
    offer_path = ctx.artifact_path("stage7-offer.md")
    artifact_data = {}
    if offer_path:
        exists, _ = validate_artifact_file(offer_path)
        if exists:
            result = parse_artifact(offer_path)
            artifact_data = result.data

    # Merge stdin data with artifact data
    offer_raw = raw.get("offer", artifact_data.get("offer", {}))
    band_ref = raw.get("compensation_band", artifact_data.get("compensation_band_reference", {}))
    status = raw.get("status", artifact_data.get("status", "extended"))

    # 1. Required fields
    if not offer_raw.get("base_salary"):
        errors.append("offer.base_salary is required")
    if not offer_raw.get("start_date"):
        errors.append("offer.start_date is required")

    # 2. Compensation band compliance
    base = offer_raw.get("base_salary", 0)
    band_min = band_ref.get("min", 0)
    band_max = band_ref.get("max", 0)

    if band_min > 0 and band_max > 0:
        if base < band_min:
            errors.append(f"Base salary ${base:,} below band minimum ${band_min:,}")
        elif base > band_max:
            errors.append(f"Base salary ${base:,} exceeds band maximum ${band_max:,}")

    # 3. Offer status validation
    valid_statuses = ["extended", "accepted", "declined", "negotiating"]
    if status not in valid_statuses:
        errors.append(f"Invalid offer status: '{status}'. Must be one of: {valid_statuses}")

    # 4. Check for multi-candidate conflicts
    open_offers = os.path.join(ctx.entity_root, "data", "open-offers.json")
    if os.path.exists(open_offers):
        try:
            with open(open_offers, "r") as f:
                offers = json.load(f)
                role_id = raw.get("role_id", ctx.role_id or "")
                active = [o for o in offers
                          if o.get("role_id") == role_id
                          and o.get("status") in ("extended", "negotiating")
                          and o.get("candidate_id") != ctx.candidate_id]
                if active:
                    warnings.append(f"Active offer exists for role {role_id}: candidate {active[0].get('candidate_id')}")
        except (json.JSONDecodeError, IOError):
            pass

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
    is_valid, errors, warnings = validate_offer(raw, ctx)

    audit_data = {
        "event_type": "stage_7_offer_validation",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "is_valid": is_valid,
        "error_count": len(errors),
        "within_band": raw.get("within_band", True),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Offer validation passed", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Offer validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
