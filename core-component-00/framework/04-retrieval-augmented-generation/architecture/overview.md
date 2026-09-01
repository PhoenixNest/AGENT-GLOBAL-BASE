# RAG System Architecture Overview

## 1. High-Level Architecture

### 1.1 Component Architecture Diagram

```mermaid
graph TB
    subgraph EnterpriseRAG["Enterprise RAG System"]
        UserQueries[User Queries]
        Orchestrator[Orchestrator]
        PromptEng[Prompt Engineering]
        EmbeddingSvc[Embedding Service]
        VectorDB[(Vector Database)]
        Reranker[Reranking Service]
        LLMEngine[LLM Inference Engine]
        EvalFramework[Evaluation Framework]
    end

    UserQueries --> Orchestrator
    Orchestrator <--> PromptEng
    Orchestrator --> EmbeddingSvc
    EmbeddingSvc --> VectorDB
    VectorDB --> Reranker
    Reranker --> Orchestrator
    Orchestrator --> LLMEngine
    LLMEngine <--> EvalFramework
```

### 1.2 Data Flow Architecture

```mermaid
flowchart TD
    UserQuery([User Query]) --> CacheCheck{Query Cache Check}
    CacheCheck -->|Cache Hit| Return([Return Cached Response])
    CacheCheck -->|No| EmbedModel[Embedding Model]
    EmbedModel --> VectorDB[(Vector Database)]
    VectorDB -->|Top-K Results| Reranker[Reranking Service]
    Reranker --> ContextAssembly[Context Assembly]
    ContextAssembly --> PromptEng[Prompt Engineering Layer]
    PromptEng --> LLMEngine[LLM Generation Engine]
    LLMEngine --> Response[Response + Citations]
    Response --> EvalMetrics[Evaluation Metrics]
```

## 2. Architecture Layers

### 2.1 Presentation Layer

| Component  | Responsibility                                    | Technologies          |
| ---------- | ------------------------------------------------- | --------------------- |
| Web UI     | Interactive chat interface with document explorer | React, Tailwind CSS   |
| REST API   | HTTP/JSON endpoints for programmatic access       | FastAPI, OpenAPI spec |
| CLI Client | Command-line tool for batch operations            | Python click/typer    |

### 2.2 Orchestration Layer

| Component        | Responsibility                 | Technologies          |
| ---------------- | ------------------------------ | --------------------- |
| RAG Orchestrator | Main workflow coordination     | LangChain/LlamaIndex  |
| Query Cache      | LRU cache for frequent queries | Redis/Memcached       |
| Session Manager  | Maintains conversation context | Redis + timestamp TTL |

### 2.3 Retrieval Layer

| Component            | Responsibility               | Technologies               |
| -------------------- | ---------------------------- | -------------------------- |
| Embedding Service    | Text → vector transformation | sentence-transformers      |
| Vector Database      | Persistent vector storage    | Qdrant/Weaviate/pgvector   |
| Reranking Service    | Cross-encoder refinement     | bge-reranker/cross-encoder |
| Hybrid Search Engine | BM25 + vector fusion         | Elasticsearch/Whoosh       |

### 2.4 Generation Layer

| Component              | Responsibility              | Technologies         |
| ---------------------- | --------------------------- | -------------------- |
| LLM Inference          | Text generation API         | vLLM/TGI/Ollama      |
| Prompt Template Engine | Dynamic prompt construction | Jinja2/Mustache      |
| Context Window Manager | Token budget allocation     | Custom token counter |

### 2.5 Evaluation Layer

| Component           | Responsibility                 | Technologies             |
| ------------------- | ------------------------------ | ------------------------ |
| Test Suite          | Automated evaluation framework | pytest + LLM graders     |
| Metrics Collector   | Aggregates and reports metrics | Prometheus/InfluxDB      |
| Human Eval Platform | Interface for human judgment   | React + annotation tools |

### 2.6 Security Layer

| Component      | Responsibility             | Technologies            |
| -------------- | -------------------------- | ----------------------- |
| Access Control | Per-document permissions   | OAuth2 + JWT + ACL      |
| PII Handler    | Sensitive data masking     | spaCy + regex patterns  |
| Audit Logger   | Immutable operation logs   | PostgreSQL + encryption |
| DLP Rules      | Content filtering policies | Custom rules engine     |

## 3. Deployment Topologies

### 3.1 Single-Node (Development)

```mermaid
graph TB
    subgraph SingleNode["Single Node — Development"]
        WebUI[Web UI]
        VectorDB["Vector DB (Qdrant)"]
        LLM["LLM (Ollama)"]
        EmbeddingSvc[Embedding Service]
        Redis["Redis (Cache)"]
        Logger["Logger / PostgreSQL"]
    end
```

