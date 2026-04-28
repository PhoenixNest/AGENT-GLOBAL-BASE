# Contract Verification Report (KMP Shared Module / Flutter)

**Project:** [Project Name]
**Platform:** [KMP Shared Module / Flutter]
**Author:** Cross-Platform Lead (Mei-Ling Johansson)
**Reviewers:** Android Lead (Kofi Asante-Mensah), iOS Lead (Seo-Yeon Park)
**Date:** YYYY-MM-DD
**Checkpoint:** [30% Contract Verification / 70% Integration Verification]
**Version:** v1

> **Note:** This report is produced twice per Stage 5 — at 30% (Contract Verification) and 70% (Integration Verification). Each production creates a new version. Increment the version number for the second checkpoint.

---

## Purpose

This report verifies that the shared module's public API contract (KMP) or Flutter plugin interface correctly serves both platform consumers. Conducted at 30% and 70% Stage 5 completion milestones per the Platform Strategy ADR.

---

## 1. API Contract Definition

| Contract Item                    | Description            | Input Types      | Output Types       | Platform A Support? | Platform B Support? | Status                |
| -------------------------------- | ---------------------- | ---------------- | ------------------ | ------------------- | ------------------- | --------------------- |
| [e.g., UserRepository.getUser()] | [Fetches user profile] | [userId: String] | [User: data class] | ☐ Yes / ☐ No        | ☐ Yes / ☐ No        | ☐ Verified / ☐ Failed |
| [e.g., NetworkClient.post()]     | [HTTP POST with auth]  | [endpoint, body] | [Response]         | ☐ Yes / ☐ No        | ☐ Yes / ☐ No        | ☐ Verified / ☐ Failed |

---

## 2. Contract Changes Since Last Checkpoint

| Contract Item | Previous Definition | New Definition  | Breaking Change? | Platform Impact        | Remediation       |
| ------------- | ------------------- | --------------- | ---------------- | ---------------------- | ----------------- |
| [Item name]   | [Old signature]     | [New signature] | ☐ Yes / ☐ No     | [Android / iOS / Both] | [Action required] |

> **Breaking changes must be communicated to both platform leads within 24 hours.** Platform leads acknowledge receipt and submit impact assessment within 48 hours.

---

## 3. Platform Consumer Verification

### Android Consumer (Track A)

| Contract Item | Integrated?  | Compiles?    | Runtime Pass? | Notes   |
| ------------- | ------------ | ------------ | ------------- | ------- |
| [Item name]   | ☐ Yes / ☐ No | ☐ Yes / ☐ No | ☐ Yes / ☐ No  | [Notes] |

### iOS Consumer (Track B)

| Contract Item | Integrated?  | Compiles?    | Runtime Pass? | Notes   |
| ------------- | ------------ | ------------ | ------------- | ------- |
| [Item name]   | ☐ Yes / ☐ No | ☐ Yes / ☐ No | ☐ Yes / ☐ No  | [Notes] |

---

## 4. Security Contract Verification

| Security Control    | Defined in Contract? | Implemented in Shared Module? | Implemented in Platform A? | Implemented in Platform B? | Parity Confirmed? |
| ------------------- | -------------------- | ----------------------------- | -------------------------- | -------------------------- | ----------------- |
| Crypto delegation   | ☐ Yes / ☐ No         | ☐ Yes / ☐ No                  | ☐ Yes / ☐ No               | ☐ Yes / ☐ No               | ☐ Yes / ☐ No      |
| Auth token handling | ☐ Yes / ☐ No         | ☐ Yes / ☐ No                  | ☐ Yes / ☐ No               | ☐ Yes / ☐ No               | ☐ Yes / ☐ No      |
| Error sanitization  | ☐ Yes / ☐ No         | ☐ Yes / ☐ No                  | ☐ Yes / ☐ No               | ☐ Yes / ☐ No               | ☐ Yes / ☐ No      |

---

## 5. Checkpoint Result

| Metric                     | 30% Checkpoint | 70% Checkpoint |
| -------------------------- | -------------- | -------------- |
| Total contract items       | [N]            | [N]            |
| Verified items             | [N]            | [N]            |
| Failed items               | [N]            | [N]            |
| Blocking issues            | [N]            | [N]            |
| Contract verification rate | [XX]%          | [XX]%          |

**Pass threshold:** ≥ 90% contract verification rate required to proceed. Any blocking issue must be resolved before the next checkpoint.

**Checkpoint result:** ☐ Pass — proceed / ☐ Conditional Pass — remediation plan attached / ☐ Fail — STOP, resolve blocking issues

---

## 5. Cross-Platform String Parity Report

> Verifies that string keys are consistent across all platform resource files. Required for Both Native, KMP, and Flutter projects.

### Key Parity Check

| Metric                                                    | Android (strings.xml) | iOS (Localizable.strings) | KMP/Flutter (shared) | Parity Confirmed? |
| --------------------------------------------------------- | --------------------- | ------------------------- | -------------------- | ----------------- |
| Total keys                                                | [N]                   | [N]                       | [N]                  | ☐ Yes / ☐ No      |
| Keys with translation in all target languages             | [N]                   | [N]                       | [N]                  | ☐ Yes / ☐ No      |
| Missing keys (present in one platform, absent in another) | [N]                   | [N]                       | [N/A]                | ☐ Yes / ☐ No      |
| Placeholder format mismatches                             | [N]                   | [N]                       | [N]                  | ☐ Yes / ☐ No      |

### Translation Style Guide Compliance

| Language | Style Guide Followed? | Deviations | Impact  | Resolved?    |
| -------- | --------------------- | ---------- | ------- | ------------ |
| [ZH-CN]  | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |
| [ZH-TW]  | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |
| [JA]     | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |
| [KO]     | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |
| [FR-FR]  | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |
| [FR-CA]  | ☐ Yes / ☐ No          | [N]        | [UI/UX] | ☐ Yes / ☐ No |

**Parity result:** ☐ Pass — all platforms have equivalent string coverage / ☐ Fail — [N] key mismatches remaining

---

## 6. Sign-Off

| Role                | Name               | Sign-off                | Date       |
| ------------------- | ------------------ | ----------------------- | ---------- |
| Cross-Platform Lead | Mei-Ling Johansson | ☐ Approved / ☐ Rejected | YYYY-MM-DD |
| Android Lead        | Kofi Asante-Mensah | ☐ Approved / ☐ Rejected | YYYY-MM-DD |
| iOS Lead            | Seo-Yeon Park      | ☐ Approved / ☐ Rejected | YYYY-MM-DD |
