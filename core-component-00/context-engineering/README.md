# Context Engineering

> The discipline of deciding **what information** the model needs, **how to structure it**, and **how to maintain it** across the full lifecycle of an agent session.

---

## What Is Context Engineering?

Context Engineering is the architectural layer between your application and the model's context window. While prompt engineering asks _"how do I write this instruction?"_, context engineering asks _"what should be in the context window at all?"_

It answers three questions that no other discipline covers:

1. **What to include** — which memories, documents, tool results, and instructions belong in the current context window
2. **How to structure it** — which slot (system / history / retrieved / tool) each piece of information should occupy, and in what order
3. **How to maintain it** — how context evolves across turns, how memory persists between sessions, and how to prevent degradation

---

## Documentation Structure

| File / Folder                            | Purpose                                                  | Target Audience         |
| ---------------------------------------- | -------------------------------------------------------- | ----------------------- |
| `README.md`                              | This file — overview and navigation                      | All                     |
| `CONCEPTS.md`                            | The Six Pillars of Context Engineering                   | Architects, Leads       |
| `quick-reference.md`                     | Decision matrices, assembly cheat sheet, memory selector | All engineers           |
| `fundamentals/context-window-anatomy.md` | What belongs in each slot and why                        | Engineers               |
| `fundamentals/memory-types.md`           | Episodic, semantic, procedural, working memory           | Engineers, Architects   |
| `patterns/assembly-patterns.md`          | Dynamic context assembly patterns                        | Implementers            |
| `patterns/multi-agent-handoff.md`        | Context forwarding between agents                        | Orchestration engineers |
| `implementations/context_assembler.py`   | Production context assembly engine                       | Implementers            |
| `implementations/memory_store.py`        | Memory type implementations                              | Implementers            |
| `implementations/context_compressor.py`  | Advanced context compression                             | Implementers            |
| `testing/test_context_assembler.py`      | Executable pytest suite                                  | QA, CI/CD               |
| `testing/test_memory_store.py`           | Executable pytest suite                                  | QA, CI/CD               |
| `testing/edge-cases.md`                  | Context poisoning, overflow, stale memory scenarios      | QA Engineers            |
| `workspace/strategy.md`                  | Context engineering strategy for this workspace          | Leads                   |
| `workspace/integration-guide.md`         | Integration with harness-engineering and RAG             | All engineers           |

---

## Quick Start (3-Minute Tour)

### Step 1: Understand the Four Context Slots

Every model call has four slots. Fill them intentionally:

| Slot             | Contains                             | Token Budget |
| ---------------- | ------------------------------------ | ------------ |
| **System**       | Role, rules, persistent instructions | ≤ 15%        |
| **History**      | Conversation turns (compressed)      | ≤ 40%        |
| **Retrieved**    | RAG documents, memory lookups        | ≤ 30%        |
| **Tool Outputs** | Results from tool calls              | ≤ 15%        |

### Step 2: Choose Your Memory Type

| I need to remember...               | Use                |
| ----------------------------------- | ------------------ |
| What happened in this session       | `EpisodicMemory`   |
| Facts that are always true          | `SemanticMemory`   |
| How to behave in certain situations | `ProceduralMemory` |
| What I am doing right now           | `WorkingMemory`    |

### Step 3: Assemble Context at Runtime

```python
from implementations.context_assembler import ContextAssembler
from implementations.memory_store import EpisodicMemory, SemanticMemory

assembler = ContextAssembler(max_tokens=128_000)
assembler.set_system("You are an expert software architect.")
assembler.add_retrieved(semantic_mem.query("authentication patterns"))
assembler.add_history(episodic_mem.recent_turns(n=5))

context = assembler.build()  # Returns priority-ordered, budget-aware context
```

---

## How Context Engineering Relates to the Other Modules

```
prompt-engineering/         ← How to write instructions (what words to use)
        ↓
context-engineering/        ← What to put in the window and how to structure it
        ↓
harness-engineering/        ← How to safely execute the model call at runtime
        ↑
retrieval-augmented-generation/ ← Source of retrieved content fed into context
```

Context engineering sits at the centre of the stack. It consumes output from RAG (retrieved content), shapes the input for harness-engineering (the assembled context), and is informed by prompt engineering (how instructions are written within each slot).

---

## Security Checklist

Before any deployment:

| Check                                                                               | Security Risk Mitigated                              |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------- |
| System slot contains only static, validated instructions (no user-injected content) | Prompt injection — user gains system-level authority |
| Retrieved content is ACL-filtered before assembly                                   | Unauthorised documents reaching the model's context  |
| History is compressed and PII-scrubbed before inclusion                             | Privacy leakage in shared or logged contexts         |
| Tool outputs are schema-validated before entering context                           | Model reasoning from corrupted or malicious data     |
| Total assembled context is within 90% of model's context limit                      | Silent context overflow and unpredictable truncation |

---

## Document Status

| Document                               | Version | Last Updated |
| -------------------------------------- | ------- | ------------ |
| README.md                              | 1.0     | 2026-04-28   |
| CONCEPTS.md                            | 1.0     | 2026-04-28   |
| quick-reference.md                     | 1.0     | 2026-04-28   |
| fundamentals/context-window-anatomy.md | 1.0     | 2026-04-28   |
| fundamentals/memory-types.md           | 1.0     | 2026-04-28   |
| patterns/assembly-patterns.md          | 1.0     | 2026-04-28   |
| patterns/multi-agent-handoff.md        | 1.0     | 2026-04-28   |
| implementations/context_assembler.py   | 1.0     | 2026-04-28   |
| implementations/memory_store.py        | 1.0     | 2026-04-28   |
| implementations/context_compressor.py  | 1.0     | 2026-04-28   |

**Maintained by:** Claude Lab Engineering Team
