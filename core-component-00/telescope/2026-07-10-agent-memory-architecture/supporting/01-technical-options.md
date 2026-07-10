# Technical Options — Persistent Agent Memory on Qdrant

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** `../research-report.md`
> **Audience:** Engineers implementing or extending the memory store against the workspace's
> Qdrant-backed retrieval infrastructure.
> **Last Updated:** 2026-07-10

---

## 1. Scope

This document specifies **technical options** for persisting the four CC-00 memory types
(episodic, semantic, procedural, working — `context-engineering/implementations/memory_store.py`)
against Qdrant, extending the lightweight RAG retrieval component
(`retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`) that already backs
the `workspace-knowledge` MCP server. It does not cover the forgetting/decay policy (see
`03-forgetting-strategy.md`) or step-by-step deployment (see `02-deployment-guidelines.md`).

---

## 2. Foundational Decision: Memory Is Primary Data, Not a Derived Index

The RAG architecture's **Corpus-as-Source-of-Truth principle**
(`retrieval-augmented-generation/architecture/overview.md` §10) treats every vector index as a
derived, rebuildable artifact of a Markdown document corpus. Agent memory breaks that assumption:
a memory record (a decision, a corrected fact, a consolidated episodic summary) is **generated at
runtime** — it has no prior document to derive from. Storing it only inside Qdrant would violate
the workspace's own design rule ("never store information in a retrieval index that is not
derivable from the document corpus") and would make an accidental index rebuild destructive rather
than merely slow.

**Design rule — Memory-as-Corpus:** every memory write is first appended to a durable,
human-readable log (JSONL) that becomes the corpus for that memory type; the Qdrant collection is
a **derived semantic index over the log**, exactly as the existing knowledge-base collection is a
derived index over `company/`, `studio/`, and `core-component-00/` Markdown. This preserves the
workspace's existing rebuild/rollback guarantees and lets the four-tier graceful-degradation stack
(`architecture/overview.md` §11) apply to memory retrieval unmodified — BM25/FAISS/raw-scan
fallback all still work because the log is plain text.

```
Agent turn → MemoryStore API call → append to <type>.jsonl (source of truth)
                                          ↓ (sync upsert, see 02-deployment-guidelines.md)
                                    Qdrant collection (derived index)
```

---

## 3. Collection Design

Use **separate Qdrant collections per memory type**, not one shared collection with a
`memory_type` filter field. Rationale: each type has a distinct retention policy, payload schema,
and query pattern (episodic is queried by `session_id` + recency; semantic is queried by embedding
similarity across all sessions); a shared collection would force every decay/GC pass to scan and
filter the whole collection instead of operating on a type-scoped one, and would couple unrelated
retention policies to a single collection configuration (shards, HNSW params).

| Collection          | Backs                          | Retention                                                                                                                                                                            | Primary Query Pattern                              |
| ------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| `memory_episodic`   | `EpisodicMemory` events        | Session-scoped; decays per `03-forgetting-strategy.md`                                                                                                                               | `session_id` filter + recency, rarely by embedding |
| `memory_semantic`   | `SemanticMemory` facts         | Cross-session persistent; decays by salience                                                                                                                                         | Embedding similarity (`query_text`)                |
| `memory_procedural` | `ProceduralMemory` corrections | Persistent; procedural memory's primary form remains the file-based skill/profile documents (§7) — this collection holds only runtime-learned corrections, not the skills themselves | Embedding similarity, filtered by `skill_name`     |

`WorkingMemory` is **never persisted to Qdrant** — it lives entirely in the active context window
and is cleared every turn (`memory_store.py` `WorkingMemory.clear()`). Persisting working memory
would defeat its purpose (task-scoped, disposable state) and create a fourth collection with no
retrieval value.

### 3.1 Payload Schema (all three collections share this superset; unused fields are omitted per type)

