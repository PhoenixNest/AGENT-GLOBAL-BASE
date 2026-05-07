---
inclusion: fileMatch
fileMatchPattern: "**/prompt-engineering/**"
---

# Prompt Engineering — Layer 1

**Steering File:** Prompt Engineering (CC-00 Layer 1)  
**Inclusion:** Conditional — Activated when working in `prompt-engineering/`  
**Authority:** CC-00 Laboratory — Layer 1: What to write

---

## Module Identity

**Prompt Engineering** is Layer 1 of the CC-00 engineering stack — the discipline of designing effective LLM instructions.

| Field          | Detail                                                                                                |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| **Layer**      | 1 — What to write                                                                                     |
| **Type**       | Knowledge base (no production code)                                                                   |
| **Scope**      | Foundational research, zero-shot to chain-of-thought prompting, advanced patterns, workspace strategy |
| **Output**     | Prompt patterns, instruction templates, workspace-specific guidance                                   |
| **Downstream** | Feeds into `context-engineering/` (System slot of context window)                                     |

---

## Core Concepts

### Prompt Engineering Hierarchy

1. **Zero-Shot Prompting** — Direct instruction with no examples
2. **Few-Shot Prompting** — Instruction + examples
3. **Chain-of-Thought (CoT)** — Step-by-step reasoning
4. **Advanced Patterns** — Socratic, Devil's Advocate, Schema-Constrained

### Workspace Integration

Prompt patterns are integrated into:

- **Agent profiles** (`agent/profile.md`) — Identity and operating mode
- **Skill files** (`skills/*.md`) — Executable specifications
- **Steering files** (`.kiro/steering/*.md`) — Context and instructions
- **Hooks** (`.kiro/hooks/*.json`) — Event-driven prompts

---

## Key Documents

All paths relative to `core-component-00/prompt-engineering/`:

| Document                       | Purpose                                               |
| ------------------------------ | ----------------------------------------------------- |
| `fundamentals/research.md`     | Foundational prompt engineering research and patterns |
| `patterns/zero-shot.md`        | Direct instruction patterns                           |
| `patterns/few-shot.md`         | Example-based instruction patterns                    |
| `patterns/chain-of-thought.md` | Step-by-step reasoning patterns                       |
| `patterns/advanced.md`         | Socratic, Devil's Advocate, Schema-Constrained        |
| `workspace/strategy.md`        | How to integrate prompts into workspace artifacts     |

---

## Agent Behavior Rules for Prompt Engineering

When working with prompts:

1. **Use established patterns** — Reference `patterns/` before inventing new prompt structures
2. **Follow workspace strategy** — Integrate prompts into agent profiles, skills, steering, and hooks per `workspace/strategy.md`
3. **No ad-hoc prompts in production** — All production prompts must follow documented patterns (ASE compliance requirement)
4. **Test prompt stability** — Verify prompts work across different model versions
5. **Document prompt rationale** — Explain why a specific pattern was chosen

---

## Integration with Context Engineering

Prompt patterns fill the **System slot** of the context window:

```
Context Window (Four Slots)
├── System ← Prompt Engineering patterns go here
├── Retrieved ← RAG content
├── History ← Conversation memory
└── Tool Outputs ← Function call results
```

See `core-component-00/context-engineering/fundamentals/context-window-anatomy.md` for full context window structure.

---

**This steering file is automatically activated when working in `prompt-engineering/` directories.**
