# Log Entry 05 — `register_backup_task.ps1` Retention Decision — 2026-08-14

Part of `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 3 — Execution (`core-component-00/maintenance-records/pipeline.md`), a status-only
follow-up on the same topic per the topic-boundary test (same system/resource named in the main
record: `agent-memory/scripts/register_backup_task.ps1` and its Linux/macOS counterpart).

**Trigger:** Following log entry 04, the CEO asked whether `register_backup_task.ps1` could now
be removed, since a Linux/macOS counterpart (`register_backup_task.py`) exists. Dr. Vance was
asked for a recommendation before any file change.

**State before:** Both scripts present in `agent-memory/scripts/` — `.ps1` (Windows Task
Scheduler, verified working since the original remediation) and `.py` (systemd timer / crontab,
written 2026-08-14, explicitly unverified — see log entry 04).

**Actions taken:**

1. Dr. Vance reviewed `register_backup_task.py`'s `main()`, which raises `SystemExit` and refuses
   to run at all on `sys.platform == "win32"` — the two scripts are platform-exclusive, not
   redundant implementations of the same capability.
2. Recommended against removal: deleting `.ps1` now would leave Windows — the only platform this
   workspace can currently test on — with no working DR-scheduling script, while Linux/macOS would
   gain only the unverified `.py` in its place. Net effect would be a regression in actual DR
   readiness, not a cleanup.
3. CEO agreed: keep both scripts for now; no removal.

**Verification:**

| Check performed                                                            | Result                                                                               |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Re-read `register_backup_task.py`'s platform guard                         | Confirmed: raises `SystemExit` on `win32`, directing the user to `.ps1` instead      |
| Audit of `agent-memory/README.md` and this topic's `maintenance-record.md` | No existing content claims removal was planned or pending — no stale text to correct |

**Independent-review gate (pipeline.md stage 4):** Not applicable — no file removed, no
production-touching change made.

**Outcome:** No code or script changes. `register_backup_task.ps1` and `register_backup_task.py`
both remain in place. This entry records the decision and its rationale so it isn't re-litigated
without the platform-exclusivity context surfacing again.

**Handoff to next stage:** Close for this entry. Removing `.ps1` becomes a like-for-like swap only
once `register_backup_task.py` is confirmed working for real on Linux and/or macOS — tracked as
Open Follow-Up Item 3 on the main record, unchanged by this decision.