```json
{
  "id": "uuid4",
  "memory_type": "episodic | semantic | procedural",
  "content": "string — the fact, event, or correction text",
  "created_at": "ISO 8601 UTC",
  "last_accessed_at": "ISO 8601 UTC",
  "access_count": 0,
  "importance": 0.0,
  "confidence": 1.0,
  "decay_weight": 1.0,
  "status": "active | dormant | archived",
  "source_session_id": "string | null",
  "source_turn": 0,
  "sacred": false,
  "tags": [],
  "consolidated_from": [],
  "modality": "text | image | audio",
  "media_ref": "string | null — see §3.2, null for text"
}
```

See `03-forgetting-strategy.md` §3 for how `importance`, `decay_weight`, and `status` are computed
and mutated over time, and `context-engineering/implementations/memory_store.py`'s
`SACRED_EVENT_TYPES` for the `sacred` flag's source (decisions/commitments — never decays,
mirroring `EpisodicMemory.get_sacred_context()`).

### 3.2 Multimodal Memory (Images, Audio)

`content` remains the only field that gets embedded, regardless of `modality`. For a non-text
memory, `content` holds a **derived textual representation** — an image caption or an audio
transcript/summary — generated by the model itself at write time, using its native multimodal
understanding of whatever it just saw or heard in-context. The raw media file is not embedded and
is not stored in Qdrant; it is written to disk at
`core-component-00/context-engineering/memory/media/<uuid>.<ext>`, and `media_ref` holds that path.

This follows directly from §2's Memory-as-Corpus principle rather than introducing a new one: a
derived representation (the caption) must never be the only surviving copy of its source (the
image or audio itself), the same reasoning that makes the JSONL log — not Qdrant — the source of
truth for text memory. Retrieval on a multimodal memory record is therefore two steps: semantic
search over `content` as usual, then an optional file read against `media_ref` if the agent needs
to re-examine the original media rather than just its own prior caption of it.

**MarkItDown is explicitly out of scope for this write path.** Microsoft's MarkItDown converts
external documents (PDF, Office, HTML, images via OCR, audio via transcription) to Markdown for
batch ingestion — that is a document-corpus concern
(`retrieval-augmented-generation/`, owned by Almeida/Fontán), not a memory-write concern. A memory
record is generated by the model in the middle of a live turn, already looking at or listening to
the source directly; routing that back out through an external OCR/ASR tool would discard
information the model already extracted natively and add a dependency for no retrieval benefit.
Reserve MarkItDown for converting externally-sourced multimodal files into the document knowledge
base, not for populating `memory_episodic` or `memory_semantic`.

Chunking is unaffected — §5 still applies; a long audio transcript should go through
`ContextCompressor.extractive_compress()` before being written as `content`, exactly as a long text
memory would. Embedding is caption-then-text (all-MiniLM-L6-v2, no new model dependency) for this
design; direct multimodal embedding (e.g., a CLIP-style joint image/text encoder) is deferred as a
v2 enhancement, not a v1 requirement — see `06-self-review-and-evaluation.md` for the security
follow-up this extension requires before implementation.

---

## 4. Embedding Model Options

Reuse the workspace's existing technology stack reference
(`retrieval-augmented-generation/architecture/overview.md` §4) rather than introducing a new
model dependency:

| Option                             | Fit for Memory Writes                                                                                              | Trade-off                                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **all-MiniLM-L6-v2 (recommended)** | Already used as the RAG module's alternative embedding model; 384-dim, fast enough for per-turn synchronous writes | Slightly lower retrieval quality ceiling than bge-small                                                 |
| bge-small-en-v1.5                  | Primary embedding model for the document corpus; higher retrieval quality                                          | Marginally higher per-write latency — matters because memory writes happen every turn, not per document |

**Recommendation:** use `all-MiniLM-L6-v2` for `memory_episodic` and `memory_semantic` writes
(write-frequency-sensitive), and keep `bge-small-en-v1.5` for the existing document corpus
collection unchanged. Using two embedding models across collections is acceptable because Qdrant
collections are independently configured — there is no cross-collection similarity comparison
requirement between memory and documents.

---

## 5. Chunking Strategy: None

