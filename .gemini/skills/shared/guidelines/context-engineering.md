# Context Engineering

> **Addresses Gaps:** #1 (Positional Optimization), #8 (MVC Enforcement)

---

## Overview

Context Engineering is the discipline of curating, structuring, and positioning information within an agent's context window to maximize task performance. This guideline applies to **every agent invocation** in the multi-agent pipeline.

---

## Principles

### 1. Positional Optimization — The Primacy-Recency Rule

LLMs exhibit attention bias toward content at the **beginning** and **end** of their context window ("Lost in the Middle" effect).

**Mandatory placement protocol:**

```
┌──────────────────────────────────────────────┐
│  ZONE A — PRIMACY (First 10% of context)     │
│  • Agent identity (role, constraints, rules)  │
│  • Non-negotiable rules (P0/P1 blocking)      │
│  • Current task objective                     │
├──────────────────────────────────────────────┤
│  ZONE B — BODY (Middle 80% of context)        │
│  • Retrieved knowledge (skill guidelines)     │
│  • Previous stage artifacts (summarized)      │
│  • Reference materials, examples              │
├──────────────────────────────────────────────┤
│  ZONE C — RECENCY (Last 10% of context)      │
│  • Specific action requested                  │
│  • Output format / schema requirements        │
│  • Gate criteria for current stage            │
│  • "Do NOT" constraints (anti-patterns)       │
└──────────────────────────────────────────────┘
```

**Key rules:**

- **Never place gate criteria in Zone B.** They must be in Zone A or C.
- **Never place the task objective after reference materials.**
- **Anti-pattern constraints ("do NOT") go in Zone C** for recency bias.

### 2. Minimum Viable Context (MVC)

Every invocation should include the **minimum context required** — no more.

**MVC Checklist — Apply before every agent dispatch:**

| Question                                        | Action if YES                     | Action if NO     |
| :---------------------------------------------- | :-------------------------------- | :--------------- |
| Does the agent need the full PRD?               | Include Stage Transition Summary  | Omit             |
| Does the agent need all previous stage outputs? | Include only prior stage summary  | Omit earlier     |
| Does the agent need the full skill guideline?   | Include relevant sections only    | Omit             |
| Does the agent need other agents' outputs?      | Include structured output schemas | Omit raw outputs |
| Does context exceed 50% of model's window?      | Summarize Zone B content          | Proceed as-is    |

### 3. Hierarchical Summarization — Stage Transitions

When passing artifacts between stages, **never pass raw artifacts**. Create a **Stage Transition Summary** (see `STAGE-TRANSITION-SUMMARY.md` template).

**Rules:**

- Every stage gate **must** produce a Stage Transition Summary as mandatory output.
- The receiving stage loads only the summary, not full upstream artifacts.
- If more detail is needed, retrieve the full artifact on demand.

### 4. Schema-Driven Communication

Agents passing structured data must use **defined output schemas** to prevent ambiguity. Schema definitions live alongside stage templates in `.gemini/pipeline/*/templates/`.

---

## Anti-Patterns

| Anti-Pattern                | Description                                     | Remedy                          |
| :-------------------------- | :---------------------------------------------- | :------------------------------ |
| **Context dumping**         | Passing entire knowledge base to every agent    | Apply MVC checklist             |
| **Flat context**            | No positional structure; critical info buried   | Apply Zone A/B/C protocol       |
| **Raw artifact forwarding** | Full PRD/SRD/UML between stages without summary | Create Stage Transition Summary |
| **Implicit schemas**        | Agents assume output format without definition  | Define JSON schemas             |
| **Identity-last ordering**  | Agent constraints placed after task content     | Identity always in Zone A       |
| **Stale context**           | Including superseded ADRs or outdated artifacts | Reference only current versions |

---

## When to Use This Guideline

- **Always** — when assembling context for any agent invocation
- **Especially** at stage transitions (Stages 1→2, 2→3, ..., 9→10)
- **Especially** when multiple agents collaborate within a stage (Stage 6 panel)
- **Especially** when context window usage exceeds 30% of capacity

---

## References

- ASE Framework: § Layer 2 — Context Engineering
- CEO Report: § Part II, Layer 2 Mapping
- `AGENTS.md` § Non-Negotiable Rules — Zone A content
- `.gemini/pipeline/*/pipeline.md` — Stage definitions for transitions
