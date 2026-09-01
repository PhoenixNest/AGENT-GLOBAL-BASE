# Technical Options — Persistent Agent Memory on Qdrant

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md)
> **Audience:** Engineers implementing or extending the memory store — and anyone else who wants
> to understand how it actually stores things, without needing a database background.
> **Last Updated:** 2026-08-10

---

## 1. What This Document Covers

This document specifies **how memory is technically stored** — not the forgetting/decay policy
(see [03-forgetting-strategy.md](03-forgetting-strategy.md)) and not step-by-step deployment
instructions (see [02-deployment-guidelines.md](02-deployment-guidelines.md)). It extends the
workspace's existing lightweight Qdrant-based retrieval system
([lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md))
that already powers document search — the same underlying technology, applied to a new kind of
content: things an AI agent has said, decided, or learned, rather than documents someone wrote.

---

## 2. Foundational Decision: Memory Is Primary Data, Not a Derived Index

The workspace's retrieval system has a standing rule: a search index (the fast lookup structure
that makes semantic search possible) should always be a _disposable, rebuildable copy_ of some
underlying document — never the only place information exists. Agent memory breaks that
assumption in one specific way: a memory record (a decision, a corrected fact, a distilled
summary of a past conversation) is **created at the moment the agent writes it** — there's no
prior document it was copied from. If it only lived inside the search index, an accidental index
rebuild would be _destructive_ instead of merely slow, which violates the workspace's own rule.

**The fix — "Memory-as-Corpus":** every memory write is first appended to a durable,
human-readable log file (JSONL — one JSON object per line, plain text, readable in any editor).
That log file is the actual source of truth. The Qdrant search index is a **derived copy** built
from the log, exactly the same relationship the existing document knowledge base already has with
its own Markdown files. This means the same four-tier fallback plan that protects document search
(see [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md)) can, in principle, apply to memory too — because
the log is just plain text, nothing fancy is required to read it directly if the search index is
ever unavailable.

```
Agent turn → MemoryStore API call → append to <type>.jsonl (source of truth)
                                          ↓ (synchronous upsert, see 02-deployment-guidelines.md)
                                    Qdrant collection (derived index)
```

---

## 3. Collection Design

Use **one Qdrant collection per memory type**, not a single shared collection with a "which type
is this" filter. The reason: each type is queried differently and kept for a different length of
time. A conversation-scoped memory ("in this session, the user asked me to check X") is looked up
by session and recency; a durable fact ("the user prefers metric units") is looked up by meaning,
across every session. Cramming them into one collection would force every cleanup pass to scan the
whole thing instead of working on just the relevant slice, and would tie unrelated retention
rules to one shared configuration.

| Collection          | Backs                                                                                                                            | Retention                                                                                                                                          | Primary Query Pattern                                     |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `memory_episodic`   | Individual conversation events                                                                                                   | Session-scoped; decays per [03-forgetting-strategy.md](03-forgetting-strategy.md)                                                                  | Filtered by session, sorted by recency; rarely by meaning |
| `memory_semantic`   | Durable, cross-session facts                                                                                                     | Persistent; fades by importance                                                                                                                    | Meaning-based search across all sessions                  |
| `memory_procedural` | Runtime-learned corrections                                                                                                      | Persistent — but see § 7: the _primary_ form of procedural knowledge in this workspace is still plain skill/profile documents, not this collection | Meaning-based search, filtered by which skill it corrects |
| `memory_reflection` | **Not in the original design** — added later in implementation, one log + one Qdrant collection, same pattern as the other three | Persistent                                                                                                                                         | Same pattern as `memory_semantic`                         |

