# Local RAG Deployment Proposal

**Document Type:** Strategic Deployment Proposal
**Prepared By:** Core Component 00 Laboratory — Dr. Elias Vance, Laboratory Director
**Date:** 2026-06-24
**Status:** Awaiting CEO Authorization
**Reference:** `telescope/2026-06-20-mcp-server-assessment/research-report.md`

---

## Executive Summary

The workspace's internal documentation — spanning company pipelines, studio operations, CC-00
research, and agent profiles — has grown to a scale where the current keyword-matching search
system fails to surface relevant information reliably. Claude Code agents are forced to browse
files manually for cross-module and conceptual queries, degrading quality and increasing session
length.

This proposal recommends a two-phase upgrade to the local RAG (Retrieval-Augmented Generation)
system that runs entirely on existing hardware with no cloud dependency. Phase 1 delivers
meaningful improvement within one working day using a proven information-retrieval algorithm
(BM25). Phase 2, in a following sprint, adds lightweight AI-powered semantic understanding using
a model small enough to run on any modern laptop CPU.

**Total estimated effort:** 3 days across two phases. **No new infrastructure. No recurring
costs.**

---

## Problem Statement

### The Gap

The current `workspace-knowledge` MCP server — the only tool available for querying workspace
documentation — uses a primitive term-counting approach: it scores documents by how many times a
search term appears verbatim. This approach fails in three common, high-value scenarios:

| Scenario                         | Example Query                                     | Why It Fails Today                                |
| -------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| **Synonym / paraphrase queries** | "context window management"                       | Won't match docs that say "token budget"          |
| **Cross-module lookups**         | "how does RAG connect to harness engineering?"    | Requires reading across two unrelated directories |
| **Research report discovery**    | "what did we investigate about hook engineering?" | `telescope/` is not included in the search index  |

The third failure is particularly costly: the Telescope research archive — the workspace's
institutional memory for past investigations — is completely invisible to the search system.
Every research report, including prior CEO-requested investigations, returns zero results.

### The Constraint

The workspace operates on a local-only repository with no remote and, per the CEO's assessment,
hardware that cannot support large AI models (which typically require 4–16 GB of GPU memory). Any
solution must:

- Run fully offline
- Operate on CPU without a GPU
- Require no external API calls or recurring costs
- Stay within approximately 400 MB of additional memory usage

---

## Proposed Solution Architecture

### Design Principle

> _An MCP server adds value only when it performs computation that Claude Code's native tools
> cannot replicate adequately. The workspace-knowledge server earns its place — it needs to earn
> it better._

The upgraded system replaces term-counting with two progressively more capable retrieval
strategies, introduced in phases to manage risk and validate each improvement before layering the
next.

---

### Phase 1 — BM25 with Metadata-Aware Chunking

**What it is:** BM25 (Best Match 25) is the industry-standard text-search algorithm used inside
Elasticsearch, Solr, and Lucene. It is significantly more accurate than term counting because it
accounts for how rare a term is across all documents (not just how often it appears in one). It
runs on CPU, requires no model files, and adds one lightweight Python library.

**What changes:**

1. The search engine in `workspace-knowledge/server.py` is rewritten from term-counting to BM25.
2. Documents are split into paragraph-sized chunks (≈512 words) rather than indexed as single
   large files. This means search results point to the relevant _section_ of a document, not the
   entire file.
3. Document headers and YAML metadata (title, date, module) are extracted and stored alongside
   each chunk as filterable fields.
4. The `telescope/` directory is added to the index, making all research reports searchable.
5. The index rebuilds automatically each time the server starts, ensuring newly created documents
   are always included.

**What this fixes:** Multi-word queries, phrase matching, and cross-document searches improve
substantially. Research reports become discoverable. Snippets returned are precise rather than
file-wide.

**What this does not fix:** Conceptual/synonym queries (e.g., "context window" ≠ "token budget")
still require the human to know the exact terminology used in the document. That is addressed in
Phase 2.

---

### Phase 2 — Hybrid Semantic + Keyword Retrieval

**What it is:** A small AI embedding model (`all-MiniLM-L6-v2`) converts each document chunk
and each query into a vector of numbers that encodes _meaning_, not just words. Chunks with
similar meaning score highly even when they use different vocabulary. The model is 80 MB — small
enough to run on any modern laptop CPU in under half a second per query.

