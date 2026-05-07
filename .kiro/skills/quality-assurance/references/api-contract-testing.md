---
name: api_contract_testing
description: API contract testing using Pact — consumer-driven contracts, Pact Broker integration, provider verification in CI, and the workflow for catching API breaking changes before they reach production. Covers mobile client contracts (iOS/Android) as both Pact consumers, and how Rachel Kim coordinates with the Backend Chapter Lead (Dev Malhotra) on contract verification gates. Use when setting up contract tests for a new API integration, when a breaking API change is proposed, or when debugging a contract verification failure in CI.
version: "1.0.0"
---

# API Contract Testing

| Competency                     | Description                                                                                                                                                                              | Quality Criteria                                                                                                                                                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pact Contract Testing Workflow | Consumer test authoring, pact file generation, pact publication to broker, provider verification, contract change detection, can-i-deploy checks                                         | Consumer tests use `@Pact` annotation or `PactDslWithProvider` builder; pact files generated in JSON format; published to Pact Broker with version tags; provider verification runs against published pacts; `can-i-deploy` checks before release                                         |
| Provider/Consumer Setup        | Consumer-side Pact DSL configuration, provider-side verification setup, state management (`@State` handlers), request/response matching rules, metadata configuration                    | Consumer tests define expected interactions via Pact DSL; provider tests use `@Provider` annotation with pact source configured; state handlers reset provider to known state before each interaction; matching rules use `like()`, `regex()`, `eachLike()` for flexible validation       |
| Contract Versioning            | Consumer version tags, provider version tracking, branch-based pact publication, version selectors (`latest`, `main`, `prod`), pacticipant management                                    | Consumer versions tagged with git branch and release version; provider versions tracked independently; version selectors used in provider verification config; pacticipants consistently named across services                                                                            |
| CI/CD Integration              | Pact publication on consumer build, provider verification on provider build, `can-i-deploy` gate in release pipeline, webhook notifications for contract changes, pending pacts handling | CI publishes pacts on every consumer build; provider CI runs verification against latest consumer pacts; `can-i-deploy` blocks release if verification fails; webhooks notify teams of contract changes; pending pacts allow consumer-driven development before provider implementation   |
| Consumer-Driven Contract Tests | Consumer expectation definition, interaction modeling, response body matching, request header validation, query parameter matching, optional field handling, array matching              | Tests model realistic consumer interactions; response bodies use type matchers (`like`) not exact values; arrays use `eachLike` for item structure validation; optional fields handled correctly; headers and query params validated with equality or regex matchers                      |
| Pact Broker Management         | Broker deployment/configuration, pacticipant registration, webhook setup, pact versioning, tagging strategy, matrix dashboard interpretation, pact cleanup                               | Broker hosted on cloud infrastructure or PactFlow; webhooks configured for contract change notifications; matrix dashboard shows compatibility between all consumer/provider version combinations; cleanup policy removes pacts older than retention period; tags managed via CI pipeline |

## Purpose

API contract testing is the practice of verifying that service providers (backend APIs) fulfill the contracts their consumers (mobile clients, frontend) depend on — before code reaches production. Rachel Kim owns the contract testing framework and drives adoption across the company's mobile and web clients. This fills the gap that unit tests (too narrow) and end-to-end tests (too slow/fragile) cannot cover: integration at API boundaries.

## Why Contract Testing Matters Here

The company ships two mobile apps (iOS/Android) plus a web frontend, all consuming the same backend APIs. Without contract tests:

- Backend changes can break mobile clients silently — discovered in Stage 7 integration testing or in production
- Mobile engineers must manually verify every API change affects their client correctly
- API version migrations are high-risk, requiring synchronized deployments

With contract tests:

- Backend engineers get immediate CI feedback when their changes break a mobile contract
- Mobile engineers document their API expectations as executable specifications
- Breaking API changes are caught at Stage 5 (Full Production) development, not Stage 7

## Pact Framework Overview

The company uses **Pact** (consumer-driven contract testing):

1. **Consumer** (mobile/web client) defines what it sends and expects from the API
2. Pact generates a **contract file** (JSON) from the consumer test
3. **Provider** (backend) verifies its implementation satisfies all consumer contracts
4. **Pact Broker** stores contract files and verification results; manages provider/consumer version compatibility

```
iOS Client → [Pact Consumer Test] → Contract JSON
Android Client → [Pact Consumer Test] → Contract JSON
                                              ↓
                              Pact Broker (published, versioned)
                                              ↓
                         Backend API → [Pact Provider Verification] → Pass/Fail
```

## Writing Consumer Tests (Mobile)

Mobile clients (iOS/Android) define their contracts. Rachel provides the template and reviews consumer tests before they are merged:

### Android (Kotlin) Consumer Test

```kotlin
@ExtendWith(PactConsumerTestExt::class)
@PactTestFor(providerName = "UserServiceProvider")
class UserProfileContractTest {

    @Pact(consumer = "AndroidApp")
    fun getUserProfilePact(builder: PactDslWithProvider): RequestResponsePact {
        return builder
            .given("User 123 exists")
            .uponReceiving("GET /users/123")
                .method("GET")
                .path("/users/123")
                .headers(mapOf("Authorization" to Matchers.regex("Bearer .+", "Bearer valid-token")))
            .willRespondWith()
                .status(200)
                .headers(mapOf("Content-Type" to "application/json"))
                .body(PactDslJsonBody()
                    .integerType("id", 123)
                    .stringType("name", "Test User")
                    .stringType("email", "test@example.com")
                    .booleanType("isActive", true))
            .toPact()
    }

    @Test
    @PactTestFor(pactMethod = "getUserProfilePact")
    fun testGetUserProfile(mockServer: MockServer) {
        val client = UserApiClient(baseUrl = mockServer.getUrl())
        val profile = client.getUserProfile(123)
        assertEquals("Test User", profile.name)
        assertTrue(profile.isActive)
    }
}
```

