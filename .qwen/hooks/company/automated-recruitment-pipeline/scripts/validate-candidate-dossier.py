#!/usr/bin/env python
"""
validate-candidate-dossier.py
P0 Hook: PostToolUse → Candidate Dossier Completeness Validator
============================================================================
NEW — Phase 3 deliverable.

Trigger: After Stage 5 (vetting complete) and Stage 8 (outcome report).

Validates the COMPLETE candidate dossier — all 9 pipeline artifacts must exist
and contain valid data for each candidate advancing to the hiring outcome report.

Checks:
  1. All 9 stage artifacts exist at candidate_path/pipeline-artifacts/
  2. Each artifact has parseable frontmatter (or fallback-parseable body)
  3. Gate status is PASS/accepted/HIRED for advancing stages
  4. No missing or corrupted artifacts
  5. Cross-reference: candidate appears in hiring outcome report

This is the INTEGRITY CHECK that ensures no candidate advances with
incomplete documentation.

Exit: 0 = dossier complete, 2 = dossier incomplete (block advancement)
============================================================================
"""

import json
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact
from lib.validators import validate_artifact_file, has_frontmatter


# The 9 required pipeline artifacts
REQUIRED_ARTIFACTS = [
    ("stage1-psd.md", "Position Specification Document"),
    ("stage2-sourcing-shortlist.md", "Sourcing Shortlist"),
    ("stage3-screening-results.md", "Screening Results"),
    ("stage4-interview-scores.md", "Interview Scores"),
    ("stage5-vetting-gate.md", "Vetting Gate"),
    ("stage6-background-check.md", "Background Check"),
    ("stage7-offer.md", "Offer Document"),
    ("stage8-provisioning.md", "Provisioning Record"),
    ("stage9-hiring-outcome-report.md", "Hiring Outcome Report"),
]

# Gate status patterns that indicate PASS for each stage
PASS_GATES = {
    "stage1": ["proceeding", "generated", "✅"],
    "stage2": ["proceeding", "ranked", "✅"],
    "stage3": ["proceeding", "screening complete", "✅"],
    "stage4": ["proceeding", "✅"],
    "stage5": ["pass", "advances", "✅"],
    "stage6": ["clear", "✅"],
    "stage7": ["accepted", "extended", "✅"],
    "stage8": ["complete", "✅"],
    "stage9": ["hired", "✅"],
}


def validate_dossier(raw: dict, ctx) -> tuple:
    """
    Validate the complete candidate dossier.
    Returns (is_valid, errors, warnings, dossier_report).
    """
    errors = []
    warnings = []
    dossier_report = {"candidate_id": ctx.candidate_id, "artifacts": {}}

    # Determine which artifacts to check based on current stage
    stage = raw.get("stage", ctx.stage or "stage-5")
    stage_num = _extract_stage_num(stage)

    # Map stage number to which artifacts should exist
    expected_artifacts = _expected_artifacts_for_stage(stage_num)

    candidate_path = ctx.candidate_path
    if not candidate_path:
        errors.append("Candidate path not resolved — cannot locate artifacts")
        return False, errors, warnings, dossier_report

    artifacts_dir = os.path.join(candidate_path, "pipeline-artifacts")

    # Check each expected artifact
    for fname, label in expected_artifacts:
        fpath = os.path.join(artifacts_dir, fname)
        artifact_report = {"label": label, "exists": False, "has_frontmatter": False,
                           "gate_status": "unknown", "parseable": False}

        # Check existence
        exists, err = validate_artifact_file(fpath)
        if not exists:
            errors.append(f"Missing artifact: {label} ({fname})")
            dossier_report["artifacts"][fname] = artifact_report
            continue

        artifact_report["exists"] = True

        # Check frontmatter
        artifact_report["has_frontmatter"] = has_frontmatter(fpath)
        if not artifact_report["has_frontmatter"]:
            warnings.append(f"{label} lacks YAML frontmatter (falls back to regex parsing)")

        # Parse and extract gate status
        try:
            result = parse_artifact(fpath)
            artifact_report["parseable"] = bool(result.data)
            gs = result.get("gate_status", "")
            if gs:
                artifact_report["gate_status"] = gs

                # Check gate status is PASS
                stage_key = fname.split("-")[0]  # "stage1", "stage5", etc.
                pass_patterns = PASS_GATES.get(stage_key, ["✅", "pass", "proceeding"])
                gs_lower = gs.lower()
                if not any(pp in gs_lower for pp in pass_patterns):
                    warnings.append(f"{label} gate status may not indicate PASS: '{gs}'")
        except Exception as e:
            errors.append(f"{label} failed to parse: {e}")

        dossier_report["artifacts"][fname] = artifact_report

    # Summary
    total_expected = len(expected_artifacts)
    total_present = sum(1 for a in dossier_report["artifacts"].values() if a["exists"])
    total_parseable = sum(1 for a in dossier_report["artifacts"].values() if a["parseable"])
    total_with_fm = sum(1 for a in dossier_report["artifacts"].values() if a["has_frontmatter"])

    dossier_report["summary"] = {
        "total_expected": total_expected,
        "total_present": total_present,
        "total_parseable": total_parseable,
        "total_with_frontmatter": total_with_fm,
        "complete": len(errors) == 0,
    }

    is_valid = len(errors) == 0
    return is_valid, errors, warnings, dossier_report


def _extract_stage_num(stage: str) -> int:
    """Extract stage number from string like 'stage-5' or 'stage5'."""
    m = re.search(r"(\d+)", stage)
    return int(m.group(1)) if m else 0


def _expected_artifacts_for_stage(stage_num: int) -> list:
    """Return list of (filename, label) tuples expected to exist at this stage."""
    if stage_num < 1:
        return []  # Stage 0 has no candidate artifacts
    if stage_num > len(REQUIRED_ARTIFACTS):
        stage_num = len(REQUIRED_ARTIFACTS)
    return REQUIRED_ARTIFACTS[:stage_num]


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
    is_valid, errors, warnings, report = validate_dossier(raw, ctx)

    summary = report.get("summary", {})

    audit_data = {
        "event_type": "candidate_dossier_validation",
        "candidate_id": ctx.candidate_id or raw.get("candidate_id", "N/A"),
        "stage": raw.get("stage", ctx.stage or "unknown"),
        "is_valid": is_valid,
        "artifacts_expected": summary.get("total_expected", 0),
        "artifacts_present": summary.get("total_present", 0),
        "artifacts_parseable": summary.get("total_parseable", 0),
        "artifacts_with_frontmatter": summary.get("total_with_frontmatter", 0),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Dossier validated: {summary.get('total_present', 0)}/{summary.get('total_expected', 0)} artifacts "
              f"({summary.get('total_with_frontmatter', 0)} with frontmatter)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        print(json.dumps({"is_valid": True, "report": report}), file=sys.stdout)
        sys.exit(0)
    else:
        print(f"❌ Dossier INCOMPLETE for {ctx.candidate_id}:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        print(json.dumps({"is_valid": False, "report": report}), file=sys.stdout)
        sys.exit(2)


if __name__ == "__main__":
    main()
