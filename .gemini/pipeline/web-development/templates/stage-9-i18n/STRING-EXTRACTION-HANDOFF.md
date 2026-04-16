# String Extraction Handoff

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 5/9 — String Extraction Readiness

---

## 1. Audit Summary

| Metric                              | Value           |
| ----------------------------------- | --------------- |
| **Total strings found**             | [N]             |
| **Hardcoded strings remaining**     | [N]             |
| **Hardcoded strings as % of total** | [X]%            |
| **Threshold**                       | ≤5%             |
| **Pass/Fail**                       | ☐ Pass / ☐ Fail |

---

## 2. Platform Resource Files

| Platform | Resource File Format       | Location          | String Count | Generated?   | Validated?   |
| -------- | -------------------------- | ----------------- | ------------ | ------------ | ------------ |
| Web (EN) | `locales/en/messages.json` | `src/locales/en/` | [N]          | ☐ Yes / ☐ No | ☐ Yes / ☐ No |
| Web (ZH) | `locales/zh/messages.json` | `src/locales/zh/` | [N]          | ☐ Yes / ☐ No | ☐ Yes / ☐ No |
| Web (JA) | `locales/ja/messages.json` | `src/locales/ja/` | [N]          | ☐ Yes / ☐ No | ☐ Yes / ☐ No |
| Web (KO) | `locales/ko/messages.json` | `src/locales/ko/` | [N]          | ☐ Yes / ☐ No | ☐ Yes / ☐ No |
| Web (FR) | `locales/fr/messages.json` | `src/locales/fr/` | [N]          | ☐ Yes / ☐ No | ☐ Yes / ☐ No |

---

## 3. key-index.csv Parity

| Language    | Key Count | Matches EN?  | Missing Keys | Extra Keys |
| ----------- | --------- | ------------ | ------------ | ---------- |
| EN (source) | [N]       | —            | —            | —          |
| ZH          | [N]       | ☐ Yes / ☐ No | [N]          | [N]        |
| JA          | [N]       | ☐ Yes / ☐ No | [N]          | [N]        |
| KO          | [N]       | ☐ Yes / ☐ No | [N]          | [N]        |
| FR          | [N]       | ☐ Yes / ☐ No | [N]          | [N]        |

---

## 4. String Key Naming Convention

Format: `{feature}.{screen}.{component}.{property}`

| Example Key                 | Value                  | Location                            |
| --------------------------- | ---------------------- | ----------------------------------- |
| `auth.login.submitLabel`    | "Sign In"              | `src/components/auth/LoginForm.tsx` |
| `dashboard.welcome.message` | "Welcome back, {name}" | `src/pages/Dashboard.tsx`           |

---

## 5. Hardcoded String Exceptions

| String   | Location    | Reason                                         | Classification       |
| -------- | ----------- | ---------------------------------------------- | -------------------- |
| [String] | [File:line] | [Brand name / technical constant / error code] | [Approved exception] |

---

## 6. Remaining Hardcoded Strings

| String   | Location    | Severity                       | Assigned To | Target Date |
| -------- | ----------- | ------------------------------ | ----------- | ----------- |
| [String] | [File:line] | P1 (core flow) / P2 (non-core) | [Name]      | [Date]      |

---

## 7. Placeholder Integrity

| String Key             | Placeholders         | Validated?   |
| ---------------------- | -------------------- | ------------ |
| `auth.welcome.message` | `{name}`             | ☐ Yes / ☐ No |
| `order.summary.total`  | `{count}`, `{price}` | ☐ Yes / ☐ No |

---

## 8. Text Expansion Risk

| Language | Avg Expansion vs EN | Risk Strings (>40% increase) | Mitigation                         |
| -------- | ------------------- | ---------------------------- | ---------------------------------- |
| German   | +25-35%             | [N] strings                  | [CSS truncation / flexible layout] |
| French   | +15-25%             | [N] strings                  | [CSS truncation / flexible layout] |

---

## 9. Sign-Off

| Role            | Name | Signature | Date       |
| --------------- | ---- | --------- | ---------- |
| I18n Specialist |      |           | YYYY-MM-DD |
| Frontend Lead   |      |           | YYYY-MM-DD |
| CTO             |      |           | YYYY-MM-DD |
