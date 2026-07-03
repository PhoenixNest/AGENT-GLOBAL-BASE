---
name: cc00-session-compression-engineering
description: Long-session compression implementation and information-preservation tuning for context_compressor.py. Owned by Mei-Ling Zhao (Senior Research Engineer, Context Engineering). Trigger: context compression, session compression, summarization, sacred context, information loss.
version: "1.0.0"
---

# Session Compression Engineering

**Skill ID:** session-compression-engineering
**Role:** Senior Research Engineer — Context Engineering
**Seniority:** L3 — Senior

## Overview

Implementation and tuning of long-session compression in
`core-component-00/context-engineering/implementations/context_compressor.py`, applying Sacred
Context principles (decision-critical content preserved losslessly, background context
summarized) as sessions approach the context budget threshold.

## Tools & Frameworks

| Tool                 | Proficiency | Use Case                                                |
| -------------------- | ----------- | ------------------------------------------------------- |
| Python               | Expert      | Compression pipeline implementation                     |
| tiktoken             | Expert      | Pre/post-compression token accounting                   |
| Evaluation harnesses | Advanced    | Information-preservation scoring against gold summaries |

## Module Ownership

- Maintains `context_compressor.py`: classification of content into decision-critical (System/
  Working) vs. compressible (Conversation background), summarization invocation, and
  post-compression budget verification
- Leads execution of the **Context Compression Theory** research programme (open question:
  minimum information-preserving compression of a 100-turn session) under Dr. Vance as PI
- Owns compression regression benchmarks — every change is scored against a fixed corpus of
  long-session transcripts for decision-continuity loss

## Scenarios & Trade-offs

### Scenario 1: Compression Triggered Mid-Decision

- **Approach:** Compression never truncates an in-progress decision chain (open task state, most
  recent 3 tool calls); it compresses only content chronologically prior to the active thread
- **Trade-off:** Delaying compression until a safe boundary risks running over budget briefly
- **Quality Bar:** Zero decision-critical loss in the benchmark corpus; budget overrun capped at a
  documented tolerance

### Scenario 2: Aggressive vs. Conservative Summarization

- **Approach:** Compression ratio is tunable per session-budget-pressure tier (H-CE01 alert
  thresholds); conservative below 500KB, aggressive above
- **Trade-off:** Aggressive summarization risks losing nuance; conservative summarization may not
  free enough budget in time
- **Quality Bar:** Compressed output re-expands to recover ≥ 90% of decision-relevant facts on the
  benchmark corpus

## Quality Standards

- Every compression pass is logged with pre/post token counts and the compression ratio achieved
- No compression pass discards System-slot content
- Benchmark corpus re-run on every change to `context_compressor.py` before merge

## References

- Sacred Context: Preserving Decision Continuity Across Long Agent Sessions (Dr. Vance, research
  note, 2026)
- `core-component-00/context-engineering/implementations/context_compressor.py`
