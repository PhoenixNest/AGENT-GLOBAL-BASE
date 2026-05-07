# Company Pipeline Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Part II — The Three Systems § 4. The Company

---

## Overview

The **Company Pipeline Power** provides comprehensive support for the Company's 13-stage development pipeline across all four variants: Mobile, Web, Backend API, and Full-Stack development.

This Power packages:

- **Pipeline Documentation**: Complete 13-stage pipeline specifications
- **ASE Templates**: Agent Systems Engineering compliance templates
- **Steering Files**: Conditional activation for pipeline-specific guidance
- **Templates**: PRD, SRD, ADR, TSD, and monitoring templates

---

## What This Power Provides

### 1. Pipeline Documentation

Access to the complete 13-stage development pipeline:

| Stage | Name                                            | Key Deliverables      |
| ----- | ----------------------------------------------- | --------------------- |
| 0     | Problem Validation                              | Problem statement     |
| 1     | Requirements → PRD + SRD                        | PRD, SRD              |
| 2     | PRD → Web Prototype + IDS                       | Prototype, IDS        |
| 3     | Prototype → UML Engineering Package             | UML, ADRs, TSD        |
| 4     | UML → Implementation Plan + Gantt               | Plan, Gantt           |
| 5     | Plan → Software Development                     | Code                  |
| 6     | Development → Arch. & Conformance Review        | Review report         |
| 7     | Arch. Review → Automated Testing                | Test suite            |
| 8     | Testing → Integrity Verification                | Verification report   |
| 9     | Integrity Verification → Translation Production | Translations          |
| 9.5   | Internal Dogfood                                | Dogfood feedback      |
| 10    | Translation Production → Release Readiness      | Release package       |
| 11    | Live Operations                                 | Monitoring, incidents |

### 2. Pipeline Variants

- **Mobile Development**: Android, iOS, KMP, Flutter
- **Web Development**: React, Vue, Angular, PWA
- **Backend API**: REST, GraphQL, gRPC
- **Full-Stack**: Combined frontend + backend

### 3. Templates

All templates are located in `company/pipeline/<variant>/templates/`:

- **PRD Template**: Product Requirements Document
- **SRD Template**: Security Requirements Document
- **ADR Template**: Architecture Decision Record
- **TSD Template**: Technology Selection Document
- **Monitoring Templates**: ASE compliance monitoring

### 4. Steering Files

Conditional steering files auto-activate when working in pipeline directories:

- `company-pipeline-overview.md` — Overall 13-stage pipeline
- `mobile-pipeline.md` — Mobile-specific rules
- `web-pipeline.md` — Web-specific rules
- `backend-pipeline.md` — Backend API rules
- `full-stack-pipeline.md` — Full-stack rules

---

## How to Use This Power

### Activate the Power

```typescript
kiroPowers({
  action: "activate",
  powerName: "company-pipeline",
});
```

### Start a New Pipeline Project

1. **Choose your pipeline variant**: Mobile, Web, Backend API, or Full-Stack
2. **Navigate to**: `company/pipeline/<variant>/`
3. **Read**: `pipeline.md` for complete stage specifications
4. **Use templates**: Copy from `templates/` directory
5. **Follow stage gates**: Respect user approval requirements (✅)

### Key Pipeline Rules

| Rule                         | Applies At | Detail                                                             |
| ---------------------------- | ---------- | ------------------------------------------------------------------ |
| **Technology Decision Lock** | Stage 3    | ADRs and TSD are immutable after user approval                     |
| **Trim-to-Pass Forbidden**   | Stage 8    | Never remove features/security to pass integrity verification      |
| **Defect Severity (P0–P3)**  | All stages | P0/P1 classification is non-overridable                            |
| **Stage 6 Remediation Loop** | Stage 6    | Full review panel process repeats after any remediation            |
| **PRD + SRD Pairing**        | Stage 1+   | These two documents travel as a unit through all subsequent stages |

