# QWEN.md

This file provides guidance to Qwen Code when working with this repository.

> **Adapter notice.** This file is a Qwen-Code-specific adapter for [`AGENTS.md`](./AGENTS.md). The canonical rules — pipeline stage ownership, defect severity, P0/P1 escalation, and the Progress Sync Protocol — live there. **In case of disagreement, `AGENTS.md` wins** and this adapter is fixed within 24 hours per the Adapter Pattern (`AGENTS.md` § Documentation Strategy). This file MAY add Qwen-specific guidance (`.qwen/` tooling, SubAgent invocation, skill paths, operational conventions); it MUST NOT redefine pipeline rules, defect severity, the roster, or stage ownership.

---

## Development Environment (Asus Zenbook Pro 14 Duo OLED — UX8402VV)

> **Recorded:** April 12, 2026 — Critical for script compatibility and test execution.

### Hardware

| Component             | Specification                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------- |
| **Model**             | Asus Zenbook Pro 14 Duo OLED UX8402VV                                                     |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads (6× P-Cores @ 5.4 GHz, 8× E-Cores @ 4.1 GHz) |
| **GPU**               | NVIDIA GeForce RTX 4060 Laptop — 8 GB GDDR6                                               |
| **RAM**               | 32 GB DDR5                                                                                |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB, expandable)                                                  |
| **Primary Display**   | 14.5" OLED, 16:10, 2880×1800, 120 Hz, Touch, Stylus                                       |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864                                                       |
| **Ports**             | 2× Thunderbolt 4, 1× USB 3.2 Type-A, 1× HDMI, 1× 3.5mm, 1× microSD                        |
| **Networking**        | Wi-Fi 6E (802.11ax), Bluetooth 5.3                                                        |
| **Battery**           | 76 WHrs, 4-cell Li-ion                                                                    |
| **Weight**            | 1.75 kg (3.86 lbs)                                                                        |
| **OS**                | Windows 11 Home Chinese Edition (家庭中文版)                                              |

### Software

| Component         | Path / Version                              | Notes                                                      |
| ----------------- | ------------------------------------------- | ---------------------------------------------------------- |
| **Python**        | `C:\Program Files\Python\313\python.exe`    | Use `python`, NOT `python3`                                |
| **Git Bash**      | `C:\Program Files\Git\bin\bash.exe`         | Available but **not preferred** for hooks                  |
| **Shell**         | `cmd.exe` (primary), PowerShell (secondary) | Git bash has pipe/subprocess issues with Python            |
| **Qwen Code CLI** | Running locally                             | Hooks feature enabled, configured in `.qwen/settings.json` |

### Critical Rules for This Environment

| Rule                                        | Rationale                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Use `python`, not `python3`**             | Windows installation uses `python.exe`; `python3` is a non-functional WindowsApps stub             |
| **No `set -euo pipefail` in shell scripts** | `set -u` breaks on empty bash arrays; `pipefail` causes false exit codes through Python subprocess |
| **Avoid `xxd`, `/dev/urandom` in scripts**  | Not reliably available in Git bash. Use Python's `hashlib` and `random` instead                    |

### Verified Working Configuration

