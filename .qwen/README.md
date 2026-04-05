# .qwen/ Directory Index

This directory contains the company's SubAgent configurations, skills, and workflow definitions for the mobile product development pipeline.

---

## Directory Structure

```
.qwen/
├── README.md                    # This index file
├── agents/                      # Qwen SubAgent configurations (20 agents)
│   ├── C-Suite (7 files)
│   ├── R&D Supervisors (5 files)
│   └── Teammates (8 files)
├── workflows/                   # Pipeline definitions
│   └── pipeline.md              # 10-stage development workflow
└── skills/                      # Skill files (43 total)
    ├── architecture-design/     # 11 files
    ├── implementation/          # 4 files
    ├── security/                # 4 files
    ├── product-strategy/        # 7 files
    ├── testing-quality/         # 2 files
    ├── localization-i18n/       # 8 files
    └── recruitment/             # 7 files
```

---

## SubAgent Configurations

All 20 company personnel are configured as Qwen SubAgents in the `agents/` directory. Each SubAgent file contains:

- **YAML frontmatter** with `name`, `description`, and `tools` array
- **Full agent profile** with background, strengths, gaps, and operating mode
- **Skills index** linking to relevant skill files
- **Pipeline stages owned** for workflow reference

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

## Workflow Definition

| File | Description |
|------|-------------|
| `workflows/pipeline.md` | Ten-stage development pipeline: Requirements → PRD/SRD → Prototype → UML → Implementation Plan → Development → Code Review → Testing → Integrity Verification → i18n → Release |

### Pipeline Stage Summary

| # | Stage | Key Output | Responsible |
|---|-------|------------|-------------|
| 1 | Requirements | PRD + SRD | CPO, CSO |
| 2 | Prototype | Web Prototype + IDS | CDO |
| 3 | UML Engineering | UML Package + ADRs + TSD | CTO, CIO |
| 4 | Implementation Plan | Plan + Gantt Chart | CTO |
| 5 | Development | Development Codebase | CTO + Platform Leads |
| 6 | Code Review | Defect Report + Sign-off | CTO (panel) |
| 7 | Automated Testing | Test Suite + Results | CTO + Test Lead |
| 8 | Integrity Verification | Integrity Sign-off | CTO (panel) |
| 9 | i18n Engineering | Localised Codebase + Translation Report | CTO-L + R&D |
| 10 | Release Readiness | Release Report + Decision | CTO (panel) + User |

---

## Skills Index

### Architecture and Design (12)

| Skill File | Description |
|------------|-------------|
| `uml-engineering-package.md` | UML Engineering Package production |
| `mobile-architecture-patterns.md` | Cross-platform mobile architecture |
| `architecture-decision-records.md` | ADR authorship |
| `software-architecture-design.md` | Software architecture design with UML |
| `mobile-architecture-strategy.md` | Mobile-native infrastructure strategy |
| `mobile-design-systems.md` | Mobile design system creation |
| `interaction-design-specification.md` | IDS authorship |
| `interaction-design-specification-cdo.md` | CDO-specific IDS authorship: component specs, state diagrams, gesture vocabularies, edge case matrices |
| `design-to-engineering-handoff.md` | Design-engineering handoff documentation |
| `user-research-driven-design.md` | Research-backed design decisions |
| `web-prototype-development.md` | Interactive web prototype development |

### Implementation (4)

| Skill File | Description |
|------------|-------------|
| `android-implementation.md` | Android: Jetpack Compose, MVVM, Kotlin Coroutines |
| `ios-implementation.md` | iOS: SwiftUI, Swift Concurrency, MVVM |
| `kmp-implementation.md` | Kotlin Multiplatform implementation |
| `flutter-implementation.md` | Flutter application development |

### Security (4)

| Skill File | Description |
|------------|-------------|
| `mobile-security-architecture.md` | Mobile platform security architecture |
| `application-security-hardening.md` | Application security hardening |
| `security-risk-assessment.md` | Security risk assessment |
| `emerging-threat-evaluation.md` | Emerging technology security evaluation |

### Product and Strategy (7)

| Skill File | Description |
|------------|-------------|
| `mobile-product-strategy.md` | Mobile product strategy and roadmap |
| `prd-authorship.md` | PRD authorship with platform constraints |
| `mobile-technology-strategy.md` | Mobile technology strategy |
| `technology-evaluation.md` | Emerging technology evaluation |
| `technical-selection-documentation.md` | Technical selection documents |
| `spec-development.md` | SPEC development and technical specification |
| `technical-project-management.md` | Technical project management |

### Testing and Quality (2)

| Skill File | Description |
|------------|-------------|
| `automated-test-suite.md` | Automated test suite design for iOS/Android |
| `defect-triage-and-classification.md` | P0-P3 defect classification |

### Localization and i18n (8)

| Skill File | Description |
|------------|-------------|
| `language-translation-module.md` | Language Translation Module governance |
| `mobile-ui-translation.md` | Mobile UI string translation (general) |
| `mobile-ui-translation-chinese.md` | Mobile UI string translation (Chinese) |
| `mobile-ui-translation-japanese.md` | Mobile UI string translation (Japanese) |
| `mobile-ui-translation-korean.md` | Mobile UI string translation (Korean) |
| `mobile-ui-translation-english.md` | Mobile UI string translation (English QA) |
| `string-extraction-and-resource-files.md` | Mobile string extraction |
| `localization-pipeline-engineering.md` | Localization pipeline and TMS integration |

### Recruitment (HR) (7)

| Skill File | Description |
|------------|-------------|
| `vet-candidate.md` | Elite candidate vetting gate |
| `recruit-engineering.md` | Engineering role family recruitment |
| `recruit-product.md` | Product role family recruitment |
| `recruit-design.md` | Design role family recruitment |
| `recruit-data.md` | Data and ML role family recruitment |
| `recruit-translation.md` | Translation role family recruitment |
| `recruit-business.md` | Business role family recruitment |

---

## Summary

| Resource | Count | Location |
|----------|-------|----------|
| SubAgent Configurations | 20 | `agents/` |
| Skill Files | 44 | `skills/` |
| Workflow Definitions | 1 | `workflows/pipeline.md` |

---

## Usage

### Using SubAgents

To use a SubAgent, reference it by its file name (without `.md` extension). For example:

- `chief-technology-officer` — for architecture, SPEC development, UML Engineering Package
- `chief-design-officer` — for design systems, interaction design specifications
- `test-lead` — for automated testing and P0-P3 defect triage
- `software-architect` — for UML diagrams and Architecture Decision Records

Each SubAgent's `description` field in the YAML frontmatter indicates when to engage that agent.

### Pipeline Reference

The `workflows/pipeline.md` file contains the authoritative 10-stage development workflow definition. Reference it for:

- Stage gate criteria
- Artifact requirements (In/Out)
- Responsible producers and reviewers
- Defect handling procedures
