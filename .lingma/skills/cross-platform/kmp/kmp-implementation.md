---
name: kmp-implementation
description: Implement shared business logic and data layers using Kotlin Multiplatform for projects targeting both Android and iOS.
---

# KMP Implementation

## Purpose

Implement shared business logic and data layers using Kotlin Multiplatform for projects targeting both Android and iOS. The KMP shared module contains platform-agnostic code that eliminates duplication while the Android and iOS leads own their respective platform UI layers.

## When KMP is the Right Choice

Use KMP (not Flutter) when:

- The platform has already committed to native UI on both Android (Compose) and iOS (SwiftUI)
- The shared code requirement is business logic, networking, and database — not UI
- The team has existing native iOS/Android expertise and wants to share logic, not UI
- The TSD has selected KMP per Stage 3 technology evaluation

Use Flutter (see `flutter-implementation.md`) when:

- The project wants a single UI codebase across both platforms
- Speed of cross-platform UI delivery is prioritised over pixel-perfect native feel

## Module Structure

```
root/
  shared/                     ← KMP shared module
    src/
      commonMain/kotlin/       ← All shared code
        domain/               ← Use cases, domain models, repository interfaces
        data/                 ← Repository implementations, DTOs, mappers
        network/              ← Ktor HTTP client setup
        database/             ← SQLDelight schema and queries
      androidMain/kotlin/      ← Android-specific actual declarations
      iosMain/kotlin/          ← iOS-specific actual declarations
    build.gradle.kts

  androidApp/                  ← Android application module (Compose UI)
  iosApp/                      ← iOS application (Xcode project, SwiftUI)
```

**Boundary rule:** `commonMain` must have zero Android SDK or iOS SDK imports. All platform-specific implementations live in `androidMain` or `iosMain`.

## expect/actual Pattern

```kotlin
// commonMain — declare the interface
expect class PlatformClock {
    fun nowMillis(): Long
}

// androidMain — Android implementation
actual class PlatformClock {
    actual fun nowMillis() = System.currentTimeMillis()
}

// iosMain — iOS implementation
actual class PlatformClock {
    actual fun nowMillis() = NSDate().timeIntervalSince1970.toLong() * 1000
}
```

Use `expect`/`actual` sparingly — only for genuinely platform-divergent behaviour (date/time, file system, crypto, secure storage access, platform-specific SDK calls). Business logic should be in `commonMain` using cross-platform libraries.

## Networking (Ktor)

```kotlin
// commonMain
val client = HttpClient {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true })
    }
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
    }
}

suspend fun fetchItems(): List<ItemDto> =
    client.get("https://api.example.com/items").body()
```

## Database (SQLDelight)

```sql
-- shared/src/commonMain/sqldelight/com/example/Item.sq
CREATE TABLE Item (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    createdAt INTEGER NOT NULL
);

selectAll:
SELECT * FROM Item;

insert:
INSERT INTO Item (id, name, createdAt) VALUES (?, ?, ?);
```

```kotlin
// commonMain — using generated queries
class ItemLocalDataSource(private val database: AppDatabase) {
    fun getAll(): List<Item> = database.itemQueries.selectAll().executeAsList()
    fun insert(item: Item) = database.itemQueries.insert(item.id, item.name, item.createdAt)
}
```

## Swift Interoperability

KMP generates an Objective-C/Swift framework for iOS consumption. Key rules:

- Use `@ObjCName` to control the Swift name of Kotlin declarations
- Kotlin `suspend` functions become `(result, error)` callback-style in Swift — use the `skie` or `KMP-NativeCoroutines` library to expose them as `async` Swift functions
- Kotlin `Flow` becomes `AsyncStream<T>` with KMP-NativeCoroutines or SKIE
- Kotlin sealed classes become Swift enums with associated values

```kotlin
// Add to shared module — enables clean Swift async/await consumption
@ObjCName("ItemRepository")
interface ItemRepository {
    suspend fun fetchItems(): List<Item>
}
```

## Coroutines on iOS

- Main dispatcher: use `Dispatchers.Main` (requires `kotlinx-coroutines-core` with native support)
- Never use `runBlocking` from iOS main thread — it deadlocks
- Use `MainScope()` or inject a coroutine scope via constructor for iOS entry points

## Gradle Build Configuration

```kotlin
// shared/build.gradle.kts
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.sqldelight.runtime)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
            implementation(libs.sqldelight.android.driver)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
            implementation(libs.sqldelight.native.driver)
        }
    }
}
```

## Code Review Standards

Before Stage 6:

- [ ] `commonMain` has zero Android SDK or iOS SDK imports
- [ ] All `expect`/`actual` declarations have implementations for all targets
- [ ] Shared module builds for all targets: `./gradlew :shared:build`
- [ ] iOS framework generates without linker errors: `./gradlew :shared:linkDebugFrameworkIosSimulatorArm64`
- [ ] All strings that pass through the shared module are resource keys, not hardcoded literals
- [ ] Coroutine scopes are properly cancelled on iOS — no memory leaks
