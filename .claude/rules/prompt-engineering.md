---
paths:
  - "**/prompt-engineering/**"
description: Prompt Engineering (Layer 1) patterns and behavior rules
---

# Prompt Engineering — Layer 1

**Scope:** Foundational research, zero-shot to chain-of-thought prompting, workspace strategy

---

## Prompt Engineering Hierarchy

1. **Zero-Shot** — Direct instruction with no examples
2. **Few-Shot** — Instruction + examples
3. **Chain-of-Thought (CoT)** — Step-by-step reasoning
4. **Advanced Patterns** — Socratic, Devil's Advocate, Schema-Constrained

---

## Key Documents

| Document                       | Purpose                                           |
| ------------------------------ | ------------------------------------------------- |
| `fundamentals/research.md`     | Foundational prompt engineering research          |
| `patterns/zero-shot.md`        | Direct instruction patterns                       |
| `patterns/few-shot.md`         | Example-based instruction patterns                |
| `patterns/chain-of-thought.md` | Step-by-step reasoning patterns                   |
| `patterns/advanced.md`         | Socratic, Devil's Advocate, Schema-Constrained    |
| `workspace/strategy.md`        | How to integrate prompts into workspace artifacts |

---

## Integration with Context Engineering

Prompt patterns fill the **System slot** of the context window:

```
Context Window
├── System ← Prompt Engineering patterns go here
├── Retrieved ← RAG content
├── History ← Conversation memory
└── Tool Outputs ← Function call results
```

---

## Behavior Rules

1. Use established patterns from `patterns/` before inventing new structures
2. Follow workspace strategy — integrate into profiles, skills, rules, and hooks
3. No ad-hoc prompts in production — all must follow documented patterns (ASE requirement)
4. Test prompt stability across model versions
5. Document prompt rationale
