# String Extraction Handoff

**Project:** [Project Name]
**Author:** Internationalization Specialist (Tomas Dvoracek)
**Reviewer:** CTO-L (Dr. Amara Osei-Mensah)
**Date:** YYYY-MM-DD
**Phase:** Phase A (R&D Extraction) -> Phase B (TMS Translation)
**Version:** v1

---

## Purpose

This artifact certifies the completion of Phase A (String Extraction Validation) and serves as the formal handoff to Phase B (TMS Translation). It is produced by the Internationalization Specialist after scanning the integrity-verified codebase and extracting all localizable strings into backend-appropriate localization files.

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

## 2. Localization Files Generated

| Target                          | File Path                                        | Keys | Status                    |
| ------------------------------- | ------------------------------------------------ | ---- | ------------------------- |
| API Error Messages              | `locales/en/errors.json`                         | [N]  | Generated / Validated     |
| API Error Messages (template)   | `locales/{locale}/errors.json`                   | [N]  | Generated / Validated     |
| Developer Portal Content        | `docs/locales/en/portal.json`                    | [N]  | Generated / Validated     |
| Developer Portal Content (template) | `docs/locales/{locale}/portal.json`          | [N]  | Generated / Validated     |
| API Documentation (OpenAPI desc)| `docs/locales/en/openapi-descriptions.json`      | [N]  | Generated / Validated     |
| Email Templates                 | `templates/locales/en/emails.json`               | [N]  | Generated / Validated     |
| Webhook Payload Descriptions    | `docs/locales/en/webhook-payloads.json`          | [N]  | Generated / Validated     |

---

## 3. key-index.csv Validation

| Validation Check                                    | Result          | Notes                          |
| --------------------------------------------------- | --------------- | ------------------------------ |
| All keys present in key-index.csv                   | Pass / Fail     | [N keys verified]              |
| All keys follow taxonomy convention                 | Pass / Fail     | [N exceptions, all documented] |
| No duplicate keys across files                      | Pass / Fail     | [N duplicates merged]          |
| All keys have source string (English)               | Pass / Fail     | [N keys verified]              |
| Pluralisation keys have proper format               | Pass / Fail     | [N plural keys verified]       |
| Placeholder format consistent across all files      | Pass / Fail     | [%s or {key} format verified]  |

---

## 4. Translation Package for TMS

| Package           | Format            | Target Languages                     | Word Count | TM Leverage % |
| ----------------- | ----------------- | ------------------------------------ | ---------- | ------------- |
| [Project strings] | [XLIFF 2.0 / TMX] | [ZH-CN, ZH-TW, JA, KO, FR-FR, FR-CA] | [N words]  | [XX]%         |

### Per-Language Breakdown

| Language                | File              | Strings | Words | 100% TM Match | 75-99% TM Match | New Strings |
| ----------------------- | ----------------- | ------- | ----- | ------------- | --------------- | ----------- |
| [Chinese (Simplified)]  | [errors_zh_CN.xliff] | [N]  | [N]   | [N]           | [N]             | [N]         |
| [Chinese (Traditional)] | [errors_zh_TW.xliff] | [N]  | [N]   | [N]           | [N]             | [N]         |
| [Japanese]              | [errors_ja.xliff]    | [N]  | [N]   | [N]           | [N]             | [N]         |
| [Korean]                | [errors_ko.xliff]    | [N]  | [N]   | [N]           | [N]             | [N]         |
| [French (France)]       | [errors_fr_FR.xliff] | [N]  | [N]   | [N]           | [N]             | [N]         |
| [French (Canada)]       | [errors_fr_CA.xliff] | [N]  | [N]   | [N]           | [N]             | [N]         |

---

## 5. API Error Message Localization

> Backend APIs return error messages in the response body. The `Accept-Language` header or per-user locale preference determines which locale file is used.

| Error Category          | Keys Extracted | Localized? | Notes                    |
| ----------------------- | -------------- | ---------- | ------------------------ |
| Authentication errors   | [N]            | Yes / No   | 401 responses            |
| Authorization errors    | [N]            | Yes / No   | 403 responses            |
| Validation errors       | [N]            | Yes / No   | 400 responses            |
| Not found errors        | [N]            | Yes / No   | 404 responses            |
| Rate limit errors       | [N]            | Yes / No   | 429 responses            |
| Server errors           | [N]            | Yes / No   | 500 responses (generic)  |

---

## 6. Developer Portal Content Localization

> The developer portal (API documentation, guides, quickstarts) must be localized for all target markets.

| Content Type            | Keys Extracted | Localized? | Notes                    |
| ----------------------- | -------------- | ---------- | ------------------------ |
| API endpoint descriptions | [N]          | Yes / No   | OpenAPI description fields|
| Getting started guide   | [N]            | Yes / No   | Markdown + frontmatter   |
| Authentication guide    | [N]            | Yes / No   | OAuth/API key docs        |
| Error reference         | [N]            | Yes / No   | Error code catalog        |
| SDK documentation       | [N]            | Yes / No   | Per-SDK language docs     |
| FAQ                     | [N]            | Yes / No   | Common questions          |

---

## 7. Outstanding Issues

| Issue ID | Description                                                   | Severity | Assigned To | Resolution Target |
| -------- | ------------------------------------------------------------- | -------- | ----------- | ----------------- |
| EXT-001  | [e.g., "3 hardcoded error messages remaining in auth module"] | [P1/P2]  | [Name]      | [Date]            |
| EXT-002  | [e.g., "Key naming exception: err.2fa.invalid -- needs rename"] | [P2]   | [Name]      | [Date]            |

---

## 8. Handoff Certification

**I certify that:**

- [x] All localizable strings have been extracted from the codebase
- [x] Localization JSON files have been generated for all content types
- [x] key-index.csv is complete and validated
- [x] Translation packages are ready for TMS ingestion
- [x] All outstanding issues are documented with severity and ownership

---

**Prepared by Internationalization Specialist (Tomas Dvoracek) on YYYY-MM-DD**
**Reviewed and accepted by CTO-L (Dr. Amara Osei-Mensah) on YYYY-MM-DD**

> **Phase B begins upon CTO-L acceptance.** The Localization Department ingests the translation packages into the TMS and begins the five-phase Language Translation Module process.
