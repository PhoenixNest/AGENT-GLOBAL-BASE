# LINGMA.md

This file provides guidance to **Lingma (通义灵码)** — Alibaba's AI coding assistant — when working with this repository.

---

## Repository Purpose

This is an **agent knowledge base** — not a software project. It defines a simulated mobile product company composed of named AI agent personas, each with a role, tier, skills, and pipeline stage ownership. There are no build commands, tests, or code to run.

The repo has three primary functions:

1. **Company Library** (`company/library/`) — Reference documentation for navigating the company's structure, personnel, pipeline, and cross-cutting topics.
2. **Agent Profiles & Skills** (`.lingma/agents/` and `.lingma/skills/`) — 77 SubAgent definitions and 199 skill files used to instruct Lingma how to behave when embodying a given agent or applying specialized expertise.
3. **Pipeline Definition** (`company/pipeline/`) — The authoritative 10-stage development workflow state machine.

---

## Development Environment (Asus Zenbook Pro 14 Duo OLED — UX8402VV)

> **Recorded:** April 15, 2026 — Critical for script compatibility and tool execution.

### Hardware

| Component             | Specification                                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Model**             | Asus Zenbook Pro 14 Duo OLED UX8402VV                                                                                              |
| **Category**          | Dual-screen creator laptop                                                                                                         |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads (6× P-Cores @ 5.4 GHz, 8× E-Cores @ 4.1 GHz)                                          |
| **GPU**               | NVIDIA GeForce RTX 4060 Laptop — 8 GB GDDR6 VRAM                                                                                   |
| **RAM**               | 32 GB DDR5                                                                                                                         |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB base, expandable via M.2 2280 slot)                                                                    |
| **Primary Display**   | 14.5" OLED, 16:10, 2880×1800 (234 PPI), 120 Hz, 0.2ms, 550 nits HDR, 100% DCI-P3, PANTONE Validated, Glossy, Touch, Stylus support |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864, Glossy, Stylus support                                                                        |
| **I/O Ports**         | 2× Thunderbolt 4 (USB-C), 1× USB 3.2 Gen 2 Type-A, 1× HDMI, 1× 3.5mm Combo Audio Jack, 1× DC-in (ø6.0), 1× microSD Card Reader     |
| **Networking**        | Wi-Fi 6E (802.11ax, 2×2, 6 GHz), Bluetooth 5.3                                                                                     |
| **OS**                | Windows 11 Home Chinese Edition (家庭中文版)                                                                                       |

### Software

| Tool     | Path                                        | Notes                                   |
| -------- | ------------------------------------------- | --------------------------------------- |
| Python   | `C:\Program Files\Python\313\python.exe`    | Use `python`, NOT `python3`             |
| Git Bash | `C:\Program Files\Git\bin\bash.exe`         | Available but not preferred for scripts |
| Shell    | `cmd.exe` (primary), PowerShell (secondary) | Native Windows shells work best         |

---

## Repository Structure

```
.lingma/                    ← Lingma-specific configurations
├── agents/                 ← 77 SubAgent configurations
│   ├── C-Suite (7)
│   ├── VP Engineering (4)
│   ├── R&D Supervisors (5)
│   ├── R&D Leads & Architects (7)
│   ├── R&D Engineers (39)
│   ├── Security (6)
│   ├── HR (1)
│   ├── Localization (7)
│   └── Brand Design (1)
├── skills/                 ← 199 skill guidelines across 14 categories
│   ├── architecture/       (21 skills)
│   ├── product-management/ (3 skills)
│   ├── design/             (8 skills)
│   ├── security/           (25 skills)
│   ├── hr-recruiting/      (9 skills)
│   ├── localization/       (8 skills)
│   ├── android/            (13 skills)
│   ├── ios/                (16 skills)
│   ├── cross-platform/     (6 skills)
│   ├── frontend-web/       (20 skills)
│   ├── backend/            (21 skills)
│   ├── testing-qa/         (21 skills)
│   ├── devops/             (21 skills)
│   └── shared/             (7 skills)
├── pipeline/               ← Pipeline definitions
│   ├── mobile-development/ (10 stages, 28 templates)
│   ├── web-development/    (10 stages, 11 templates)
│   ├── backend-api/        (10 stages, 11 templates)
│   ├── full-stack/         (10 stages, 11 templates)
│   └── recruitment/        (10 stages, CHRO-owned)
├── library/                ← Reference materials
├── reference/              ← Environment and mistake logs
└── README.md               ← Detailed index

company/                    ← Company knowledge base
├── departments/            ← Agent source profiles and skills
├── library/                ← Central knowledge hub
├── pipeline/               ← Pipeline templates and monitoring
└── project/                ← Project-specific artifacts

studio/                     ← Studio-specific content
└── casual-games/           ← First independent studio (Casual mini-games, Unity 6.3 LTS)
```

