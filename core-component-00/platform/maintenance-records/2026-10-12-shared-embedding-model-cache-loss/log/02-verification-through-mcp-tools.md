# Log Entry 02 — Verification — 2026-10-12

| Field            | Detail                                                                                                                                                                                                                                                                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/maintenance-record.md`, pipeline stage 4 — Verification (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                 |
| **Trigger**      | CEO-approved re-test once the model files were restored (`core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/log/01-investigation-and-restore.md`)                                                                                                                                                         |
| **State before** | Both model slugs populated (20 files in `_shared/models/`). `agent-memory` server process started 2026-10-12 00:18, before the restore. `health_check` reported `embedder_service_state: unavailable`, `in_process_fallback_state: loading`. No `embedder-service` process; nothing listening on `127.0.0.1:8791`. No `workspace-knowledge` process |

**Actions taken:**

1. Executed by the lead orchestrator through the `agent-memory` MCP tools, in the session that
   reported the fault. No server was restarted and no code, hook, rule or configuration changed.
2. Polled `http://127.0.0.1:8791/health` for about 70 seconds after the restore.
3. Called `health_check`, then `search_memory` on the `reflection` collection with one unrelated
   query and two queries each aimed at a different stored record, `top_k=1`.
4. Called `write_memory` once with a labelled test record (`memory_type: episodic`, session
   `bcu00-save-test-2026-10-12`), then searched for it and looked the point up directly on
   `qdrant-memory`.

**Verification:**

| Check performed                                                                                 | Result                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `health_check` → `search_capability`                                                            | Pass, on the fallback. `in_process_fallback_state: ready`, `effective_path: in-process-fallback`. `embedder_service_state` remained `unavailable`            |
| `embedder-service` reachable on `127.0.0.1:8791`                                                | Fail. Not answering after about 70 s; no `embedder-service` process; `embedder-service.lock` still dated 00:27:16                                            |
| `search_memory`, query about `../`-chain cross-references                                       | Pass. `REFLECT-002` returned first, `degraded: false`, `tier: 1`                                                                                             |
| `search_memory`, query about the prompt-gate confirmation being skipped                         | Pass. `REFLECT-001` returned first, `degraded: false`, `tier: 1`                                                                                             |
| `search_memory`, unrelated query ("recipe for chocolate cake with buttercream frosting")        | Fail against the stated criterion. `REFLECT-003` returned, `degraded: false`, `tier: 1`. The vector path returns the nearest record with no similarity floor |
| `write_memory`, labelled test record                                                            | Pass. `written: true`, `lane: routine`, `status: quarantined`, record `8eda7265-286f-404a-ab11-d5234131bb0a`. The same call was rejected before the restore  |
| Test record retrievable through `search_memory` (session-scoped, dormant and archived included) | Fail. Zero results. The point exists on `qdrant-memory` with `status: quarantined`; `search_memory` has no parameter that includes quarantined records       |
| `workspace-knowledge` reconnect, `health_check`, one live search                                | Not run. The server was not connected in the executing session                                                                                               |

Independent review of this entry by Dr. Tomasz Wieczorek is outstanding.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | The fault this topic opened on is cleared for `agent-memory`: semantic search and writes work, served by the in-process fallback. Three items stay open. `embedder-service` did not start after the restore. An unrelated query still returns a record on the vector path, so preventive change (e) applies to tier 1 as well as tier 3. A routine write lands as `quarantined` and is not reachable through `search_memory`. One test point, `8eda7265-286f-404a-ab11-d5234131bb0a`, remains in `memory_episodic` |
| **Handoff to next stage** | Not closed. Stage 4 stays open until `embedder-service` is shown to start, `workspace-knowledge` is re-tested, and Dr. Wieczorek has reviewed this entry. Remaining items are listed in the topic's `maintenance-record.md` Open Follow-Up Items                                                                                                                                                                                                                                                                   |
