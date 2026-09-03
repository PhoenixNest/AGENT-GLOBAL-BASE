# Log Entry 01 — Investigation & Execution — 2026-08-06

| Field            | Detail                                                                                                                                                                                                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `2026-09-02-workspace-knowledge-embedding-cache-retrofit/maintenance-record.md`, stage 1 — Investigation                                                                                                                                                                         |
| **Trigger**      | Routine review of `workspace-knowledge`'s embedding-model loading found a private, duplicated model cache.                                                                                                                                                                       |
| **State before** | `workspace-knowledge/embedding/model/` held a private 418.4 MB copy of `all-mpnet-base-v2`, separate from the shared cache at `_shared/models/sentence-transformers--all-mpnet-base-v2/` that the embedding-model provisioning convention established for all CC-00 MCP servers. |

**Actions taken:**

1. Pointed `workspace-knowledge`'s fallback loader (`SearchEngine._MODEL_DIR`, used when `embedder-service` is unavailable) at `_shared/models/sentence-transformers--all-mpnet-base-v2/` for both the query path and the batch index-build/reseed/upsert paths.
2. Verified output parity between the private copy and the shared-cache copy.
3. Deleted the private `workspace-knowledge/embedding/model/` copy.

**Verification:**

| Check performed                                             | Result                             |
| ----------------------------------------------------------- | ---------------------------------- |
| Cosine similarity, private-copy vs. shared-cache embeddings | Pass — 1.0 (byte-identical output) |

| Field                     | Detail                                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | `workspace-knowledge` now reads `all-mpnet-base-v2` directly from the shared cache; no private per-server copy remains. |
| **Handoff to next stage** | Close — no follow-up items. See this topic's `maintenance-record.md` Open Follow-Up Items (none).                       |
