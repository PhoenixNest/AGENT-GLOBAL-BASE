# RAG Integration Blueprint — Casual Games Studio

> **ASE Layer:** 4 — RAG / Memory
> **Status:** Intentional Scope Exception (documented rationale below)
> **Authority:** Studio Director Dr. Marcus Vogel + CTO Dr. Kenji Nakamura
> **Exception rationale required by:** `adr-ase-001.md` (studio) §Layer 4

---

## 1. Exception Statement

The Casual Games Studio **intentionally operates without a live retrieval pipeline** at this time. This is a documented exception under ADR-ASE-001 §Exceptions — not an oversight.

This document records the rationale, the alternative mechanisms used in place of RAG, and the conditions that would trigger L4 implementation.

---

## 2. Rationale for Intentional Absence

### 2.1 Knowledge Base Is Static and Bounded

The studio's knowledge corpus is:

| Source                          | Type                      | Size   | Access method    |
| :------------------------------ | :------------------------ | :----- | :--------------- |
| Crew profiles (38+ documents)   | Static, versioned         | Small  | Direct file read |
| GDD / PRD / SRD (per project)   | Project-scoped            | Medium | Direct file read |
| Pipeline specification          | Static                    | Small  | Direct file read |
| Kill gate threshold definitions | Embedded in pipeline spec | Tiny   | Direct file read |
| Stage artifact templates        | Static                    | Small  | Direct file read |

None of these require embedding-based retrieval. All are directly navigable by an LLM agent with file-reading capability.

### 2.2 No Time-Sensitive External Facts

The studio does not depend on:

- Real-time market data
- Live analytics feeds (these are ingested at defined pipeline stages, not continuously)
- External knowledge APIs
- Frequently-changing competitive intelligence at inference time

### 2.3 Retrieval Latency Is Not a Bottleneck

Stage transitions occur on human-scale timelines (days to weeks). Sub-second retrieval is not a requirement. The overhead of a vector database + embedding pipeline would add complexity with no observable benefit.

### 2.4 Alternative Mechanisms Cover the Need

| RAG capability         | Studio alternative                                              |
| :--------------------- | :-------------------------------------------------------------- |
| Knowledge retrieval    | Direct file read of GDD, profiles, pipeline spec                |
| Institutional memory   | `knowledge-transfer-protocol.md` Tier 3 retrospectives          |
| Session memory         | `checkpoint.json` (machine-readable state) + `session-log.md`   |
| Cross-project learning | Project retrospective documents under `library/retrospectives/` |

---

## 3. Alternative: Static Knowledge Base Pattern

The studio uses the **Knowledge Item (KI) pattern** from CC-00 for high-frequency reference data:

```
Hot knowledge items (included in every dispatch context):
  - Kill gate thresholds for the current stage (from pipeline spec)
  - Active GDD chapter relevant to the crew member's division
  - Crew member's own profile + skills

Warm knowledge items (included on request):
  - Prior stage outputs summarised in checkpoint.json
  - Retrospective lessons from the last project

Cold knowledge items (not routinely included):
  - Full GDD (reference only the active chapter)
  - Full crew roster (reference only relevant division)
  - Complete pipeline specification (reference only current stage)
```

This MVC (Minimum Viable Context) discipline achieves the intent of retrieval — providing the right information at the right time — without an embedding pipeline.

---

## 4. Trigger Conditions for L4 Implementation

This exception must be re-evaluated if **any** of the following occur:

| Trigger                              | Threshold                                    | Action                      |
| :----------------------------------- | :------------------------------------------- | :-------------------------- |
| Multiple simultaneous game projects  | ≥ 2 projects in Stage 5+ concurrently        | Evaluate L4                 |
| Knowledge corpus growth              | Total crew + project documents > 500 files   | Evaluate L4                 |
| Crew agent knowledge-access friction | > 2 documented incidents per stage cycle     | L4 implementation triggered |
| External data dependency added       | Any real-time market/analytics feed required | L4 required immediately     |
| Studio Director QBR recommendation   | Explicit recommendation at any QBR           | L4 planning initiated       |

---

## 5. Planned L4 Architecture (If Triggered)

If the exception is lifted, the studio will implement a RAG pipeline following the CC-00 reference architecture:

| Phase                 | Implementation                                                                   | Reference                                                                   |
| :-------------------- | :------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| Phase 1 (File-based)  | Direct file retrieval; no embedding                                              | Current state                                                               |
| Phase 2 (Embedding)   | Embed crew profiles + GDD corpus using `all-MiniLM-L6-v2`; local Qdrant instance | `core-component-00/retrieval-augmented-generation/`                         |
| Phase 3 (Agentic RAG) | Multi-step retrieval with reranking; ACL per crew division                       | `core-component-00/retrieval-augmented-generation/architecture/overview.md` |

**Chunking strategy (Phase 2):** 500–800 tokens per chunk, 100–200 token overlap.
**Embedding model:** Pin to `all-MiniLM-L6-v2` until specialisation is warranted.
**Reranking:** Cross-encoder rerank; top-K = 10 before context assembly.
**ACL:** Per-division access control — audio crew cannot retrieve engineering branch ADRs.

---

## 6. Review Schedule

- **Each QBR (Stage 10):** Studio Director reviews trigger conditions §4
- **On new project launch:** Check simultaneous project count
- **Annually:** Full review of knowledge corpus size and crew friction metrics
