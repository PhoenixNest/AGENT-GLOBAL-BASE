# Log Entry 25 — Approval — 2026-09-01

| Field            | Detail                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 2 — Approval (`core-component-00/platform/maintenance-records/pipeline.md`) |
| **Trigger**      | `log/24`'s handoff: Item #10 (`workspace-knowledge/server.py`'s `_build_or_load_faiss_index` never creates its output directory before writing to it) was reported, not fixed, pending Approval on scope.          |
| **State before** | Item #10 open, unfixed; `workspace-knowledge` on BM25-only fallback on this machine.                                                                                                                               |

**Actions taken:**

1. CEO approved fixing Item #10 and directed Execution.
2. Chose the code fix (`self._INDEX_DIR.mkdir(parents=True, exist_ok=True)` guard in
   `_build_or_load_faiss_index`) over the manual on-this-machine workaround `log/24` also
   floated (creating `embedding/` by hand). The manual workaround only fixes this one machine;
   `workspace-knowledge/embedding/` is gitignored and runtime-only, so any other machine that has
   never run the full FAISS-build path — a fresh clone, Item #8's exact scenario — hits the same
   crash. The code fix is durable across machines and is a one-line, low-risk addition consistent
   with `pathlib`'s idempotent `exist_ok=True` semantics (safe to call whether or not the
   directory already exists).

**Verification:**

N/A — this is an approval-stage entry recording a decision, not a code change.

| Field                     | Detail                                                                           |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Outcome**               | Code-fix approach approved for Execution over the manual per-machine workaround. |
| **Handoff to next stage** | Routes to stage 3 — Execution, recorded in `log/26`.                             |