> **Use Case:** Development, prototyping, testing
> **Latency:** ~800–1500ms end-to-end
> **Capacity:** ~10–50 concurrent users

### 3.2 Multi-Node (Production)

```mermaid
graph LR
    LB[Load Balancer] --> Worker1[Worker Node 1]
    LB --> Worker2[Worker Node 2]
    LB --> WorkerN[Worker Node N]
    Worker1 --> VectorDB[(Vector Database)]
    Worker2 --> CacheCluster[(Cache Cluster)]
    WorkerN --> CacheCluster
    WorkerN --> LLMCluster[LLM Service Cluster]
```

> **Use Case:** Production enterprise deployment
> **Latency:** ~300–600ms end-to-end
> **Capacity:** ~500–2000 concurrent users (scaling)

### 3.3 Hybrid Cloud-Edge

```mermaid
graph LR
    subgraph EdgeNodes["Edge Nodes (Local Vector DB)"]
        LocalVDB[(Local Vector DB)]
    end

    subgraph CentralCloud["Central Cloud (Training/Indexing)"]
        Indexing[Training and Indexing]
    end

    LocalVDB <--> Indexing
```

> **Use Case:** Multi-region deployment, data residency requirements
> **Latency:** ~100–300ms local, ~50–200ms cloud
> **Capacity:** Scales with edge node count

## 4. Technology Stack Reference

| Layer         | Component       | Recommended Options                    | Alternatives                    |
| ------------- | --------------- | -------------------------------------- | ------------------------------- |
| **Vector DB** | Primary storage | Qdrant (preferred), Weaviate, Pinecone | Milvus, Chroma, pgvector        |
| **Embedding** | Model           | bge-small-en-v1.5, all-MiniLM-L6-v2    | E5-small, sentence-transformers |
| **Reranker**  | Cross-encoder   | bge-reranker-large, Cohere Rerank      | UCSD/reranker-large             |
| **LLM**       | Inference       | vLLM (preferred), TGI, Ollama          | TextGenWebUI, llama-cpp-python  |
| **Cache**     | Query/results   | Redis (preferred), Memcached           | Cassandra, ScyllaDB             |
| **Logging**   | Metrics/audit   | PostgreSQL, ClickHouse                 | TimescaleDB, InfluxDB           |

## 5. Performance Targets

| Metric                      | Development | Production Goal | SLA Target |
| --------------------------- | ----------- | --------------- | ---------- |
| Query latency (p50)         | 300ms       | 250ms           | <400ms     |
| Query latency (p95)         | 800ms       | 600ms           | <1000ms    |
| Retrieval accuracy (EM)     | 0.65        | 0.75            | ≥0.70      |
| Reranking improvement (MRR) | +0.30       | +0.35           | ≥+0.30     |
| Cache hit rate              | 20%         | 50%             | ≥40%       |
| Context utilization         | 60-80%      | 70-85%          | 60-90%     |

## 6. Scalability Guidelines

### Horizontal Scaling Patterns

| Component         | Scale Factor             | Bottleneck Mitigation                    |
| ----------------- | ------------------------ | ---------------------------------------- |
| Embedding Service | ×N (load balanced)       | Batch processing, async queues           |
| Vector DB         | Sharding by collection   | Consistent hashing, range queries        |
| Reranking         | ×N (parallel candidates) | Two-stage filtering (coarse→fine)        |
| LLM Inference     | Multi-GPU batching       | vLLM PagedAttention, continuous batching |

### Data Volume Guidelines

| Document Count | Vector DB Choice  | Index Strategy       | Expected Latency |
| -------------- | ----------------- | -------------------- | ---------------- |
| <100K          | Any (Chroma)      | Full index           | ~100ms           |
| 100K-1M        | Qdrant/Weaviate   | HNSW index           | ~200-300ms       |
| 1M-10M         | Weaviate/Pinecone | IVF_PQ + HNSW        | ~300-500ms       |
| >10M           | Pinecone/Weaviate | Multi-stage indexing | ~500-800ms       |

## 10. Corpus-as-Source-of-Truth Principle

Every search index — whether FAISS, Qdrant, BM25, or keyword — is a **derived artifact**. The
document corpus is the single, authoritative source of truth for a RAG system. This principle
has three concrete architectural implications:

| Implication                                         | Consequence                                                                               |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Indexes are always rebuildable from source          | Migration risk is bounded by re-indexing cost, not by data-loss risk                      |
| There is no "index migration" in the database sense | Moving between vector stores is a re-seeding operation, not a data transfer requiring ETL |
| Rollback is always available at any migration phase | Any retrieval backend can be abandoned and the previous one rebuilt from source documents |

