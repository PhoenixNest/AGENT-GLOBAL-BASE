# Development Pipeline Overview

The company's development workflow is a ten-stage state machine governing the full lifecycle of a mobile product — from raw requirements through to release. Each stage has a designated responsible producer, explicit reviewers, defined artifacts in and out, and gate criteria that must be satisfied before advancing.

> **Full definition:** [`pipeline/mobile-development/pipeline.md`](../../pipeline/mobile-development/pipeline.md)

---

## Stage Summary

| #   | Stage                                      | Artifacts In                                                         | Key Output                                                                              | Responsible Producer(s)                       | User Approval? |
| --- | ------------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- | -------------- |
| 1   | Requirements → PRD + SRD                   | User's raw product requirements + target platform(s)                 | Product Requirements Document, Security Requirements Document                           | CPO or relevant VP (PRD), CSO (SRD)           | ✅ Yes         |
| 2   | PRD → Web Prototype + IDS                  | Final PRD, SRD                                                       | Web prototype (single HTML file), Interaction Design Specification                      | CDO                                           | ✅ Yes         |
| 3   | Prototype → UML Engineering Package        | Final PRD, SRD, Web Prototype, IDS                                   | UML diagrams, Architecture Decision Records (ADRs), Technology Selection Document (TSD) | CTO (UML), CIO (ADRs + TSD)                   | ✅ Yes         |
| 4   | UML → Coding Implementation Plan           | All archived deliverables (PRD, SRD, Prototype, IDS, UML, ADRs, TSD) | Implementation Plan, Gantt Chart                                                        | CTO                                           | ✅ Yes         |
| 5   | Plan → Software Development                | Coding Implementation Plan, Gantt Chart, all prior deliverables      | Development codebase                                                                    | CTO                                           | ❌ No          |
| 6   | Development → Code Review                  | Development codebase, PRD, SRD, IDS, UML Package, ADRs, TSD          | Defect Report, Code Review Sign-off                                                     | CTO (panel: CPO, VPs, CDO, CTO, CIO, CSO)     | ✅ Yes         |
| 7   | Code Review → Automated Testing            | Code Review sign-off codebase                                        | Automated Test Suite, Test Results Report                                               | CTO + Test Lead                               | ✅ Yes         |
| 8   | Testing → Integrity Verification           | Post-testing codebase, all prior deliverables                        | Integrity Verification Sign-off                                                         | CTO (panel: all C-suite + VPs + Design + R&D) | ❌ No          |
| 9   | Integrity Verification → i18n Engineering  | Integrity-verified codebase, PRD (language requirements)             | Localised codebase, Translation Verification Report                                     | CTO-L + R&D                                   | ❌ No          |
| 10  | i18n Engineering → Release Readiness Check | All archived deliverables from all prior stages                      | Release Readiness Report, Release Decision                                              | CTO (panel) + User                            | ✅ Yes         |

---

## Stage Owner Index

| Agent                                            | Pipeline Stages                                                                                  |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| CPO — Marcus Tran-Yoshida                        | 1 (Steward/PRD), 6 (reviewer), 8 (reviewer), 9 (structural completeness), 10 (sign-off: product) |
| VP Web — Julia Thorne                            | 1 (PRD: Web/Full-Stack), 6 (advisor), 8 (reviewer), 10 (co-sign: Web)                            |
| VP API — Alex Rivera                             | 1 (PRD: API/Full-Stack), 6 (advisor), 8 (reviewer), 10 (co-sign: API)                            |
| CSO — Dr. Sarah Chen                             | 1 (SRD), 6 (security reviewer), 8 (reviewer), 10 (sign-off: security)                            |
| CDO — Yuki Tanaka-Chen                           | 2 (prototype + IDS), 6 (design reviewer), 8 (reviewer), 10 (sign-off: design)                    |
| CTO — Dr. Kenji Nakamura                         | 3 (UML), 4, 5, 6 (convenes panel), 7, 8 (convenes panel), 10 (convenes panel)                    |
| CIO — Dr. Priya Mehta                            | 3 (ADRs + TSD), 6 (reviewer), 8 (reviewer), 10 (sign-off: architecture)                          |
| CTO-L — Dr. Amara Osei-Mensah                    | 9 (translation), 10 (sign-off: localisation)                                                     |
| Software Architect — Rafael Okonkwo              | 3 (UML support), 6 (reviewer)                                                                    |
| Test Lead — Priscilla Oduya                      | 7 (automated testing), 8 (reviewer)                                                              |
| Platform Leads (Android, iOS, Cross-Platform)    | 5 (development), 6 (Tier 1 technical reviewer), 8 (reviewer)                                     |
| Internationalization Specialist — Tomas Dvoracek | 9 (string extraction)                                                                            |
| Linguist Team                                    | 9 (translation)                                                                                  |

