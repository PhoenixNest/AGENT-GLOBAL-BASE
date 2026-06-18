# core-component-00/prompt-engineering/ — Layer 1: Prompt Engineering

CC-00 Layer 1 — "What to write." This module is a pure knowledge base covering the theory and
practice of writing effective prompts for LLM-powered systems.

---

## What Lives Here

This module contains **documentation only** — no Python implementations and no pytest test suite.
It is the knowledge layer that informs how prompts are structured across all other CC-00 modules.

---

## Directory Structure

```
prompt-engineering/
├── fundamentals/      ← Core concepts: instruction types, few-shot, chain-of-thought
├── patterns/          ← Reusable prompt patterns and templates
└── references/        ← Research references and external resources
```

---

## What This Module Covers

| Topic              | What It Addresses                                            |
| ------------------ | ------------------------------------------------------------ |
| Instruction design | How to write clear, unambiguous system and user instructions |
| Few-shot prompting | When and how to use examples to guide model behaviour        |
| Chain-of-thought   | Reasoning elicitation patterns for complex tasks             |
| Role prompting     | How to define agent personas and authority scopes            |
| Output formatting  | Controlling structure, length, and format in model responses |
| Prompt robustness  | Handling adversarial inputs and edge cases                   |

---

## How to Use This Module

1. Read `fundamentals/` documents to understand the theoretical foundation
2. Browse `patterns/` for reusable prompt templates applicable to your task
3. Apply these patterns when writing prompts in any CC-00 module or system

---

## Relationship to Other Modules

Prompt Engineering is the foundation layer. Its patterns are applied inside:

- **Context Engineering (Layer 2):** System slot content, instruction templates
- **Harness Engineering (Layer 3):** Safety instruction patterns, constraint prompts
- **RAG (Layer 4):** Retrieval query prompts, grounding instructions
- **Multi-Agent Engineering (Layer 5):** Agent role prompts, orchestrator instructions

---

## Rules

- There is **no runnable code** in this module. Do not create Python implementations here — they
  belong in the appropriate Layer 2–5 module.
- There is **no pytest test suite** in this module. Testing prompt patterns happens through
  integration testing in Layers 2–5.
- Prompt patterns defined here are guidance, not hard constraints — they must be adapted to
  the specific model, task, and context window at hand.
- New prompt patterns added here must align with ASE compliance standards in
  `agent-systems-engineering/governance/compliance-standard.md`.
