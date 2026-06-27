# RAG Evaluation Framework - Reference Table

## Complete Specification of Metrics, Tools, and Testing Patterns

This reference table provides comprehensive specifications for evaluating RAG system performance across all key dimensions.

---

## Evaluation Metrics Matrix

| #      | Metric Category     | Specific Metric            | Type             | Target Range  | Measurement Method              | Tool/Implementation      |
| ------ | ------------------- | -------------------------- | ---------------- | ------------- | ------------------------------- | ------------------------ |
| **1**  | Retrieval Quality   | Exact Match (EM)@K         | Normalized       | ≥0.70         | Gold-standard QA pairs          | Custom evaluator / RAGAS |
| **2**  | Retrieval Quality   | F1 Score@K                 | Normalized       | ≥0.65         | Partial overlap scoring         | Custom evaluator         |
| **3**  | Retrieval Quality   | NDCG@K                     | Normalized       | ≥0.60         | Position-weighted ranking       | Scikit-learn             |
| **4**  | Retrieval Quality   | MRR (Mean Reciprocal Rank) | Normalized       | ≥0.75         | First relevant hit position     | Custom evaluator         |
| **5**  | Retrieval Quality   | Recall@K                   | Normalized       | ≥0.80         | Retrieved vs total relevant     | Ground truth comparison  |
| **6**  | Retrieval Quality   | Precision@K                | Normalized       | ≥0.65         | Correct / retrieved count       | Ground truth comparison  |
| **7**  | Generation Quality  | BERTScore                  | Normalized       | ≥0.75         | Semantic similarity (BERT)      | bert-score library       |
| **8**  | Generation Quality  | ROUGE-L                    | Absolute         | 50-65         | Longest common subsequence      | rouge_score              |
| **9**  | Generation Quality  | BLEU Score                 | Absolute         | 40-55         | N-gram overlap with reference   | sacreBLEU                |
| **10** | Faithfulness        | Hallucination Rate         | Percentage       | <5%           | Claims not supported by context | Fact-checking pipeline   |
| **11** | Faithfulness        | Answer Relevance           | Normalized       | ≥0.65         | Semantic match to gold answer   | RAGAS answer_relevance   |
| **12** | Context Utilization | Token Efficiency           | % of budget      | 60-80%        | Used tokens / max budget        | Prompt logging analysis  |
| **13** | Citation Quality    | Citation Accuracy          | % correct        | ≥90%          | Citations match claims          | Manual + automated check |
| **14** | Citation Quality    | Citation Coverage          | % needed covered | ≥85%          | Ground truth spans retrieved    | Span-matching algorithm  |
| **15** | System Performance  | Query Latency (p95)        | Time             | <600ms        | End-to-end timing               | Prometheus metrics       |
| **16** | System Performance  | Cache Hit Rate             | Percentage       | ≥40%          | Cached / total queries          | Redis stats              |
| **17** | System Performance  | Throughput (qps)           | Queries/sec      | >50 sustained | Requests per second             | Load testing             |
| **18** | Cost Efficiency     | Tokens per Query           | Absolute         | <3,000        | Total input+output tokens       | Usage tracking           |
| **19** | Cost Efficiency     | Cost per Query             | USD              | <$0.10        | Provider billing / queries      | Financial tracking       |
| **20** | User Satisfaction   | Response Relevance         | 1-5 scale        | ≥4.0 avg      | Human rating task               | Survey/annotation tool   |

---

## Golden Dataset Schema

### JSONL Format Specification

| Field            | Type       | Required | Description                           | Example                                            |
| ---------------- | ---------- | -------- | ------------------------------------- | -------------------------------------------------- |
| `id`             | string     | Yes      | Unique question identifier            | `q-001`                                            |
| `query`          | string     | Yes      | User query text                       | `"What is RAG?"`                                   |
| `relevant_docs`  | list[str]  | Yes      | Document IDs that should be retrieved | `["doc_chunk_42"]`                                 |
| `relevant_spans` | list[dict] | Optional | Specific text spans within documents  | `[{"doc_id": "doc_42", "start": 100, "end": 250}]` |
| `gold_answer`    | string     | Yes      | Expected answer (ground truth)        | `"RAG combines retrieval with generation..."`      |
| `answer_type`    | enum       | Optional | Answer classification                 | `"factoid"`, `"procedure"`, `"summary"`            |
| `difficulty`     | float      | Optional | Estimated difficulty 0.0-1.0          | `0.75`                                             |
| `category`       | string     | Optional | Topic category                        | `"basics"`, `"architecture"`                       |

