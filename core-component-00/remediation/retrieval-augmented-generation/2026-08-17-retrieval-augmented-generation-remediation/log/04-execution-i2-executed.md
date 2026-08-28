# Log Entry 04 — Execution — 2026-08-24

Part of `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/implementation-plan.md`.
Pipeline stage 3 — Execution (`core-component-00/remediation/pipeline.md`).

**Trigger:** Stage 2 Approval complete for I2 (`log/02-approval-i1-i2-approved.md`); no
Hook-Change Gate applies. Owner (Diego Fontán) begins Execution.

**Items covered:** I2 (RAG R2 — PII masking entirely unimplemented despite being a mandatory ASGF
control, per `.claude/rules/rag-engineering.md` § Security Controls).

**Actions taken:**

1. Added a new module `implementations/pii_masking.py` with `mask_pii(text) -> str`: regex-based
   detection and redaction of email addresses, phone numbers (both short `NXX-XXXX` and full
   `(XXX) XXX-XXXX` forms), SSN-like numbers (`XXX-XX-XXXX`), and credit-card-like numbers
   (16 digits, space- or dash-grouped). Patterns are applied email → credit-card → SSN → phone, so
   the more specific longer patterns are redacted first and can't leave a digit fragment for the
   looser phone pattern to partially re-match. This is pattern-based coverage only, per the plan's
   Approach — not a full NER-based PII system.
2. Wired masking into `RAGPipeline.ingest()` in `implementations/pipeline.py`, between chunking and
   embedding: `masked_text = mask_pii(chunk.text)` now runs before `self.embedder(masked_text)`,
   before the `vector_store.upsert()` payload's `"text"` field, and before the chunk is written
   into the local BM25 index (`self._documents`) — so masked text, not raw text, is what every
   downstream consumer (embedder, vector store, local index) ever sees.
3. Added `mask_pii` to `implementations/__init__.py`'s public exports.
4. Added a new dedicated test file, `testing/test_pii_masking.py`, with synthetic PII fixtures
   (`.invalid`-domain emails, NANP-reserved `555-01xx` phone numbers, `000-`-prefixed synthetic
   SSNs, and the well-known `4111-1111-1111-1111` Visa test card number — no real PII):
   - `TestMaskPii` (8 tests) — unit coverage of each pattern individually, multiple patterns in one
     string, non-PII text passing through unchanged, and the empty-string edge case.
   - `TestPipelineMasksBeforeEmbedding` (5 tests) — integration coverage asserting a spy embedder
     never receives raw PII, a recording vector-store's stored payload text never contains raw PII,
     the local BM25 index never retains raw PII, and PII-free ingestion is unaffected (masking is a
     no-op when no pattern matches).

**Verification:**

| Check performed                                                                                     | Result                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pytest retrieval-augmented-generation/testing/ -v` (run from `core-component-00/`)                 | Pass — 83 passed, 0 failed, 0 skipped                                                                                                                        |
| New `TestMaskPii` unit tests (8)                                                                    | Pass                                                                                                                                                         |
| New `TestPipelineMasksBeforeEmbedding` integration tests (5)                                        | Pass                                                                                                                                                         |
| Pre-existing `TestIngest`/`TestQuery`/`TestHybridRetrieval` classes in `test_pipeline.py` re-run    | Pass — no regressions (sample fixtures contain no PII, so masking is a no-op there; chunk counts, embedder-call counts, and ACL roles are unaffected)        |
| Environment: RAG `requirements.txt` heavy deps (torch, sentence-transformers, qdrant-client, spaCy) | Not required — masking is pure-`re` stdlib, and the rest of the module's test suite mocks all heavy I/O boundaries; no install step was needed for this item |

Independent-review gate (pipeline.md stage 4) is a separate stage — not performed here; Reviewer
is Dr. Elias Vance per the plan's Metadata.

**Outcome:** PII masking is now implemented and enforced at ingest time. Chunks containing
synthetic PII patterns are masked before reaching the embedder call, the vector store payload, and
the local BM25 index — verified directly by the new dedicated test file.

**Handoff to next stage:** Stage 4 — Verification, by Dr. Elias Vance (Reviewer, independent of
Owner), including a green run of `pytest retrieval-augmented-generation/testing/ -v`. `Status`
updated to "Executed, pending verification" — not "Verified", which requires that independent
sign-off.
