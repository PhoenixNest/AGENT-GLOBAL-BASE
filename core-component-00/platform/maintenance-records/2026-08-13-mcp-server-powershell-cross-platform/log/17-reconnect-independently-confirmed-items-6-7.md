# Log Entry 17 — Verification — Items #6 & #7 Independently Confirmed — 2026-08-30

Part of
`core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 4 — Verification (`core-component-00/platform/maintenance-records/pipeline.md`).

**Trigger:** CEO ran a live `/mcp` reconnect following `log/15` (Item #6) and `log/16` (Item #7),
both of which had self-executed verification only and were explicitly held at "pending
verification" per the stage-4 independent-review gate for changes touching a shared production
resource (`.mcp.json` and the MCP servers it configures).

**State before:** Item #6 — `.mcp.json` gitignored, `.mcp.json.example` template committed,
`mcp-config-platform-check.py` rewritten to bootstrap-once/patch-if-stale — foreground/simulated
verification only. Item #7 — `workspace-knowledge/server.py`'s vendor-shim insertion made
conditional — foreground verification only (reached `Starting MCP server`, no real client
attached).

**Actions taken:**

1. CEO ran `/mcp` (reconnect). Output: `Reconnected to workspace-knowledge.` then
   `Reconnected to agent-memory.` — both servers, over Claude Code's real MCP client, not a
   foreground/simulated test.
2. No further action needed on `.mcp.json` or the hook — this confirms the machine-local file
   Item #6 bootstrapped (or left in place) resolves correctly for both servers under the new
   gitignored/generate-once design, and confirms Item #7's conditional vendor-shim fix resolves
   `workspace-knowledge`'s real startup path, not just the foreground import path checked in
   `log/16`.

**Verification:**

| Check performed                              | Result                                |
| -------------------------------------------- | ------------------------------------- |
| Live `/mcp` reconnect, `workspace-knowledge` | `Reconnected to workspace-knowledge.` |
| Live `/mcp` reconnect, `agent-memory`        | `Reconnected to agent-memory.`        |

**Independent-review gate (pipeline.md stage 4):** Satisfied for both Item #6 and Item #7 — the
CEO, not the executing session, ran the live reconnect against the real Claude Code MCP client.

**Outcome:** Both items close.

- **Item #6** (`.mcp.json` template/gitignore/generate-once bootstrap redesign): closes. The one
  caveat `log/14`/`log/15` flagged and never resolved — whether Claude Code reads `.mcp.json`
  before or after `SessionStart` hooks run on a genuinely fresh clone with no file at all — remains
  formally untested (this session's `.mcp.json` already existed throughout; no true first-clone
  case occurred), but is no longer blocking, since the change is in normal use and reconnecting
  cleanly. Recorded as a residual, non-blocking note rather than an open item.
- **Item #7** (`workspace-knowledge` `peak`-shim regression): closes. Confirmed unrelated to Item
  #6 and pre-existing, per `log/16`.

**Handoff to next stage:** Close. Only Item #3 (Linux/macOS DR backup scheduling,
`register_backup_task.py`) remains open in this topic — explicitly deferred, no work requested on
it this session.
