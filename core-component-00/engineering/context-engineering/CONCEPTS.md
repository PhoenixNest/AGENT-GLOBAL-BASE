# Context Engineering: Core Concepts and Foundations

## 1. What Is Context Engineering?

### Definition

**Context Engineering** is the discipline of architecting, assembling, and maintaining the information state that a language model receives at inference time. It treats the context window not as a passive text buffer, but as a **precision-managed resource** that directly determines response quality.

### The Central Insight

LLMs have no persistent memory. They cannot remember previous sessions. They cannot look things up unless you put that information in the context window. Every piece of knowledge, every instruction, every fact the model needs must be explicitly placed in the window before inference — or it will be lost or hallucinated.

> Context Engineering is the discipline of deciding what that window contains.

### How Context Engineering Differs from Related Disciplines

| Dimension           | Prompt Engineering                       | Harness Engineering                           | Context Engineering                          |
| ------------------- | ---------------------------------------- | --------------------------------------------- | -------------------------------------------- |
| **Core Question**   | How do I write this instruction?         | How do I safely execute this model call?      | What information should be in the window?    |
| **Primary Concern** | Wording, structure, examples in a prompt | Error handling, token limits, tool boundaries | Memory, assembly, slot allocation, freshness |
| **Time Horizon**    | Single prompt                            | Single model call                             | Entire agent session or multi-turn workflow  |
| **Key Output**      | A well-structured prompt                 | A safely wrapped API call                     | A precision-assembled context window         |
| **Primary Skill**   | Language and reasoning patterns          | Software engineering                          | Information architecture                     |

---

## 2. The Six Pillars of Context Engineering

### Pillar 1: Context Window Anatomy

The context window is not a single text blob. It has four distinct **slots**, each with a different purpose, authority level, and token budget:

```
┌─────────────────────────────────────────────────────┐
│  SYSTEM SLOT          ≤ 15% of budget               │
│  Role definition, persistent rules, output format   │
│  Authority: Highest — sets model behaviour          │
├─────────────────────────────────────────────────────┤
│  RETRIEVED SLOT       ≤ 30% of budget               │
│  RAG documents, memory lookups, external facts      │
│  Authority: Informational — cited, not trusted      │
├─────────────────────────────────────────────────────┤
│  HISTORY SLOT         ≤ 40% of budget               │
│  Compressed conversation turns                      │
│  Authority: Contextual — informs but doesn't rule   │
├─────────────────────────────────────────────────────┤
│  TOOL OUTPUT SLOT     ≤ 15% of budget               │
│  Results from tool calls, validated responses       │
│  Authority: Factual — treated as ground truth       │
└─────────────────────────────────────────────────────┘
```

**Key Principle:** Mixing slot types degrades performance. User-injected content must never reach the system slot. Retrieved content must be labelled as such. Tool outputs must be validated before entering context.

---

### Pillar 2: Memory Architecture

An agent session involves four distinct types of memory, each serving a different cognitive function:

| Memory Type           | What It Stores                                                          | Lifespan      | Storage Layer                 |
| --------------------- | ----------------------------------------------------------------------- | ------------- | ----------------------------- |
| **Working Memory**    | The current task and its immediate sub-goals                            | Single turn   | Active context window         |
| **Episodic Memory**   | What happened — events, decisions, outcomes from this session           | Session       | In-session store              |
| **Semantic Memory**   | What is known — persistent facts, user preferences, domain knowledge    | Cross-session | Persistent database           |
| **Procedural Memory** | How to behave — learned patterns, workflow templates, skill activations | Cross-session | Agent profile / system prompt |

**Key Principle:** Only working memory lives in the context window at all times. All other memory types are selectively retrieved into the retrieved slot when needed — not dumped wholesale.

---

### Pillar 3: Dynamic Context Assembly

Context is not static. The right context for a code review task is different from the right context for a creative writing task. Assembly must be **task-aware** and **priority-ordered**.

```
Input: Task type, user query, available memory
       ↓
Step 1: Classify task (analytical / creative / tool-use / retrieval)
Step 2: Select memory types needed for this task
Step 3: Retrieve from memory stores (episodic + semantic)
Step 4: Allocate slot budgets based on task type
Step 5: Prioritize content within each slot (recency + relevance)
Step 6: Compress to fit budget (lossy for history, lossless for tools)
Step 7: Assemble final context in slot order (system → retrieved → history → tools)
Output: Budget-compliant, priority-ordered context window
```

**Key Principle:** Never assemble context by concatenation. Always assemble by priority score within budget constraints.

---

### Pillar 4: Context Compression

As sessions grow, raw context exceeds the token budget. Compression must be **selective** (not every turn is equally important) and **typed** (different content types compress differently):

| Content Type               | Compression Strategy                             | Information Loss   |
| -------------------------- | ------------------------------------------------ | ------------------ |
| Conversation turns         | Hierarchical summarization                       | Lossy — acceptable |
| Tool outputs               | Schema-reduction (keep keys, drop verbose prose) | Lossless           |
| Retrieved documents        | Extractive summarization + citation preservation | Low-loss           |
| Decisions and commitments  | Never compress — always retain verbatim          | None               |
| Error messages and retries | Drop resolved errors; keep unresolved            | Low-loss           |

**Key Principle:** Decisions and commitments made during the session are **sacred context** — they must never be compressed or discarded. Losing them causes the model to contradict itself or re-open closed decisions.