Document RAG chunking (`retrieval-augmented-generation/fundamentals/` — fixed-size / semantic /
hybrid) does not apply to memory. Memory entries are already atomic units by construction — one
episodic event, one semantic fact, one procedural correction — written directly by
`EpisodicMemory.record_event()` / `SemanticMemory.store()` / `ProceduralMemory.register()`.
Chunking an already-atomic record would fragment a single decision across multiple vector points
with no benefit. If a single memory record's content exceeds a reasonable token budget (e.g. a
long consolidated episodic summary), apply `ContextCompressor.extractive_compress()`
(`context-engineering/implementations/context_compressor.py`) **before** the record is written,
not chunking after.

---

## 6. Retrieval Strategy

Apply the same hybrid retrieval principle already mandated for RAG
(`.claude/rules/rag-engineering.md`): semantic (Qdrant) + keyword (BM25) fusion, reusing
`retrieval-augmented-generation/implementations/retrieval.py`'s RRF fusion. Two retrieval modes:

| Mode                    | Used By                                              | Query Shape                                                                      |
| ----------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Recency-filtered**    | `EpisodicMemory.recent_turns()` equivalent           | Qdrant filter on `source_session_id` + sort by `created_at`, no embedding needed |
| **Semantic similarity** | `SemanticMemory.query()` / `ProceduralMemory` lookup | Embedding similarity + BM25 fusion, filtered to `status = "active"`              |

`sacred = true` records must always be included in recency-filtered retrieval regardless of any
decay-driven `status`, per `EpisodicMemory.get_sacred_context()`'s existing contract that
decisions/commitments are returned verbatim every time.

---

## 7. Procedural Memory Stays File-Based

Procedural memory's canonical form in this workspace is **not** a vector store — it is the agent
`profile.md` and `skills/*.md` files that already govern behavior (per Activation Protocol,
CLAUDE.md §7 and `crew/CLAUDE.md`). `memory_procedural` in Qdrant exists only for a narrower
purpose: runtime-learned corrections that have not yet been promoted into a formal skill file edit
(e.g., "user corrected the retry threshold to 3, not 5, on 2026-07-08"). Treat any
`memory_procedural` entry that recurs across ≥3 sessions as a signal to escalate a documentation
update to the skill file itself — at that point the correction becomes canonical documentation and
the memory record is archived (see `03-forgetting-strategy.md` §4, Consolidation).

---

## 8. Deployment Mode

Follow the existing mandate in `lightweight-rag-deployment.md` §Vector Database Deployment Mode
Selection without exception: **Docker/Server mode only** — embedded mode's data-format
incompatibility with server mode (§Critical Constraint in that document) applies identically here.

**Memory runs on its own dedicated Qdrant instance, physically separate from the document
knowledge base's `qdrant-workspace` container.** This is a deliberate architectural boundary, not
a convenience default: the two systems serve different use cases (a curated, ACL-governed
document corpus vs. dynamic, session-scoped agent memory), have different write-load profiles
(document writes are occasional; memory writes happen nearly every agent turn), and warrant
independent failure domains — a memory-instance outage should not take document retrieval down
with it, and vice versa. Collection-level separation within a single shared instance was
considered and rejected: it is logically sufficient for data isolation but insufficient for blast
radius, workload isolation, and security-boundary rigor, all of which the memory system's design
requires independent of this workspace's current single-node hardware profile. See
`02-deployment-guidelines.md` §1 for the dedicated container specification.

Memory data is materially harder to reseed than document data because it has no external corpus
to re-derive from if the JSONL log (§2) were ever lost — reinforcing why the JSONL log, not the
Qdrant collection, must be the durable source of truth, independent of which instance holds the
derived index.

---

## References

| Resource                                     | Location                                                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Memory type implementations                  | `core-component-00/context-engineering/implementations/memory_store.py`                     |
| Context compression (pre-write reduction)    | `core-component-00/context-engineering/implementations/context_compressor.py`               |
| RAG architecture / Corpus-as-Source-of-Truth | `core-component-00/retrieval-augmented-generation/architecture/overview.md` §10, §11        |
| Lightweight RAG deployment (Qdrant modes)    | `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md` |
| Retrieval/RRF fusion implementation          | `core-component-00/retrieval-augmented-generation/implementations/retrieval.py`             |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
