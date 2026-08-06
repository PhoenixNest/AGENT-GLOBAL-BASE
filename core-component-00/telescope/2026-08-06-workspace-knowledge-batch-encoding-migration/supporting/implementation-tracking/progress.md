# Progress — Phase 6: Workspace-Knowledge Batch-Encoding Migration

**Record status:** Maintained live, per-phase, as execution proceeded — not compiled
retroactively.

## Current State

**Status:** Complete. All 5 phases executed, merged into `core00/dev/engineering`, and
independently verified. See `implementation-plan.md` §10 for the full closeout review.

## Phase Status

| Phase | Status   | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | **Done** | Full-corpus benchmark (no sampling): 1,570 real `.md` files → 3,697 real chunks. Local CUDA 34.5 chunks/sec vs. HTTP-batched 34.0 chunks/sec — throughput equivalent. Surfaced a real fix requirement: the client's default 8.0s timeout is too tight for full 256-chunk batches (server-side cost ~7.4s alone); Phase 2 must pass `timeout=30.0` explicitly.                                                                                            |
| 1     | **Done** | Governance-gap sequencing: Option B (track PII-scrubbing gap in parallel) — applied per Dr. Vance's recommendation, endorsed by CEO sign-off.                                                                                                                                                                                                                                                                                                            |
| 2     | **Done** | Sofia Almeida: `_encode_batch_vectors()` added, three batch call sites redirected, `timeout=30.0` applied. Branch `agent/sofia/workspace-knowledge-batch-encoding-migration`, commit `d678b851`.                                                                                                                                                                                                                                                         |
| 3     | **Done** | Dr. Wieczorek: independent adversarial review, **PASS** (executed the real committed code under adversarial mocks). Connor O'Malley: fault-injection, 5/5 pass on `_encode_batch_vectors()` itself, found 1 real defect one level up (`_upsert_file_to_qdrant` delete-before-check ordering) — fixed and committed (`7d17fb83`) before merge, verified with a targeted regression test.                                                                  |
| 4     | **Done** | Real regression check against the actual merged code: mean cosine similarity 1.000000 (min 0.9999998807907104), top-3 nearest-neighbor exact agreement 20/20, 92 real chunks from 40 real files. Zero retrieval-quality regression.                                                                                                                                                                                                                      |
| 5     | **Done** | Caught and closed a design gap the plan under-specified: repointed the fallback loader (`SearchEngine._MODEL_DIR`) from the private copy to the shared cache — verified byte-identical output (cosine similarity 1.0) before deletion. Deleted `workspace-knowledge/embedding/model/` (418.4 MB reclaimed), re-verified the fallback still works with the private copy actually gone. Updated `.claude/rules/mcp-governance.md` to reflect the retrofit. |

## Open Items

None outstanding. Two non-blocking future-hardening items logged by Dr. Wieczorek (unvalidated
vector-count-length in `embedder_client.embed()`; unlocked `self._model` mutable state) — tracked
as harness-engineering backlog, not a condition of this closeout.
