# Workflow Diagrams — Persistent Agent Memory System

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** `../research-report.md`
> **Audience:** Visual reference for the CEO and implementing engineers — read after
> `06-self-review-and-evaluation.md`, or first if a visual overview is wanted before the prose.
> **Last Updated:** 2026-07-10
> **Convention:** Follows the Mermaid diagram style established in
> `retrieval-augmented-generation/architecture/diagrams.md` — no new diagramming convention
> introduced.

---

## 1. End-to-End Memory Workflow (Overview)

```mermaid
graph TB
    subgraph "Agent Turn"
        AgentAction[Agent generates a decision, fact, correction, or media caption]
        WorkingMem[WorkingMemory — in-process, cleared every turn]
    end

    subgraph "Write Path"
        MemStoreCall["MemoryStore API call\n(record_event / store / register)"]
        SacredCheck{Sacred?\ndecision or commitment}
        JSONLAppend[("Append to type.jsonl\n(source of truth)")]
        Embed[Embed content\nall-MiniLM-L6-v2]
        QdrantUpsert[("Qdrant upsert\nmemory_episodic / memory_semantic / memory_procedural")]
    end

    subgraph "Maintenance Job (scheduled, sleep-consolidation cadence)"
        DecayRecompute["Recompute decay_weight\n(Ebbinghaus-style exponential)"]
        ConsolidationCheck{"cumulative importance x\naccess_count >= threshold?"}
        Consolidate["Summarize episodic cluster\n-> new memory_semantic record\n(consolidated_from provenance)"]
        ContradictionCheck{"New semantic fact\ncontradicts existing?"}
        Invalidate["Mark superseded record\nstatus = archived\n(never deleted)"]
        StatusTransition["active -> dormant -> archived\n(decay-weight thresholds)"]
        ManualGC{{"Hard delete\n(operator-confirmed only,\nnever automatic)"}}
    end

    subgraph "Retrieval Path"
        Query[Agent needs memory]
        RecencyFilter["Recency-filtered\n(session_id + created_at)"]
        SemanticSearch["Semantic similarity\n(Qdrant + BM25 fusion)"]
        SacredMerge["Sacred records always included\n(bypasses decay-driven status filter)"]
        Return[Return to context window]
    end

    AgentAction --> MemStoreCall
    WorkingMem -.never persisted.-> MemStoreCall
    MemStoreCall --> SacredCheck
    SacredCheck -->|yes: decay_weight pinned at 1.0| JSONLAppend
    SacredCheck -->|no| JSONLAppend
    JSONLAppend --> Embed
    Embed --> QdrantUpsert

    QdrantUpsert -.periodic scan.-> DecayRecompute
    DecayRecompute --> ConsolidationCheck
    ConsolidationCheck -->|yes| Consolidate
    Consolidate --> JSONLAppend
    ConsolidationCheck -->|no| StatusTransition
    DecayRecompute --> ContradictionCheck
    ContradictionCheck -->|UPDATE| Invalidate
    ContradictionCheck -->|ADD / NOOP| StatusTransition
    Invalidate --> StatusTransition
    StatusTransition --> ManualGC

    Query --> RecencyFilter
    Query --> SemanticSearch
    RecencyFilter --> SacredMerge
    SemanticSearch --> SacredMerge
    QdrantUpsert -.-> RecencyFilter
    QdrantUpsert -.-> SemanticSearch
    SacredMerge --> Return
```

---

## 2. Write Path Detail (Sequence)

```mermaid
sequenceDiagram
    participant Agent as Agent (in-turn)
    participant MS as MemoryStore API
    participant Log as type.jsonl (source of truth)
    participant Embedder as all-MiniLM-L6-v2
    participant Qdrant as Qdrant collection

    Agent->>MS: record_event() / store() / register()
    MS->>MS: Is this a decision or commitment? (sacred check)
    alt Sacred
        MS->>MS: importance = 1.0, decay_weight pinned = 1.0
    else Ordinary
        MS->>MS: importance assigned at write time (0.0-1.0)
    end
    MS->>Log: Append record (durable, human-readable)
    Log-->>MS: Ack
    MS->>Embedder: Embed content field
    Embedder-->>MS: Vector (384-dim)
    MS->>Qdrant: Upsert point (vector + payload)
    Qdrant-->>MS: Ack (<100ms p95 target)
    MS-->>Agent: Write complete — no staleness window\n(unlike document RAG, write path is the index-update path)
```

---

## 3. Maintenance Job Detail (Decay, Consolidation, Forgetting)

```mermaid
graph TD
    Trigger([Scheduled trigger\n~once per real-world day]) --> ScanEpisodic[Scan memory_episodic per session]
    Trigger --> ScanSemantic[Scan memory_semantic]

    ScanEpisodic --> ImportanceSum{"Sum(importance x access_count)\n>= 150?"}
    ImportanceSum -->|yes| LLMSummarize["LLM summarization call\n(ContextCompressor)"]
    LLMSummarize --> NewSemantic["Write new memory_semantic record\nconsolidated_from = [episodic IDs]"]
    ImportanceSum -->|no| DecayStep

    NewSemantic --> ContradictionJudge{"LLM-judged:\nADD / UPDATE / DELETE / NOOP\nvs existing similar facts"}
    ContradictionJudge -->|UPDATE| InvalidateOld["Superseded record:\nstatus = archived\n(t_invalid set, never deleted)"]
    ContradictionJudge -->|ADD or NOOP| DecayStep

    ScanSemantic --> DecayStep[Recompute decay_weight\nimportance x e^-Δt/strength]
    InvalidateOld --> DecayStep

    DecayStep --> DormantCheck{decay_weight < 0.5?}
    DormantCheck -->|yes| MarkDormant[status = dormant\nexcluded from default retrieval]
    DormantCheck -->|no| StayActive[status stays active]

    MarkDormant --> ArchiveCheck{"decay_weight < 0.15 AND\nno access for 30+ days?"}
    ArchiveCheck -->|yes| MarkArchived[status = archived\nexcluded from all retrieval tiers]
    ArchiveCheck -->|no| StayDormant[remains dormant, recoverable]

    MarkArchived --> GCGate{{"Hard delete from JSONL?\nOPERATOR CONFIRMATION REQUIRED\n— never automatic"}}
    GCGate -->|confirmed| Purge[Physically removed]
    GCGate -->|not confirmed| Retained[Retained indefinitely\nin archived state]

    SacredNote["sacred = true records\nskip this entire flow\n(pinned active, decay_weight = 1.0)"]
```

---

## Diagram Usage Guide

| Use Case                                                        | Recommended Diagram       |
| --------------------------------------------------------------- | ------------------------- |
| Presenting the system to the CEO / non-implementing stakeholder | #1 End-to-End Overview    |
| Implementing the `MemoryStore` write-through integration        | #2 Write Path Detail      |
| Implementing the scheduled maintenance/decay job                | #3 Maintenance Job Detail |

These diagrams are a visual complement to the prose specification — they do not introduce any
mechanism not already documented in `01-technical-options.md`, `02-deployment-guidelines.md`, and
`03-forgetting-strategy.md`. Where a diagram and the prose ever appear to disagree after a future
edit, the prose documents remain authoritative, consistent with this workspace's general
precedence rule that visual/summary artifacts may lag their canonical source
(`CLAUDE.md` §5, Document precedence when sources conflict).

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
