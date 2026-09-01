# Log Entry 13 — Windows Reconnect Independently Confirmed — 2026-08-26

Part of `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 4 — Verification (`core-component-00/platform/maintenance-records/pipeline.md`), closing out
`log/12`'s open independent-review requirement — the same class of gate `log/07` satisfied for the
2026-08-20 WSL/Linux fix.

**Trigger:** The CEO ran `/mcp` (reconnect) against `.mcp.json` as fixed by `log/11` (OS-path
self-healing hook) and `log/12` (Windows venv sync + `jsonref`/`proxytypes` compatibility shim),
and reported the result.

**State before:** Both servers foreground-verified in isolation (`log/12`), but per `pipeline.md`'s
stage-4 gate, that self-verification was explicitly insufficient on its own for a
`.mcp.json`-registered-server change — this topic's own precedent (`log/03`, `log/06`) is that a
change which launches cleanly in the foreground can still fail under the Claude Code host's actual
spawn environment.

**Actions taken:**

1. User ran `/mcp` (reconnect). Host output: `Reconnected to agent-memory.` and
   `Reconnected to workspace-knowledge.` — both succeeded, from the actual Claude Code host
   process, not a foreground shell test.
2. Called each server's own `health_check` tool over the live MCP connection to confirm the
   reconnect was a real, working connection, not just a clean process spawn:
   - `workspace-knowledge.health_check` — responded.
     `document_knowledge_base: {reachable: true, point_count: 3664, search_tier: "hybrid_qdrant",
degradation_reason: null}` — full capability, **not** degraded to the `rawfs` fallback
     `log/07` observed on 2026-08-20 (that degradation was due to a missing `rank_bm25`, which
     this session's full `uv sync` installed). `memory_instance.reachable: true`.
   - `agent-memory.health_check` — responded. `memory_instance.reachable: true`, `point_counts`
     returned correctly. `search_capability.effective_path: "embedder-service"`
     (`embedder_service_state: "ready"`) — full capability, **not** degraded to
     `"unavailable"` as `log/07` observed (that degradation was the missing torch/
     sentence-transformers stack, also fixed by this session's full `uv sync`).
     `write_rate_limiting` telemetry present and at baseline (zero writes this session).

**Verification:**

| Check performed                                               | Result                                                                                          |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `/mcp` reconnect from live Claude Code host, both servers     | Both reconnected successfully                                                                   |
| `workspace-knowledge.health_check()` over the live connection | Fully healthy — `hybrid_qdrant` search tier, no degradation, 3664 indexed points                |
| `agent-memory.health_check()` over the live connection        | Fully healthy — `embedder-service` effective path, no degradation, write rate limiter reporting |

**Independent-review gate (`pipeline.md` stage 4):** Satisfied. The reconnect was performed and
reported by the CEO, not the executor of `log/11`/`log/12`'s fixes — this is the independent
confirmation those entries' Status lines said was still needed.

**Outcome:** This topic's Item #1 (`.mcp.json` cross-platform launch path) is now genuinely closed
on this Windows machine, and closed to a _higher_ bar than the 2026-08-20 WSL/Linux verification —
both servers report full, non-degraded capability rather than a working-but-degraded connection.
The durable `SessionStart` self-healing hook (`log/11`) is confirmed to correctly fix the OS-path
problem going forward; this session's additional fixes (`uv sync` for both venvs, the
`jsonref`/`proxytypes` vendored shim) resolved the two further problems `log/12` found while
attempting this verification.

**Handoff to next stage:** Close. No further reopen expected on this incident specifically. The two
items still open from before this reopen (Item #2's `manage_embedder_service.py` Linux/macOS path,
and Item #3's DR-scheduling) are unaffected by this entry and remain open, per
`maintenance-record.md`'s Open Follow-Up Items table.
