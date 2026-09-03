# CC-00 Enterprise Benchmark Archive

**Classification:** External Benchmark Log
**Owner:** Core Component 00 Laboratory
**Director:** Dr. Elias Vance
**Purpose:** Record of assessments comparing CC-00 modules — or the workspace's LLM engineering
design as a whole — against current external, enterprise-grade / industry-standard practice

---

## Overview

This folder holds enterprise-level benchmark assessments: is a CC-00 module's design and
implementation at, above, or below what production systems elsewhere are currently doing. Created
at CEO direction, 2026-08-16, as a dedicated home for this comparative work — separate from
`core-component-00/telescope/` (internal research investigations) and internal ASGF compliance
audits (`crew/director/elias-vance/skills/asgf-compliance-audit.md`), which check against our own
standard rather than the outside world.

Every assessment here required a **live external research pass in the same session it was
written** — see `template/enterprise-assessment.md`'s Research Freshness section. A knowledge-cutoff
disclosure alone does not satisfy that requirement.

---

## Directory Structure

```
core-component-00/platform/benchmarks/
├── README.md                          ← This file
├── CLAUDE.md                          ← Claude Code operating layer for this folder
├── template/
│   └── enterprise-assessment.md       ← Copy for every new assessment
├── engineering/                       ← Type-scoped legacy taxonomy label (see CLAUDE.md)
│   ├── prompt-engineering/            ← Layer 1
│   ├── context-engineering/           ← Layer 2
│   ├── harness-engineering/           ← Layer 3
│   └── multi-agent-engineering/       ← Layer 5
└── retrieval-augmented-generation/    ← Layer 4 — parallel to engineering/, not inside it
```

---

## Scope expansion to `platform/` (2026-08-31)

Following the `core-component-00/` reorganization that created `framework/` (the five modules +
ASGF) and `platform/` (MCP servers, maintenance records, benchmarks, remediation), the CEO
directed that this archive's scope expand beyond the five `framework/` modules to also cover the
`platform/` domain itself — the MCP server implementations
(`platform/model-context-protocol-servers/`) and maintenance operations
(`platform/maintenance-records/`) now sit within the same enterprise-benchmark remit as the five
engineering modules always did. Ownership for platform-domain assessments: **Dr. Tomasz Wieczorek**
(Safety & Evaluation Engineer — assessment methodology, consistent with his existing Reviewer role
across all benchmark work) paired with **Ravi Deshmukh** (Infrastructure Engineer — platform-domain
subject expertise, per his existing ownership of `platform/maintenance-records/`). This pairing was
Dr. Vance's proposed default, adopted because the CEO did not name an alternative; it should be
revisited if either owner's actual workload proves it wrong.

Full authoring rules, including the layer-sequence convention for running assessments as a set:
`CLAUDE.md` (this folder).

---

## Assessment Index

Add a row here for each new assessment, newest first. Listed by **layer sequence** (1 → 2 → 3 →
4 → 5), not by date, so the table itself reads as the stack in order — a fresh row for a later
pass on an already-assessed module goes in the same layer group as its predecessor.

