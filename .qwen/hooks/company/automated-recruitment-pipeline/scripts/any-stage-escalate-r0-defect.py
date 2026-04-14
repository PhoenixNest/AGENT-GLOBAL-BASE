#!/usr/bin/env python
"""
any-stage-escalate-r0-defect.py
P0 Hook: PostToolUseFailure → R0/R1 Defect Escalation
============================================================================
Trigger: Any tool use failure matching assessment|background-check|offer-generation|scoring.

Behavior:
  1. Classify error as R0-R3
  2. R0/R1 → exit 2 (blocks pipeline), log to entity audit
  3. R2/R3 → exit 0 (continues), log to entity audit
  4. Write defect entry to entity-specific audit log

Exit: 0 = R2/R3 (continue), 2 = R0/R1 (block)
============================================================================
"""

import json
import sys
import os
import hashlib
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


R0_KEYWORDS = [
    "discriminat", "bias", "illegal", "compliance violation", "gdpr violation",
    "fcra violation", "data breach", "unauthorized access", "data leak",
    "pii exposure", "security breach", "regulatory violation",
]
R1_KEYWORDS = [
    "scoring error", "data corruption", "score miscalculation",
    "integrity check failed", "assessment engine", "grading failed",
    "test suite error", "sandbox failure", "artifact not found",
    "missing required field", "schema validation failed",
]
R2_KEYWORDS = ["notification delay", "scheduling conflict", "email failed"]
R3_KEYWORDS = ["formatting", "cosmetic", "metadata", "non-blocking", "warning"]


def classify(error: str) -> str:
    e = error.lower()
    if any(k in e for k in R0_KEYWORDS):
        return "R0"
    if any(k in e for k in R1_KEYWORDS):
        return "R1"
    if any(k in e for k in R2_KEYWORDS):
        return "R2"
    if any(k in e for k in R3_KEYWORDS):
        return "R3"
    return "R1"  # Default to R1 for unknown errors


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            c = sys.stdin.read().strip()
            if c:
                raw = json.loads(c)
    except json.JSONDecodeError:
        pass

    ctx = resolve_entity(raw)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    tool_name = raw.get("tool_name", "unknown")
    stage = raw.get("stage", "unknown")
    error_msg = raw.get("error", "unknown")
    candidate_id = raw.get("candidate_id", "N/A")
    severity = classify(error_msg)
    defect_id = f"DEF-{ts[:10].replace('-', '')}-{hashlib.sha256(error_msg.encode()).hexdigest()[:6]}"
    action = "pipeline_pause" if severity in ("R0", "R1") else "continue"

    # Audit
    audit_data = {
        "event_type": "defect_classification",
        "defect_id": defect_id,
        "severity": severity,
        "tool": tool_name,
        "stage": stage,
        "candidate_id": candidate_id,
        "error": error_msg,
        "action": action,
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass  # Never block on audit failure

    icons = {"R0": "🔴", "R1": "🟠", "R2": "🟡", "R3": "⚪"}
    print(f"{icons.get(severity, '⚠️')} {severity} DEFECT {defect_id}: {error_msg[:80]}", file=sys.stderr)
    if severity in ("R0", "R1"):
        print(f"   Pipeline PAUSED. CHRO escalation triggered.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"   Logged, continuing.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