---

## Pipeline Governance

### User Approval Gates

Stages marked **User Approval? ✅** are **hard stops**:

- Stage 1: Requirements → PRD + SRD
- Stage 2: PRD → Web Prototype + IDS
- Stage 3: Prototype → UML Engineering Package
- Stage 4: UML → Implementation Plan + Gantt
- Stage 6: Development → Arch. & Conformance Review
- Stage 7: Arch. Review → Automated Testing
- Stage 10: Translation Production → Release Readiness Check

### ASE Compliance

All pipelines enforce the Agent Systems Engineering (ASE) framework:

- **Layer 1**: Prompt Engineering — Standardized instruction patterns
- **Layer 2**: Context Engineering — Structured handoffs, context windows
- **Layer 3**: Harness Engineering — Automated gate enforcement
- **Layer 4**: RAG / Memory — Institutional knowledge retention
- **Layer 5**: Multi-Agent — Swarm orchestration and isolation

---

## Related Powers

- **CC-00 Engineering**: LLM engineering patterns for agent-powered systems
- **Casual Games Pipeline**: Studio's 11-stage game development pipeline
- **Organizational Agents**: Type A agent activation and management

---

## Quick Start Examples

### Example 1: Start Mobile Development Project

```typescript
// 1. Activate the power
kiroPowers({ action: "activate", powerName: "company-pipeline" });

// 2. Navigate to mobile pipeline
// Read: company/pipeline/mobile-development/pipeline.md

// 3. Stage 0: Problem Validation
// Work with CPO to validate the problem

// 4. Stage 1: Create PRD + SRD
// Use templates from company/pipeline/mobile-development/templates/
// - prd-template.md
// - srd-template.md

// 5. Get user approval for Stage 1 ✅

// 6. Continue through stages...
```

### Example 2: Execute Specific Stage

```typescript
// Use pipeline-stage-executor agent
invokeSubAgent({
  name: "pipeline-stage-executor",
  prompt: "Execute Stage 3 (UML Engineering Package) for the dark mode feature",
  explanation: "Delegating Stage 3 execution to pipeline executor",
  contextFiles: [
    "company/pipeline/mobile-development/pipeline.md",
    "project/prd.md",
    "project/srd.md",
  ],
});
```

### Example 3: Review Stage Deliverables

```typescript
// Activate relevant organizational agent
invokeSubAgent({
  name: "company-research-develop-chief-technology-officer-kenji-nakamura",
  prompt: "Review the UML Engineering Package for Stage 3 compliance",
  explanation: "CTO review of Stage 3 deliverables",
  contextFiles: [
    "project/uml-package/",
    "company/pipeline/mobile-development/pipeline.md",
  ],
});
```

---

## Defect Classification Guide

### P0 — Critical (Blocks Release)

**Examples:**

- App crashes on launch
- Data corruption or loss
- Security vulnerability (SQL injection, XSS, authentication bypass)
- Payment processing failure
- Complete loss of core functionality

**Response:** Immediate fix required (same day)

### P1 — High (Blocks Release)

**Examples:**

- Login fails for specific user types
- Critical user flow broken (checkout, signup)
- Major performance degradation (>5s load time)
- Data sync failures

**Response:** Fix within 24 hours

### P2 — Medium (User Decides)

**Examples:**

- Minor UI glitches
- Non-critical feature not working
- Cosmetic issues
- Minor performance issues

**Response:** Fix within 1 week

### P3 — Low (User Decides)

**Examples:**

- Typos in UI text
- Minor visual inconsistencies
- Feature enhancement requests
- Documentation issues

**Response:** Next sprint

---

## Templates Overview

### PRD Template (Product Requirements Document)

Located at: `company/pipeline/<variant>/templates/prd-template.md`

**Sections:**

1. Executive Summary
2. Problem Statement
3. Goals and Success Metrics
4. User Stories
5. Functional Requirements
6. Non-Functional Requirements
7. Out of Scope
8. Dependencies
9. Timeline

