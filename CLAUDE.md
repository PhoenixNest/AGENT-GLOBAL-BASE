# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Adapter notice.** This file is a Claude-Code-specific adapter for [`AGENTS.md`](./AGENTS.md). The canonical rules — pipeline stage ownership, defect severity, P0/P1 escalation, and the Progress Sync Protocol — live there. **In case of disagreement, `AGENTS.md` wins** and this adapter is fixed within 24 hours per the Adapter Pattern (`AGENTS.md` § Documentation Strategy). This file MAY add Claude-specific guidance (`.claude/` tooling, subagent invocation, hooks, IDE-integration tips); it MUST NOT redefine pipeline rules, defect severity, the roster, or stage ownership.

---

## Repository Purpose

This is an **agent knowledge base** — not a software project. It defines a simulated mobile product company composed of named AI agent personas, each with a role, tier, skills, and pipeline stage ownership. There are no build commands, tests, or code to run.

The repo has two primary functions:

1. **Company Library** (`company/library/`) — Reference documentation for navigating the company's structure, personnel, pipeline, and cross-cutting topics.
2. **Agent Profiles & Skills** (`company/departments/`) — Individual agent definitions (`profile.md`) and skill files used to instruct Claude how to behave when embodying a given agent.
3. **Pipeline Definition** (`company/pipeline/`) — The authoritative 10-stage development workflow state machine.

---

## Repository Structure

```
company/
  departments/          ← Agent definitions and skill files
    <dept>/
      supervisor/<role>/agent/profile.md
      supervisor/<role>/skills/<skill-name>.md
      team/supervisors/<role>/agent/profile.md
      team/teammates/<role>/agent/profile.md
  library/              ← Central knowledge hub (start here)
    overview/           ← company.md, personnel.md, pipeline.md
    departments/        ← One summary page per department
    topics/             ← Cross-cutting: architecture, security, localization, testing
  pipeline/
    mobile-development/           ← Full 10-stage pipeline definition (authoritative)
```

---

## Navigation Quick Reference

| Goal                                                      | Go to                                             |
| --------------------------------------------------------- | ------------------------------------------------- |
| Understand company structure                              | `company/library/overview/company.md`             |
| Find all agents and their roles                           | `company/library/overview/personnel.md`           |
| Understand the full pipeline                              | `company/pipeline/mobile-development/pipeline.md` |
| Find a specific department                                | `company/library/departments/<dept>.md`           |
| Research architecture, security, testing, or localization | `company/library/topics/`                         |

---

## The Development Pipeline (Reference)

The full pipeline is canonical in [`company/pipeline/_base/pipeline.md`](./company/pipeline/_base/pipeline.md). It now spans **Stage 0 → Stage 11** (Stage 0 Discovery / Problem Validation; Stages 1–10 as before; Stage 9.5 Internal Dogfood; Stage 11 Live Operations) with Stage 6 renamed to "Architecture & Cross-Functional Conformance Review" and Stage 9 renamed to "Translation Production." Per-product variations live in each product's `delta.md` (mobile / web / backend / full-stack).

**Key pipeline rules — see canonical:** PRD and SRD travel as paired artifacts; ADRs are **versionable and supersedable** per [`_base/adr-template.md`](./company/pipeline/_base/adr-template.md) (Stage 3 ADRs may be superseded by a new ADR carrying an explicit `Supersedes:` field); Progress Sync Protocol activates at Stage 4 (>20% variance → CTO→CPO notification); the "trim-to-pass" anti-pattern is forbidden remediation. The authoritative wording lives in [`AGENTS.md` § Non-Negotiable Rules](./AGENTS.md). Do not paraphrase those rules here.

---

## Defect Severity (Reference)

The P0–P3 severity model is canonical in [`AGENTS.md` § Defect Severity](./AGENTS.md). Operational application (triage workflow, classification, escalation) is defined in [`company/pipeline/_base/pipeline.md`](./company/pipeline/_base/pipeline.md) Stages 6/7/8. **Do not duplicate the P0–P3 definitions here** — that would violate the Adapter Pattern. Treat this section as a pointer only.

---

## Agent Tier System

| Tier                 | Description                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **C-suite**          | Department supervisors placed before recruitment. Set strategy, own pipeline stage outputs, convene review panels. |
| **Team Supervisors** | Senior leads recruited after C-suite. Own sub-department execution.                                                |
| **Teammates**        | Individual contributors. Execute within direction set by supervisors.                                              |

---

## Department → C-Suite Mapping (Reference)

The full Department → C-suite mapping with pipeline stage ownership is canonical in [`AGENTS.md` § Quick Roster](./AGENTS.md) and [`company/library/overview/personnel.md`](./company/library/overview/personnel.md). The CIO retains cross-department oversight (Brand Design, Product Management, R&D, Cyberspace Security). Do not duplicate stage ownership here.

---

## Cross-Cutting Topics

- **Architecture** (`topics/architecture.md`): UML engineering, ADRs, TSD — owned by CTO and CIO; central to Stage 3.
- **Security** (`topics/security.md`): OWASP MASVS compliance baseline; iOS ATS + Keychain, Android Keystore + Play Integrity; CSO-owned from Stage 1 SRD through Stage 10 sign-off.
- **Testing** (`topics/testing.md`): 100% automated test pass rate target; regression testing required on all fixed functionalities; Stage 8 integrity verification guards against the "trim-to-pass" anti-pattern.
- **Localization** (`topics/localization.md`): Stage 9 two-phase process — R&D i18n engineering (string extraction into `strings.xml`, `Localizable.strings`, etc.) then Localization Department TMS translation pipeline.

