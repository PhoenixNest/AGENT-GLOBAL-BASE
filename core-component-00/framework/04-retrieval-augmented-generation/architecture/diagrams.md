# RAG System Architecture Diagrams

## Complete Visual Reference for Enterprise RAG Implementation

This document provides comprehensive architectural diagrams for designing and implementing an enterprise-level RAG system.

---

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        WebUI[Web UI Chat]
        RESTAPI[REST API Endpoint]
        CLI[CLI Client]
    end

    subgraph "Orchestration Layer"
        Orchestrator[RAG Orchestrator Service]
        QueryCache[(Query Cache)]
    end

    subgraph "Retrieval Layer"
        Embedding[Embedding Model]
        VectorDB[(Vector Database)]
        Reranker[Reranking Service]
        HybridSearch[Hybrid Search Engine]
    end

    subgraph "Generation Layer"
        LLM[LLM Inference Engine]
        PromptEngine[Prompt Template Engine]
        ContextWindow[Context Window Manager]
    end

    subgraph "Evaluation Layer"
        EvalPipeline[Evaluation Pipeline]
        MetricsStore[(Metrics Store)]
    end

    subgraph "Security Layer"
        ACL[Access Control Service]
        PIIHandler[PII Masking Service]
        AuditLogger[Audit Logger]
    end

    WebUI --> Orchestrator
    RESTAPI --> Orchestrator
    CLI --> Orchestrator

    Orchestrator --> QueryCache
    QueryCache --> Orchestrator

    Orchestrator --> Embedding
    Embedding --> VectorDB
    VectorDB --> Reranker
    Reranker --> Orchestrator

    Orchestrator --> HybridSearch
    HybridSearch --> VectorDB

    Orchestrator --> LLM
    Orchestrator --> PromptEngine
    LLM --> ContextWindow

    Orchestrator -.-> EvalPipeline
    EvalPipeline -.-> MetricsStore

    Orchestrator -.-> ACL
    Orchestrator -.-> PIIHandler
    PIIHandler -.-> VectorDB
    AuditLogger -.-> Orchestrator
```

---

## 2. Data Flow Diagram - End-to-End Query Processing

```mermaid
sequenceDiagram
    participant User as User/Client
    participant API as REST API
    participant Cache as Query Cache (Redis)
    participant ACL as Access Control
    participant Embed as Embedding Service
    participant VectorDB as Vector Database (Qdrant)
    participant Rerank as Reranking Service
    participant PII as PII Handler
    participant Context as Context Compressor
    participant Prompt as Prompt Engine
    participant LLM as LLM Inference
    participant Output as Response Formatter

    User->>API: Submit Query + User Credentials
    API->>Cache: Check Query Cache (TTL=10min)

    alt Cache Hit
        Cache-->>API: Return Cached Response
        API-->>User: Response (200 OK)
    else Cache Miss
        Cache-->>API: No Entry

        ACL->>VectorDB: Pre-filter by Permission
        ACL->>Embed: Pass User Context

        Embed->>Embed: Create Query Embedding
        Embed-->>VectorDB: Query Vector + Metadata Filters

        VectorDB-->>Rerank: Top-20 Candidate Chunks
        Rerank->>Rerank: Score Candidates (Cross-Encoder)
        Rerank-->>Context: Top-5 Ranked Chunks

        PII->>PII: Detect and Mask Sensitive Data
        PII-->>Context: Sanitized Context

        Context->>Context: Compress/Summarize Context
        Context-->>Prompt: Optimized Context (under 4096 tokens)

        Prompt->>Prompt: Construct Generation Prompt
        Prompt-->>LLM: Final Prompt with System Instructions

        LLM->>LLM: Generate Response
        LLM-->>Output: Raw Text + Metadata

        Output->>Output: Add Citations + Format
        Output-->>API: Formatted Response

        API-->>Cache: Store for Future Queries

    end

    alt Response Contains PII
        PII->>Output: Mask Additional Sensitive Data
    end

    API-->>User: Final Response (JSON)
