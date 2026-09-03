# Log Entry 03 — Incident & Revert — 2026-08-13

| Field            | Detail                                                                                                                                                                                                                                                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3→1 — Reopen (`core-component-00/platform/maintenance-records/pipeline.md`): a new problem found during Execution routes back to Investigation rather than closing                          |
| **Trigger**      | Immediately after `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/02-remediation.md`'s item 1 landed, the user ran `/mcp reconnect` for both `workspace-knowledge` and `agent-memory` and got `Failed to reconnect ...: -32000` for both, repeatedly, across several attempts. |
| **State before** | `.mcp.json`'s `"command"` was `"uv"` (bare command name, `PATH`-resolved) for both servers, per `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/log/02-remediation.md`'s item 1.                                                                                                   |

**Root cause:** Manual testing from an interactive PowerShell session — including a
`.NET Process.Start` test with `PATH` explicitly restricted to the machine-scope value only —
found `uv` reliably resolvable and the full configured launch command starting cleanly every
time, with exit code 0 and a normal FastMCP startup banner. This did **not** match the live
failures, meaning the discrepancy was not in the command's correctness but in _which process
environment_ was resolving `"uv"`. The Claude Code host process that actually spawns MCP server
child processes uses its own long-lived process environment — captured whenever that host process
itself started — not a freshly-opened interactive shell's environment. A `uv` executable added to
the user `PATH` (`C:\Users\ASUS\.local\bin\uv.exe`, confirmed via `where.exe uv`) after the host
process started is invisible to that host until the host itself restarts; `/mcp reconnect` alone
re-spawns the MCP child using the same stale host environment, so it fails identically on every
retry. This is exactly the class of defect `mcp-servers/CLAUDE.md` already warned about for a
bare `"python"` — item 1 reintroduced an equivalent risk with `"uv"` instead, and it wasn't caught
before landing because verification was performed from a fresh interactive shell, which does not
reproduce the host's actual spawn environment.

**Actions taken:**

1. Confirmed `uv`'s resolved location (`where.exe uv` → `C:\Users\ASUS\.local\bin\uv.exe`) and
   that it resolves fine from a fresh shell, including under a machine-PATH-only environment —
   ruling out a simple "uv not installed" explanation and pointing at host-process environment
   staleness instead.
2. Ran the exact configured `uv run --project ... --no-sync python server.py` command in the
   foreground — confirmed it starts cleanly (FastMCP banner, exit 0), proving the command itself
   was not the defect.
3. Reverted `.mcp.json`'s `"command"` for both servers back to the direct, absolute interpreter
   path (`${CLAUDE_PROJECT_DIR:-.}/core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe`),
   removing the `uv run`/`--project`/`--no-sync`/`UV_PROJECT_ENVIRONMENT` scaffold entirely — the
   exact configuration known-working for the ~month-plus before this topic's remediation touched
   it.
4. Re-verified the reverted command launches cleanly via a direct foreground run.
5. Updated `mcp-servers/CLAUDE.md`'s interpreter-resolution table with an incident note
   explaining why `"uv"` is now excluded from the same defect class as bare `"python"`, and
   updated `.claude/rules/mcp-governance.md` and both server READMEs' `.mcp.json` examples to
   match the reverted command shape.

**Verification:**

| Check performed                                                                                         | Result                                                                              |
| ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `where.exe uv` from an interactive shell                                                                | Resolves to `C:\Users\ASUS\.local\bin\uv.exe`                                       |
| `.NET Process.Start` with `PATH` forced to machine-scope value only, `FileName="uv"`, `--version`       | Succeeded (`uv 0.12.0`) — ruled out a simple missing-from-PATH explanation          |
| Foreground run of the exact configured `uv run --project ... --no-sync python server.py` command        | Started cleanly, FastMCP banner printed, exit code 0                                |
| Foreground run of the reverted direct-interpreter command (`.venv/Scripts/python.exe server.py --help`) | Started cleanly, embedder-service background thread and FastMCP banner both printed |

**Not verified:** whether the live Claude Code host process actually picks up the reverted
`.mcp.json` on the user's next `/mcp reconnect` — depends on the user re-running it. If reconnect
still fails after this revert, the host process itself (not just the MCP connection) likely needs
a full restart.

| Field                | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**          | `.mcp.json` is back to the exact command shape that was working before this topic's Execution stage touched it — a full functional revert of item 1. The `.mcp.json` portion of this topic's original Investigation finding (item 1) is **reopened**: no longer "fixed," it is back to "Windows-only hardcoded path, now with an explicit one-line documented edit for Linux/macOS deployment" instead of the Execution stage's "automatic" claim, which did not survive contact with the actual host spawn environment. Items 2–5 (the `agent-memory/server.py` psutil port, the `manage_embedder_service.py` port, the DR-scheduling documentation, and the README fence reformatting) are **unaffected** — none depend on `.mcp.json`'s launch mechanism or on `uv`/`PATH` resolution. |
| **Handoff to Close** | No further reopen expected on this incident specifically — the revert is a known-working configuration, verified by prior operation, not a novel untested one. Two items remain open at Close, carried forward to `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`'s Open Follow-Up Items table: (1) the `.mcp.json` zero-edit cross-platform question, still genuinely unsolved; (2) Linux/macOS verification of items 2–3, still genuinely un-performable from this machine. Neither blocks Close — both are pre-existing, documented gaps, not new risk introduced by this incident.                                                                                                                             |
