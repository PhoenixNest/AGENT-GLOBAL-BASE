# Log Entry 04 — Linux/macOS DR-Scheduling Script — 2026-08-14

Part of `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 3 — Execution (`core-component-00/maintenance-records/pipeline.md`), following the
plan approved at stage 2 below. Same topic per the topic-boundary test in `pipeline.md`: same
system/resource (`register_backup_task.ps1`'s Linux/macOS gap, named in the main record's System /
resource affected field) and a direct follow-up to Discovery item 4 / Remediation item 4.

**Trigger:** The CEO reviewed this topic's Discovery finding 4 (`register_backup_task.ps1`'s
Linux/macOS gap, deferred at Remediation as "not urgent while inactive") and asked why it should
stay deferred rather than migrated now. Dr. Vance gave an honest assessment: the script isn't a
like-for-like port (Windows Task Scheduler has no direct Linux/macOS equivalent — it requires a
new implementation, not a swap), and it can't be tested from this Windows-only machine — the same
kind of unverified-environment risk that caused the `.mcp.json` incident in log entry 03.
Recommended writing it now but explicitly flagged as unverified rather than either silently
shipping it as if tested or leaving the gap open indefinitely. **Approval (pipeline stage 2):**
CEO approved this path — "Write it now, flagged as unverified."

**State before:** `register_backup_task.ps1` (Windows Task Scheduler) was the only scheduling
registration script. No Linux/macOS equivalent existed. `agent-memory/README.md` documented this
as an intentional, undocumented-until-needed gap.

**Actions taken:**

1. Read `register_backup_task.ps1` and `backup_memory_log.py` in full to mirror the original's
   safety pattern exactly: dry-run by default, an explicit activation flag required, same task
   name/time defaults, same "CEO approval to write is not approval to activate" framing.
2. Wrote `core-component-00/mcp-servers/agent-memory/scripts/register_backup_task.py` — a Python
   CLI supporting two mechanisms: a systemd `--user` service+timer pair (Linux, preferred) or a
   crontab entry (Linux/macOS fallback), with `--mechanism auto` detecting which is available via
   `systemctl --user status`. `--activate` is required to actually register anything; omitting it
   prints the unit files / crontab line and exits. macOS's proper native mechanism (launchd) is
   explicitly **not** implemented — the cron fallback covers macOS only nominally, and modern
   macOS's TCC/Full-Disk-Access restrictions on cron are called out in the script's own docstring
   rather than glossed over.
3. Marked the script UNVERIFIED in three places: the module docstring, a runtime banner printed
   on every invocation (dry-run or not), and this log entry — so the flag survives even if someone
   reads only one of the three.
4. Updated `agent-memory/README.md`'s scripts table and folder tree to list the new script
   alongside the same unverified caveat, and corrected the prior "must be written first" framing
   (which implied ongoing deferral) to reflect that it now exists but is untested.

**Verification:**

| Check performed                                                                                                                                               | Result                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python -m py_compile register_backup_task.py`                                                                                                                | Passed — no syntax errors                                                                                                                           |
| Direct call of `_parse_time`, `_systemd_units`, `_register_systemd(..., activate=False)`, `_register_cron(..., activate=False)` via `importlib`, from Windows | Executed without error; produced well-formed systemd unit text and a syntactically correct crontab line — confirms the Python logic itself is sound |
| Real `systemctl --user` timer registration on Linux                                                                                                           | **Not performed — no Linux machine available**                                                                                                      |
| Real `crontab -l` / `crontab -` round-trip on Linux or macOS                                                                                                  | **Not performed — no non-Windows machine available**                                                                                                |
| Confirmation the resulting timer/cron entry actually fires `backup_memory_log.py` at the scheduled time                                                       | **Not performed**                                                                                                                                   |

**Independent-review gate (pipeline.md stage 4):** this change does not touch a shared production
resource other sessions currently depend on — the DR-backup path remains INACTIVE, so the
independent-review gate does not apply as a hard blocker here. Recorded anyway for completeness: no
reviewer other than the author has looked at this yet; flagged as a natural task for whoever next
has Linux/macOS access.

**Outcome:** The Linux/macOS scheduling gap now has a written implementation instead of a
documented absence, closing the "isn't written yet" half of the original finding — but the harder
half (does it actually work) remains genuinely open. This is not a stealth downgrade of rigor: the
script is explicitly labeled unverified everywhere a reader would encounter it, per the same
honesty discipline already applied to the `agent-memory/server.py` and `manage_embedder_service.py`
ports' own Linux/macOS status.

**Handoff to next stage:** Close for this session — no further action possible without a
non-Windows machine. Carries forward as an open follow-up item on the main record: verify
`register_backup_task.py` for real (systemd timer AND crontab paths) before ever activating it in
a real DR scenario, and decide whether macOS needs a proper launchd implementation or whether the
documented cron-with-caveats fallback is acceptable long-term.
