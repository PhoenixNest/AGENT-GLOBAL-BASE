---
name: llm-system-design
description: Full-stack LLM system architecture using the CC-00 five-module stack. Given a problem description or set of requirements, produces a complete architectural specification covering all five layers — Prompt, Context, Harness, RAG, and Multi-Agent. Use whenever a new LLM-powered system or agent pipeline needs to be designed from scratch.
version: "1.0.0"
---

# LLM System Design

## Purpose

Given requirements for an LLM-powered system, produce a complete architectural
specification that addresses all five CC-00 layers in a coherent, integrated design. The
goal is to prevent the most common class of LLM system failure: layers designed in
isolation that cannot feed each other at runtime.

A well-designed specification means that the engineering team implementing each layer
already knows what the adjacent layers expect from them — no architectural ambiguity
remains after the document is delivered.

## Why Holistic Design Matters

LLM systems have a layered dependency graph: multi-agent orchestration consumes harness
execution, the harness consumes context assembly, context assembly consumes both prompt
patterns and RAG retrieval. If these layers are designed independently, the seams between
them accumulate mismatch: a context design that produces token budgets the harness
doesn't enforce, a RAG pipeline that retrieves chunks in a format the context assembler
can't slot, a swarm topology that passes more context than the handoff protocol can carry.

Designing top-down across all five layers before any code is written prevents this class
of problem. The specification is the contract between layers.

## Reference Architecture

All five layers are specified in `core-component-00/`. The canonical integration guide
is `core-component-00/context-engineering/workspace/integration-guide.md`. Consult it
alongside this skill before producing the design.

## Design Process

### Step 1 — Requirements Intake

Before designing any layer, establish the following. Clarify any gaps before proceeding
— a design built on unclear requirements produces a specification nobody trusts.

| Requirement Dimension        | Key Question                                                                     |
| ---------------------------- | -------------------------------------------------------------------------------- |
| **System purpose**           | What problem does this LLM system solve? Who uses it?                            |
| **Input / output contract**  | What does the system receive? What must it produce?                              |
| **Session characteristics**  | Single-turn, multi-turn, or long-running agent session? Expected session length? |
| **Agent topology hint**      | Single agent, or does the task decompose naturally into specialist roles?        |
| **Knowledge requirements**   | Needs external retrieval, or is the model's parametric knowledge sufficient?     |
| **Reliability requirements** | What failure modes are unacceptable? Acceptable latency at p99?                  |

### Step 2 — Layer-by-Layer Design

Work through the layers in dependency order — from what the model reads (Prompt) through
what coordinates the agents (Multi-Agent). Each layer's design should be informed by what
the layer above it will demand.

#### Layer 1 — Prompt Engineering

Specify the instruction patterns that will be used in system prompts, task prompts, and
any tool-use prompts.

| Decision                               | Options / Reference                                                                                             |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Prompting technique                    | Zero-shot, few-shot, CoT, Schema-Constrained, Socratic — see `prompt-engineering/patterns/advanced-patterns.md` |
| Role / persona definition              | Define if using an agent profile; specify identity, constraints, and mode                                       |
| System prompt vs. task prompt boundary | System: persistent identity and rules; task: per-request instructions                                           |
| Output format requirements             | If downstream requires structured output, use schema-constrained prompting                                      |

#### Layer 2 — Context Engineering

Specify the context window architecture.

| Decision                                       | Options / Reference                                                                                            |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Memory types needed                            | Episodic / Semantic / Procedural / Working — see `context-engineering/fundamentals/memory-types.md`            |
| Four-slot composition                          | System / Retrieved / History / Tool outputs — see `context-engineering/fundamentals/context-window-anatomy.md` |
| Slot priority order under token pressure       | Default: System > Retrieved > History > Tool outputs. Document any deviation                                   |
| Context preservation across session boundaries | Specify compression strategy and what is marked as sacred                                                      |
| Multi-agent handoff tier                       | Full / Scoped / Minimal per agent transition — see `context-engineering/patterns/multi-agent-handoff.md`       |

#### Layer 3 — Harness Engineering

Specify the execution envelope around each model call.

