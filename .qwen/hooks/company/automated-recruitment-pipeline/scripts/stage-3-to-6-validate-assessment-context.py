#!/usr/bin/env python
"""
stage-3-to-6-validate-assessment-context.py
P1 Hook: PreToolUse → Assessment Integrity Pre-flight (Stages 3–6)
============================================================================
Trigger: Before any assessment execution.

6-Check Pre-flight:
  1. Candidate ID present and non-empty
  2. Role family matches assessment battery
  3. Sandbox/environment ID provided
  4. Rule version (quarter) specified
  5. Assessment type valid for role family
  6. No prior assessment already recorded (prevent re-scoring)

Exit: 0 = context valid, 2 = context invalid (block assessment)
============================================================================
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.validators import check_required, validate_artifact_file

VALID_ASSESSMENT_TYPES = {
    "engineering": ["coding-challenge", "system-design", "technical-interview",
                     "behavioral-interview", "code-review-exercise"],
    "product": ["product-case-study", "product-sense-interview",
                 "metrics-reasoning", "behavioral-interview"],
    "design": ["portfolio-review", "design-challenge-phase1",
               "design-challenge-phase2", "design-challenge-phase3",
               "design-critique-interview"],
    "art": ["portfolio-review", "environment-challenge", "panel-interview",
            "behavioral-interview", "technical-assessment"],
    "audio": ["portfolio-review", "audio-challenge", "panel-interview",
              "behavioral-interview"],
    "leadership": ["leadership-case-study", "strategic-interview",
                    "behavioral-interview"],
    "production": ["production-case-study", "process-interview",
                    "behavioral-interview"],
    "live-ops": ["liveops-case-study", "analytics-interview",
                  "behavioral-interview"],
    "data": ["statistical-reasoning", "ml-system-design", "data-pipeline-challenge"],
    "translation": ["translation-quality-test", "localization-engineering",
                     "style-guide-compliance"],
    "security": ["owasp-masvs-exam", "threat-modeling",
                  "vulnerability-identification", "incident-response"],
    "business": ["case-study-analysis", "financial-modeling", "strategic-reasoning"],
}


def validate_assessment_context(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    # Check 1: Candidate ID
    cid = raw.get("candidate_id", "") or ctx.candidate_id
    if not cid:
        errors.append("Candidate ID is required")

    # Check 2: Role family
    rf = raw.get("role_family", "").lower().strip()
    if not rf:
        errors.append("Role family is required")

    # Check 3: Sandbox/environment
    sandbox = raw.get("sandbox_id", "")
    if not sandbox:
        warnings.append("No sandbox_id provided — assessment may use shared environment")

    # Check 4: Rule version
    rule_ver = raw.get("rule_version", "")
    if not rule_ver:
        warnings.append("No rule_version (quarter) specified — using current config")

    # Check 5: Assessment type valid for role family
    atype = raw.get("assessment_type", "")
    if rf and atype:
        valid_types = VALID_ASSESSMENT_TYPES.get(rf, [])
        if valid_types and atype not in valid_types:
            errors.append(f"Assessment type '{atype}' not valid for role family '{rf}'. Valid: {valid_types}")

    # Check 6: No prior assessment (check for existing artifact)
    # Only applicable to scoring stages (4-5); stages 3 and 6 have no scoring artifacts
    stage = raw.get("stage", "")
    if ctx.candidate_path and atype and stage in ("stage-4", "stage-5"):
        # Check if interview scores artifact already exists
        interview_path = ctx.artifact_path("stage4-interview-scores.md")
        if interview_path:
            exists, _ = validate_artifact_file(interview_path)
            if exists:
                warnings.append(f"Prior assessment artifact exists: {interview_path} — re-scoring detected")

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
    is_valid, errors, warnings = validate_assessment_context(raw, ctx)

    checks_total = 6
    checks_passed = checks_total - len(errors) - len(warnings)

    audit_data = {
        "event_type": "assessment_context_validation",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "assessment_type": raw.get("assessment_type", "unknown"),
        "is_valid": is_valid,
        "error_count": len(errors),
        "checks_total": checks_total,
        "checks_passed": max(0, checks_passed),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Assessment context validated ({max(0, checks_passed)}/{checks_total} checks)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Assessment context validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
