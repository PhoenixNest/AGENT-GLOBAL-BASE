# Log Entry 02 — Remediation — 2026-08-13

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`), following the plan approved at stage 2 in `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/01-discovery.md` |
| **Trigger**      | The CEO reviewed the discovery entry, confirmed the maintenance-record's own follow-up table already functioned as the implementation plan (no separate implementation-plan document needed), and approved proceeding with execution as planned.                                                                                                                                    |
| **State before** | As documented in `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/01-discovery.md`'s five findings.                                                                                                                                                                                                                              |

**Actions taken:**

**Item 1 — `.mcp.json` interpreter resolution.** Replaced both servers' `"command"` (a literal
`.venv/Scripts/python.exe` path) with `"command": "uv"`, `"args": ["run", "--project",
"<server-dir>", "--no-sync", "python", "<server-dir>/server.py"]`, and added `"env":
{"UV_PROJECT_ENVIRONMENT": ".../mcp-servers/.venv"}`. `uv run` resolves
`UV_PROJECT_ENVIRONMENT` to `Scripts/python.exe` on Windows and `bin/python` on Linux/macOS
internally — neither hardcoded. `--no-sync` prevents `uv` from attempting to reconcile the shared
venv against whichever server's `pyproject.toml` happens to be pointed at, since the venv is
intentionally shared across three different `pyproject.toml`s. **This item was reverted the same
day — see `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/03-incident-revert.md`.**

**Item 2 — `agent-memory/server.py` sibling-cleanup.** Removed
`_build_sibling_match_filter_clause` (built a PowerShell WHERE-clause string) and the
`powershell`/`Get-CimInstance`/`Stop-Process` subprocess calls in
`_cleanup_stale_sibling_processes` and `_diag_log_ppid_filtered_out_count`. Replaced with
`_sibling_matches()` (a pure-Python predicate) and `_iter_sibling_candidates()`/
`_scan_sibling_pids()` (backed by `psutil.process_iter`), preserving every documented guarantee
from the 2026-08-09/10 hardening: trailing-argument suffix match (not a substring anywhere), the
`_SIBLING_CLEANUP_MIN_AGE_S` age gate (unchanged), parent-PID scoping via `_SELF_PARENT_PID`,
self-exclusion, and the `_call_with_hard_timeout` watchdog around the scan. Removed the
`if sys.platform != "win32": return` early exit entirely — the function now runs on every
platform. Added `psutil>=6.0.0` to `agent-memory/pyproject.toml` and installed it into the shared
venv. Removed the now-unused `subprocess` import. **Unaffected by the later revert.**

**Item 3 — `manage_embedder_service.ps1` → `.py` port.** Wrote
`_shared/embedder-service/manage_embedder_service.py` (argparse CLI: `start`/`stop`/`status`/
`cleanup`), using `psutil` for process listing/termination and `urllib.request` (stdlib) for the
`/health` and `/shutdown` HTTP calls — no new HTTP dependency needed. Interpreter resolution
mirrors the original script's precedence (`EMBEDDER_SERVICE_PYTHON` override → shared venv,
resolved per-OS → `python` on `PATH` with a warning). Retired `manage_embedder_service.ps1`
(`git rm`), following the same `.ps1`/`.sh` → single `uv run` Python precedent used for
`.claude/hooks/prompt-gate-enforcer.py`. Updated `mcp-servers/CLAUDE.md`'s interpreter-resolution
table and `.claude/rules/mcp-governance.md`'s bare-`"python"` warning to reference the `.py` file.
**Unaffected by the later revert.**

**Item 4 — `register_backup_task.ps1` DR-scheduling gap.** Added a note to
`agent-memory/README.md`'s Disaster Recovery section stating this script is Windows-only _by
construction_ (wraps `Register-ScheduledTask`, no cross-platform analog) rather than by oversight,
and that a Linux/macOS deployment needs its own `cron`/`systemd`-timer script before scheduled DR
backup is ever activated there — explicitly not a line-for-line port target. No code changed; the
DR-backup path remains INACTIVE by default. **Unaffected by the later revert.**

**Item 5 — README code fences.** In both server READMEs: split every PowerShell-only
install/setup block that had a real bash equivalent into paired ` ```bash ` / ` ```powershell `
fences (docker `run` commands, pip/uv install commands, venv-interpreter paths); relabeled one
block in `workspace-knowledge/README.md` that was fenced `powershell` but contained no
OS-specific syntax to a plain fence; and updated both READMEs' `.mcp.json` configuration examples
to match item 1's command shape (later re-updated again after the revert). Also fixed the same
class of stale Windows-only fence in `mcp-servers/CLAUDE.md`'s torch-pinning example while editing
that file for items 1 and 3. **Unaffected by the later revert.**

**Verification:**

| Check performed                                                                                                                                                      | Result                                                                                                                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Launched `workspace-knowledge` via the new `uv run --project ... --no-sync python server.py` command shape, Windows                                                  | Ran ≥6s with no error output; `sys.executable` confirmed resolving to the shared venv, not a new local one                                                                                                                                                                        |
| Launched `agent-memory` via the exact new `.mcp.json` command shape, Windows                                                                                         | FastMCP banner printed, `Starting MCP server 'agent-memory' with transport 'stdio'` — clean start                                                                                                                                                                                 |
| `pytest tests/test_embedder_reliability_fixes.py` (rewritten for the psutil port) from `agent-memory/`                                                               | 35/35 passed                                                                                                                                                                                                                                                                      |
| `pytest tests/` — full `agent-memory` suite                                                                                                                          | 249/249 passed                                                                                                                                                                                                                                                                    |
| `manage_embedder_service.py status` / `start` / `status` / `stop` / `status`, real service lifecycle, Windows                                                        | STOPPED → started (pid confirmed, both models loaded) → RUNNING → graceful stop succeeded → STOPPED                                                                                                                                                                               |
| `manage_embedder_service.py cleanup` against a clean state                                                                                                           | "0 orphaned process(es) removed" — no false positives                                                                                                                                                                                                                             |
| Real (non-mocked) `_cleanup_stale_sibling_processes()` run with `AGENT_MEMORY_ENABLE_SIBLING_CLEANUP=true` on live OS processes                                      | Correctly found 0 same-parent-PID siblings and correctly identified 4 same-suffix processes under _different_ PPIDs as non-matches (diagnostic-only, never killed) — proves the cross-checkout/worktree safety scoping survived the port against real system data, not just mocks |
| Post-test cleanup: confirmed the pre-existing live session MCP server process (started before this session's edits, old command shape) was left untouched throughout | Confirmed via `Get-CimInstance` before and after cleanup — only test-spawned processes were terminated                                                                                                                                                                            |

**Not verified (cannot be from this Windows-only machine):** actual process launch and the
`_sibling_matches`/`_scan_sibling_pids` scan under a real Linux/macOS `psutil` build, and `uv run`
resolving `UV_PROJECT_ENVIRONMENT` to `bin/python` there — flagged as an open item, not claimed as
tested. This remains open — see `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/03-incident-revert.md`'s follow-up item.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | All five items were implemented; items 1–3 (the only ones with runnable code) were verified working on Windows in isolated testing, including one real, non-mocked exercise of the psutil-based sibling-cleanup against live system processes. `agent-memory` test suite green at 249/249. `manage_embedder_service.ps1` retired in favor of the Python port. **Item 1 did not survive contact with the live MCP host — see `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/03-incident-revert.md`.** |
| **Handoff to next stage** | User needed to run `/mcp reconnect` for both servers to pick up the new `.mcp.json` command. This is what surfaced the incident documented next — the topic reopened at pipeline stage 1 rather than closing here.                                                                                                                                                                                                                                                                                                                                        |
