# KMP Shared Modules

**Category:** Mobile Engineering — Cross-Platform (KMP)
**Owner:** Cross-Platform Engineer (Dmitri Volkov)

## Overview

This skill implements Kotlin Multiplatform shared module architecture covering expect/actual patterns, Kotlin/Native compilation, platform interop, and shared business logic design. It applies to Stage 5 (Development) where KMP shared modules are the foundation for cross-platform code reuse, Stage 6 (Code Review) where expect/actual completeness and platform interop correctness are audited, and Stage 8 (Integrity Verification) where shared module behavior is verified on both platforms.

## Competency Dimensions

| Dimension                    | Description                                                                                           | Proficiency Indicators                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Shared Module Architecture   | Module structure, source set organization, dependency management, Gradle multiplatform plugin         | Clean source set hierarchy (commonMain, androidMain, iosMain); shared module compiles for all targets; dependencies correctly scoped       |
| Expect/Actual Pattern        | Declaration in common, platform-specific implementations, compile-time resolution, testing strategy   | Every `expect` has matching `actual` for all targets; actual implementations handle platform edge cases; expect/actual tested per platform |
| Kotlin/Native Compilation    | Binary framework generation, cinterop, memory management, threading model, distribution               | Framework compiles for iosArm64 and iosSimulatorArm64; cinterop bindings correct; memory management follows Kotlin/Native rules            |
| Platform Interop             | Swift/Kotlin bridging, sealed class mapping, coroutine interop, error translation, data class mapping | Kotlin sealed classes map to Swift enums correctly; coroutines map to Swift async/await; errors translated to Swift Error protocol         |
| Shared Business Logic Design | Domain layer sharing, use case abstraction, serialization, validation, state management               | >70% business logic shared between platforms; domain entities are pure Kotlin; platform-specific concerns (UI, storage) abstracted         |

## Execution Guidance

### Shared Module Structure

```
shared/
├── build.gradle.kts
├── src/
│   ├── commonMain/kotlin/
│   │   ├── domain/
│   │   │   ├── model/          # Pure Kotlin domain entities
│   │   │   ├── repository/     # Repository interfaces (contracts)
│   │   │   └── usecase/        # Use case interactors
│   │   ├── data/
│   │   │   ├── remote/         # API client abstractions
│   │   │   ├── local/          # Storage abstractions
│   │   │   └── mapper/         # DTO ↔ Domain mappers
│   │   └── di/                 # Dependency injection (Koin)
│   ├── androidMain/kotlin/
│   │   ├── data/
│   │   │   ├── remote/         # Retrofit implementations
│   │   │   └── local/          # Room/SharedPreferences implementations
│   │   └── di/                 # Android-specific DI modules
│   └── iosMain/kotlin/
│       ├── data/
│       │   ├── remote/         # Ktor client implementations
│       │   └── local/          # Keychain/UserDefaults implementations
│       └── di/                 # iOS-specific DI modules
```

**build.gradle.kts:**

```kotlin
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
    id("com.android.library")
    id("org.jetbrains.compose")
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions.jvmTarget = "17"
        }
    }

    listOf(
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "Shared"
            isStatic = true  // Static framework for iOS

            // Export dependencies to iOS
            export(libs.koin.core)
            export(libs.ktor.client.core)
        }
    }

    sourceSets {
        val commonMain by getting {
            dependencies {
                api(libs.kotlinx.coroutines.core)
                api(libs.koin.core)
                api(libs.kotlinx.serialization.json)
                api(libs.ktor.client.core)
                api(libs.ktor.client.contentNegotiation)
                api(libs.ktor.serialization.kotlinx.json)
            }
        }

        val androidMain by getting {
            dependencies {
                api(libs.ktor.client.okhttp)
                api(libs.koin.android)
            }
        }

        val iosArm64Main by getting
        val iosSimulatorArm64Main by getting
        val iosMain by creating {
            dependsOn(commonMain)
            iosArm64Main.dependsOn(this)
            iosSimulatorArm64Main.dependsOn(this)

            dependencies {
                api(libs.ktor.client.darwin)
            }
        }
    }
}
```

