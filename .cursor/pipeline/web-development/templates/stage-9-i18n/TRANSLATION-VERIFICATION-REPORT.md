# Translation Verification Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 9 — i18n Engineering

---

## 1. Translation Summary

| Metric                          | Value            |
| ------------------------------- | ---------------- |
| **Source language**             | English (EN-US)  |
| **Target languages**            | [ZH, JA, KO, FR] |
| **Total source strings**        | [N]              |
| **Translation completion rate** | [XX]%            |
| **BLEU threshold**              | ≥ 0.80           |

---

## 2. Translation Quality Scores

| Language | BLEU Score | TER Score | Pass/Fail       | Notes |
| -------- | ---------- | --------- | --------------- | ----- |
| ZH-CN    | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |
| ZH-TW    | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |
| JA       | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |
| KO       | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |
| FR-FR    | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |
| FR-CA    | [0.XX]     | [XX]%     | ☐ Pass / ☐ Fail |       |

---

## 3. Platform Resource File Validation

| Platform | Resource File              | Validated?   | Issues          |
| -------- | -------------------------- | ------------ | --------------- |
| Web (EN) | `locales/en/messages.json` | ☐ Yes / ☐ No | [Issues if any] |
| Web (ZH) | `locales/zh/messages.json` | ☐ Yes / ☐ No | [Issues if any] |
| Web (JA) | `locales/ja/messages.json` | ☐ Yes / ☐ No | [Issues if any] |
| Web (KO) | `locales/ko/messages.json` | ☐ Yes / ☐ No | [Issues if any] |
| Web (FR) | `locales/fr/messages.json` | ☐ Yes / ☐ No | [Issues if any] |

**Validation checks:**

- All keys present in all language files
- No empty/missing values
- Placeholder integrity (`{name}`, `{count}`, etc. preserved)
- No broken JSON syntax

---

## 4. Text Expansion & Truncation

| Language | Avg Expansion vs EN       | Truncation Threshold | Strings Exceeding Threshold | UI Issues Found              |
| -------- | ------------------------- | -------------------- | --------------------------- | ---------------------------- |
| ZH       | -30 to -40% (compression) | N/A (compresses)     | 0                           | [None]                       |
| JA       | -20 to -30% (compression) | N/A (compresses)     | 0                           | [None]                       |
| KO       | -10 to -20% (compression) | N/A (compresses)     | 0                           | [None]                       |
| FR-FR    | +15 to +25%               | 40%                  | [N]                         | [UI overflow in buttons/nav] |
| FR-CA    | +20 to +30%               | 40%                  | [N]                         | [UI overflow in buttons/nav] |

---

## 5. Locale-Specific Formatting

| Locale | Date Format    | Number Format | Currency   | Register/Tone        | Platform Conventions      |
| ------ | -------------- | ------------- | ---------- | -------------------- | ------------------------- |
| ZH-CN  | yyyy/MM/dd     | 1,000.50      | ¥100       | Simplified, neutral  | [Web conventions]         |
| ZH-TW  | yyyy/MM/dd     | 1,000.50      | NT$100     | Traditional, neutral | [Web conventions]         |
| JA     | yyyy年MM月dd日 | 1,000.50      | ¥100       | Desu-Masu (polite)   | [Web conventions]         |
| KO     | yyyy.MM.dd     | 1,000.50      | ₩100       | Polite (해요체)      | [Web conventions]         |
| FR-FR  | dd/MM/yyyy     | 1 000,50      | 100,00 €   | Formal (vouvoiement) | [Web: use guillemets « »] |
| FR-CA  | yyyy-MM-dd     | 1 000,50      | 100,00 $CA | Formal               | [Web conventions]         |

---

## 6. Accessibility Labels Localized

| Label Type         | EN  | ZH  | JA  | KO  | FR  | All Localized? |
| ------------------ | --- | --- | --- | --- | --- | -------------- |
| ARIA labels        | [N] | [N] | [N] | [N] | [N] | ☐ Yes / ☐ No   |
| Alt text           | [N] | [N] | [N] | [N] | [N] | ☐ Yes / ☐ No   |
| Screen reader text | [N] | [N] | [N] | [N] | [N] | ☐ Yes / ☐ No   |

---

## 7. Commercial Copy Localized

| Content Type      | EN  | ZH  | JA  | KO  | FR  | All Localized? |
| ----------------- | --- | --- | --- | --- | --- | -------------- |
| Marketing text    | ☐   | ☐   | ☐   | ☐   | ☐   | ☐ Yes / ☐ No   |
| Legal disclaimers | ☐   | ☐   | ☐   | ☐   | ☐   | ☐ Yes / ☐ No   |
| Terms of service  | ☐   | ☐   | ☐   | ☐   | ☐   | ☐ Yes / ☐ No   |
| Privacy policy    | ☐   | ☐   | ☐   | ☐   | ☐   | ☐ Yes / ☐ No   |

---

## 8. Defects Found

| Defect ID | Language   | Description   | Severity    | Status               |
| --------- | ---------- | ------------- | ----------- | -------------------- |
| I18N-001  | [Language] | [Description] | P0/P1/P2/P3 | ☐ Open / ✅ Resolved |

---

## 9. Sign-Off

| Role              | Name | Signature | Date       |
| ----------------- | ---- | --------- | ---------- |
| CTO-L             |      |           | YYYY-MM-DD |
| Chinese Linguist  |      |           | YYYY-MM-DD |
| Japanese Linguist |      |           | YYYY-MM-DD |
| Korean Linguist   |      |           | YYYY-MM-DD |
| French Linguist   |      |           | YYYY-MM-DD |
| English QA        |      |           | YYYY-MM-DD |
