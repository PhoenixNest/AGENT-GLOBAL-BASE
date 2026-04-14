#!/usr/bin/env python
"""
stage-2-init-sourcing-agent.py
P3 Hook: SubagentStart → Sourcing Agent Initialization (Stage 2)
============================================================================
Trigger: When sourcing agents are dispatched for a role.

Behavior:
  1. Initializes 7 sourcing channels
  2. Creates deduplication index
  3. Loads quarterly config for channel weights
  4. Writes sourcing config to entity data directory

Exit: 0 = sourcing agents initialized
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


DEFAULT_CHANNELS = [
    {"name": "linkedin", "quality_weight": 1.0, "budget_allocation": 0.25},
    {"name": "github", "quality_weight": 0.8, "budget_allocation": 0.15},
    {"name": "referrals", "quality_weight": 1.5, "budget_allocation": 0.20},
    {"name": "artstation", "quality_weight": 1.3, "budget_allocation": 0.10},
    {"name": "conference_speakers", "quality_weight": 1.2, "budget_allocation": 0.10},
    {"name": "alumni_networks", "quality_weight": 0.9, "budget_allocation": 0.10},
    {"name": "competitor_mapping", "quality_weight": 1.1, "budget_allocation": 0.10},
]


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
    role_id = raw.get("role_id", ctx.role_id or "unknown")
    quarter = raw.get("quarter", "unknown")

    # Ensure data directory
    data_dir = os.path.join(ctx.entity_root, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Create dedup index
    dedup = {
        "role_id": role_id,
        "quarter": quarter,
        "initialized_at": datetime.now(timezone.utc).isoformat(),
        "channels": raw.get("channels", DEFAULT_CHANNELS),
        "dedup_index": {},
        "total_raw": 0,
        "unique_after_dedup": 0,
    }
    dedup_path = os.path.join(data_dir, f"dedup-index-{role_id}.json")
    with open(dedup_path, "w") as f:
        json.dump(dedup, f, indent=2)

    # Audit
    audit_data = {
        "event_type": "stage_2_sourcing_init",
        "role_id": role_id,
        "channels_count": len(dedup["channels"]),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    print(f"✅ Sourcing agents initialized: {len(dedup['channels'])} channels, role={role_id}", file=sys.stderr)
    print(json.dumps({"sourcing_initialized": True, "role_id": role_id,
                       "channels": len(dedup["channels"]), "dedup_path": dedup_path}), file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