This principle structurally lowers the risk of retrieval backend migrations compared to classical
database migrations: there is no data to "move," only index representations to rebuild and
validate against the corpus.

**Design rule:** Never store information in a retrieval index that is not derivable from the
document corpus. Information that exists only in the index will be silently lost if the index
is rebuilt.

---

## 11. Graceful Degradation Stack Architecture

Production RAG systems must define an **explicit degradation stack** — an ordered sequence of
fallback retrieval tiers, each less capable but more available than the previous. Without a
defined degradation stack, any component failure produces undefined recovery behaviour.

### Reference Stack (workspace-knowledge MCP server)

```
Tier 1 (HYBRID_QDRANT)  — Qdrant semantic search + BM25 keyword fusion        [primary]
Tier 2 (HYBRID)         — FAISS semantic search + BM25 keyword fusion          [hot standby]
Tier 3 (BM25)           — BM25 keyword-only search                             [warm standby]
Tier 4 (Raw Corpus Scan) — Full corpus scan, no index required                 [cold fallback]
```

### Tier Activation Conditions

| Tier            | Activates When                                                                         |
| --------------- | -------------------------------------------------------------------------------------- |
| HYBRID_QDRANT   | External vector store client available and collection health confirmed                 |
| HYBRID          | External vector store unavailable; in-process index on disk and embedding model loaded |
| BM25            | Embedding model not yet loaded (initialisation window) or in-process index missing     |
| Raw Corpus Scan | All index-based tiers unavailable                                                      |

### Permanent Retention Rule

In local deployments where external services (Docker, managed cloud) cannot be guaranteed
available (developer workstations, CI environments, air-gapped machines), in-process retrieval
tiers **must be permanently retained** — not removed after migrating to an external vector store.
This ensures the system degrades gracefully rather than failing completely when external
dependencies are unavailable.

**Constraint (local and offline deployments):** In-process search code paths, embedding model
dependencies, and local index files must remain in the codebase after migrating to an external
vector store. Removing them to reduce code complexity is an availability regression. This
constraint does not apply to deployments with guaranteed external service availability (e.g.,
fully managed cloud environments backed by an uptime SLA).

### Rollback Procedure (External Vector Store → In-Process Tier)

```
1. Set SEARCH_BACKEND=faiss in the MCP server configuration
2. Restart the MCP server process
3a. If the in-process index file is on disk: available immediately (< 60 s)
3b. If the in-process index file is missing: call rebuild_index from corpus (2–5 min)
```

This procedure is always available because: (a) the corpus is the source of truth (§10) and
the index can always be rebuilt, and (b) the in-process tier is permanently retained (Permanent
Retention Rule above).

**Cross-reference:** `patterns/index-sync-hooks.md` — Phase-Adaptive Index Sync Hook pattern
for maintaining index freshness across all degradation tiers.

## 7. Cost Optimization Strategies

| Strategy               | Implementation                  | Expected Savings                     |
| ---------------------- | ------------------------------- | ------------------------------------ |
| Query caching          | Redis with TTL-based eviction   | 40-60% LLM calls reduced             |
| Model quantization     | INT4/INT8 weights via vLLM      | 50-75% inference cost reduction      |
| Batch embedding        | Async processing pipeline       | 60-80% embedding cost reduction      |
| Hybrid search fallback | BM25 for quick retrieval        | Reduces expensive reranking calls    |
| Tiered vector DB       | Hot/warm/cold data partitioning | Low-cost storage for historical data |

## 8. Monitoring Dashboards

### Key Dashboard Metrics

| Metric Category | Specific Metrics                  | Alerts                    |
| --------------- | --------------------------------- | ------------------------- |
| **Latency**     | Query latency (p50, p95, p99)     | >1s → Page, >500ms → Warn |
| **Accuracy**    | Retrieval EM@K, Rerank MRR        | Drop >0.05 → Page         |
| **Throughput**  | Queries/second, requests/GPU-hour | <50% capacity utilization |
| **Quality**     | Context utilization rate          | <50% or >90% → Review     |
| **Cost**        | Tokens per query, embedding calls | >$100/hour → Optimize     |

## 9. Failure Mode Analysis

| Failure Scenario          | Mitigation Strategy                      | Recovery Time                  |
| ------------------------- | ---------------------------------------- | ------------------------------ |
| Embedding service down    | Failover to backup instance              | 5-10 min (cold start: 2-3 min) |
| Vector DB connection loss | Circuit breaker + retry                  | 1-2 min reconnection           |
| LLM quota exhausted       | Graceful degradation to cached responses | N/A (preventive limits)        |
| Cache memory pressure     | LRU eviction policy                      | Auto-handled (<100ms)          |
| Context window overflow   | Truncate least-relevant chunks first     | <50ms                          |
