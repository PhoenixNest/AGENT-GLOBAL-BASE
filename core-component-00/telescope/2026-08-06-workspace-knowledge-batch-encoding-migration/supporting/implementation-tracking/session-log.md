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
