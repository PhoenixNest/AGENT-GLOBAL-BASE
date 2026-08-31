# Enterprise-Level Engineering Assessment — Retrieval-Augmented Generation (Layer 4)

---

## Metadata

| Field                           | Value                                                             |
| ------------------------------- | ----------------------------------------------------------------- |
| **Assessment ID**               | `2026-08-16-retrieval-augmented-generation-enterprise-assessment` |
| **Date**                        | 2026-08-16                                                        |
| **Assessor**                    | Sofia Almeida (Senior Research Engineer, RAG module lead)         |
| **Reviewer**                    | Dr. Elias Vance (Laboratory Director) — reviewed 2026-08-16       |
| **Module(s) / System Assessed** | `core-component-00/framework/04-retrieval-augmented-generation/`               |
| **Requestor**                   | CEO, via user — Layer 4 of the CC-00 enterprise benchmark series  |
| **Prior Assessment**            | None — first pass                                                 |

---

## Research Freshness (Mandatory)

**Knowledge cutoff of assessor:** January 2026 — no claim in this document rests on training-data
recall. Every external row below was retrieved by fetching the source page itself this session and
copying the supporting text out of it; every internal row was produced by opening the cited file
this session.

**Live research performed this session:** Yes

### Source Register

| ID  | Claim Supported                                                                                           | Query Run                                                                               | Source                                                                                                                                                                                                                  | Retrieval Date | Verbatim Excerpt                                                                                                                                                                                                                                           | Status                                     |
| --- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| S1  | Hybrid retrieval is the enterprise default and measurably improves retrieval recall over a single leg     | "enterprise RAG 2026 hybrid retrieval reranking chunking performance"                   | [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)                                                            | 2026-08-16     | "Enterprises that default to hybrid retrieval report 20–40% higher retrieval recall in benchmarked scenarios."                                                                                                                                             | Verified — excerpt supports claim          |
| S2  | Access control should be enforced inside the retrieval query so unauthorized documents are never returned | "RAG vector database permission filtering at query time payload filter enterprise 2026" | [Permission-Aware Retrieval: Why Access Control in Enterprise RAG Must Live in the Vector Layer — TianPan.co](https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control)              | 2026-08-16     | "At query time, the retrieval query includes a filter that restricts results to chunks the requesting user has permission to see. The vector store never returns an unauthorized document in the first place."                                             | Verified — excerpt supports claim          |
| S3  | Retrieving unfiltered then discarding disallowed results is an identified failure mode                    | "RAG vector database permission filtering at query time payload filter enterprise 2026" | [Permission-Aware Retrieval — TianPan.co](https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control)                                                                                  | 2026-08-16     | "query the vector store without filters, retrieve the top-k documents, then discard results the user isn't allowed to see. This has two failure modes."                                                                                                    | Verified — excerpt supports claim          |
| S4  | Robust pipelines apply access filtering at both ingestion and retrieval — defense in depth, not either/or | "RAG PII masking access control enterprise security best practices 2026"                | [RAG Pipeline Security Best Practices for 2026 — Kiteworks](https://www.kiteworks.com/cybersecurity-risk-management/rag-pipeline-security-best-practices/)                                                              | 2026-08-16     | "Robust RAG pipelines apply both pre-filtering at ingestion and post-filtering at retrieval." … "Pre-filtering blocks unauthorized data from ever being indexed; retrieval filters verify that authorization remains valid at the exact moment of access." | Verified — excerpt supports claim          |
| S5  | PII/PHI should be redacted or tokenized before the embedding step                                         | "RAG PII masking access control enterprise security best practices 2026"                | [RAG Pipeline Security Best Practices for 2026 — Kiteworks](https://www.kiteworks.com/cybersecurity-risk-management/rag-pipeline-security-best-practices/)                                                              | 2026-08-16     | "Protected health information (PHI) and personally identifiable information (PII) should be redacted or tokenized before embedding."                                                                                                                       | Verified — excerpt supports claim          |
| S6  | Sought: an external source establishing PII masking as a _mandatory_ RAG control                          | "RAG PII masking Elasticsearch LlamaIndex sensitive data"                               | [RAG: How to protect sensitive and PII info with Elasticsearch & LlamaIndex — Elastic Search Labs](https://www.elastic.co/search-labs/blog/rag-security-masking-pii)                                                    | 2026-08-16     | "It is highly recommended to test these approaches based on your usecase and needs before adopting." … "we will explore options on how to Mask PII information"                                                                                            | Partial — excerpt supports a weaker claim  |
| S7  | Cross-encoder reranking measurably improves retrieval precision                                           | "enterprise RAG 2026 hybrid retrieval reranking chunking performance"                   | [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)                                                            | 2026-08-16     | "Cross-encoder re-ranking improves precision by 18–42%"                                                                                                                                                                                                    | Verified — excerpt supports claim          |
| S8  | Two-stage retrieval retrieves a wide candidate set, reranks it, and passes a narrow set to the LLM        | "RAG best practices chunking embeddings reranking hybrid search enterprise"             | [RAG Best Practices for Enterprise AI — StackAI](<https://www.stackai.com/insights/retrieval-augmented-generation-(rag)-best-practices-for-enterprise-ai-chunking-embeddings-reranking-and-hybrid-search-optimization>) | 2026-08-16     | "Retrieve topM candidates: 50–200" … "Rerank all candidates" … "Keep topK for context: 5–12"                                                                                                                                                               | Verified — excerpt supports claim          |
| S9  | Semantic chunking outperforms fixed-size chunking on a published enterprise benchmark                     | "enterprise RAG 2026 hybrid retrieval reranking chunking performance"                   | [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)                                                            | 2026-08-16     | "One of the most striking insights from FloTorch's FinanceBench evaluations is the impact of chunk segmentation on RAG accuracy:" … "Semantic chunking (no metadata): 42%" … "Fixed chunking + metadata: 25%"                                              | Verified — excerpt supports claim          |
| S10 | Semantic chunking is called mandatory for production-grade RAG in regulated/technical corpora             | "enterprise RAG 2026 hybrid retrieval reranking chunking performance"                   | [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)                                                            | 2026-08-16     | "In financial, compliance, and technical corpora, semantic chunking is now mandatory for production-grade RAG"                                                                                                                                             | Verified — excerpt supports claim          |
| S11 | Counter-position sought on S10: is a single chunking strategy universally prescribed?                     | "RAG best practices chunking embeddings reranking hybrid search enterprise"             | [RAG Best Practices for Enterprise AI — StackAI](<https://www.stackai.com/insights/retrieval-augmented-generation-(rag)-best-practices-for-enterprise-ai-chunking-embeddings-reranking-and-hybrid-search-optimization>) | 2026-08-16     | "There isn't one universal approach. The best strategy depends on document structure and how users ask questions."                                                                                                                                         | Contradicted — source states the opposite  |
| S12 | Automated staleness alerting to a responsible team is current practice                                    | "RAG index freshness staleness monitoring document owner escalation enterprise 2026"    | [The Knowledge Decay Problem — RAG About It](https://ragaboutit.com/the-knowledge-decay-problem-how-to-build-rag-systems-that-stay-fresh-at-scale/)                                                                     | 2026-08-16     | "When freshness score drops below 85%, automated alerts notify the knowledge management team"                                                                                                                                                              | Partial — excerpt supports a weaker claim  |
| S13 | Sought: per-document-owner notification with an escalation path when owners are unresponsive              | "RAG index freshness staleness monitoring document owner escalation enterprise 2026"    | —                                                                                                                                                                                                                       | 2026-08-16     | —                                                                                                                                                                                                                                                          | Searched — no supporting source found      |
| S14 | `pipeline.query()` runs a BM25 leg and a vector leg and merges them with RRF                              | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:103-120`                                                                                                                                  | 2026-08-16     | "bm25_results = bm25_score(query, corpus)[: self.top_k \* 2]" … "raw = self.vector_store.search(q_vector, top_k=self.top_k \* 2)" … "fused = rrf_fusion(lists_to_fuse)[: self.top_k \* 2]"                                                                 | Internal — verified against primary source |
| S15 | RRF smoothing constant is 60, matching the RRF paper's default                                            | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/retrieval.py:96,102`                                                                                                                                  | 2026-08-16     | "k: int = 60," … "k: Smoothing constant (default 60, per the RRF paper)."                                                                                                                                                                                  | Internal — verified against primary source |
| S16 | ACL is applied only after fusion, on an already-retrieved in-memory list                                  | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:120-123`                                                                                                                                  | 2026-08-16     | "fused = rrf_fusion(lists_to_fuse)[: self.top_k \* 2]" … "# ACL filter" … "accessible = acl_filter(fused, user_role)[: self.top_k]"                                                                                                                        | Internal — verified against primary source |
| S17 | `acl_filter()` is a pure post-hoc list filter with no index/query-side hook                               | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/retrieval.py:127-153`                                                                                                                                 | 2026-08-16     | "def acl_filter(\n results: List[ScoredDocument],\n user_role: str,\n) -> List[ScoredDocument]:" … "Args:\n results: Ranked documents to filter."                                                                                                          | Internal — verified against primary source |
| S18 | PII masking is a mandatory ASGF compliance control for this module                                        | [n/a — internal]                                                                        | `.claude/rules/rag-engineering.md:47,50,58`                                                                                                                                                                             | 2026-08-16     | "## Security Controls (Mandatory for ASGF Compliance)" … "- **PII Masking:** Redact sensitive information before retrieval" … "2. Apply ACL filtering and PII masking (ASGF compliance requirement)"                                                       | Internal — verified against primary source |
| S19 | No PII-masking and no reranking code exists in the module's shipped Python                                | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/` and `testing/` — 7 `.py` files, searched this session                                                                                               | 2026-08-16     | Case-insensitive search for `pii\|mask\|redact\|rerank` across `__init__.py`, `chunker.py`, `pipeline.py`, `retrieval.py`, `conftest.py`, `test_chunking.py`, `test_pipeline.py`, `test_retrieval.py` returned **zero matches**                            | Internal — verified against primary source |
| S20 | The module's own README prescribes cross-encoder reranking as a best practice                             | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/README.md:110,124`                                                                                                                                                    | 2026-08-16     | "\| **Multi-Stage Reranking** \| Applies coarse-to-fine filtering for optimal retrieval quality \|" … "\| Reranking \| Always use a cross-encoder reranker (bge-reranker) with top-K=10 before context assembly \|"                                        | Internal — verified against primary source |
| S21 | `RAGPipeline` defaults to `FixedSizeChunker` when no chunker is injected                                  | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:50`                                                                                                                                       | 2026-08-16     | "self.chunker = chunker or FixedSizeChunker()"                                                                                                                                                                                                             | Internal — verified against primary source |
| S22 | Semantic and hybrid chunkers are implemented and available for injection                                  | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/implementations/chunker.py:36,71,125`                                                                                                                                 | 2026-08-16     | "class FixedSizeChunker:" … "class SemanticChunker:" … "class HybridChunker:"                                                                                                                                                                              | Internal — verified against primary source |
| S23 | Freshness is handled as a write-time debounce policy, with no alerting component described                | [n/a — internal]                                                                        | `core-component-00/framework/04-retrieval-augmented-generation/CLAUDE.md` § Active Research Programme                                                                                                                                | 2026-08-16     | "Staleness in agent-native deployments is a policy variable — the debounce threshold of a post-write hook — not an architectural invariant."                                                                                                               | Internal — verified against primary source |
| S24 | The module's test suite is green as of this session                                                       | [n/a — internal]                                                                        | `pytest retrieval-augmented-generation/testing/ -q`, run 2026-08-16                                                                                                                                                     | 2026-08-16     | "61 passed in 0.10s"                                                                                                                                                                                                                                       | Internal — verified against primary source |

### Notes on Two Rows

**S6 is registered but not cited as evidence for anything.** It was retrieved while looking for an
external source that makes PII masking mandatory. Read on its own, the excerpt establishes the
opposite posture — masking presented as an option to evaluate, not a requirement — so it cannot
carry the mandatory framing the PII finding needs. That framing comes from S18, an internal rule,
which is where it genuinely lives. S5 corroborates the _practice_ (redact before embedding) without
being asked to carry the word "mandatory."

**S11 contradicts S10 and both are reported.** Flotorch states semantic chunking is now mandatory
in regulated corpora; StackAI states there is no universal approach. Benchmark row B5 states both
positions rather than picking whichever one made our default look worse.

---

## Assessment Scope

### What Was Assessed

`implementations/chunker.py` (FixedSizeChunker, SemanticChunker, HybridChunker),
`implementations/retrieval.py` (bm25_score, rrf_fusion, acl_filter),
`implementations/pipeline.py` (RAGPipeline end-to-end orchestration), and the module's
`testing/` pytest suite — benchmarked against current external enterprise RAG practice on six
dimensions: hybrid retrieval, access-control placement, PII handling, reranking, chunking
strategy, and retrieval freshness.

### Why Now

Layer 4 of the CEO-directed enterprise benchmark series, run in the canonical layer order defined
by `core-component-00/platform/benchmarks/CLAUDE.md` § Layer Sequence.

### Out of Scope

- **The production reference deployment** (`core-component-00/platform/model-context-protocol-servers/workspace-knowledge/`).
  It is a separate MCP server governed by `.claude/rules/mcp-governance.md`, not this
  reference-implementation module. Findings here describe the reference implementation only.
- **Cross-module dependency integrity** (Context Engineering's `memory_vector_store.py` loading
  this module's `bm25_score`). Verified sound this session, but "does our own wiring still match
  our own docs" is an internal-consistency question, not a benchmark against external practice —
  it belongs to an ASGF compliance audit, per this template's guidance.
- **Test/CI gating discipline.** The suite is green (S24), but no external source was sought or
  quoted for what enterprise CI gating requires, so no benchmark row was written for it rather
  than asserting a standard from recall.

---

## Verdict Vocabulary

This assessment uses the template's fixed vocabulary: **Pass at parity**, **Pass, ahead**,
**Partial**, **Gap**, **N/A**, **Unassessed — no source**.

---

## Benchmark Table

| ID  | Dimension                           | Our Current State                                                                                                                                                                                                                     | Internal Source ID(s) | Enterprise-Standard Practice                                                                                                                                                                                                                                                                  | External Source ID(s) | Verdict                | Severity |
| --- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------- | -------- |
| B1  | Hybrid retrieval architecture       | `pipeline.query()` runs a BM25 leg and a vector leg over the same corpus and merges the two ranked lists with Reciprocal Rank Fusion at k=60                                                                                          | S14, S15              | Hybrid retrieval is the enterprise default, reported at 20–40% higher retrieval recall than a single-leg baseline                                                                                                                                                                             | S1                    | Pass at parity         | —        |
| B2  | Access-control placement            | ACL is enforced once, as `acl_filter()` on the already-fused in-memory result list; no role parameter reaches `vector_store.search()` or the BM25 candidate selection, and the `top_k` slice is applied after filtering               | S16, S17              | Access filtering belongs in the retrieval query itself so the store never returns an unauthorized document (S2); retrieving unfiltered and then discarding is a named failure mode (S3); robust pipelines run **both** an ingestion-side pre-filter and a retrieval-side filter (S4)          | S2, S3, S4            | Partial                | P1       |
| B3  | PII masking before embedding        | No PII detection, masking, or redaction code exists anywhere in `implementations/` or `testing/` — a case-insensitive search of all 7 module `.py` files returned zero matches — while the module's governing rule names it mandatory | S18, S19              | PHI and PII should be redacted or tokenized before the embedding step                                                                                                                                                                                                                         | S5                    | Gap                    | P1       |
| B4  | Reranking stage                     | `pipeline.query()` goes fusion → ACL filter → `top_k` slice with no rescoring stage and no injection point for one, while the README prescribes a cross-encoder reranker                                                              | S19, S20              | Two-stage retrieval retrieves 50–200 candidates, reranks them all, and keeps 5–12 for the LLM (S8); cross-encoder reranking is reported to improve precision by 18–42% (S7)                                                                                                                   | S7, S8                | Gap                    | P2       |
| B5  | Default chunking strategy           | `RAGPipeline.__init__` falls back to `FixedSizeChunker()` when no chunker is injected; `SemanticChunker` and `HybridChunker` are implemented, tested, and injectable but are not the default                                          | S21, S22              | Sources diverge and both positions are reported: Flotorch measures semantic 42% vs fixed 25% on FinanceBench (S9) and calls semantic chunking mandatory for financial/compliance/technical corpora (S10); StackAI states "There isn't one universal approach" and ties choice to corpus (S11) | S9, S10, S11          | Partial                | P2       |
| B6  | Retrieval freshness handling        | Freshness is resolved as a write-time policy variable — the debounce threshold of a post-write index-sync hook — with no monitoring or alerting component described                                                                   | S23                   | Narrower claim, matching the excerpt: a freshness score is tracked and automated alerts notify a responsible team when it drops below a threshold                                                                                                                                             | S12                   | Partial                | P3       |
| B7  | Owner escalation on stale documents | Not present; would sit on top of the B6 hook if adopted                                                                                                                                                                               | S23                   | —                                                                                                                                                                                                                                                                                             | S13                   | Unassessed — no source | —        |

**Note on B2's verdict.** This is `Partial`, not `Gap`. S4 describes two filtering layers and we
implement one of them correctly — the retrieval-side check. The named missing element is the
query-side push-down described by S2: no role or permission predicate is passed into
`vector_store.search()`, so a consumer swapping in a real vector store inherits fetch-then-filter
by default. A secondary consequence visible in the code (S16): because ACL runs on a `top_k * 2`
candidate window and the `top_k` slice follows it, a restricted role can silently receive fewer
than `top_k` results.

---

## Severity-Ordered Remediation Plan

**Declared scale for this assessment:** **Scale A — ASGF Gap Severity**. The assessed surface is a
CC-00 engineering module's reference implementation, not a shipping product surface, so Scale A
governs and these findings compose with any follow-on ASGF audit.

| ID  | Priority | Benchmark Row | Gap                                                                                                      | Source ID(s)           | Owner         | Fix                                                                                                                                                                                                                     | Severity Justification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --- | -------- | ------------- | -------------------------------------------------------------------------------------------------------- | ---------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | P1       | B2            | ACL enforced only as a post-fusion in-memory filter; no permission predicate reaches the retrieval query | S2, S3, S4, S16, S17   | Sofia Almeida | Thread `user_role` into `vector_store.search()` as a filter predicate and into the BM25 leg's candidate selection, keeping `acl_filter()` as the second layer S4 describes; document the two-layer pattern for adapters | ASGF Scale A — P1: "Gap that will degrade output quality or reliability at scale but does not cause outages." The single implemented layer is correct and tested, so no leak occurs in this module today; what degrades is reliability of the pattern consumers inherit — a real vector store filtered only after the fact, plus the truncated-result-set effect in S16. **Explicitly not P0:** P0 requires a gap that "will cause production failure under normal load or after extended sessions," and this has no load or session-length trigger and has produced no failure. |
| R2  | P1       | B3            | PII masking entirely unimplemented despite being a mandatory ASGF control for this module                | S5, S18, S19           | Diego Fontán  | Add a masking step between chunking and embedding, invoked from `RAGPipeline.ingest()` before `self.embedder(chunk.text)`, with a dedicated test file under `testing/`                                                  | ASGF Scale A — P1: "Gap that will degrade output quality or reliability at scale but does not cause outages." A named-mandatory control at zero implementation is a compliance and reliability defect in the reference pattern. **Explicitly not P0:** the module ships no data and serves no traffic, so it cannot "cause production failure under normal load"; the exposure is inherited by consumers, not realised here.                                                                                                                                                     |
| R3  | P2       | B4            | No reranking stage and no injection point for one, contradicting the module's own README                 | S7, S8, S19, S20       | Sofia Almeida | Add an injectable `reranker` callable to `RAGPipeline`, mirroring the existing `embedder`/`vector_store` injection pattern, defaulting to a pass-through so the code matches the documented practice                    | ASGF Scale A — P2: "Gap that reduces engineering maintainability or makes the system harder to extend." The pipeline's injectable-dependency design is precisely the extension mechanism, and it has no seam for the one stage S7/S8 identify as the highest-leverage quality lever — a consumer must fork `query()` rather than inject.                                                                                                                                                                                                                                         |
| R4  | P2       | B5            | Zero-argument default is `FixedSizeChunker`, the weaker arm of S9's measured comparison                  | S9, S10, S11, S21, S22 | Diego Fontán  | Document the strategy choice at the constructor and in the README's chunking row, citing S9's measured delta and S11's corpus-dependence caveat; change the default only if a corpus-type argument makes it unambiguous | ASGF Scale A — P2: "Gap that reduces engineering maintainability or makes the system harder to extend." Both better strategies are already implemented, tested, and injectable (S22), so capability is not missing — the defect is that the default teaches the weaker arm without saying so. Kept below P1 because S11 shows the correct choice is corpus-dependent, so a blanket default swap would trade one unqualified default for another.                                                                                                                                 |
| R5  | P3       | B6            | No staleness monitoring or alerting on top of the write-time debounce hook                               | S12, S23               | Sofia Almeida | Extend `patterns/index-sync-hooks.md` with a freshness-score-and-alert pattern matching S12's narrower claim; keep it a documented pattern until a consumer needs it                                                    | ASGF Scale A — P3: "Improvement opportunity with no current reliability impact." The write-time hook already bounds staleness at ingestion; alerting adds observability over a mechanism that functions without it, and no failure is attributable to its absence.                                                                                                                                                                                                                                                                                                               |

---

## Compliance Verdict

**Conditional — P1 gaps open.**

The retrieval core stands up: hybrid BM25 + vector search fused with RRF at the paper's default
constant is at parity with the enterprise default, and it is backed by a green 61-test suite. The
two open P1s are both in the security layer of the reference pattern rather than in its ranking
quality — access control is enforced in one place where current practice puts it in two, and PII
masking is named mandatory by the module's own governing rule while shipping at zero lines of
code. The single highest-leverage fix is R1: threading a permission predicate into
`vector_store.search()` converts the pipeline from fetch-then-filter into the two-layer pattern,
and it is the finding a consumer is most likely to inherit unexamined.

### Evidence Completeness Statement

Of the seven benchmark rows, **five** carry at least one `Verified` external source (B1, B2, B3,
B4, B5); **one** (B6) rests on a `Partial` source and its claim is restated in the row to match
what the excerpt actually says rather than what was sought; **one** (B7) is
`Unassessed — no source`. Every external excerpt in the Source Register was obtained by fetching
the source page itself this session, not from a search-result snippet; every internal excerpt was
copied from a file opened this session, and the S19 negative result comes from a search actually
executed across all seven module `.py` files.

Two dimensions I considered important could not be sourced to the standard this template requires.
**Owner-level escalation for stale documents** (B7, S13) — searched, nothing quoting an escalation
path for unresponsive owners was found, so the dimension is recorded unassessed rather than
asserted. **PII masking as a mandatory rather than recommended control** (S6) — the external
source retrieved frames masking as an option to evaluate, so the mandatory framing in B3 rests on
the internal rule (S18) alone, with the external source carrying only the narrower
redact-before-embedding practice (S5). I also declined to benchmark test/CI gating discipline
because I did not seek an external standard for it.

The Reviewer named in Metadata has completed the excerpt-to-claim check (see Metadata). This
assessment is signed off and eligible for the `benchmarks/README.md` index.

---

## Sources

- **S1** — [The 2026 RAG Performance Landscape: What Every Enterprise Leader Needs to Know — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)
- **S2** — [Permission-Aware Retrieval: Why Access Control in Enterprise RAG Must Live in the Vector Layer — TianPan.co](https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control)
- **S3** — [Permission-Aware Retrieval: Why Access Control in Enterprise RAG Must Live in the Vector Layer — TianPan.co](https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control)
- **S4** — [RAG Pipeline Security Best Practices for 2026: Protecting Sensitive Data — Kiteworks](https://www.kiteworks.com/cybersecurity-risk-management/rag-pipeline-security-best-practices/)
- **S5** — [RAG Pipeline Security Best Practices for 2026: Protecting Sensitive Data — Kiteworks](https://www.kiteworks.com/cybersecurity-risk-management/rag-pipeline-security-best-practices/)
- **S6** — [RAG: How to protect sensitive and PII info with Elasticsearch & LlamaIndex — Elastic Search Labs](https://www.elastic.co/search-labs/blog/rag-security-masking-pii) — _retrieved; supports masking as an option to evaluate, not as a mandatory control; not cited as evidence_
- **S7** — [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)
- **S8** — [RAG Best Practices for Enterprise AI: Chunking, Embeddings, Reranking, Hybrid Search — StackAI](<https://www.stackai.com/insights/retrieval-augmented-generation-(rag)-best-practices-for-enterprise-ai-chunking-embeddings-reranking-and-hybrid-search-optimization>)
- **S9** — [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)
- **S10** — [The 2026 RAG Performance Landscape — Flotorch](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know)
- **S11** — [RAG Best Practices for Enterprise AI — StackAI](<https://www.stackai.com/insights/retrieval-augmented-generation-(rag)-best-practices-for-enterprise-ai-chunking-embeddings-reranking-and-hybrid-search-optimization>) — _counter-position to S10; both reported_
- **S12** — [The Knowledge Decay Problem: How to Build RAG Systems That Stay Fresh at Scale — RAG About It](https://ragaboutit.com/the-knowledge-decay-problem-how-to-build-rag-systems-that-stay-fresh-at-scale/)
- **S13** — _Searched, no supporting source found: "RAG index freshness staleness monitoring document owner escalation enterprise 2026"_
- **S14** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:103-120`
- **S15** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/retrieval.py:96,102`
- **S16** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:120-123`
- **S17** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/retrieval.py:127-153`
- **S18** — `.claude/rules/rag-engineering.md:47,50,58`
- **S19** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/*.py`, `core-component-00/framework/04-retrieval-augmented-generation/testing/*.py` (7 files, zero matches)
- **S20** — `core-component-00/framework/04-retrieval-augmented-generation/README.md:110,124`
- **S21** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/pipeline.py:50`
- **S22** — `core-component-00/framework/04-retrieval-augmented-generation/implementations/chunker.py:36,71,125`
- **S23** — `core-component-00/framework/04-retrieval-augmented-generation/CLAUDE.md` § Active Research Programme
- **S24** — `pytest retrieval-augmented-generation/testing/ -q` — 61 passed, run 2026-08-16

---

## Version History

| Version | Date       | Author        | Changes                       |
| ------- | ---------- | ------------- | ----------------------------- |
| 1.0     | 2026-08-16 | Sofia Almeida | Initial enterprise assessment |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-16
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
