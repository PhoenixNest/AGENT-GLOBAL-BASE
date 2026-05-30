---
paths:
  - "**/context-engineering/**"
  - "**/*context*.py"
description: Context Engineering (Layer 2) patterns and behavior rules
---

# Context Engineering — Layer 2

**Scope:** Context window anatomy, memory types, dynamic assembly, multi-agent handoff

---

## Four-Slot Context Window

```
Context Window Anatomy
├── System Slot      ← Prompt patterns, agent identity, operating rules
├── Retrieved Slot   ← RAG-retrieved chunks (ACL-filtered, reranked)
├── History Slot     ← Conversation memory (episodic + working)
└── Tool Outputs Slot ← Function call results, execution logs
```

---

## Four Memory Types

| Memory Type    | Purpose                                  | Lifespan    |
| -------------- | ---------------------------------------- | ----------- |
| **Episodic**   | What happened (events, actions, results) | Session     |
| **Semantic**   | What is known (facts, definitions)       | Persistent  |
| **Procedural** | How to do things (workflows, patterns)   | Persistent  |
| **Working**    | Current task state (active context)      | Task-scoped |

---

## Key Implementations

| File                    | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| `context_assembler.py`  | Four-slot context window assembly at runtime         |
| `memory_store.py`       | Episodic, semantic, procedural, working memory       |
| `context_compressor.py` | Long-session compression for token budget compliance |

---

## Multi-Agent Context Handoff Protocol

| Tier        | What's Shared                            | When to Use                         |
| ----------- | ---------------------------------------- | ----------------------------------- |
| **Full**    | Complete context window (all four slots) | Successor agent continues same task |
| **Scoped**  | Task-specific subset                     | Specialist agent handles subtask    |
| **Minimal** | Task description only                    | Independent parallel agent          |

---

## Behavior Rules

1. Use four-slot structure for all context windows
2. Choose correct memory type matching information lifespan
3. Apply appropriate handoff tier (Full / Scoped / Minimal)
4. Monitor token budget with `context_monitor.py`
5. Compress long sessions with `context_compressor.py`
6. Preserve Sacred Context — maintain decision continuity
