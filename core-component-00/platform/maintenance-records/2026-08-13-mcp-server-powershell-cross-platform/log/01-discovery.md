# Log Entry 01 — Discovery — 2026-08-13

Part of `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 1 — Investigation (`core-component-00/platform/maintenance-records/pipeline.md`).

**Trigger:** The CEO observed that CC-00's MCP servers still depend on PowerShell commands and
asked whether this breaks OS universality for users on Linux/macOS. Dr. Vance and the relevant
CC-00 crew were asked to investigate and report.

**State before:** No prior audit of PowerShell/Windows-only dependencies existed for the MCP
server deployment surface.

**Actions taken:**

1. Confirmed the request scope (Dr. Vance + relevant CC-00 crew to assess and report).
2. Grepped `core-component-00/platform/model-context-protocol-servers/` for `powershell|pwsh|PowerShell|\.ps1` (case
   insensitive) across all source, docs, and tests to build a complete inventory rather than
   relying on the CEO's example.
3. Read the full text of `manage_embedder_service.ps1`, the relevant sections of
   `agent-memory/server.py` (lines 120–310), both server READMEs, and root `.mcp.json` to confirm
   each finding against actual code rather than filenames alone.
4. Cross-referenced `core-component-00/crew/CLAUDE.md` and
   `crew/infrastructure/ravi-deshmukh/agent/profile.md` to identify the correct crew owner for
   infrastructure/cross-platform-environment work.
5. Delivered a findings report (severity-ranked, with remediation recommendations) to the CEO in
   the originating session. No code was changed as part of this investigation.

**Findings — five PowerShell/Windows-only dependencies, ranked by severity:**

1. **`.mcp.json` (root), both server entries** — `"command"` hardcodes `.venv/Scripts/python.exe`
   (Windows venv layout). A Linux/macOS `.venv` places the interpreter at `.venv/bin/python`
   instead — this path does not resolve there, so neither `workspace-knowledge` nor
   `agent-memory` can be launched by Claude Code at all on a non-Windows machine as configured.
   Highest severity: blocks server startup outright.
2. **`agent-memory/server.py:154–299`** (`_cleanup_stale_sibling_processes`, the fix for the
   2026-08-09 reconnect mutual-kill race documented in `.claude/rules/mcp-governance.md`'s
   `agent-memory` row) — shells out to `powershell -NoProfile -NonInteractive -Command ...`
   (`Get-CimInstance Win32_Process`, `Stop-Process`) to find and terminate orphaned sibling
   processes on every server start. Already OS-guarded (`if sys.platform != "win32": return`),
   so it degrades to a documented no-op rather than crashing — but the orphan-cleanup protection
   this function exists to provide is silently absent on Linux/macOS.
3. **`_shared/embedder-service/manage_embedder_service.ps1`** — the only start/stop/status/cleanup
   supervisor for the shared embedder-service, entirely PowerShell (`Invoke-RestMethod`,
   `Get-CimInstance`, `Stop-Process`). Not required for normal operation (the service
   self-launches and self-idles-out), but the only manual-recovery tool for the orphaned-process
   problem it was written to solve — that recovery path did not exist at all on Linux/macOS.
4. **`agent-memory/scripts/register_backup_task.ps1`** — registers the DR backup job into Windows
   Task Scheduler. Currently inactive (nothing calls it automatically). Windows-only by
   construction; Task Scheduler has no direct cross-platform analog.
5. **Both server READMEs** — install/setup instructions fenced as ` ```powershell `, including
   backtick line-continuation syntax that fails outright under bash/zsh. Lower severity
   (documentation, not executed code) but actively misleading for a non-Windows operator.

Precedent already existed inside this workspace for fixing exactly this class of problem:
`.claude/hooks/prompt-gate-enforcer.py` and `prompt-gate-clear.py` were themselves once separate
`.ps1`/`.sh` scripts and are now a single cross-platform Python implementation invoked via
`uv run` (root `CLAUDE.md` §11; full root-cause record at workspace-root
`telescope/2026-07-30-cross-platform-config-automation/research-report.md`).

**Verification:**

| Check performed                                                                                      | Result                                                                                            |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Read root `.mcp.json` — confirmed literal `"command"` value for both servers                         | Confirmed: `.../mcp-servers/.venv/Scripts/python.exe` on both entries (Windows-only path)         |
| Read `agent-memory/server.py:242` — confirmed the sibling-cleanup OS guard                           | Confirmed: `if sys.platform != "win32": return` — non-Windows path is a no-op, not a crash        |
| Grep sweep of `core-component-00/platform/model-context-protocol-servers/` for PowerShell references | Confirmed 8 matching files (server.py, 2 test files, backup script, 2 READMEs, `.ps1`, CLAUDE.md) |
| Read `manage_embedder_service.ps1` in full                                                           | Confirmed: no `.py`/`.sh` equivalent existed anywhere in `_shared/embedder-service/`              |
| Read `register_backup_task.ps1`'s calling context via `agent-memory/README.md`                       | Confirmed: STATUS is "implemented, INACTIVE" — no automatic caller, opt-in only                   |

**Outcome:** The CEO's concern was confirmed accurate and, in one respect, understated — the
`.mcp.json` interpreter path was a hard launch blocker on Linux/macOS, not merely a degraded
feature. Ownership assigned per the standing model in
`core-component-00/platform/maintenance-records/CLAUDE.md` (Dr. Vance
owner, Ravi Deshmukh operational owner), applied to this specific defect.

**Findings handed to stage 2 (Approval) as the remediation plan:**

| #   | Item                                                                                                                                                                     | Owner                                                                                                                                                                        | Approval needed                                                                                       |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | Fix `.mcp.json` interpreter resolution so both servers launch cross-platform (blocking — do first)                                                                       | Ravi Deshmukh                                                                                                                                                                | Dr. Vance — changes the shared deployment contract both registered servers depend on                  |
| 2   | Replace the `powershell`/`Get-CimInstance`/`Stop-Process` calls in `agent-memory/server.py` with `psutil`, removing the `win32`-only gate rather than just tolerating it | Ravi Deshmukh, in consultation with Kwame Asante / Connor O'Malley (harness engineering — hardened this exact function across the 2026-08-09/10 mutual-kill-race fix rounds) | Dr. Vance — touches the reconnect-reliability fix history in `mcp-governance.md`'s `agent-memory` row |
| 3   | Port `manage_embedder_service.ps1` to a Python CLI invoked via `uv run`, following the hook-migration precedent                                                          | Ravi Deshmukh                                                                                                                                                                | Self-authorized within Infrastructure Engineer scope once item 1 lands                                |
| 4   | Document a Linux/macOS DR-scheduling equivalent (cron/systemd timer) for `register_backup_task.ps1` — not a line-for-line port target                                    | Ravi Deshmukh                                                                                                                                                                | Self-authorized — required only before any non-Windows DR activation, not urgent while inactive       |
| 5   | Reformat README install/setup code fences to POSIX-shell-compatible commands (or OS-tabbed pairs)                                                                        | Ravi Deshmukh                                                                                                                                                                | Self-authorized — documentation only                                                                  |
