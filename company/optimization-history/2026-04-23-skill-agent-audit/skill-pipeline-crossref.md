# Skill ↔ Pipeline Cross-Reference Map

**Generated:** 2026-04-25
**Owner:** Software Architect (Rafael Okonkwo)
**Purpose:** Bidirectional mapping between skills and pipeline templates. Skills that govern pipeline stages reference the relevant template files. Pipeline templates reference the governing skills.

---

## 1. Pipeline → Skills Mapping

### Mobile Development Pipeline (`.opencode/pipeline/mobile-development/`)

| Pipeline Stage | Template File | Governing Skills |
| -------------- | ------------- | ---------------- |
| Stage 1: Requirements | `pipeline.md` §Stage 1 | `company/departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md`, `company/departments/product-management/supervisor/chief-product-officer/skills/mobile-product-strategy.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/mobile-security-architecture.md` |
| Stage 2: Prototype + IDS | `pipeline.md` §Stage 2 | `company/departments/brand-design/supervisor/chief-design-officer/skills/mobile-design-systems.md`, `company/departments/brand-design/supervisor/chief-design-officer/skills/interaction-design-specification.md`, `company/departments/brand-design/supervisor/chief-design-officer/skills/design-to-engineering-handoff.md`, `company/departments/brand-design/team/teammates/product-ui-ux-prototyper/lena-vasquez/skills/web-prototype-development.md` |
| Stage 3: UML + ADRs | `pipeline.md` §Stage 3 | `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/uml-engineering-package.md`, `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/architecture-decision-records.md`, `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/mobile-architecture-patterns.md`, `company/departments/cyberspace-security/supervisor/chief-information-officer/skills/technology-evaluation.md`, `company/departments/cyberspace-security/supervisor/chief-information-officer/skills/technical-selection-documentation.md` |
| Stage 4: Implementation Plan | `pipeline.md` §Stage 4 | `company/departments/research-develop/supervisor/chief-technology-officer/skills/spec-development.md`, `company/departments/research-develop/supervisor/chief-technology-officer/skills/software-architecture-design.md`, `company/departments/research-develop/supervisor/chief-technology-officer/skills/mobile-technology-strategy.md` |
| Stage 5: Development | `pipeline.md` §Stage 5 | `company/departments/research-develop/team/supervisors/android-development-lead/kofi-asante-mensah/skills/android-implementation.md`, `company/departments/research-develop/team/supervisors/ios-development-lead/seo-yeon-park/skills/ios-implementation.md`, `company/departments/research-develop/team/supervisors/cross-platform-development-lead/mei-ling-johansson/skills/kmp-implementation.md`, `company/departments/research-develop/team/supervisors/cross-platform-development-lead/mei-ling-johansson/skills/flutter-implementation.md` |
| Stage 6: Code Review | `pipeline.md` §Stage 6 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/defect-triage-and-classification.md`, `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/architecture-decision-records.md` |
| Stage 7: Automated Testing | `pipeline.md` §Stage 7 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/automated-test-suite.md` |
| Stage 8: Integrity Verification | `pipeline.md` §Stage 8 | `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/application-security-hardening.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/emerging-threat-evaluation.md` |
| Stage 9: i18n Engineering | `pipeline.md` §Stage 9 | `company/departments/localization/supervisor/chief-translation-officer/skills/language-translation-module.md`, `company/departments/localization/team/teammates/localization-engineer/skills/localization-pipeline-engineering.md` |
| Stage 10: Release Readiness | `pipeline.md` §Stage 10 | `company/departments/research-develop/supervisor/chief-technology-officer/skills/mobile-technology-strategy.md`, `company/departments/research-develop/supervisor/chief-technology-officer/skills/pipeline.md` |

### Web Development Pipeline (`.opencode/pipeline/web-development/`)

| Pipeline Stage | Template File | Governing Skills |
| -------------- | ------------- | ---------------- |
| Stage 1: Requirements | `pipeline.md` §Stage 1 | `company/departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md` |
| Stage 3: UML + ADRs | `pipeline.md` §Stage 3 | `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/uml-engineering-package.md`, `company/departments/research-develop/team/teammates/frontend-chapter-lead/amira-voss/skills/frontend-security.md`, `company/departments/research-develop/team/teammates/frontend-chapter-lead/amira-voss/skills/design-systems.md` |
| Stage 5: Development | `pipeline.md` §Stage 5 | `company/departments/research-develop/team/teammates/frontend-chapter-lead/amira-voss/skills/performance-optimization.md` |
| Stage 6: Code Review | `pipeline.md` §Stage 6 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/defect-triage-and-classification.md` |
| Stage 7: Automated Testing | `pipeline.md` §Stage 7 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/automated-test-suite.md` |
| Stage 9: i18n Engineering | `pipeline.md` §Stage 9 | `company/departments/localization/supervisor/chief-translation-officer/skills/language-translation-module.md` |
| Stage 10: Release Readiness | `pipeline.md` §Stage 10 | `company/departments/research-develop/supervisor/chief-technology-officer/skills/pipeline.md` |

