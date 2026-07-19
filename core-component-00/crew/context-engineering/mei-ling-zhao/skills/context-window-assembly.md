---
name: cc00-context-window-assembly
description: Four-slot context window assembly implementation and tuning for context_assembler.py. Owned by Mei-Ling Zhao (Senior Research Engineer, Context Engineering). Trigger: context window assembly, slot priority, context assembler, four-slot model.
version: "1.0.0"
---

# Context Window Assembly

**Skill ID:** context-window-assembly
**Role:** Senior Research Engineer — Context Engineering
**Seniority:** L3 — Senior

## Overview

Production implementation and tuning of the four-slot context window assembly pattern defined in
`core-component-00/engineering/context-engineering/implementations/context_assembler.py`: System, Working,
Retrieved, and Conversation slots, assembled under a token budget with deterministic priority
ordering.

## Tools & Frameworks

| Tool               | Proficiency | Use Case                                                      |
| ------------------ | ----------- | ------------------------------------------------------------- |
| Python (tiktoken)  | Expert      | Token counting and budget enforcement                         |
| pytest             | Expert      | Assembly regression + slot-priority tests                     |
| CC-00 test harness | Advanced    | Module-scoped test execution (`context-engineering/testing/`) |

## Module Ownership

- Maintains `context_assembler.py`: slot-priority assembly, truncation order, and budget overflow
  handling
- Owns the module's `pytest` coverage for slot assembly, including adversarial cases (over-budget
  System slot, empty Retrieved slot, Conversation slot truncation mid-turn)
- Signs off on any change to slot priority ordering before merge; escalates cross-module priority
  conflicts (e.g., harness budget signals vs. assembler truncation) to Dr. Vance

## Scenarios & Trade-offs

### Scenario 1: System Slot Exceeds Budget

- **Approach:** System slot (identity, rules) is never truncated; overflow is rejected upstream
  with an explicit error rather than silently dropping instructions
- **Trade-off:** Hard failure vs. silent degradation — hard failure surfaces config errors early
- **Quality Bar:** Zero silent instruction loss; overflow raises a typed exception with the
  offending slot named

### Scenario 2: Retrieved Slot Competing with Conversation History

- **Approach:** Retrieved content is capped at a configurable percentage of remaining budget after
  System + Working are assembled; Conversation history is truncated oldest-first within its
  remaining allocation
- **Trade-off:** Retrieval freshness vs. conversational continuity — over-favoring retrieval starves
  multi-turn coherence
- **Quality Bar:** No single slot exceeds its configured cap; truncation order is logged for audit

## Quality Standards

- 100% branch coverage on truncation and overflow paths in `context_assembler.py`
- All assembly decisions are deterministic and reproducible given identical inputs
- Token accounting matches the target model's tokenizer within 1% error margin

## References

- CC-00 Six Pillars of Context Engineering (Dr. Vance, internal framework, 2025)
- `core-component-00/engineering/context-engineering/implementations/context_assembler.py`
