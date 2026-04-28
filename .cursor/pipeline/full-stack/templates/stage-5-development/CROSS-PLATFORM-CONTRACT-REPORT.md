# Cross-Platform Contract Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Full-Stack Cross-Platform (P3)
**Stage:** 5 — Software Development

---

## Purpose

This report verifies API parity across all platforms and validates shared data model consistency.

---

## API Parity Verification

| Endpoint / Feature | Web Client     | iOS Client     | Android Client | Backend        | Parity? |
| ------------------ | -------------- | -------------- | -------------- | -------------- | ------- |
| [GET /api/users]   | ✅ Implemented | ✅ Implemented | ✅ Implemented | ✅ Implemented | ✅ Yes  |
| [POST /api/auth]   | ✅ Implemented | ✅ Implemented | ✅ Implemented | ✅ Implemented | ✅ Yes  |
| [Feature X]        | ✅ Implemented | ☐ Missing      | ☐ Missing      | ✅ Implemented | ❌ No   |

## Shared Data Model Verification

| Model / Schema    | Web Client | iOS Client | Android Client | Backend   | Consistent? |
| ----------------- | ---------- | ---------- | -------------- | --------- | ----------- |
| User schema       | ✅ Matches | ✅ Matches | ✅ Matches     | ✅ Source | ✅ Yes      |
| Auth token schema | ✅ Matches | ✅ Matches | ✅ Matches     | ✅ Source | ✅ Yes      |
| [Model X]         | ✅ Matches | ☐ Diverges | ✅ Matches     | ✅ Source | ❌ No       |

## Contract Verification Results

| Contract Test Suite | Total Tests | Passed | Failed | Coverage |
| ------------------- | ----------- | ------ | ------ | -------- |
| API contract (Pact) | [N]         | [N]    | [N]    | [XX]%    |
| Schema validation   | [N]         | [N]    | [N]    | [XX]%    |
| Cross-platform E2E  | [N]         | [N]    | [N]    | [XX]%    |

## Feature Coverage Analysis

| Feature     | Web | iOS | Android | Gap? | Severity | Remediation Plan        |
| ----------- | --- | --- | ------- | ---- | -------- | ----------------------- |
| [Feature 1] | ✅  | ✅  | ✅      | No   | —        | —                       |
| [Feature 2] | ✅  | ☐   | ☐       | Yes  | P2       | Assign to mobile tracks |
| [Feature 3] | ✅  | ✅  | ☐       | Yes  | P2       | Assign to Android track |

## Platform Divergence Issues

| Issue                     | Platform(s) Missing | Severity | Root Cause | Remediation Plan | Target Date |
| ------------------------- | ------------------- | -------- | ---------- | ---------------- | ----------- |
| [Feature not implemented] | [iOS, Android]      | [P2/P3]  | [Cause]    | [Plan]           | YYYY-MM-DD  |

## Sign-Off

| Role             | Name | Signature | Date       |
| ---------------- | ---- | --------- | ---------- |
| Integration Lead |      |           | YYYY-MM-DD |
| Frontend Lead    |      |           | YYYY-MM-DD |
| Backend Lead     |      |           | YYYY-MM-DD |
| Mobile Lead      |      |           | YYYY-MM-DD |
| CTO              |      |           | YYYY-MM-DD |
