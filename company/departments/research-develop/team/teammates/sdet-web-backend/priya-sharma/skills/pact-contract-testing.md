---
version: "1.0.0"
---

# Pact Contract Testing

| Competency                         | Description                                                                                                                                                                              | Quality Criteria                                                                                                                                                                                                                                                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pact Contract Testing Workflow** | Consumer test authoring, pact file generation, pact publication to broker, provider verification, contract change detection, can-i-deploy checks                                         | Consumer tests use `@Pact` annotation or `PactDslWithProvider` builder; pact files generated in JSON format; published to Pact Broker with version tags; provider verification runs against published pacts; `can-i-deploy` checks before release                                            |
| **Provider/Consumer Setup**        | Consumer-side Pact DSL configuration, provider-side verification setup, state management (`@State` handlers), request/response matching rules, metadata configuration                    | Consumer tests define expected interactions via Pact DSL; provider tests use `@Provider` annotation with pact source configured; state handlers reset provider to known state before each interaction; matching rules use `like()`, `regex()`, `eachLike()` for flexible validation          |
| **Contract Versioning**            | Consumer version tags, provider version tracking, branch-based pact publication, version selectors (`latest`, `main`, `prod`), pacticipant management                                    | Consumer versions tagged with git branch (`main`, `develop`, `feature/xyz`) and release version (`1.2.3`); provider versions tracked independently; version selectors used in provider verification config; pacticipants (consumer/provider names) consistently named across services        |
| **CI/CD Integration**              | Pact publication on consumer build, provider verification on provider build, `can-i-deploy` gate in release pipeline, webhook notifications for contract changes, pending pacts handling | CI publishes pacts on every consumer build; provider CI runs verification against latest consumer pacts; `can-i-deploy` blocks release if pact verification fails; webhooks notify teams of contract changes; pending pacts allow consumer-driven development before provider implementation |
| **Consumer-Driven Contract Tests** | Consumer expectation definition, interaction modeling, response body matching, request header validation, query parameter matching, optional field handling, array matching              | Tests model realistic consumer interactions; response bodies use type matchers (`like`) not exact values; arrays use `eachLike` for item structure validation; optional fields marked with `eachLike` with `min` count; headers and query params validated with equality or regex matchers   |
| **Pact Broker Management**         | Broker deployment/configuration, pacticipant registration, webhook setup, pact versioning, tagging strategy, matrix dashboard interpretation, pact cleanup                               | Broker hosted on cloud infrastructure or PactFlow; webhooks configured for contract change notifications; matrix dashboard shows compatibility between all consumer/provider version combinations; cleanup policy removes pacts older than retention period; tags managed via CI pipeline    |

## Pipeline Integration

| Stage                                | Application                                                                                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5** (Development)            | Author consumer pact tests alongside mobile client development; define expected API contracts before backend implementation; publish pending pacts              |
| **Stage 6** (Code Review)            | Review pact test coverage for all consumer-provider interactions; verify matching rule appropriateness (not too strict, not too loose)                          |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute consumer pact tests and provider verification; run `can-i-deploy` checks; validate no contract drift; classify contract defects |
| **Stage 8** (Integrity Verification) | Re-run full pact verification suite; confirm all contracts verified; ensure no breaking changes introduced during bug-fix cycle                                 |

## Quality Standards

| Metric                          | Target                                                     | Measurement                                                         |
| ------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Consumer pact coverage          | 100% of consumer-provider API interactions                 | Every API call from mobile app has a corresponding pact interaction |
| Provider verification pass rate | 100% on main branch                                        | CI gate — provider build fails if any pact verification fails       |
| can-i-deploy gate               | Must pass before any release                               | Release blocked if `can-i-deploy` returns "no"                      |
| Pending pact resolution time    | < 5 business days from publication to verification         | Tracked via Pact Broker dashboard; aging pending pacts = P2 defect  |
| Contract change notification    | < 5 minutes from pact publication to provider notification | Webhook latency monitoring                                          |
| Pact Broker uptime              | 99.9% availability                                         | Monitored via health checks; broker downtime = P1 incident          |
| Matching rule audit             | Reviewed quarterly for over/under-specification            | Prevents false positives from overly strict matchers                |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