### Sample Golden Dataset Entry (JSONL)

```jsonl
{"id": "rag-basics-001", "query": "What is RAG?", "relevant_docs": ["architecture/overview.md:45"], "gold_answer": "RAG (Retrieval Augmented Generation) combines information retrieval with generative models by retrieving relevant context from a knowledge base and providing it as input to an LLM before generation.", "answer_type": "factoid", "difficulty": 0.65, "category": "basics"}
{"id": "architecture-001", "query": "How does the embedding service work?", "relevant_docs": ["components/reference-table.md:78"], "gold_answer": "The embedding service converts text into dense vector representations using models like all-MiniLM-L6-v2, with typical latency of ~40ms per batch on GPU.", "answer_type": "procedure", "difficulty": 0.75, "category": "architecture"}
```

---

## Evaluation Tool Comparison

| Tool              | Purpose                       | Language     | Dependencies          | Difficulty | License    | Best For                 |
| ----------------- | ----------------------------- | ------------ | --------------------- | ---------- | ---------- | ------------------------ |
| **ragas**         | Full RAG evaluation framework | Python       | `pip install ragas`   | Medium     | MIT        | Comprehensive eval suite |
| **trulens**       | LLM observability & eval      | Python       | `pip install trulens` | Medium     | Apache 2.0 | Tracing + evaluation     |
| **langsmith**     | LangChain-specific evals      | Python       | Built into LangChain  | Easy       | MIT        | LangChain users          |
| **custom**        | Custom metric calculation     | Any language | scikit-learn + numpy  | Medium     | Choose     | Specific needs           |
| **arize-phoenix** | Tracing + evaluation          | Python SDK   | Docker deployment     | Hard       | Apache 2.0 | Enterprise observability |

---

## Benchmark Results (Typical)

### Embedding Model Benchmarks

| Model                 | Size | Latency (p50) | Memory | EM@K  | Recommendation            |
| --------------------- | ---- | ------------- | ------ | ----- | ------------------------- |
| **all-MiniLM-L6-v2**  | 22M  | ~40ms         | 450MB  | ~0.70 | Default choice            |
| **bge-small-en-v1.5** | 23M  | ~45ms         | 480MB  | ~0.72 | Slightly better retrieval |
| **E5-small-v2**       | 26M  | ~50ms         | 520MB  | ~0.71 | Good for multilingual     |
| **all-MiniLM-L12-v2** | 280M | ~400ms        | 2GB    | ~0.78 | Better quality, slower    |

### Reranker Model Benchmarks

| Model                        | Size | Latency (p50) | Memory | MRR Improvement | Recommendation   |
| ---------------------------- | ---- | ------------- | ------ | --------------- | ---------------- |
| **bge-reranker-base**        | 115M | ~150ms        | 2.5GB  | +0.25           | Good balance     |
| **bge-reranker-large**       | 479M | ~300ms        | 4GB    | +0.35           | Best quality     |
| **cohere-rerank-english-v2** | N/A  | ~200ms (API)  | N/A    | +0.30           | Easy integration |

---

## Edge Case Testing Matrix

| Category                   | Test Cases                            | Expected Behavior                                    | Failure Mode                 | Mitigation                                    |
| -------------------------- | ------------------------------------- | ---------------------------------------------------- | ---------------------------- | --------------------------------------------- |
| **Out of Scope**           | Questions about topics outside domain | "I don't have information on..."                     | Hallucinates answer          | Guardrail prompts + explicit scope statements |
| **Ambiguous Query**        | Multiple possible interpretations     | Ask clarifying questions or provide multiple answers | Chooses wrong interpretation | Query rewriting + multi-path retrieval        |
| **Contradictory Sources**  | Retrieved docs disagree               | Present all views with citations                     | Picks one arbitrarily        | Weight by recency/reputation in reranking     |
| **Very Short Context**     | Single-chunk relevant info            | Respond concisely, cite the chunk                    | Truncates important info     | Use smaller chunks for specific lookup        |
| **Very Long Context**      | Multiple relevant long docs           | Summarize key points from all sources                | Token budget overflow        | Compress context + hierarchical summarization |
| **Uncertain Query Intent** | User hasn't specified exact need      | Request clarification                                | Premature response           | Detect ambiguity → clarification branch       |

