# .lingma/ Directory Index

This directory contains the company's SubAgent configurations and skills for **Lingma (通义灵码)** - Alibaba's AI coding assistant.

---

## Quick Start

### Using SubAgents

**Method 1: Automatic Trigger**
Describe your task in natural language, and Lingma will automatically select the appropriate agent based on the description:

```
Help me review the PRD for this mobile app
```

**Method 2: Manual Trigger**
Use `/agent-name` to manually invoke a specific agent:

```
/chief-product-officer
```

### Using Skills

**Method 1: Automatic Trigger**
Directly describe your requirement, the model will automatically determine if a skill should be used:

```
Help me write a PRD document for a mobile product
```

**Method 2: Manual Trigger**
Input `/skill-name` to manually trigger:

```
/prd-authorship
```

---

## Directory Structure

```
.lingma/
├── agents/                    # SubAgent configurations (20 agents)
│   ├── C-Suite (7 files)
│   ├── R&D Supervisors (5 files)
│   └── Teammates (8 files)
├── skills/                    # Skill files (43 total)
│   ├── architecture-design/   # 11 skills
│   ├── implementation/        # 4 skills
│   ├── security/              # 4 skills
│   ├── product-strategy/      # 7 skills
│   ├── testing-quality/       # 2 skills
│   ├── localization-i18n/     # 8 skills
│   └── recruitment/           # 7 skills
└── README.md                  # This file
```

---

## SubAgent Roster

### C-Suite Supervisors (7)

| Agent | File | Pipeline Stages |
|-------|------|-----------------|
| Chief Technology Officer | `chief-technology-officer.md` | 3, 4, 5, 6, 7, 8, 10 |
| Chief Design Officer | `chief-design-officer.md` | 2, 6, 8, 10 |
| Chief Product Officer | `chief-product-officer.md` | 1, 6, 8, 10 |
| Chief Information Officer | `chief-information-officer.md` | 3, 6, 8, 10 |
| Chief Security Officer | `chief-security-officer.md` | 1, 6, 8, 10 |
| Chief Human Resources Officer | `chief-human-resources-officer.md` | Recruitment only |
| Chief Translation Officer | `chief-translation-officer.md` | 9, 10 |

### R&D Team Supervisors (5)

| Agent | File | Pipeline Stages |
|-------|------|-----------------|
| Software Architect | `software-architect.md` | 3, 6, 8 |
| Test Lead | `test-lead.md` | 7, 8 |
| Android Development Lead | `android-development-lead.md` | 5, 8 |
| iOS Development Lead | `ios-development-lead.md` | 5, 8 |
| Cross-Platform Development Lead | `cross-platform-development-lead.md` | 5, 8 |

### Teammates (8)

| Agent | File | Pipeline Stages |
|-------|------|-----------------|
| Product UI/UX Prototyper | `product-ui-ux-prototyper.md` | 2 |
| Internationalization Specialist | `internationalization-specialist.md` | 9 |
| English Linguist | `english-linguist.md` | 9 |
| Chinese Linguist | `chinese-linguist.md` | 9 |
| Japanese Linguist | `japanese-linguist.md` | 9 |
| Korean Linguist | `korean-linguist.md` | 9 |
| French Linguist | `french-linguist.md` | 9 |
| Localization Engineer | `localization-engineer.md` | 9 |

---

## Skills Index

### Architecture and Design (11)

| Skill | Description |
|-------|-------------|
| `uml-engineering-package` | UML Engineering Package production |
| `mobile-architecture-patterns` | Cross-platform mobile architecture |
| `architecture-decision-records` | ADR authorship |
| `software-architecture-design` | Software architecture design with UML |
| `mobile-architecture-strategy` | Mobile-native infrastructure strategy |
| `mobile-design-systems` | Mobile design system creation |
| `interaction-design-specification` | IDS authorship |
| `design-to-engineering-handoff` | Design-engineering handoff documentation |
| `user-research-driven-design` | Research-backed design decisions |
| `web-prototype-development` | Interactive web prototype development |

### Implementation (4)

| Skill | Description |
|-------|-------------|
| `android-implementation` | Android: Jetpack Compose, MVVM, Kotlin Coroutines |
| `ios-implementation` | iOS: SwiftUI, Swift Concurrency, MVVM |
| `kmp-implementation` | Kotlin Multiplatform implementation |
| `flutter-implementation` | Flutter application development |

### Security (4)

| Skill | Description |
|-------|-------------|
| `mobile-security-architecture` | Mobile platform security architecture |
| `application-security-hardening` | Application security hardening |
| `security-risk-assessment` | Security risk assessment |
| `emerging-threat-evaluation` | Emerging technology security evaluation |

### Product and Strategy (7)

| Skill | Description |
|-------|-------------|
| `mobile-product-strategy` | Mobile product strategy and roadmap |
| `prd-authorship` | PRD authorship with platform constraints |
| `mobile-technology-strategy` | Mobile technology strategy |
| `technology-evaluation` | Emerging technology evaluation |
| `technical-selection-documentation` | Technical selection documents |
| `spec-development` | SPEC development and technical specification |
| `technical-project-management` | Technical project management |

### Testing and Quality (2)

