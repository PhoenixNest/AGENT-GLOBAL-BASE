# Disk-Level DR Backup Design — Phase 5, Item 2 (agent-memory Enterprise-Readiness Build)

**Parent Report:** `../research-report.md`
**Relates to:** `05-disaster-recovery-and-resilience.md` (Qdrant-outage resilience — a different
failure class, see Context below), `10-observability-fix-phase0.md` (Phase 5, item 1 — the
stale-process diagnosis addendum)
**Date:** 2026-08-08
**Authorized by:** CEO, via Dr. Elias Vance (Lab Director) — Phase 5, item 2 (scheduled DR
backups with RTO/RPO). Implementation of the four designs below is approved; **activation of
the associated logic is explicitly withheld for now** — see Activation Status.
**Executed by:** Dr. Elias Vance, directly, in a live interactive session

---

## Context

`05-disaster-recovery-and-resilience.md` already establishes a **zero-RPO guarantee against
`qdrant-memory` outages**: the JSONL log is written before any Qdrant upsert is attempted, so a
Qdrant crash or unreachability never loses data — only searchability, until resync. That argument
has one load-bearing assumption: **the JSONL log itself survives.** It says nothing about disk
failure, accidental deletion, filesystem corruption, or host loss — anything that destroys
`core-component-00/engineering/context-engineering/memory/` directly, the one thing every
Qdrant collection is rebuildable from via `QdrantMemoryIndex.rebuild_from_log()`
(`memory_vector_store.py`, acceptance-tested 2026-07-13 against real `qdrant-memory` using
disposable test collections — see `.claude/rules/mcp-governance.md`'s `agent-memory` row).

This document designs the missing layer: **backing up the JSONL log itself**, off the single copy
that `05-...md`'s guarantee depends on existing at all.

**Current data footprint** (verified directly, 2026-08-07): only `reflection/reflection-log.jsonl`
has real content (9,616 bytes, 4 records). `episodic/` exists but is empty; no `semantic.jsonl` or
`procedural.jsonl` files exist yet — consistent with `health_check`'s point counts
(episodic/semantic/procedural = 0, reflection = 4). No automated write path exists yet (Phase 2/3
of the write-capable-tool track remain blocked, per `11-write-path-threat-model-phase1.md`'s
no-go verdict) — today's write velocity is near-zero and manual. This smallness is directly
relevant to the RTO/RPO targets below: both replay time and backup storage cost are currently
negligible constraints, not engineering problems to solve for.

**Correction carried into this design:** an earlier reference in this Programme's own discussion
loosely cited this workspace's `CronCreate` tool as a candidate scheduler. Checked directly against
its actual contract before designing anything on top of it: `CronCreate` is **session-scoped**
in-memory state — it dies when the authoring Claude session ends, auto-expires after 7 days, and
only fires while the REPL is idle. That is unusable for a DR backup job, which must run
independently of any chat session. This design uses **Windows Task Scheduler** instead (§2).

---

## 1. Proposed Recovery Objectives

| Objective                                | Target         | Justification                                                                                                                                                                                                               |
| ---------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RPO** (max acceptable data loss)       | **24 hours**   | No automated write path exists today; write velocity is near-zero and manual. A daily snapshot is generous relative to actual change rate. Revisit once Phase 3 (automatic capture) ships and write frequency rises.        |
| **RTO** (max acceptable time to restore) | **15 minutes** | At current volume (~10 KB), `rebuild_from_log()` replay is sub-second (consistent with its 2026-07-13 acceptance test). RTO is dominated by a human noticing the failure and running the restore command, not compute time. |

These are distinct from — and additive to — `05-disaster-recovery-and-resilience.md` §6's
zero-RPO/immediate-RTO objectives, which cover Qdrant-outage-with-JSONL-intact. This design's
objectives cover the case where the JSONL log itself is the thing that was lost.

---

## 2. The Four Design Components

### 2.1 Backup mechanism — `mcp-servers/agent-memory/scripts/backup_memory_log.py`

Copies `core-component-00/engineering/context-engineering/memory/` (the `JSONLMemoryLog` root —
already the durable source of truth by design; Qdrant itself is fully disposable/rebuildable from
it) into a dated, timestamped snapshot directory under
`mcp-servers/agent-memory/backups/snapshots/<UTC timestamp>/`. Plain `shutil.copytree` — no
external dependency, no network call, nothing that can itself become a new failure mode.

### 2.2 Scheduler — `mcp-servers/agent-memory/scripts/register_backup_task.ps1`

Registers a Windows Task Scheduler job (`New-ScheduledTaskAction` / `-Trigger Daily` /
`Register-ScheduledTask`) that runs `backup_memory_log.py` daily at 03:00 using the shared
`mcp-servers/.venv/Scripts/python.exe` interpreter (the same shared venv every other CC-00 MCP
process uses — see `.claude/rules/mcp-governance.md`'s Python Environment note). Chosen over
`CronCreate` for the reason in Context above: Task Scheduler jobs are OS-level, durable across
reboots, and independent of any Claude session.

**Safety property, not just a documentation note:** the script defaults to a dry run. Running it
with no arguments prints the task definition it _would_ register and registers nothing. Only
`-Activate` performs the actual `Register-ScheduledTask` call. This means the script is safe to
have on disk — running it by accident does not wire anything in.

### 2.3 Restore verification — `mcp-servers/agent-memory/scripts/verify_backup_restore.py`

A backup nobody has restored isn't a verified backup. This script takes the most recent snapshot,
replays it through the same proven `QdrantMemoryIndex.rebuild_from_log()` path used for
production recovery, but into a disposable, uniquely-suffixed test collection per memory type
(`memory_<type>__dr_verify_test` — never the production `memory_*` collections), then compares
the replayed count against the record count read directly from the snapshot's own JSONL files.
Every test collection is dropped afterward regardless of outcome. Mirrors the pattern already
proven in Phase 0's acceptance testing (disposable test collections, never touching production
data) and in `test_memory_vector_store.py`'s own `rebuild_from_log` unit tests.

Exits `0` and prints `OK` when every memory type's replayed count matches its JSONL record count;
exits `1` naming the first mismatch otherwise — a design that fails loudly rather than reporting
"backup exists" without ever confirming it's usable.

### 2.4 Retention policy

Embedded as a parameter of the backup script rather than a separate component: `--retain 14`
(default). After each snapshot, `prune_old_snapshots()` keeps the 14 most recent
timestamp-named snapshot directories and deletes the rest. At current data volume, storage cost
is not a meaningful constraint — 14 days gives two weeks of rollback room, revisit if/when write
volume grows materially (Phase 3+).

---

## 3. Activation Status — Explicitly Inactive

| Component              | File                                 | State                                                                                                                                                                                                                                                                    |
| ---------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Backup mechanism       | `backup_memory_log.py`               | Implemented. Not scheduled, not invoked by any running process. Only runs if executed by hand.                                                                                                                                                                           |
| Scheduler registration | `register_backup_task.ps1`           | Implemented, **dry-run by default**. No scheduled task exists in Windows Task Scheduler as a result of writing this file. Requires an explicit future `-Activate` run, which itself requires a fresh, explicit authorization to activate — not implied by this document. |
| Restore verification   | `verify_backup_restore.py`           | Implemented. Not scheduled, not invoked by any running process, **not yet executed against a live Qdrant instance** — no snapshot exists yet for it to verify (no backup has been run).                                                                                  |
| Retention policy       | (embedded in `backup_memory_log.py`) | Implemented as inert logic — only runs when the backup script itself runs.                                                                                                                                                                                               |

No files under `core-component-00/mcp-servers/agent-memory/server.py` were touched — this build
adds new, standalone scripts only. Nothing in the running `agent-memory` MCP server's request path
is affected by any of the above; a live MCP connection behaves identically before and after this
build.

---

## 4. What Remains for a Future Activation Decision

1. Confirm the RTO/RPO targets in §1 still hold once Phase 3 (automatic capture) ships and write
   volume is no longer near-zero.
2. Decide on an off-machine/off-disk backup target (cloud storage, network share) — this design
   deliberately only specifies local-disk versioned snapshots for now; off-machine replication is
   a distinct decision this document does not make.
3. Run `register_backup_task.ps1 -Activate` only after that authorization is given explicitly —
   this document is the design input to that future decision, not the decision itself, matching
   the same pattern `11-write-path-threat-model-phase1.md` established for Phase 2 authorization.
4. Once activated, run `verify_backup_restore.py` at least once to confirm the first real snapshot
   actually restores, before relying on the schedule alone.

---

## Files Changed

- `core-component-00/mcp-servers/agent-memory/scripts/backup_memory_log.py` — new
- `core-component-00/mcp-servers/agent-memory/scripts/register_backup_task.ps1` — new
- `core-component-00/mcp-servers/agent-memory/scripts/verify_backup_restore.py` — new
- This document

---

## References

| Resource                                                                                | Location                                                                                   |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Qdrant-outage resilience (zero-RPO guarantee, different failure class)                  | `05-disaster-recovery-and-resilience.md`                                                   |
| JSONL log mechanism (`JSONLMemoryLog`, `DEFAULT_MEMORY_ROOT`)                           | `core-component-00/engineering/context-engineering/implementations/memory_vector_store.py` |
| Replay mechanism (`QdrantMemoryIndex.rebuild_from_log()`), acceptance-tested 2026-07-13 | same file; `.claude/rules/mcp-governance.md`'s `agent-memory` row                          |
| Phase 5 item 1 (stale-process diagnosis, same authorization batch)                      | `10-observability-fix-phase0.md` § Addendum                                                |
| Phase 1 write-path threat model (precedent for "design now, activate later" gating)     | `11-write-path-threat-model-phase1.md`                                                     |
| Shared Python environment convention                                                    | `.claude/rules/mcp-governance.md` § Shared Infrastructure                                  |

---

## Version History

| Version | Date       | Author                         | Changes                                                                                                                         |
| ------- | ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-08-08 | Dr. Elias Vance (live session) | Initial design: RTO/RPO proposal, four design components implemented inactive, CronCreate-vs-Task-Scheduler correction recorded |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-08
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
