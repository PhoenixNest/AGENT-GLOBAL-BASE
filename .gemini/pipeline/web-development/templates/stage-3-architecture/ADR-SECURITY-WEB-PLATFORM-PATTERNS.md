# ADR: Web Platform Security Patterns

| Field         | Value                                            |
| ------------- | ------------------------------------------------ |
| **Status**    | Proposed                                         |
| **Context**   | Stage 3 — Web Application Pipeline (P1)          |
| **Decision**  | Web platform-specific security patterns          |
| **Date**      | YYYY-MM-DD                                       |
| **Authors**   | CSO (primary), Security Architect, Frontend Lead |
| **Reviewers** | CTO, CIO, Frontend Lead                          |

---

## Decision

[State the chosen web platform-specific security patterns.]

## URL Routing Security

| Pattern              | Implementation             | Coverage             |
| -------------------- | -------------------------- | -------------------- |
| Route validation     | [Server-side route guards] | All routes           |
| Deep link protection | [Auth-required deep links] | Protected routes     |
| 404 handling         | [Generic error pages]      | All unmatched routes |

## Service Worker Security

| Pattern              | Implementation                     | Scope                    |
| -------------------- | ---------------------------------- | ------------------------ |
| SW scope restriction | [Scope-limited registration]       | App-specific paths only  |
| SW update strategy   | [Skip-waiting / user prompt]       | On new version available |
| SW cache integrity   | [Cache-busting / versioned assets] | All cached resources     |
| SW offline fallback  | [Offline page / cached shell]      | Critical paths only      |

## Push Notification Security

| Pattern                  | Implementation                | Rationale                 |
| ------------------------ | ----------------------------- | ------------------------- |
| Push subscription auth   | [VAPID keys]                  | Prevent unauthorized push |
| Payload encryption       | [AES-GCM / web push protocol] | Encrypt notification data |
| Notification permissions | [User-gated, context-aware]   | Prevent spam/abuse        |

## PWA-Specific Security

| Pattern                   | Implementation            | Rationale                  |
| ------------------------- | ------------------------- | -------------------------- |
| manifest.json integrity   | [CSP for manifest]        | Prevent manifest tampering |
| Install prompt security   | [User-initiated only]     | Prevent forced installs    |
| App identity verification | [origin trial / verified] | Ensure app authenticity    |

## Content Security Policy (Web-Specific)

| Directive   | Value                   | Rationale                          |
| ----------- | ----------------------- | ---------------------------------- |
| script-src  | ['self' + trusted CDNs] | Prevent XSS from untrusted scripts |
| worker-src  | ['self']                | Restrict service worker sources    |
| connect-src | ['self' + API domains]  | Restrict outbound connections      |
| frame-src   | ['none' / trusted]      | Prevent clickjacking via iframes   |

## STRIDE Mapping

| Threat                 | Web Platform Attack Vector     | Mitigation                                         |
| ---------------------- | ------------------------------ | -------------------------------------------------- |
| Spoofing               | Fake PWA install prompts       | Manifest verification, origin checks               |
| Tampering              | Service worker injection       | SW scope restriction, integrity checks             |
| Repudiation            | Push notification forgery      | VAPID auth, payload encryption                     |
| Information Disclosure | SW cache poisoning             | Cache-busting, versioned assets                    |
| Denial of Service      | SW infinite loop / cache bloat | SW update strategy, cache limits                   |
| Elevation of Privilege | Route manipulation             | Server-side route guards, auth-required deep links |

---

**Lock-down:** Once approved at Stage 3 gate, these patterns are locked — weakening any pattern requires Stage 3 re-entry.
