# ADR: Web Security — Storage

| Field         | Value                              |
| ------------- | ---------------------------------- |
| **Status**    | Proposed                           |
| **Context**   | Stage 3 — Web Application Pipeline |
| **Decision**  | Web storage security patterns      |
| **Date**      | YYYY-MM-DD                         |
| **Authors**   | CSO (primary), Security Architect  |
| **Reviewers** | CTO, CIO, Frontend Lead            |

---

## Decision

[State the chosen storage security patterns for the web application.]

## Cookie Security

| Attribute | Value               | Rationale                                      |
| --------- | ------------------- | ---------------------------------------------- |
| HttpOnly  | Yes                 | Prevent XSS from reading session cookies       |
| Secure    | Yes (HTTPS only)    | Prevent transmission over unencrypted channels |
| SameSite  | [Strict / Lax]      | Prevent CSRF attacks                           |
| Path      | [/]                 | Limit cookie scope                             |
| Domain    | [.example.com]      | Subdomain access control                       |
| Max-Age   | [Session / X hours] | Limit exposure window                          |

## localStorage / sessionStorage Security

| Data Type            | Storage Location | Encryption | Rationale                        |
| -------------------- | ---------------- | ---------- | -------------------------------- |
| Session tokens       | HttpOnly cookie  | N/A        | More secure than localStorage    |
| User preferences     | localStorage     | No         | Non-sensitive data               |
| Cached API responses | sessionStorage   | No         | Session-scoped, cleared on close |
| PII                  | Server-side only | N/A        | Never store PII client-side      |

## IndexedDB Security

| Aspect             | Decision                     | Rationale            |
| ------------------ | ---------------------------- | -------------------- |
| Data stored        | [What data goes here?]       | [Why IndexedDB?]     |
| Encryption at rest | [Yes/No — which approach]    | [Security rationale] |
| Access control     | [Origin-scoped / additional] | [Why?]               |

## Server-Side Storage

| Data Type           | Storage            | Encryption at Rest | Access Control  |
| ------------------- | ------------------ | ------------------ | --------------- |
| User credentials    | [Database/system]  | bcrypt / argon2    | AuthZ enforced  |
| Session state       | [Redis / DB]       | TLS in transit     | Token-bound     |
| PII                 | [Encrypted DB]     | AES-256            | Role-based      |
| Application secrets | [Vault / env vars] | Encrypted          | Service account |

## Data Breach Response

| Severity | SLA       | Response Action                  |
| -------- | --------- | -------------------------------- |
| Critical | <1 hour   | Incident response team activated |
| High     | <4 hours  | Contain + assess impact          |
| Medium   | <24 hours | Investigate + remediate          |

---

**Lock-down:** Once approved at Stage 3 gate, storage security patterns are locked — weakening any pattern requires Stage 3 re-entry.
