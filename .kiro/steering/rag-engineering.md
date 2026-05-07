---
inclusion: fileMatch
fileMatchPattern: "**/retrieval-augmented-generation/**"
---

# Retrieval-Augmented Generation — Layer 4

**Steering File:** RAG Engineering (CC-00 Layer 4)  
**Inclusion:** Conditional — Activated when working in `retrieval-augmented-generation/`  
**Authority:** CC-00 Laboratory — Layer 4: Where to get content

---

## Module Identity

**Retrieval-Augmented Generation (RAG)** is Layer 4 of the CC-00 engineering stack — the discipline of combining LLMs with external knowledge bases.

| Field          | Detail                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------- |
| **Layer**      | 4 — Where to get content                                                                     |
| **Type**       | Production framework                                                                         |
| **Scope**      | Embedding pipelines, vector databases, reranking, chunking, evaluation, security, deployment |
| **Output**     | RAG architectures, retrieval implementations, security controls                              |
| **Has Code**   | Yes — 1 Python implementation                                                                |
| **Upstream**   | Ingests agent-generated artifacts from `harness-engineering/` (feedback loop)                |
| **Downstream** | Feeds retrieved, reranked, ACL-filtered chunks to `context-engineering/` (Retrieved slot)    |

---

## Core Concepts

### RAG Pipeline Architecture

```
Document Corpus
    ↓
Chunking Strategy
    ↓
Embedding Model
    ↓
Vector Database
    ↓
Query → Retrieval → Reranking → ACL Filtering → PII Masking
    ↓
Retrieved Slot (Context Engineering)
```

### Three RAG Layers

| Layer         | Purpose                                             | Key Patterns                          |
| ------------- | --------------------------------------------------- | ------------------------------------- |
| **Ingestion** | Chunk documents, generate embeddings, store vectors | Chunking strategies, embedding models |
| **Retrieval** | Query vector DB, retrieve candidates, rerank        | Semantic + keyword fusion, reranking  |
| **Security**  | ACL filtering, PII masking, access control          | Role-based retrieval, data masking    |

---

## Key Production Implementation

All paths relative to `core-component-00/retrieval-augmented-generation/implementations/`:

| File              | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| `rag_pipeline.py` | End-to-end RAG pipeline (ingestion → retrieval) |

---

## Key Architecture Documents

All paths relative to `core-component-00/retrieval-augmented-generation/architecture/`:

| Document             | Purpose                                                |
| -------------------- | ------------------------------------------------------ |
| `overview.md`        | RAG architecture overview and design principles        |
| `chunking.md`        | Document chunking strategies (fixed, semantic, hybrid) |
| `embedding.md`       | Embedding model selection and evaluation               |
| `vector-database.md` | Vector DB architecture and deployment patterns         |
| `reranking.md`       | Reranking strategies for improving retrieval quality   |

---

## Security Controls

All paths relative to `core-component-00/retrieval-augmented-generation/security/`:

| Control            | Purpose                                           | Document   |
| ------------------ | ------------------------------------------------- | ---------- |
| **ACL Filtering**  | Role-based access control for retrieved documents | `guide.md` |
| **PII Masking**    | Redact sensitive information before retrieval     | `guide.md` |
| **Access Logging** | Audit trail for all retrieval operations          | `guide.md` |

---

## Chunking Strategies

| Strategy       | When to Use                                         | Trade-offs                          |
| -------------- | --------------------------------------------------- | ----------------------------------- |
| **Fixed-size** | Uniform documents (e.g., logs, transcripts)         | Simple but may split semantic units |
| **Semantic**   | Narrative documents (e.g., articles, documentation) | Preserves meaning but variable size |
| **Hybrid**     | Mixed document types                                | Best quality but most complex       |

---

## Retrieval Strategies

| Strategy            | Purpose                                    |
| ------------------- | ------------------------------------------ |
| **Semantic Search** | Vector similarity search (embedding-based) |
| **Keyword Search**  | BM25 or full-text search (term-based)      |
| **Hybrid (Fusion)** | Combine semantic + keyword, rerank results |

**Recommended:** Hybrid retrieval with reranking for production systems.

---

## Agent Behavior Rules for RAG Engineering

When working with RAG:

1. **Use hybrid retrieval** — Combine semantic + keyword search, then rerank
2. **Apply security controls** — ACL filtering and PII masking are mandatory (ASE compliance)
3. **Choose appropriate chunking** — Match chunking strategy to document type
4. **Evaluate retrieval quality** — Use evaluation frameworks to measure precision/recall
5. **Feed back to RAG** — Agent-generated artifacts should be ingested back into the knowledge base
6. **Monitor retrieval freshness** — Track staleness of retrieved facts (active research programme)

---

## Integration Points

| From                   | To                                      | What Flows                                |
| ---------------------- | --------------------------------------- | ----------------------------------------- |
| `harness-engineering/` | RAG Engineering                         | Agent-generated artifacts (feedback loop) |
| RAG Engineering        | `context-engineering/` (Retrieved slot) | Retrieved, reranked, ACL-filtered chunks  |

---

## Active Research Programme

**Retrieval Freshness Guarantees** — How do we bound the staleness of retrieved facts at inference time?

See `core-component-00/README.md` § Active Research Programmes for current status.

---

## Evaluation Framework

All paths relative to `core-component-00/retrieval-augmented-generation/evaluation/`:

| Metric          | Purpose                                                 |
| --------------- | ------------------------------------------------------- |
| **Precision@K** | Fraction of top-K results that are relevant             |
| **Recall@K**    | Fraction of relevant documents in top-K results         |
| **MRR**         | Mean Reciprocal Rank (position of first relevant doc)   |
| **NDCG**        | Normalized Discounted Cumulative Gain (ranking quality) |

---

**This steering file is automatically activated when working in `retrieval-augmented-generation/` directories.**
