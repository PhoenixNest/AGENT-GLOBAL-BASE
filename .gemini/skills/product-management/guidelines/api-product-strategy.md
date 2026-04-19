---
name: api-product-strategy
description: Specialized strategy for API-as-a-Product, covering OpenAPI standards, SDK ergonomics, Developer Experience (DX) KPIs, API pricing models, and the deprecation lifecycle. Use this skill when authoring Section 5 of an API-focused PRD or when defining developer platform roadmaps.
---

# API Product Strategy

Alex Rivera (VP API) leads the API and Developer Platform strategy, treating our APIs as first-class products. This skill defines how we build, scale, and maintain our developer interfaces.

---

## 1. OpenAPI Standards and Governance

Consistency across endpoints is the foundation of a good developer experience.

- **Contract-First Design:** Use OpenAPI (Swagger) specs as the source of truth _before_ implementation begins.
- **Naming Conventions:** Strict adherence to RESTful patterns (nouns for resources, plural naming, standard HTTP verbs).
- **Version Heterogeneity:** Ensure consistent header-based or URL-based versioning across all services.
- **Error Schemas:** Use standard RFC 7807 (Problem Details for HTTP APIs) for all error responses.

---

## 2. SDK Ergonomics and DX

An API is only as good as the tools used to consume it.

- **Language Idioms:** SDKs must feel native to the target language (e.g., Promises/Async-Await in JS, Types/Interfaces in TS).
- **Zero-Config Quickstarts:** A developer should be able to make their first successful API call in under 5 minutes.
- **Documentation:** Auto-generated reference docs must be supplemented by hand-written conceptual guides and "Use Case" tutorials.

---

## 3. Developer Experience (DX) KPIs

Measure what matters for developers:

- **TTHW (Time to Hello World):** Time from account creation to first successful API response.
- **Request Success Rate:** Percentage of non-4xx/5xx responses.
- **API Latency (p95/p99):** Critical for real-time integrations.
- **SDK Adoption Rate:** Percentage of traffic coming through official SDKs vs. raw HTTP calls.
- **Documentation NPS:** Qualitative feedback on the clarity and utility of docs.

---

## 4. API Pricing and Commercial Models

APIs require specific monetization strategies:

- **Tiered Usage:** Free/Developer tier (limited rate), Growth (pay-per-call), Enterprise (committed volume).
- **Rate Limiting:** Protect infrastructure while aligning with pricing (e.g., 10 req/sec for Free, 1000 req/sec for Enterprise).
- **Overage Logic:** Define behavior when limits are exceeded (Hard-stop vs. Soft-cap with billing).

---

## 5. Deprecation and Version Lifecycle

Breaking changes are the leading cause of developer churn.

- **Sunset Policy:** Minimum 6-month notice for deprecation of major versions.
- **Deprecation Headers:** Use `Deprecation` and `Link` headers to notify developers in-band.
- **Migration Guides:** Every major version increment must be accompanied by a step-by-step migration path.
- **LTS (Long Term Support):** Identify specific versions that will receive security patches for 12+ months.

---

## 6. API-Specific PRD Extension (Section 5)

When authoring Section 5 for an API PRD, document:

- **Endpoint Definition:** (Verbs, Paths, Auth requirements).
- **Request/Response Schemas:** (Reference to OpenAPI spec or draft JSON).
- **Rate Limits:** (Per-tier limits).
- **Breaking Change Assessment:** (Is this a new version or a backward-compatible update?).
- **SDK Impact:** (Which SDKs need updates?).
