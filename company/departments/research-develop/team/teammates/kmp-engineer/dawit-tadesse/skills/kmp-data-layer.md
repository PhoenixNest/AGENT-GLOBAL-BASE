---
name: kmp-data-layer
description: KMP shared data layer architecture and implementation. Use when designing or implementing the SQLDelight database schema for a KMP project, building the Ktor-based shared networking layer, implementing the repository pattern in shared Kotlin, designing offline-first data synchronisation across platforms, or advising on cross-platform data persistence and caching strategy.
version: "1.0.0"
---

# KMP Data Layer

## Purpose

The shared data layer is the highest-leverage component of a KMP project — it is where platform-divergence bugs most commonly arise, and where eliminating duplication saves the most maintenance cost. A well-designed shared data layer provides a single source of truth for the application's data model, eliminates platform-specific database and networking code, and allows offline-first behaviour to be implemented once and tested once.

---

## Data Layer Architecture

### Layer Diagram

```
┌─────────────────────────────────────┐
│          UI / ViewModel              │  (Android: Compose; iOS: SwiftUI)
├─────────────────────────────────────┤
│         Shared ViewModel             │  (commonMain — optional)
├─────────────────────────────────────┤
│           Use Cases                  │  (commonMain)
├─────────────────────────────────────┤
│          Repository                  │  (commonMain — interface + impl)
├────────────────┬────────────────────┤
│  Local Source  │   Remote Source    │  (commonMain — interfaces)
│  (SQLDelight)  │      (Ktor)        │
└────────────────┴────────────────────┘
```

**Design rule:** Every component above the Repository layer is platform-independent. The Repository interface is defined in `commonMain`; its implementation is also in `commonMain` if only SQLDelight and Ktor are needed. Platform-specific sources (e.g., Android Room, iOS CoreData) belong in `expect`/`actual` implementations, but should be avoided when SQLDelight covers the requirement.

---

## SQLDelight

### Schema Definition

SQLDelight generates type-safe Kotlin from `.sq` files. Organise schema by feature domain:

```sql
-- User.sq
CREATE TABLE User (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    createdAt INTEGER NOT NULL  -- store as Unix epoch (Long)
);

selectAll:
SELECT * FROM User;

selectById:
SELECT * FROM User WHERE id = ?;

insert:
INSERT INTO User(id, name, email, createdAt) VALUES (?, ?, ?, ?);

deleteById:
DELETE FROM User WHERE id = ?;
```

### Driver Selection

| Platform     | Driver                                                             |
| ------------ | ------------------------------------------------------------------ |
| Android      | `AndroidSqliteDriver` (from `sqldelight-android-driver`)           |
| iOS          | `NativeSqliteDriver` (from `sqldelight-native-driver`)             |
| JVM tests    | `JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)`                     |
| Common tests | Use `expect`/`actual` to provide the in-memory driver per platform |

Provide the driver via dependency injection (Koin or constructor injection) — never hard-code it in the shared module.

### Migration Strategy

SQLDelight migrations use versioned `.sqm` files. Apply these rules:

- Never modify a previously shipped migration file
- Test migrations on both Android (SQLiteOpenHelper) and iOS (NativeSqliteDriver) before releasing
- Add a migration test that runs the full migration sequence on the in-memory driver

---

## Ktor Shared Networking

### Client Configuration

```kotlin
// commonMain
val httpClient = HttpClient {
    install(ContentNegotiation) { json() }
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 10_000
    }
    install(Logging) { level = LogLevel.INFO }
    defaultRequest {
        header(HttpHeaders.ContentType, ContentType.Application.Json)
    }
}
```

### Engine Selection

```kotlin
// androidMain
actual fun createHttpClient(): HttpClient = HttpClient(OkHttp) { /* config */ }

// iosMain
actual fun createHttpClient(): HttpClient = HttpClient(Darwin) { /* config */ }
```

`OkHttp` is the Android engine; `Darwin` is the iOS engine. Both implement the Ktor `HttpClientEngine` interface, so the shared networking code is platform-agnostic.

---

## Repository Pattern

### Interface (commonMain)

```kotlin
interface UserRepository {
    fun observeUsers(): Flow<List<User>>
    suspend fun syncUsers(): Result<Unit>
    suspend fun getUserById(id: String): User?
}
```

### Implementation (commonMain)

```kotlin
class UserRepositoryImpl(
    private val localSource: UserLocalDataSource,
    private val remoteSource: UserRemoteDataSource,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.Default
) : UserRepository {

    override fun observeUsers(): Flow<List<User>> =
        localSource.observeAll()  // SQLDelight Flow

    override suspend fun syncUsers(): Result<Unit> = withContext(ioDispatcher) {
        runCatching {
            val remoteUsers = remoteSource.fetchUsers()
            localSource.replaceAll(remoteUsers)
        }
    }
}
```

**Key conventions:**

- Return `Flow<T>` for observable data (backed by SQLDelight `asFlow()`)
- Return `suspend fun ... : Result<T>` for write operations — never throw from the repository
- Inject the `CoroutineDispatcher` to enable testing with `TestCoroutineDispatcher`

---

## Offline-First Synchronisation

For features requiring offline-first behaviour:

1. **Write to local first** — User actions write to SQLDelight immediately; UI updates from the local `Flow` reactively. No network round-trip blocks the user.

2. **Sync in background** — A background sync job (WorkManager on Android, BGAppRefreshTask on iOS, scheduled via `expect`/`actual`) pushes local changes to the server and pulls remote changes.

3. **Conflict resolution** — Define a conflict resolution strategy per data type. For most cases, "last write wins" (by server timestamp) is sufficient. For complex scenarios, implement vector clock comparison in shared Kotlin.

4. **Sync state** — Maintain a sync metadata table in SQLDelight: last sync time, pending operation count, last error. Expose this as a `Flow<SyncState>` so the UI can show sync indicators.

---

## Output Standards

- Every SQLDelight query must be covered by an in-memory driver test before shipping.
- Repositories must never expose `Exception` — use `Result<T>` or sealed classes for error handling.
- Network responses must be mapped to domain models at the data source boundary — the repository and use case layers never see raw API response types.
