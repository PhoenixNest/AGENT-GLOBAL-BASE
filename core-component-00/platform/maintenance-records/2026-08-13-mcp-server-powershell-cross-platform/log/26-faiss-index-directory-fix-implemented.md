# Log Entry 26 — Execution — 2026-09-01

| Field            | Detail                                                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`) |
| **Trigger**      | `log/25`'s Approval — implement the `mkdir` guard fix for Item #10.                                                                                                                                                 |
| **State before** | `workspace-knowledge/server.py`'s `_build_or_load_faiss_index` crashes with a FAISS `FileIOWriter` error whenever `embedding/` doesn't already exist; `workspace-knowledge` stuck on BM25 fallback on this machine. |

**Actions taken:**

1. Added `self._INDEX_DIR.mkdir(parents=True, exist_ok=True)` as the first statement of
   `_build_or_load_faiss_index` (`server.py:391`, immediately before `index_file`/`state_file` are
   derived from `self._INDEX_DIR`), so the directory exists before either the write branch
   (`faiss.write_index` / `state_file.write_text`) or the read branch (`faiss.read_index`) touches
   it.
2. Attempted a full live reproduction first (instantiate `SearchEngine`, call
   `_build_or_load_faiss_index` directly with the real model and real chunks) — aborted partway
   through: this machine already had three live `workspace-knowledge` server processes running
   (pre-existing MCP connections) holding the GPU at 100% utilization / ~7.5 GB of 8 GB VRAM, and
   the test process's in-process embedding fallback stalled contending for the same GPU rather
   than failing. Killed the test process (PID 7598/7600) rather than let it keep starving the
   live, already-connected servers — this class of GPU contention is a pre-existing operational
   condition on this machine, not something Item #10's fix introduces or needs to solve.
3. Re-verified with an isolated, GPU-free test instead: constructed a bare `SearchEngine` (no
   model, no embedder-service), deleted `embedding/` if present, confirmed a `faiss.write_index`
   call against the missing directory reproduces the exact pre-fix crash class, then applied the
   same `mkdir(parents=True, exist_ok=True)` line the patched function now runs and confirmed the
   write succeeds and both `faiss.index` and `index_state.json` are created. Cleaned up the
   scratch directory afterward — no test artifacts left in place of a real index.

**Verification:**

| Check performed                                                                               | Result                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ls workspace-knowledge/embedding/` before fix                                                | Confirmed absent on this machine (`No such file or directory`)                                                                                                                                                                 |
| Reproduce pre-fix crash: `faiss.write_index()` against `_INDEX_DIR` with the directory absent | Confirmed: `RuntimeError` from `faiss::FileIOWriter::FileIOWriter` — "could not open ... for writing" — the same failure class `log/24`'s `rebuild_index` call hit                                                             |
| Apply `self._INDEX_DIR.mkdir(parents=True, exist_ok=True)`, retry the same write              | Succeeded: `faiss.index` and `index_state.json` both created under `embedding/`                                                                                                                                                |
| Read `server.py:389-393` post-edit                                                            | Confirmed the `mkdir` call is the first statement in the function, ahead of both `index_file`/`state_file` derivation and the `needs_rebuild` read/write branches                                                              |
| End-to-end live reproduction via a real `SearchEngine` instance with real embeddings          | Not completed — aborted early due to GPU contention with the three already-running live server processes (see Actions Taken #2); not required to confirm this specific `mkdir` fix, which is independent of the embedding step |

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | The `mkdir` fix is implemented and confirmed correct in isolation: it reproduces the exact pre-fix crash and confirms the fix resolves it, without depending on or contending for GPU resources the live, already-connected MCP servers are using. Full end-to-end confirmation (a live `workspace-knowledge` process running the patched code, actually building a real FAISS index against real embeddings) has not yet happened, since the three running server processes still hold the pre-fix code in memory. |
| **Handoff to next stage** | Routes to stage 4 — Verification, pending a live `/mcp reconnect` for `workspace-knowledge` (restarting its process onto the patched `server.py`) followed by a `rebuild_index`/`health_check` call to confirm the FAISS index actually builds end-to-end on this machine — the same independent-review pattern this topic has used throughout (e.g. `log/13`, `log/17`, `log/21`). Not yet committed, per this session's standing rule to hold commits for Verification.                                           |
