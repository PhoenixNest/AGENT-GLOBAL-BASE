#!/usr/bin/env python3
"""
Disaster-recovery backup — restore verification.

STATUS: implemented, INACTIVE. Not scheduled, not invoked by any running
process, not yet executed against a live Qdrant instance. Run manually (or
via a future scheduled trigger, once activated) to confirm the latest
snapshot is actually restorable — a backup nobody has restored isn't a
verified backup.

Replays the most recent snapshot under
core-component-00/platform/model-context-protocol-servers/agent-memory/backups/snapshots/ through the
already-proven QdrantMemoryIndex.rebuild_from_log() path, into a disposable,
uniquely-suffixed test collection per memory type (never the production
memory_* collections), compares the replayed count against the record count
read straight from the snapshot's own JSONL files, then drops every test
collection it created. Read-only against the snapshot; confined to its own
throwaway collections in Qdrant — production data is never touched.

Usage:
    python verify_backup_restore.py [--qdrant-url http://localhost:6335]

Exits 0 and prints "OK" on a clean verify (every memory type's replayed count
matches its JSONL record count); exits 1 with a description of the first
mismatch/failure otherwise.
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONTEXT_ENGINEERING_ROOT = SCRIPT_DIR.parents[3] / "framework" / "02-context-engineering"
sys.path.insert(0, str(CONTEXT_ENGINEERING_ROOT))

from implementations.memory_vector_store import (  # noqa: E402
    COLLECTION_BY_TYPE,
    JSONLMemoryLog,
    QdrantMemoryIndex,
)

BACKUP_ROOT = SCRIPT_DIR.parent / "backups" / "snapshots"
TEST_COLLECTION_SUFFIX = "__dr_verify_test"


def latest_snapshot(backup_root: Path = BACKUP_ROOT) -> Path:
    if not backup_root.exists():
        raise FileNotFoundError(f"no snapshots directory found: {backup_root}")
    snapshots = sorted((p for p in backup_root.iterdir() if p.is_dir()), key=lambda p: p.name)
    if not snapshots:
        raise FileNotFoundError(f"no snapshots found under {backup_root}")
    return snapshots[-1]


def _expected_count(log: JSONLMemoryLog, memory_type: str) -> int:
    """Mirrors rebuild_from_log()'s own read dispatch, so this is a genuine
    check that every record the replay *read* was also successfully
    *upserted* — not a re-derivation of the same number."""
    if memory_type == "episodic":
        return len(log.read_all_episodic_sessions())
    if memory_type == "reflection":
        return len(log.read_all_reflections())
    return len(log.read_all(memory_type))


def verify(snapshot_dir: Path, qdrant_url: str):
    from qdrant_client import QdrantClient

    client = QdrantClient(url=qdrant_url, timeout=5)
    log = JSONLMemoryLog(root_dir=snapshot_dir)

    lines = []
    mismatches = []
    created_collections = []

    try:
        for memory_type in COLLECTION_BY_TYPE:
            index = QdrantMemoryIndex(memory_type, client=client)
            index.collection_name = COLLECTION_BY_TYPE[memory_type] + TEST_COLLECTION_SUFFIX
            created_collections.append(index.collection_name)

            expected = _expected_count(log, memory_type)
            replayed = index.rebuild_from_log(log)  # sync_state=None: never touches production bookkeeping

            status = "OK" if replayed == expected else "MISMATCH"
            lines.append(f"{memory_type}: expected {expected}, replayed {replayed} [{status}]")
            if replayed != expected:
                mismatches.append(memory_type)
    finally:
        for collection_name in created_collections:
            try:
                client.delete_collection(collection_name=collection_name)
            except Exception as exc:
                lines.append(f"WARNING: could not clean up test collection '{collection_name}': {exc}")

    return not mismatches, "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qdrant-url", default="http://localhost:6335", help="qdrant-memory URL")
    args = parser.parse_args()

    try:
        snapshot_dir = latest_snapshot()
    except FileNotFoundError as exc:
        print(f"FAILED: {exc}")
        return 1

    print(f"verifying snapshot: {snapshot_dir}")
    try:
        ok, report = verify(snapshot_dir, args.qdrant_url)
    except Exception as exc:
        print(f"FAILED: could not complete verification: {exc}")
        return 1

    print(report)
    print("OK" if ok else "FAILED: one or more memory types did not fully replay")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
