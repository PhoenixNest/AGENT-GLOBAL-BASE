# ADR: API Security — Storage

| Field         | Value                                        |
| ------------- | -------------------------------------------- |
| **Status**    | Proposed                                     |
| **Context**   | Stage 3 — Backend API Pipeline (P2)          |
| **Decision**  | Backend storage security patterns            |
| **Date**      | YYYY-MM-DD                                   |
| **Authors**   | CSO (primary), Security Architect, Data Lead |
| **Reviewers** | CTO, CIO, Backend Lead                       |

---

## Decision

[State the chosen storage security patterns for the backend API.]

## Database Encryption at Rest

| Data Type           | Encryption Method        | Key Management  | Rationale                |
| ------------------- | ------------------------ | --------------- | ------------------------ |
| User credentials    | bcrypt / argon2 (hashed) | N/A (hashing)   | Industry standard        |
| PII                 | AES-256 (column-level)   | KMS / Vault     | Regulatory compliance    |
| Session tokens      | Encrypted (if stored)    | Application key | Security in transit+rest |
| Application secrets | Encrypted at rest        | HashiCorp Vault | Centralized management   |

## KMS Integration

| Aspect         | Decision                        | Rationale   |
| -------------- | ------------------------------- | ----------- |
| Key management | [AWS KMS / GCP KMS / Vault]     | [Rationale] |
| Key rotation   | [Automatic / manual — interval] | [Rationale] |
| Access control | [IAM roles / service accounts]  | [Rationale] |

## Connection Pooling Security

| Aspect               | Decision                     | Rationale                  |
| -------------------- | ---------------------------- | -------------------------- |
| Pool size            | [Max connections]            | [Performance vs security]  |
| TLS to database      | [Yes/No]                     | [Encryption in transit]    |
| Credential injection | [Secrets manager / env vars] | [No hardcoded credentials] |

## Backup Encryption

| Aspect            | Decision                | Rationale              |
| ----------------- | ----------------------- | ---------------------- |
| Backup encryption | AES-256                 | Compliance requirement |
| Key storage       | Separate from data keys | Defense in depth       |
| Retention         | [X days/weeks/months]   | Recovery window        |

---

**Lock-down:** Once approved at Stage 3 gate, storage security patterns are locked — weakening any pattern requires Stage 3 re-entry.
