# ADR: Web Security Patterns

| Field         | Value                                            |
| ------------- | ------------------------------------------------ |
| **Status**    | Proposed                                         |
| **Context**   | Stage 3 — Web Application Pipeline               |
| **Decision**  | Web-specific security patterns                   |
| **Date**      | YYYY-MM-DD                                       |
| **Authors**   | CSO (primary), Security Architect, Frontend Lead |
| **Reviewers** | CTO, CIO, Frontend Lead                          |

---

## Decision

[State the chosen security patterns for the web application.]

## XSS Prevention Strategy

| Pattern                 | Implementation           | Coverage               |
| ----------------------- | ------------------------ | ---------------------- |
| Content Security Policy | CSP header configuration | All pages              |
| Input sanitization      | [Library/approach]       | All user inputs        |
| Output encoding         | [Library/approach]       | All DOM insertions     |
| DOMPurify / equivalent  | [Yes/No — which library] | User-generated content |

## CSRF Protection

| Mechanism         | Implementation                       | Scope                       |
| ----------------- | ------------------------------------ | --------------------------- |
| CSRF tokens       | [Approach: same-site cookie / token] | All state-changing requests |
| SameSite cookies  | [Strict / Lax / None]                | Session cookies             |
| Origin validation | [Header check / middleware]          | API endpoints               |

## CSP Header Configuration

```
Content-Security-Policy: [policy directives]
```

| Directive       | Value              | Rationale                 |
| --------------- | ------------------ | ------------------------- |
| default-src     | ['self']           | Restrict resource loading |
| script-src      | ['self' ...]       | Allow trusted scripts     |
| style-src       | ['self' ...]       | Allow trusted styles      |
| img-src         | ['self' data: ...] | Allow images              |
| connect-src     | ['self' ...]       | Allow API connections     |
| frame-ancestors | ['none']           | Prevent clickjacking      |

## OAuth 2.0 Session Security

| Aspect               | Decision                            | Rationale            |
| -------------------- | ----------------------------------- | -------------------- |
| Token type           | [JWT / opaque]                      | [Rationale]          |
| Token storage        | [HttpOnly cookie / localStorage]    | [Security rationale] |
| Refresh strategy     | [Rotation / fixed expiry]           | [Rationale]          |
| Session invalidation | [Server-side blacklist / short TTL] | [Rationale]          |

## CORS Policy

| Origin              | Allowed? | Methods   | Credentials |
| ------------------- | -------- | --------- | ----------- |
| [Production domain] | Yes      | GET, POST | Yes         |
| [Staging domain]    | Yes      | GET, POST | Yes         |
| [Other]             | No       | —         | —           |

## Dependency Vulnerability Response

| Severity | SLA       | Response Action          |
| -------- | --------- | ------------------------ |
| Critical | <24 hours | Immediate patch + deploy |
| High     | <72 hours | Scheduled patch + deploy |
| Medium   | <1 sprint | Next sprint patch        |

## STRIDE Mapping

| Threat            | Pattern Addressed         | Verification Method        |
| ----------------- | ------------------------- | -------------------------- |
| XSS               | CSP + input sanitization  | ZAP DAST + manual pen test |
| CSRF              | CSRF tokens + SameSite    | ZAP DAST + automated tests |
| Session hijacking | Secure cookies + rotation | Security audit             |
| Clickjacking      | frame-ancestors: none     | Manual security review     |

---

**Lock-down:** Once approved at Stage 3 gate, these patterns are locked — weakening any pattern requires Stage 3 re-entry.
