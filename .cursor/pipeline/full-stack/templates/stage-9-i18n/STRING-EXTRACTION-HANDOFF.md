# String Extraction Handoff

**Project:** [Project Name]
**Author:** Internationalization Specialist (Tomas Dvoracek)
**Reviewer:** CTO-L (Dr. Amara Osei-Mensah)
**Date:** YYYY-MM-DD
**Phase:** Phase A (R&D Extraction) → Phase B (TMS Translation)
**Version:** v1

---

## Purpose

This artifact certifies the completion of Phase A (String Extraction Validation) and serves as the formal handoff to Phase B (TMS Translation). It is produced by the Internationalization Specialist after scanning the integrity-verified codebase and extracting all localizable strings into platform resource files.

---

## 1. Extraction Summary

| Metric                                              | Value |
| --------------------------------------------------- | ----- |
| Total strings extracted                             | [N]   |
| Strings in key-index.csv                            | [N]   |
| Hardcoded strings found (not extracted)             | [N]   |
| Hardcoded strings remediated                        | [N]   |
| Hardcoded strings remaining (classified as defects) | [N]   |
| Duplicate keys merged                               | [N]   |
| Keys following taxonomy convention                  | [N]   |
| Keys with convention violations (exceptions)        | [N]   |

---

## 2. Platform Resource Files Generated

| Platform     | File Path                          | Keys | Status                    |
| ------------ | ---------------------------------- | ---- | ------------------------- |
| Web Frontend | `locales/{lang}/messages.json`     | [N]  | ☐ Generated / ☐ Validated |
| Web Frontend | `locales/{lang}/metadata.json`     | [N]  | ☐ Generated / ☐ Validated |
| Android      | `res/values/strings.xml`           | [N]  | ☐ Generated / ☐ Validated |
| Android      | `res/values/strings-plurals.xml`   | [N]  | ☐ Generated / ☐ Validated |
| iOS          | `en.lproj/Localizable.strings`     | [N]  | ☐ Generated / ☐ Validated |
| iOS          | `en.lproj/Localizable.stringsdict` | [N]  | ☐ Generated / ☐ Validated |
| KMP Shared   | `shared/resources/strings.json`    | [N]  | ☐ Generated / ☐ Validated |
| Flutter      | `lib/l10n/app_en.arb`              | [N]  | ☐ Generated / ☐ Validated |

---

## 3. key-index.csv Validation

| Validation Check                                    | Result          | Notes                          |
| --------------------------------------------------- | --------------- | ------------------------------ |
| All keys present in key-index.csv                   | ☐ Pass / ☐ Fail | [N keys verified]              |
| All keys follow taxonomy convention                 | ☐ Pass / ☐ Fail | [N exceptions, all documented] |
| No duplicate keys across files                      | ☐ Pass / ☐ Fail | [N duplicates merged]          |
| All keys have source string (English)               | ☐ Pass / ☐ Fail | [N keys verified]              |
| Pluralisation keys have stringsdict/plurals entries | ☐ Pass / ☐ Fail | [N plural keys verified]       |
| String-array keys have all items                    | ☐ Pass / ☐ Fail | [N array keys verified]        |

---

## 4. Translation Package for TMS

| Package           | Format            | Target Languages                     | Word Count | TM Leverage % |
| ----------------- | ----------------- | ------------------------------------ | ---------- | ------------- |
| [Project strings] | [XLIFF 2.0 / TMX] | [ZH-CN, ZH-TW, JA, KO, FR-FR, FR-CA] | [N words]  | [XX]%         |

### Per-Language Breakdown

| Language                | File              | Strings | Words | 100% TM Match | 75-99% TM Match | New Strings |
| ----------------------- | ----------------- | ------- | ----- | ------------- | --------------- | ----------- |
| [Chinese (Simplified)]  | [app_zh_CN.xliff] | [N]     | [N]   | [N]           | [N]             | [N]         |
| [Chinese (Traditional)] | [app_zh_TW.xliff] | [N]     | [N]   | [N]           | [N]             | [N]         |
| [Japanese]              | [app_ja.xliff]    | [N]     | [N]   | [N]           | [N]             | [N]         |
| [Korean]                | [app_ko.xliff]    | [N]     | [N]   | [N]           | [N]             | [N]         |
| [French (France)]       | [app_fr_FR.xliff] | [N]     | [N]   | [N]           | [N]             | [N]         |
| [French (Canada)]       | [app_fr_CA.xliff] | [N]     | [N]   | [N]           | [N]             | [N]         |

---

## 5. Outstanding Issues

| Issue ID | Description                                                   | Severity | Assigned To | Resolution Target |
| -------- | ------------------------------------------------------------- | -------- | ----------- | ----------------- |
| EXT-001  | [e.g., "3 hardcoded strings remaining in Android login flow"] | [P1/P2]  | [Name]      | [Date]            |
| EXT-002  | [e.g., "Key naming exception: auth.2fa.title — needs rename"] | [P2]     | [Name]      | [Date]            |

---

## 6. Handoff Certification

**I certify that:**

- [x] All localizable strings have been extracted from the codebase
- [x] Platform resource files have been generated for all active tracks
- [x] key-index.csv is complete and validated
- [x] Translation packages are ready for TMS ingestion
- [x] All outstanding issues are documented with severity and ownership

---

**Prepared by Internationalization Specialist (Tomas Dvoracek) on YYYY-MM-DD**
**Reviewed and accepted by CTO-L (Dr. Amara Osei-Mensah) on YYYY-MM-DD**

> **Phase B begins upon CTO-L acceptance.** The Localization Department ingests the translation packages into the TMS and begins the five-phase Language Translation Module process.