**What changes:**

1. On first startup after Phase 2 deployment, the server generates embeddings for every indexed
   chunk and saves a compact search index (FAISS) to disk.
2. All subsequent startups load the index from disk in under two seconds — no re-embedding needed
   unless documents change.
3. When a query arrives, the server runs both BM25 (exact terms) and embedding search
   (semantic meaning), then combines the scores using a standard fusion algorithm (Reciprocal
   Rank Fusion). Results that rank highly in both methods rise to the top.

**What this fixes:** Synonym queries, paraphrase queries, and conceptual cross-references that
Phase 1 cannot handle. A query for "how do we handle errors in agent systems?" will now surface
documents discussing "exception recovery," "fault tolerance," and "harness safety" — even if the
word "errors" never appears in those documents.

---

## Hardware and Dependency Requirements

### Phase 1

| Item               | Requirement    | Notes                                    |
| ------------------ | -------------- | ---------------------------------------- |
| CPU                | Any modern CPU | No GPU required                          |
| RAM overhead       | < 100 MB       | Index held in process memory             |
| Disk               | < 5 MB         | Index is regenerated, not persisted      |
| New Python library | `rank_bm25`    | Install via `pip install rank_bm25`      |
| Python version     | 3.9+           | Already satisfied in current environment |

### Phase 2 (additive to Phase 1)

| Item                 | Requirement                          | Notes                                              |
| -------------------- | ------------------------------------ | -------------------------------------------------- |
| CPU                  | Any modern CPU                       | No GPU required; ~200–400 ms per query             |
| RAM overhead         | ~400 MB total                        | Model (~200 MB) + FAISS index (~varies by corpus)  |
| Disk                 | ~100–200 MB                          | Model file + persisted FAISS index                 |
| New Python libraries | `sentence-transformers`, `faiss-cpu` | Both CPU-native, no CUDA dependency                |
| Internet (first run) | Required once                        | Model downloads from Hugging Face on first startup |
| Internet (ongoing)   | Not required                         | Fully offline after first model download           |

> **Note on the one-time download:** `all-MiniLM-L6-v2` is approximately 80 MB and downloads
> automatically on first server startup after Phase 2 is deployed. Subsequent startups load the
> model from disk. No recurring internet access is needed.

---

## Phased Implementation Roadmap

### Phase 1 — BM25 Upgrade (Estimated: 1–2 working days)

| Step | Task                                                                                     | Effort |
| ---- | ---------------------------------------------------------------------------------------- | ------ |
| 1    | Install `rank_bm25` into workspace Python environment                                    | 5 min  |
| 2    | Rewrite `workspace-knowledge/server.py` search engine                                    | 4 hrs  |
| 3    | Add paragraph chunking with header metadata extraction                                   | 2 hrs  |
| 4    | Expand `key_dirs` to include `telescope/`                                                | 15 min |
| 5    | Update tool description strings (remove false "semantic" claim)                          | 15 min |
| 6    | Implement graceful-degradation three-tier fallback (Hybrid → BM25 → Raw FS) with `_meta` | 4 hrs  |
| 7    | Manual validation: run representative queries, confirm improvement                       | 30 min |
| 8    | Prettier format + commit                                                                 | 15 min |

**Acceptance criteria:**

- [ ] Query for "context window management" returns results from token budget documents
- [ ] Query for "MCP server assessment" returns the Telescope research report
- [ ] Snippets are paragraph-level, not full-file dumps
- [ ] Server starts and indexes all directories including `telescope/` in under 5 seconds
- [ ] Server returns valid results when `rank_bm25` is uninstalled (Raw FS disaster-recovery tier active)
- [ ] Every query response includes a `_meta.search_tier` field declaring the active retrieval tier

---

### Phase 2 — Semantic Embeddings (Estimated: 2 working days, following sprint)

| Step | Task                                                                 | Effort |
| ---- | -------------------------------------------------------------------- | ------ |
| 1    | Install `sentence-transformers` and `faiss-cpu`                      | 10 min |
| 2    | Implement embedding pipeline for indexed chunks                      | 4 hrs  |
| 3    | Build and persist FAISS index to disk                                | 2 hrs  |
| 4    | Implement Reciprocal Rank Fusion for hybrid BM25 + embedding scoring | 3 hrs  |
| 5    | Add mtime-based delta detection (re-embed only changed files)        | 2 hrs  |
| 6    | Benchmark: measure query latency on full corpus                      | 1 hr   |
| 7    | Validation: synonym queries, cross-module conceptual queries         | 1 hr   |
| 8    | Prettier format + commit                                             | 15 min |

