# Translation Verification Report

**Project:** [Project Name]
**Stage:** 9 — i18n Engineering
**Version:** v1
**Date:** YYYY-MM-DD
**Author:** CTO-L (Dr. Amara Osei-Mensah)
**String Extraction Lead:** Tomas Dvoracek

---

## Structural Completeness (CPO/CDO/CTO Review)

| Check                                   | Result          | Notes                             |
| --------------------------------------- | --------------- | --------------------------------- |
| Zero hardcoded strings in codebase      | ☐ Pass / ☐ Fail |                                   |
| All resource files correctly structured | ☐ Pass / ☐ Fail |                                   |
| No untranslated UI components           | ☐ Pass / ☐ Fail |                                   |
| String key naming convention followed   | ☐ Pass / ☐ Fail | Per ADR-NNN                       |
| `key-index.csv` parity confirmed        | ☐ Pass / ☐ Fail | All keys present across platforms |

---

## Translation Completeness

| Language        | Total Strings | Translated | TM Leverage % | Post-Editing % | QA Pass Rate | Status      |
| --------------- | ------------- | ---------- | ------------- | -------------- | ------------ | ----------- |
| English         | [N]           | [N]        | —             | —              | —            | ✅ Complete |
| Chinese (ZH-CN) | [N]           | [N]        | XX%           | XX%            | XX%          | ✅ Complete |
| Japanese (JA)   | [N]           | [N]        | XX%           | XX%            | XX%          | ✅ Complete |
| Korean (KO)     | [N]           | [N]        | XX%           | XX%            | XX%          | ✅ Complete |
| French (FR-FR)  | [N]           | [N]        | XX%           | XX%            | XX%          | ✅ Complete |

---

## Platform Resource File Validation

| Platform       | File                      | Valid?       | Placeholder Integrity                           | Truncation Risks                                 |
| -------------- | ------------------------- | ------------ | ----------------------------------------------- | ------------------------------------------------ |
| Web Frontend   | `messages.json`           | ☐ Yes / ☐ No | All `{placeholder}` intact                      | [>40% generic — flexible CSS layout]             |
| Web Frontend   | `metadata.json`           | ☐ Yes / ☐ No | SEO/meta strings valid                          | [Title: 60 chars, Description: 160 chars]        |
| Android        | `strings.xml`             | ☐ Yes / ☐ No | All `%1$s`, `%d` intact                         | [>35% expansion for buttons, >50% for body text] |
| Android        | `strings-plurals.xml`     | ☐ Yes / ☐ No | Plural rules correct                            | [N/A]                                            |
| iOS            | `Localizable.strings`     | ☐ Yes / ☐ No | All `%@`, `%d` intact                           | [>30% expansion for nav titles, >45% for body]   |
| iOS            | `Localizable.stringsdict` | ☐ Yes / ☐ No | All pluralisation keys have stringsdict entries | [N/A]                                            |
| KMP            | `key-index.csv`           | ☐ Yes / ☐ No | All placeholders intact                         | [>40% generic — flexible layout]                 |
| Flutter        | `.arb`                    | ☐ Yes / ☐ No | All `{placeholder}` intact                      | [>40% generic — flexible layout]                 |

> **Platform-specific truncation thresholds:** Android buttons 35%, Android body 50%, iOS nav titles 30%, iOS body 45%, Flutter generic 40%. CJK languages compress 30-40% vs English; German expands 25-35%.

---

## Linguistic Quality

| Language   | Reviewer        | Quality Rating                  | Issues Found | Resolved?    |
| ---------- | --------------- | ------------------------------- | ------------ | ------------ |
| [Language] | [Linguist name] | [Excellent / Good / Needs Work] | [N issues]   | ☐ Yes / ☐ No |

### Platform-Specific Translation Style Guides

Each target language must have a style guide entry documenting platform-specific conventions:

