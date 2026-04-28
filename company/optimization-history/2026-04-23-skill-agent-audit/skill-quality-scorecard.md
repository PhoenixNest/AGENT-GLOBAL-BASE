# Skill Quality Scorecard — Q2 2026 Baseline

**Audit Date:** 2026-04-23
**Auditor:** CIO (Dr. Priya Mehta) + CTO (Dr. Kenji Nakamura)
**Next Review:** Q3 2026 (2026-07-01)
**Framework:** skill-creator evaluation standards (frontmatter, description, body quality, progressive disclosure, bundled resources, "why" explained)

---

## 1. Executive Summary

| Ecosystem  | Total Skills | Avg Grade | Frontmatter | Description | Body Quality | Progressive Disclosure | Bundled Resources | "Why" Explained |
| ---------- | ------------ | --------- | ----------- | ----------- | ------------ | ---------------------- | ----------------- | --------------- |
| Company    | 39           | **B**     | 100%        | 85%         | 90%          | 95%                    | 0%                | 65%             |
| Opencode   | 213          | **C−**    | 100%        | 8%          | 84%          | 93%                    | 0%                | 40%             |
| Studio     | 76           | **C**     | 0%          | 0%          | 85%          | 100%                   | 0%                | 50%             |
| **Total**  | **328**      | **C+**    | **77%**     | **51%**     | **86%**      | **95%**                | **0%**            | **50%**         |

**Critical Gaps (P0 for Q3):**
1. **Bundled Resources: 0% across all 328 skills** — No skill includes scripts, configs, templates, or reference files inline.
2. **Opencode descriptions: 8% actionable** — ~200 skills use `'Category skill: Name'` format instead of trigger descriptions.
3. **Studio frontmatter: 0%** — No YAML frontmatter on any studio skill; undiscoverable by AI platforms.

---

## 2. Company Skills — Per-Skill Scorecard (39 skills)

| Skill | Owner | Lines | FM | Desc | Body | PD | Res | Why | Grade | Q3 Target |
| ----- | ----- | ----- | -- | ---- | ---- | -- | --- | --- | ----- | --------- |
| android-implementation | Kofi Asante-Mensah | 171 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B+ | A |
| mobile-security-architecture | Dr. Sarah Chen | 149 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| prd-authorship | Marcus Tran-Yoshida | 288 | ✅ | ✅ | EXCEL | ✅ | ❌ | ✅ | A | A |
| pipeline | Dr. Kenji Nakamura | 194 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B+ | A- |
| personnel | Dr. Evelyn Hartwell | 121 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B+ | A- |
| localization-pipeline-engineering | Dr. Amara Osei-Mensah | 7 | ✅ | ✅ | FAIL | ✅ | N/A | N/A | C− | B |
| defect-triage-and-classification | Priscilla Oduya | ~150 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| application-security-hardening | Dr. Sarah Chen | ~130 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| architecture-decision-records | Rafael Okonkwo | ~200 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| automated-test-suite | Priscilla Oduya | ~180 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B+ | A- |
| design-to-engineering-handoff | Yuki Tanaka-Chen | ~160 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| interaction-design-specification | Yuki Tanaka-Chen | ~140 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| ios-implementation | Seo-Yeon Park | ~170 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| kmp-implementation | Mei-Ling Johansson | ~190 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| flutter-implementation | Mei-Ling Johansson | ~180 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| mobile-architecture-patterns | Rafael Okonkwo | ~200 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| mobile-architecture-strategy | Dr. Priya Mehta | ~150 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| mobile-design-systems | Yuki Tanaka-Chen | ~170 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| mobile-product-strategy | Marcus Tran-Yoshida | ~160 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| mobile-technology-strategy | Dr. Kenji Nakamura | ~140 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| mobile-ui-translation | Dr. Amara Osei-Mensah | ~120 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| prototyper-interaction-design-spec | Lena Vasquez | ~150 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-business | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-data | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-design | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-engineering | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-product | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| recruit-translation | Dr. Evelyn Hartwell | ~100 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| security-risk-assessment | Dr. Sarah Chen | ~160 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| software-architecture-design | Dr. Kenji Nakamura | ~180 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| spec-development | Dr. Kenji Nakamura | ~170 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| technical-project-management | Dr. Kenji Nakamura | ~150 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| technical-selection-documentation | Dr. Priya Mehta | ~160 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| technology-evaluation | Dr. Priya Mehta | ~140 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| uml-engineering-package | Rafael Okonkwo | ~170 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| user-research-driven-design | Yuki Tanaka-Chen | ~150 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| vet-candidate | Dr. Evelyn Hartwell | ~130 | ✅ | ✅ | GOOD | ✅ | ❌ | ✅ | B+ | A- |
| web-prototype-development | Lena Vasquez | ~160 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |
| emerging-threat-evaluation | Dr. Sarah Chen | ~120 | ✅ | ✅ | GOOD | ✅ | ❌ | ⚠️ | B | A- |