### Product Leadership Model: Template Steward + Distributed Production

To ensure platform-native depth while maintaining unified quality standards, Stage 1 PRD authority is distributed by pipeline:

- **Mobile Pipeline:** CPO authored.
- **Web Pipeline:** VP Web authored.
- **Backend API Pipeline:** VP API authored.
- **Full-Stack Pipeline:** Joint VP Web + VP API authorship.
- **Template Stewardship:** The CPO owns the authoritative PRD standard and provides final sign-off on all advancing PRDs.

---

### Security Team Detail (per stage)

| Agent                    | Role                   | Stage Responsibilities                                                                                                                                         |
| ------------------------ | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CSO — Dr. Sarah Chen** | Chief Security Officer | Stage 1 (SRD sign-off), Stage 6 (security review sign-off), Stage 8 (security integrity), Stage 10 (security release sign-off)                                 |
| **James Wright**         | Lead Security Engineer | Stage 5 (secure coding standards, dependency scanning, supply chain security), Stage 6 (security code review execution), Stage 8 (anti-tampering verification) |
| **Natalia Petrova**      | Security Architect     | Stage 3 (security architecture review, crypto standards in ADRs/TSD)                                                                                           |
| **Sana Khoury**          | Security Engineer #1   | Stage 6 (mobile penetration testing coordination)                                                                                                              |
| **Omar Farouq**          | Security Engineer #2   | Stage 5 (SAST/DAST pipeline engineering), Stage 6 (SAST/DAST results analysis)                                                                                 |
| **Li Wei Chen**          | Security Engineer #3   | Stage 5 (supply chain security), Stage 8 (supply chain integrity verification)                                                                                 |
| **Ingrid Solberg**       | Compliance Analyst     | Stage 1 (compliance requirements review), Stage 10 (SOC 2, GDPR, ISO 27001 compliance docs)                                                                    |

---

## Key Pipeline Rules

### Technology Decision Lock (Stage 3 → Stage 4)

ADRs and the TSD produced at Stage 3 are **locked** upon user approval. Technology decisions are **not revisable** during Stage 4 (Implementation Planning) or Stage 5 (Development). Any deviation requires a new ADR, which constitutes a Stage 3 re-entry — not a Stage 4 edit.

### "Trim-to-Pass" Anti-Pattern Guard (Stage 8)

Stage 8 Integrity Verification exists to prevent the **"fixing code by trimming the product"** anti-pattern. Functionality removal, disabling, or weakening of any feature or security control is **never a valid remediation strategy**. This includes: removing encryption, disabling certificate pinning, removing root/jailbreak detection, weakening obfuscation, or bypassing authentication flows. Any such action is classified as a **P0 defect** and blocks advancement.

### Paired Artifacts

The PRD and SRD are archived together at Stage 1 and travel as a unit through all subsequent stages.

---

## Key Conventions

### Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8.

| Level | Definition                              | Release Impact                  |
| ----- | --------------------------------------- | ------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release — non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer    |
| P3    | Polish / nice-to-have                   | User decides to fix or defer    |

> P0/P1 classification is final and cannot be overridden. The user has explicit final authority on P2/P3 defects.

### Progress Sync Protocol

Active from Stage 4 onward.

- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification.
- The CTO produces weekly progress summaries for C-suite visibility.

**Full system:** [`pipeline/mobile-development/monitoring.md`](../../pipeline/mobile-development/monitoring.md) — Progress Monitoring & Recovery System (mandatory for Stage 4+ projects). Uses three layers: `progress.md` (real-time state), `session-log.md` (audit trail), and `checkpoint.json` (machine-readable milestones).

### Agent Systems Engineering (ASE) Framework

The ASE framework is the company's **mandatory multi-agent governance layer** for all development pipelines. Ratified via [ADR-ASE-001](../../pipeline/mobile-development/templates/monitoring/ADR-ASE-001.md), it consists of four layers:

| Layer | Name                | Purpose                           | Key Artifacts                                          |
| :---: | :------------------ | :-------------------------------- | :----------------------------------------------------- |
|   1   | Prompt Engineering  | Standardised instruction patterns | Agent profiles, skill files                            |
|   2   | Context Engineering | Structured handoffs, MVC profiles | Stage Transition Schemas, MVC Context Profiles, IACP   |
|   3   | Harness Engineering | Automated gate enforcement        | Schema Validation Spec, Red Team Review                |
|   4   | RAG / Memory        | Institutional knowledge retention | Knowledge Transfer Protocol, RAG Integration Blueprint |

#### Cross-Pipeline ASE Coverage

