# ADR: API Security Patterns

| Field         | Value                                           |
| ------------- | ----------------------------------------------- |
| **Status**    | Proposed                                        |
| **Context**   | Stage 3 — Backend API Pipeline (P2)             |
| **Decision**  | API-specific security patterns                  |
| **Date**      | YYYY-MM-DD                                      |
| **Authors**   | CSO (primary), Security Architect, Backend Lead |
| **Reviewers** | CTO, CIO, Backend Lead                          |

---

## Decision

[State the chosen security patterns for the API.]

## Rate Limiting

| Strategy     | Implementation                  | Thresholds          |
| ------------ | ------------------------------- | ------------------- |
| Per-client   | [Token bucket / sliding window] | [X requests/minute] |
| Per-endpoint | [Yes/No — which endpoints]      | [Thresholds]        |
| Global       | [Yes/No]                        | [Max throughput]    |

## Input Validation

| Pattern                      | Implementation                    | Coverage           |
| ---------------------------- | --------------------------------- | ------------------ |
| Schema validation            | [JSON Schema / Zod / Joi]         | All request bodies |
| SQL injection prevention     | [Parameterized queries / ORM]     | All DB queries     |
| Command injection prevention | [Input sanitization / allowlists] | All system calls   |

## AuthZ Enforcement

| Pattern             | Implementation                           | Scope                       |
| ------------------- | ---------------------------------------- | --------------------------- |
| Role-based access   | [RBAC / ABAC]                            | All endpoints               |
| Resource-level auth | [Yes/No — ownership checks]              | Protected resources         |
| Token validation    | [JWT verification / opaque token lookup] | All authenticated endpoints |

## CORS Policy

| Origin              | Allowed? | Methods   | Credentials |
| ------------------- | -------- | --------- | ----------- |
| [Production domain] | Yes      | GET, POST | Yes         |
| [Staging domain]    | Yes      | GET, POST | Yes         |
| [Other]             | No       | —         | —           |

## API Key Rotation

| Aspect            | Decision               | Rationale            |
| ----------------- | ---------------------- | -------------------- |
| Rotation interval | [X days / months]      | [Security rationale] |
| Delivery method   | [Header / query param] | [Rationale]          |
| Revocation        | [Immediate / delayed]  | [Rationale]          |

## Network Isolation

| Aspect            | Decision                 | Rationale   |
| ----------------- | ------------------------ | ----------- |
| VPC/VNet          | [Yes/No]                 | [Rationale] |
| Private endpoints | [Yes/No]                 | [Rationale] |
| WAF               | [Yes/No — which product] | [Rationale] |

---

**Lock-down:** Once approved at Stage 3 gate, these patterns are locked — weakening any pattern requires Stage 3 re-entry.
