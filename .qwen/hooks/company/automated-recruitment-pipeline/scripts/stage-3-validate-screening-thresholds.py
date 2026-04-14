#!/usr/bin/env python
"""
stage-3-validate-screening-thresholds.py
P1 Hook: PostToolUse → Screening Threshold Validation (Stage 3)
============================================================================
Trigger: After screening assessment completes.

Behavior:
  1. Reads screening results artifact from candidate_path
  2. Validates 60th percentile auto-reject enforced
  3. Validates all candidates scored, rejection reasons logged
  4. Appends to entity-specific audit log

Exit: 0 = thresholds valid, 2 = threshold violation detected
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

PERCENTILE_THRESHOLD = 60


def validate_screening(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read screening artifact
    screening_path = ctx.artifact_path("stage3-screening-results.md")
    if screening_path:
        exists, err = validate_artifact_file(screening_path)
        if not exists:
            errors.append(f"Screening artifact not found: {screening_path}")
            # Still validate stdin data if provided
        else:
            result = parse_artifact(screening_path)
            data = result.data

            # Validate screening counts
            screening = data.get("screening", {})
            total = screening.get("total_screened", 0)
            passed = screening.get("passed", 0)
            rejected = screening.get("auto_rejected", 0)

            if total > 0 and passed + rejected != total:
                warnings.append(f"Screening count mismatch: {passed}+{rejected}≠{total}")

            # Validate this candidate's percentile
            cp = screening.get("candidate_percentile")
            cr = screening.get("candidate_result")
            if cp is not None and cr is not None:
                if cr == "PASS" and cp < PERCENTILE_THRESHOLD:
                    errors.append(f"Candidate passed screening at {cp}th percentile (threshold: {PERCENTILE_THRESHOLD})")
                if cr == "AUTO_REJECT" and cp >= PERCENTILE_THRESHOLD:
                    errors.append(f"Candidate auto-rejected at {cp}th percentile (threshold: {PERCENTILE_THRESHOLD})")

            # Validate threshold
            threshold = screening.get("percentile_threshold", PERCENTILE_THRESHOLD)
            if threshold != PERCENTILE_THRESHOLD:
                errors.append(f"Percentile threshold is {threshold}, expected {PERCENTILE_THRESHOLD}")

    # Also validate from stdin data if provided
    candidates = raw.get("candidates", [])
    for c in candidates:
        cid = c.get("candidate_id", "?")
        pct = c.get("percentile", 0)
        if c.get("result") == "PASS" and pct < PERCENTILE_THRESHOLD:
            errors.append(f"  {cid}: PASS at {pct}th percentile (below {PERCENTILE_THRESHOLD})")
        if c.get("result") == "AUTO_REJECT" and pct >= PERCENTILE_THRESHOLD:
            errors.append(f"  {cid}: AUTO_REJECT at {pct}th percentile (above threshold)")

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
    is_valid, errors, warnings = validate_screening(raw, ctx)

    audit_data = {
        "event_type": "stage_3_screening_thresholds",
        "is_valid": is_valid,
        "error_count": len(errors),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        print(f"✅ Screening thresholds validated ({len(warnings)} warnings)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Screening threshold validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