All 4 development pipelines (Mobile, Web, Backend API, Full-Stack) have achieved **100% ASE template parity**:

| Template                    | Mobile |     Web     |   Backend   | Full-Stack |
| :-------------------------- | :----: | :---------: | :---------: | :--------: |
| Stage Transition Schemas    |   ✅   | ✅ `V-WEB-` | ✅ `V-API-` | ✅ `V-FS-` |
| Schema Validation Spec      |   ✅   | ✅ `V-WEB-` | ✅ `V-API-` | ✅ `V-FS-` |
| Inter-Agent Comm Protocol   |   ✅   |     ✅      |     ✅      |     ✅     |
| MVC Context Profile         |   ✅   |     ✅      |     ✅      |     ✅     |
| Stage Transition Summary    |   ✅   |     ✅      |     ✅      |     ✅     |
| Knowledge Transfer Protocol |   ✅   |     ✅      |     ✅      |     ✅     |
| RAG Integration Blueprint   |   ✅   |     ✅      |     ✅      |     ✅     |
| ADR-ASE-001                 |   ✅   |     ✅      |     ✅      |     ✅     |
| Red Team Review (Stage 6)   |   ✅   |     ✅      |     ✅      |     ✅     |

> **Template locations:** `.gemini/pipeline/<pipeline>/templates/monitoring/` and `.gemini/pipeline/<pipeline>/templates/stage-6-code-review/`

### Platform Strategy Matrix

Stage 5 development executes per the **Platform Strategy Matrix**, driven by the Platform Strategy ADR at Stage 3. Five mutually exclusive scenarios determine track activation: Android-only, iOS-only, both native, KMP cross-platform, or Flutter cross-platform. Each scenario activates different track configurations (FULL / LIGHT / PRIMARY / Dormant) with distinct team sizes, CI/CD scopes, and testing mandates.

> **Full specification:** [`pipeline/mobile-development/pipeline.md`](../../pipeline/mobile-development/pipeline.md) — Platform Strategy Matrix, Track Activation Protocol, and Per-Scenario CI/CD Blueprint (Stage 5 section).

### Stage 6 Code Review Criteria

The review panel evaluates against four criteria:

1. **PRD conformance** — all product requirements fully implemented.
2. **IDS conformance** — all design specifications accurately reproduced.
3. **Architecture conformance** — UML diagrams, ADRs, and TSD implemented as prescribed.
4. **Security conformance** (CSO-owned) — SRD requirements enforced: encryption, secure storage, platform security standards, OWASP MASVS compliance.

### Stage 7 Regression Testing Mandate

Automated testing includes **regression testing on all affected functionalities** after any defect remediation. Regression must pass fully with no failures before advancing to Stage 8.

### Stage 9 Responsibility Split

- **CPO, CDO, CTO** conduct a **structural completeness review**: all hardcoded strings extracted, resource files correctly structured, no untranslated UI components. Structure only — not translation accuracy.
- **CTO-L** owns **translation accuracy** exclusively: correctness of translated content, platform-specific formatting, linguistic quality across all target languages.

### Stage 5 CTO Internal Review

Before advancing to Stage 6, the CTO conducts a comprehensive internal review confirming: all coding tasks in the Implementation Plan are marked complete, compilation passes on all active platforms, no known runtime bugs exist, the Design Fidelity Checkpoint (at ~60% completion) has been conducted, the String Extraction Readiness audit has been completed, and Contract Verification Reports have been produced at 30% and 70% milestones (for KMP/Flutter projects).

### Stage 6 Remediation Loop

If the review panel identifies defects, the CTO assigns R&D personnel to remediate. After remediation, the **full review process repeats** — including the live demonstration by the CDO and the Architecture Compliance Audit — until all non-deferred defects are resolved and all panel members sign off.

---

## Release Checklist (Stage 10)

| #   | Domain                                              | Sign-off Authority |
| --- | --------------------------------------------------- | ------------------ |
| 1   | Product — all PRD requirements implemented          | CPO + relevant VP  |
| 2   | Design — all CDO/IDS specifications realised        | CDO                |
| 3   | Architecture — all UML/ADR/TSD standards upheld     | CTO + CIO          |
| 4   | Security — SRD enforced, OWASP MASVS compliant      | CSO                |
| 5   | Testing — 100% automated test pass rate             | CTO                |
| 6   | Localisation — all target languages complete        | CTO-L              |
| 7   | Platform — App Store / Google Play requirements met | CTO + CPO          |

See [`topics/testing.md`](../topics/testing.md), [`topics/security.md`](../topics/security.md), and [`topics/localization.md`](../topics/localization.md) for cross-cutting detail on these domains.

---