### Expect/Actual — Production Patterns

```kotlin
// MARK: - commonMain

// Storage abstraction — platform-specific implementation
expect class SecureStorage() {
    suspend fun put(key: String, value: String)
    suspend fun get(key: String): String?
    suspend fun delete(key: String)
    suspend fun clear()
}

// Network client abstraction
expect fun createHttpClient(): HttpClient

// Platform info
expect object PlatformInfo {
    val name: String
    val version: String
    val osVersion: String
}

// MARK: - androidMain

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

actual class SecureStorage actual constructor() {
    private lateinit var preferences: EncryptedSharedPreferences

    actual suspend fun put(key: String, value: String) {
        ensureInitialized()
        preferences.edit().putString(key, value).apply()
    }

    actual suspend fun get(key: String): String? {
        ensureInitialized()
        return preferences.getString(key, null)
    }

    actual suspend fun delete(key: String) {
        ensureInitialized()
        preferences.edit().remove(key).apply()
    }

    actual suspend fun clear() {
        ensureInitialized()
        preferences.edit().clear().apply()
    }

    private fun ensureInitialized() {
        if (::preferences.isInitialized) return
        val context = getAppContext()  // Provided via DI
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
        preferences = EncryptedSharedPreferences.create(
            context,
            "secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        ) as EncryptedSharedPreferences
    }
}

actual fun createHttpClient(): HttpClient {
    return HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 15_000
        }
    }
}

actual object PlatformInfo {
    actual val name: String = "Android"
    actual val version: String = BuildConfig.VERSION_NAME
    actual val osVersion: String = Build.VERSION.RELEASE
}

// MARK: - iosMain

import platform.Foundation.NSUserDefaults
import platform.Foundation.NSKeyedArchiver

actual class SecureStorage actual constructor() {
    private val userDefaults = NSUserDefaults.standardUserDefaults

    actual suspend fun put(key: String, value: String) {
        userDefaults.setObject(value, key)
        userDefaults.synchronize()
    }

    actual suspend fun get(key: String): String? {
        return userDefaults.stringForKey(key)
    }

    actual suspend fun delete(key: String) {
        userDefaults.removeObjectForKey(key)
        userDefaults.synchronize()
    }

    actual suspend fun clear() {
        val dictionary = userDefaults.dictionaryRepresentation()
        dictionary.keys.forEach { key ->
            userDefaults.removeObjectForKey(key as String)
        }
        userDefaults.synchronize()
    }
}

actual fun createHttpClient(): HttpClient {
    return HttpClient(Darwin) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 15_000
        }
        engine {
            configureRequest {
                setAllowsCellularAccess(true)
            }
        }
    }
}

actual object PlatformInfo {
    actual val name: String = "iOS"
    actual val version: String = NSBundle.mainBundle.infoDictionary?.getValue("CFBundleShortVersionString") as? String ?: "unknown"
    actual val osVersion: String = UIDevice.currentDevice.systemVersion
}
```

### Kotlin/Native — Swift Interop

**Sealed class to Swift enum mapping:**

```kotlin
// Kotlin — sealed interface
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Error(val message: String, val code: Int) : Result<Nothing>
}

// Swift — generated as protocol + classes
// protocol Result
// class ResultSuccess<T> : Result
// class ResultError : Result

// Better: use @ObjCName for cleaner Swift names
@OptIn(ExperimentalObjCName::class)
@ObjCName("Result", exact = true)
sealed interface Result<out T> {
    @ObjCName("Success", exact = true)
    data class Success<T>(val data: T) : Result<T>

    @ObjCName("Failure", exact = true)
    data class Failure(val message: String, val code: Int) : Result<Nothing>
}
```

**Coroutine to Swift async/await mapping:**

```kotlin
// Kotlin — suspend function
class UserFetcher(private val api: UserApi) {
    suspend fun fetchUser(id: String): User {
        return api.getUser(id)
    }
}

// Swift — generated as async function
// let fetcher = UserFetcher(api: api)
// let user = try await fetcher.fetchUser(id: "123")

// Kotlin — Flow
class UserObserver(private val api: UserApi) {
    fun observeUser(id: String): Flow<User> {
        return flow {
            while (isActive) {
                val user = api.getUser(id)
                emit(user)
                delay(30_000)
            }
        }
    }
}

// Swift — generated as AsyncSequence
// for try await user in fetcher.observeUser(id: "123") {
//     print(user.name)
// }
```

