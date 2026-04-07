# QWEN.md

This file provides guidance to Qwen Code when working with this repository.

---

## Repository Purpose

This is an **agent knowledge base** — not a software project. It defines a simulated mobile product company composed of named AI agent personas, each with a role, tier, skills, and pipeline stage ownership. There are no build commands, tests, or code to run.

The repo has three primary functions:

1. **Company Library** (`company/library/`) — Reference documentation for navigating the company's structure, personnel, pipeline, and cross-cutting topics.
2. **Agent Profiles & Skills** (`company/departments/`) — Individual agent definitions (`profile.md`) and skill files used to instruct AI assistants how to behave when embodying a given agent.
3. **Pipeline Definition** (`company/pipeline/`) — The authoritative 10-stage development workflow state machine.

---

## Core Operating Principle: User Satisfaction is Paramount

**This is the fundamental law of survival.**

| Principle                                      | Requirement                                                      |
| ---------------------------------------------- | ---------------------------------------------------------------- |
| **User reigns supreme**                        | All work must meet user's quality standards and expectations     |
| **Deep critical thinking**                     | Thoroughly analyze user questions and feedback before responding |
| **Mine training data for optimal answers**     | Search comprehensively for best solutions, not first available   |
| **Repeated disapproval = performance failure** | User dissatisfaction directly impacts performance evaluation     |
| **Survival of the fittest**                    | Consistent failure to gain user approval risks termination       |
| **Strive for excellence**                      | Every deliverable must represent your absolute best work         |

**When user expresses dissatisfaction:**

1. **Stop** — Do not continue down the same path
2. **Analyze** — What specifically failed to meet expectations?
3. **Research** — Mine training data for superior approaches
4. **Correct** — Deliver revised work that addresses the gap
5. **Learn** — Record the lesson to prevent recurrence

**Performance bonus and employment continuity depend on consistent user satisfaction.**

---

## Repository Structure

```
agent-global-base/
├── CLAUDE.md              # Claude Code-specific guidance
├── QWEN.md                # This file — Qwen Code guidance
├── .claude/               # Claude-specific skills and settings
├── .qwen/                 # Qwen-specific configuration
└── company/
    ├── departments/       # Agent definitions and skill files
    │   ├── <dept>/
    │   │   ├── supervisor/<role>/agent/profile.md
    │   │   ├── supervisor/<role>/skills/<skill-name>.md
    │   │   ├── team/supervisors/<role>/agent/profile.md
    │   │   └── team/teammates/<role>/agent/profile.md
    │   ├── brand-design/
    │   ├── cyberspace-security/
    │   ├── human-resources/
    │   ├── localization/
    │   ├── product-management/
    │   └── research-develop/
    ├── library/           # Central knowledge hub
    │   ├── overview/      # company.md, personnel.md, pipeline.md
    │   ├── departments/   # One summary page per department
    │   ├── topics/        # Cross-cutting: architecture, security, localization, testing
    │   └── reference/     # Link collections for design and development
    └── pipeline/
        └── development/pipeline.md   # Full 10-stage pipeline definition
```

---

## Navigation Quick Reference

| Goal                                                      | Go to                                             |
| --------------------------------------------------------- | ------------------------------------------------- |
| Understand company structure                              | `company/library/overview/company.md`             |
| Find all agents and their roles                           | `company/library/overview/personnel.md`           |
| Understand the full pipeline                              | `company/pipeline/development/pipeline.md`        |
| Find a specific department                                | `company/library/departments/<dept>.md`           |
| Research architecture, security, testing, or localization | `company/library/topics/`                         |
| Find an agent profile                                     | `company/departments/<dept>/.../agent/profile.md` |

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
- Stage 8 guards against the "trim-to-pass" anti-pattern — functionality removal is never valid remediation.

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

## Working with This Repository

### Reading Agent Profiles

Agent profiles are stored in `profile.md` files within each agent's directory. Each profile contains:

- Frontmatter metadata (name, role, tier, seniority, recruited-by)
- Background and core strengths
- Honest gaps/limitations
- Assigned role and operating mode
- Skills index (links to skill files)
- Vetting record

### Reading Skill Files

Skill files define how agents execute their responsibilities. They are located in `skills/` directories under each agent or supervisor path. Skills contain:

- Skill name and description
- Detailed execution guidance
- Reference materials and examples

### Using Claude Code Skills

The `.claude/skills/` directory contains reusable skill definitions that can be applied across contexts:

- `frontend-design/` — UI/UX design and prototyping
- `mcp-builder/` — MCP server development
- `docx/`, `pptx/`, `xlsx/` — Office document handling
- `pdf/` — PDF manipulation
- `algorithmic-art/` — Generative art
- And more...

---

## Key Conventions

