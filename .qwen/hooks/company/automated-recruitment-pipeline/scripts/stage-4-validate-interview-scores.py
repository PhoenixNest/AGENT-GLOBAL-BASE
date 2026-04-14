#!/usr/bin/env python
"""
stage-4-validate-interview-scores.py
P1 Hook: PostToolUse → Interview Scores Validation (Stage 4)
============================================================================
Trigger: After interview simulation completes and scores are recorded.

Validates:
  1. >= 2 assessment components present
  2. Sum of assessment weights ≈ 1.0 (±0.01)
  3. Composite score ≈ sum of weighted_scores (±0.01)
  4. Each assessment score in 0-5 range
  5. 80th percentile auto-reject enforced
  6. Bar raiser consistency (NO_HIRE with PASS is invalid)
  7. Reads interview scores artifact for structured validation

Exit: 0 = scores valid, 2 = scores invalid (auto-reject or data error)
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

PERCENTILE_THRESHOLD = 80
WEIGHT_TOLERANCE = 0.01


def validate_interview_scores(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Read interview artifact
    interview_path = ctx.artifact_path("stage4-interview-scores.md")
    artifact_data = {}
    if interview_path:
        exists, _ = validate_artifact_file(interview_path)
        if exists:
            result = parse_artifact(interview_path)
            artifact_data = result.data

    # Merge stdin data with artifact data
    assessments = raw.get("assessments", artifact_data.get("assessments", []))
    composite = raw.get("composite_score", artifact_data.get("composite_score"))
    percentile = raw.get("percentile", artifact_data.get("percentile"))
    bar_raiser = raw.get("bar_raiser", artifact_data.get("bar_raiser", ""))
    result_status = raw.get("result", artifact_data.get("result", ""))

    # 1. >= 2 assessment components
    if not assessments or len(assessments) < 2:
        errors.append(f"Need >= 2 assessment components, got {len(assessments) if assessments else 0}")

    # 2. Weight sum ≈ 1.0
    if assessments:
        weights = []
        weighted_scores = []
        for i, a in enumerate(assessments):
            score = a.get("score")
            weight = a.get("weight")
            ws = a.get("weighted_score")

            # 4. Each score in 0-5
            if score is not None:
                try:
                    s = float(score)
                    if s < 0 or s > 5:
                        errors.append(f"Assessment {i} score {s} out of range [0, 5]")
                    weights.append(float(weight) if weight is not None else 0)
                    weighted_scores.append(float(ws) if ws is not None else 0)
                except (TypeError, ValueError):
                    errors.append(f"Assessment {i} has non-numeric score/weight")
            elif weight is not None:
                weights.append(float(weight))
                weighted_scores.append(0)  # Unscored assessment contributes 0

        if weights:
            total_weight = sum(weights)
            if abs(total_weight - 1.0) > WEIGHT_TOLERANCE:
                errors.append(f"Weight sum = {total_weight:.4f}, expected 1.0 ± {WEIGHT_TOLERANCE}")

        # 3. Composite ≈ sum of weighted scores
        if composite is not None and weighted_scores:
            expected_composite = sum(weighted_scores)
            if abs(float(composite) - expected_composite) > WEIGHT_TOLERANCE:
                errors.append(
                    f"Composite score {composite} ≠ sum of weighted scores {expected_composite:.4f}"
                )

    # 5. 80th percentile auto-reject
    if percentile is not None and result_status:
        if result_status == "PASS" and percentile < PERCENTILE_THRESHOLD:
            errors.append(
                f"Candidate PASS at {percentile}th percentile (threshold: {PERCENTILE_THRESHOLD})"
            )
        if result_status == "AUTO_REJECT" and percentile >= PERCENTILE_THRESHOLD:
            errors.append(
                f"Candidate AUTO_REJECT at {percentile}th percentile (above threshold)"
            )

    # 6. Bar raiser consistency
    if bar_raiser and result_status:
        if bar_raiser.upper() == "NO_HIRE" and result_status == "PASS":
            errors.append("Bar raiser is NO_HIRE but result is PASS — inconsistent")

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
    is_valid, errors, warnings = validate_interview_scores(raw, ctx)

    checks_total = 6
    checks_passed = checks_total - len(errors) - len(warnings)

    audit_data = {
        "event_type": "stage_4_interview_scores_validation",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "is_valid": is_valid,
        "error_count": len(errors),
        "composite_score": raw.get("composite_score"),
        "percentile": raw.get("percentile"),
        "assessments_count": len(raw.get("assessments", [])),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Interview scores validated ({max(0, checks_passed)}/{checks_total} checks)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Interview scores validation FAILED ({max(0, checks_passed)}/{checks_total} checks):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
