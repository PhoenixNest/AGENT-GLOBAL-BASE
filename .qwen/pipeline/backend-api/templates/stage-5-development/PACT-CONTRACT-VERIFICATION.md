# Contract Verification Report (Backend API)

**Project:** [Project Name]
**Component:** Backend API Service
**Author:** Backend Lead
**Reviewers:** Frontend Lead (Web Consumer), Security Lead
**Date:** YYYY-MM-DD
**Checkpoint:** [30% Contract Verification / 70% Integration Verification]
**Version:** v1

> **Note:** This report is produced twice per Stage 5 -- at 30% (Contract Verification) and 70% (Integration Verification). Each checkpoint creates a new version. Increment the version number for the second checkpoint.

---

## Purpose

This report verifies that the backend API's public contract (OpenAPI/Swagger specification) correctly serves all API consumers: web frontend, mobile clients, and third-party integrations. Conducted at 30% and 70% Stage 5 completion milestones per the API Contract ADR.

---

## 1. API Contract Definition

| Contract Item                    | Description              | Input Schema         | Output Schema        | Web Frontend Support? | Third-Party Support? | Status                |
| -------------------------------- | ------------------------ | -------------------- | -------------------- | --------------------- | -------------------- | --------------------- |
| [e.g., GET /api/users/:id]       | [Fetches user profile]   | [path: userId]       | [UserResponse]       | Yes / No              | Yes / No             | Verified / Failed     |
| [e.g., POST /api/auth/login]     | [Authenticate user]      | [LoginRequest body]  | [AuthResponse]       | Yes / No              | Yes / No             | Verified / Failed     |
| [e.g., GET /api/items?filter=]   | [List items with filter] | [query params]       | [ItemListResponse]   | Yes / No              | Yes / No             | Verified / Failed     |

---

## 2. Contract Changes Since Last Checkpoint

| Contract Item | Previous Definition | New Definition  | Breaking Change? | Consumer Impact              | Remediation       |
| ------------- | ------------------- | --------------- | ---------------- | ---------------------------- | ----------------- |
| [Item name]   | [Old signature]     | [New signature] | Yes / No         | [Web Frontend / Third-Party] | [Action required] |

> **Breaking changes must be communicated to all consumers within 24 hours.** Consumer leads acknowledge receipt and submit impact assessment within 48 hours.

---

## 3. Consumer Verification

### Web Frontend Consumer

| Contract Item | Integrated?  | Compiles/Builds? | Runtime Pass? | Notes   |
| ------------- | ------------ | ---------------- | ------------- | ------- |
| [Item name]   | Yes / No     | Yes / No         | Yes / No      | [Notes] |

### Third-Party API Consumer (if applicable)

| Contract Item | Integrated?  | Compiles/Builds? | Runtime Pass? | Notes   |
| ------------- | ------------ | ---------------- | ------------- | ------- |
| [Item name]   | Yes / No     | Yes / No         | Yes / No      | [Notes] |

### Internal Service Consumer (microservice architecture)

| Contract Item | Integrated?  | Compiles/Builds? | Runtime Pass? | Notes   |
| ------------- | ------------ | ---------------- | ------------- | ------- |
| [Item name]   | Yes / No     | Yes / No         | Yes / No      | [Notes] |

---

## 4. Security Contract Verification

| Security Control         | Defined in Spec? | Implemented in API? | Verified by Consumer? | Parity Confirmed? |
| ------------------------ | ---------------- | ------------------- | --------------------- | ----------------- |
| Authentication required  | Yes / No         | Yes / No            | Yes / No              | Yes / No          |
| Authorization scopes     | Yes / No         | Yes / No            | Yes / No              | Yes / No          |
| Error response format    | Yes / No         | Yes / No            | Yes / No              | Yes / No          |
| Rate limit headers       | Yes / No         | Yes / No            | Yes / No              | Yes / No          |
| Pagination format        | Yes / No         | Yes / No            | Yes / No              | Yes / No          |

---

## 5. Checkpoint Result

| Metric                     | 30% Checkpoint | 70% Checkpoint |
| -------------------------- | -------------- | -------------- |
| Total contract items       | [N]            | [N]            |
| Verified items             | [N]            | [N]            |
| Failed items               | [N]            | [N]            |
| Blocking issues            | [N]            | [N]            |
| Contract verification rate | [XX]%          | [XX]%          |

**Pass threshold:** >= 90% contract verification rate required to proceed. Any blocking issue must be resolved before the next checkpoint.

**Checkpoint result:** Pass -- proceed / Conditional Pass -- remediation plan attached / Fail -- STOP, resolve blocking issues

---

## 6. API Response Parity Report

> Verifies that API response formats are consistent across all consumer types.

### Response Format Consistency

| Metric                                    | Web Frontend | Third-Party API | Internal Service | Parity Confirmed? |
| ----------------------------------------- | ------------ | --------------- | ---------------- | ----------------- |
| Error response structure matches spec     | Yes / No     | Yes / No        | Yes / No         | Yes / No          |
| Pagination metadata format consistent     | Yes / No     | Yes / No        | Yes / No         | Yes / No          |
| Field naming convention (snake_case/camelCase) | Yes / No | Yes / No   | Yes / No         | Yes / No          |
| Date/time format consistent (ISO 8601)    | Yes / No     | Yes / No        | Yes / No         | Yes / No          |
| Null vs omit behavior documented          | Yes / No     | Yes / No        | Yes / No         | Yes / No          |

---

## 7. Sign-Off

| Role           | Name           | Sign-off                | Date       |
| -------------- | -------------- | ----------------------- | ---------- |
| Backend Lead   | [Name]         | Approved / Rejected     | YYYY-MM-DD |
| Frontend Lead  | [Name]         | Approved / Rejected     | YYYY-MM-DD |
| Security Lead  | [Name]         | Approved / Rejected     | YYYY-MM-DD |
