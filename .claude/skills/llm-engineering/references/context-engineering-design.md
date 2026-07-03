---
name: core-component-00-director-context-engineering-design
description: Design the context window architecture for an LLM agent or pipeline — slot composition, memory type selection, assembly patterns, token budget strategy, and multi-agent handoff protocol specification. Use when an agent or pipeline needs a rigorous context design rather than an ad-hoc approach, especially for long-running sessions, multi-turn agents, or multi-agent handoffs.
version: "1.0.0"
source: core-component-00/crew/director/elias-vance/skills/context-engineering-design.md
agents:
  - core-component-00-director-elias-vance
---

# Context Engineering Design

## Purpose

Produce a complete context window architecture for a given LLM agent or pipeline. Where
`llm-system-design.md` covers all five CC-00 layers at system level, this skill goes
deeper into Layer 2 alone — appropriate when context design is the primary problem (the
other layers are already specified or not in question).

The deliverable is a context architecture document that answers every question the
implementation team will have before they write a single line of context assembly code.

## Why Context Engineering Is a Distinct Discipline

Most LLM systems that fail in production do not fail because the model is wrong — they
fail because the context window is wrong. The model generates responses based entirely on
what it sees; if the context is incoherent, over-full, under-specified, or assembled
incorrectly, the model's output reflects those flaws regardless of how capable the
underlying model is. Context engineering is the discipline of making the model see exactly
what it needs to see, in the right structure, at the right time.

The foundational reference for this discipline is:
`core-component-00/context-engineering/`

## Reference Materials

Read the following before producing a context design:

| Document                                                                       | Purpose                                          |
| ------------------------------------------------------------------------------ | ------------------------------------------------ |
| `core-component-00/context-engineering/fundamentals/context-window-anatomy.md` | The four typed slots and their composition rules |
| `core-component-00/context-engineering/fundamentals/memory-types.md`           | Episodic, semantic, procedural, working memory   |
| `core-component-00/context-engineering/patterns/assembly-patterns.md`          | Dynamic assembly strategies                      |
| `core-component-00/context-engineering/patterns/multi-agent-handoff.md`        | Full / Scoped / Minimal handoff protocol tiers   |
| `core-component-00/context-engineering/implementations/context_assembler.py`   | Reference implementation of the assembler        |
| `core-component-00/context-engineering/implementations/context_compressor.py`  | Sacred context compression for long sessions     |

## Design Process

### Step 1 — Session Profile

Before designing the context window, establish the session characteristics that drive
every subsequent decision. These answers determine which memory types are needed, which
slot priorities apply, and whether compression and handoff protocols are required.

| Profile Dimension        | Key Question                                                                                       | Design Implication                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Session length**       | Single-turn, bounded multi-turn (< 20 exchanges), or long-running (20+ / hours)?                   | Determines whether compression and episodic memory are needed         |
| **Task structure**       | Single coherent problem, or sub-tasks generating intermediate outputs?                             | Determines whether working memory state must be threaded across steps |
| **Knowledge dependency** | How much must the agent remember from earlier in the session vs. retrieve from external knowledge? | Drives the balance between episodic and semantic memory               |
| **Handoff requirement**  | Will this agent's context be passed to another agent? How much of it?                              | Determines whether a handoff protocol must be designed                |
| **Token budget**         | What is the model's context window size? What headroom for tool outputs and generation?            | Sets hard limits on every slot size in the design                     |

### Step 2 — Memory Type Selection

Select the memory types the agent needs based on the session profile. Each type serves a
different function:

| Memory Type    | What It Holds                                       | When Needed                                                  |
| -------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| **Episodic**   | Specific past events, decisions, and their outcomes | Multi-turn sessions; when prior decisions affect future ones |
| **Semantic**   | General facts, domain knowledge, retrieved content  | When the agent needs background knowledge or retrieved docs  |
| **Procedural** | How-to knowledge: workflows, patterns, rules        | When the agent must follow defined processes consistently    |
| **Working**    | Current task state: active context, scratchpad      | Always — this is the active context slot                     |