### Backend API Pipeline (`.opencode/pipeline/backend-api/`)

| Pipeline Stage | Template File | Governing Skills |
| -------------- | ------------- | ---------------- |
| Stage 1: Requirements | `pipeline.md` §Stage 1 | `company/departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md` |
| Stage 3: UML + ADRs | `pipeline.md` §Stage 3 | `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/uml-engineering-package.md`, `company/departments/research-develop/team/teammates/backend-chapter-lead/dev-malhotra/skills/api-gateway-design.md`, `company/departments/research-develop/team/teammates/backend-chapter-lead/dev-malhotra/skills/database-architecture.md` |
| Stage 5: Development | `pipeline.md` §Stage 5 | `company/departments/research-develop/team/teammates/backend-chapter-lead/dev-malhotra/skills/distributed-systems.md` |
| Stage 6: Code Review | `pipeline.md` §Stage 6 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/defect-triage-and-classification.md` |
| Stage 7: Automated Testing | `pipeline.md` §Stage 7 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/automated-test-suite.md` |
| Stage 10: Release Readiness | `pipeline.md` §Stage 10 | `company/departments/research-develop/supervisor/chief-technology-officer/skills/pipeline.md` |

### Full-Stack Cross-Platform Pipeline (`.opencode/pipeline/full-stack/`)

