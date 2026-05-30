---
paths:
  - "**/retrieval-augmented-generation/**"
description: RAG Engineering (Layer 4) patterns and behavior rules
---

# Retrieval-Augmented Generation — Layer 4

**Scope:** Embedding pipelines, vector databases, reranking, chunking, evaluation, security

---

## RAG Pipeline Architecture

```
Document Corpus → Chunking → Embedding Model → Vector Database
                                                      ↓
Query → Retrieval → Reranking → ACL Filtering → PII Masking
                                                      ↓
                              Retrieved Slot (Context Engineering)
```

---

## Chunking Strategies

| Strategy       | When to Use                           | Trade-offs                          |
| -------------- | ------------------------------------- | ----------------------------------- |
| **Fixed-size** | Uniform documents (logs, transcripts) | Simple but may split semantic units |
| **Semantic**   | Narrative documents (articles, docs)  | Preserves meaning but variable size |
| **Hybrid**     | Mixed document types                  | Best quality, most complex          |

---

## Retrieval Strategies

| Strategy            | Purpose                                    |
| ------------------- | ------------------------------------------ |
| **Semantic Search** | Vector similarity search (embedding-based) |
| **Keyword Search**  | BM25 or full-text search (term-based)      |
| **Hybrid (Fusion)** | Combine semantic + keyword, rerank results |

**Recommended:** Hybrid retrieval with reranking for production systems.

---

## Security Controls (Mandatory for ASE Compliance)

- **ACL Filtering:** Role-based access control for retrieved documents
- **PII Masking:** Redact sensitive information before retrieval
- **Access Logging:** Audit trail for all retrieval operations

---

## Behavior Rules

1. Use hybrid retrieval in production
2. Apply ACL filtering and PII masking (ASE compliance requirement)
3. Choose appropriate chunking strategy for document type
4. Evaluate retrieval quality using Precision@K, Recall@K, MRR, NDCG
5. Feed agent-generated artifacts back into the knowledge base
6. Monitor retrieval freshness — track staleness of retrieved facts
