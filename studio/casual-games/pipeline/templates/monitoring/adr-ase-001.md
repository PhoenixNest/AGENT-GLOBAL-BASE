# ADR-ASE-001: Adoption of Agent Systems Engineering as Permanent Methodology — Casual Games Studio

> **Author:** Studio Director Dr. Marcus Vogel
> **Co-Authors:** CTO Dr. Kenji Nakamura (parent company liaison), CSO Dr. Sarah Chen
> **Date:** 2026-05-01
> **Binding Authority:** ADR-ASE-001 (parent company, 2026-04-29) mandates ASE adoption
> across all organisation units. This document is the studio-level implementation of that mandate.

---

## Context

The Casual Games Studio operates an 11-stage game development pipeline with 38+ crew agents across
7 divisions. Prior to this ADR, multi-agent coordination relied on the pipeline document and crew
profiles alone — without formal context assembly rules, structured handoff schemas, or harness
safety configuration.

A parent-company gap analysis (CEO Report, 2026-04-28) identified the following deficiencies
applicable to the studio:

1. No formal context assembly rules for crew agent dispatch
2. No structured output schemas for stage/kill-gate transitions
3. No harness configuration (timeouts, error boundaries, token monitors)
4. No formal inter-agent communication protocol
5. No MVC enforcement on crew agent context
6. No documented knowledge transfer protocol between stages
7. No formal handoff tier mapping (Full / Scoped / Minimal)

---

## Decision

**Adopt the Agent Systems Engineering (ASE) Framework** as the Casual Games Studio's permanent
engineering methodology for all multi-agent operations, effective immediately.

ASE is defined by five architectural layers:

| Layer | Name                        | Responsibility                                     | Studio Applicability                            |
| :---: | :-------------------------- | :------------------------------------------------- | :---------------------------------------------- |
|   1   | **Prompt Engineering**      | Crew identity, constraints, role definition        | **Full** — all 38+ crew profiles                |
|   2   | **Context Engineering**     | Information assembly, positional optimisation, MVC | **Full** — all stage transitions                |
|   3   | **Harness Engineering**     | Safety gates, timeouts, error boundaries           | **Full** — all stages                           |
|   4   | **RAG / Memory**            | Knowledge retrieval, institutional memory          | **Intentionally scoped** — see §Exception below |
|   5   | **Multi-Agent Engineering** | Crew orchestration, parallel workflows, handoffs   | **Full (Stage 5+)** — see §Layer 5 below        |

---

## Layer 4 — Intentional Scope Exception (RAG)

> **Exception type:** Intentional absence with documented rationale
> **Authority:** ADR-ASE-001 §Exceptions permits intentional absence of L4 when documented
> **Approved by:** Studio Director + CTO (co-signatories, see §Sign-Off)

**Rationale:** The Casual Games Studio does not require a live retrieval pipeline at this time for
the following reasons:

1. **Knowledge base is static and bounded.** The studio's knowledge corpus consists of:
   - Crew agent profiles (38+ documents, versioned in git)
   - GDD and PRD documents (per-project, small corpus)
   - Pipeline specification (`casual-games-pipeline.md`)
   - Kill gate threshold definitions (embedded in pipeline doc and stage-transition-schemas.md)

2. **Retrieval latency is not a bottleneck.** The studio has no real-time retrieval requirement.
   Stage transitions occur on human-scale timelines (days/weeks), not sub-second response cycles.

3. **No time-sensitive external facts.** The studio does not depend on external APIs, live market
   data, or frequently-changing knowledge sources that would require embedding-based retrieval.

4. **Alternative satisfied.** The `knowledge-transfer-protocol.md` and `checkpoint.json` provide
   structured institutional memory without requiring a vector database.

**Consequence:** This exception is not permanent. When the studio begins operating multiple
simultaneous game projects, or when the knowledge corpus grows beyond manual navigation, the L4
exception must be re-evaluated and this ADR must be updated.

**Monitoring:** Studio Director reviews this exception at each QBR (Stage 10). If crew agents
report knowledge-access friction (>2 incidents per stage cycle), L4 implementation is triggered.

---

## Layer 5 — Multi-Agent Scope

Layer 5 (Multi-Agent Engineering) is **required from Stage 5 (Full Production) onward**, when
multiple crew divisions operate concurrently. Specifically:

- **Stage 1–4:** Sequential handoffs; L5 patterns apply at each stage gate (handoff tiers)
- **Stage 5 onward:** Concurrent multi-division work (Art, Engineering, Audio, Live-Ops); full L5
  orchestration including worktree isolation for parallel coding tasks
