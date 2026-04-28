# Single-Source-of-Truth: Company Skills → Platform Adapters

> **ADR Reference:** Following AGENTS.md adapter discipline — company skills are the canonical source; platform-specific skill directories (`.opencode/skills/`) are adapters that translate canonical content into platform-specific conventions.

## Architecture

```
company/departments/          ← Canonical source skills (39 unique)
    ├── brand-design/
    ├── cyberspace-security/
    ├── human-resources/
    ├── localization/
    ├── product-management/
    └── research-develop/

.opencode/skills/             ← Platform adapters (213 skills)
    ├── android-*/            ← Android platform adapters
    ├── ios-*/                ← iOS platform adapters
    ├── backend-*/            ← Backend platform adapters
    ├── frontend-web-*/       ← Frontend platform adapters
    ├── devops-*/             ← DevOps platform adapters
    ├── security-*/           ← Security platform adapters
    ├── testing-*/            ← Testing platform adapters
    ├── architecture-*/       ← Architecture platform adapters
    ├── design-*/             ← Design platform adapters
    ├── localization-*/       ← Localization platform adapters
    ├── cross-platform-*/     ← Cross-platform adapters
    ├── hr-recruiting-*/      ← HR/Recruiting adapters
    ├── product-management-*/ ← Product Management adapters
    └── shared-*/             ← Shared guidelines adapters
```

## Adapter Discipline Rules

1. **Company skills define the WHAT and WHY** — business logic, pipeline governance, role responsibilities, and organizational standards.
2. **Opencode skills define the HOW** — platform-specific implementation patterns, tool configurations, code examples, and CI/CD pipelines.
3. **No contradiction allowed** — if an opencode skill contradicts its company skill counterpart, the company skill wins.
4. **Sync cadence** — when a company skill is updated, all dependent opencode adapter skills must be reviewed within 24 hours.
5. **Version alignment** — adapter skills reference their parent company skill version in the `prerequisites:` field.

## Mapping: Company Skills → Opencode Adapters

| Company Skill                       | Opencode Adapter Skills                                                                                                                                                    |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `android-implementation`            | `android-language-core-implementation`, `android-ui-ux-jetpack-compose`, `android-architecture-clean-architecture`                                                         |
| `mobile-security-architecture`      | `android-security-ci-cd-security`, `android-security-ci-cd-security-basics`, `ios-infrastructure-ios-implementation`, `security-architecture-mobile-security-architecture` |
| `prd-authorship`                    | `product-management-guidelines-prd-authorship`, `product-management-guidelines-prd-fluency`                                                                                |
| `pipeline`                          | All `architecture-guidelines-pipeline-*`, `devops-guidelines-ci-cd-*`, `testing-qa-strategy-cicd-*`                                                                        |
| `personnel`                         | `hr-recruiting-overview`, all `hr-recruiting-guidelines-*`                                                                                                                 |
| `localization-pipeline-engineering` | `localization-guidelines-localization-pipeline-engineering`, `localization-guidelines-string-extraction-and-resource-files`                                                |
| `mobile-product-strategy`           | `product-management-guidelines-mobile-product-strategy`                                                                                                                    |
| `mobile-architecture-patterns`      | `architecture-guidelines-mobile-architecture-patterns`, `cross-platform-kmp-architecture`, `cross-platform-flutter-architecture`                                           |
| `mobile-architecture-strategy`      | `architecture-guidelines-mobile-architecture-strategy`, `architecture-guidelines-mobile-technology-strategy`                                                               |
| `mobile-design-systems`             | `design-guidelines-mobile-design-systems`, `design-guidelines-design-systems`                                                                                              |
| `mobile-ui-translation`             | `localization-guidelines-mobile-ui-translation`, `localization-guidelines-mobile-ui-translation-*`                                                                         |
| `ios-implementation`                | `ios-infrastructure-ios-implementation`, `ios-ui-ux-swiftui`, `ios-architecture-swift-concurrency`                                                                         |
| `kmp-implementation`                | `cross-platform-kmp-implementation`, `cross-platform-kmp-shared-modules`                                                                                                   |
| `flutter-implementation`            | `cross-platform-flutter-implementation`, `cross-platform-flutter-architecture`                                                                                             |
| `defect-triage-and-classification`  | `testing-qa-strategy-defect-triage-and-classification`                                                                                                                     |
| `automated-test-suite`              | `testing-qa-api-contract-automated-test-suite`, `testing-qa-mobile-testing-fundamentals`                                                                                   |
| `design-to-engineering-handoff`     | `design-guidelines-design-to-engineering-handoff`                                                                                                                          |
| `interaction-design-specification`  | `design-guidelines-interaction-design-specification`, `design-guidelines-ids-fluency`                                                                                      |
| `architecture-decision-records`     | `architecture-guidelines-adr-governance`, `architecture-guidelines-adr-technical-writing`                                                                                  |
| `software-architecture-design`      | `architecture-guidelines-software-architecture-design`, `architecture-guidelines-uml-engineering`                                                                          |
| `spec-development`                  | `architecture-guidelines-spec-development`                                                                                                                                 |
| `technical-project-management`      | `architecture-guidelines-technical-project-management`                                                                                                                     |
| `technical-selection-documentation` | `architecture-guidelines-technical-selection-documentation`, `architecture-guidelines-technology-evaluation`                                                               |
| `uml-engineering-package`           | `architecture-guidelines-uml-engineering-package`                                                                                                                          |
| `user-research-driven-design`       | `design-guidelines-user-research-driven-design`                                                                                                                            |
| `vet-candidate`                     | `hr-recruiting-guidelines-vet-candidate`                                                                                                                                   |
| `web-prototype-development`         | `design-guidelines-web-prototype-development`                                                                                                                              |
| `emerging-threat-evaluation`        | `security-architecture-emerging-threat-evaluation`                                                                                                                         |
| `security-risk-assessment`          | `security-architecture-security-risk-assessment`, `security-compliance-auditing`                                                                                           |
| `application-security-hardening`    | `security-architecture-application-security-hardening`                                                                                                                     |
| `recruit-*`                         | `hr-recruiting-guidelines-recruit-*`                                                                                                                                       |

## Sync Protocol

When a company skill is modified:

1. **Identify affected adapters** using the mapping table above.
2. **Review each adapter** for contradiction or outdated information.
3. **Update adapters** within 24 hours of the company skill change.
4. **Log the sync** in the adapter's changelog with reference to the company skill change.
5. **Run eval suite** (Step 11) to verify triggering still works correctly.

## Version History

| Version | Date       | Author | Change                                                                            |
| ------- | ---------- | ------ | --------------------------------------------------------------------------------- |
| 1.0.0   | 2026-04-24 | CTO    | Initial single-source-of-truth pattern established per OPT-2026-04-23-001 Step 12 |
| 1.1.0   | 2026-04-25 | CTO    | Renamed 43 redundant skill folders; standardized template dirs to scripts/        |