**Legend:** FM=Frontmatter, Desc=Description, Body=Body Quality, PD=Progressive Disclosure, Res=Bundled Resources, Why="Why" Explained
**Grades:** A/A−/B+/B/B−/C+/C/C−/D+/D

### Company Skills — Aggregate Metrics

| Metric | Q2 2026 (Baseline) | Q3 2026 Target | Gap |
| ------ | ------------------ | -------------- | --- |
| Frontmatter coverage | 100% | 100% | — |
| Actionable descriptions | 85% | 95% | +10% |
| Body quality ≥ GOOD | 90% | 95% | +5% |
| Progressive disclosure | 95% | 100% | +5% |
| Bundled resources | 0% | 30% | +30% |
| "Why" explained | 65% | 80% | +15% |
| Overall grade avg | B | A− | +1 grade |

---

## 3. Opencode Skills — Category Scorecard (213 skills)

| Category | Count | FM | Desc | Body | PD | Res | Grade | Q3 Target |
| -------- | ----- | -- | ---- | ---- | -- | --- | ----- | --------- |
| Android | 12 | 100% | 5% | 85% | 92% | 0% | C− | B |
| iOS | 12 | 100% | 5% | 85% | 92% | 0% | C− | B |
| Backend | 14 | 100% | 10% | 90% | 86% | 0% | C | B |
| Frontend Web | 15 | 100% | 10% | 80% | 93% | 0% | C | B |
| DevOps | 22 | 100% | 5% | 82% | 91% | 0% | C− | B |
| Security | 14 | 100% | 5% | 88% | 86% | 0% | C− | B |
| Testing/QA | 22 | 100% | 5% | 85% | 82% | 0% | D+ | B− |
| Architecture | 14 | 100% | 10% | 88% | 93% | 0% | C | B |
| Design | 7 | 100% | 5% | 86% | 100% | 0% | C− | B |
| Localization | 7 | 100% | 5% | 86% | 100% | 0% | C− | B |
| Cross-Platform | 5 | 100% | 10% | 80% | 100% | 0% | C | B |
| HR/Recruiting | 8 | 100% | 5% | 75% | 100% | 0% | D+ | B− |
| Product Management | 3 | 100% | 10% | 83% | 100% | 0% | C | B |
| Shared | 8 | 100% | 5% | 75% | 100% | 0% | D+ | B− |
| Overview skills | 12 | 100% | 50% | 70% | 100% | 0% | C+ | B+ |
| **Total** | **213** | **100%** | **~8%** | **~84%** | **~93%** | **0%** | **C−** | **B** |

### Opencode Skills — Critical Pattern

**Description field anti-pattern:** ~200 of 213 skills use `'Category skill: Skill Name'` format (e.g., `"Android skill: Android Implementation"`). This is a category label, not a trigger description. It prevents reliable skill auto-discovery.

**Q3 Remediation:** Convert all description fields to trigger-based format following skill-creator standards:
- **Before:** `"Android skill: Android Implementation"`
- **After:** `"Android application development — Jetpack Compose UI, MVVM + StateFlow + Repository architecture, Kotlin Coroutines, Hilt DI, Room, Retrofit, platform security (Keystore, EncryptedSharedPreferences), Google Play submission. Owned by Kofi Asante-Mensah (Android Lead)."`

---

## 4. Studio Skills — Category Scorecard (76 skills)