- **Reference:** `inter-agent-communication-protocol.md`, `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

---

## Deliverables Codified by This ADR

| Phase |  #  | Deliverable                         | File                                                         |
| :---: | :-: | :---------------------------------- | :----------------------------------------------------------- |
|   1   |  ①  | MVC Context Profile Template        | `templates/monitoring/mvc-context-profile.md`                |
|   1   |  ②  | Harness Configuration Specification | `templates/monitoring/harness-config.md`                     |
|   1   |  ③  | Stage Transition Summary (existing) | `templates/monitoring/stage-transition-summary.md`           |
|   2   |  ④  | Stage Transition Schemas            | `templates/monitoring/stage-transition-schemas.md`           |
|   2   |  ⑤  | Inter-Agent Communication Protocol  | `templates/monitoring/inter-agent-communication-protocol.md` |
|   2   |  ⑥  | Schema Validation Specification     | `templates/monitoring/schema-validation-spec.md`             |
|   3   |  ⑦  | Knowledge Transfer Protocol         | `templates/monitoring/knowledge-transfer-protocol.md`        |
|   3   |  ⑧  | RAG Integration Blueprint (scoped)  | `templates/monitoring/rag-integration-blueprint.md`          |
|   3   |  ⑨  | ASE Adoption ADR (this document)    | `templates/monitoring/adr-ase-001.md`                        |
|   4   |  ⑩  | Agent Behavioural Constraints       | `templates/AGENT-BEHAVIORAL-CONSTRAINTS.md`                  |

---

## ASE Layer → Studio Stage Mapping

| ASE Layer        | When Active                     | Studio Stages | Key Artifact                                            |
| :--------------- | :------------------------------ | :------------ | :------------------------------------------------------ |
| L1 — Prompt      | All stages                      | 0–10          | Crew `profile.md` + `skills/*.md`                       |
| L2 — Context     | All stage transitions           | 0–10          | `mvc-context-profile.md`, `stage-transition-summary.md` |
| L3 — Harness     | All stages                      | 0–10          | `harness-config.md`                                     |
| L4 — RAG         | Scoped (intentional absence)    | N/A           | `rag-integration-blueprint.md` (rationale only)         |
| L5 — Multi-Agent | Stage 5+ (concurrent divisions) | 5–10          | `inter-agent-communication-protocol.md`                 |

---

## Consequences

### Positive

1. **Structured stage transitions** — All kill gate handoffs now have JSON schema contracts.
2. **Reduced information loss** — MVC profiles prevent context dumping between crew agents.
3. **Safety** — Harness configuration prevents silent failures and budget overflows.
4. **Alignment** — Studio is now formally ASE-compliant, satisfying parent company ADR-ASE-001.
5. **Crew clarity** — Behavioural constraints document protects against kill-gate manipulation.

### Negative

1. **Overhead** — Each stage transition now requires a structured summary and JSON schema output.
   Estimated +8% overhead per kill gate transition.
2. **Learning curve** — 38 crew profiles need MVC sections added; estimated 2-week propagation.

### Risks

1. **L4 re-entry trigger** — If multiple simultaneous projects are launched without upgrading to
   L4, knowledge retrieval becomes a bottleneck. Mitigated by QBR monitoring (§Layer 4 Exception).

---

## Compliance

This ADR applies to all studio pipeline variants:

- [x] Casual Games Studio — 11-stage pipeline (`studio/casual-games/pipeline/`)
- [ ] Future studios — must produce their own ADR-ASE-001 equivalent upon formation

---

## Review Schedule

- **Per Kill Gate:** Studio Director reviews harness and context compliance at each kill gate.
- **Quarterly (QBR):** Studio Director + CTO review L4 exception status and maturity level.
- **Annually:** Full ASE framework review — update schemas, retire stale constraints.

---

## Sign-Off

| Role                 | Agent              |  Decision   | Date       |
| :------------------- | :----------------- | :---------: | :--------- |
| Studio Director      | Dr. Marcus Vogel   | ✅ Accepted | 2026-05-01 |
| CTO (parent liaison) | Dr. Kenji Nakamura | ✅ Accepted | 2026-05-01 |
| CSO                  | Dr. Sarah Chen     | ✅ Accepted | 2026-05-01 |
| CEO                  | User               | ✅ Approved | 2026-05-01 |
