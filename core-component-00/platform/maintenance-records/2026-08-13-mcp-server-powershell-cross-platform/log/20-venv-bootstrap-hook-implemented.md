# Log Entry 20 — Execution — 2026-09-01

| Field            | Detail                                                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`) |
| **Trigger**      | `log/19`'s approval — CEO directed building the new, independent venv-bootstrap hook.                                                                                                                               |
| **State before** | Both `workspace-knowledge/.venv/` and `agent-memory/.venv/` absent on this machine; `.mcp.json` held stale Windows-style interpreter paths for both servers; both MCP servers disconnected (`ENOENT`).              |

**Actions taken:**

1. Read `.claude/hooks/mcp-config-platform-check.py`, `.claude/hooks/_hook_log.py`,
   `.claude/settings.json`, `.mcp.json`, and `.claude/hooks/harness-rate-limiter-turn-reset.py`
   (house style reference) before writing anything.
2. Built `.claude/hooks/mcp-venv-bootstrap.py`: a `SessionStart` hook that reads this session's
   own `mcp-config-platform-check` invocation record from `hook-invocations.jsonl`, and — only
   when it reports `reason: "neither_os_path_exists"` for a server — runs `uv sync` in that
   server's directory (300s timeout per server, fail-open on any error/timeout/exception,
   fast no-op when nothing needs bootstrapping).
3. Registered the new hook in `.claude/settings.json`, as a second entry in the existing
   `SessionStart` hook group immediately after `mcp-config-platform-check`, guaranteeing
   execution order within a session (self-heal always logs first, this hook reads that log).
4. Validated `.claude/settings.json` remained valid JSON and the new hook file compiles
   (`python3 -m py_compile`).
5. Ran the new hook for real against the live broken state (functional test + immediate unblock,
   per the `log/11` precedent): fed it this session's actual `session_id`, which had a real
   `neither_os_path_exists` record for both servers already in the invocation log.
6. Immediately after, ran `mcp-config-platform-check.py` directly to confirm the sibling hook's
   own self-heal logic now succeeds against the newly-created venvs.

**Verification:**

| Check performed                                                               | Result                                                                                                                           |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `python3 -m py_compile mcp-venv-bootstrap.py`                                 | Pass — compiles cleanly                                                                                                          |
| `python3 -c "json.load(open('.claude/settings.json'))"`                       | Pass — valid JSON after the registration edit                                                                                    |
| Live run of `mcp-venv-bootstrap.py` against this session's real broken state  | `decision: "synced"`, `extra: {"synced": ["workspace-knowledge", "agent-memory"], "failed": []}` — both `uv sync` calls exited 0 |
| `ls workspace-knowledge/.venv/bin/python`, `ls agent-memory/.venv/bin/python` | Both now exist on disk (POSIX layout, this OS)                                                                                   |
| Live run of `mcp-config-platform-check.py` immediately after                  | `decision: "corrected"` — flipped both servers' `.mcp.json` command from the stale Windows path to the now-existing POSIX path   |
| `.mcp.json` contents after both hooks ran                                     | Both servers' `"command"` now read `.../\<server\>/.venv/bin/python`, matching the real venv on disk                             |

Independent-review gate (`pipeline.md` stage 4, shared-resource change): not yet satisfied by this
entry — self-verification only so far. A live `/mcp` reconnect by the CEO, confirming both servers
actually connect and respond to `health_check`, is still required per this topic's established
pattern for every prior item (`log/07`, `log/13`, `log/17`).

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | `.claude/hooks/mcp-venv-bootstrap.py` built and registered, fully separate from `mcp-config-platform-check.py` (which was not modified). Live-tested against this session's own real broken state — both servers' venvs are now bootstrapped and `.mcp.json` self-healed to the correct POSIX paths, all self-verified. `mcp-config-platform-check.py`'s existing fast/fail-open contract is unaffected: it still does zero extra work in the common case where venvs already exist. |
| **Handoff to next stage** | Routes to stage 4 — Verification. Item #8 does **not** close on this entry alone — needs the CEO to run a live `/mcp` reconnect and confirm both `workspace-knowledge` and `agent-memory` actually connect and respond to `health_check`, satisfying the independent-review gate for this shared-resource change, same as every prior item in this topic.                                                                                                                            |