| Division | Count | FM | Desc | Body | PD | Res | Grade | Q3 Target |
| -------- | ----- | -- | ---- | ---- | -- | --- | ----- | --------- |
| Leadership | 6 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Engineering | 20 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Creative/Design | 11 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Art | 14 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Audio | 4 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Production | 3 | 0% | 0% | GOOD | PASS | 0% | C | B |
| Live Ops | 11 | 0% | 0% | GOOD | PASS | 0% | C | B |
| QA/SDET | 7 | 0% | 0% | GOOD | PASS | 0% | C | B |
| **Total** | **76** | **0%** | **0%** | **~85%** | **~100%** | **0%** | **C** | **B** |

### Studio Skills — Critical Pattern

**Zero YAML frontmatter:** All 76 studio skills start directly with `# Title` markdown. They cannot be discovered by AI platforms that rely on frontmatter for skill registration.

**Q3 Remediation:** Add YAML frontmatter (`name`, `description`, `owner`, `category`, `version`) to all 76 studio skills.

---

## 5. Cross-Ecosystem Quality Trends

| Dimension | Company | Opencode | Studio | Overall | Q3 Target |
| --------- | ------- | -------- | ------ | ------- | --------- |
| Frontmatter | 100% | 100% | 0% | 77% | 95% |
| Description | 85% | 8% | 0% | 51% | 70% |
| Body Quality | 90% | 84% | 85% | 86% | 90% |
| Progressive Disclosure | 95% | 93% | 100% | 95% | 98% |
| Bundled Resources | 0% | 0% | 0% | 0% | 15% |
| "Why" Explained | 65% | 40% | 50% | 50% | 65% |

---

## 6. Quarterly Tracking Log

| Quarter | Date | Auditor | Overall Grade | Key Changes |
| ------- | ---- | ------- | ------------- | ----------- |
| Q2 2026 | 2026-04-23 | CIO + CTO | C+ | Baseline established. 328 skills audited. P2-01 (path resolution) completed. |
| Q3 2026 | 2026-07-01 | TBD | Target: B | Opencode description remediation. Studio frontmatter addition. Bundled resources pilot. |
| Q4 2026 | 2026-10-01 | TBD | Target: B+ | Full bundled resources coverage. "Why" explained improvement. |
| Q1 2027 | 2027-01-01 | TBD | Target: A− | All dimensions ≥ 80%. |

---

## 7. Scoring Methodology

### Dimension Definitions

| Dimension | Weight | Pass Criteria | Scoring |
| --------- | ------ | ------------- | ------- |
| **Frontmatter** | 10% | Valid YAML with `name`, `description`, `owner` | Binary: present/absent |
| **Description** | 20% | Trigger-based, not category label; includes owner and scope | 0-5 scale |
| **Body Quality** | 25% | Well-structured, actionable, progressive disclosure | FAIL/PASS/GOOD/EXCEL |
| **Progressive Disclosure** | 15% | Overview → detail → reference pattern | Binary: present/absent |
| **Bundled Resources** | 15% | Scripts, configs, templates, or references included | 0-5 scale |
| **"Why" Explained** | 15% | Rationale and context provided, not just "how" | Binary: present/absent |

### Grade Mapping

| Overall Score | Grade |
| ------------- | ----- |
| 90-100% | A |
| 80-89% | A− |
| 75-79% | B+ |
| 70-74% | B |
| 65-69% | B− |
| 60-64% | C+ |
| 55-59% | C |
| 50-54% | C− |
| 45-49% | D+ |
| < 45% | D |

---

## 8. Remediation Backlog

| ID | Finding | Ecosystem | Priority | Owner | Target Quarter |
| -- | ------- | --------- | -------- | ----- | -------------- |
| SQ-001 | Description anti-pattern (~200 skills) | Opencode | P0 | CTO | Q3 2026 |
| SQ-002 | Zero YAML frontmatter (76 skills) | Studio | P0 | Studio Director | Q3 2026 |
| SQ-003 | Zero bundled resources (328 skills) | All | P1 | CTO + CIO | Q3-Q4 2026 |
| SQ-004 | "Why" not explained (50% of skills) | All | P2 | Skill Owners | Q3-Q4 2026 |
| SQ-005 | localization-pipeline-engineering stub (7 lines) | Company | P1 | CTO-L | Q3 2026 |

---

_Scorecard generated 2026-04-25. Next review: 2026-07-01._