```

---

## 3. Vector Database Schema Design

```mermaid
erDiagram
    RAG_DOC ||--o{ CHUNK : "contains"
    DOC_COLLECTION ||--|| RAG_DOC : "owns"
    CHUNK ||--|| CHUNK_METADATA : "described by"

    RAG_DOC {
        string id "unique vector ID"
        string embedding "384-dim vector"
        text text "chunk content"
        timestamp created_at "ingestion timestamp"
        timestamp updated_at "last update"
        int relevance_score "for reranking"
    }

    DOC_COLLECTION {
        string collection_name "e.g., docs-v1"
        jsonb metadata_schema "expected fields"
    }

    CHUNK {
        string chunk_id "unique chunk identifier"
        string doc_id "reference to RAG_DOC.id"
    }

    CHUNK_METADATA {
        string chunk_id "reference to CHUNK.chunk_id"
        string source_path "original file path"
        int chunk_index "position in document"
        text chunk_title "heading/title of chunk"
        boolean has_code "contains code blocks"
        boolean contains_diagram "has images/diagrams"
    }
```

---

## 4. Component Deployment Architecture (Kubernetes)

```mermaid
graph TB
    subgraph "Ingress Layer"
        LB[Load Balancer]
        Nginx[Nginx Ingress Controller]
    end

    subgraph "Application Layer"
        RAGAPI["RAG API Service\n2 replicas\nCPU: 4C/8GiB\nGPU: 1xT4"]

        Frontend["React Web UI\n1 replica\nCPU: 1C/2GiB"]
    end

    subgraph "Microservices Layer"
        EmbeddingSvc["Embedding Service\n2 replicas\nCPU: 2C/4GiB"]

        RerankSvc["Reranking Service\n2 replicas\nCPU: 1C/4GiB\nGPU: True"]

        QuerySvc["Query Expander Service\n1 replica\nCPU: 1C/2GiB"]
    end

    subgraph "Data Layer"
        VectorDB[("Qdrant Vector DB\n50GB storage")]

        Redis[("Redis Cache\nMemory: 8GiB")]

        PostgreSQL[("PostgreSQL\nAudit logs + ACL")]
    end

    subgraph "Observability Stack"
        Prometheus[("Prometheus\nMetrics collection")]

        Grafana["Grafana Dashboard\nVisualization"]

        Loki["Loki\nLog aggregation"]
        Jaeger["Jaeger\nTracing"]
    end

    subgraph "Security Layer"
        OAuth[OAuth2/OIDC Auth]
        WAF[Web Application Firewall]
    end

    LB --> Nginx
    Nginx --> RAGAPI
    Nginx --> Frontend

    RAGAPI --> EmbeddingSvc
    RAGAPI --> QuerySvc
    EmbeddingSvc --> VectorDB
    EmbeddingSvc --> Redis
    RerankSvc --> VectorDB
    RerankSvc --> Redis
    QuerySvc --> Redis

    VectorDB --> PostgreSQL
    Redis --> PostgreSQL

    Prometheus --> RAGAPI
    Prometheus --> EmbeddingSvc
    Prometheus --> RerankSvc
    Prometheus --> VectorDB

    Grafana --> Prometheus
    Loki --> Grafana
    Jaeger --> Grafana

    WAF --> LB
    OAuth --> RAGAPI
```

---

## 5. Retrieval Pipeline with Multiple Strategies

```mermaid
graph TD
    Start([User Query]) --> QueryRewrite{Query Rewriting?}

    QueryRewrite -->|Yes| Rewrite[Generate Variations]
    Rewrite --> Embed1[Embed Original + Rewrites]
    QueryRewrite -->|No| Embed1

    Embed1 --> VectorDB[(Vector Search)]
    VectorDB --> BM25[BM25 Keyword Search]

    BM25 --> Fuse{Hybrid Fusion}
    VectorDB --> Fuse

    Fuse --> Rank1[Pre-filter: Top 50]
    Rank1 --> Reranker[Reranking Model]

    Reranker --> Rank2[Post-filter: Top K=5]
    Rank2 --> PermissionCheck{Permission Check?}

    PermissionCheck -->|Yes| PII[PII Masking]
    PermissionCheck -->|No| SkipPermissions[Skip PII Mask]

    PII --> Compress[Context Compression]
    SkipPermissions --> Compress

    Compress --> PromptEngine[Prompt Construction]

    PromptEngine --> LLMSep([LLM Generation])

    LLMSep --> ResponseFormatter[Response with Citations]
    ResponseFormatter --> Evaluate[Evaluate Quality]
    Evaluate --> Response[(Final Response)]
```

---

## 6. Caching Layer Architecture

```mermaid
graph LR
    Query([Incoming Query])

    subgraph "Query Cache (Redis)"
        Q1[Query A Hash] --> Result1[Result Object]
        Q2[Query B Hash] --> Result2[Result Object]
        Q3[Query C Hash] --> Result3[Result Object]

        Meta[Metadata: user_id, source_hash, ttl]
    end

    subgraph "Result Cache (Redis)"
        R1[Response A]
        R2[Response B]
        R3[Response C]

        Frag[Fragmented by Component]
    end

    subgraph "Circuit Breakers"
        CB1[E5 Failure Threshold]
        CB2[R30 Recovery Timeout]
    end

    Query --> Q1
    Result1 -.-> R1
    Result2 -.-> R2
    Result3 -.-> R3

    Q1 -.-> Meta
    Q2 -.-> Meta
    Q3 -.-> Meta

    R1 -.-> Frag
    R2 -.-> Frag
    R3 -.-> Frag

    R1 --CB1--> CB1
    R2 --CB1--> CB1
    R3 --CB1--> CB1
    CB1 -.-> CB2
```

---

## 7. Security Architecture Overview

```mermaid
graph TB
    subgraph "External Access"
        Internet[Internet] --> WAF[Web Application Firewall]
        WAF --> LB[Load Balancer with SSL Termination]
    end

    subgraph "Authentication Layer"
        LB --> Auth[OIDC/OAuth2 Authentication]
        Auth -->|JWT Token| RAGAPI[RAG API Gateway]
    end

    subgraph "Authorization Layer (Per-Request)"
        RAGAPI --> ACLService[ACL Service Check]
        ACLService -->|Deny| Reject[Return 403 Forbidden]
        ACLService -->|Allow| EmbeddingSvc[Embedding Service]
    end

    subgraph "Data Protection Layer"
        EmbeddingSvc --> PIIHandler[PII Detection & Masking]
        PIIHandler --> VectorDB[(Vector Database)]

        VectorDB -.-> Audit["Audit Log (Immutable)"]
    end

    subgraph "Observability with Security"
        RAGAPI --> Sentinel[Sentry Error Tracking]
        Audit --> WORMStore[Write-Once Storage]
    end
```

---

## 8. Evaluation Pipeline Architecture

```mermaid
graph TB
    GoldQA[(Golden QA Dataset)] --> Evaluate[Evaluation Orchestrator]

    subgraph "Retrieval Metrics"
        EMCalculator["EM@K Calculator"]
        F1Calculator[F1 Score Calculator]
        NDCGCalculator["NDCG@K Calculator"]
        MRRCalculator[MRR Calculator]
    end

    subgraph "Generation Metrics"
        BLEUCalculator[BLEU Scorer]
        ROUGEScorer[ROUGE-L Scorer]
        BERTScorer[BERTScore Calculator]
        PerplexityCal[Perplexity Calculator]
    end

    subgraph "Quality Metrics"
        HallucinationChecker[Hallucination Detector]
        CitationValidator[Citation Accuracy Checker]
        FaithfulnessChecker[Faithfulness Scorer]
    end

    subgraph "System Metrics"
        LatencyAnalyzer[Latency Analyzer]
        CacheAnalyzer[Cache Hit Rate Calculator]
        TokenAnalyzer[Token Usage Analyzer]
    end

    Evaluate --> EMCalculator
    Evaluate --> F1Calculator
    Evaluate --> NDCGCalculator
    Evaluate --> MRRCalculator

    Evaluate --> BLEUCalculator
    Evaluate --> ROUGEScorer
    Evaluate --> BERTScorer
    Evaluate --> PerplexityCal

    Evaluate --> HallucinationChecker
    Evaluate --> CitationValidator
    Evaluate --> FaithfulnessChecker

    Evaluate --> LatencyAnalyzer
    Evaluate --> CacheAnalyzer
    Evaluate --> TokenAnalyzer

    EMCalculator --> Dashboard[Grafana Dashboard]
    F1Calculator --> Dashboard
    BLEUCalculator --> Dashboard
    LatencyAnalyzer --> Dashboard

    HallucinationChecker --> Alert["Alert if >5%"]
    LatencyAnalyzer -->|p95 > 800ms| Alert
```

---

## 9. Ingestion Pipeline Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        Markdown[Markdown Files]
        PDF[PDF Documents]
        GitRepo[Git Repositories]
        Confluence[Confluence API]
        Database[(SQL Database)]
        RESTAPI[REST API Endpoint]
    end

    subgraph "Processing Layer"
        Parser[Document Parser Service]
        Chunker[Chunking Engine]
        MetaExtractor[META Data Extractor]
    end

    subgraph "Quality Control"
        Validator[Content Validator]
        Deduplicator[Duplicate Detector]
        PIIScanner[PII Scanner]
    end

    subgraph "Storage Layer"
        IndexBuilder[Index Builder Service]
        VectorStore[(Vector Database)]
        ACLStore[(ACL Metadata Store)]
    end

    Markdown --> Parser
    PDF --> Parser
    GitRepo --> Parser
    Confluence --> Parser
    Database --> Parser
    RESTAPI --> Parser

    Parser --> Chunker
    Chunker --> MetaExtractor
    MetaExtractor --> Validator
    MetaExtractor --> PIIScanner
    MetaExtractor --> Deduplicator

    Validator --> IndexBuilder
    PIIScanner --> IndexBuilder
    Deduplicator --> IndexBuilder

    IndexBuilder --> VectorStore
    IndexBuilder --> ACLStore
```

---

## 10. Monitoring Dashboard Layout

```mermaid
graph TB
    subgraph "Dashboard Top Row"
        Health[Health Status Widget]
        OverallLatency["Overall Latency (p50/p95/p99)"]
        QPS[Gauge: Queries Per Second]
        CacheHit["Cache Hit Rate %"]
    end

    subgraph "Dashboard Middle Section"
        LeftColumn[Left Column]
        RetrievalGraph["Retrieval EM@K Trend"]
        LatencyTrend[Latency Over Time Graph]
        RightColumn[Right Column]
        ErrorRate[Error Rate Gauge]
        TokenBudget[Token Budget Utilization]
    end

    subgraph "Dashboard Bottom Row"
        SlowQueries[Top 10 Slowest Queries Table]
        ComponentHealth[Component Health Grid]
        RecentErrors[Recent Errors Feed]
    end

    LeftColumn --> RetrievalGraph
    LeftColumn --> LatencyTrend
    RightColumn --> ErrorRate
    RightColumn --> TokenBudget

    Health --> OverallLatency
    Health --> QPS
    Health --> CacheHit
```

---

## Diagram Usage Guide

| Use Case                        | Recommended Diagram        | Location in Docs |
| ------------------------------- | -------------------------- | ---------------- |
| System overview to stakeholders | #1 High-Level Architecture | This document    |
| Debugging query failures        | #2 Data Flow Sequence      | This document    |
| Database optimization           | #3 Vector Schema           | This document    |
| Infrastructure planning         | #4 Kubernetes Deployment   | This document    |
| Retrieval strategy tuning       | #5 Multi-Strategy Pipeline | This document    |
| Caching performance analysis    | #6 Caching Layer           | This document    |
| Security audit documentation    | #7 Security Architecture   | This document    |
| ML evaluation setup             | #8 Evaluation Pipeline     | This document    |
| Data ingestion planning         | #9 Ingestion Pipeline      | This document    |
| Dashboard creation              | #10 Monitoring Layout      | This document    |