---

## Evaluation Dashboard Metrics

### Key Metrics to Monitor

| Metric              | Target Value | Alert Threshold  | Grafana Panel Type | Update Frequency |
| ------------------- | ------------ | ---------------- | ------------------ | ---------------- |
| Query Latency (p50) | <300ms       | >800ms → Warn    | Time series graph  | 5s               |
| Query Latency (p95) | <600ms       | >1000ms → Page   | Time series graph  | 5s               |
| Retrieval EM@K      | ≥0.70        | <0.60 → Critical | Stat panel         | 1min             |
| Cache Hit Rate      | ≥40%         | <30% → Warn      | Gauge chart        | 10s              |
| Context Utilization | 60-80%       | >90% → Warn      | Heatmap            | 1min             |
| Hallucination Rate  | <5%          | >10% → Page      | Gauge chart        | 5min             |

---

## Best Practices Checklist

### Golden Dataset Setup

- [ ] Create initial golden dataset with 50-100 queries minimum
- [ ] Cover diverse topics and answer types (factoid, procedure, comparison)
- [ ] Include edge case queries for adversarial testing
- [ ] Document ground truth answers from authoritative sources
- [ ] Version the golden dataset with changelog

### Continuous Evaluation Cadence

| Test Type                | Frequency             | Trigger                    | Owner         |
| ------------------------ | --------------------- | -------------------------- | ------------- |
| Golden QA test suite     | Daily                 | Cron job + CI/CD           | Platform team |
| Fresh query evaluation   | Weekly                | Sample 1000 random queries | ML ops        |
| Regression testing       | On every model change | Git push trigger           | Platform team |
| User satisfaction survey | Monthly               | Random sample of users     | Product team  |
| Security audit           | Quarterly             | External + internal review | Security team |

### Alerting Rules

| Condition                                 | Severity | Action                              |
| ----------------------------------------- | -------- | ----------------------------------- |
| EM@K drops >0.1 from baseline             | Critical | Page on-call + rollback plan        |
| p95 latency >1s for 3 consecutive minutes | Warning  | Alert → investigate root cause      |
| Cache hit rate <25%                       | Info     | Log → optimize cache strategy       |
| Hallucination rate >10%                   | High     | Review prompts + increase citations |

---

## Common Evaluation Pitfalls

| Pitfall                       | Symptom                                          | Solution                                                  |
| ----------------------------- | ------------------------------------------------ | --------------------------------------------------------- |
| **Golden set bias**           | Scores artificially inflated on training data    | Use held-out test set; add adversarial examples           |
| **Metric myopia**             | Optimizing one metric hurts others               | Track full metric suite; use multi-objective optimization |
| **Ignoring latency**          | High accuracy but unusable response times        | Include latency in composite score; add SLA constraints   |
| **Static evaluation**         | Metrics don't reflect query distribution changes | Re-sample golden set quarterly; monitor query mix shifts  |
| **Hallucination blind spots** | Focusing only on factual correctness             | Add factuality metrics; include adversarial queries       |

---

## Incremental Upsert vs. Full-Rebuild Decision Framework

When a RAG pipeline processes document writes, the index update strategy must be chosen
deliberately. Updating only the modified document (incremental upsert) and rebuilding the
entire index from the corpus (full rebuild) have fundamentally different cost and correctness
profiles.

### Decision Criteria

| Criterion         | Full Rebuild                                     | Incremental Upsert                                                      |
| ----------------- | ------------------------------------------------ | ----------------------------------------------------------------------- |
| Backend support   | Any (FAISS, Qdrant, BM25)                        | Requires vector store with upsert API (Qdrant, Weaviate, pgvector)      |
| Corpus size       | Typically < 500 documents / < 10,000 chunks      | Warranted at ≥ 500 documents or ≥ 10,000 chunks                         |
| Rebuild latency   | < 10 s on available hardware (acceptable)        | —                                                                       |
| Write frequency   | Infrequent (hours between writes)                | Frequent (multiple writes per session or per day)                       |
| Index correctness | Full corpus parity guaranteed after each rebuild | Per-file consistency; orphaned points accumulate without a parity check |

