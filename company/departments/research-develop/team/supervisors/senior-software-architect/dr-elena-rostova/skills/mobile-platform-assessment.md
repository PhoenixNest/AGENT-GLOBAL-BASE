---
name: mobile-platform-assessment
description: Evaluate the current mobile platform stack against industry benchmarks and the organisation's strategic roadmap — producing a Platform Assessment Report that identifies capability gaps, technology risk, and a prioritised remediation roadmap for CTO review.
version: "1.0.0"
---

# Mobile Platform Assessment

| Competency                 | Description                                                                 | Quality Criteria                                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------- | ---------------- | ---------------- |
| Stack Benchmarking         | Compare current platform against industry peers and best-practice baselines | Uses quantitative criteria (build time, test coverage, crash rate, ANR rate); compares against published Google/Apple benchmarks |
| Technology Risk Assessment | Identify end-of-life SDKs, deprecated APIs, and support cliff risks         | Produces risk table: Component                                                                                                   | Version | EOL Date         | Risk Level       | Migration Effort |
| Capability Gap Analysis    | Map platform capabilities to product roadmap requirements                   | Identifies features blocked by current stack limitations; ranks by roadmap impact                                                |
| Remediation Roadmap        | Prioritised action plan with effort and impact estimates                    | Roadmap items: Priority                                                                                                          | Action  | Estimated Effort | Expected Outcome | Target Quarter   |

## Execution Guidance

### Assessment Dimensions

| Dimension              | Key Metrics                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| Build performance      | Clean build time, incremental build time, CI build time (p95)        |
| Test coverage          | Unit test coverage %, integration test pass rate, E2E test stability |
| Crash & ANR rates      | Industry benchmark: <0.1% crash rate, <0.47% ANR rate (Google Play)  |
| API target compliance  | Min SDK, target SDK, deprecated API usage count                      |
| Third-party SDK health | Version currency, known CVEs, active maintenance status              |
| Developer experience   | Time to onboard new engineer, PR cycle time, build cache hit rate    |

### Technology Risk Rating

| Risk Level | Definition                                                        |
| ---------- | ----------------------------------------------------------------- |
| Critical   | EOL within 6 months or active CVE with no patch available         |
| High       | EOL within 12 months or deprecated API removed in next OS release |
| Medium     | Deprecated but still functional; migration effort >2 sprints      |
| Low        | Modern and supported; monitoring only                             |

The Platform Assessment Report is delivered quarterly to the CTO and informs Stage 4 Implementation Plan resource allocation.