### Consumer Test Quality Standards

Rachel reviews every consumer test for:

- **Matchers over literals:** Use `stringType`, `integerType`, `regex` — not hardcoded values. Contracts should be flexible enough to tolerate non-breaking provider changes.
- **State specified:** The `given()` state must match a provider state the backend team has confirmed they can set up for testing.
- **Error contract included:** Not just happy path — consumer must also define 404, 401, and relevant error responses.

## Provider Verification (Backend)

The Backend Chapter Lead (Dev Malhotra) owns provider verification. Rachel coordinates the integration:

```kotlin
@Provider("UserServiceProvider")
@PactBroker(
    host = "pact.company.internal",
    authentication = PactBrokerAuth(token = System.getenv("PACT_BROKER_TOKEN"))
)
class UserServiceProviderVerification {

    @BeforeEach
    fun setupProvider(context: PactVerificationContext) {
        context.target = HttpTestTarget("localhost", 8080)
    }

    @State("User 123 exists")
    fun setupUser123() {
        userRepository.save(User(id = 123, name = "Test User", email = "test@example.com"))
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider::class)
    fun pactVerificationTestTemplate(context: PactVerificationContext) {
        context.verifyInteraction()
    }
}
```

## CI Pipeline Integration

Rachel integrates Pact into the CI pipeline at two critical points:

```yaml
# Consumer side (mobile PR CI)
- name: Pact consumer tests
  run: ./gradlew pactTest

- name: Publish contracts to Pact Broker
  run: |
    pact-broker publish ./build/pacts \
      --broker-base-url $PACT_BROKER_URL \
      --consumer-app-version $GITHUB_SHA \
      --tag $BRANCH_NAME

# Provider side (backend PR CI)
- name: Pact provider verification
  run: ./gradlew pactVerify
  env:
    PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
    PACT_PROVIDER_VERSION: ${{ github.sha }}

- name: Publish verification results
  run: |
    pact-broker can-i-deploy \
      --pacticipant UserServiceProvider \
      --version $GITHUB_SHA \
      --to-environment production
```

**`can-i-deploy` gate:** Rachel's pipeline blocks any backend deployment if `can-i-deploy` returns failure — meaning the provider version does not satisfy all current consumer contracts.

## Stage 7 — Contract Test Integration

Rachel includes contract test results in the Stage 7 Test Results Report:

| Check                            | Criteria                                                                      | Stage 7 Gate                                    |
| -------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------- |
| All consumer contracts published | 100% of mobile/web consumers have published contracts for the release version | Block if any consumer has no contract published |
| All provider verifications pass  | 100% of provider verifications succeed against published contracts            | Block if any verification fails                 |
| `can-i-deploy` status            | All consumers can deploy to production with this provider version             | Block if `can-i-deploy` returns failure         |

## Pipeline Integration

| Stage                                | Application                                                                                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5** (Development)            | Author consumer pact tests alongside mobile client development; define expected API contracts before backend implementation; publish pending pacts              |
| **Stage 6** (Code Review)            | Review pact test coverage for all consumer-provider interactions; verify matching rule appropriateness (not too strict, not too loose)                          |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute consumer pact tests and provider verification; run `can-i-deploy` checks; validate no contract drift; classify contract defects |
| **Stage 8** (Integrity Verification) | Re-run full pact verification suite; confirm all contracts verified; ensure no breaking changes introduced during bug-fix cycle                                 |

## Coordinating API Version Migrations

When Dev Malhotra proposes a breaking API change, Rachel facilitates the contract migration:

1. Dev files a **Breaking Change Notice** in Jira 2 weeks before the change is implemented
2. Rachel notifies all consumers (Android chapter lead, iOS chapter lead, Frontend chapter lead Amira Voss)
3. Each consumer team updates their contract tests to handle both the old and new API (using Pact tags: `v1` and `v2`)
4. Provider supports both versions during transition; contracts verify both
5. When all consumers confirm `v2` is in production, `v1` contracts are deprecated and `v1` support is removed

## Quality Standards

| Metric                          | Target                                                     | Measurement                                                         |
| ------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Consumer pact coverage          | 100% of consumer-provider API interactions                 | Every API call from mobile app has a corresponding pact interaction |
| Provider verification pass rate | 100% on main branch                                        | CI gate — provider build fails if any pact verification fails       |
| `can-i-deploy` gate             | Must pass before any release                               | Release blocked if `can-i-deploy` returns "no"                      |
| Pending pact resolution time    | < 5 business days from publication to verification         | Tracked via Pact Broker dashboard; aging pending pacts = P2 defect  |
| Contract change notification    | < 5 minutes from pact publication to provider notification | Webhook latency monitoring                                          |
| Pact Broker uptime              | 99.9% availability                                         | Monitored via health checks; broker downtime = P1 incident          |
| Matching rule audit             | Reviewed quarterly for over/under-specification            | Prevents false positives from overly strict matchers                |

- All new API integrations must have Pact consumer tests before Stage 5 feature development begins
- Provider verification runs on every backend PR to main/release branches
- `can-i-deploy` gate active on all backend deployments — no manual overrides without Rachel + Dev written approval
- Breaking change notices issued at least 2 weeks before implementation