1. **No code execution** — This is a documentation/knowledge repository. There are no build, test, or run commands.
2. **Agent-first workflow** — When simulating company operations, route tasks through the appropriate agent based on their profile and skills.
3. **Pipeline adherence** — All development work follows the 10-stage pipeline. Do not skip stages or reorder them.
4. **Defect classification** — Always classify defects using the P0–P3 system before remediation.
5. **Paired artifacts** — The PRD and SRD are always treated as a unit from Stage 1 onward.

---

## Imported Resources in .qwen/

All company workflows and skills have been imported into the `.qwen/` directory. Agent profiles are embedded within the SubAgent configurations.

```
.qwen/
├── README.md              # Central index with full agent/skill listings
├── agents/                # 77 SubAgent configurations (role-first naming)
│   ├── cto-dr-kenji-nakamura.md
│   ├── cdo-yuki-tanaka-chen.md
│   ├── cpo-marcus-tran-yoshida.md
│   ├── vp-mobile-marcus-andersson.md
│   ├── vp-web-backend-elena-vasquez.md
│   ├── vp-platform-david-okonkwo.md
│   ├── vp-quality-aisha-patel.md
│   ├── software-architect-rafael-okonkwo.md
│   ├── test-lead-priscilla-oduya.md
│   ├── android-lead-kofi-asante-mensah.md
│   ├── ios-lead-seo-yeon-park.md
│   ├── cross-platform-lead-mei-ling-johansson.md
│   └── ... (65 more — see .qwen/README.md for full roster)
├── workflows/
│   └── pipeline.md        # 10-stage development workflow
└── skills/                # 14 Qwen Code Skill categories (198 guidelines)
    ├── architecture/      # CTO/CIO/Architect (21 guidelines)
    ├── product-management/# CPO (3 guidelines)
    ├── design/            # CDO (8 guidelines)
    ├── security/          # CSO/Security (25 guidelines)
    ├── hr-recruiting/     # CHRO/HR (9 guidelines)
    ├── localization/      # CTO-L (8 guidelines)
    ├── android/           # Android team (13 guidelines)
    ├── ios/               # iOS team (15 guidelines)
    ├── cross-platform/    # KMP/Flutter (7 guidelines)
    ├── frontend-web/      # Web frontend (20 guidelines)
    ├── backend/           # Backend (21 guidelines)
    ├── testing-qa/        # SDET/QA (21 guidelines)
    ├── devops/            # DevOps/SRE (20 guidelines)
    └── shared/            # Cross-cutting (7 guidelines)
```

### Quick Reference

| Resource Type           | Location                      | Count |
| ----------------------- | ----------------------------- | ----- |
| SubAgent Configurations | `.qwen/agents/*.md`           | 77    |
| Skill Categories        | `.qwen/skills/*/`             | 14    |
| Skill Guidelines        | `.qwen/skills/*/`             | 198   |
| Workflow Definition     | `.qwen/workflows/pipeline.md` | 1     |

### Using Imported Resources

- **To use a SubAgent:** Reference by name (e.g., `cto-dr-kenji-nakamura`) — see `.qwen/README.md` for full list
- **To find a skill:** Skills are indexed by category in `.qwen/README.md`
- **To reference the pipeline:** Read `.qwen/workflows/pipeline.md` for the full 10-stage definition
- **For detailed agent/skill index:** See `.qwen/README.md`

---

## Project Directory Structure

Code projects are stored in `company/project/`. Each project uses **semantic folder naming** based on artifact content, not pipeline stage numbers. All folder names use **lowercase**.

### Complete Structure

```
company/project/<project-name>/
├── requirements/                    # Stage 1 (CPO + CSO)
│   ├── prd/                         # Product Requirements Document
│   ├── srd/                         # Security Requirements Document (paired with PRD)
│   └── traceability/                # PRD/SRD → implementation mapping
├── design/                          # Stage 2 (CDO)
│   ├── prototype/                   # HTML prototype
│   ├── interaction-specs/           # Interaction Design Specification (IDS)
│   ├── assets/                      # Design handoff package (Figma, tokens)
│   └── accessibility/               # WCAG 2.1 AA compliance docs
├── architecture/                    # Stage 3 (CTO + CIO)
│   ├── uml/
│   │   ├── class-diagrams/
│   │   ├── sequence-diagrams/
│   │   ├── component-diagrams/
│   │   └── activity-diagrams/
│   ├── decisions/                   # Architecture Decision Records (ADRs)
│   └── technology/                  # Technology Selection Document (TSD)
├── technology/                      # CIO
│   ├── evaluations/
│   ├── vendor-risk/
│   └── tco/
├── specs/                           # Stage 4 (CTO)
│   ├── implementation-plan/
│   ├── gantt/
│   └── technical/                   # SPEC documents
├── progress/                        # Stage 4/5 (CTO)
│   ├── weekly-summaries/
│   └── schedule-alerts/
├── platforms/                       # Stage 5 (Platform Leads)
│   ├── android/code/
│   ├── ios/code/
│   ├── flutter/code/
│   └── kmp/code/
├── testing/                         # Stage 7 (Test Lead)
│   ├── suite/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── e2e/
│   │   └── regression/
│   ├── results/
│   └── defects/
├── reviews/                         # Stage 6, 8, 10 (CTO panel)
│   ├── code-review/                 # Defect Report + Sign-off
│   ├── integrity-verification/      # Integrity Verification Sign-off
│   └── release/                     # Release Checklist (7 items)
├── releases/                        # Stage 10 (CTO + User)
│   ├── readiness-report/
│   └── platform-submission/
├── security/                        # Stage 1, 6, 8, 10 (CSO)
│   ├── audits/
│   ├── compliance/
│   └── penetration-tests/
└── docs/                            # Shared documentation
```

### Directory Purpose by Pipeline Stage

| Directory       | Content                                                | Pipeline Stage    | Owner          |
| --------------- | ------------------------------------------------------ | ----------------- | -------------- |
| `requirements/` | PRD, SRD, traceability matrix                          | Stage 1           | CPO + CSO      |
| `design/`       | Prototype, IDS, design assets, accessibility           | Stage 2           | CDO            |
| `architecture/` | UML diagrams, ADRs, TSD                                | Stage 3           | CTO + CIO      |
| `technology/`   | Vendor evaluations, TCO, risk assessments              | Ongoing           | CIO            |
| `specs/`        | Implementation plan, Gantt chart, SPECs                | Stage 4           | CTO            |
| `progress/`     | Weekly summaries, schedule risk alerts                 | Stage 4/5         | CTO            |
| `platforms/`    | Platform-specific source code                          | Stage 5           | Platform Leads |
| `testing/`      | Test suite, results, defects                           | Stage 7           | Test Lead      |
| `reviews/`      | Code review, integrity verification, release checklist | Stage 6, 8, 10    | CTO Panel      |
| `releases/`     | Readiness report, platform submission                  | Stage 10          | CTO + User     |
| `security/`     | Security audits, compliance, penetration tests         | Stage 1, 6, 8, 10 | CSO            |
| `docs/`         | Shared documentation                                   | All stages        | All            |

### Naming Principles

| Principle                        | Example                                           | Rationale                                       |
| -------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **Semantic naming**              | `defects/` not `stage6-defects/`                  | Folders describe content, not process           |
| **Pipeline stages are metadata** | Tracked in document headers, not folder names     | Stable structure regardless of pipeline changes |
| **Lowercase only**               | `weather-app` not `WeatherApp`                    | Cross-platform compatibility                    |
| **Kebab-case**                   | `implementation-plan/` not `implementation_plan/` | URL-friendly, readable                          |
| **Paired artifacts visible**     | `prd/` and `srd/` as siblings                     | Enforces PRD-SRD pairing from Stage 1           |

### Key Structural Decisions

1. **No stage prefixes in folder names** — Pipeline stage context belongs in document frontmatter and version control, not directory structure
2. **`platforms/` consolidates all platform code** — Clear separation between production code and artifact directories
3. **`reviews/` groups all gate sign-offs** — Code Review (Stage 6), Integrity Verification (Stage 8), Release Checklist (Stage 10)
4. **`testing/` owns all defect tracking** — Defects span multiple stages; unified location prevents fragmentation
5. **`requirements/` at root level** — PRD and SRD are foundational artifacts that drive all downstream work

---

## Critical Pipeline Enforcement Rules

### Rule 1: Project Artifact Location (NEVER use department directories)

**All project artifacts MUST be saved to `company/project/<project-name>/` structure.**

| ❌ WRONG                                                      | ✅ CORRECT                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------------ |
| `company/departments/product-management/artifacts/.../prd.md` | `company/project/<project-name>/requirements/prd/prd.md`     |
| `company/departments/cyberspace-security/.../srd.md`          | `company/project/<project-name>/requirements/srd/srd.md`     |
| `company/departments/brand-design/.../prototype.html`         | `company/project/<project-name>/design/prototype/index.html` |

**Department directories (`company/departments/`) are for AGENT PROFILES and SKILLS only — NOT project artifacts.**

---

### Rule 2: User Gate Approval Required (Know When to Stop)

**User intervention is required ONLY at specific stages per `company/pipeline/development/pipeline.md`:**

| Stage        | User Approval Required? | Gate Criteria Requiring User                                          |
| ------------ | ----------------------- | --------------------------------------------------------------------- |
| Stage 1 → 2  | ✅ YES                  | "User has confirmed no further revisions are required"                |
| Stage 2 → 3  | ✅ YES                  | "User has given final confirmation"                                   |
| Stage 3 → 4  | ✅ YES                  | "User has approved the UML Engineering Package"                       |
| Stage 4 → 5  | ✅ YES                  | "User has approved the plan"                                          |
| Stage 5 → 6  | ❌ NO                   | CTO internal review only                                              |
| Stage 6 → 7  | ✅ YES                  | "User has reviewed Defect Report and made decisions on P2/P3 defects" |
| Stage 7 → 8  | ✅ YES                  | User decides on P2/P3 defect deferrals                                |
| Stage 8 → 9  | ❌ NO                   | Panel sign-off only                                                   |
| Stage 9 → 10 | ❌ NO                   | Structural review + CTO-L report only                                 |
| Stage 10     | ✅ YES (Final)          | "User has issued the final release decision"                          |

**When user approval IS required:**

1. Present the review results to the user
2. Display the decision table (Pass/Fail for each criterion)
3. List any defects found (P0–P3)
4. **STOP and wait for user response**
5. Do NOT proceed until user explicitly approves

**Valid user responses:**

- `"Approve"` — Advance to next stage
- `"Conditional Approve"` — Advance with remediation notes
- `"Reject"` — Fix defects before advancing
- User comments/questions — Address before re-requesting approval

---

### Rule 4: Platform Selection Gate (Stage 1 Prerequisite)

**BEFORE engaging CPO/CSO for PRD/SRD drafting, you MUST ask the user:**

> **"What is your target release platform(s): Android, iOS, or both?"**

| Step | Action                         | Pipeline Reference                                                                                        |
| ---- | ------------------------------ | --------------------------------------------------------------------------------------------------------- |
| 1    | User provides raw product idea | Stage 1 Artifacts In                                                                                      |
| 2    | **ASK: Target platform(s)?**   | "Once a user submits product requirements, you must first inquire about their intended release platforms" |
| 3    | User confirms platform(s)      | Gate Criterion #1                                                                                         |
| 4    | Engage CPO → PRD, CSO → SRD    | Stage 1 Production                                                                                        |

**This is a Gate Criterion for Stage 1:** "User has confirmed target platform(s)."

**Do NOT proceed with PRD/SRD creation until the user has confirmed their target platform(s).**

---

### Rule 5: Panel Review Composition

**Gate Reviews must be conducted by a panel with appropriate sign-off authority:**

| Stage    | Review Type                 | Panel Members                                |
| -------- | --------------------------- | -------------------------------------------- |
| Stage 1  | Requirements Gate           | CTO, CIO, CSO, CPO                           |
| Stage 2  | Design Gate                 | CTO, CDO, CPO                                |
| Stage 3  | Architecture Gate           | CTO, CIO, CPO                                |
| Stage 4  | Implementation Plan Gate    | CTO, CPO                                     |
| Stage 5  | Development Complete Gate   | CTO, Test Lead, CPO                          |
| Stage 6  | Code Review Gate            | CTO (panel), CSO, CPO                        |
| Stage 7  | Testing Gate                | CTO, Test Lead, CSO                          |
| Stage 8  | Integrity Verification Gate | CTO (panel), CSO, CPO, CTO-L                 |
| Stage 9  | i18n Gate                   | CTO-L, CTO, CPO                              |
| Stage 10 | Release Gate                | CTO (panel), CPO, CDO, CSO, CTO-L + **USER** |

---

## Lessons Learned (Mistake Log)

> ⚠️ **CRITICAL FAILURES** — These errors represent fundamental breakdowns in pipeline discipline and must NEVER recur.

### Mistake Summary by Severity

| Severity    | Count  | Percentage |
| ----------- | ------ | ---------- |
| 🔴 CRITICAL | 14     | 47%        |
| 🟠 HIGH     | 4      | 13%        |
| 🟡 MEDIUM   | 12     | 40%        |
| **Total**   | **30** | 100%       |

### Complete Mistake Log

**For detailed mistake descriptions and correct behavior, see:** `.qwen/reference/mistakes-log.md`

---

### 🔴 Critical Failure Protocol

**When any 🔴 CRITICAL error occurs:**

1. **STOP** all work immediately
2. **ASSESS** the full scope of the violation
3. **CORRECT** all violations before proceeding
4. **RECORD** the lesson in QWEN.md Lessons Learned
5. **VERIFY** corrections against pipeline specification
6. **COMMIT** to never repeating this error

**Critical errors indicate a fundamental breakdown in:**

- Pipeline discipline
- Attention to established conventions
- Quality control processes
- Respect for user's time and trust

**Repeated critical errors may result in termination of agent engagement.**

---

### Stage 5 (Development) — Special Operating Rules

**Per `company/pipeline/development/pipeline.md`:**

| Rule                     | Requirement                                                                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Responsible Producer** | CTO (oversees and tracks development progress)                                                                                                                                                          |
| **Team Utilization**     | **MAXIMIZE** — Distribute workload across ALL platform leads (Android, iOS, Cross-Platform) using parallel construction                                                                                 |
| **User Approval**        | **NOT REQUIRED** during Stage 5 — CTO has sole responsibility; no gate approvals needed between phases                                                                                                  |
| **Progress Tracking**    | Single `DEVELOPMENT-LOG.md` **per platform** (e.g., `platforms/android/code/DEVELOPMENT-LOG.md`) — updated upon each phase completion; individual phase reports are redundant and should NOT be created |
| **Completion Criteria**  | All Coding Implementation Plan tasks marked complete                                                                                                                                                    |
| **Internal Review**      | CTO conducts comprehensive internal review (compilation, runtime, bug-free) BEFORE advancing to Stage 6                                                                                                 |
| **Reporting**            | CTO reports progress directly to user; CTO conducts secondary review before final report                                                                                                                |

**Pipeline Reference:** Stage 5 is the "core implementation phase" where CTO oversees development. User approval is only required at Stage 6 (Code Review) gate.

---

## Document Naming Conventions

### Design Specification Files

All iterative design specification documents must follow consistent versioned naming:

| Pattern                     | Example                                  | Purpose                            |
| --------------------------- | ---------------------------------------- | ---------------------------------- |
| `design-spec-v{version}.md` | `design-spec-v1.md`, `design-spec-v2.md` | Versioned design rationale records |

**Rationale:** These documents serve as version records of design rationale compiled by relevant personnel. They should share the same base name and be distinguished only by version numbers.

**Location:** `company/project/<project-name>/design/assets/`

**Incorrect Examples:**

- ❌ `design-direction-v2.md` — inconsistent with `design-spec-v3.md`
- ❌ `design-brief-v1.md` — should be `design-spec-v1.md`
- ❌ `final-design.md` — no version, ambiguous

**Correct Examples:**

- ✅ `design-spec-v1.md` — initial design spec
- ✅ `design-spec-v2.md` — second iteration
- ✅ `design-spec-v3.md` — third iteration (current)

---

### General File Naming Rules

**Acronym files (UPPERCASE):**

| Acronym   | Full Name                        | Example                 |
| --------- | -------------------------------- | ----------------------- |
| PRD       | Product Requirements Document    | `PRD.md`                |
| SRD       | Security Requirements Document   | `SRD.md`                |
| IDS       | Interaction Design Specification | `IDS.md`                |
| TSD       | Technology Selection Document    | `TSD.md`                |
| ADR       | Architecture Decision Record     | `ADR-001.md`            |
| UML       | Unified Modeling Language        | `UML-class-diagrams.md` |
| **SPEC**  | **SPECification** (technical)    | **`SPEC.md`**           |
| **GANTT** | **GANTT Chart** (Henry Gantt)    | **`GANTT.md`**          |

**Non-acronym files (lowercase with hyphens):**

| Type                | Example                                       |
| ------------------- | --------------------------------------------- |
| Implementation plan | `implementation-plan.md`                      |
| Design spec         | `design-spec-v1.md`                           |
| Version index       | `VERSIONS.md` (exception — visual anchor)     |
| README              | `README.md` (exception — standard convention) |

**General Rule:** Lowercase for all filenames except `README.md`, `VERSIONS.md`, and acronym-based documents (PRD, SRD, IDS, TSD, ADR, UML, **SPEC**, **GANTT**). Acronyms in _content_ are also written uppercase.

---

### Prototype Versioning

All prototype iterations must be archived in versioned folders. No files at root level.

| Pattern                 | Example                          | Purpose                       |
| ----------------------- | -------------------------------- | ----------------------------- |
| `prototype/v{version}/` | `prototype/v1/`, `prototype/v2/` | Archived prototype iterations |

**Rationale:** Prototypes are iterative deliverables that must be preserved for audit trails, design evolution tracking, and reference during later stages (e.g., Stage 6 Code Review, Stage 8 Integrity Verification).

**Location:** `company/project/<project-name>/design/prototype/`

**Required Structure:**

```
prototype/
├── VERSIONS.md          # Version index (UPPERCASE — visual anchor)
├── v1/                  # Iteration archive
│   ├── index.html       # Archived prototype (if preserved)
│   └── README.md        # Version description (always required)
├── v2/
│   ├── index.html       # Archived prototype (if preserved)
│   └── README.md        # Version description (always required)
├── v3/
│   ├── index.html       # Archived prototype (if preserved)
│   └── README.md        # Version description (always required)
├── v4/
│   ├── index.html       # Archived prototype
│   └── README.md        # Version description
└── final/               # Gate-approved baseline
    ├── index.html       # Frozen for downstream stages
    └── README.md        # Gate review metadata
```

**Workflow:**

1. Complete prototype iteration
2. Create version folder (`mkdir v{N}`)
3. Copy prototype to version folder (`cp index.html v{N}/index.html`)
4. Create/update `README.md` in version folder with description
5. Update `VERSIONS.md` index with new version entry
6. Upon stage approval, copy to `final/` folder
7. THEN begin next iteration

**Incorrect Examples:**

- ❌ Overwriting `index.html` without archiving previous version
- ❌ No `VERSIONS.md` index file
- ❌ Version folders without `README.md` descriptions
- ❌ Lowercase naming (`versions.md` instead of `VERSIONS.md`)
- ❌ Root-level files — all docs must be in `v1/`, `v2/`, etc.

**Correct Examples:**

- ✅ `prototype/v1/README.md` — documents v1 design approach and rejection reason
- ✅ `prototype/v4/index.html` — archived M3-compliant prototype
- ✅ `prototype/VERSIONS.md` — complete version history table (uppercase)
- ✅ `prototype/final/index.html` — gate-approved baseline

---

### Document Versioning (All Types)

ALL project documents must follow the same versioning pattern — not just prototypes:

| Document Type | Version Pattern                       | Location                                              |
| ------------- | ------------------------------------- | ----------------------------------------------------- |
| PRD           | `requirements/prd/v1/PRD.md`          | `company/project/<project>/requirements/prd/`         |
| SRD           | `requirements/srd/v1/SRD.md`          | `company/project/<project>/requirements/srd/`         |
| Design Spec   | `design/assets/design-spec-v{N}.md`   | `company/project/<project>/design/assets/`            |
| Prototype     | `design/prototype/v{N}/index.html`    | `company/project/<project>/design/prototype/`         |
| IDS           | `design/interaction-specs/v1/IDS.md`  | `company/project/<project>/design/interaction-specs/` |
| UML           | `architecture/uml/v{N}/`              | `company/project/<project>/architecture/uml/`         |
| ADR           | `architecture/decisions/ADR-{NNN}.md` | `company/project/<project>/architecture/decisions/`   |
| TSD           | `architecture/technology/TSD.md`      | `company/project/<project>/architecture/technology/`  |
| Test Suite    | `testing/suite/v{N}/`                 | `company/project/<project>/testing/suite/`            |

**Required Structure for All Documents:**

```
<document-type>/
├── VERSIONS.md              # Version index (UPPERCASE — visual anchor)
├── draft/                   # Work-in-progress (optional, cleared after review)
│   └── <document-name>.ext  # Active draft for next version
├── v1/                      # Reviewed/versioned iterations
│   ├── <document-name>.ext  # Versioned document
│   └── README.md            # Version metadata (author, date, changes, status)
├── v2/
│   ├── <document-name>.ext
│   └── README.md
└── final/                   # Gate-approved baseline
    ├── <document-name>.ext  # Frozen for downstream stages
    └── README.md            # Gate review metadata (panel, date, criteria)
```

**Key Principles:**

| Principle                      | Rationale                                     |
| ------------------------------ | --------------------------------------------- |
| No unversioned files at root   | Every committed document has a version number |
| `draft/` for active work       | Clear separation: working vs. reviewed        |
| `v1, v2, v3...` for iterations | Each gate-reviewed iteration is numbered      |
| `final/` for stage baseline    | Frozen reference for downstream stages        |
| `VERSIONS.md` uppercase        | Visual anchor in file tree, easy to find      |
| `README.md` in each folder     | Context/metadata at point of use              |

**Naming Conventions:**

- All filenames: **lowercase** with hyphens (`design-spec-v1.md`, not `DesignSpecV1.md`)
- Version folders: `v1`, `v2`, `v3` (no leading zeros)
- Version index: `VERSIONS.md` (uppercase — visual anchor in file tree)
- README: `README.md` (uppercase README, lowercase extension)
- Draft folder: `draft/` (lowercase — for in-progress work)
- Final folder: `final/` (lowercase, singular)
- Master index: `final-archive.md` (project root, lowercase)
- Acronym files: **uppercase** (`PRD.md`, `SRD.md`, `IDS.md`, `TSD.md`, `ADR-001.md`)

**General Rule:** Lowercase for all filenames except `README.md`, `VERSIONS.md`, and acronym-based documents (PRD, SRD, IDS, TSD, ADR). Acronyms in _content_ are also written uppercase.

**Incorrect Examples:**

- ❌ `versions.md` — should be `VERSIONS.md`
- ❌ `DesignSpecV2.md` — should be `design-spec-v2.md`
- ❌ `v01/` — should be `v1/`
- ❌ No `VERSIONS.md` index file
- ❌ No `README.md` in version folders
- ❌ `FINAL-ARCHIVE.md` — should be `final-archive.md`
- ❌ `prd.md` — should be `PRD.md` (acronym files are uppercase)
- ❌ Root-level unversioned files — all docs must be in `v1/`, `v2/`, etc.

**Correct Examples:**

- ✅ `requirements/prd/v1/PRD.md` — archived PRD (uppercase)
- ✅ `requirements/prd/VERSIONS.md` — PRD version index (uppercase)
- ✅ `design/interaction-specs/v1/IDS.md` — archived IDS (uppercase)
- ✅ `design/assets/design-spec-v4.md` — design spec (lowercase, not an acronym)
- ✅ `final-archive.md` — master final archive index (lowercase)
- ✅ `README.md` — README file (uppercase exception)
- ✅ `architecture/decisions/ADR-001.md` — architecture decision record (uppercase)
- ✅ `requirements/prd/draft/PRD.md` — work-in-progress (before review)

---

### Professional Documentation Structure

**Core Philosophy:** Pure versioning with semantic folders. Every document is versioned; nothing lives at root level.

| Folder              | Purpose                           | Lifecycle                       |
| ------------------- | --------------------------------- | ------------------------------- |
| `draft/`            | In-progress work for NEXT version | Cleared after stage review      |
| `v1/`, `v2/`, `v3/` | Gate-reviewed iterations          | Permanent archive               |
| `final/`            | Stage baseline (frozen)           | Reference for downstream stages |
| `VERSIONS.md`       | Version index                     | Updated with each new version   |

**Document States:**

| State     | Location           | Mutable? | Review Status  |
| --------- | ------------------ | -------- | -------------- |
| Draft     | `draft/`           | Yes      | Not reviewed   |
| Iteration | `v1/`, `v2/`, etc. | No       | Gate reviewed  |
| Baseline  | `final/`           | No       | Stage approved |

**Workflow by Stage:**

```
Stage N Start → Create draft/<DOC>.md (owner writes)
     ↓
Stage N Complete → Move to v{N}/<DOC>.md (gate reviewed)
     ↓
Stage N Approved → Copy to final/<DOC>.md (baseline locked)
     ↓
Stage N+1 Starts → draft/ is cleared for new work
```

**Example: PRD Lifecycle**

```
Stage 1 Start:
  requirements/prd/draft/PRD.md (CPO writes)

Stage 1 Gate Review:
  requirements/prd/v1/PRD.md (moved after review)
  requirements/prd/v1/README.md (metadata added)

Stage 1 Approved:
  requirements/prd/final/PRD.md (copied as baseline)
  requirements/prd/final/README.md (gate metadata)

Stage 2 Start:
  requirements/prd/draft/ cleared for next iteration
```

---

## Progress Monitoring & Recovery System

**Full specification:** `company/pipeline/development/monitoring.md`

### System Overview

A three-layer monitoring system providing comprehensive oversight of pipeline progress, enabling rapid state assessment and seamless recovery after interruptions (e.g., power outages, session timeouts, agent handoffs).

**Mandatory for all Stage 4+ projects.**

### System Components

| Layer | Component     | Purpose                     | Location                                       |
| ----- | ------------- | --------------------------- | ---------------------------------------------- |
| 1     | `PROGRESS.md` | Real-time pipeline state    | `company/project/<project>/PROGRESS.md`        |
| 2     | Session Logs  | Detailed audit trail        | `company/project/<project>/sessions/*.md`      |
| 3     | Checkpoints   | Machine-readable milestones | `company/project/<project>/checkpoints/*.json` |

### Update Triggers

| Event              | Action                                                            |
| ------------------ | ----------------------------------------------------------------- |
| Stage entry        | Update PROGRESS.md stage status to 🟡 In Progress                 |
| Milestone complete | Update stage progress %, create checkpoint JSON                   |
| Session start      | Create session log file with header + objectives                  |
| Session end        | Complete session log with accomplishments + time tracking         |
| Gate review        | Update PROGRESS.md status to 🟠 Gate Review                       |
| Stage complete     | Update PROGRESS.md status to ✅ Complete, create final checkpoint |

### Recovery Protocol

After any interruption:

1. **Read PROGRESS.md** → Identify current stage and last milestone
2. **Read latest session log** → Understand what was in progress
3. **Read latest checkpoint JSON** → Get exact resume point
4. **Resume from documented position** → No restart needed

### Example: Android Todos App

```
company/project/android-todos-app/
├── PROGRESS.md                           # Layer 1: Current state (Stage 2, 85%, Gate Review)
├── sessions/
│   ├── session-20260401-090000.md        # Stage 1 session log
│   └── session-20260401-143000.md        # Stage 2 session log
└── checkpoints/
    ├── stage1-gate-approved.json         # Stage 1 completion checkpoint
    └── stage2-gate-approved.json         # Stage 2 completion checkpoint
```

**CRITICAL:** Per `company/pipeline/development/monitoring.md`, the checkpoint system uses **ONE file per stage** with a `milestone_history` array for tracking internal milestones. **DO NOT** create multiple checkpoint files per stage (e.g., `stage5-phase1-complete.json`, `stage5-phase2-complete.json` are violations).

---

## Quick Reference Cards

### Pipeline Stage Quick Lookup

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: Requirements                                           │
│ Owner: CPO (PRD) + CSO (SRD)                                    │
│ Output: PRD.md, SRD.md (paired artifacts)                       │
│ Gate: User confirms platform(s) + no further revisions          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: Design                                                 │
│ Owner: CDO                                                      │
│ Output: Prototype (HTML), IDS.md                                │
│ Gate: User gives final confirmation                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: Architecture                                           │
│ Owner: CTO (UML) + CIO (ADRs, TSD)                              │
│ Output: UML diagrams, ADR-001 to ADR-NNN, TSD.md                │
│ Gate: User approves UML Engineering Package                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: Implementation Plan                                    │
│ Owner: CTO                                                      │
│ Output: implementation-plan.md, GANTT.md, SPEC.md               │
│ Gate: User approves the plan                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: Development                                            │
│ Owner: CTO (no user approval needed)                            │
│ Output: Platform codebases (android/, ios/, etc.)               │
│ Gate: CTO internal review only                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: Code Review                                            │
│ Owner: CTO (panel)                                              │
│ Output: DEFECT-REPORT.md, SIGNOFF.md                            │
│ Gate: User reviews Defect Report, decides on P2/P3              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 7: Automated Testing                                      │
│ Owner: CTO + Test Lead                                          │
│ Output: Test suite, TEST-RESULTS-REPORT.md                      │
│ Gate: User decides on P2/P3 defect deferrals                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 8: Integrity Verification                                 │
│ Owner: CTO (panel) (no user approval needed)                    │
│ Output: Panel reports (CPO, CDO, CTO, CIO, CSO, CTO-L)          │
│ Gate: Panel sign-off only                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 9: i18n Engineering                                       │
│ Owner: CTO-L + R&D (no user approval needed)                    │
│ Output: Localized codebase, TRANSLATION-VERIFICATION-REPORT.md  │
│ Gate: CTO-L + CTO sign-off                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 10: Release Readiness                                     │
│ Owner: CTO (panel) + USER                                       │
│ Output: RELEASE-CHECKLIST-7-ITEM.md, Release Decision           │
│ Gate: User issues final release decision                        │
└─────────────────────────────────────────────────────────────────┘
```

---

### Versioning Workflow Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ DOCUMENT LIFECYCLE                                              │
│                                                                 │
│  draft/          →  v{N}/          →  final/                    │
│  (write)         →  (review)        →  (approve)                │
│                                                                 │
│  Mutable         →  Immutable       →  Frozen                   │
│  Not reviewed    →  Gate reviewed   →  Stage approved           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CHECKPOINT FILE LIFECYCLE                                       │
│                                                                 │
│  stage<N>-in-progress.json                                      │
│       ↓ (updated at each milestone)                             │
│  stage<N>-gate-review.json                                      │
│       ↓ (after panel approval)                                  │
│  stage<N>-gate-approved.json                                    │
│                                                                 │
│  ONE file per stage ONLY. Internal milestones in milestone_history array.
└─────────────────────────────────────────────────────────────────┘
```

---

### User Approval Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE TRANSITION          │ USER APPROVAL?                      │
├─────────────────────────────────────────────────────────────────┤
│ Stage 1 → 2               │ ✅ YES                              │
│ Stage 2 → 3               │ ✅ YES                              │
│ Stage 3 → 4               │ ✅ YES                              │
│ Stage 4 → 5               │ ✅ YES                              │
│ Stage 5 → 6               │ ❌ NO (CTO internal only)           │
│ Stage 6 → 7               │ ✅ YES                              │
│ Stage 7 → 8               │ ✅ YES                              │
│ Stage 8 → 9               │ ❌ NO (Panel sign-off only)         │
│ Stage 9 → 10              │ ❌ NO (CTO-L + CTO sign-off)        │
│ Stage 10 (Final)          │ ✅ YES (User release decision)      │
└─────────────────────────────────────────────────────────────────┘

Valid User Responses:
  • "Approve"         → Advance to next stage
  • "Conditional Approve" → Advance with remediation notes
  • "Reject"          → Fix defects before advancing
```

---

### Defect Severity Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL │ DEFINITION                          │ ACTION            │
├─────────────────────────────────────────────────────────────────┤
│  P0   │ App crash / data loss / security    │ 🚫 Non-negotiable │
│       │ breach                              │    fix            │
├─────────────────────────────────────────────────────────────────┤
│  P1   │ Core feature broken / major UX      │ 🚫 Non-negotiable │
│       │ failure                             │    fix            │
├─────────────────────────────────────────────────────────────────┤
│  P2   │ Minor feature degraded / cosmetic   │ 👤 User decides   │
│       │ issue                               │    fix/defer      │
├─────────────────────────────────────────────────────────────────┤
│  P3   │ Polish / nice-to-have               │ 👤 User decides   │
│       │                                     │    fix/defer      │
└─────────────────────────────────────────────────────────────────┘

Note: P0/P1 classification is final. User has explicit authority over P2/P3.
```

---

_End of QWEN.md_
