# Context Assembly Patterns

## Overview

Context assembly is the process of building the context window from its constituent parts at runtime. These patterns define _how_ to assemble — not what to put in each slot (see [Context Window Anatomy](core-component-00/context-engineering/fundamentals/context-window-anatomy.md)) but how to make the runtime decision of what to include, in what order, and at what volume.

---

## Pattern 1: Task-Aware Assembly

**Problem:** A fixed context template wastes budget — a code generation task needs more retrieved content, while a creative task needs more history.

**Solution:** Classify the task first; derive slot budgets from the classification.

```python
BUDGET_PROFILES = {
    "factual_qa":        {"system": 0.10, "retrieved": 0.65, "history": 0.10, "tools": 0.15},
    "code_generation":   {"system": 0.15, "retrieved": 0.45, "history": 0.20, "tools": 0.20},
    "creative_writing":  {"system": 0.20, "retrieved": 0.20, "history": 0.50, "tools": 0.10},
    "tool_research":     {"system": 0.10, "retrieved": 0.35, "history": 0.15, "tools": 0.40},
    "multi_turn_reason": {"system": 0.15, "retrieved": 0.20, "history": 0.55, "tools": 0.10},
    "orchestration":     {"system": 0.20, "retrieved": 0.30, "history": 0.10, "tools": 0.40},
}

def assemble(task_type: str, system: str, retrieved: list, history: list,
             tools: list, max_tokens: int) -> list:
    profile = BUDGET_PROFILES.get(task_type, BUDGET_PROFILES["multi_turn_reason"])
    budgets = {k: int(v * max_tokens) for k, v in profile.items()}
    return build_context(system, retrieved, history, tools, budgets)
```

**When to use:** Always. Task-aware assembly should be the default, not the exception.

---

## Pattern 2: Priority-Score Assembly

**Problem:** When there is more content available than fits in the budget, naive truncation cuts the wrong things.

**Solution:** Score every candidate content item by relevance, recency, and importance; fill slots greedily by score until budget is exhausted.

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ContextItem:
    content: str
    slot: str           # "system" | "retrieved" | "history" | "tools"
    relevance: float    # 0.0 – 1.0 (semantic similarity to current query)
    recency: float      # 0.0 – 1.0 (1.0 = most recent)
    importance: float   # 0.0 – 1.0 (manual or computed weight)
    sacred: bool = False  # Sacred items are always included regardless of score

    @property
    def score(self) -> float:
        if self.sacred:
            return float("inf")
        return (self.relevance * 0.5) + (self.recency * 0.3) + (self.importance * 0.2)

def priority_fill(items: List[ContextItem], budget_tokens: int,
                  estimate_tokens) -> List[ContextItem]:
    """Fill a slot budget greedily by priority score."""
    sacred = [i for i in items if i.sacred]
    candidates = sorted([i for i in items if not i.sacred],
                        key=lambda x: x.score, reverse=True)
    selected = list(sacred)
    used = sum(estimate_tokens(i.content) for i in sacred)

    for item in candidates:
        cost = estimate_tokens(item.content)
        if used + cost <= budget_tokens:
            selected.append(item)
            used += cost

    return selected
```

**When to use:** Any time retrieved content or history exceeds its slot budget.

---

## Pattern 3: Sacred Context Injection

**Problem:** Decisions and commitments made early in a session get compressed away, causing the model to contradict itself.

**Solution:** Designate certain episodic memory entries as "sacred" — they are re-injected verbatim at the start of the history slot on every turn.

```
[HISTORY SLOT]
═══════════════════════════════════════════
DECISIONS AND COMMITMENTS (SACRED — never compress)
- Decision [Turn 3]: User chose PostgreSQL over MySQL.
- Commitment [Turn 7]: Agent will deliver a complete migration script.
═══════════════════════════════════════════
[Compressed summary of turns 1–15]
[Turn 16 verbatim]
[Turn 17 verbatim]
[Turn 18 verbatim — most recent]
```

**When to use:** Any session where decisions or commitments have been made. This should be automatic — the `ContextAssembler` handles it.

---

## Pattern 4: Progressive Compression

**Problem:** Simple "keep last N turns" pruning discards potentially important older context.

**Solution:** Apply compression in tiers — older content is compressed more aggressively, preserving the information gradient from rich (recent) to sparse (old).

```
Turn 1–5   →  Single paragraph summary
Turn 6–10  →  Three-sentence summary per turn
Turn 11–15 →  One-sentence summary per turn
Turn 16–18 →  Verbatim (last 3 turns always kept full)
```

```python
def progressive_compress(history: list, keep_recent: int = 3) -> list:
    if len(history) <= keep_recent:
        return history

    recent = history[-keep_recent:]
    older = history[:-keep_recent]

    tiers = _split_into_tiers(older, tier_sizes=[5, 5, 5])
    compressed = []
    for i, tier in enumerate(tiers):
        compression_level = ["paragraph", "sentence", "phrase"][min(i, 2)]
        compressed.append(_summarise_tier(tier, level=compression_level))

    return compressed + recent
```

**When to use:** Sessions exceeding 10 turns, or when history budget exceeds 75% of its allocated slot.

---

## Pattern 5: Slot-Order Anchoring

**Problem:** Models have an attention bias toward the beginning and end of the context. Critical content buried in the middle receives less weight.

**Solution:** Place the highest-priority items at the **start** and **end** of each slot. Use the middle for supporting context.

```
[RETRIEVED SLOT — correct order]
--- Most relevant document (HIGH PRIORITY) ← START
--- Supporting document 2
--- Supporting document 3 (medium relevance)
--- Second most relevant document (HIGH PRIORITY) ← END

[RETRIEVED SLOT — anti-pattern]
--- Supporting document 2
--- Most relevant document (buried in middle — WRONG)
--- Supporting document 3
--- Least relevant document
```

**When to use:** Always. Implement as a post-sort step in `ContextAssembler.build()`.

---

## Pattern 6: Layered Retrieval

**Problem:** Semantic retrieval alone misses exact-match facts. Exact-match retrieval alone misses conceptually related content.

**Solution:** Combine both retrieval strategies and merge results before assembly.

```
Query: "How does our authentication middleware work?"

Semantic retrieval  → auth_design.md (conceptually related)
                   → middleware_patterns.md (conceptually related)
Keyword retrieval  → auth_middleware.py (exact match on "authentication middleware")

Merged + deduped + reranked → auth_middleware.py, auth_design.md, middleware_patterns.md
```

**When to use:** Any production RAG integration. Pure semantic retrieval is insufficient for technical queries with specific terminology.

---

## Assembly Anti-Patterns

| Anti-Pattern               | Problem                                                       | Fix                                                        |
| -------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------- |
| **Concatenation assembly** | Content appended in arrival order, not priority order         | Score and sort all items before assembly                   |
| **Slot flooding**          | One slot (e.g. history) consumes the entire budget            | Enforce hard slot budget limits before assembly            |
| **Uniform compression**    | All history turns compressed equally regardless of importance | Use progressive compression with sacred context protection |
| **Late tool injection**    | Tool results appended after history instead of in tool slot   | Always place tool outputs in the tool output slot (last)   |
| **System slot mutation**   | System prompt rebuilt with user input each turn               | Keep system slot static; never include user text in it     |
| **No-retrieval assembly**  | Context assembled from history only, no memory lookup         | Always query episodic + semantic memory before assembly    |

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Multi-Agent Handoff](./multi-agent-handoff.md) · [context_assembler.py](core-component-00/context-engineering/implementations/context_assembler.py) · [Context Window Anatomy](core-component-00/context-engineering/fundamentals/context-window-anatomy.md)
