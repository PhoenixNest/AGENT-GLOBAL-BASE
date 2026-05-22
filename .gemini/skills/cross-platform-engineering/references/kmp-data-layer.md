---
name: kmp-data-layer
description: Architect and implement the KMP shared data layer — SQLDelight for local persistence, Ktor for networking, repository pattern for single source of truth, and offline-first synchronisation strategies across Android and iOS.
version: "1.0.0"
---

# KMP Data Layer

| Competency         | Description                                                            | Quality Criteria                                                                                  |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| SQLDelight Schema  | Design and migrate the shared database schema across all targets       | Migrations are versioned and additive-only; schema generates type-safe Kotlin queries             |
| Ktor Networking    | Implement platform-appropriate HTTP client with shared request logic   | `OkHttp` engine on Android, `Darwin` engine on iOS; retry and timeout policy in shared code       |
| Repository Pattern | Implement repository interfaces in `commonMain` with platform adapters | Single source of truth enforced; no direct DB or network access outside repositories              |
| Offline-First Sync | Implement offline-first data synchronisation with conflict resolution  | Conflict resolution strategy documented; sync protocol handles concurrent edits deterministically |

## Execution Guidance

### Data Layer Module Structure

```
shared/
├── commonMain/
│   ├── data/
│   │   ├── db/          # SQLDelight schema + generated queries
│   │   ├── network/     # Ktor client + API models
│   │   ├── repository/  # Repository interfaces + implementations
│   │   └── sync/        # Offline-first sync protocol
│   └── domain/
│       ├── model/       # Domain models (pure Kotlin data classes)
│       └── repository/  # Repository interfaces (domain layer)
├── androidMain/
│   └── data/db/        # Android-specific SQLDelight driver
└── iosMain/
    └── data/db/        # iOS-specific SQLDelight driver
```

### SQLDelight Driver Setup

```kotlin
// androidMain
actual fun createDriver(schema: SqlSchema, name: String): SqlDriver =
    AndroidSqliteDriver(schema, context, name)

// iosMain
actual fun createDriver(schema: SqlSchema, name: String): SqlDriver =
    NativeSqliteDriver(schema, name)
```

### Offline-First Sync Protocol

```
1. Local Write → immediately persist to SQLDelight
2. Queue for Sync → add to sync queue with vector clock timestamp
3. Background Sync → when connectivity available:
   a. Fetch server state
   b. Apply conflict resolution (Last-Write-Wins or domain-specific)
   c. Update local DB with resolved state
   d. Emit update via StateFlow to UI layer
4. Retry Policy → exponential backoff; max 5 retries before user notification
```