```
Platform: Windows 11
Device: Asus Zenbook Pro 14 Duo OLED (UX8402VV)
CPU: Intel Core i9-13900H (14 cores / 20 threads)
RAM: 32 GB DDR5
GPU: NVIDIA RTX 4060 (8 GB GDDR6)
Python: C:\Program Files\Python\313\python.exe
```

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
│   ├── pipeline/          # Pipeline definitions for Qwen Code agents
│   │   ├── mobile-development/  # 10-stage mobile development workflow + templates
│   │   ├── web-development/     # 10-stage web application workflow
│   │   ├── backend-api/         # 10-stage backend API workflow
│   │   ├── full-stack/          # 10-stage full-stack cross-platform workflow
│   │   └── recruitment/         # 10-stage automated recruitment pipeline (Stage 0 planning + Stages 1-9 execution)
│   ├── agents/            # 77 SubAgent configurations
│   ├── skills/            # 14 skill categories (199 guidelines)
│   └── reference/         # Reference materials
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
        ├── mobile-development/
        │   ├── pipeline.md           # Full 10-stage development pipeline definition
        │   ├── monitoring.md         # Progress Monitoring & Recovery System
        │   └── optimization-history/ # Historical optimization plans
        ├── web-development/          # Web app development (PWA/SPA/SSR)
        │   ├── pipeline.md           # Web application pipeline definition
        │   └── monitoring.md         # Progress Monitoring & Recovery System
        ├── backend-api/              # Backend API service development
        │   ├── pipeline.md           # Backend API pipeline definition
        │   └── monitoring.md         # Progress Monitoring & Recovery System
        ├── full-stack/               # Full-stack cross-platform delivery
        │   ├── pipeline.md           # Full-stack pipeline definition
        │   └── monitoring.md         # Progress Monitoring & Recovery System
        └── recruitment/pipeline.md   # 10-stage automated recruitment pipeline (Stage 0 planning + Stages 1-9 execution) (CHRO-owned)
```

---

## Navigation Quick Reference

| Goal                                                      | Go to                                             |
| --------------------------------------------------------- | ------------------------------------------------- |
| Understand company structure                              | `company/library/overview/company.md`             |
| Find all agents and their roles                           | `company/library/overview/personnel.md`           |
| Understand the full pipeline                              | `company/pipeline/mobile-development/pipeline.md` |
| Understand web development pipeline                       | `company/pipeline/web-development/pipeline.md`    |
| Understand backend API pipeline                           | `company/pipeline/backend-api/pipeline.md`        |
| Understand full-stack cross-platform pipeline             | `company/pipeline/full-stack/pipeline.md`         |
| Understand the recruitment pipeline                       | `company/pipeline/recruitment/pipeline.md`        |
| Find a specific department                                | `company/library/departments/<dept>.md`           |
| Research architecture, security, testing, or localization | `company/library/topics/`                         |
| Find an agent profile                                     | `company/departments/<dept>/.../agent/profile.md` |

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
- **Testing** (`topics/testing.md`): 100% automated test pass rate target; regression testing required on all fixed functionalities; Stage 8 integrity verification guards against the "trim-to-pass" anti-pattern. Stage 7 mandates DAST (OWASP ZAP), penetration testing (MASVS categories), and performance benchmark verification.
- **Localization** (`topics/localization.md`): Stage 9 two-phase process — Phase A: R&D i18n engineering (string extraction into platform resource files, validated via STRING-EXTRACTION-HANDOFF.md); Phase B: Localization Department TMS translation pipeline. Translation quality verified via BLEU/TER scores (≥ 0.80), platform-specific style guides, and the TRANSLATION-VERIFICATION-REPORT.md.

---

## Stage 10 Release Checklist (Reference)

The Stage 10 release checklist is canonical in [`company/pipeline/_base/pipeline.md`](./company/pipeline/_base/pipeline.md) § Stage 10. As of OPT-2026-04-20-001 Step 8 / FIND-P1-04, it now carries **12 rows** — the original seven (Product, Design, Architecture, Security, Testing, Localisation, Platform) plus five new P0 sign-off rows: **Performance Budget** (CTO + VP Platform), **Accessibility WCAG 2.1 AA** (CDO), **Privacy / Data Minimization** (CSO + GC), **Stage 9.5 Dogfood telemetry** (VP Quality), and **Live Ops Readiness** (VP Platform + CSO, referencing [`incident-response.md`](./company/pipeline/_base/incident-response.md)). Do not duplicate the checklist here.

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
3. **Pipeline adherence** — All development work follows the 10-stage pipeline. Do not skip stages or reorder them. The **recruitment pipeline** (`company/pipeline/recruitment/pipeline.md`) is a separate 10-stage automated workflow (Stage 0 planning + Stages 1-9 execution) owned by the CHRO, governing hiring from need identification through 90-day onboarding. It operates independently of the development pipeline.
4. **Defect classification** — Always classify defects using the P0–P3 system before remediation.
5. **Paired artifacts** — The PRD and SRD are always treated as a unit from Stage 1 onward.
6. **Game Studio organizational principle** — The game studio (`studio/`) operates **independently** from the parent company's development pipeline and department structure. Each studio has its own folder under `studio/<studio-name>/` with its own workflow (`studio/<studio-name>/pipeline/`), reference materials (`studio/<studio-name>/library/`), and recruitment plan (`studio/<studio-name>/team/`). The current studio is `studio/casual-games/`. However, each studio **reports directly to and is accountable to** the parent company's Chief Officers (CPO, CTO, CDO, CIO, CSO, CHRO, CTO-L). All studio gate reviews, kill decisions, and release approvals require C-suite panel participation and User (CEO) final sign-off. **No studio document, decision, or artifact should ever be saved outside the `studio/` directory.**

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
├── pipeline/              # Pipeline definitions for Qwen Code agents
│   ├── mobile-development/  # 10-stage mobile development workflow + monitoring + templates
│   │   ├── pipeline.md      # Mobile development workflow (source of truth)
│   │   ├── monitoring.md    # Progress Monitoring & Recovery System
│   │   └── templates/       # 28 pipeline templates organized by stage
│   ├── web-development/     # 10-stage web application workflow
│   │   ├── pipeline.md      # Web app development workflow (PWA/SPA/SSR)
│   │   ├── monitoring.md    # Progress Monitoring & Recovery System
│   │   └── templates/       # 11 pipeline templates organized by stage
│   ├── backend-api/         # 10-stage backend API workflow
│   │   ├── pipeline.md      # API service development workflow (REST/GraphQL/gRPC)
│   │   ├── monitoring.md    # Progress Monitoring & Recovery System
│   │   └── templates/       # 11 pipeline templates organized by stage
│   ├── full-stack/          # 10-stage full-stack cross-platform workflow
│   │   ├── pipeline.md      # Coordinated web + mobile + backend delivery
│   │   ├── monitoring.md    # Progress Monitoring & Recovery System
│   │   └── templates/       # 11 pipeline templates organized by stage
│   └── recruitment/         # 10-stage automated recruitment pipeline (Stage 0 planning + Stages 1-9 execution)
│       └── pipeline.md      # CHRO-owned, unanimous C-Suite sign-off
└── skills/                # 14 Qwen Code Skill categories (199 guidelines)
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

| Resource Type           | Location                                          | Count |
| ----------------------- | ------------------------------------------------- | ----- |
| SubAgent Configurations | `.qwen/agents/*.md`                               | 77    |
| Skill Categories        | `.qwen/skills/*/`                                 | 14    |
| Skill Guidelines        | `.qwen/skills/*/`                                 | 199   |
| Development Pipelines   | `.qwen/pipeline/{mobile,web,backend,full-stack}/` | 4     |
| Recruitment Pipeline    | `.qwen/pipeline/recruitment/pipeline.md`          | 1     |

### Using Imported Resources

- **To use a SubAgent:** Reference by name (e.g., `cto-dr-kenji-nakamura`) — see `.qwen/README.md` for full list
- **To find a skill:** Skills are indexed by category in `.qwen/README.md`
- **To reference the pipeline:**
  - **Mobile Development:** `.qwen/pipeline/mobile-development/pipeline.md` (10 stages, source of truth)
  - **Web Development:** `.qwen/pipeline/web-development/pipeline.md` (PWA/SPA/SSR apps)
  - **Backend API:** `.qwen/pipeline/backend-api/pipeline.md` (REST/GraphQL/gRPC services)
  - **Full-Stack Cross-Platform:** `.qwen/pipeline/full-stack/pipeline.md` (coordinated web + mobile + backend)
  - **Recruitment:** `.qwen/pipeline/recruitment/pipeline.md` (10 stages, CHRO-owned, fully automated with outcome-only review at Stage 8)
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

## Pipeline Enforcement Rules (Reference)

The operational rules that previously lived inline here — project artifact location (`company/project/<project-name>/`), user gate-approval points per stage, the Stage 1 platform selection gate, and panel composition by stage — are all canonical in [`company/pipeline/_base/pipeline.md`](./company/pipeline/_base/pipeline.md) (gate criteria, panel composition) and [`AGENTS.md` § Non-Negotiable Rules](./AGENTS.md) (artifact location, user approval gates). The per-project dashboard index is [`company/project/_dashboard.md`](./company/project/_dashboard.md). **Do not redefine these rules here** — this pointer exists so Qwen/Gemini/Lingma agents land on the same canonical source that every other agent uses.

---

## Lessons Learned (Mistake Log)

> ⚠️ **CRITICAL FAILURES** — These errors represent fundamental breakdowns in pipeline discipline and must NEVER recur.

### Mistake Summary by Severity

| Severity    | Count  | Percentage |
| ----------- | ------ | ---------- |
| 🔴 CRITICAL | 15     | 48%        |
| 🟠 HIGH     | 4      | 13%        |
| 🟡 MEDIUM   | 12     | 40%        |
| **Total**   | **31** | 100%       |

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

**Pipeline applicability:** These rules apply to all development pipelines. Platform-specific team composition varies by pipeline type.

| Rule                                         | Requirement                                                                                                                                                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Responsible Producer**                     | CTO (oversees and tracks development progress)                                                                                                                                                                               |
| **Team Utilization**                         | **MAXIMIZE** — Distribute workload across ALL available platform/specialty leads using parallel construction                                                                                                                 |
|                                              | • Mobile: Android Lead, iOS Lead, Cross-Platform Lead                                                                                                                                                                        |
|                                              | • Web: Frontend Lead, Backend Lead                                                                                                                                                                                           |
|                                              | • Backend API: API Service Lead                                                                                                                                                                                              |
|                                              | • Full-Stack: Coordinated across all relevant platforms                                                                                                                                                                      |
| **User Approval**                            | **NOT REQUIRED** during Stage 5 — CTO has sole responsibility; no gate approvals needed between phases                                                                                                                       |
| **Progress Tracking**                        | Single `DEVELOPMENT-LOG.md` **per platform/service** (e.g., `platforms/android/code/DEVELOPMENT-LOG.md`) — updated upon each phase completion; individual phase reports are redundant and should NOT be created              |
| **Design Fidelity Checkpoint**               | At ~60% completion, the CDO conducts a formal Design Fidelity Checkpoint against the IDS. ≥ 90% pass rate → proceed; 70–89% → proceed with remediation plan; < 70% → STOP, CTO notifies CPO.                                 |
| **String Extraction Readiness**              | Before Stage 6 entry, the Internationalization Specialist audits the codebase for hardcoded strings. Remaining strings classified as P2 defects (P1 if core user flow affected).                                             |
| **Contract Verification** (KMP/Flutter only) | Contract Verification Reports produced at 30% and 70% completion milestones. Blocking issues must be resolved before the next checkpoint.                                                                                    |
| **Completion Criteria**                      | All Coding Implementation Plan tasks marked complete                                                                                                                                                                         |
| **Internal Review**                          | CTO conducts comprehensive internal review (compilation, runtime, bug-free, Design Fidelity Checkpoint completed, String Extraction Readiness completed, Contract Verification Reports produced) BEFORE advancing to Stage 6 |
| **Reporting**                                | CTO reports progress directly to user; CTO conducts secondary review before final report                                                                                                                                     |

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

**Full specification:** See monitoring.md in each pipeline directory:

- Mobile: `company/pipeline/mobile-development/monitoring.md`
- Web: `company/pipeline/web-development/monitoring.md`
- Backend API: `company/pipeline/backend-api/monitoring.md`
- Full-Stack: `company/pipeline/full-stack/monitoring.md`

### System Overview

A three-layer monitoring system providing comprehensive oversight of pipeline progress, enabling rapid state assessment and seamless recovery after interruptions (e.g., power outages, session timeouts, agent handoffs).

**Mandatory for all Stage 4+ projects across all pipeline types.**

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

### Example: Project Monitoring Structure

```markdown
# Mobile Project

company/project/android-todos-app/
├── PROGRESS.md # Layer 1: Current state (Stage 2, 85%, Gate Review)
├── sessions/
│ ├── session-20260401-090000.md # Stage 1 session log
│ └── session-20260401-143000.md # Stage 2 session log
└── checkpoints/
├── stage1-gate-approved.json # Stage 1 completion checkpoint
└── stage2-gate-approved.json # Stage 2 completion checkpoint

# Web Project

company/project/web-dashboard/
├── PROGRESS.md
├── sessions/
└── checkpoints/

# Backend API Project

company/project/user-api-service/
├── PROGRESS.md
├── sessions/
└── checkpoints/

# Full-Stack Project

company/project/ecommerce-platform/
├── PROGRESS.md
├── sessions/
└── checkpoints/
```

**CRITICAL:** Per pipeline monitoring specifications, the checkpoint system uses **ONE file per stage** with a `milestone_history` array for tracking internal milestones. **DO NOT** create multiple checkpoint files per stage (e.g., `stage5-phase1-complete.json`, `stage5-phase2-complete.json` are violations).

---

## Quick Reference Cards

### Pipeline Stage Quick Lookup

**Note:** These 10 stages apply across all 4 development pipelines (Mobile, Web, Backend API, Full-Stack). Platform-specific outputs vary by pipeline type.

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
│ Output: Platform codebases                                      │
│   • Mobile: android/, ios/, flutter/, kmp/                      │
│   • Web: frontend/, backend/                                    │
│   • Backend API: api-service/                                   │
│   • Full-Stack: coordinated across platforms                    │
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

See [`AGENTS.md` § Defect Severity](./AGENTS.md) for the canonical P0–P3 table. Operational triage lives in [`_base/pipeline.md`](./company/pipeline/_base/pipeline.md) Stages 6/7/8. P0/P1 classification is final; user has explicit authority over P2/P3.

---

## Document Version History

| Version | Date           | Author            | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | April 20, 2026 | Tech Writer       | Initial adapter file authored with platform tooling guidance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 2.0     | April 21, 2026 | Tech Writer + CTO | **Adapter Pattern conformance** (per `AGENTS.md` § Documentation Strategy, OPT-2026-04-20-001 Step 19 / FIND-P2-15). Added the canonical adapter notice header. Converted five sections that previously redefined canonical rules into "see canonical" pointer paragraphs: (a) 10-Stage Pipeline table → `_base/pipeline.md` (now Stage 0 → 11, Stage 6/9 renamed, ADRs versionable per Step 14); (b) Defect Severity P0–P3 table → `AGENTS.md`; (c) Department → C-Suite mapping → `AGENTS.md` Quick Roster + `personnel.md`; (d) Stage 10 release checklist → `_base/pipeline.md` § Stage 10 (now 12 rows per Step 8 / FIND-P1-04); (e) Critical Pipeline Enforcement Rules → `_base/pipeline.md` + `AGENTS.md`. ALL other content preserved verbatim — Core Operating Principle, Repository Structure, Navigation, Agent Tier System, Cross-Cutting Topics, Imported Resources (`.qwen/` directory tree), Project Directory Structure, Key Conventions, Lessons Learned / Mistake Log, Document Naming Conventions, Document Versioning, Progress Monitoring & Recovery System, and Quick Reference Cards. Per user feedback on this optimization plan closeout: preserve platform-specific operational content; strip only forbidden rule-redefinition tables. |
