#!/usr/bin/env python3
"""
Disaster-recovery backup — snapshot the JSONL memory log.

STATUS: implemented, INACTIVE. Nothing calls this script automatically — no
scheduled task, no server code path invokes it. It only runs if someone runs
it by hand or `register_backup_task.ps1 -Activate` has been run to wire it
into Windows Task Scheduler. See:
core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/02-deployment-guidelines.md
§9

Copies core-component-00/framework/02-context-engineering/memory/ (the
JSONLMemoryLog root — the durable source of truth every Qdrant collection is
rebuilt from via QdrantMemoryIndex.rebuild_from_log()) into a dated snapshot
directory, then prunes snapshots beyond the retention count.

Usage:
    python backup_memory_log.py [--retain N]
"""

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MEMORY_ROOT = SCRIPT_DIR.parents[3] / "framework" / "02-context-engineering" / "memory"
BACKUP_ROOT = SCRIPT_DIR.parent / "backups" / "snapshots"
DEFAULT_RETAIN = 14


def create_snapshot(memory_root: Path = MEMORY_ROOT, backup_root: Path = BACKUP_ROOT) -> Path:
    if not memory_root.exists():
        raise FileNotFoundError(f"memory log root not found: {memory_root}")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = backup_root / timestamp
    shutil.copytree(memory_root, dest)
    return dest


def prune_old_snapshots(backup_root: Path = BACKUP_ROOT, retain: int = DEFAULT_RETAIN) -> list:
    if not backup_root.exists():
        return []
    snapshots = sorted((p for p in backup_root.iterdir() if p.is_dir()), key=lambda p: p.name)
    stale = snapshots[:-retain] if retain > 0 else snapshots
    for path in stale:
        shutil.rmtree(path)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--retain",
        type=int,
        default=DEFAULT_RETAIN,
        help=f"Number of daily snapshots to keep (default: {DEFAULT_RETAIN})",
    )
    args = parser.parse_args()

    dest = create_snapshot()
    print(f"snapshot written: {dest}")

    removed = prune_old_snapshots(retain=args.retain)
    for path in removed:
        print(f"pruned stale snapshot: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