| Language | Date/Time Format | Number Format | Currency Format | Formality Level      | Platform Notes                           |
| -------- | ---------------- | ------------- | --------------- | -------------------- | ---------------------------------------- |
| [ZH-CN]  | [yyyy年MM月dd日] | [1,000.50]    | [¥100.00]       | [Neutral]            | [Simplified characters]                  |
| [ZH-TW]  | [yyyy年MM月dd日] | [1,000.50]    | [NT$100.00]     | [Neutral]            | [Traditional characters]                 |
| [JA]     | [yyyy/MM/dd]     | [1,000.50]    | [¥100]          | [Keigo/Desu-Masu]    | [iOS/Android UI conventions]             |
| [KO]     | [yyyy.MM.dd]     | [1,000.50]    | [₩100]          | [Honorific level]    | [iOS/Android UI conventions]             |
| [FR-FR]  | [dd/MM/yyyy]     | [1 000,50]    | [100,00 €]      | [Formal/Vouvoiement] | [Android: use guillemets « »]            |
| [FR-CA]  | [yyyy-MM-dd]     | [1 000,50]    | [100,00 $]      | [Standard]           | [Canadian conventions differ from FR-FR] |

**Style Guide Conformance:** ☐ All languages conform / ☐ [N] languages have deviations documented below.

| Language   | Deviation from Style Guide | Impact         | Resolved?    |
| ---------- | -------------------------- | -------------- | ------------ |
| [Language] | [Description]              | [UI/UX impact] | ☐ Yes / ☐ No |

### Quantitative Quality Metrics (BLEU/TER)

| Language | BLEU Score | TER Score | Error Rate (per 1K words) | Meets Target?   |
| -------- | ---------- | --------- | ------------------------- | --------------- |
| [ZH-CN]  | [0.XX]     | [XX%]     | [X.X]                     | ☐ Pass / ☐ Fail |
| [JA]     | [0.XX]     | [XX%]     | [X.X]                     | ☐ Pass / ☐ Fail |
| [KO]     | [0.XX]     | [XX%]     | [X.X]                     | ☐ Pass / ☐ Fail |
| [FR-FR]  | [0.XX]     | [XX%]     | [X.X]                     | ☐ Pass / ☐ Fail |

**Quality targets:** BLEU ≥ 0.80 for all tier-1 languages; TER ≤ 25% for MT post-editing; error rate ≤ 2 per 1,000 words.

### Accessibility String Quality

Screen reader labels and hints verified in each target language for clarity and correctness:

| Language | Screen Reader Labels Verified? | VoiceOver/TalkBack Tested? | Issues Found | Resolved?    |
| -------- | ------------------------------ | -------------------------- | ------------ | ------------ |
| [ZH-CN]  | ☐ Yes / ☐ No                   | ☐ Yes / ☐ No               | [N issues]   | ☐ Yes / ☐ No |
| [JA]     | ☐ Yes / ☐ No                   | ☐ Yes / ☐ No               | [N issues]   | ☐ Yes / ☐ No |
| [KO]     | ☐ Yes / ☐ No                   | ☐ Yes / ☐ No               | [N issues]   | ☐ Yes / ☐ No |
| [FR-FR]  | ☐ Yes / ☐ No                   | ☐ Yes / ☐ No               | [N issues]   | ☐ Yes / ☐ No |

> **Note:** Literal translations of accessibility labels may be confusing. Labels reviewed by native speaker familiar with platform screen reader behavior.

### Commercial Copy Localization

| Language | Paywall Copy Reviewed? | Reviewer | Issues | Resolved?    |
| -------- | ---------------------- | -------- | ------ | ------------ |
| [ZH-CN]  | ☐ Yes / ☐ No           | [Name]   | [N]    | ☐ Yes / ☐ No |
| [JA]     | ☐ Yes / ☐ No           | [Name]   | [N]    | ☐ Yes / ☐ No |
| [KO]     | ☐ Yes / ☐ No           | [Name]   | [N]    | ☐ Yes / ☐ No |
| [FR-FR]  | ☐ Yes / ☐ No           | [Name]   | [N]    | ☐ Yes / ☐ No |

---

## CTO-L Sign-Off

**All target languages complete and verified.**
**Translation accuracy confirmed across all target languages.**

**Approved by CTO-L (Dr. Amara Osei-Mensah) on YYYY-MM-DD**

---

## Structural Completeness Sign-Off (CPO/CDO/CTO)

| Reviewer                              | Structural Completeness | Date | Signature |
| ------------------------------------- | ----------------------- | ---- | --------- |
| CPO                                   | ☐ Pass / ☐ Fail         |      |           |
| CDO                                   | ☐ Pass / ☐ Fail         |      |           |
| CTO                                   | ☐ Pass / ☐ Fail         |      |           |
| CTO-L (advisory on resource validity) | ☐ Pass / ☐ Fail         |      |           |
