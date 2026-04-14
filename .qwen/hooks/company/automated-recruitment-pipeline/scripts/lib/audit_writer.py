"""
audit_writer.py — SHA-256 chained immutable audit trail.

Writes audit entries to the entity-specific audit log (NOT to .qwen/).
Each entry is chained to the previous entry's hash for tamper detection.
Uses file locking to prevent chain corruption under concurrent writes.

Usage:
    from lib.audit_writer import append_audit_log

    entry = append_audit_log(ctx, {
        "event_type": "stage_5_vetting_gate",
        "candidate_id": "G24",
        "result": "PASS",
        ...
    })
"""

import json
import hashlib
import os
from datetime import datetime, timezone


# Cross-platform file locking
try:
    import msvcrt  # Windows
    _HAS_LOCK = True

    def _lock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

    def _unlock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
except ImportError:
    try:
        import fcntl  # Unix
        _HAS_LOCK = True

        def _lock_file(f):
            fcntl.flock(f, fcntl.LOCK_EX)

        def _unlock_file(f):
            fcntl.flock(f, fcntl.LOCK_UN)
    except ImportError:
        _HAS_LOCK = False

        def _lock_file(f):
            pass

        def _unlock_file(f):
            pass


def compute_entry_hash(entry: dict) -> str:
    """Compute SHA-256 hash of entry content (excluding signature fields)."""
    hashable = {k: v for k, v in entry.items()
                if k not in ("signature", "previous_hash", "entry_hash")}
    return hashlib.sha256(json.dumps(hashable, sort_keys=True).encode()).hexdigest()


def get_last_hash(audit_log_path: str) -> str:
    """Get the hash of the last audit entry for chain linkage."""
    if not os.path.exists(audit_log_path):
        return "genesis"
    try:
        with open(audit_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return "genesis"
            last_entry = json.loads(lines[-1])
            return last_entry.get("entry_hash", "genesis")
    except (json.JSONDecodeError, IOError, IndexError):
        return "genesis"


def append_audit_log(ctx, data: dict) -> dict:
    """
    Append an audit entry to the entity-specific audit log.

    Args:
        ctx: EntityContext from entity_resolver
        data: Dict with audit entry fields (event_type, candidate_id, etc.)

    Returns:
        The complete audit entry dict (with hash and signature added).
    """
    # Ensure audit directory exists
    audit_dir = ctx.audit_dir
    os.makedirs(audit_dir, exist_ok=True)
    audit_log_path = ctx.audit_path

    # Build entry with common fields
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {
        "timestamp": data.get("timestamp", now),
        "entity_type": ctx.entity_type,
        "entity_root": ctx.entity_root,
        "event_type": data.get("event_type", "unknown"),
        "stage": data.get("stage", ctx.stage or "unknown"),
        "candidate_id": data.get("candidate_id", ctx.candidate_id or "N/A"),
        "candidate_name": data.get("candidate_name", ctx.candidate_name or "N/A"),
        "role_id": data.get("role_id", ctx.role_id or "N/A"),
        "hiring_cycle_id": data.get("hiring_cycle_id", ctx.hiring_cycle_id or "N/A"),
    }

    # Merge additional data fields
    for key, value in data.items():
        if key not in entry:
            entry[key] = value

    # Chain to previous entry (with file lock to prevent race conditions)
    file_exists = os.path.exists(audit_log_path)

    if _HAS_LOCK:
        mode = "r+" if file_exists else "w"
        with open(audit_log_path, mode, encoding="utf-8") as f:
            _lock_file(f)
            try:
                if file_exists:
                    lines = f.readlines()
                    previous_hash = json.loads(lines[-1]).get("entry_hash", "genesis") if lines else "genesis"
                else:
                    previous_hash = "genesis"
                entry["previous_hash"] = previous_hash
                entry_hash = compute_entry_hash(entry)
                entry["entry_hash"] = entry_hash
                sig_input = json.dumps(entry, sort_keys=True)
                checksum = hashlib.sha256(sig_input.encode()).hexdigest()[:16]
                entry["checksum"] = f"sha256:{checksum}"
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            finally:
                _unlock_file(f)
    else:
        # No locking available — best effort
        previous_hash = get_last_hash(audit_log_path)
        entry["previous_hash"] = previous_hash
        entry_hash = compute_entry_hash(entry)
        entry["entry_hash"] = entry_hash
        sig_input = json.dumps(entry, sort_keys=True)
        checksum = hashlib.sha256(sig_input.encode()).hexdigest()[:16]
        entry["checksum"] = f"sha256:{checksum}"
        with open(audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry
