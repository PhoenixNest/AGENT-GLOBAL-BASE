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

| Goal | Go to |
| --- | --- |
| Understand company structure | `company/library/overview/company.md` |
| Find all agents and their roles | `company/library/overview/personnel.md` |
| Understand the full pipeline | `company/pipeline/development/pipeline.md` |
| Find a specific department | `company/library/departments/<dept>.md` |
| Research architecture, security, testing, or localization | `company/library/topics/` |
| Find an agent profile | `company/departments/<dept>/.../agent/profile.md` |

---

## The 10-Stage Development Pipeline

The pipeline is a **state machine** — each stage has explicit Artifacts In/Out, a Responsible Producer, Gate Criteria, and Defect Handling. Stages must be completed in order; gate criteria must be satisfied before advancing.

| # | Stage | Key Output | Responsible Producer |
| - | ----- | ---------- | -------------------- |
| 1 | Requirements → PRD + SRD | PRD + Security Requirements Document | CPO (PRD), CSO (SRD) |
| 2 | PRD → Web Prototype + IDS | HTML prototype + Interaction Design Specification | CDO |
| 3 | Prototype → UML Engineering Package | UML diagrams + ADRs + TSD | CTO (UML), CIO (ADRs + TSD) |
| 4 | UML → Coding Implementation Plan | Implementation Plan + Gantt Chart | CTO |
| 5 | Plan → Software Development | Development codebase | CTO |
| 6 | Development → Code Review | Defect Report + Code Review Sign-off | CTO (panel) |
| 7 | Code Review → Automated Testing | Test Suite + Test Results Report | CTO + Test Lead |
| 8 | Testing → Integrity Verification | Integrity Verification Sign-off | CTO (panel) |
| 9 | Integrity → i18n Engineering | Localised codebase + Translation Verification Report | CTO-L + R&D |
| 10 | i18n → Release Readiness Check | Release Readiness Report + Release Decision | CTO (panel) + User |

**Key pipeline rules:**

- The PRD and SRD are **paired artifacts** — they travel together through all stages.
- Technology decisions locked at Stage 3 (ADRs/TSD) are **not revisable** in Stage 4+.
- The Progress Sync Protocol activates at Stage 4: any task exceeding estimated duration by >20% triggers a CTO → CPO notification.
- Stage 8 guards against the "trim-to-pass" anti-pattern — functionality removal is never valid remediation.

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. Classification is done before remediation begins.

| Level | Definition | Release Impact |
| ----- | ---------- | -------------- |
| P0 | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1 | Core feature broken / major UX failure | Blocks release — non-negotiable |
| P2 | Minor feature degraded / cosmetic issue | User decides to fix or defer |
| P3 | Polish / nice-to-have | User decides to fix or defer |

P0/P1 classification is final. The user has explicit final authority over P2/P3 defects.

---

## Agent Tier System

| Tier | Description |
| --- | --- |
| **C-suite** | Department supervisors placed before recruitment. Set strategy, own pipeline stage outputs, convene review panels. |
| **Team Supervisors** | Senior leads recruited after C-suite. Own sub-department execution. |
| **Teammates** | Individual contributors. Execute within direction set by supervisors. |

---

## Department → C-Suite Mapping

| Department | Supervisor(s) | Key Pipeline Stages |
| --- | --- | --- |
| Brand Design | CDO (Yuki Tanaka-Chen) | 2, 6, 8, 10 |
| Cyberspace Security | CIO (Dr. Priya Mehta), CSO (Dr. Sarah Chen) | 1, 3, 6, 8, 10 |
| Human Resources | CHRO (Dr. Evelyn Hartwell) | Recruitment only |
| Localization | CTO-L (Dr. Amara Osei-Mensah) | 9, 10 |
| Product Management | CPO (Marcus Tran-Yoshida) | 1, 6, 8, 10 |
| Research & Development | CTO (Dr. Kenji Nakamura) | 3, 4, 5, 6, 7, 8, 10 |

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

