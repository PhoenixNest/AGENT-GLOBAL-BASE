# core-component-00/agent-systems-governance-framework/ — ASGF Governing Framework

The Agent Systems Governance Framework (ASGF) meta-module. This is the **mandatory governing layer** above all
five CC-00 engineering modules. Read this before any compliance, maturity, or integration work.

---

## What ASGF Is

ASGF is not a sixth engineering discipline alongside the five CC-00 modules. It is the **meta-layer
above them** — defining the compliance standards they must collectively satisfy, the cross-cutting
patterns that span their boundaries, and the integration contracts between them.

ASGF is ratified via **ADR-ASGF-001** and is mandatory across all company and studio pipelines. No
agent may bypass it. All new LLM-powered systems must be grounded in CC-00 patterns and satisfy
ASGF compliance before production.

---

## Directory Structure

```
agent-systems-governance-framework/
├── governance/
│   ├── adr-asgf-001.md             ← Ratifying ADR — binding authority
│   ├── compliance-standard.md     ← Per-layer requirements for production
│   └── maturity-model.md          ← Levels 0–5 maturity model
├── integration/
│   └── four-layer-composition.md  ← Runtime integration contracts (all five layers)
├── patterns/                      ← Cross-cutting ASGF patterns
└── CONCEPTS.md                    ← Theoretical synthesis of all five disciplines
```

---

## Governing Documents

| Document                                | Purpose                                                     | Read When                                  |
| --------------------------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| `governance/adr-asgf-001.md`            | Binding authority and rationale for ASGF                    | Starting any LLM system work               |
| `governance/compliance-standard.md`     | Per-layer requirements every system must satisfy            | Pre-production compliance check            |
| `governance/maturity-model.md`          | Levels 0–5 for assessing and evolving agent systems         | Maturity assessment / improvement planning |
| `integration/four-layer-composition.md` | Runtime integration contracts between all five CC-00 layers | Designing multi-layer systems              |
| `CONCEPTS.md`                           | Synthesis of how all five modules converge                  | Architecture / research orientation        |

---

## ASGF Layer Map

| Layer | Name                | CC-00 Module                           | Requirement Class                    |
| ----- | ------------------- | -------------------------------------- | ------------------------------------ |
| 1     | Prompt Engineering  | `engineering/prompt-engineering/`      | Standardised instruction patterns    |
| 2     | Context Engineering | `engineering/context-engineering/`     | Structured handoffs, context windows |
| 3     | Harness Engineering | `engineering/harness-engineering/`     | Automated gate enforcement           |
| 4     | RAG / Memory        | `retrieval-augmented-generation/`      | Institutional knowledge retention    |
| 5     | Multi-Agent         | `engineering/multi-agent-engineering/` | Swarm orchestration and isolation    |

---

## Pipeline Parity Status

All four company development pipelines (Mobile, Web, Backend API, Full-Stack) have achieved 100%
ASGF template parity. Monitoring templates live at:

```
company/pipeline/<type>/templates/monitoring/
```

---

## MCP Server

A live `cc00-tools` MCP server provides ASGF tooling:

| Tool                      | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `analyze_handoff`         | Analyse a context handoff packet           |
| `assess_maturity`         | Evaluate system maturity against the model |
| `check_context_budget`    | Verify token budget compliance             |
| `validate_ase_compliance` | Run full ASGF compliance validation        |

---

## Rules

- ASGF compliance is **mandatory** — it cannot be waived by any agent (only the User can override).
- New agent systems, RAG pipelines, harness implementations, and context solutions must be grounded
  in CC-00 patterns. Do not invent ad-hoc alternatives.
- Read `governance/adr-asgf-001.md` before making architectural decisions on any LLM-powered system.
- The maturity model (`governance/maturity-model.md`) is the framework for all maturity assessments.
  Do not invent alternative maturity criteria.
