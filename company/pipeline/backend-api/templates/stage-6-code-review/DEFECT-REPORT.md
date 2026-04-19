# Defect Report

**Project:** [Project Name]
**Stage:** 6 -- Code Review
**Version:** v1
**Date:** YYYY-MM-DD
**Reviewed By:** CTO Panel (CPO, CTO, CIO, CSO) + Backend Lead + Security Lead

---

## Executive Summary

| Metric              | Value                |
| ------------------- | -------------------- |
| **Product advisor** | VP API (Alex Rivera) |
| Total defects found | [N]                  |
| P0 (non-negotiable) | [N]                  |
| P1 (non-negotiable) | [N]                  |
| P2 (user decides)   | [N]                  |
| P3 (user decides)   | [N]                  |
| Review rounds       | [N]                  |
| Sign-offs received  | [X/5]                |

---

## Pre-Tier 1 Automated Quality Gates

**These gates MUST pass before Tier 1 cross-review begins.** If any gate fails, Tier 1 is blocked.

| Gate            | Tool                               | Result                | Failure Details          | Status      |
| --------------- | ---------------------------------- | --------------------- | ------------------------ | ----------- |
| SAST            | Semgrep + CodeQL                   | [N findings]          | [Critical/High findings] | Pass / Fail |
| Secret scanning | gitleaks                           | [N secrets found]     | [Details]                | Pass / Fail |
| Dependency scan | Snyk / Dependabot                  | [N vulnerabilities]   | [Critical/High CVEs]     | Pass / Fail |
| Linting         | [ESLint / golangci-lint / ruff]    | [N violations]        | [Details]                | Pass / Fail |
| Unit tests      | [Go test / Jest / Vitest / pytest] | [N passed / N failed] | [Failed tests]           | Pass / Fail |

**Gate Result:** All gates passed -- Tier 1 may proceed / Gates failed -- remediate before Tier 1

---

## Defect Details

### P0 -- Critical

| ID     | Category                  | PRD Feature | Description   | Location      | Remediation    | Status       |
| ------ | ------------------------- | ----------- | ------------- | ------------- | -------------- | ------------ |
| P0-001 | [Security / Crash / Data] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | Open / Fixed |

### P1 -- Major

| ID     | Category            | PRD Feature | Description   | Location      | Remediation    | Status       |
| ------ | ------------------- | ----------- | ------------- | ------------- | -------------- | ------------ |
| P1-001 | [Core Feature / UX] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | Open / Fixed |

### P2 -- Minor (User Decision)

| ID     | Category           | PRD Feature | Description   | Location      | Remediation    | User Decision | Status       |
| ------ | ------------------ | ----------- | ------------- | ------------- | -------------- | ------------- | ------------ |
| P2-001 | [Cosmetic / Minor] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | Fix / Defer   | Open / Fixed |

### P3 -- Polish (User Decision)

| ID     | Category | PRD Feature | Description   | Location      | Remediation    | User Decision | Status       |
| ------ | -------- | ----------- | ------------- | ------------- | -------------- | ------------- | ------------ |
| P3-001 | [Polish] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | Fix / Defer   | Open / Fixed |

---

## Backend Lead Review Memo

| Aspect                       | Assessment                           | Details                       |
| ---------------------------- | ------------------------------------ | ----------------------------- |
| **Code quality**             | [Excellent / Good / Needs Work]      | [Specific observations]       |
| **Architecture conformance** | [Matches UML/ADR / Deviations noted] | [List deviations]             |
| **Security observations**    | [Findings]                           | [File-level references]       |
| **Test quality**             | [Adequate / Gaps noted]              | [Missing test areas]          |
| **API design quality**       | [RESTful / RPC style, consistency]   | [Endpoint naming, versioning] |
| **Key findings**             | [Top 3 concerns]                     | [Details]                     |

**Sign-off:** Approved / Approved with conditions / Rejected
**Conditions:** [List any]

---

## Security Lead Review Memo

| Aspect                    | Assessment                              | Details                    |
| ------------------------- | --------------------------------------- | -------------------------- |
| **Input validation**      | [All endpoints validated / Gaps]        | [Missing validations]      |
| **AuthZ enforcement**     | [Consistent / Gaps]                     | [Endpoints missing checks] |
| **SQL injection surface** | [All parameterized / Raw queries found] | [File references]          |
| **Dependency security**   | [All deps pinned / Vulnerable deps]     | [CVE details]              |
| **Log sanitization**      | [No sensitive data in logs / Leaks]     | [Log line references]      |
| **Key findings**          | [Top 3 security concerns]               | [Details]                  |

**Sign-off:** Approved / Approved with conditions / Rejected
**Conditions:** [List any]

---

## Architecture Compliance Audit (Layer 2 -- ADR/TSD Enforcement)

**Auditor:** Senior Architect (Dr. Elena Rostova)
**Date:** YYYY-MM-DD
**Scope:** Independent audit of codebase against all Stage 3 ADRs and TSD

### ADR Compliance Audit

