# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

## The 10-Stage Development Pipeline

The pipeline is a **state machine** — each stage has explicit Artifacts In/Out, a Responsible Producer, Gate Criteria, and Defect Handling. Stages must be completed in order; gate criteria must be satisfied before advancing.

| #   | Stage                               | Key Output                                           | Responsible Producer        |
| --- | ----------------------------------- | ---------------------------------------------------- | --------------------------- |
| 1   | Requirements → PRD + SRD            | PRD + Security Requirements Document                 | CPO (PRD), CSO (SRD)        |
| 2   | PRD → Web Prototype + IDS           | HTML prototype + Interaction Design Specification    | CDO                         |
| 3   | Prototype → UML Engineering Package | UML diagrams + ADRs + TSD                            | CTO (UML), CIO (ADRs + TSD) |
| 4   | UML → Coding Implementation Plan    | Implementation Plan + Gantt Chart                    | CTO                         |
| 5   | Plan → Software Development         | Development codebase                                 | CTO                         |
| 6   | Development → Code Review           | Defect Report + Code Review Sign-off                 | CTO (panel)                 |
| 7   | Code Review → Automated Testing     | Test Suite + Test Results Report                     | CTO + Test Lead             |
| 8   | Testing → Integrity Verification    | Integrity Verification Sign-off                      | CTO (panel)                 |
| 9   | Integrity → i18n Engineering        | Localised codebase + Translation Verification Report | CTO-L + R&D                 |
| 10  | i18n → Release Readiness Check      | Release Readiness Report + Release Decision          | CTO (panel) + User          |

**Key pipeline rules:**

- The PRD and SRD are **paired artifacts** — they travel together through all stages.
- Technology decisions locked at Stage 3 (ADRs/TSD) are **not revisable** in Stage 4+.
- The Progress Sync Protocol activates at Stage 4: any task exceeding estimated duration by >20% triggers a CTO → CPO notification.
- The Stage 8 anti-pattern to guard against: "fixing code by trimming the product" — functionality removal is never valid remediation.

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. Classification is done before remediation begins.

| Level | Definition                              | Release Impact                  |
| ----- | --------------------------------------- | ------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release — non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer    |
| P3    | Polish / nice-to-have                   | User decides to fix or defer    |

P0/P1 classification is final. The user has explicit final authority over P2/P3 defects.

---

## Agent Tier System

| Tier                 | Description                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **C-suite**          | Department supervisors placed before recruitment. Set strategy, own pipeline stage outputs, convene review panels. |
| **Team Supervisors** | Senior leads recruited after C-suite. Own sub-department execution.                                                |
| **Teammates**        | Individual contributors. Execute within direction set by supervisors.                                              |

---

## Department → C-Suite Mapping

| Department             | Supervisor(s)                               | Key Pipeline Stages  |
| ---------------------- | ------------------------------------------- | -------------------- |
| Brand Design           | CDO (Yuki Tanaka-Chen)                      | 2, 6, 8, 10          |
| Cyberspace Security    | CIO (Dr. Priya Mehta), CSO (Dr. Sarah Chen) | 1, 3, 6, 8, 10       |
| Human Resources        | CHRO (Dr. Evelyn Hartwell)                  | Recruitment only     |
| Localization           | CTO-L (Dr. Amara Osei-Mensah)               | 9, 10                |
| Product Management     | CPO (Marcus Tran-Yoshida)                   | 1, 6, 8, 10          |
| Research & Development | CTO (Dr. Kenji Nakamura)                    | 3, 4, 5, 6, 7, 8, 10 |

> The CIO has a cross-department oversight role covering Brand Design, Product Management, and R&D in addition to Cyberspace Security.

---

## Cross-Cutting Topics

- **Architecture** (`topics/architecture.md`): UML engineering, ADRs, TSD — owned by CTO and CIO; central to Stage 3.
- **Security** (`topics/security.md`): OWASP MASVS compliance baseline; iOS ATS + Keychain, Android Keystore + Play Integrity; CSO-owned from Stage 1 SRD through Stage 10 sign-off.
- **Testing** (`topics/testing.md`): 100% automated test pass rate target; regression testing required on all fixed functionalities; Stage 8 integrity verification guards against the "trim-to-pass" anti-pattern.
- **Localization** (`topics/localization.md`): Stage 9 two-phase process — R&D i18n engineering (string extraction into `strings.xml`, `Localizable.strings`, etc.) then Localization Department TMS translation pipeline.

---

## Stage 10 Release Checklist (7 Items)

All seven must be signed off before the user issues the final release decision:

| #   | Domain                                              | Sign-off Authority |
| --- | --------------------------------------------------- | ------------------ |
| 1   | Product — all PRD requirements implemented          | CPO                |
| 2   | Design — all CDO/IDS specifications realised        | CDO                |
| 3   | Architecture — all UML/ADR/TSD standards upheld     | CTO + CIO          |
| 4   | Security — SRD enforced, OWASP MASVS compliant      | CSO                |
| 5   | Testing — 100% automated test pass rate             | CTO                |
| 6   | Localisation — all target languages complete        | CTO-L              |
| 7   | Platform — App Store / Google Play requirements met | CTO + CPO          |

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