---

## How to Use Lingma with This Repository

### Using SubAgents (77 Total)

**Method 1: Automatic Trigger**  
Describe your task naturally, and Lingma will select the appropriate agent:

```
Help me review the PRD for this mobile app
```

**Method 2: Manual Trigger**  
Use `/agent-name` to invoke a specific agent:

```
/chief-product-officer
/cto-dr-kenji-nakamura
/android-lead-kofi-asante-mensah
```

### Key Agents by Role

#### C-Suite (7)

- `/cpo-marcus-tran-yoshida` — Product strategy, PRD authorship (Stages 1, 6, 8, 10)
- `/cto-dr-kenji-nakamura` — Architecture, SPEC, UML, tech evaluation (Stages 3-8, 10)
- `/cdo-yuki-tanaka-chen` — Design systems, IDS, prototyping (Stages 2, 6, 8, 10)
- `/cio-dr-priya-mehta` — Technology selection, architecture strategy (Stages 3, 6, 8, 10)
- `/cso-dr-sarah-chen` — Security architecture, risk assessment (Stages 1, 6, 8, 10)
- `/chro-dr-evelyn-hartwell` — Recruitment, candidate vetting
- `/cto-l-dr-amara-osei-mensah` — Localization, translation module (Stages 9, 10)

#### R&D Leads (5)

- `/software-architect-rafael-okonkwo` — UML, ADRs, architecture patterns (Stages 3, 6, 8)
- `/test-lead-priscilla-oduya` — Test automation, defect triage (Stages 7, 8)
- `/android-lead-kofi-asante-mensah` — Android implementation (Stages 5, 8)
- `/ios-lead-seo-yeon-park` — iOS implementation (Stages 5, 8)
- `/cross-platform-lead-mei-ling-johansson` — KMP, Flutter (Stages 5, 8)

### Using Skills (199 Total)

**Method 1: Automatic Trigger**  
Describe your requirement, and Lingma will apply the relevant skill:

```
Help me write a PRD document for a mobile product
```

**Method 2: Manual Trigger**  
Input `/skill-name` to manually trigger:

```
/prd-authorship
/android-implementation
/architecture-decision-records
```

### Key Skills by Category

#### Architecture & Design (32 skills)

- `/spec-development` — Technical specification authorship
- `/software-architecture-design` — UML modeling and system design
- `/architecture-decision-records` — ADR authorship
- `/uml-engineering-package` — UML diagrams (PlantUML/Mermaid)
- `/mobile-design-systems` — Platform-specific design systems
- `/interaction-design-specification` — IDS authorship
- `/web-prototype-development` — Interactive HTML prototypes

#### Mobile Implementation (35 skills)

- `/android-implementation` — Jetpack Compose, MVVM, Kotlin Coroutines
- `/ios-implementation` — SwiftUI, Swift Concurrency, MVVM
- `/kmp-implementation` — Kotlin Multiplatform shared modules
- `/flutter-implementation` — Flutter application development

#### Backend & Web (41 skills)

- `/backend` — Go, Python/FastAPI, PostgreSQL, GraphQL
- `/frontend-web` — React, Vue, Angular, SSR/Next.js
- `/api-gateway-design` — API gateway patterns
- `/distributed-systems` — Microservices, event sourcing

#### Security (25 skills)

- `/mobile-security-architecture` — Platform security design
- `/application-security-hardening` — Code obfuscation, anti-tampering
- `/security-risk-assessment` — Threat modeling, compliance
- `/owasp-masvs-compliance` — MASVS auditing

#### Testing & QA (21 skills)

- `/automated-test-suite` — Test pyramid for iOS/Android
- `/defect-triage-and-classification` — P0-P3 classification
- `/mobile-test-automation` — Espresso, XCTest, Maestro, Appium

#### Localization (8 skills)

- `/language-translation-module` — Translation workflow governance
- `/mobile-ui-translation` — UI string translation (multi-language)
- `/string-extraction-and-resource-files` — Platform resource generation

#### Product & Strategy (3 skills)

- `/mobile-product-strategy` — Roadmap, prioritization, OKRs
- `/prd-authorship` — PRD writing with platform constraints

#### Recruitment (7 skills)

- `/vet-candidate` — Elite candidate vetting gate
- `/recruit-engineering` — Engineering role recruitment
- `/recruit-product` — Product role recruitment

---

## 10-Stage Development Pipeline

The company follows a structured 10-stage development workflow:

