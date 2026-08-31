# Log Entry 03 — Execution — 2026-08-24

Part of `core-component-00/platform/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/implementation-plan.md`.
Pipeline stage 3 — Execution (`core-component-00/platform/remediation/pipeline.md`).

**Trigger:** Stage 2 Approval complete for I1 (`log/02-approval-i1-i2-approved.md`); no
Hook-Change Gate applies (neither item touches `.claude/hooks/*.py`). Owner (Sofia Almeida) begins
Execution.

**Items covered:** I1 (RAG R1 — ACL enforced only as a post-fusion in-memory filter).

**Actions taken:**

1. Added a shared `_role_has_access()` predicate and a new `filter_by_role(documents, user_role)`
   function to `implementations/retrieval.py` — a query-level ACL predicate that filters a
   candidate `Document` list _before_ any scoring runs, distinct from `acl_filter()` (which trims
   a `ScoredDocument` list _after_ ranking). `acl_filter()` itself was refactored to reuse the same
   `_role_has_access()` predicate but its external behavior and test contract are unchanged — it
   remains the documented second (post-fusion) defense layer.
2. Updated `RAGPipeline.query()` in `implementations/pipeline.py` to call
   `filter_by_role(corpus, user_role)` before either retrieval leg runs, then pass the
   role-accessible candidate set into `bm25_score()` — the BM25 leg's candidate selection now
   excludes out-of-role documents at the query level, not just after fusion.
3. Threaded `user_role` into the semantic leg's call:
   `self.vector_store.search(q_vector, top_k=self.top_k * 2, user_role=user_role)`. Updated the
   `RAGPipeline` docstring to document the new `vector_store.search(vector, top_k, user_role=None)`
   contract — `user_role`, when provided, must be applied as a query-level ACL predicate.
4. Updated `testing/conftest.py`'s `mock_vector_store` fixture so `search()` genuinely applies
   `user_role` as a filter over each entry's stored `acl_roles` payload before ranking — not a
   post-hoc trim — so the fixture demonstrates the same real-predicate behavior a production
   vector store (e.g. Qdrant payload filtering) is expected to implement. Backward compatible:
   `user_role=None` (the prior call shape, still used directly by `test_ingest_calls_vector_store_upsert`)
   skips the filter and returns all entries, unchanged from before.
5. Added `filter_by_role()` to `implementations/__init__.py`'s public exports.
6. Added new tests:
   - `testing/test_retrieval.py::TestFilterByRole` (4 tests) — unit coverage of `filter_by_role()`,
     including a test that runs `bm25_score()` against a `filter_by_role()`-shrunk candidate list
     and asserts the excluded document can never surface regardless of query terms.
   - `testing/test_pipeline.py::TestPreFusionACLEnforcement` (4 tests) — inspects the candidate set
     the pipeline builds _before_ `acl_filter()` runs: spies on `bm25_score()` to assert the
     documents it receives already exclude out-of-role chunks; spies on `vector_store.search()` to
     assert `user_role` is actually passed through; and calls `mock_vector_store.search()` directly
     (bypassing the pipeline and any post-fusion step entirely) to assert its raw returned
     candidate set already excludes out-of-role documents, and includes in-role ones.

**Verification:**

| Check performed                                                                                     | Result                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pytest retrieval-augmented-generation/testing/ -v` (run from `core-component-00/`)                 | Pass — 83 passed, 0 failed, 0 skipped                                                                                                                                                                                                                                                               |
| New `TestFilterByRole` tests (4)                                                                    | Pass                                                                                                                                                                                                                                                                                                |
| New `TestPreFusionACLEnforcement` tests (4)                                                         | Pass                                                                                                                                                                                                                                                                                                |
| Full pre-existing suite (75 tests: chunking, retrieval, pipeline) re-run unmodified-behavior        | Pass — no regressions                                                                                                                                                                                                                                                                               |
| Environment: RAG `requirements.txt` heavy deps (torch, sentence-transformers, qdrant-client, spaCy) | Not required — this module's code and test suite are pure Python with all heavy I/O boundaries (embedder, vector store) injected as mocks/stubs per `implementations/pipeline.py`'s design; `pytest` itself was already importable in this environment, so no install step was needed for this item |

Independent-review gate (pipeline.md stage 4) is a separate stage — not performed here; Reviewer
is Dr. Elias Vance per the plan's Metadata.

**Outcome:** ACL is now enforced as a genuine query-level predicate on both retrieval legs
(`filter_by_role()` pre-filtering the BM25 candidate corpus; `user_role` threaded into
`vector_store.search()`), in addition to the pre-existing post-fusion `acl_filter()` layer, which
is preserved unchanged as defense-in-depth per the Approach. A role-restricted query's raw
candidate set — verified directly via the new tests — never contains out-of-role documents, even
before any post-filter step runs.

**Handoff to next stage:** Stage 4 — Verification, by Dr. Elias Vance (Reviewer, independent of
Owner), including a green run of `pytest retrieval-augmented-generation/testing/ -v`. `Status`
updated to "Executed, pending verification" — not "Verified", which requires that independent
sign-off.