| ADR                              | Compliant? | Deviations Found | Defect IDs | Notes |
| -------------------------------- | ---------- | ---------------- | ---------- | ----- |
| ADR-NNN (Platform Strategy)      | Yes / No   | [N]              | [P#-XXX]   |       |
| ADR-NNN (String Key Taxonomy)    | Yes / No   | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: Cryptography) | Yes / No   | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: API Security) | Yes / No   | [N]              | [P#-XXX]   |       |
| ADR-NNN (Data Model)             | Yes / No   | [N]              | [P#-XXX]   |       |
| ADR-NNN (Error Handling)         | Yes / No   | [N]              | [P#-XXX]   |       |
| TSD vN                           | Yes / No   | [N]              | [P#-XXX]   |       |

**Audit Result:** Pass / Fail -- [N] ADR deviations found
**Signed by Senior Architect (Dr. Elena Rostova) on YYYY-MM-DD**

---

## API Conformance Matrix

Row-by-row mapping of every API specification item (OpenAPI/Swagger) to its implementation status. Completed during Stage 6 Code Review.

### Endpoint Conformance

| Spec Section | Endpoint               | Implemented? | Matches Spec? | Deviation Notes          | Defect ID (if any) |
| ------------ | ---------------------- | ------------ | ------------- | ------------------------ | ------------------ |
| API §3.1     | [GET /api/users/:id]   | Yes / No     | Yes / No      | [Describe any deviation] | [P#-XXX or None]   |
| API §3.2     | [POST /api/auth/login] | Yes / No     | Yes / No      | [Describe any deviation] | [P#-XXX or None]   |

### Request/Response Conformance

| Spec Section | Endpoint      | Direction | Schema Matches? | Status Codes Correct? | Headers Present? | Defect ID (if any) |
| ------------ | ------------- | --------- | --------------- | --------------------- | ---------------- | ------------------ |
| API §4       | [GET /items]  | Response  | Yes / No        | Yes / No              | Yes / No         | [P#-XXX or None]   |
| API §4       | [POST /items] | Request   | Yes / No        | Yes / No              | Yes / No         | [P#-XXX or None]   |

### Error Response Conformance

| Error Code | Documented in Spec? | Consistent Format? | Includes trace_id? | Includes helpful message? | Defect ID (if any) |
| ---------- | ------------------- | ------------------ | ------------------ | ------------------------- | ------------------ |
| 400        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |
| 401        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |
| 403        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |
| 404        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |
| 429        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |
| 500        | Yes / No            | Yes / No           | Yes / No           | Yes / No                  | [P#-XXX or None]   |

### Pagination Conformance

| Endpoint         | Uses Consistent Format? | Meta Object Present? | Links Object Present? | Page Size Honors Limit? | Defect ID (if any) |
| ---------------- | ----------------------- | -------------------- | --------------------- | ----------------------- | ------------------ |
| [GET /api/items] | Yes / No                | Yes / No             | Yes / No              | Yes / No                | [P#-XXX or None]   |
| [GET /api/users] | Yes / No                | Yes / No             | Yes / No              | Yes / No                | [P#-XXX or None]   |

### Security Header Conformance

| Header                      | Present? | Correct Value? | Defect ID (if any) |
| --------------------------- | -------- | -------------- | ------------------ |
| `Strict-Transport-Security` | Yes / No | Yes / No       | [P#-XXX or None]   |
| `X-Content-Type-Options`    | Yes / No | Yes / No       | [P#-XXX or None]   |
| `X-Frame-Options`           | Yes / No | Yes / No       | [P#-XXX or None]   |
| `Content-Security-Policy`   | Yes / No | Yes / No       | [P#-XXX or None]   |

### Conformance Summary

| Category         | Total Items | Compliant | Minor Deviation | Major Deviation | Not Implemented | Conformance % |
| ---------------- | ----------- | --------- | --------------- | --------------- | --------------- | ------------- |
| Endpoints        | [N]         | [N]       | [N]             | [N]             | [N]             | [XX]%         |
| Request/Response | [N]         | [N]       | [N]             | [N]             | [N]             | [XX]%         |
| Error Responses  | [N]         | [N]       | [N]             | [N]             | [N]             | [XX]%         |
| Pagination       | [N]         | [N]       | [N]             | [N]             | [N]             | [XX]%         |
| Security Headers | [N]         | [N]       | [N]             | [N]             | [N]             | [XX]%         |
| **Overall**      | **[N]**     | **[N]**   | **[N]**         | **[N]**         | **[N]**         | **[XX]%**     |

**Overall conformance >= 95% required for sign-off.** Any "Major Deviation" or "Not Implemented" item is automatically classified as at least **P1** (P0 if it blocks a core API flow or creates a security vulnerability).

---

## C-Suite Panel Sign-Off

| Role | Name                | Sign-off | Date |
| ---- | ------------------- | -------- | ---- |
| CPO  | Marcus Tran-Yoshida | Yes / No |      |
| CTO  | Dr. Kenji Nakamura  | Yes / No |      |
| CIO  | Dr. Priya Mehta     | Yes / No |      |
| CSO  | Dr. Sarah Chen      | Yes / No |      |

---

**All P0 and P1 defects must be resolved before advancement.**
**User has made decisions on all P2/P3 defects.**
**Remediation completed and re-review passed on YYYY-MM-DD**