### SRD Template (Security Requirements Document)

Located at: `company/pipeline/<variant>/templates/srd-template.md`

**Sections:**

1. Security Overview
2. Authentication Requirements
3. Authorization Requirements
4. Data Protection
5. Network Security
6. Compliance Requirements
7. Security Testing
8. Incident Response

### ADR Template (Architecture Decision Record)

Located at: `company/pipeline/<variant>/templates/adr-template.md`

**Sections:**

1. Title
2. Status (Proposed/Accepted/Deprecated/Superseded)
3. Context
4. Decision
5. Consequences
6. Alternatives Considered

### TSD Template (Technology Selection Document)

Located at: `company/pipeline/<variant>/templates/tsd-template.md`

**Sections:**

1. Technology Stack Overview
2. Frontend Technologies
3. Backend Technologies
4. Database Selection
5. Infrastructure
6. Third-Party Services
7. Rationale
8. Risk Assessment

---

## Monitoring and Progress Tracking

### Required Files (Stage 4+)

For any project at or beyond Stage 4, maintain these files:

| File              | Purpose                     | Location     |
| ----------------- | --------------------------- | ------------ |
| `progress.md`     | Real-time state             | Project root |
| `session-log.md`  | Audit trail                 | Project root |
| `checkpoint.json` | Machine-readable milestones | Project root |

### Progress Monitoring Format

```markdown
# Project Progress

**Project:** Dark Mode Feature
**Pipeline:** Mobile Development
**Current Stage:** 5 (Software Development)
**Last Updated:** 2026-05-06

## Stage Status

- [x] Stage 0: Problem Validation
- [x] Stage 1: Requirements → PRD + SRD
- [x] Stage 2: PRD → Web Prototype + IDS
- [x] Stage 3: Prototype → UML Engineering Package
- [x] Stage 4: UML → Implementation Plan + Gantt
- [ ] Stage 5: Plan → Software Development (IN PROGRESS)
- [ ] Stage 6: Development → Arch. & Conformance Review
- [ ] Stage 7: Arch. Review → Automated Testing
- [ ] Stage 8: Testing → Integrity Verification
- [ ] Stage 9: Integrity Verification → Translation Production
- [ ] Stage 9.5: Internal Dogfood
- [ ] Stage 10: Translation Production → Release Readiness
- [ ] Stage 11: Live Operations

## Current Tasks

1. Implement dark mode theme switching
2. Update all UI components for dark mode
3. Add user preference persistence

## Blockers

None

## Next Milestone

Complete Stage 5 by 2026-05-10
```

---

## Troubleshooting

### Issue: Technology change requested at Stage 5

**Solution:** Technology decisions lock at Stage 3. Any change requires:

1. Create new ADR documenting the change
2. Return to Stage 3 for full re-entry
3. Get user approval for new Stage 3 deliverables
4. Never edit existing ADRs or TSD

### Issue: P0 defect found at Stage 8

**Solution:**

1. Classify defect severity (P0 = blocks release)
2. Never downgrade to P2 to pass the stage
3. Fix the defect
4. Re-run Stage 8 verification
5. P0/P1 classification is non-negotiable

### Issue: Stage 6 remediation completed

**Solution:**

1. After any remediation, the full review panel process repeats
2. Do not resume at defect verification only
3. Full panel review from the beginning

---

## References

- **Pipeline Specifications**: `company/pipeline/<variant>/pipeline.md`
- **Company Overview**: `company/library/README.md`
- **Personnel Roster**: `company/library/overview/personnel.md`
- **AGENTS.md**: § Part II — The Three Systems § 4. The Company
- **ASE Framework**: `core-component-00/agent-systems-engineering/`

---

**Power Maintained By:** Company C-Suite (CPO, CDO, CTO, CIO, CSO, CTO-L, CHRO)  
**Last Updated:** 2026-05-06
