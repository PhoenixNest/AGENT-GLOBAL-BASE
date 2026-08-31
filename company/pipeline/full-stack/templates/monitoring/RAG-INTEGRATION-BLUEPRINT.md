# RAG Integration Blueprint — Semantic Retrieval Architecture

> **Addresses Gap:** #6 (No vector/semantic search over project artifacts)

---

## 1. Purpose

This blueprint defines the architecture for **semantic retrieval** over the company's accumulated knowledge — enabling agents to find relevant context by meaning, not just by file path or keyword. It transforms the static knowledge base into a queryable memory system.

---

## 2. Current State (Pre-RAG)

| Retrieval Method     | How It Works                                 | Limitation                                 |
| :------------------- | :------------------------------------------- | :----------------------------------------- |
| **File path**        | Orchestrator knows where files are           | Requires memorizing 200+ file locations    |
| **Keyword search**   | `grep` / `ripgrep` over workspace            | Misses semantic matches ("auth" ≠ "login") |
| **MVC Profile**      | Agent profiles list required context         | Static — doesn't adapt to task content     |
| **Manual injection** | Orchestrator reads files, copies into prompt | Expensive, error-prone, doesn't scale      |

**Result:** ~65% RAG/Memory coverage. Agents can access knowledge, but retrieval is manual and fragile.

---

## 3. Target Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    AGENT CONTEXT WINDOW                       │
│  Zone A: Identity + Rules                                    │
│  Zone B: Retrieved Context (from RAG) ◄──── NEW             │
│  Zone C: Output Schema + Constraints                         │
└─────────────────────────┬────────────────────────────────────┘
                          │ Query
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   RAG RETRIEVAL LAYER                         │
│                                                              │
│  ┌─────────────┐  ┌───────────────┐  ┌──────────────────┐   │
│  │  Semantic    │  │   Keyword     │  │  Structured      │   │
│  │  Search      │  │   Search      │  │  Lookup          │   │
│  │  (Embeddings)│  │   (ripgrep)   │  │  (JSON schemas)  │   │
│  └──────┬──────┘  └───────┬───────┘  └────────┬─────────┘   │
│         │                 │                    │              │
│         └─────────────────┼────────────────────┘              │
│                           │                                   │
│                    ┌──────▼──────┐                            │
│                    │  Re-Ranker  │                            │
│                    │  + MVC      │                            │
│                    │  Filter     │                            │
│                    └──────┬──────┘                            │
│                           │                                   │
└───────────────────────────┼──────────────────────────────────┘
                            │ Ranked Results
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE STORE                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Tier 1     │  │   Tier 2     │  │   Tier 3         │   │
│  │   Session    │  │   Project    │  │   Institutional  │   │
│  │   Artifacts  │  │   Retros     │  │   Memory         │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Agent      │  │   Skill      │  │   Pipeline       │   │
│  │   Profiles   │  │   Guidelines │  │   Definitions    │   │
│  │   (79 files) │  │   (201 files)│  │   (5 pipelines)  │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Knowledge Corpus Definition

| Corpus Partition          | Source                                                        |  File Count   | Update Frequency          |
| :------------------------ | :------------------------------------------------------------ | :-----------: | :------------------------ |
| **Agent Profiles**        | `company/departments/**/agent/profile.md`                     |      80       | Rare (profile updates)    |
| **Skill Guidelines**      | `company/departments/**/skills/*.md`                          |     ~250      | Moderate (new guidelines) |
| **Pipeline Definitions**  | `company/pipeline/*/pipeline.md`                              |       5       | Rare (ADR-level changes)  |
| **Pipeline Templates**    | `company/pipeline/*/templates/**/*.md`                        |      34       | Moderate (new templates)  |
| **Company Library**       | `company/library/**/*.md`                                     |      ~30      | Low                       |
| **Tier 1 Artifacts**      | `company/project/*/stages/**`                                 |   Variable    | High (per project)        |
| **Tier 2 Retrospectives** | `company/project/*/retrospective.md`                          | 1 per project | Once (at Stage 10)        |
| **Tier 3 Institutional**  | `company/library/topics/institutional-memory.md`              |       1       | Quarterly                 |
| **ASGF Framework**        | `core-component-00/framework/05-multi-agent-engineering/*.md` |      ~5       | Low                       |

**Total Static Corpus:** ~355 files
**Total Dynamic Corpus:** Grows with each project

---

## 5. Retrieval Strategies

### 5.1 Pre-Stage Retrieval (Proactive)

Before dispatching to any agent, the orchestrator executes:

```
1. Read agent's MVC Profile for Stage N
2. For each ✅ context item:
   a. If item is a specific file → direct file read
   b. If item is a category ("security ADRs") → structured lookup
   c. If item is conceptual ("similar past decisions") → semantic search
3. Apply MVC filter: include only ✅ items
4. Apply size budget: Zone B ≤ 40% of context window
5. If over budget → summarize longest items first
```

### 5.2 On-Demand Retrieval (Reactive)

During task execution, an agent may need additional context:

```
Agent issues a CONTEXT_REQUEST:
  query: "How did we handle certificate pinning in the last project?"
  scope: [Tier 2, Tier 3]  // limit search space
  max_results: 3

Orchestrator executes:
  1. Semantic search over specified scope
  2. Re-rank by relevance to agent's current stage
  3. Apply MVC filter (no sensitive data leakage across agents)
  4. Return top-K results as Zone B context addition
```

### 5.3 Cross-Project Retrieval

When starting a new project, the orchestrator executes:

```
1. Read all Tier 2 retrospectives for projects with similar:
   - Platform strategy (native_dual, kmp, flutter)
   - Feature domain (payments, social, content)
   - Team composition
2. Extract relevant Tier 3 patterns
3. Inject into Stage 1 agent context as "Prior Art" section
4. Flag any estimation calibration data for Stage 4
```

---

## 6. Implementation Phases

### Phase 3A — File-Based RAG (Current Session)

**Approach:** Use the existing file system + ripgrep + structured lookups.

- The orchestrator reads files directly based on MVC Profiles
- Keyword search via `grep_search` for discovery
- Stage Transition Schemas provide structured lookup targets
- Knowledge Transfer Protocol defines retrieval tiers

**Coverage improvement:** 65% → **80%**

### Phase 3B — Embedding-Based RAG (Future)

**Approach:** Index all corpus files into a vector store.

| Component       | Recommendation                                                     |
| :-------------- | :----------------------------------------------------------------- |
| Embedding model | `text-embedding-004` (Google) or `text-embedding-3-small` (OpenAI) |
| Vector store    | ChromaDB (local), Pinecone (cloud), or Vertex AI Vector Search     |
| Chunk size      | 512 tokens with 64-token overlap                                   |
| Metadata        | `{file_path, stage, agent_tier, knowledge_tier, last_updated}`     |
| Re-ranker       | Cross-encoder on top-20 candidates → return top-5                  |

**Coverage improvement:** 80% → **95%**

### Phase 3C — Agentic RAG (Future)

**Approach:** Agents can autonomously query the knowledge store during execution.

- Agents issue `CONTEXT_REQUEST` messages per IACP
- Orchestrator brokers retrieval using semantic search
- Results injected as mid-execution context updates
- Token budget managed dynamically

**Coverage improvement:** 95% → **98%+**

---

## 7. Quality Metrics

| Metric                   | Target                                                  | Measurement                                |
| :----------------------- | :------------------------------------------------------ | :----------------------------------------- |
| **Retrieval relevance**  | ≥ 85% of retrieved items are actually used              | Agent reports unused context items         |
| **Context completeness** | ≥ 95% of needed items found without manual intervention | Agent issues ≤ 1 CONTEXT_REQUEST per stage |
| **Latency**              | < 5 seconds per retrieval                               | Measured at orchestrator                   |
| **Budget compliance**    | Zone B ≤ 40% of window                                  | Measured before dispatch                   |
| **Staleness rate**       | ≤ 5% of retrieved items are outdated                    | Cross-reference with artifact versions     |

---

## 8. Security Constraints

| Constraint                     | Rule                                                                                               |
| :----------------------------- | :------------------------------------------------------------------------------------------------- |
| **Cross-project isolation**    | Tier 1 artifacts from Project A are NOT accessible to Project B agents unless promoted to Tier 2/3 |
| **Security artifact handling** | SRD, SIS, and Red Team reports are retrievable ONLY by CSO, security engineers, and CTO            |
| **No raw credential exposure** | API keys, secrets, and credentials are NEVER indexed in the RAG corpus                             |
| **Agent tier access**          | IC-tier agents cannot retrieve C-Suite strategy documents                                          |

---

## 9. Integration Points

| Component                               | RAG Integration                                           |
| :-------------------------------------- | :-------------------------------------------------------- |
| `mvc-context-profile.md`                | Defines what to retrieve for each agent/stage combination |
| `knowledge-transfer-protocol.md`        | Defines the 3-tier knowledge hierarchy that RAG indexes   |
| `stage-transition-schemas.md`           | Structured lookup targets for stage artifact retrieval    |
| `inter-agent-communication-protocol.md` | `CONTEXT_REQUEST` message format for reactive retrieval   |
| `context-engineering.md`                | Zone A/B/C placement rules for retrieved content          |