| #   | Stage                  | Key Output                  | Responsible          | User Approval? |
| --- | ---------------------- | --------------------------- | -------------------- | -------------- |
| 1   | Requirements           | PRD + SRD                   | CPO, CSO             | ✅ YES         |
| 2   | Prototype              | Web Prototype + IDS         | CDO                  | ✅ YES         |
| 3   | UML Engineering        | UML Package + ADRs + TSD    | CTO, CIO             | ✅ YES         |
| 4   | Implementation Plan    | Plan + Gantt Chart          | CTO                  | ✅ YES         |
| 5   | Development            | Development codebase        | CTO + Platform Leads | ❌ NO          |
| 6   | Code Review            | Defect Report + Sign-off    | CTO (panel)          | ✅ YES         |
| 7   | Automated Testing      | Test Suite + Results        | CTO + Test Lead      | ✅ YES         |
| 8   | Integrity Verification | Integrity Sign-off          | CTO (panel)          | ❌ NO          |
| 9   | i18n Engineering       | Localised codebase + Report | CTO-L + R&D          | ❌ NO          |
| 10  | Release Readiness      | Release Report + Decision   | CTO (panel) + User   | ✅ YES (Final) |

### Pipeline Types

- **Mobile Development** — iOS/Android native apps (`.lingma/pipeline/mobile-development/`)
- **Web Development** — PWA/SPA/SSR applications (`.lingma/pipeline/web-development/`)
- **Backend API** — REST/GraphQL/gRPC services (`.lingma/pipeline/backend-api/`)
- **Full-Stack** — Coordinated web + mobile + backend (`.lingma/pipeline/full-stack/`)
- **Recruitment** — Automated hiring pipeline (`.lingma/pipeline/recruitment/`)

---

## Non-Negotiable Rules

1. **Pipeline stages are sequential** — gate criteria must be satisfied before advancing
2. **PRD + SRD are paired** — they travel together through all stages
3. **Technology decisions lock at Stage 3** — ADRs/TSD from Stage 3 are not revisable in Stage 4+
4. **P0/P1 defects are non-negotiable release blockers** — cannot be overridden by anyone
5. **The user has final authority over P2/P3** — always present these for user decision
6. **"Trim-to-pass" anti-pattern** — functionality removal is never valid remediation
7. **Progress Sync Protocol** — any task >20% over estimate triggers CTO → CPO notification (Stage 4+)

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. All defects must be classified before remediation:

| Level | Definition                             | Action             |
| ----- | -------------------------------------- | ------------------ |
| P0    | Crash / data loss / security breach    | Non-negotiable fix |
| P1    | Core feature broken / major UX failure | Non-negotiable fix |
| P2    | Minor degradation / cosmetic           | User decides       |
| P3    | Polish / nice-to-have                  | User decides       |

---

## Navigation Quick Reference

### Start Here

- **Company Overview:** `company/library/overview/company.md`
- **Personnel Directory:** `company/library/overview/personnel.md`
- **Pipeline Guide:** `company/library/overview/pipeline.md`
- **Lingma Index:** `.lingma/README.md`

### By Department

- **Engineering:** `company/library/departments/research-develop.md`
- **Security:** `company/library/departments/cyberspace-security.md`
- **Product:** `company/library/departments/product-management.md`
- **Design:** `company/library/departments/brand-design.md`
- **Localization:** `company/library/departments/localization.md`
- **HR:** `company/library/departments/human-resources.md`

### By Topic

- **Architecture:** `company/library/topics/architecture.md`
- **Security:** `company/library/topics/security.md`
- **Testing:** `company/library/topics/testing.md`
- **Localization:** `company/library/topics/localization.md`
- **Monitoring:** `company/library/topics/monitoring.md`

---

## Common Workflows

### Workflow 1: Start a New Mobile Product (Stage 1)

```
I want to create a new mobile app - it's a fitness tracker
```

Lingma will engage:

- `/cpo-marcus-tran-yoshida` for PRD creation
- `/cso-dr-sarah-chen` for SRD creation
- Skills: `/mobile-product-strategy`, `/prd-authorship`, `/security-risk-assessment`

### Workflow 2: Design Phase (Stage 2)

```
/cdo-yuki-tanaka-chen Create interaction design prototypes based on the PRD
```

Or use the skill directly:

```
/web-prototype-development
/interaction-design-specification
```

### Workflow 3: Architecture Phase (Stage 3)

```
/cto-dr-kenji-nakamura Create UML engineering package and architecture documentation
```

Skills involved:

- `/uml-engineering-package`
- `/architecture-decision-records`
- `/software-architecture-design`

### Workflow 4: Android Development (Stage 5)

```
/android-lead-kofi-asante-mensah Implement the authentication screen
```

Skills applied:

- `/android-implementation`
- `/jetpack-compose`
- `/android-security`

### Workflow 5: Code Review (Stage 6)

```
/test-lead-priscilla-oduya Perform defect review on the code
```

This engages:

- `/test-lead-priscilla-oduya` for defect triage
- `/defect-triage-and-classification` skill for P0-P3 classification

### Workflow 6: Localization (Stage 9)

```
/cto-l-dr-amara-osei-mensah Translate the app to Chinese and Japanese
```

Skills involved:

- `/language-translation-module`
- `/mobile-ui-translation-chinese`
- `/mobile-ui-translation-japanese`
- `/string-extraction-and-resource-files`

---

## File Format Reference

### Agent Format (`.lingma/agents/*.md`)

```markdown
---
name: agent-identifier
description: Brief description of when to use this agent
tools:
  - read_file
  - write_file
  - read_many_files
  - run_shell_command
---

# Agent Name

## Title

Role title

## Background

...

## Core Strengths

...

## Pipeline Stages Owned

Stage X, Y, Z
```

### Skill Format (`.lingma/skills/{category}/SKILL.md`)

```markdown
---
name: skill-name
description: When and how to use this skill
---

# Skill Name

## Overview

...

## Sub-Guidelines

...
```

---

## Critical Environment Rules

| Rule                                       | Rationale                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| **All scripts MUST be Python (`.py`)**     | Shell scripts (`.sh`) fail on Windows due to Git bash + Python subprocess pipe issues  |
| **Use `python`, not `python3`**            | Windows installation uses `python.exe`; `python3` is a non-functional WindowsApps stub |
| **Avoid `xxd`, `/dev/urandom` in scripts** | Not reliably available in Git bash. Use Python's `hashlib` and `random` instead        |
| **Test runner must be Python-based**       | Batch files have ERRORLEVEL capture issues with pipes. Use Python test runners         |

---

## Lingma Configuration Support

### Official Configuration Files

Lingma IDE supports the following project-level configuration mechanisms:

#### 1. Custom Agents (`.lingma/agents/`)

- **Location:** `${project}/.lingma/agents/<agentName>.md`
- **Format:** Markdown with YAML frontmatter
- **Fields:** `name`, `description`, `tools`
- **Trigger:** Automatic (by description) or manual (`/agent-name`)
- **Documentation:** [Custom Agent Guide](https://help.aliyun.com/zh/lingma/user-guide/custom-agent)

#### 2. Custom Commands (`.lingma/commands/`)

- **Location:** `${project}/.lingma/commands/`
- **Purpose:** Reusable prompts and workflows
- **Trigger:** Manual (`/command-name`)
- **Scope:** Project-level (shared via Git)
- **Documentation:** [Custom Commands Guide](https://help.aliyun.com/zh/lingma/user-guide/custom-commands)

#### 3. Skills (`.lingma/skills/`)

- **Location:** `${project}/.lingma/skills/{category}/SKILL.md`
- **Purpose:** Specialized expertise and implementation guidelines
- **Trigger:** Automatic (by intent) or manual (`/skill-name`)
- **Format:** Markdown with YAML frontmatter

### About LINGMA.md

**This File's Status:**

- ✅ **Human-readable documentation** for project navigation
- ✅ **Follows industry convention** (similar to QWEN.md, CLAUDE.md)
- ⚠️ **Not officially documented** as auto-read by Lingma IDE
- 💡 **Recommended to keep** for team reference and consistency

**Why Keep This File:**

1. Provides comprehensive project overview for developers
2. Maintains consistency with existing QWEN.md and CLAUDE.md
3. Serves as quick reference for all 77 agents and 199 skills
4. Documents environment specifications and critical rules
5. May be supported in future Lingma updates

---

## Summary Statistics

| Resource                | Count | Location                        |
| ----------------------- | ----- | ------------------------------- |
| SubAgent Configurations | 77    | `.lingma/agents/`               |
| Skill Guidelines        | 199   | `.lingma/skills/`               |
| Development Pipelines   | 4     | `.lingma/pipeline/`             |
| Recruitment Pipeline    | 1     | `.lingma/pipeline/`             |
| Pipeline Templates      | 61+   | `.lingma/pipeline/*/templates/` |

---

## References

- **Lingma Documentation:** `.lingma/README.md`
- **Company Library:** `company/library/README.md`
- **Company Pipeline:** `company/pipeline/README.md`
- **Environment Specs:** `.lingma/reference/environment.md`
- **Mistakes Log:** `.lingma/reference/mistakes-log.md`
- **Lingma Custom Agents:** https://help.aliyun.com/zh/lingma/user-guide/custom-agent
- **Lingma Skills:** https://help.aliyun.com/zh/lingma/user-guide/skills
- **Lingma Product Overview:** https://help.aliyun.com/zh/lingma/product-overview/introduction-of-lingma

---

**Last Updated:** April 15, 2026  
**Maintained By:** Lingma AI Assistant