`WorkingMemory` (the agent's in-the-moment scratch space during a single turn) is **never**
persisted to Qdrant — it lives only in the active context window and is cleared every turn.
Persisting it would defeat its purpose (disposable, task-scoped state) for no retrieval benefit.

**Correction (2026-08-10):** the original version of this document scoped exactly three
persisted memory types. The live codebase (`memory_vector_store.py`) actually maintains a fourth,
`memory_reflection`, with its own log file and its own Qdrant collection, following the same
Memory-as-Corpus pattern as the other three. This wasn't a deviation anyone needs to undo — it's
simply something the original design didn't anticipate and this document previously didn't
mention. No further engineering action is implied here; this is a documentation correction only.

### 3.1 Payload Schema (all four collections share this superset; unused fields are omitted per type)

```json
{
  "id": "uuid4",
  "memory_type": "episodic | semantic | procedural | reflection",
  "content": "string — the fact, event, correction, or reflection text",
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
  "media_ref": "string | null — see § 3.2, null for text"
}
```

See [03-forgetting-strategy.md](03-forgetting-strategy.md) § 3 for how `importance`, `decay_weight`, and `status` are
computed and change over time. A memory marked `sacred = true` (a decision or firm commitment) is
the one kind of record that skips almost all of this — it never decays and is always returned.

### 3.2 Multimodal Memory (Images, Audio)

Regardless of `modality`, the field that actually gets searched is always `content` — plain text.
For a non-text memory, `content` holds a **derived textual description** — an image caption or an
audio transcript — that the model writes for itself at the moment it originally sees or hears the
media, using its own native understanding of what's in front of it. The raw media file itself is
never embedded and never stored in Qdrant; it's saved to disk, and `media_ref` points to where.

This follows directly from § 2's core principle rather than introducing a new one: a derived
description (the caption) should never be the _only_ surviving copy of the thing it describes —
the same reasoning that makes the log file, not the search index, the source of truth for text
memory. Looking up a multimodal memory later is a two-step process: search over `content` as
normal, then optionally read the file at `media_ref` if the agent needs to look at the original
media again rather than trust its own past description of it.

**An external document-conversion tool is deliberately not used for this path.** That kind of tool
(OCR/transcription for _externally sourced_ files — PDFs, screenshots, recordings someone else
made) belongs to the separate document-knowledge-base pipeline. Routing a memory write back
through it would throw away information the model already extracted natively in the moment, for
no benefit.

Very long content should be shortened with the workspace's existing summarization tool
(`context_compressor.py`) _before_ being written as `content` — the same rule applies whether the
source was a long audio transcript or a long piece of text; there's no separate chunking step (see
§ 5). Embedding today is caption-then-text, using the same lightweight model as everything else
(§ 4) — a model that understands images and audio jointly, without a captioning step first, is a
possible future upgrade, not a current requirement.

---

## 4. Embedding Model

**In production, the embedding model is `all-MiniLM-L6-v2`** (384-dimensional vectors) — the
lightweight model already used elsewhere in this workspace's retrieval stack, chosen because
memory is written on nearly every agent turn, so write speed matters more here than it does for
the document knowledge base, which writes far less often and uses a higher-quality (but slower)
model instead. Using two different models across the two systems is fine: each Qdrant collection
is configured independently, and nothing ever compares a memory vector to a document vector
directly.

**One addition since the original design (not a change to the model choice itself):** both this
system and the document knowledge base now route their embedding calls through a small shared
background process, `embedder-service`, that loads the model once and serves requests over a
local connection — instead of each system loading its own copy of the model into memory
separately. If that shared process is ever unavailable, this system falls back to its old
behavior (loading the model directly, in-process) automatically — nothing breaks, it's just
slightly slower to start. This is purely an efficiency detail; it doesn't change which model is
used or what gets embedded.

---

## 5. Chunking Strategy: None

Document chunking (splitting a long document into overlapping pieces before embedding — see
`retrieval-augmented-generation/fundamentals/`) doesn't apply to memory. A memory record is
already a single, complete unit by construction: one event, one fact, one correction. Splitting an
already-atomic record into pieces would fragment a single decision across multiple search results
for no benefit. If one memory's content is unusually long, shorten it with the summarization tool
_before_ writing it (§ 3.2) — don't chunk it after.

---

## 6. Retrieval Strategy

Retrieval follows the same "combine meaning-based search with keyword search" principle already
required for the document knowledge base, reusing the same fusion logic. Two modes:

| Mode                    | Used For                                                 | How It Works                                                                     |
| ----------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Recency-filtered**    | "What happened recently in this conversation?"           | Filter by session + sort by time — no embedding needed, so it's essentially free |
| **Semantic similarity** | "What do we already know that's relevant to this topic?" | Meaning-based search + keyword search, combined, restricted to active records    |

A `sacred = true` record (a decision or commitment) is always included in recency-filtered
retrieval no matter what its decay-driven status is — this preserves an existing rule elsewhere in
the codebase that a firm decision is always returned verbatim, never silently filtered out.

---

## 7. Procedural Memory Stays File-Based

The workspace's real, canonical form of "procedural knowledge" (how an agent should behave) is not
a vector store at all — it's the plain `profile.md` and `skills/*.md` files that already govern
agent behavior. `memory_procedural` in Qdrant exists for a narrower purpose only: a runtime-learned
correction that hasn't yet been promoted into an actual skill-file edit (for example, "the user
corrected a retry threshold from 5 to 3 on a specific date"). If the same correction shows up
again across three or more separate sessions, treat that as a signal to make it a real
documentation change — at that point it becomes canonical, and the memory record can be archived.

---

## 8. Deployment Mode

Follow the workspace's existing rule without exception: Qdrant runs in Docker/Server mode only,
never the alternative "embedded" mode — the two store data in incompatible formats, so mixing them
is not an option (see [lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md)).

**Memory runs on its own dedicated Qdrant instance, entirely separate from the document knowledge
base's instance.** This was a deliberate choice, not a convenience default: the two systems serve
different jobs (a curated document library vs. fast-changing, per-session agent memory), write at
very different rates (documents occasionally, memory almost every turn), and benefit from
independent failure domains — a memory-instance outage shouldn't take document search down with
it, or vice versa. A single shared instance with a "which system does this belong to" filter was
considered and rejected: it would technically separate the _data_, but not the _blast radius_, the
_workload_, or the _security boundary_ — all things this design specifically wanted, independent
of today's single-machine hardware. See [02-deployment-guidelines.md](02-deployment-guidelines.md) § 1 for the actual container
setup.

Memory is materially harder to recreate from scratch than document data, because it has no
external source document to regenerate from if the log file were ever lost — which is exactly why
§ 2's rule (the log file, not the search index, is the permanent record) matters so much here.

**Verified against the live codebase (2026-08-10):** every claim in §§ 3–8 above about what is
_actually implemented_ — separate collections, the 384-dimension embedding vectors, the
JSONL-log-as-source-of-truth pattern — was directly confirmed against the running code as of this
rewrite. See [00-sources-and-references.md](00-sources-and-references.md) § 6 for the full mechanism-by-mechanism audit,
including the two mechanisms that are _not_ fully built yet (contradiction checking and the
in-between fallback tiers) — neither of which is a storage/collection-design matter, so neither
changes anything in this document.

---

## References

| Resource                                     | Location                                                                                                                                                                                                                   |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Memory type implementations                  | [memory_store.py](core-component-00/framework/02-context-engineering/implementations/memory_store.py), [memory_vector_store.py](core-component-00/framework/02-context-engineering/implementations/memory_vector_store.py) |
| Context compression (pre-write reduction)    | [context_compressor.py](core-component-00/framework/02-context-engineering/implementations/context_compressor.py)                                                                                                          |
| RAG architecture / Corpus-as-Source-of-Truth | [overview.md](core-component-00/framework/04-retrieval-augmented-generation/architecture/overview.md) §§ 10–11                                                                                                             |
| Lightweight RAG deployment (Qdrant modes)    | [lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md)                                                                                    |
| Retrieval / fusion implementation            | [retrieval.py](core-component-00/framework/04-retrieval-augmented-generation/implementations/retrieval.py)                                                                                                                 |
| Shared embedder process                      | [embedder-service/server.py](core-component-00/platform/model-context-protocol-servers/_shared/embedder-service/server.py)                                                                                                 |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
