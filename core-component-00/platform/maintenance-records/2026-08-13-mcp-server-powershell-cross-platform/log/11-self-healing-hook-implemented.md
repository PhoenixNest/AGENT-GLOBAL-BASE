# Log Entry 11 — Self-Healing Hook Implemented — 2026-08-25

Part of `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`), executing the
CEO-approved plan from `log/10-windows-reopen-and-proposed-fix.md`.

**Trigger:** CEO reviewed `log/10`'s proposal and approved the durable fix, authorizing Execution.

**State before:** `.mcp.json`'s two `"command"` values pointed at the Linux/WSL venv path
(`.venv/bin/python`, set in `log/06`), which does not exist on this Windows machine — both
registered MCP servers unreachable, per `log/10`.

**Actions taken:**

1. Built `.claude/hooks/mcp-config-platform-check.py`, a `SessionStart` hook (run via `uv run`,
   consistent with this workspace's existing 15-hook `uv run` convention). On every session start
   it reads root `.mcp.json`, and for each server in `mcpServers` whose configured `"command"`
   file does not exist on disk, rewrites it to the sibling per-OS suffix
   (`.venv/bin/python` ↔ `.venv/Scripts/python.exe`) — but only if that sibling path _does_ exist
   on disk; otherwise the server is left untouched and logged as unresolved, never guessed at.
   Every write is a fully-resolved, existence-verified absolute path — never a bare command name
   — so this cannot reintroduce the `log/03` stale-host-`PATH` failure mode that broke bare `"uv"`
   on 2026-08-13.
2. Named the file with the workspace's standard hyphenated hook-filename convention
   (`mcp-config-platform-check.py`), a small deviation from `log/10`'s proposed
   `mcp_config_platform_check.py` — cosmetic only, does not change the proposed behavior.
3. Registered the hook under a new `"SessionStart"` block in `.claude/settings.json` (this
   workspace's first use of that hook event), pointed at the new file via the same
   `${CLAUDE_PROJECT_DIR}` + `uv run` pattern every other hook uses.
4. Ran the hook directly against the live, currently-broken `.mcp.json` (`'{"session_id":"test"}'
| uv run .claude/hooks/mcp-config-platform-check.py`) as both a functional test and the
   immediate unblock in one action — see Verification.
5. Updated `core-component-00/platform/model-context-protocol-servers/CLAUDE.md`'s "Cross-platform consequence" note, which
   previously documented the manual one-line-edit-per-OS workaround as the accepted permanent
   state ("a one-line, documented change per server, not an automatic one") — marked superseded,
   describing the new self-healing mechanism instead.

**Verification:**

| Check performed                                                                      | Result                                                                                                                                          |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| First run against the live, broken `.mcp.json` (Linux paths on this Windows machine) | Exit 0. Both `"command"` values rewritten to `.venv/Scripts/python.exe`. `additionalContext`/`systemMessage` correctly listed both corrections. |
| Re-run immediately after (paths now already correct for this OS)                     | Exit 0, no stdout output, no file rewrite — confirms idempotency (no-op once already correct)                                                   |
| `.mcp.json` re-parsed as JSON after the hook's rewrite                               | Valid JSON, both servers' `env`/`args` blocks unchanged, only `"command"` values touched                                                        |
| `.claude/settings.json` re-parsed as JSON after adding the `SessionStart` block      | Valid JSON                                                                                                                                      |

**Independent-review gate (`pipeline.md` stage 4):** **Not yet satisfied.** `.mcp.json` is a
shared production resource other sessions/machines depend on, and this topic's own precedent
(`log/03`, `log/06`) is explicit that a foreground/self-run check is not sufficient on its own for
this class of change — a live `/mcp reconnect` from the Claude Code host, performed or witnessed
by someone other than the executor, is the confirming test. That has not happened yet in this
entry. **Status stays "Executed, pending independent verification"** until it does.

**Outcome:** `.mcp.json` is corrected for this Windows session (both servers should now launch).
The durable fix — the `SessionStart` self-healing hook — is implemented, registered, and
functionally verified by direct invocation, but not yet confirmed against a live Claude Code host
`/mcp reconnect`, which is this topic's actual bar for calling a `.mcp.json`-touching change done.

**Handoff to next stage:** Ask the user/CEO to run `/mcp` (reconnect) now that this session is
live, and call each server's `health_check` tool over the resulting connection — the same
two-step confirmation `log/07` used for the 2026-08-20 fix. A follow-up entry (`log/12`) should
record that result: if it succeeds, Item #1 re-closes and this topic's `Status` returns to
"Completed"; if it fails, this is a new incident requiring its own `log/` entry per the Reopen
edge, not a silent retry.
