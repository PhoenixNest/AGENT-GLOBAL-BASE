---
name: core-component-00-director-ase-compliance-audit
description: Audit an existing LLM-powered agent system against the Agent Systems Engineering (ASE) four-layer framework. Identifies gaps across Prompt, Context, Harness, and RAG/Memory layers, classifies their severity, and produces a prioritised remediation plan. Use when an existing system needs to be assessed before production, after an incident, or when onboarding an externally-built LLM system into this organisation.
version: "1.0.0"
source: core-component-00/crew/director/elias-vance/skills/ase-compliance-audit.md
agents:
  - core-component-00-director-elias-vance
---

# ASE Compliance Audit

## Purpose

Given a description of an existing LLM-powered agent system, produce a structured
compliance assessment against the Agent Systems Engineering (ASE) four-layer framework.
The audit identifies which layers are absent, under-engineered, or incorrectly implemented
— and produces a remediation plan ordered by impact.

The ASE framework is ratified via ADR-ASE-001 and is mandatory across all company and
studio pipelines. This skill is the enforcement mechanism for that mandate.

**Governing documents:**

- ADR: `core-component-00/agent-systems-engineering/governance/adr-ase-001.md`
- Standard: `core-component-00/agent-systems-engineering/governance/compliance-standard.md`
- Maturity: `core-component-00/agent-systems-engineering/governance/maturity-model.md`

The **Compliance Standard** is the authoritative specification for pass/fail criteria.
When in doubt about a requirement, the standard takes precedence over this skill.

## Why ASE Compliance Matters

An LLM system that passes functional testing can still fail in production due to
architectural gaps that only manifest under load, across long sessions, or at security
boundaries.

| Missing Layer                 | Production Failure Mode                                                           |
| ----------------------------- | --------------------------------------------------------------------------------- |
| Harness engineering           | Fails silently when rate limits or timeouts hit                                   |
| Context engineering           | Degrades over long sessions as the context window fills with low-priority content |
| RAG / Memory                  | Produces hallucinations when parametric knowledge is insufficient or stale        |
| Structured prompt engineering | Produces inconsistent outputs that break downstream consumers                     |

An ASE audit surfaces these gaps before they become incidents.

## Audit Scope

The ASE framework covers four layers. Each layer is audited independently, then the
inter-layer integration is assessed:

| Layer | Name                | What It Covers                                                  |
| ----- | ------------------- | --------------------------------------------------------------- |
| 1     | Prompt Engineering  | Instruction quality, role definition, output format constraints |
| 2     | Context Engineering | Context window design, memory management, handoff protocols     |
| 3     | Harness Engineering | Error boundaries, token budget enforcement, tool use controls   |
| 4     | RAG / Memory        | Knowledge retrieval, chunking, embedding, access control        |

## Evidence Intake

Before auditing, collect available evidence about the system. The more complete the
evidence, the more actionable the audit findings.

| Evidence Type             | Examples                                                           |
| ------------------------- | ------------------------------------------------------------------ |
| System prompts            | The literal text of system prompts used in production              |
| Context assembly logic    | Code or description of how the context window is built at runtime  |
| Model call wrappers       | Code surrounding API calls — error handling, retry logic, timeouts |
| Retrieval pipeline        | Chunking strategy, embedding model, vector store, retrieval code   |
| Incident history          | Past failures, hallucinations, timeouts, or context-related bugs   |
| Session logs (anonymised) | Representative samples of production sessions                      |

When evidence is incomplete, note the gap and audit based on what is available — a
partial audit with documented evidence gaps is more useful than a deferred audit.

## Audit Process

### Layer 1 — Prompt Engineering Audit

Assess the quality and structure of the system's instruction layer:

- Is there a defined role or persona for the agent? Is it specific enough to constrain
  behaviour, or is it vague?
- Are task instructions separated from identity/role definitions (system prompt) and
  specific task prompts (user/task prompt)?
- Is the output format specified? If the downstream system depends on structured output,
  is schema-constrained prompting used?
- Are there few-shot examples where they would materially improve output consistency?
- Do the prompts reflect the techniques documented in
  `core-component-00/prompt-engineering/patterns/advanced-patterns.md`, or are they
  ad-hoc?

**Checklist:**

| Check                             | Pass / Fail / Partial | Evidence | Gap Description |
| --------------------------------- | --------------------- | -------- | --------------- |
| Role/persona defined              |                       |          |                 |
| System vs. task prompt separation |                       |          |                 |
| Output format constrained         |                       |          |                 |
| Prompting technique appropriate   |                       |          |                 |
| Few-shot examples where warranted |                       |          |                 |

### Layer 2 — Context Engineering Audit

Assess how the context window is designed and managed:

- Are the four context slots (System / Retrieved / History / Tool outputs) explicitly
  structured, or is context assembled ad-hoc?
- Is there a defined slot priority order for when the token budget is under pressure?
- For multi-turn sessions: is history managed with a rolling window and compression
  strategy, or does the full history accumulate until the context overflows?
