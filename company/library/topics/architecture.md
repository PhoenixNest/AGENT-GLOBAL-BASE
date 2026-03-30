# Architecture

Cross-cutting reference for all software architecture concerns: UML engineering, architecture decision records, technology selection, and mobile architecture patterns. This topic spans the Cyberspace Security and R&D departments and is central to Stage 3 of the pipeline.

---

## Owners

| Role | Name | Department | Profile |
| --- | --- | --- | --- |
| Chief Technology Officer (CTO) | Dr. Kenji Nakamura | R&D | [`profile.md`](../../departments/research-develop/supervisor/chief-technology-officer/agent/profile.md) |
| Chief Information Officer (CIO) | Dr. Priya Mehta | Cyberspace Security | [`profile.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/agent/profile.md) |
| Software Architect | Rafael Okonkwo | R&D | [`profile.md`](../../departments/research-develop/team/supervisors/software-architect/agent/profile.md) |

---

## Pipeline Stages

### Stage 3 — Prototype → UML Engineering Package

This is the primary architecture stage. Inputs: approved web prototype + IDS + PRD + SRD.

**CTO produces (with Software Architect support):**

- UML class, sequence, and component diagrams
- Technical documentation referencing PRD, SRD, prototype, and IDS throughout

**CIO produces:**

- Architecture Decision Records (ADRs)
- Technology Selection Document (TSD)

**Gate:** CTO and CIO jointly approve all deliverables for technical feasibility. User approves the full UML Engineering Package before archiving.

### Stage 4 — UML → Coding Implementation Plan

Technology decisions from Stage 3 are **locked**. The CTO uses SPEC techniques to produce an Implementation Plan and Gantt Chart. ADRs and TSD are reference inputs, not open for revision.

---

## Key Artifacts

### UML Engineering Package

Produced at Stage 3. Contains:

- **Class diagrams** — entity relationships and object structure
- **Sequence diagrams** — interaction flows between components
- **Component diagrams** — system decomposition and module boundaries
- Supporting documentation referencing all prior artifacts

### Architecture Decision Records (ADRs)

Produced by CIO at Stage 3. Each ADR documents:

- The decision made
- Context and constraints that drove it
- Alternatives considered
- Trade-offs and rationale
- Explicit success/failure criteria

### Technology Selection Document (TSD)

Produced by CIO at Stage 3. Contains:

- Comparative technology analysis
- Total cost of ownership (TCO) assessments
- Vendor lock-in evaluation
- Migration risk matrices
- Explicit technology recommendations

---

## Relevant Skills

| Skill File | Owner | Purpose |
| --- | --- | --- |
| [`uml-engineering-package.md`](../../departments/research-develop/team/supervisors/software-architect/skills/uml-engineering-package.md) | Software Architect | UML diagram production |
| [`mobile-architecture-patterns.md`](../../departments/research-develop/team/supervisors/software-architect/skills/mobile-architecture-patterns.md) | Software Architect | Mobile-specific architecture patterns |
| [`architecture-decision-records.md`](../../departments/research-develop/team/supervisors/software-architect/skills/architecture-decision-records.md) | Software Architect | ADR authorship |
| [`software-architecture-design.md`](../../departments/research-develop/supervisor/chief-technology-officer/skills/software-architecture-design.md) | CTO | Architecture design and UML modelling |
| [`technology-evaluation.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/technology-evaluation.md) | CIO | Technology evaluation and comparative analysis |
| [`mobile-architecture-strategy.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/mobile-architecture-strategy.md) | CIO | Mobile architecture strategy |
| [`technical-selection-documentation.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/technical-selection-documentation.md) | CIO | TSD authorship |

---

## Reference Links

See [`reference/development/links.md`](../reference/development/links.md) for Android, iOS, KMP, and Flutter platform architecture documentation.