| Skill | Description |
|-------|-------------|
| `automated-test-suite` | Automated test suite design for iOS/Android |
| `defect-triage-and-classification` | P0-P3 defect classification |

### Localization and i18n (8)

| Skill | Description |
|-------|-------------|
| `language-translation-module` | Language Translation Module governance |
| `mobile-ui-translation` | Mobile UI string translation (general) |
| `mobile-ui-translation-chinese` | Mobile UI string translation (Chinese) |
| `mobile-ui-translation-japanese` | Mobile UI string translation (Japanese) |
| `mobile-ui-translation-korean` | Mobile UI string translation (Korean) |
| `mobile-ui-translation-english` | Mobile UI string translation (English QA) |
| `string-extraction-and-resource-files` | Mobile string extraction |
| `localization-pipeline-engineering` | Localization pipeline and TMS integration |

### Recruitment (HR) (7)

| Skill | Description |
|-------|-------------|
| `vet-candidate` | Elite candidate vetting gate |
| `recruit-engineering` | Engineering role family recruitment |
| `recruit-product` | Product role family recruitment |
| `recruit-design` | Design role family recruitment |
| `recruit-data` | Data and ML role family recruitment |
| `recruit-translation` | Translation role family recruitment |
| `recruit-business` | Business role family recruitment |

---

## 10-Stage Development Pipeline

The company follows a structured 10-stage development workflow:

| # | Stage | Key Output | Responsible | User Approval? |
|---|-------|------------|-------------|----------------|
| 1 | Requirements → PRD + SRD | PRD + Security Requirements | CPO, CSO | ✅ YES |
| 2 | PRD → Web Prototype + IDS | HTML prototype + IDS | CDO | ✅ YES |
| 3 | Prototype → UML Package | UML + ADRs + TSD | CTO, CIO | ✅ YES |
| 4 | UML → Implementation Plan | Plan + Gantt Chart | CTO | ✅ YES |
| 5 | Plan → Development | Development codebase | CTO | ❌ NO |
| 6 | Development → Code Review | Defect Report + Sign-off | CTO (panel) | ✅ YES |
| 7 | Code Review → Testing | Test Suite + Results | CTO + Test Lead | ✅ YES |
| 8 | Testing → Integrity Verification | Integrity Sign-off | CTO (panel) | ❌ NO |
| 9 | Integrity → i18n Engineering | Localised codebase + Report | CTO-L + R&D | ❌ NO |
| 10 | i18n → Release Readiness | Release Report + Decision | CTO (panel) + User | ✅ YES (Final) |

---

## Non-Negotiable Rules

1. **Pipeline stages are sequential** — gate criteria must be satisfied before advancing
2. **PRD + SRD are paired** — they travel together through all stages
3. **Technology decisions lock at Stage 3** — ADRs/TSD from Stage 3 are not revisable in Stage 4+
4. **P0/P1 defects are non-negotiable release blockers** — cannot be overridden
5. **The user has final authority over P2/P3** — always present these for user decision
6. **"Trim-to-pass" anti-pattern** — functionality removal is never valid remediation
7. **Progress Sync Protocol** — any task >20% over estimate triggers CTO → CPO notification (Stage 4+)

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. All defects must be classified before remediation:

| Level | Definition | Action |
|-------|------------|--------|
| P0 | Crash / data loss / security breach | Non-negotiable fix |
| P1 | Core feature broken / major UX failure | Non-negotiable fix |
| P2 | Minor degradation / cosmetic | User decides |
| P3 | Polish / nice-to-have | User decides |

---

## Usage Examples

### Example 1: Start a New Project (Stage 1)

```
I want to create a new mobile app product - it's a fitness tracker
```

Lingma will automatically engage:

- `chief-product-officer` (Marcus) for PRD creation
- `chief-security-officer` (Dr. Chen) for SRD creation

### Example 2: Design Phase (Stage 2)

```
/chief-design-officer Create interaction design prototypes based on the PRD
```

Or use the skill directly:

```
/web-prototype-development
```

### Example 3: Architecture Phase (Stage 3)

```
/chief-technology-officer Create UML engineering package and architecture documentation
```

Skills involved:

- `uml-engineering-package`
- `architecture-decision-records`
- `software-architecture-design`

### Example 4: Code Review (Stage 6)

```
/test-lead Perform defect review on the code
```

This will engage:

- `test-lead` (Priscilla) for defect triage
- `defect-triage-and-classification` skill for P0-P3 classification

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

### Skill Format (`.lingma/skills/{skill-name}/SKILL.md`)

```markdown
---
name: skill-name
description: When and how to use this skill
---

# Skill Name

## Purpose
...

## When to Use
...

## Execution Guidance
...
```

---

## References

- [Lingma Custom Agents Documentation](https://help.aliyun.com/zh/lingma/user-guide/custom-agent)
- [Lingma Skills Documentation](https://help.aliyun.com/zh/lingma/user-guide/skills)
- [Lingma Product Overview](https://help.aliyun.com/zh/lingma/product-overview/introduction-of-lingma)
- Company Pipeline: `company/pipeline/development/pipeline.md`
- Company Library: `company/library/README.md`
