# API Contract Parity Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 5 — Software Development

---

## 1. Purpose

This report verifies API contract parity between the frontend consumer (Track W-FE) and backend provider (Track W-BE). It ensures all backend endpoints are correctly consumed by the frontend with matching request/response signatures.

---

## 2. API Contract Summary

| Contract | Version | Format | Consumers |
| -------- | ------- | ------ | --------- |
| [API name] | v[N] | [OpenAPI / GraphQL SDL / Pact] | [Web Frontend] |

---

## 3. Endpoint Parity Verification

| Endpoint | Method | Backend Provides | Frontend Consumes | Contract Matches? | Issues |
| -------- | ------ | --------------- | ----------------- | ----------------- | ------ |
| [GET /api/resource] | GET | ☐ Yes | ☐ Yes | ☐ Yes / ☐ No | [Issues if any] |
| [POST /api/resource] | POST | ☐ Yes | ☐ Yes | ☐ Yes / ☐ No | [Issues if any] |

---

## 4. Schema Parity Verification

| Field | Backend Schema | Frontend Type | Matches? | Issues |
| ----- | -------------- | ------------- | -------- | ------ |
| [field_name] | [Type, required/optional] | [TypeScript interface] | ☐ Yes / ☐ No | [Issues if any] |

---

## 5. Contract Breaking Changes

| Change | Old Signature | New Signature | Consumer Updated? | Affected Components | Action Required |
| ------ | ------------- | ------------- | ----------------- | ------------------- | --------------- |
| [Item name] | [Old signature] | [New signature] | ☐ Yes / ☐ No | [Component names] | [Action required] |

---

## 6. Frontend Consumer (Track W-FE)

| Metric | Value |
| ------ | ----- |
| Endpoints consumed | [N] / [Total backend endpoints] |
| Contract tests passing | [N] / [Total contract tests] |
| Type safety (TypeScript) | ☐ Full / ☐ Partial / ☐ None |
| Error handling coverage | [XX]% of error responses handled |

---

## 7. Backend Provider (Track W-BE)

| Metric | Value |
| ------ | ----- |
| Endpoints implemented | [N] / [Total planned] |
| Contract tests passing | [N] / [Total contract tests] |
| OpenAPI/Swagger docs current | ☐ Yes / ☐ No |
| Error response consistency | [XX]% consistent format |

---

## 8. String Parity (i18n)

| Metric | Frontend | Backend | Parity Confirmed? |
| ------ | -------- | ------- | ----------------- |
| Total string keys | [N] | — | — |
| Keys in key-index.csv | [N] | — | ☐ Yes / ☐ No |
| Error message keys | [N] | [N] | ☐ Yes / ☐ No |
| Placeholder format consistent | — | — | ☐ Yes / ☐ No |

---

## 9. Defects Found

| Defect ID | Severity | Description | Location | Assigned To | Target Date |
| --------- | -------- | ----------- | -------- | ----------- | ----------- |
| API-001 | [P1/P2] | [Description] | [Endpoint/Component] | [Name] | YYYY-MM-DD |

---

## 10. Sign-Off

| Role | Name | Signature | Date |
| ---- | ---- | --------- | ---- |
| Frontend Lead (W-FE) | | | YYYY-MM-DD |
| Backend Lead (W-BE) | | | YYYY-MM-DD |
| CTO | | | YYYY-MM-DD |