**cinterop for native APIs:**

```kotlin
// Build.gradle.kts — cinterop configuration
kotlin {
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        val iosMain by getting {
            dependencies {
                // cinterop bindings for native libraries
                // Defined in .def files
            }
        }
    }
}

// crypto.def — cinterop definition file
language = Objective-C
modules = CryptoKit
headers = CryptoKit/CryptoKit.h
compilerOpts = -framework CryptoKit
linkerOpts = -framework CryptoKit
```

### Shared Business Logic — Domain Layer

```kotlin
// MARK: - Pure Kotlin Domain (commonMain)

// Domain entity — no platform dependencies
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: Instant,
    val preferences: UserPreferences
)

data class UserPreferences(
    val theme: Theme,
    val notificationsEnabled: Boolean,
    val language: String
)

enum class Theme { LIGHT, DARK, SYSTEM }

// Repository interface — defined in domain
interface UserRepository {
    fun observeUser(id: String): Flow<User>
    suspend fun fetchUser(id: String): Result<User, ApiError>
    suspend fun updateUser(user: User): Result<Unit, ApiError>
}

// Use case — pure business logic
class GetUserProfileUseCase(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(userId: String): Result<User, DomainError> {
        if (userId.isBlank()) {
            return Result.Error(DomainError.InvalidArgument("User ID cannot be empty"))
        }

        return userRepository.fetchUser(userId).mapLeft { apiError ->
            when (apiError) {
                is ApiError.NotFound -> DomainError.UserNotFound(userId)
                is ApiError.Unauthorized -> DomainError.AuthenticationRequired
                is ApiError.NetworkError -> DomainError.NetworkUnavailable
                else -> DomainError.Unknown(apiError.message)
            }
        }
    }
}

// Result type — Arrow-style
sealed class Result<out T, out E> {
    data class Success<T>(val value: T) : Result<T, Nothing>()
    data class Error<E>(val error: E) : Result<Nothing, E>()

    fun <R> map(transform: (T) -> R): Result<R, E> = when (this) {
        is Success -> Success(transform(value))
        is Error -> Error(error)
    }

    fun <F> mapLeft(transform: (E) -> F): Result<T, F> = when (this) {
        is Success -> Success(value)
        is Error -> Error(transform(error))
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes KMP for shared business logic. Scope defined: domain layer + data abstractions shared; UI platform-specific.
- **Stage 5 (Development):** Primary skill for KMP shared module implementation. Expect/actual declarations, shared domain logic, platform interop.
- **Stage 6 (Code Review):** KMP review: expect/actual completeness for all targets, coroutine interop correctness, sealed class Swift mapping, memory management.
- **Stage 7 (Automated Testing):** Shared module tests run on JVM; platform-specific tests run on Android emulator and iOS simulator.
- **Stage 8 (Integrity Verification):** Shared module behavior verified on both platforms — same inputs produce same outputs.

## Quality Standards

- **>70%** code sharing ratio for business logic (domain + data abstractions)
- **100%** `expect` declarations have matching `actual` for all targets (Android + iOS)
- Shared module compiles for **iosArm64 and iosSimulatorArm64** — no simulator-only builds
- Domain entities are **pure Kotlin** — zero platform imports in commonMain
- Kotlin sealed interfaces map to **clean Swift protocols** — @ObjCName used for clarity
- Suspend functions map to **Swift async/await** — no completion handler bridging
- Flow maps to **Swift AsyncSequence** — observable streams work natively on iOS
- Shared module tests run on **JVM** — fast feedback loop during development
- Ktor client used for networking — **not** platform-specific HTTP clients in shared code
- Kotlinx.serialization used for JSON — **not** platform-specific serializers in shared code
- Framework is **static** (isStatic = true) for iOS distribution
- Memory management follows Kotlin/Native rules — no manual ref counting in shared code