| Decision                | Options / Reference                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Timeout thresholds      | Set per the system's p99 latency requirement                                                                       |
| Tool call whitelist     | Which tools are permitted via the Tool Registry; specify call limits                                               |
| Retry logic             | Governs rate-limit and transient errors; use exponential backoff                                                   |
| Token budget thresholds | When to trigger graceful degradation vs. hard abort — see `harness-engineering/implementations/context_monitor.py` |

#### Layer 4 — Retrieval-Augmented Generation

Specify the knowledge retrieval pipeline if the system needs external knowledge. If
external knowledge retrieval is not required, document why and note that this layer is
not instantiated.

| Decision                          | Options / Reference                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------ |
| Knowledge source(s)               | What is being indexed and at what refresh cadence                                          |
| Chunking strategy                 | Fixed-size, semantic, or document-boundary — depends on content type                       |
| Embedding model and vector store  | Select based on latency, scale, and cost requirements                                      |
| ACL filtering                     | Required if retrieved chunks carry user-level access controls                              |
| Reranking before context assembly | Specify the reranking step — see `retrieval-augmented-generation/architecture/overview.md` |

#### Layer 5 — Multi-Agent Engineering

Specify the agent topology if the system decomposes into multiple agents. If the system
is single-agent, document why and note that this layer is not instantiated.

| Decision                                | Options / Reference                                                                                                           |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Swarm topology                          | Hierarchical / Flat / Mesh / Pipeline / Hybrid — see `multi-agent-engineering/fundamentals/swarm-topologies.md`               |
| Agent roles and authority boundaries    | Define each agent's responsibility, input, output, and escalation path                                                        |
| Work decomposition and result synthesis | How tasks are divided across agents and how results are merged                                                                |
| Orchestration patterns                  | Pipeline / Fork-Join / Router / Supervisor-Worker / Debate — see `multi-agent-engineering/patterns/orchestration-patterns.md` |

### Step 3 — Integration Validation

Before finalising the specification, validate that the layers form a coherent whole.
Document any decisions that required adjustment.

| Cross-layer check        | Passes when                                                                                         |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| RAG → Context            | Retrieval output format matches what the context assembler expects as input                         |
| Context → Harness        | Context assembler's token budget assumption matches what the harness enforces                       |
| Handoff tier sufficiency | Each handoff tier carries enough context for downstream agents without exceeding their slot budgets |
| Dependency graph         | No circular dependencies between layers                                                             |

### Step 4 — Deliver the Specification

## Output Format

Deliver as a structured Markdown document with one section per layer. Each layer section
covers:

- **Design decision:** What was chosen and why
- **Configuration:** The key parameters and thresholds
- **Integration contract:** What this layer provides to and requires from adjacent layers
- **Reference:** The CC-00 module file that governs this layer's implementation

Use this section header pattern:

```
# LLM System Design — [System Name]

## System Overview
[Purpose, users, input/output contract]

## Layer 1 — Prompt Engineering
[Design decision · Configuration · Integration contract · Reference]

## Layer 2 — Context Engineering
[Design decision · Configuration · Integration contract · Reference]

## Layer 3 — Harness Engineering
[Design decision · Configuration · Integration contract · Reference]

## Layer 4 — Retrieval-Augmented Generation
[Design decision · Configuration · Integration contract · Reference]
OR: [Rationale for not instantiating this layer]

## Layer 5 — Multi-Agent Engineering
[Design decision · Configuration · Integration contract · Reference]
OR: [Rationale for not instantiating this layer]

## Integration Validation Summary
[Cross-layer compatibility notes · Adjustments made]
```

## Quality Signal

| Quality Attribute                | Test / Evidence                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Layer legibility**             | An engineer reading Layer N can immediately identify what Layer N−1 delivers to them and what Layer N+1 expects from them |
| **Decision traceability**        | Every design decision cites a CC-00 reference or provides explicit rationale for deviating from the reference pattern     |
| **No silent absences**           | Layers 4 and 5 are either specified or explicitly justified as not needed — never silently omitted                        |
| **Numerical budget assumptions** | Token budget values are stated as numbers, not vague phrases like "as much as needed"                                     |
