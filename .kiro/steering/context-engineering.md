---
inclusion: fileMatch
fileMatchPattern: "**/context-engineering/**,**/*context*.py"
description: Context Engineering (Layer 2) patterns and implementations
version: "1.0.0"
---

# Context Engineering — Layer 2

**Steering File:** Context Engineering (CC-00 Layer 2)  
**Inclusion:** Conditional — Activated when working in `context-engineering/` or context-related Python files  
**Authority:** CC-00 Laboratory — Layer 2: How to structure it

---

## Module Identity

**Context Engineering** is Layer 2 of the CC-00 engineering stack — the discipline of architecting the LLM's context window.

| Field          | Detail                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------- |
| **Layer**      | 2 — How to structure it                                                                         |
| **Type**       | Knowledge base + Production framework                                                           |
| **Scope**      | Context window anatomy, memory types, dynamic assembly, multi-agent handoff, session management |
| **Output**     | Context assembly patterns, memory implementations, handoff protocols                            |
| **Has Code**   | Yes — 3 Python implementations                                                                  |
| **Upstream**   | Consumes prompt patterns from `prompt-engineering/` and retrieved content from RAG              |
| **Downstream** | Feeds assembled context windows to `harness-engineering/` for safe execution                    |

---

## Core Concepts

### Four-Slot Context Window

```
Context Window Anatomy
├── System Slot ← Prompt patterns, agent identity, operating rules
├── Retrieved Slot ← RAG-retrieved chunks (ACL-filtered, reranked)
├── History Slot ← Conversation memory (episodic + working)
└── Tool Outputs Slot ← Function call results, execution logs
```

### Four Memory Types

| Memory Type    | Purpose                                  | Lifespan    | Example                                    |
| -------------- | ---------------------------------------- | ----------- | ------------------------------------------ |
| **Episodic**   | What happened (events, actions, results) | Session     | "User approved Stage 3 at 14:32"           |
| **Semantic**   | What is known (facts, definitions)       | Persistent  | "The project uses Kotlin Multiplatform"    |
| **Procedural** | How to do things (workflows, patterns)   | Persistent  | "Run prettier before committing"           |
| **Working**    | Current task state (active context)      | Task-scoped | "Currently implementing dark mode feature" |

---

## Key Production Implementations

All paths relative to `core-component-00/context-engineering/implementations/`:

| File                    | Purpose                                              | Test Suite                     |
| ----------------------- | ---------------------------------------------------- | ------------------------------ |
| `context_assembler.py`  | Four-slot context window assembly at runtime         | `../testing/test_assembler.py` |
| `memory_store.py`       | Episodic, semantic, procedural, working memory       | `../testing/test_memory.py`    |
| `context_compressor.py` | Long-session compression for token budget compliance | —                              |

---

## Key Patterns

All paths relative to `core-component-00/context-engineering/patterns/`:

| Pattern                      | Purpose                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `multi-agent-handoff.md`     | Context Handoff Protocol (Full / Scoped / Minimal tiers)   |
| `sacred-context.md`          | Preserving decision continuity across long agent sessions  |
| `dynamic-assembly.md`        | Runtime context window assembly based on task requirements |
| `token-budget-management.md` | Managing context window size within model limits           |

---

## Multi-Agent Context Handoff Protocol

When passing context between agents:

| Tier        | What's Shared                                            | When to Use                         |
| ----------- | -------------------------------------------------------- | ----------------------------------- |
| **Full**    | Complete context window (all four slots)                 | Successor agent continues same task |
| **Scoped**  | Task-specific subset (working memory + relevant history) | Specialist agent handles subtask    |
| **Minimal** | Task description only (no history)                       | Independent parallel agent          |

See `patterns/multi-agent-handoff.md` for full protocol specification.

---

## Agent Behavior Rules for Context Engineering

When working with context:

1. **Use four-slot structure** — All context windows must follow System / Retrieved / History / Tool Outputs anatomy
2. **Choose correct memory type** — Match memory type to information lifespan and purpose
3. **Apply handoff protocol** — Use appropriate tier (Full / Scoped / Minimal) when passing context between agents
4. **Monitor token budget** — Use `context_monitor.py` from harness-engineering to enforce limits
5. **Compress long sessions** — Apply `context_compressor.py` when approaching context budget limits
6. **Preserve Sacred Context** — Maintain decision continuity per `patterns/sacred-context.md`

---

## Integration Points

| From                              | To                                   | What Flows                                 |
| --------------------------------- | ------------------------------------ | ------------------------------------------ |
| `prompt-engineering/`             | Context Engineering (System slot)    | Prompt patterns                            |
| `retrieval-augmented-generation/` | Context Engineering (Retrieved slot) | RAG-retrieved, reranked chunks             |
| Context Engineering               | `harness-engineering/`               | Assembled, budget-compliant context window |
| `multi-agent-engineering/`        | Context Engineering                  | Handoff packets (Full / Scoped / Minimal)  |

---

## Related Steering Files

- `prompt-engineering.md` — Layer 1: Prompt patterns that fill the System slot
- `harness-engineering.md` — Layer 3: Safe execution of assembled context windows
- `rag-engineering.md` — Layer 4: Retrieved content that fills the Retrieved slot
- `multi-agent-engineering.md` — Layer 5: Context handoff between agents
- `ase-framework.md` — ASE governance and compliance requirements
- `cc00-overview.md` — Complete CC-00 laboratory overview

---

**This steering file is automatically activated when working in `context-engineering/` directories or context-related Python files.**