**Acceptance criteria:**

- [ ] Query for "context window management" returns documents using "token budget" terminology
- [ ] Query latency under 500 ms at p95 for corpus of current size
- [ ] FAISS index persists between server restarts (no re-embedding on restart)
- [ ] Model loads from disk on subsequent startups (no internet required after first run)
- [ ] Re-indexing triggered only for files modified since last index build

---

## Risk Assessment

| Risk                                                | Likelihood | Impact | Mitigation                                                |
| --------------------------------------------------- | ---------- | ------ | --------------------------------------------------------- |
| BM25 improves recall but query quality disappoints  | Low        | Low    | Evaluate with representative queries before Phase 2       |
| `sentence-transformers` install conflict            | Low        | Medium | Use isolated virtual environment; tested library          |
| First-run model download fails (no internet)        | Medium     | Low    | Manual download and local placement as fallback           |
| RAM overhead exceeds hardware capacity              | Low        | High   | Monitor at Phase 2 deploy; fallback to Phase 1 only       |
| FAISS index becomes stale after large doc additions | Low        | Medium | `rebuild_index` tool remains available for manual refresh |
| Phase 2 query latency exceeds 500 ms                | Low        | Low    | FAISS Flat index scales well to current corpus size       |

**Worst-case outcome:** Phase 2 RAM overhead or latency is unacceptable on the hardware. In this
case, Phase 1 (BM25 only) remains as the permanent solution — it is already a significant
improvement over the current state and carries zero hardware risk.

---

## Complementary Tool Extensions

Upon successful Phase 1 and Phase 2 deployment, seven additional tool endpoints can be added to
the same `workspace-knowledge` server at no additional infrastructure cost. These tools pass the
MCP Inclusion Charter three-gate test and address high-value capability gaps not covered by the
core RAG upgrade:

| Phase Dependency | Tool                         | Capability Gap                                               |
| ---------------- | ---------------------------- | ------------------------------------------------------------ |
| Phase 1          | `summarize_context`          | Pre-digests multi-document briefings for agent context slots |
| Phase 1          | `check_adr_precedent`        | Surfaces prior ADRs before a Technology Decision is made     |
| Phase 1          | `validate_pipeline_document` | Validates document structure against canonical pipeline spec |
| Phase 2          | `find_related_documents`     | Returns semantically similar documents to a seed file        |
| Phase 2          | `list_research_by_topic`     | Makes Telescope archive discoverable by topic cluster        |
| Phase 2          | `agent_knowledge_brief`      | Compiles full agent activation packet on demand              |

These extensions are out of scope for the current authorization request and are presented for the
CEO's awareness as a logical Phase 3 roadmap. Full specifications are in the research report (R7).

---

## What This Proposal Does Not Include

To keep scope clear, the following are explicitly out of scope for this proposal:

- **Cloud RAG services** (e.g., OpenAI embeddings, Cohere) — ruled out due to offline-first
  requirement and recurring cost
- **Large local models** (e.g., Ollama, LLaMA, Mistral) — ruled out due to hardware constraints
- **Cross-server RAG** (indexing external sources beyond the workspace) — out of scope
- **`pipeline-automation` or `cc00-tools` upgrades** — separate retirement decision, covered in
  the main research report

---

## CEO Authorization

This proposal is submitted for review and authorization. Upon approval, Phase 1 implementation
will commence immediately with no dependency on external resources or procurement.

| Decision                                 | Authorization |
| ---------------------------------------- | ------------- |
| Authorize Phase 1 (BM25 upgrade)         | ☐ Yes / ☐ No  |
| Authorize Phase 2 (Semantic embeddings)  | ☐ Yes / ☐ No  |
| Defer both phases pending further review | ☐ Yes / ☐ No  |

**Notes / Conditions:**

> _(CEO to complete)_

---

**Prepared by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Reviewed by:** _(pending CEO sign-off)_
**Document version:** 1.1 — 2026-06-24
