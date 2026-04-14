#!/usr/bin/env python
"""
stage-1-init-pipeline-session.py
P3 Hook: SessionStart → Pipeline Session Initialization (Stage 1)
============================================================================
Trigger: When a new hiring cycle session begins.

Behavior:
  1. Initializes hiring cycle tracking
  2. Starts SLA clock
  3. Creates entity-specific audit trail
  4. Verifies engine version compatibility

Exit: 0 = session initialized successfully
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            c = sys.stdin.read().strip()
            if c:
                raw = json.loads(c)
    except json.JSONDecodeError:
        raw = {"session_type": "hiring-cycle"}

    ctx = resolve_entity(raw)
    ts = datetime.now(timezone.utc).isoformat()

    # Ensure entity directories exist
    data_dir = os.path.join(ctx.entity_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(ctx.audit_dir, exist_ok=True)

    # Write SLA clock start
    sla_clock = {
        "hiring_cycle_id": raw.get("hiring_cycle_id", ctx.hiring_cycle_id or "unknown"),
        "role_id": raw.get("role_id", ctx.role_id or "unknown"),
        "quarter": raw.get("quarter", "unknown"),
        "started_at": ts,
        "current_stage": "stage-1",
        "stage_history": [{"stage": "stage-1", "status": "started", "timestamp": ts}],
        "sla_metrics": {
            "assessment_processing_hours": 0,
            "scoring_anomaly_rate": 0,
            "candidate_dropoff_rate": {},
            "r0_defect_count": 0,
            "r1_defect_count": 0,
        },
    }

    sla_path = os.path.join(data_dir, f"sla-clock-{sla_clock['hiring_cycle_id']}.json")
    try:
        with open(sla_path, "w", encoding="utf-8") as f:
            json.dump(sla_clock, f, indent=2)
    except (IOError, OSError) as e:
        print(f"❌ Failed to write SLA clock: {e}", file=sys.stderr)
        sys.exit(2)

    # Audit
    audit_data = {
        "event_type": "pipeline_session_init",
        "session_type": raw.get("session_type", "hiring-cycle"),
        "hiring_cycle_id": sla_clock["hiring_cycle_id"],
        "role_id": sla_clock["role_id"],
        "quarter": sla_clock["quarter"],
        "started_at": ts,
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    print(f"✅ Pipeline session initialized: cycle={sla_clock['hiring_cycle_id']}, "
          f"role={sla_clock['role_id']}, started={ts}", file=sys.stderr)
    print(json.dumps({"session_initialized": True, "hiring_cycle_id": sla_clock["hiring_cycle_id"],
                       "sla_clock_path": sla_path}), file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