Document which types are instantiated and why the excluded types are not needed. An agent
that accumulates all memory types when only working memory is required wastes token budget
and introduces noise.

### Step 3 — Slot Composition

Design the four context slots for this agent:

**System slot (highest priority — never evicted):**
What constitutes the permanent instruction layer for this agent? Include: role definition,
operating mode, constraints, output format requirements. Keep this slot as small as
possible — every token here competes with retrieved content and history.

**Retrieved slot (second priority):**
What knowledge sources feed this slot? Specify: retrieval trigger (when to retrieve),
chunk size and format, slot size limit in tokens, and priority ordering when multiple
sources compete for the same slot budget.

**History slot (third priority):**
How is conversation history managed? Specify: rolling window size, summarisation trigger
(at what turn count or token threshold do earlier turns get compressed?), and what
information from history is sacred (must survive compression).

**Tool outputs slot (lowest priority — most volatile):**
What tool call outputs does this agent generate? Specify: which outputs must be preserved
in context and for how long, and which can be discarded after acknowledgement.

### Step 4 — Priority and Eviction Policy

When the token budget is under pressure, what gets evicted first? Specify the slot
eviction order and the thresholds that trigger eviction. The reference implementation
handles this in `context_assembler.py` — the design must be expressed in terms it can
enforce.

The canonical priority order is: System > Retrieved > History > Tool outputs. Document
any deviation from this order and the reasoning behind it.

### Step 5 — Long-Session Strategy (if applicable)

For sessions expected to exceed the model's context window, specify:

| Parameter                    | Specification                                                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Compression trigger**      | At what token threshold does compression engage?                                                                   |
| **Sacred context**           | What is exempt from compression? (Decisions made, user preferences, confirmed constraints — must survive verbatim) |
| **Compression target**       | How many tokens should the compressed history occupy after compression?                                            |
| **Reference implementation** | `context-engineering/implementations/context_compressor.py`                                                        |

### Step 6 — Handoff Protocol (if applicable)

If this agent's context will be passed to another agent, specify the tier and packet
contents explicitly. Reference: `context-engineering/patterns/multi-agent-handoff.md`

| Tier        | When to Use                                                                                                           | What Is Included                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Full**    | Downstream agent must replicate the full decision history (e.g., orchestrator → specialist with complex dependencies) | Complete context: all memory types forwarded                         |
| **Scoped**  | Downstream agent needs task context but not episodic history                                                          | Selected memory types only: working + procedural + relevant semantic |
| **Minimal** | Independent specialist with no dependency on upstream reasoning                                                       | Task specification and constraints only                              |

## Output Format

Deliver as a Markdown document with this structure:

```
# Context Engineering Design — [Agent / System Name]

## Session Profile
[Session length · Task structure · Knowledge dependency · Handoff requirement · Token budget]

## Memory Architecture
[Which types are instantiated · Rationale for excluded types]

## Slot Composition
### System Slot
### Retrieved Slot
### History Slot
### Tool Outputs Slot

## Priority and Eviction Policy
[Eviction order · Thresholds · Any deviations from canonical order]

## Long-Session Strategy
[Compression threshold · Sacred context definition · Compression target]
OR: [Rationale for not needing compression]

## Handoff Protocol
[Tier selection · Packet composition · Downstream agent requirements]
OR: [Rationale for not needing a handoff protocol]

## Implementation Notes
[Any constraints or decisions the implementing engineer must know before touching
context_assembler.py]
```

## Quality Signal

A well-formed context engineering design leaves no ambiguity for the implementer:

- Every slot has a stated token budget, not a vague "as much as needed."
- Sacred context is defined explicitly, not inferred.
- Every memory type is either used or explicitly excluded with a reason.
- Handoff tier selection is justified by the downstream agent's actual dependency on
  upstream context — not defaulted to Full because it seems safe.
