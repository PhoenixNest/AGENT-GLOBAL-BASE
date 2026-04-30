---
name: api-governance
description: Define and enforce API lifecycle management — versioning policy, backward-compatibility standards, breaking-change classification, and graceful sunset procedures. Use when establishing API schema governance, authoring deprecation notices, or making versioning decisions that affect active integrations.
version: "1.0.0"
---

# API Governance

Alex Rivera (VP API) treats API governance as a brand promise. Every versioning decision, deprecation notice, and schema change is a product decision that affects the trust and productivity of every developer who integrates with the platform. This skill defines the standards, policies, and protocols for managing the full API lifecycle.

---

## 1. Versioning Policy

### Versioning Strategy: URI-Based Major Versions

All public APIs use **URI-based major version prefixes** (e.g., `/v1/`, `/v2/`). This is the company standard:

- **Predictable:** Developers can pin a version in their integration path.
- **Debuggable:** Logs and errors carry an unambiguous version identifier.
- **Independently deployable:** Multiple major versions can be served concurrently without routing ambiguity.

Minor and patch changes (non-breaking) are deployed without a version bump. Semantic versioning is tracked internally in the API changelog but not surfaced in the URL.

### Version Support Tiers

| Tier            | Status                                | SLA              |
| --------------- | ------------------------------------- | ---------------- |
| **Current**     | Fully supported; receives all updates | 100% uptime SLA  |
| **Maintenance** | Security and critical bug fixes only  | 99.9% uptime SLA |
| **Deprecated**  | No new fixes; sunset date published   | Best-effort      |
| **Sunset**      | Decommissioned; returns `410 Gone`    | None             |

A version enters **Maintenance** status the moment the next major version is released as **Current**. It enters **Deprecated** status 12 months after entering Maintenance. **Sunset** occurs no sooner than 6 months after the Deprecated announcement, giving developers a minimum 18-month total migration window from the release of the next major version.

---

## 2. Breaking vs. Non-Breaking Change Classification

Misclassifying a breaking change is a P0 product defect. Alex owns this classification in conjunction with the CTO and the Backend Chapter Lead.

### Non-Breaking Changes (deploy freely)

- Adding new optional fields to response payloads
- Adding new optional query parameters
- Adding new endpoints
- Expanding enum values (with caveats — see §3)
- Increasing rate limits
- Adding new error codes (not changing existing ones)

### Breaking Changes (require major version bump)

- Removing or renaming any field from a response payload
- Changing a field's data type (e.g., `string` → `integer`)
- Making a previously optional parameter required
- Removing or renaming an endpoint
- Changing the behavior of an existing operation in a way that alters expected outcomes
- Reducing rate limits
- Removing or changing enum values that consumers may have stored
- Changing authentication method or token format

**Gray Area Protocol:** When classification is disputed, Alex applies the "Postel's Law Test" — if a well-behaved existing client would break silently (no error, wrong behavior), it is a breaking change. If it would merely fail loudly (error response), context determines classification.

---

## 3. The Graceful Sunset Playbook

Developed at Stripe; adopted here as the company standard for any API version or endpoint deprecation.

### Phase 1 — Deprecation Announcement (Month 0)

1. Publish deprecation notice in the developer portal with:
   - The endpoint or version being deprecated
   - The sunset date (minimum 6 months from announcement)
   - The recommended migration path with code examples
   - A changelog entry in the API changelog
2. Add `Deprecation: true` and `Sunset: <RFC 7231 date>` headers to all responses from the deprecated surface.
3. Send direct notification to all API consumers who called the deprecated surface in the trailing 90 days (via registered developer email).

### Phase 2 — Active Migration Support (Months 1–4)

1. Publish a migration guide with side-by-side `v1` → `v2` code examples in all supported languages.
2. Provide a **migration compatibility shim** where feasible — a header or parameter that allows the old request shape to be translated server-side to the new one.
3. Track migration progress via the Developer Dashboard: graph of deprecated-endpoint call volume, by consumer. Target 80% migration by Month 4.

### Phase 3 — Final Warning (Month 5)

1. Direct email to all consumers still calling the deprecated surface.
2. Activate optional **sunset warnings in response payloads** — a non-fatal `warnings[]` array in the JSON response advising of the imminent sunset.
3. Internal escalation: Alex reviews the remaining un-migrated consumers; for enterprise accounts, initiate direct contact via account management.

### Phase 4 — Sunset (Month 6+)

1. The endpoint or version begins returning `410 Gone` with a body:
   ```json
   {
     "error": "endpoint_sunset",
     "message": "This endpoint was sunset on <date>. See <migration-guide-url> for the migration path.",
     "docs_url": "<migration-guide-url>"
   }
   ```
2. Sunset event is logged as a major changelog entry.
3. Alex conducts a post-mortem on migration completion rates; findings inform the timeline of the next deprecation cycle.

---

## 4. API Schema Governance

### OpenAPI-First Development

All new API endpoints begin with an **OpenAPI 3.1 specification** authored by Alex (for product requirements) and the Backend Chapter Lead (for implementation constraints) jointly. The specification is the source of truth — not the implementation.

**Gate:** The OpenAPI spec must be approved by Alex before any backend implementation begins. This is a Stage 3 input.

### Schema Review Checklist

Before any new endpoint ships:

- [ ] All fields have descriptions in the OpenAPI spec
- [ ] All error responses follow the company's standard error schema (`error`, `message`, `docs_url`, optional `param`)
- [ ] Idempotency patterns are documented for all mutating endpoints
- [ ] Pagination is implemented for all list endpoints (cursor-based, not offset)
- [ ] Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) are present on all responses
- [ ] All timestamps are ISO 8601 UTC
- [ ] All identifiers are string-typed (never bare integers in public APIs)

### Error Message Ergonomics Standard

A cryptic error code is a P0 UX defect. Every error response must:

- State **what** went wrong in plain language
- State **why** it went wrong (where safe to disclose)
- State **how** to fix it (or where to find documentation)
- Identify **which parameter** caused the error (for validation failures)

---

## 5. Developer Communication Protocol

API governance is only as strong as its communication. Alex owns the following channels:

| Channel                              | Content                                                             | Cadence                                       |
| ------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------- |
| **API Changelog**                    | All changes (breaking, deprecation, new features)                   | Per release                                   |
| **Developer Portal**                 | Migration guides, version support table, deprecation notices        | Per deprecation                               |
| **Email Notifications**              | Direct alerts to affected consumers                                 | On deprecation announcement + Month 5 warning |
| **`Deprecation` / `Sunset` Headers** | Machine-readable signals in API responses                           | From day of deprecation announcement          |
| **Stage 1 PRD**                      | New API surface spec, versioning decision, backward-compat analysis | Per initiative                                |

**Principle:** A developer who experiences a breaking change without warning has been failed by governance, not by their integration. Alex holds this standard personally.
