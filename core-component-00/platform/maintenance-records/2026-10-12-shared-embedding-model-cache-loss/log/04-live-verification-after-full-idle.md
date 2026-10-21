# Log Entry 04 — Live Verification After a Full Idle Period — 2026-10-13

| Field            | Detail                                                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/maintenance-record.md`, pipeline stage 4 — Verification                                                    |
| **Trigger**      | CEO-approved new round of testing of the repair recorded in `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/log/03-idle-recovery-repair-and-self-check.md` |
| **State before** | Both MCP servers connected to Claude Code had been started at 07:51, after the repair, and were running the changed code. Nothing listening on `127.0.0.1:8791` (idle for about 15 minutes)             |

**Actions taken:**

1. Executed by the lead orchestrator through the live MCP tools. Read-only: no code change, no
   write to either Qdrant store.
2. Round 1, service already idled out: `agent-memory` `health_check`, then `search_memory`; then
   `workspace-knowledge` `health_check` and `search_docs`.
3. Left both servers untouched until `embedder-service` exited on its own 600 s idle timeout
   (still answering at about 570 s idle, closed within the following 42 s).
4. Round 2: `workspace-knowledge` `health_check`, then `search_docs`; then `agent-memory`
   `search_memory`; then `health_check` on both.

**Verification:**

| Check performed                                                | Result                                                                                                                       |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Round 1 `agent-memory` `health_check`, service down            | Pass. `embedder_service_probe: failed`, `effective_path: unavailable`                                                        |
| Round 1 `agent-memory` first `search_memory` after idle        | Pass. `degraded: false`, `tier: 1`; `embedder-service` relaunched                                                            |
| Round 1 `workspace-knowledge` `health_check` and `search_docs` | Pass. `hybrid_qdrant`, no degradation reason                                                                                 |
| `embedder-service` exits after the real 600 s idle timeout     | Pass                                                                                                                         |
| Round 2 `workspace-knowledge` `health_check`, service down     | Pass. `effective_search_tier: bm25` with the reason stated, `embedder_service_probe: failed`                                 |
| Round 2 `workspace-knowledge` first `search_docs` after idle   | Pass. `search_tier: hybrid_qdrant`, no degradation reason, same results and scores as round 1; `embedder-service` relaunched |
| Round 2 `agent-memory` `search_memory`                         | Pass. Intended record (`REFLECT-002`) returned, `degraded: false`, `tier: 1`                                                 |
| Round 2 `health_check` on both servers                         | Pass. `embedder_service_probe: ok`, `effective_path: embedder-service`                                                       |

**Observed, not resolved:** `workspace-knowledge` reported `in_process_model_loaded: false` about
30 minutes after start, so that process had no in-process fallback; had a relaunch failed, its
searches would have used BM25 (and said so). Simultaneous relaunch requests from several server
processes remain untested. The two failing `agent-memory` tests, the stale statements in
`.claude/rules/mcp-governance.md`, and independent review remain open. The change is uncommitted.