### Trigger Thresholds for Adopting Incremental Upsert

Switch from full rebuild to incremental upsert when **any one** of the following conditions is met:

| Trigger                 | Condition                                                          | Rationale                                                                      |
| ----------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Practical (latency)** | Full rebuild takes > 10 s perceptibly                              | User-observable delay; staleness window grows with rebuild time                |
| **Volumetric**          | Corpus > 500 documents or > 10,000 chunks                          | FAISS re-encode of 10,000 chunks on RTX 4060 ≈ 15–30 s; scales linearly        |
| **Architectural**       | Migration to a vector store with native incremental upsert support | Adopt the capability when available; retain full rebuild for disaster recovery |
| **Strategic**           | Explicit authorisation from system owner                           | Invest in readiness before urgency forces the transition                       |

These thresholds are hardware-dependent. The volumetric threshold (10,000 chunks ≈ 15–30 s on
RTX 4060 GPU) must be re-calibrated for the target hardware profile before use in other contexts.

### Orphaned Point Detection and Remediation

Incremental upserts introduce an index correctness failure mode absent from full-rebuild
approaches: **orphaned points** — vector store entries for chunks from files that have since
been deleted or restructured. These points persist silently and degrade retrieval quality by
surfacing stale content.

| Condition                                    | Detection Method                                               | Remediation                                                                 |
| -------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `points_count > len(corpus_chunks)`          | `health_check` tool: `parity_ok: false`, `orphaned_points > 0` | Full rebuild from corpus                                                    |
| File deleted from corpus                     | Not detected automatically — orphaned points persist           | Periodic parity check (`health_check`) + full rebuild on failure            |
| Chunk boundaries changed (file restructured) | Silent MRR degradation for queries matching the changed file   | Re-index the modified file; run MRR spot check on affected query categories |

Run a `health_check` parity check after any document deletion or bulk restructuring operation,
and after any upsert volume exceeding 20 files in a single session.

### MRR Baseline Establishment (Required Before Switching Retrieval Backends)

Switching from one retrieval backend to another (e.g., FAISS → Qdrant) requires a committed
quality baseline to prevent undetected regressions.

**Protocol:**

1. Author a query set of ≥ 20 representative queries with known-relevant documents, covering
   the full range of query types the system will serve (minimum for a pre-migration quality gate;
   the full production golden dataset requires 50-100 queries per the Golden Dataset Setup
   checklist above)
2. **Commit the query set before switching backends** — authoring baseline judgments after
   observing the new backend's results risks retrofitting ground truth to match outcomes
3. Record `prior_backend_mrr_baseline` by running the query set against the current system
4. After seeding the new backend, measure `new_backend_mrr` before switching reads
5. Block the backend switch if `new_backend_mrr < 0.95 × prior_backend_mrr_baseline`

**Query set storage format** (`tests/rag_eval/mrr_query_set.json`):

```json
[
  {
    "query": "stage gate user approval",
    "relevant_doc": "company/pipeline/mobile/pipeline.md"
  },
  {
    "query": "ADR technology decision lock",
    "relevant_doc": "company/pipeline/mobile/pipeline.md"
  }
]
```

- `query`: exact string submitted to the retrieval tool
- `relevant_doc`: the `rel_path` of the single known-relevant document (relative to workspace root)
- Completeness requirement: ≥ 20 entries (minimum for a pre-migration quality gate), no duplicate `relevant_doc` values
- Authorship: system owner or designated reviewer before Phase 1 / backend-switch entry

---

## Quick Links to Documentation

- [Architecture Overview](core-component-00/retrieval-augmented-generation/architecture/overview.md) - System design patterns
- [Security Guide](core-component-00/retrieval-augmented-generation/security/guide.md) - Compliance and security controls
- [Integration Patterns](core-component-00/retrieval-augmented-generation/integrations/overview.md) - Data source connectors
- [Components Reference](core-component-00/retrieval-augmented-generation/components/reference-table.md) - Component specifications
- [Deployment Templates](core-component-00/retrieval-augmented-generation/templates/deployment-template.yaml) - Production configs