---

### Pillar 5: Multi-Agent Context Passing

When an orchestrator agent delegates to a subagent, it must decide what context to forward. Forwarding too little causes the subagent to lack needed information. Forwarding too much wastes the subagent's token budget and introduces noise.

The **Context Handoff Protocol** defines three forwarding tiers:

| Tier                | What Gets Forwarded                      | When to Use                                     |
| ------------------- | ---------------------------------------- | ----------------------------------------------- |
| **Full handoff**    | Entire context window                    | Subagent is continuing the same task            |
| **Scoped handoff**  | System + task-specific extracted context | Subagent handles a bounded sub-task             |
| **Minimal handoff** | System + task description only           | Subagent is independent (e.g. a pure tool call) |

**Key Principle:** The subagent's context window should contain exactly what it needs to do its job — no more, no less. The orchestrator is responsible for making this selection.

---

### Pillar 6: Context Quality and Defense

Context degrades over time in predictable ways. Context Engineering includes active defenses:

| Degradation Type       | Cause                                                            | Defense                                                                     |
| ---------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Context poisoning**  | Malicious or contradictory content accumulating in history       | Input validation before history append; periodic history audit              |
| **Role drift**         | System instructions getting diluted by long conversation history | System slot always prepended, never overwritten                             |
| **Staleness**          | Semantic memory or retrieved content that is outdated            | TTL-based invalidation; timestamp-aware retrieval weighting                 |
| **Echo chamber**       | Model repeatedly affirming earlier (possibly wrong) positions    | Inject "challenge" prompt on high-confidence repeated claims                |
| **Attention dilution** | Critical information buried deep in a long context               | Always place highest-priority content at the beginning and end of each slot |

---

## 3. The Context Engineering Flow

```
┌─────────────────────────────────────────────────────────┐
│                    PRE-ASSEMBLY PHASE                    │
│  1. Receive task and user query                          │
│  2. Classify task type → determines slot budget split    │
│  3. Query episodic memory → recent session events        │
│  4. Query semantic memory → relevant persistent facts    │
│  5. Trigger RAG retrieval → relevant documents           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                    ASSEMBLY PHASE                        │
│  6. Score and rank all retrieved content by relevance    │
│  7. Allocate token budgets per slot                      │
│  8. Compress history to fit budget                       │
│  9. Build context in slot order                          │
│  10. Validate total token count ≤ 90% of limit           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                  POST-INFERENCE PHASE                    │
│  11. Extract decisions and commitments from response     │
│  12. Write new episodic memory entry                     │
│  13. Update semantic memory with new facts               │
│  14. Update working memory with task progress            │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Context Budget Allocation by Task Type

| Task Type                   | System | History | Retrieved | Tool Output |
| --------------------------- | ------ | ------- | --------- | ----------- |
| **Factual Q&A**             | 10%    | 10%     | 65%       | 15%         |
| **Code generation**         | 15%    | 20%     | 45%       | 20%         |
| **Creative writing**        | 20%    | 50%     | 20%       | 10%         |
| **Tool-augmented research** | 10%    | 15%     | 35%       | 40%         |
| **Multi-turn reasoning**    | 15%    | 55%     | 20%       | 10%         |
| **Agent orchestration**     | 20%    | 10%     | 30%       | 40%         |

---

## 5. Relationship to Other Modules

| Module                            | Provides to Context Engineering               | Receives from Context Engineering                        |
| --------------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| `prompt-engineering/`             | Patterns for writing content within each slot | Slot structure as the container for well-written prompts |
| `harness-engineering/`            | Token budget limits that constrain assembly   | A pre-assembled, budget-compliant context to execute     |
| `retrieval-augmented-generation/` | Retrieved documents for the retrieved slot    | Slot budget and priority guidance for what to retrieve   |

---

## 6. Production Checklist

| Category         | Check                                                   | Status |
| ---------------- | ------------------------------------------------------- | ------ |
| **Slot hygiene** | User input never reaches system slot                    | ☐      |
|                  | Retrieved content is labelled with source and timestamp | ☐      |
|                  | Tool outputs are schema-validated before entry          | ☐      |
| **Memory**       | Decisions and commitments retained verbatim             | ☐      |
|                  | Semantic memory has TTL or freshness check              | ☐      |
|                  | Episodic memory is session-scoped                       | ☐      |
| **Assembly**     | Context assembled by priority score, not concatenation  | ☐      |
|                  | Total tokens ≤ 90% of model limit before call           | ☐      |
| **Defense**      | Input validation before history append                  | ☐      |
|                  | System slot is prepended on every turn                  | ☐      |

---

## 7. References

- [Context Window Anatomy](./fundamentals/context-window-anatomy.md)
- [Memory Types](./fundamentals/memory-types.md)
- [Assembly Patterns](./patterns/assembly-patterns.md)
- [Multi-Agent Handoff](./patterns/multi-agent-handoff.md)
- [Harness Engineering — Token Budget Management](core-component-00/engineering/harness-engineering/implementations/context_monitor.py)
- [RAG Architecture Overview](core-component-00/retrieval-augmented-generation/architecture/overview.md)
- [Prompt Engineering Fundamentals](core-component-00/engineering/prompt-engineering/fundamentals/research.md)

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**Maintained by:** Claude Lab Engineering Team
