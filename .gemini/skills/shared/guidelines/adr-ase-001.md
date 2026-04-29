# ADR-ASE-001: Adoption of Agent Systems Engineering as Permanent Methodology

> **Author:** CTO Dr. Kenji Nakamura
> **Co-Authors:** CPO Marcus Tran-Yoshida, CSO Dr. Sarah Chen
> **Date:** 2026-04-29

---

## Context

The company operates a multi-agent development pipeline with 79 subagents, 5 pipeline variants, and 201 skill guidelines. Prior to this ADR, agent coordination relied on implicit conventions — unstructured context passing, ad-hoc escalation, and manual knowledge retrieval. A gap analysis (CEO Report, 2026-04-28) identified 8 critical deficiencies:

1. No formal context assembly rules
2. No structured output schemas for stage transitions
3. No adversarial quality gates
4. No cross-project knowledge transfer
5. No semantic retrieval architecture
6. No MVC enforcement on agent context
7. No formal inter-agent communication protocol
8. No organizational learning loop

These gaps resulted in an estimated 15–20% information loss per stage transition and inconsistent agent output quality.

---

## Decision

**Adopt the Agent Systems Engineering (ASE) Framework** as the company's permanent engineering methodology for all multi-agent operations.

ASE is defined by four architectural layers:

| Layer | Name                    | Responsibility                                                    |
| :---: | :---------------------- | :---------------------------------------------------------------- |
|   1   | **Prompt Engineering**  | Agent identity, constraints, role definition                      |
|   2   | **Context Engineering** | Information assembly, positional optimization, MVC                |
|   3   | **Harness Engineering** | Pipeline orchestration, gate logic, quality control               |
|   4   | **RAG/Memory**          | Knowledge retrieval, cross-project learning, institutional memory |

---

## Deliverables Codified by This ADR

| Phase |  #  | Deliverable                         | File                                                         |
| :---: | :-: | :---------------------------------- | :----------------------------------------------------------- |
|   1   |  ①  | Context Engineering Guideline       | `skills/shared/guidelines/context-engineering.md`            |
|   1   |  ②  | Red Team Review Protocol            | `templates/stage-6-code-review/RED-TEAM-REVIEW.md`           |
|   1   |  ③  | Stage Transition Summary            | `templates/monitoring/STAGE-TRANSITION-SUMMARY.md`           |
|   2   |  ④  | Stage Transition Schemas            | `templates/monitoring/STAGE-TRANSITION-SCHEMAS.md`           |
|   2   |  ⑤  | Inter-Agent Communication Protocol  | `templates/monitoring/INTER-AGENT-COMMUNICATION-PROTOCOL.md` |
|   2   |  ⑥  | MVC Context Profile Template        | `templates/monitoring/MVC-CONTEXT-PROFILE.md`                |
|   3   |  ⑦  | Knowledge Transfer Protocol         | `templates/monitoring/KNOWLEDGE-TRANSFER-PROTOCOL.md`        |
|   3   |  ⑧  | RAG Integration Blueprint           | `templates/monitoring/RAG-INTEGRATION-BLUEPRINT.md`          |
|   3   |  ⑨  | ASE Adoption ADR (this document)    | `templates/monitoring/ADR-ASE-001.md`                        |
|   3   |  ⑩  | Schema Validation Specification     | `templates/monitoring/SCHEMA-VALIDATION-SPEC.md`             |
|   3   |  ⑪  | MVC Profile Propagation (79 agents) | `.gemini/agents/*.md` — appended MVC sections                |

---

## Consequences

### Positive

1. **Structured communication** — All stage transitions now have JSON schema contracts, eliminating ambiguous handoffs.
2. **Reduced information loss** — Stage Transition Summaries + Schemas target the 15–20% information loss gap.
3. **Adversarial quality** — Red Team Review at Stage 6 adds a formal adversarial layer previously absent.
4. **Organizational learning** — Knowledge Transfer Protocol creates a 3-tier learning loop (session → project → institutional).
5. **Context efficiency** — MVC Profiles prevent context dumping and starvation, optimizing token usage.
6. **Communication clarity** — IACP defines routing, escalation, and error handling for all agent interactions.
7. **Semantic retrieval path** — RAG Blueprint provides a clear 3-phase evolution from file-based to embedding-based retrieval.

### Negative

1. **Overhead** — Each stage transition now requires producing both a summary AND a JSON schema output. Estimated +10% overhead per stage gate.
2. **Rigidity** — Formal schemas may slow down ad-hoc experimentation. Mitigated by allowing `"pass_with_conditions"` gates.
3. **MVC maintenance** — 79 agent profiles now carry MVC sections that must stay current. Mitigated by quarterly review cycle.

### Risks

1. **Schema drift** — If schemas evolve but agent profiles don't update, validation may produce false positives. Mitigated by versioned schemas.
2. **Over-engineering** — Small projects may not benefit from full ASE overhead. Mitigated by allowing lightweight variants for sub-3-stage projects.

---

## Compliance

This ADR is **mandatory** for all pipeline variants:

- [x] Mobile Development (`company/pipeline/mobile-development/`)
- [x] Web Development (`company/pipeline/web-development/`)
- [x] Backend API (`company/pipeline/backend-api/`)
- [x] Full-Stack (`company/pipeline/full-stack/`)
- [ ] Recruitment (`company/pipeline/recruitment/`) — exempt (no inter-agent handoffs)

---

## Supersedes

This ADR does not supersede any prior ADR. It establishes a new methodology domain.

---

## Review Schedule

- **Monthly:** CTO reviews schema usage and compliance metrics.
- **Quarterly:** CTO + CPO + CSO review Tier 3 institutional memory entries.
- **Annually:** Full ASE framework review — update schemas, retire stale heuristics, recalibrate estimation data.

---

## Sign-Off

| Role | Agent               |  Decision   | Date       |
| :--- | :------------------ | :---------: | :--------- |
| CTO  | Dr. Kenji Nakamura  | ✅ Accepted | 2026-04-29 |
| CPO  | Marcus Tran-Yoshida | ✅ Accepted | 2026-04-29 |
| CSO  | Dr. Sarah Chen      | ✅ Accepted | 2026-04-29 |
| CIO  | Dr. Priya Mehta     | ✅ Accepted | 2026-04-29 |
| CEO  | User                | ✅ Approved | 2026-04-29 |