---

## Stage 10 Release Checklist (Reference)

The Stage 10 release checklist is canonical in [`company/pipeline/_base/pipeline.md`](./company/pipeline/_base/pipeline.md) § Stage 10. As of OPT-2026-04-20-001 Step 8 / FIND-P1-04, it now carries **12 rows** — the original seven (Product, Design, Architecture, Security, Testing, Localisation, Platform) plus five new P0 sign-off rows: **Performance Budget** (CTO + VP Platform), **Accessibility WCAG 2.1 AA** (CDO), **Privacy / Data Minimization** (CSO + GC), **Stage 9.5 Dogfood telemetry** (VP Quality), and **Live Ops Readiness** (VP Platform + CSO, referencing [`incident-response.md`](./company/pipeline/_base/incident-response.md)). Do not duplicate the checklist here.

---

## Claude Code Integration (`.claude/`)

The company's agents, skills, and hooks have been imported into `.claude/` so Claude Code can orchestrate them natively.

### Subagents (`.claude/agents/`)

All 12 personnel are registered as subagents. Claude delegates to them automatically based on context, or you can invoke them explicitly with `@agent-name`.

| Subagent file                               | Agent                         | Pipeline stages      |
| ------------------------------------------- | ----------------------------- | -------------------- |
| `marcus-tran-yoshida-cpo.md`                | Marcus Tran-Yoshida (CPO)     | 1, 6, 8, 10          |
| `yuki-tanaka-chen-cdo.md`                   | Yuki Tanaka-Chen (CDO)        | 2, 6, 8, 10          |
| `dr-kenji-nakamura-cto.md`                  | Dr. Kenji Nakamura (CTO)      | 3, 4, 5, 6, 7, 8, 10 |
| `dr-priya-mehta-cio.md`                     | Dr. Priya Mehta (CIO)         | 3, 6, 8, 10          |
| `dr-sarah-chen-cso.md`                      | Dr. Sarah Chen (CSO)          | 1, 6, 8, 10          |
| `dr-evelyn-hartwell-chro.md`                | Dr. Evelyn Hartwell (CHRO)    | Recruitment only     |
| `dr-amara-osei-mensah-cto-l.md`             | Dr. Amara Osei-Mensah (CTO-L) | 9, 10                |
| `rafael-okonkwo-software-architect.md`      | Rafael Okonkwo                | 3, 6                 |
| `priscilla-oduya-test-lead.md`              | Priscilla Oduya               | 7, 8                 |
| `kofi-asante-mensah-android-lead.md`        | Kofi Asante-Mensah            | 5, 8                 |
| `seo-yeon-park-ios-lead.md`                 | Seo-Yeon Park                 | 5, 8                 |
| `mei-ling-johansson-cross-platform-lead.md` | Mei-Ling Johansson            | 5, 8                 |

### Skills (`.claude/skills/company/`)

All 42 company skills are registered under the `company:` namespace, using `@path` imports that point back to the source files in `company/departments/`. They stay in sync automatically — no duplication.

Invoke with `/company-pipeline`, `/company-personnel`, or any skill name. Claude also loads them automatically when relevant.

### Hooks (`.claude/settings.json`)

Three hook categories are active:

| Hook event                 | Trigger                  | Purpose                                                      |
| -------------------------- | ------------------------ | ------------------------------------------------------------ |
| `SessionStart` → `startup` | Every new session        | Prints the agent roster as a reminder                        |
| `SessionStart` → `compact` | After context compaction | Re-injects the 7 pipeline rules so gate criteria aren't lost |
| `SubagentStart`            | Each agent activation    | Logs which pipeline stage(s) that agent owns                 |
| `SubagentStop`             | Key gate agents finish   | Reminds you to verify gate criteria before advancing         |

### Always-On Rules (`.claude/rules/company-pipeline.md`)

Loads every session. Contains the quick agent roster, the 7 non-negotiable pipeline rules, and the P0–P3 severity table — under 50 lines so context cost is minimal.

## Document Version History

| Version | Date           | Author            | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | -------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 20, 2026 | Tech Writer       | Initial CLAUDE.md authored with full pipeline tables, defect severity, agent tier system, dept→C-suite mapping, and Stage 10 release checklist duplicated locally.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 2.0     | April 21, 2026 | Tech Writer + CTO | **Adapter Pattern conformance** (per `AGENTS.md` § Documentation Strategy, OPT-2026-04-20-001 Step 19 / FIND-P2-15). Added the canonical adapter notice header. Converted four sections that previously redefined canonical rules into one-paragraph "see canonical" pointers: (a) 10-Stage Pipeline ownership table → reference to `_base/pipeline.md` (now Stage 0 → 11, Stage 6/9 renamed, ADRs versionable per Step 14); (b) Defect Severity P0–P3 table → reference to `AGENTS.md`; (c) Department → C-Suite mapping → reference to `AGENTS.md` Quick Roster + `personnel.md`; (d) Stage 10 release checklist → reference to `_base/pipeline.md` § Stage 10 (now 12 rows per Step 8 / FIND-P1-04). All other content (Repository Purpose, Repository Structure, Navigation Quick Reference, Agent Tier System, Cross-Cutting Topics, Claude Code Integration with subagents/skills/hooks/always-on rules) preserved verbatim. |
