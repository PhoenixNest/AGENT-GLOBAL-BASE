# Log Entry 07 — Live `/mcp reconnect` Independently Confirmed — 2026-08-20

Part of `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 4 — Verification (`core-component-00/maintenance-records/pipeline.md`), closing out
`log/06-linux-launch-applied-and-verified.md`'s open independent-review requirement.

**Trigger:** The CEO ran `/mcp` (reconnect) from the live Claude Code host on this machine against
`.mcp.json` as fixed in `log/06-linux-launch-applied-and-verified.md`, and reported the result.

**State before:** Both servers foreground-verified in isolation (`log/06`), but per `pipeline.md`'s
stage 4 gate, that self-verification was explicitly insufficient for a `.mcp.json` change —
the 2026-08-13 incident (`log/03-incident-revert.md`) is the precedent for why: a change that
launches cleanly in the foreground still broke under the host's actual spawn environment.

**Actions taken:**

1. User ran `/mcp` (reconnect). Host output: `Reconnected to agent-memory.` and
   `Reconnected to workspace-knowledge.` — both succeeded, from the actual Claude Code host
   process, not a foreground shell test.
2. Called each server's own `health_check` tool over the live MCP connection to confirm the
   reconnect was a real, working connection, not just a clean process spawn:
   - `workspace-knowledge.health_check` — responded. `memory_instance.reachable: true`.
     `document_knowledge_base.reachable: false`, `search_tier: "rawfs"`,
     `degradation_reason: "rank_bm25 not installed"` — a dependency-completeness gap, not a
     launch-path failure; consistent with Open Follow-Up Item #5 (venv not fully synced).
   - `agent-memory.health_check` — responded. `memory_instance.reachable: true`,
     `point_counts` returned correctly. `search_capability.effective_path: "unavailable"`
     (`embedder_service_state: "starting"`, `in_process_fallback_state: "not started"`) — again
     the missing-torch/sentence-transformers gap already tracked as Item #5, not a new problem.

**Verification:**

| Check performed                                               | Result                                                                                      |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `/mcp` reconnect from live Claude Code host, both servers     | Both reconnected successfully                                                               |
| `workspace-knowledge.health_check()` over the live connection | Responded; `memory_instance.reachable: true`; document index degraded (missing `rank_bm25`) |
| `agent-memory.health_check()` over the live connection        | Responded; `memory_instance.reachable: true`; embedding degraded (missing torch stack)      |

**Independent-review gate (`pipeline.md` stage 4):** Satisfied. The reconnect was performed and
reported by the CEO, not the executor of `log/06`'s fix — this is the independent confirmation
that entry's Status line said was still needed.

**Outcome:** Open Follow-Up Item #1 (`.mcp.json` WSL/Linux launch defect) is now genuinely closed
— both self-verification (`log/06`) and independent live verification (this entry) confirm it.
The two degradations surfaced (`rank_bm25` missing, embedder stack missing) are the concrete,
now-observed symptoms of the already-open Item #5 (incomplete `uv sync`), not new findings —
noted here as evidence, not as a new item.

**Handoff to next stage:** Item #1 closes. Two items remain open on this topic (see
`maintenance-record.md`, updated alongside this entry): the per-server-vs-shared-venv architecture
question (Item #4) and completing the full dependency sync in each venv (Item #5, now with
concrete symptoms attached) so both servers run at full capability rather than degraded. Item #3
(Linux/macOS DR-scheduling verification) remains untouched by this entry. This topic does not
close yet — three items still open.
