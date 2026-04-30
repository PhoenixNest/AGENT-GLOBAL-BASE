---
name: developer-portal-and-devrel
description: Developer portal product strategy and developer relations — information architecture, recipe-based documentation, API sample app design, developer NPS measurement, and community feedback loops. Use when designing or improving the developer-facing portal, when evaluating documentation quality, or when defining the developer experience for a new API product.
version: "1.0.0"
---

# Developer Portal and DevRel

## Purpose

Own the developer portal as a **product** — not just a documentation site. The developer portal is the primary distribution channel for the platform's APIs; a poorly designed portal suppresses adoption regardless of API quality. Alex Rivera's role is to treat the developer experience (DX) the same way a consumer product manager treats the end-user experience: measure it, iterate on it, and hold it to an NPS standard.

## Why This Matters

API products live or die on their first-use experience. A developer who cannot get a "Hello World" response within 10 minutes in the quickstart will abandon the API and write their own solution or evaluate a competitor. Every extra hour of DX friction directly suppresses integration adoption.

## Developer Portal Information Architecture

The portal IA follows the **Divio documentation system** — four content types, each serving a distinct user need:

| Content Type                             | Question It Answers         | Examples                                                             | Owner                               |
| ---------------------------------------- | --------------------------- | -------------------------------------------------------------------- | ----------------------------------- |
| **Tutorials** (learning-oriented)        | "How do I get started?"     | Quickstart in 5 minutes, first API call, first webhook               | Alex Rivera                         |
| **How-To Guides** (task-oriented)        | "How do I achieve X?"       | Paginate results, handle rate limits, migrate from v2 to v3          | Alex Rivera + backend chapter leads |
| **Reference** (information-oriented)     | "What is X?"                | Full endpoint specifications, error code catalogue, rate limit table | Auto-generated from OpenAPI spec    |
| **Explanation** (understanding-oriented) | "Why does X work this way?" | Versioning strategy rationale, authentication model design           | Alex Rivera                         |

### Navigation Hierarchy

```
/docs
├── /quickstart                     → Tutorial: working API call in 5 minutes
├── /authentication                 → How-To + Explanation (OAuth 2.0, token management)
├── /api-reference                  → Auto-generated from OpenAPI (Redoc / Stoplight)
│   ├── /endpoints/{resource}
│   └── /errors                     → Full error code catalogue with resolution guidance
├── /guides                         → How-To library
│   ├── /pagination
│   ├── /webhooks
│   ├── /rate-limiting
│   └── /migration/v2-to-v3
├── /sample-apps                    → Working reference implementations
│   ├── /android                    → Kotlin + Retrofit sample
│   ├── /ios                        → Swift + URLSession sample
│   └── /web                        → TypeScript + fetch sample
├── /sdks                           → SDK download + changelog
│   ├── /android
│   ├── /ios
│   └── /javascript
├── /changelog                      → API changelog with migration notes per version
└── /status                         → API status page (uptime, incident history)
```

## Quickstart Standard

Every API product on the platform must have a quickstart that meets this standard:

**Target:** Developer reaches their first successful API response in ≤10 minutes from landing on `/quickstart`.

**Required elements:**

1. Prerequisites (one short list — max 5 items, no walls of text)
2. Authentication setup (copy-paste API key or OAuth flow — one path only in quickstart)
3. First API call (working cURL or language-specific snippet — copy-pasteable)
4. Expected response (actual JSON/response shown inline)
5. Next steps (3 links max to the most common next task)

**Quality gate:** Alex runs the quickstart on a freshly provisioned machine with no cached credentials before every API version release. If he cannot complete it in 10 minutes, it ships as a P1 documentation defect blocking release.

## Recipe-Based Documentation

Beyond the quickstart, the guide library follows a **recipe pattern** — each guide solves one specific problem a developer encounters in production:

````markdown
# How to Handle Rate Limits

## Problem

Your API calls are returning 429 Too Many Requests.

## Solution

Implement exponential backoff with jitter.

## Working Example

```kotlin
suspend fun callWithRetry(request: Request): Response {
    var delay = 1000L // ms
    repeat(5) { attempt ->
        val response = apiClient.execute(request)
        if (response.code != 429) return response
        val retryAfter = response.header("Retry-After")?.toLong() ?: delay
        delay(retryAfter + Random.nextLong(0, 1000)) // jitter
        delay *= 2
    }
    throw RateLimitException("Max retries exceeded")
}
```
````

## When to Use This

Use exponential backoff when...

## Common Mistakes

- ❌ Retrying immediately on 429 (thundering herd)
- ✅ Adding jitter to spread retry load

```

Recipes are added for every `429`, `401`, `403`, `500` error a developer will realistically encounter. The error code catalogue links to the relevant recipe.

## Sample Apps

Each platform API must have a maintained sample app in the three priority languages: Android (Kotlin), iOS (Swift), and Web (TypeScript). Sample apps are **production-quality reference implementations** — not toy demos.

**Sample app standards:**
- Builds from a single `README.md` command with no environment setup
- Uses the current SDK version (automated dependency update PR weekly)
- Covers authentication, the top 3 API endpoints, error handling, and offline behaviour
- Passes the CI test suite — sample apps are tested on every API change

Alex owns the sample app repository, triages issues filed against it, and ensures they are updated within 5 business days of any breaking API change.

## Developer NPS

Developer satisfaction is measured quarterly via a one-question NPS survey triggered by:
- After first successful API integration (in-portal modal, 30 days after onboarding)
- After an API version migration

**Target:** Developer NPS ≥ 40. Any score below 30 triggers a DX review meeting within 2 weeks.

**NPS follow-up:** All Detractor responses (score 0–6) receive a personal outreach from Alex within 5 business days offering a 30-minute call. Detractor feedback is triaged into actionable documentation or API issues.

**Developer NPS dashboard:**

| Metric | Target | Alert Threshold |
| --- | --- | --- |
| Overall NPS | ≥40 | <30 |
| Quickstart completion rate | ≥80% | <65% |
| Time to first API call (median) | ≤8 min | >15 min |
| Portal search success rate | ≥70% | <55% |
| SDK-related support tickets | Trending down | Flat or rising |

## Community Feedback Loops

Developer feedback channels and how Alex routes them:

| Channel | What It Produces | Alex's Action |
| --- | --- | --- |
| **Portal "Was this helpful?"** | Per-page satisfaction signal | Pages with <60% "Yes" scheduled for rewrite within 2 sprints |
| **GitHub Issues (sample apps)** | Bug reports + use-case requests | Triaged weekly; bugs fixed within sprint; use-case requests fed into backlog |
| **Support ticket tagging** | Common developer confusion patterns | Monthly review with VP API Platform + backend chapter leads to identify API or doc improvements |
| **Developer advisory group** | Direct feedback from top-tier integration partners | Quarterly meeting co-facilitated by Alex + CPO |

## Quality Standards

- Every API product must have a quickstart that Alex can complete in ≤10 minutes before release
- Developer NPS ≥40; any score below 30 triggers a DX review
- Sample apps updated within 5 business days of any breaking API change
- Error code catalogue covers 100% of documented error codes with resolution guidance
- All breaking API changes documented with a migration guide 30 days before the old version is deprecated
```
