# core-component-00/context-engineering/ — Layer 2: Context Engineering

CC-00 Layer 2 — "How to structure it." This module provides the framework for assembling, storing,
compressing, and handing off context windows in LLM-powered systems.

---

## What Lives Here

This module combines knowledge documentation with production-grade Python implementations and a
pytest test suite. It is one of three CC-00 modules with runnable code.

---

## Directory Structure

```
context-engineering/
├── fundamentals/          ← Conceptual docs: context windows, memory types, compression theory
├── patterns/              ← Reusable patterns (multi-agent handoff, sacred context, etc.)
├── implementations/       ← Production Python code (import from here)
│   ├── context_assembler.py    ← Four-slot context window assembly
│   ├── memory_store.py         ← Episodic, semantic, procedural, working memory
│   └── context_compressor.py   ← Long-session compression for token budget compliance
└── testing/               ← pytest test suite
```

---

## Key Implementations

| File                                    | Class / Entry Point | Purpose                                                    |
| --------------------------------------- | ------------------- | ---------------------------------------------------------- |
| `implementations/context_assembler.py`  | `ContextAssembler`  | Assembles the four-slot context window at runtime          |
| `implementations/memory_store.py`       | `MemoryStore`       | Manages episodic, semantic, procedural, and working memory |
| `implementations/context_compressor.py` | `ContextCompressor` | Compresses long sessions while preserving information      |

---

## Running Tests

Run from `core-component-00/` (not workspace root) to avoid import conflicts:

```powershell
pytest context-engineering/testing/ -v
```

Tests import via `from implementations.<module>` — the module root must be on `sys.path`. The test
suite handles this automatically when run from the correct directory.

---

## Import Pattern

```python
import sys
sys.path.insert(0, "path/to/core-component-00/context-engineering")
from implementations.context_assembler import ContextAssembler
from implementations.memory_store import MemoryStore
from implementations.context_compressor import ContextCompressor
```

---

## Active Research Programmes

| Programme                    | Open Question                                                    |
| ---------------------------- | ---------------------------------------------------------------- |
| Context Compression Theory   | Minimum information-preserving compression of a 100-turn session |
| Multi-Agent Memory Coherence | Distributed shared memory without a central store                |

---

## Key Patterns

| Pattern             | Location                          | When to Use                                            |
| ------------------- | --------------------------------- | ------------------------------------------------------ |
| Multi-Agent Handoff | `patterns/multi-agent-handoff.md` | Inter-agent context transfer                           |
| Sacred Context      | `fundamentals/`                   | Protecting critical context under token pressure       |
| Four-Slot Assembly  | `fundamentals/`                   | Structuring system / persistent / working / user slots |

---

## Session Management

When context budget pressure arises in any long-running session:

1. Apply Sacred Context principles (keep critical invariants in the system slot)
2. Run `ContextCompressor` to reduce session length
3. Follow the three-tier Context Handoff Protocol (Full / Scoped / Minimal) for agent transitions

Reference: `patterns/multi-agent-handoff.md`

---

## Rules

- Do not create ad-hoc context structures. Use the four-slot assembly pattern.
- Memory types (episodic, semantic, procedural, working) have distinct roles — do not conflate them.
- Run tests from `core-component-00/` or the module folder, not the workspace root.
- This module has an active test suite — any implementation change must pass `pytest context-engineering/testing/ -v` before committing.
