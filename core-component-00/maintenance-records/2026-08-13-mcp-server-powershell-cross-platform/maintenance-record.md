# Maintenance Record — CC-00 MCP Servers — PowerShell Cross-Platform Support

**Owner:** Dr. Elias Vance (CC-00 Laboratory Director) — overall; Ravi Deshmukh (Infrastructure
Engineer) — operational execution throughout.
**Authorized / reviewed by:** CEO approved recording the discovery and proceeding with the
remediation plan. Dr. Vance's architecture sign-off applied specifically to the `.mcp.json` and
`agent-memory/server.py` items, since both touch the shared deployment contract and the
reconnect-reliability fix history. The incident revert was self-authorized by Ravi Deshmukh within
Infrastructure Engineer's documented authority — reverting a same-day change back to its prior
known-working state is not a new architecture decision.
**System / resource affected:** Root `.mcp.json` (both registered servers' `"command"`),
`core-component-00/mcp-servers/agent-memory/server.py` (`_cleanup_stale_sibling_processes()` and
related), `core-component-00/mcp-servers/_shared/embedder-service/manage_embedder_service.py`
(new, replacing the retired `.ps1`), `agent-memory/scripts/register_backup_task.ps1` and its new
2026-08-14 Linux/macOS counterpart `agent-memory/scripts/register_backup_task.py`, and both server
READMEs — all running under the shared venv at `core-component-00/mcp-servers/.venv/`.
**Severity:** P1 — confirmed defect (Windows-only launch paths), briefly escalated to P0 during
the Execution stage when a fix attempt broke live service; resolved back to P1 by the revert. The
2026-08-14 DR-scheduling follow-up is P3 (routine, inactive path, no live impact).
**Status:** Completed with three follow-up items open. `.mcp.json`'s zero-edit cross-platform
resolution is reopened — current state is a documented one-line manual edit per OS, not automatic
resolution. Linux/macOS behavior of the `agent-memory/server.py` and `manage_embedder_service.py`
ports is unverified (no non-Windows machine available). `register_backup_task.py` (Linux/macOS DR
scheduling) is now written but likewise unverified on any non-Windows machine — see
`log/04-linux-macos-dr-scheduling.md`. All code and documentation changes are live in the working
tree.

---

## Pipeline Stage Log

Per `core-component-00/maintenance-records/pipeline.md`. Each stage's full account — trigger,
actions, verification, outcome — lives in its own `log/` entry; this file stays a short,
always-current summary (Zhao's working-memory / episodic-detail split — see
`core-component-00/maintenance-records/README.md` § Format Note, 2026-08-13 second revision).

| Stage                                       | Entry                                                                                                                       | Summary                                                                                                                                                                                                                                                               |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 — Investigation                           | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/01-discovery.md`                 | Confirmed the CEO's concern: five PowerShell/Windows-only dependencies found across the MCP-server deployment surface, ranked by severity. `.mcp.json`'s hardcoded interpreter path was the most severe — a hard launch blocker on Linux/macOS. Ownership assigned.   |
| 2 — Approval                                | (recorded above, in this file's header)                                                                                     | CEO approved proceeding with the five-item remediation plan as the discovery record's own follow-up table.                                                                                                                                                            |
| 3 — Execution                               | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/02-remediation.md`               | All five items implemented. Items 2–5 verified working and stand today. Item 1 (`.mcp.json` → `uv`-based launch) broke live `/mcp reconnect` immediately after landing — see next entry.                                                                              |
| 3→1 — Reopen (incident found mid-execution) | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/03-incident-revert.md`           | Root-caused the `uv` PATH-resolution failure in the Claude Code host's own environment; reverted `.mcp.json` to the prior known-working direct interpreter path. Items 2–5 unaffected.                                                                                |
| 4 — Verification                            | (embedded in each `log/` entry's own Verification table)                                                                    | Windows-only verification throughout — foreground launches, full `agent-memory` test suite (249/249), and one real non-mocked exercise of the psutil-based sibling-cleanup against live OS processes.                                                                 |
| 5 — Close                                   | This file                                                                                                                   | Closed 2026-08-13 with two open follow-ups — not a silent "Completed," per the staleness-bound rule in `core-component-00/maintenance-records/pipeline.md`.                                                                                                           |
| 3 — Execution (follow-up, 2026-08-14)       | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/04-linux-macos-dr-scheduling.md` | CEO asked why the DR-scheduling gap (follow-up item 3) should stay deferred; approved writing it now, explicitly unverified. `register_backup_task.py` (systemd timer / crontab) written and compile/dry-run checked; real Linux/macOS registration still unverified. |
| 3 — Execution (follow-up, 2026-08-14)       | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/05-ps1-retention-decision.md`    | CEO asked whether `register_backup_task.ps1` could be removed now that `.py` exists; Dr. Vance recommended against it (the two scripts are platform-exclusive, not redundant — `.py` refuses to run on Windows). CEO agreed to keep both. No files changed.           |

---

## Open Follow-Up Items

| #   | Item                                                                                                                                                                                                                                                                                                                                    | Owner                                                             | Target                                                                                  |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1   | The `.mcp.json` portion of the original cross-platform finding is reopened — no reliable zero-edit, OS-agnostic launch command has been found (`PATH`-resolved indirection failed in production); either accept the one-line-per-OS documented manual edit as the permanent answer, or find a mechanism this workspace hasn't tried yet | Ravi Deshmukh, Dr. Vance (architecture call)                      | Unscheduled — not urgent, current state is a documented manual edit, not a silent break |
| 2   | Linux/macOS behavior of the `agent-memory/server.py` psutil port and `manage_embedder_service.py` is inferred from `psutil`'s documented cross-platform design, not directly observed — no Linux/macOS machine available here                                                                                                           | Ravi Deshmukh, or whoever next runs this workspace on non-Windows | Opportunistic — first real non-Windows run                                              |
| 3   | `register_backup_task.py` (systemd timer / crontab, written 2026-08-14) has never been run for real on Linux or macOS — confirm it actually registers and fires before treating the DR-backup path as ready on either platform. macOS launchd support is not implemented (cron fallback only, with documented TCC caveats)              | Ravi Deshmukh, or whoever next has Linux/macOS access             | Before any non-Windows DR activation                                                    |

---

## Related Records

- `core-component-00/maintenance-records/pipeline.md` — the stage definitions this topic was
  retroactively organized against (the pipeline itself was established after this topic closed,
  during the same-day convention revision — see
  `core-component-00/maintenance-records/README.md` § Format Note).
- `.claude/rules/mcp-governance.md` — `agent-memory` and `workspace-knowledge` rows, updated to
  reference this topic's current state rather than narrating it inline.
- `core-component-00/mcp-servers/CLAUDE.md` § Python Environment — interpreter-resolution table
  and incident note, kept current with each stage above.
- Workspace-root `telescope/2026-07-30-cross-platform-config-automation/research-report.md` — the
  precedent the Execution stage followed (hook `.ps1`/`.sh` → single `uv run` Python
  implementation).
- `core-component-00/crew/infrastructure/ravi-deshmukh/agent/profile.md` and
  `skills/gpu-dependency-environment-management.md` — operational owner's documented authority and
  quality bar ("every workflow that assumes GPU has a documented, tested CPU fallback path" — the
  same standard applies here to OS assumptions).