- Is sacred context identified and protected from compression?
- For multi-agent systems: is a context handoff protocol specified for each agent
  transition?

**Checklist:**

| Check                            | Pass / Fail / Partial | Evidence | Gap Description |
| -------------------------------- | --------------------- | -------- | --------------- |
| Four-slot structure implemented  |                       |          |                 |
| Slot priority order defined      |                       |          |                 |
| History managed with compression |                       |          |                 |
| Sacred context defined           |                       |          |                 |
| Handoff protocol specified       |                       |          |                 |

### Layer 3 — Harness Engineering Audit

Assess the execution envelope around model calls:

- Are timeout thresholds defined and enforced at the model call level?
- Is rate-limit handling implemented with retry logic and exponential backoff?
- Is there a token budget monitor that enforces limits before context overflows the window?
- Is there a tool registry that whitelists permitted tool calls and enforces call limits?
- Is there an error boundary that recovers gracefully from transient failures rather than
  propagating raw exceptions to users?

Reference: `core-component-00/harness-engineering/implementations/`

**Checklist:**

| Check                              | Pass / Fail / Partial | Evidence | Gap Description |
| ---------------------------------- | --------------------- | -------- | --------------- |
| Timeout enforcement implemented    |                       |          |                 |
| Rate-limit retry logic present     |                       |          |                 |
| Token budget monitor active        |                       |          |                 |
| Tool registry / whitelist defined  |                       |          |                 |
| Error boundary with recovery logic |                       |          |                 |

### Layer 4 — RAG / Memory Audit

Assess the knowledge retrieval and memory system (if applicable):

- If external knowledge is required: is a retrieval pipeline implemented, or is the
  system relying on parametric knowledge for facts that should be retrieved?
- Is the chunking strategy appropriate for the content type?
- Is there a reranking step to surface the most relevant chunks before context assembly?
- Are ACL controls applied to prevent unauthorised content reaching the context window?
- Are retrieval freshness characteristics understood and documented?

If the system has no retrieval requirement, document why and mark this layer as
intentionally absent.

Reference: `core-component-00/retrieval-augmented-generation/architecture/overview.md`

**Checklist:**

| Check                           | Pass / Fail / Partial | Evidence | Gap Description |
| ------------------------------- | --------------------- | -------- | --------------- |
| Retrieval pipeline implemented  |                       |          |                 |
| Chunking strategy defined       |                       |          |                 |
| Reranking step present          |                       |          |                 |
| ACL filtering applied           |                       |          |                 |
| Freshness characteristics known |                       |          |                 |

### Cross-Layer Integration Assessment

After auditing each layer independently, assess the integration:

| Integration Check             | Passes When                                                                               |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| RAG → Context                 | Retrieval output format matches what the context assembler expects                        |
| Context → Harness             | Context assembler's token budget assumption matches what the harness enforces             |
| Prompt → Context / Tools      | Prompt patterns produce outputs the downstream context assembly or tool calls can consume |
| Handoff packets (multi-agent) | Handoff packet content matches what downstream agents declare as their required input     |

## Gap Severity Classification

Classify each identified gap by severity:

| Severity | Definition                                                                              |
| -------- | --------------------------------------------------------------------------------------- |
| **P0**   | Gap that will cause production failure under normal load or after extended sessions     |
| **P1**   | Gap that will degrade output quality or reliability at scale but does not cause outages |
| **P2**   | Gap that reduces engineering maintainability or makes the system harder to extend       |
| **P3**   | Improvement opportunity with no current reliability impact                              |

P0 and P1 gaps must be remediated before the system is considered ASE-compliant.

## Output Format

Deliver as a structured Markdown document:

```
# ASE Compliance Audit — [System Name]

## Audit Summary
[System description · Evidence available · Overall compliance status]

## Layer 1 — Prompt Engineering
[Checklist results · Gap descriptions · Severity classifications]

## Layer 2 — Context Engineering
[Checklist results · Gap descriptions · Severity classifications]

## Layer 3 — Harness Engineering
[Checklist results · Gap descriptions · Severity classifications]

## Layer 4 — RAG / Memory
[Checklist results · Gap descriptions · Severity classifications]
OR: [Rationale for intentional absence]

## Cross-Layer Integration
[Integration compatibility findings · Any cross-layer mismatches]

## Remediation Plan
[Gaps ordered by severity · Recommended CC-00 implementation references for each gap]

## Compliance Verdict
[ASE-Compliant / Non-Compliant (P0 gaps present) / Conditional (P1 gaps only)]
```

## Quality Signal

A complete ASE audit leaves no ambiguity about what must be fixed and in what order:

- Every checklist item has a Pass / Fail / Partial verdict with evidence cited.
- Every gap has a severity classification and a reference to the CC-00 pattern or
  implementation that closes it.
- The remediation plan is ordered by severity, not by layer — a P0 in Layer 4 is fixed
  before a P2 in Layer 1.
- The compliance verdict is binary at the P0/P1 boundary: a system with any P0 gap is
  not compliant, regardless of how well it scores on other layers.
