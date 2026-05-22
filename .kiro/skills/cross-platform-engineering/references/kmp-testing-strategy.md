---
name: kmp-testing-strategy
description: Design and implement comprehensive KMP multiplatform testing — kotlin.test in commonTest, platform-specific tests in androidTest/iosTest, fake network layers, in-memory SQLDelight drivers, and CI configuration for multiplatform test suites.
version: "1.0.0"
---

# KMP Testing Strategy

| Competency          | Description                                                            | Quality Criteria                                                                            |
| ------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| commonTest Coverage | Write shared unit tests for all domain and data layer logic            | ≥ 80% line coverage in `commonMain`; all use cases have happy path + error path tests       |
| Platform Tests      | Write platform-specific tests for `expect`/`actual` implementations    | `androidTest` and `iosTest` cover platform adapter behaviour; no skipped tests              |
| Fake Network Layer  | Implement a deterministic fake HTTP client for shared networking tests | Fake returns fixture data from in-memory map; no real network calls in test suite           |
| In-Memory DB Driver | Use in-memory SQLDelight driver for database tests                     | All repository tests run against in-memory driver; test setup/teardown resets state cleanly |

## Execution Guidance

### Test Module Structure

```
shared/
├── commonTest/
│   ├── data/
│   │   ├── repository/  # Repository unit tests using fakes
│   │   └── sync/        # Sync protocol unit tests
│   └── domain/
│       └── usecase/     # Use case tests
├── androidTest/
│   └── data/db/        # Android driver integration tests
└── iosTest/
    └── data/db/        # iOS driver integration tests
```

### Fake Network Layer Pattern

```kotlin
// commonTest — fake HttpClient
class FakeHttpClient(
    private val responses: Map<String, Any> = emptyMap()
) {
    suspend fun get(url: String): Response =
        responses[url]?.let { Response.Success(it) }
            ?: Response.Error(404, "Not found in fake")
}

// Use in repository tests
class UserRepositoryTest {
    private val fakeClient = FakeHttpClient(
        responses = mapOf(
            "/users/1" to UserDto(id = "1", name = "Test User")
        )
    )
    private val repository = UserRepository(fakeClient)

    @Test
    fun `getUser returns user when found`() = runTest {
        val result = repository.getUser("1")
        assertEquals("Test User", result.name)
    }
}
```

### CI Configuration for KMP Tests

```yaml
# GitHub Actions
- name: Run KMP tests
  run: |
    ./gradlew :shared:allTests
    # Equivalent to: commonTest + androidUnitTest + iosSimulatorArm64Test

- name: Run iOS tests on simulator
  run: |
    ./gradlew :shared:iosSimulatorArm64Test
```