| Layer    | Date       | Assessment                                                                                                                                                      | Module(s)                                                                              | Verdict                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | 2026-08-16 | `core-component-00/platform/benchmarks/engineering/prompt-engineering/2026-08-16-prompt-engineering-enterprise-assessment/enterprise-assessment.md`             | Prompt Engineering (Layer 1)                                                           | v1.0 rewrite — Conditional, no P0 (5 P1s: eval-harness mock client, CoT-citation misattribution, structured-output gap, prompt-injection guidance gap, conditional-CoT routing incomplete); Reviewer: Dr. Wieczorek (independent) — signed off                                                                                                                                                                                                                                                                                                                                                                                                       |
| 2        | 2026-08-16 | `core-component-00/platform/benchmarks/engineering/context-engineering/2026-08-16-context-engineering-enterprise-assessment/enterprise-assessment.md`           | Context Engineering (Layer 2)                                                          | v1.0 rewrite — Conditional, no P0 (3 P1s, all in "when to compress" — no utilization trigger, no enforcement path past the advisory hook, no asserted compression metric); Reviewer: Dr. Vance — signed off                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 3        | 2026-08-16 | `core-component-00/platform/benchmarks/engineering/harness-engineering/2026-08-16-harness-engineering-enterprise-assessment/enterprise-assessment.md`           | Harness Engineering (Layer 3)                                                          | v1.0 rewrite — **Below Standard, 2 P0s** (both reproduced live: dangerous-task regex is empty on win32 so every task is refused; error boundary has no provider-SDK exception mapping so a real 429 falls through to `UNKNOWN_ERROR`); Reviewer: Dr. Vance — signed off                                                                                                                                                                                                                                                                                                                                                                              |
| 3        | 2026-08-25 | `core-component-00/platform/benchmarks/engineering/harness-engineering/2026-08-25-harness-engineering-enterprise-assessment/enterprise-assessment.md`           | Harness Engineering (Layer 3) — refresh                                                | Post-remediation re-benchmark — both P0s from 2026-08-16 confirmed fixed (provider-error classification, win32 dangerous-task gate) plus the P1 circuit-breaker state-sharing fix; **Conditional, 1 new P1** (client-side rate limiter is request-count-based, not token-aware); 4 unchanged P2s carried from the Remediation Backlog, 1 new P2 (H-CE01's compaction trigger uses byte-size, not token count); Reviewer: Dr. Wieczorek (independent) — signed off                                                                                                                                                                                    |
| 4        | 2026-08-16 | `core-component-00/platform/benchmarks/retrieval-augmented-generation/2026-08-16-retrieval-augmented-generation-enterprise-assessment/enterprise-assessment.md` | Retrieval-Augmented Generation (Layer 4)                                               | v1.0 rewrite — Conditional, no P0 (2 P1s: ACL enforced post-fetch not at query time — architecture finding kept, citation corrected; PII masking mandatory per internal rule, zero implementation); Reviewer: Dr. Vance — signed off                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 5        | 2026-08-16 | `core-component-00/platform/benchmarks/engineering/multi-agent-engineering/2026-08-16-multi-agent-engineering-enterprise-assessment/enterprise-assessment.md`   | Multi-Agent Engineering (Layer 5)                                                      | v1.0 rewrite — Conditional, no P0 (1 P1: Supervisor-Worker/Router topologies declared but silently fall through to Hybrid, in code with zero test coverage); Reviewer: Dr. Vance — signed off                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Platform | 2026-09-01 | `core-component-00/platform/benchmarks/model-context-protocol-servers/2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md`                    | MCP Servers (`workspace-knowledge`, `agent-memory`) — first platform-domain assessment | v1.0, first pass — Conditional, no P0 (4 P1s: no scenario-regression coverage for `workspace-knowledge`'s tiered-degradation logic; `agent-memory` health-check embedder-capability field is a stale cache, live-reproduced this session; `agent-memory` PII-scrubbing gap externally corroborated, already tracked in `.claude/rules/mcp-governance.md`; 2 P2s: no structured audit logging in either server, `agent-memory` missing conformance/load/pentest test gates); Assessor: Dr. Wieczorek + Ravi Deshmukh; Reviewer: Dr. Vance — **not independently enacted, single-session self-review, see document's Evidence Completeness Statement** |

---

## Related Documentation

| Document                                                    | Purpose                                                             |
| ----------------------------------------------------------- | ------------------------------------------------------------------- |
| `CLAUDE.md`                                                 | Scope, directory structure, authoring rules                         |
| `template/enterprise-assessment.md`                         | The assessment template — full field-by-field authoring guide       |
| `core-component-00/telescope/`                              | Internal research investigation archive (not external benchmarking) |
| `core-component-00/platform/maintenance-records/`           | Operational maintenance log (not benchmarking)                      |
| `crew/director/elias-vance/skills/asgf-compliance-audit.md` | Internal compliance audit against our own ASGF standard             |
| `core-component-00/README.md`                               | CC-00 Laboratory overview                                           |

---

## Contact

**Laboratory Director:** Dr. Elias Vance
**Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`
**Authority:** AGENTS.md § 6. Core Component 00
