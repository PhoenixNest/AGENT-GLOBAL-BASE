# Studio — Topics

Cross-cutting strategies, governance frameworks, and operational standards for the game studio.

## Core Topics

| Document                                        | Description                                                                                                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Game Asset Strategy](./game-asset-strategy.md) | CTO + CDO + CSO assessment of free, commercially-licensed asset sourcing — tier list, license framework, security review pipeline, SBOM, visual coherence strategy |

## Governance & Compliance

| Topic                                 | Description                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------- |
| **[Accessibility](./accessibility/)** | Ownership assignment, WCAG 2.1 AA compliance, external consultant engagement |
| **[Compliance](./compliance/)**       | COPPA assessment, Unity licensing, SDK vetting, FTC determinations           |
| **[Governance](./governance/)**       | D&I framework, role reconciliation, Phase 1 artifact backfill flag           |
| **[Security](./security/)**           | Ownership matrix, SDK vetting process, penetration testing plan              |

## Engineering & Infrastructure

| Topic                                   | Description                                                             |
| --------------------------------------- | ----------------------------------------------------------------------- |
| **[Engineering](./engineering/)**       | Network testing strategy, CI/CD RACI, Tools Engineer decision framework |
| **[Infrastructure](./infrastructure/)** | Data pipeline ownership, multi-tenancy ADR, self-hosted adapter PoC     |

## Design & Operations

| Topic                           | Description                                                              |
| ------------------------------- | ------------------------------------------------------------------------ |
| **[Design](./design/)**         | Game IDS template, CDO Stage 2 review checklist, platform-native meta-UI |
| **[Operations](./operations/)** | Production bandwidth monitoring, UA strategy review framework            |

## Directory Structure

```
library/topics/
├── README.md                            # This file
├── game-asset-strategy.md               # Asset sourcing strategy
├── accessibility/
│   └── README.md                        # Accessibility ownership & compliance
├── compliance/
│   ├── README.md                        # Compliance status dashboard
│   ├── coppa-assessment-plan.md
│   ├── coppa-ftc-determination.md
│   ├── sdk-vetting-report.md
│   ├── unity-legal-memorandum.md
│   ├── unity-licensing-review.md
│   └── unity-term-sheet.md
├── design/
│   ├── README.md                        # Game IDS template
│   └── cdo-stage-2-review-checklist.md
├── engineering/
│   ├── README.md                        # Network testing strategy
│   ├── cicd-raci.md
│   └── tools-engineer-decision.md
├── governance/
│   ├── README.md                        # Governance overview
│   ├── di-framework.md
│   ├── phase-1-backfill-flag.md
│   └── role-reconciliation-checkpoint.md
├── infrastructure/
│   ├── README.md                        # Data pipeline ownership
│   ├── multi-tenancy-adr.md
│   ├── self-hosted-adapter-poc.md
│   └── self-hosted-poc-results.md
├── operations/
│   ├── README.md                        # Production bandwidth monitoring
│   └── ua-strategy-review-framework.md
└── security/
    ├── README.md                        # Security ownership matrix
    └── pen-testing-plan.md
```
