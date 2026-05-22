---
name: kmp-testing-strategy
description: KMP multiplatform test strategy and infrastructure. Use when designing the test strategy for a KMP shared module, writing kotlin.test-based unit or integration tests, building a fake network layer or in-memory database driver for shared tests, configuring the CI pipeline to run multiplatform tests on all targets, or diagnosing test failures that only manifest on a specific platform target.
version: "1.0.0"
---

# KMP Testing Strategy

## Purpose

Shared KMP code runs on multiple platforms, and a test that passes on the JVM (Android unit tests) can fail on Kotlin/Native (iOS). The only way to guarantee shared code behaves correctly on all targets is to test it on all targets. This skill gives the team the infrastructure and patterns to achieve that without duplicating test code.

---

## Testing Pyramid for KMP

```
               ┌───────────────────────┐
               │   Platform E2E Tests  │  (Android Espresso, iOS XCUITest)
               │    (platform-specific) │
              ┌┴───────────────────────┴┐
              │  Platform Integration   │  (XCTest for KMP Swift API surface)
              │   (iosTest, androidTest) │
             ┌┴─────────────────────────┴┐
             │  Shared Integration Tests  │  (commonTest — fake network + in-memory DB)
            ┌┴───────────────────────────┴┐
            │     Shared Unit Tests        │  (commonTest — pure Kotlin logic)
            └─────────────────────────────┘
```

Write most tests in `commonTest` — they run on all configured targets. Reserve `iosTest` and `androidTest` for platform-specific concerns.

---

## `commonTest` Setup

### Dependencies

```kotlin
// build.gradle.kts (shared module)
kotlin {
    sourceSets {
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.x.x")
            }
        }
    }
}
```

### Writing Tests

```kotlin
// commonTest
class UserRepositoryTest {
    private val fakeNetwork = FakeUserNetworkSource()
    private val inMemoryDb = createInMemoryDatabase()  // expect/actual
    private val repo = UserRepositoryImpl(
        localSource = UserLocalDataSource(inMemoryDb.userQueries),
        remoteSource = fakeNetwork
    )

    @Test
    fun `sync populates local database from remote`() = runTest {
        fakeNetwork.queueResponse(listOf(UserFixture.alice, UserFixture.bob))

        repo.syncUsers()

        val users = repo.observeUsers().first()
        assertEquals(2, users.size)
    }
}
```

`runTest` from `kotlinx-coroutines-test` handles coroutine test execution on all platforms.

---

## Fake Network Layer

Build a `FakeRemoteDataSource` that implements the same interface as the real network source:

```kotlin
// commonTest (or testFixtures)
class FakeUserNetworkSource : UserRemoteDataSource {
    private val queue = ArrayDeque<Result<List<User>>>()

    fun queueResponse(users: List<User>) {
        queue.addLast(Result.success(users))
    }

    fun queueError(error: Throwable) {
        queue.addLast(Result.failure(error))
    }

    override suspend fun fetchUsers(): List<User> =
        queue.removeFirstOrNull()?.getOrThrow()
            ?: error("No response queued")
}
```

This approach gives tests deterministic control over network responses without HTTP mocking libraries that don't work on Kotlin/Native.

---

## In-Memory SQLDelight Driver

```kotlin
// expect in commonTest
expect fun createInMemoryDriver(schema: SqlDriver.Schema): SqlDriver

// actual in androidTest
actual fun createInMemoryDriver(schema: SqlDriver.Schema): SqlDriver =
    JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY).also { schema.create(it) }

// actual in iosTest
actual fun createInMemoryDriver(schema: SqlDriver.Schema): SqlDriver =
    NativeSqliteDriver(schema, ":memory:")
```

Use the in-memory driver for all shared database tests. Never write tests that depend on a real file-backed database.

---

## CI Configuration

Run multiplatform tests on all configured targets in CI:

```yaml
# GitHub Actions (example)
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: "17", distribution: "temurin" }
      - name: Run tests
        run: |
          if [ "$RUNNER_OS" == "Linux" ]; then
            ./gradlew :shared:jvmTest :shared:linuxX64Test
          else
            ./gradlew :shared:iosSimulatorArm64Test :shared:macosArm64Test
          fi
```

**Key requirement:** iOS tests (`iosSimulatorArm64Test`, `iosX64Test`) must run on macOS runners — they require the Kotlin/Native compiler and an Apple SDK. Never skip iOS tests in CI to save time; a failing iOS test discovered post-merge is a merge-gating failure that should have been caught earlier.

---

## Platform-Specific Test Source Sets

Use `iosTest` and `androidTest` source sets for platform-specific behaviour that cannot be tested in `commonTest`:

| Test Type                  | Source Set           | When to Use                                                        |
| -------------------------- | -------------------- | ------------------------------------------------------------------ |
| Kotlin/Native memory model | `iosTest`            | Testing that objects are correctly managed by the Kotlin/Native GC |
| Swift API surface          | XCTest (iOS project) | Testing that the generated Swift API works as expected             |
| Android WorkManager        | `androidTest`        | Testing background sync scheduling                                 |
| Android-specific lifecycle | `androidTest`        | Testing `AndroidViewModel` lifecycle integration                   |

---

## Output Standards

- Shared modules must have `commonTest` coverage for all public repository and use case methods before shipping.
- CI must run `iosSimulatorArm64Test` (or equivalent) on every PR — a PR that only passes JVM tests is not validated.
- Fake implementations must be kept in sync with the interfaces they implement — a fake that doesn't implement a new method is a CI failure, not a silent gap.
