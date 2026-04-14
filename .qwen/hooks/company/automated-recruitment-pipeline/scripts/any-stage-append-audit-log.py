#!/usr/bin/env python
"""
any-stage-append-audit-log.py
P0 Hook: PostToolUse → Entity-Specific Audit Trail Append
============================================================================
Trigger: After any stage completion, scoring operation, or candidate state change.

Behavior:
  1. Read stdin JSON for event context
  2. Resolve entity context (entity_root, candidate_path)
  3. Build audit entry with SHA-256 chain
  4. Append to entity-specific audit log (NOT .qwen/)
  5. Never blocks pipeline (best-effort)

Input:  stdin JSON with event context + entity_root
Output: Audit entry appended to {entity_root}/audit/audit-log.jsonl
Exit:   0 = success (always — audit append is best-effort)
============================================================================
"""

import json
import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


def main():
    # Read stdin
    raw = {}
    try:
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
            if content:
                raw = json.loads(content)
    except json.JSONDecodeError:
        raw = {"event_type": "post_tool_use", "result": "completed"}
        print("⚠️ Invalid JSON input — creating minimal audit entry", file=sys.stderr)

    # Resolve entity
    ctx = resolve_entity(raw)

    try:
        entry = append_audit_log(ctx, raw)
        print(
            f"📝 Audit: {entry['event_type']} at {entry.get('stage', '?')} "
            f"(hash: {entry['entry_hash'][:12]}...)",
            file=sys.stderr,
        )
        print(json.dumps(entry), file=sys.stdout)
        sys.exit(0)
    except Exception as e:
        print(f"⚠️ Audit append failed (non-blocking): {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