| # | Domain | Sign-off Authority |
| - | ------ | ------------------ |
| 1 | Product — all PRD requirements implemented | CPO |
| 2 | Design — all CDO/IDS specifications realised | CDO |
| 3 | Architecture — all UML/ADR/TSD standards upheld | CTO + CIO |
| 4 | Security — SRD enforced, OWASP MASVS compliant | CSO |
| 5 | Testing — 100% automated test pass rate | CTO |
| 6 | Localisation — all target languages complete | CTO-L |
| 7 | Platform — App Store / Google Play requirements met | CTO + CPO |

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
├── agents/                # 20 SubAgent configurations (YAML frontmatter + profiles)
│   ├── chief-technology-officer.md
│   ├── chief-design-officer.md
│   ├── chief-product-officer.md
│   ├── software-architect.md
│   ├── test-lead.md
│   ├── android-development-lead.md
│   ├── ios-development-lead.md
│   ├── cross-platform-development-lead.md
│   └── ... (12 more)
├── workflows/
│   └── pipeline.md        # 10-stage development workflow
└── skills/                # 43 skill files
```

### Quick Reference

| Resource Type | Location | Count |
| ------------- | -------- | ----- |
| SubAgent Configurations | `.qwen/agents/*.md` | 20 |
| Workflow Definition | `.qwen/workflows/pipeline.md` | 1 |
| Skill Files | `.qwen/skills/*.md` | 43 |

### Using Imported Resources

- **To use a SubAgent:** Reference by name (e.g., `chief-technology-officer`) — see `.qwen/README.md` for full list
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

| Directory | Content | Pipeline Stage | Owner |
|-----------|---------|----------------|-------|
| `requirements/` | PRD, SRD, traceability matrix | Stage 1 | CPO + CSO |
| `design/` | Prototype, IDS, design assets, accessibility | Stage 2 | CDO |
| `architecture/` | UML diagrams, ADRs, TSD | Stage 3 | CTO + CIO |
| `technology/` | Vendor evaluations, TCO, risk assessments | Ongoing | CIO |
| `specs/` | Implementation plan, Gantt chart, SPECs | Stage 4 | CTO |
| `progress/` | Weekly summaries, schedule risk alerts | Stage 4/5 | CTO |
| `platforms/` | Platform-specific source code | Stage 5 | Platform Leads |
| `testing/` | Test suite, results, defects | Stage 7 | Test Lead |
| `reviews/` | Code review, integrity verification, release checklist | Stage 6, 8, 10 | CTO Panel |
| `releases/` | Readiness report, platform submission | Stage 10 | CTO + User |
| `security/` | Security audits, compliance, penetration tests | Stage 1, 6, 8, 10 | CSO |
| `docs/` | Shared documentation | All stages | All |

### Naming Principles

| Principle | Example | Rationale |
|-----------|---------|-----------|
| **Semantic naming** | `defects/` not `stage6-defects/` | Folders describe content, not process |
| **Pipeline stages are metadata** | Tracked in document headers, not folder names | Stable structure regardless of pipeline changes |
| **Lowercase only** | `weather-app` not `WeatherApp` | Cross-platform compatibility |
| **Kebab-case** | `implementation-plan/` not `implementation_plan/` | URL-friendly, readable |
| **Paired artifacts visible** | `prd/` and `srd/` as siblings | Enforces PRD-SRD pairing from Stage 1 |

### Key Structural Decisions

1. **No stage prefixes in folder names** — Pipeline stage context belongs in document frontmatter and version control, not directory structure
2. **`platforms/` consolidates all platform code** — Clear separation between production code and artifact directories
3. **`reviews/` groups all gate sign-offs** — Code Review (Stage 6), Integrity Verification (Stage 8), Release Checklist (Stage 10)
4. **`testing/` owns all defect tracking** — Defects span multiple stages; unified location prevents fragmentation
5. **`requirements/` at root level** — PRD and SRD are foundational artifacts that drive all downstream work
