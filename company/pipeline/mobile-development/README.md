# Mobile Development Pipeline

The authoritative 10-stage development workflow for mobile product delivery. Supports Android, iOS, KMP Cross-Platform, and Flutter Cross-Platform strategies.

---

## Pipeline Definition

- **Main spec:** [`pipeline.md`](pipeline.md)
- **Monitoring:** [`monitoring.md`](monitoring.md)
- **Templates:** [`templates/`](templates/)
- **Optimization history:** [`optimization-history/`](optimization-history/)

---

## Supported Platform Strategies

| Strategy | Target Platforms | Implementation Model |
|----------|-----------------|---------------------|
| Android-Only | Android (Google Play) | Track A FULL (7 engineers) |
| iOS-Only | iOS (App Store) | Track B FULL (7 engineers) |
| Both Native | Android + iOS | Track A FULL + Track B FULL (13 engineers) |
| KMP Cross-Platform | Android + iOS | Track C PRIMARY (KMP shared module) + Tracks A/B LIGHT (2 engineers each) |
| Flutter Cross-Platform | Android + iOS | Track C PRIMARY (Flutter codebase) + Tracks A/B LIGHT (2 engineers each) |

Platform strategy is determined at **Stage 3** via the Platform Strategy ADR.

---

## Pipeline Stages

| # | Stage | Responsible Producer | User Approval? |
|---|-------|---------------------|----------------|
| 1 | Requirements → PRD + SRD | CPO (PRD), CSO (SRD) | ✅ Yes |
| 2 | PRD → Web Prototype + IDS | CDO | ✅ Yes |
| 3 | Prototype → UML Engineering Package | CTO (UML), CIO (ADRs + TSD) | ✅ Yes |
| 4 | UML → Coding Implementation Plan | CTO | ✅ Yes |
| 5 | Plan → Software Development | CTO (oversees), Platform Leads (execute) | ❌ No |
| 6 | Development → Code Review | CTO (convenes panel) | ✅ Yes |
| 7 | Code Review → Automated Testing | CTO + Test Lead | ✅ Yes |
| 8 | Automated Testing → Integrity Verification | CTO (convenes panel) | ❌ No |
| 9 | Integrity → i18n Engineering | CTO-L | ❌ No |
| 10 | i18n → Release Readiness Check | CTO (panel) + **User** (final decision) | ✅ Yes |

---

## Track Coordination

| Role | Responsibility |
|------|---------------|
| VP Mobile (Marcus Andersson) | Stage 5 coordinator across all platform tracks |
| Android Lead (Kofi Asante-Mensah) | Track A execution |
| iOS Lead (Seo-Yeon Park) | Track B execution |
| Cross-Platform Lead (Mei-Ling Johansson) | Track C execution (KMP or Flutter) |

---

## Optimization History

The mobile pipeline underwent a comprehensive optimization review on April 8, 2026, with unanimous conditional approval from the 8-officer C-Suite panel (59 conditions, all resolved). See [`optimization-history/mobile-pipeline-optimization-april-2026.md`](optimization-history/mobile-pipeline-optimization-april-2026.md).

---

_Last updated: April 13, 2026_
