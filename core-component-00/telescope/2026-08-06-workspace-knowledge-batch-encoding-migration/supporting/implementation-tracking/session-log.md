# Session Log — Phase 6: Workspace-Knowledge Batch-Encoding Migration

## 2026-08-06

- CEO signed off on the implementation plan and delegated full responsibility for this migration
  to Dr. Vance and the relevant CC-00 team, applying Dr. Vance's non-binding recommendations on
  both blocker decisions (§2.1 Option B — track PII-scrubbing gap in parallel; §2.2 — hard Phase 0
  benchmark gate). CEO additionally directed use of git worktree isolation and multi-agent
  development technique for the implementation phases.
- Phase 0 benchmark script authored (`phase0_benchmark.py`), reusing the exact production
  512-word/64-word-overlap chunking algorithm from `workspace-knowledge/server.py`'s `_chunk_file`.
- First run used a 150-file / 335-chunk sample (path bug required one re-run). Confirmed CUDA
  available (`torch 2.13.0+cu130`), embedder-service startable, real throughput numbers obtainable.
- Re-ran against the **full real corpus, no sampling** (1,570 `.md` files, 3,697 chunks), since the
  sampled numbers showed raw embedding throughput (~30-35 chunks/sec) was fast enough that a full
  run was affordable (~2 minutes), directly satisfying the plan's "must actually complete this
  time, not a substituted sample" gate rather than relying on extrapolation.
- **Finding:** local CUDA and HTTP-batched-via-embedder-service achieve near-identical raw
  throughput (34.5 vs 34.0 chunks/sec) — Research Question 1 answered positively, the existing
  `/embed` batching primitive is sufficient. But 7 of ~15 full 256-chunk HTTP batches timed out at
  the client's default 8.0s bound, because a 256-chunk batch's own server-side encode cost
  (~7.4s, derived from the measured local rate) is already close to that bound before HTTP/JSON
  overhead. Root-caused as a timeout-tuning mismatch (query-path default reused unmodified for the
  batch path), not a service reliability defect — `embedder_client.embed()` already accepts a
  `timeout=` override, unused at its default in the naive case.
- Phase 0 marked complete on this real evidence. Design correction carried into Phase 2: batch
  calls must pass an explicit, longer timeout.
- Phase 1 (governance-gap sequencing) begun: recording Option B as the executed decision.
- Phase 2 dispatched to a worktree-isolated subagent as Sofia Almeida: implemented
  `_encode_batch_vectors()`, redirected the three batch call sites, applied `timeout=30.0`. Found
  and fixed one bug of her own during implementation (`self._model` assignment timing in
  `_build_or_load_faiss_index`). Committed on `agent/sofia/workspace-knowledge-batch-encoding-migration`
  (`d678b851`), not merged — awaiting Phase 3.
- Phase 3 dispatched as two parallel worktree-isolated subagents: Dr. Wieczorek (adversarial
  review) and Connor O'Malley (fault injection), both against the real committed branch.
  Wieczorek: PASS. O'Malley: found a real, reachable defect — `_upsert_file_to_qdrant` deleted a
  file's existing Qdrant points before checking whether re-encoding succeeded, so an encode
  failure could silently drop the file from the index until a later repair.
- Fix applied directly in the Sofia worktree (attributed to Kwame Asante, who owns client-side
  robustness): swapped the encode-and-check/delete order, added a targeted regression test
  covering both the failure path (no delete/upsert call) and the success path (unchanged
  delete-then-upsert order), verified both pass. Committed (`7d17fb83`).
- Docs (research-report.md, implementation-plan.md, tracking files, telescope/README.md) committed
  to `core00/dev/engineering` (`76605bea`), then the reviewed Sofia branch merged in with `--no-ff`.
- Phase 4: real regression check against the actual merged code (not a re-implementation) —
  mean cosine similarity 1.000000, top-3 exact agreement 20/20 across 92 real chunks. Zero
  retrieval-quality regression. Gate cleared.
- Phase 5: before deleting the private model copy, caught a real gap the plan itself
  under-specified — the fallback loader (`SearchEngine._MODEL_DIR`) hardcoded the private path,
  so naive deletion would have broken the degrade-never-block contract Phases 3-4 had just
  verified. Repointed `_MODEL_DIR` at the shared cache, verified byte-identical output (cosine
  similarity 1.0) before deletion, deleted `workspace-knowledge/embedding/model/` (418.4 MB),
  then re-verified the fallback still works with the private copy actually gone. Updated
  `.claude/rules/mcp-governance.md` to reflect the retrofit. Investigation closed.