| Pipeline Stage | Template File | Governing Skills |
| -------------- | ------------- | ---------------- |
| Stage 1: Requirements | `pipeline.md` §Stage 1 | `company/departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md`, `company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md` |
| Stage 3: UML + ADRs | `pipeline.md` §Stage 3 | `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/uml-engineering-package.md`, `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/mobile-architecture-patterns.md`, `company/departments/research-develop/team/supervisors/software-architect/rafael-okonkwo/skills/architecture-decision-records.md` |
| Stage 5: Development | `pipeline.md` §Stage 5 | `company/departments/research-develop/team/supervisors/android-development-lead/kofi-asante-mensah/skills/android-implementation.md`, `company/departments/research-develop/team/supervisors/ios-development-lead/seo-yeon-park/skills/ios-implementation.md`, `company/departments/research-develop/team/supervisors/cross-platform-development-lead/mei-ling-johansson/skills/kmp-implementation.md`, `company/departments/research-develop/team/supervisors/cross-platform-development-lead/mei-ling-johansson/skills/flutter-implementation.md` |
| Stage 6: Code Review | `pipeline.md` §Stage 6 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/defect-triage-and-classification.md` |
| Stage 7: Automated Testing | `pipeline.md` §Stage 7 | `company/departments/research-develop/team/supervisors/test-lead/priscilla-oduya/skills/automated-test-suite.md` |
| Stage 10: Release Readiness | `pipeline.md` §Stage 10 | `company/departments/research-develop/supervisor/chief-technology-officer/skills/pipeline.md` |

### Recruitment Pipeline (`.opencode/pipeline/recruitment/`)

| Pipeline Stage | Template File | Governing Skills |
| -------------- | ------------- | ---------------- |
| Stage 1-9: Full Pipeline | `pipeline.md` | `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-engineering.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-product.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-design.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-business.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-data.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-translation.md`, `company/departments/human-resources/supervisor/chief-human-resources-officer/skills/vet-candidate.md` |

---

## 2. Skills → Pipeline Mapping (Reverse Index)

### By Pipeline Stage

| Stage | Skills That Govern This Stage |
| ----- | ----------------------------- |
| **Stage 1** | `prd-authorship.md`, `mobile-product-strategy.md`, `security-risk-assessment.md`, `mobile-security-architecture.md` |
| **Stage 2** | `mobile-design-systems.md`, `interaction-design-specification.md`, `design-to-engineering-handoff.md`, `web-prototype-development.md` |
| **Stage 3** | `uml-engineering-package.md`, `architecture-decision-records.md`, `mobile-architecture-patterns.md`, `technology-evaluation.md`, `technical-selection-documentation.md`, `api-gateway-design.md`, `database-architecture.md`, `frontend-security.md`, `design-systems.md` |
| **Stage 4** | `spec-development.md`, `software-architecture-design.md`, `mobile-technology-strategy.md` |
| **Stage 5** | `android-implementation.md`, `ios-implementation.md`, `kmp-implementation.md`, `flutter-implementation.md`, `distributed-systems.md`, `performance-optimization.md` |
| **Stage 6** | `defect-triage-and-classification.md`, `architecture-decision-records.md` |
| **Stage 7** | `automated-test-suite.md` |
| **Stage 8** | `application-security-hardening.md`, `emerging-threat-evaluation.md` |
| **Stage 9** | `language-translation-module.md`, `localization-pipeline-engineering.md` |
| **Stage 10** | `mobile-technology-strategy.md`, `pipeline.md` |
| **Recruitment** | `recruit-engineering.md`, `recruit-product.md`, `recruit-design.md`, `recruit-business.md`, `recruit-data.md`, `recruit-translation.md`, `vet-candidate.md` |

### By Skill (Full Reverse Index)

| Skill File | Pipeline Stage(s) | Pipeline Template(s) |
| ---------- | ----------------- | -------------------- |
| `prd-authorship.md` | Stage 1 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `mobile-product-strategy.md` | Stage 1 | `mobile-development/pipeline.md` |
| `security-risk-assessment.md` | Stage 1 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `mobile-security-architecture.md` | Stage 1 | `mobile-development/pipeline.md` |
| `mobile-design-systems.md` | Stage 2 | `mobile-development/pipeline.md` |
| `interaction-design-specification.md` | Stage 2 | `mobile-development/pipeline.md` |
| `design-to-engineering-handoff.md` | Stage 2 | `mobile-development/pipeline.md` |
| `web-prototype-development.md` | Stage 2 | `mobile-development/pipeline.md` |
| `uml-engineering-package.md` | Stage 3 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `architecture-decision-records.md` | Stage 3, Stage 6 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `mobile-architecture-patterns.md` | Stage 3 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `technology-evaluation.md` | Stage 3 | `mobile-development/pipeline.md` |
| `technical-selection-documentation.md` | Stage 3 | `mobile-development/pipeline.md` |
| `api-gateway-design.md` | Stage 3 | `backend-api/pipeline.md` |
| `database-architecture.md` | Stage 3 | `backend-api/pipeline.md` |
| `frontend-security.md` | Stage 3 | `web-development/pipeline.md` |
| `design-systems.md` | Stage 3 | `web-development/pipeline.md` |
| `spec-development.md` | Stage 4 | `mobile-development/pipeline.md` |
| `software-architecture-design.md` | Stage 4 | `mobile-development/pipeline.md` |
| `mobile-technology-strategy.md` | Stage 4, Stage 10 | `mobile-development/pipeline.md` |
| `android-implementation.md` | Stage 5 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `ios-implementation.md` | Stage 5 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `kmp-implementation.md` | Stage 5 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `flutter-implementation.md` | Stage 5 | `mobile-development/pipeline.md`, `full-stack/pipeline.md` |
| `distributed-systems.md` | Stage 5 | `backend-api/pipeline.md` |
| `performance-optimization.md` | Stage 5 | `web-development/pipeline.md` |
| `defect-triage-and-classification.md` | Stage 6 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `automated-test-suite.md` | Stage 7 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `application-security-hardening.md` | Stage 8 | `mobile-development/pipeline.md` |
| `emerging-threat-evaluation.md` | Stage 8 | `mobile-development/pipeline.md` |
| `language-translation-module.md` | Stage 9 | `mobile-development/pipeline.md`, `web-development/pipeline.md` |
| `localization-pipeline-engineering.md` | Stage 9 | `mobile-development/pipeline.md` |
| `pipeline.md` | Stage 10 (all pipelines) | `mobile-development/pipeline.md`, `web-development/pipeline.md`, `backend-api/pipeline.md`, `full-stack/pipeline.md` |
| `recruit-engineering.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `recruit-product.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `recruit-design.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `recruit-business.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `recruit-data.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `recruit-translation.md` | Recruitment Stages 1-9 | `recruitment/pipeline.md` |
| `vet-candidate.md` | Recruitment Stage 5 | `recruitment/pipeline.md` |

---

## 3. Usage Guidelines

### For Skill Authors
When updating a skill, check this map to identify which pipeline stages your skill governs. If your skill's behavior changes, the corresponding pipeline template may need updating.

### For Pipeline Authors
When modifying a pipeline stage, check this map to identify which skills govern that stage. If the stage's gate criteria change, the governing skills may need updating.

### For Code Reviewers (Stage 6)
Use this map to verify that implementation artifacts reference the correct governing skills. E.g., Stage 5 Android implementation should follow `android-implementation.md`; Stage 7 testing should follow `automated-test-suite.md`.

---

_Cross-reference map generated 2026-04-25. Maintained by Software Architect. Update when new skills are created or pipeline stages are modified._
