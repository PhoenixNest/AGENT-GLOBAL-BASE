# KMP Architecture

**Category:** Mobile Engineering — Cross-Platform Architecture (KMP)
**Owner:** Cross-Platform Engineer (Dmitri Volkov)

## Overview

This skill defines Clean Architecture with Kotlin Multiplatform covering shared domain layer design, platform adapters, dependency injection across platforms, and architectural boundary enforcement. It applies to Stage 5 (Development) where the architectural backbone for cross-platform code is established, Stage 6 (Code Review) where layer compliance and boundary enforcement are audited, and Stage 8 (Integrity Verification) where architectural integrity is verified on both platforms.

## Competency Dimensions

| Dimension                   | Description                                                                                                | Proficiency Indicators                                                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Clean Architecture with KMP | Layer separation across platform boundaries, dependency inversion, shared domain, platform adapters        | Domain layer in commonMain with zero platform dependencies; platform adapters implement domain interfaces; dependency graph flows inward  |
| Shared Domain Layer         | Pure Kotlin entities, use case interactors, repository interfaces, error hierarchies, validation           | All domain code in commonMain; use cases are testable on JVM; error types are sealed interfaces; validation logic is shared               |
| Platform Adapters           | Adapter pattern for platform-specific implementations, interface contracts, adapter testing                | Each platform implements domain interfaces via adapters; adapters are thin wrappers; adapter behavior tested per platform                 |
| Cross-Platform DI           | Koin module composition, platform-specific module overrides, test module substitution, lazy initialization | DI modules composed per platform; shared modules define core bindings; platform modules override as needed; test modules substitute mocks |
| Boundary Enforcement        | Compile-time checks, source set dependencies, import restrictions, architecture tests                      | Domain layer cannot import platform packages; architecture tests run on CI; import violations caught at compile time                      |

## Execution Guidance

### Clean Architecture — KMP Layer Structure

```
shared/
├── commonMain/
│   └── kotlin/
│       ├── domain/                    # ← PURE KOTLIN (no platform deps)
│       │   ├── model/                 #    Domain entities
│       │   ├── repository/            #    Repository interfaces
│       │   ├── usecase/               #    Use case interactors
│       │   └── error/                 #    Domain error hierarchy
│       ├── data/                      # ← SHARED DATA ABSTRACTIONS
│       │   ├── remote/                #    API client interfaces
│       │   ├── local/                 #    Storage interfaces
│       │   └── mapper/                #    DTO ↔ Domain mappers
│       └── di/                        # ← SHARED DI MODULES
│           └── AppModule.kt
│
├── androidMain/
│   └── kotlin/
│       ├── data/
│       │   ├── remote/                # ← Retrofit implementations
│       │   │   └── RetrofitUserApi.kt
│       │   └── local/                 # ← Room/SharedPreferences
│       │       └── AndroidSecureStorage.kt
│       └── di/
│           └── PlatformModule.kt      # ← Android-specific bindings
│
└── iosMain/
    └── kotlin/
        ├── data/
        │   ├── remote/                # ← Ktor/Darwin implementations
        │   │   └── KtorUserApi.kt
        │   └── local/                 # ← Keychain/UserDefaults
        │       └── IosSecureStorage.kt
        └── di/
            └── PlatformModule.kt      # ← iOS-specific bindings
```

### Shared Domain Layer — Complete Implementation

```kotlin
// MARK: - Domain Entities (commonMain/domain/model/)

@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val role: UserRole,
    val createdAt: Instant,
    val updatedAt: Instant
) {
    val displayName: String
        get() = name.ifBlank { email.substringBefore("@") }

    fun hasPermission(permission: Permission): Boolean {
        return role.permissions.contains(permission)
    }
}

@Serializable
enum class UserRole {
    ADMIN, EDITOR, VIEWER;

    val permissions: Set<Permission>
        get() = when (this) {
            ADMIN -> Permission.values().toSet()
            EDITOR -> setOf(Permission.READ, Permission.WRITE)
            VIEWER -> setOf(Permission.READ)
        }
}

@Serializable
enum class Permission { READ, WRITE, DELETE, ADMIN }

// MARK: - Repository Interfaces (commonMain/domain/repository/)

interface UserRepository {
    fun observeUser(id: String): Flow<User>
    suspend fun fetchUser(id: String): Either<DomainError, User>
    suspend fun updateUser(user: User): Either<DomainError, Unit>
    suspend fun deleteUser(id: String): Either<DomainError, Unit>
    suspend fun searchUsers(query: String): Either<DomainError, List<User>>
}

interface AuthRepository {
    suspend fun login(email: String, password: String): Either<DomainError, AuthToken>
    suspend fun logout(): Either<DomainError, Unit>
    suspend fun refreshToken(): Either<DomainError, AuthToken>
    fun observeAuthState(): Flow<AuthState>
    val currentUserId: String?
}

// MARK: - Use Case Interactors (commonMain/domain/usecase/)

class GetUserProfileUseCase(
    private val userRepository: UserRepository,
    private val authRepository: AuthRepository
) {
    suspend operator fun invoke(): Either<DomainError, User> {
        val userId = authRepository.currentUserId
            ?: return Either.Left(DomainError.Unauthenticated)

        if (userId.isBlank()) {
            return Either.Left(DomainError.InvalidArgument("User ID is empty"))
        }

        return userRepository.fetchUser(userId)
    }
}

class UpdateUserProfileUseCase(
    private val userRepository: UserRepository,
    private val authRepository: AuthRepository
) {
    suspend operator fun invoke(request: UpdateUserRequest): Either<DomainError, User> {
        val userId = authRepository.currentUserId
            ?: return Either.Left(DomainError.Unauthenticated)

        // Validate request
        request.validate().onLeft { return Either.Left(it) }

        // Fetch current user
        val currentUser = userRepository.fetchUser(userId)
            .onLeft { return it }

        // Apply updates
        val updatedUser = currentUser.copy(
            name = request.name ?: currentUser.name,
            email = request.email ?: currentUser.email
        )

        // Save
        return userRepository.updateUser(updatedUser)
            .map { updatedUser }
    }
}

data class UpdateUserRequest(
    val name: String?,
    val email: String?
) {
        fun validate(): Either<DomainError, Unit> {
            name?.let {
                if (it.length > 100) {
                    return Either.Left(DomainError.InvalidArgument("Name too long"))
                }
            }
            email?.let {
                if (!android.util.Patterns.EMAIL_ADDRESS.matcher(it).matches()) {
                    return Either.Left(DomainError.InvalidArgument("Invalid email"))
                }
            }
            return Either.Right(Unit)
        }
}

// MARK: - Domain Error Hierarchy (commonMain/domain/error/)

sealed interface DomainError {
    val message: String

    data class UserNotFound(val userId: String) : DomainError {
        override val message = "User not found: $userId"
    }

    data class InvalidArgument(val reason: String) : DomainError {
        override val message = "Invalid argument: $reason"
    }

    object Unauthenticated : DomainError {
        override val message = "Authentication required"
    }

    object Unauthorized : DomainError {
        override val message = "Insufficient permissions"
    }

    object NetworkUnavailable : DomainError {
        override val message = "Network connection unavailable"
    }

    data class ServerError(val code: Int, val detail: String) : DomainError {
        override val message = "Server error ($code): $detail"
    }

    data class Unknown(override val message: String) : DomainError
}

// MARK: - Either Type (common utility)

sealed class Either<out L, out R> {
    data class Left<out L>(val value: L) : Either<L, Nothing>()
    data class Right<out R>(val value: R) : Either<Nothing, R>()

    fun isLeft(): Boolean = this is Left
    fun isRight(): Boolean = this is Right

    fun <T> map(transform: (R) -> T): Either<L, T> = when (this) {
        is Left -> Left(value)
        is Right -> Right(transform(value))
    }

    fun <T> flatMap(transform: (R) -> Either<L, T>): Either<L, T> = when (this) {
        is Left -> Left(value)
        is Right -> transform(value)
    }

    fun onLeft(action: (L) -> Unit): Either<L, R> {
        if (this is Left) action(value)
        return this
    }

    fun getOrThrow(): R = when (this) {
        is Left -> throw RuntimeException("Left: $value")
        is Right -> value
    }
}
```

### Platform Adapters

```kotlin
// MARK: - Android Adapter (androidMain/)

class AndroidUserRepository(
    private val api: UserApi,
    private val database: UserDao,
    private val mapper: UserMapper
) : UserRepository {

    override fun observeUser(id: String): Flow<User> {
        return database.observeUser(id)
            .map { entity -> mapper.toDomain(entity) }
    }

    override suspend fun fetchUser(id: String): Either<DomainError, User> {
        return try {
            val response = api.getUser(id)
            val entity = mapper.toEntity(response)
            database.upsert(entity)
            Either.Right(mapper.toDomain(entity))
        } catch (e: IOException) {
            // Try cache
            val cached = database.getUser(id)
            if (cached != null) {
                return Either.Right(mapper.toDomain(cached))
            }
            Either.Left(DomainError.NetworkUnavailable)
        } catch (e: HttpException) {
            when (e.code()) {
                404 -> Either.Left(DomainError.UserNotFound(id))
                401 -> Either.Left(DomainError.Unauthenticated)
                in 500..599 -> Either.Left(DomainError.ServerError(e.code(), e.message()))
                else -> Either.Left(DomainError.Unknown(e.message()))
            }
        }
    }

    override suspend fun updateUser(user: User): Either<DomainError, Unit> {
        return try {
            val request = mapper.toUpdateRequest(user)
            api.updateUser(user.id, request)
            database.upsert(mapper.toEntity(user))
            Either.Right(Unit)
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }

    override suspend fun deleteUser(id: String): Either<DomainError, Unit> {
        return try {
            api.deleteUser(id)
            database.delete(id)
            Either.Right(Unit)
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }

    override suspend fun searchUsers(query: String): Either<DomainError, List<User>> {
        return try {
            val response = api.searchUsers(query)
            val entities = response.map { mapper.toEntity(it) }
            database.upsertAll(entities)
            Either.Right(entities.map { mapper.toDomain(it) })
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }
}

// MARK: - iOS Adapter (iosMain/)

class IosUserRepository(
    private val api: UserApi,
    private val storage: IosUserStorage,
    private val mapper: UserMapper
) : UserRepository {

    override fun observeUser(id: String): Flow<User> {
        return storage.observeUser(id)
            .map { entity -> mapper.toDomain(entity) }
    }

    override suspend fun fetchUser(id: String): Either<DomainError, User> {
        return try {
            val response = api.getUser(id)
            val entity = mapper.toEntity(response)
            storage.saveUser(entity)
            Either.Right(mapper.toDomain(entity))
        } catch (e: IOException) {
            val cached = storage.getUser(id)
            if (cached != null) {
                return Either.Right(mapper.toDomain(cached))
            }
            Either.Left(DomainError.NetworkUnavailable)
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }

    override suspend fun updateUser(user: User): Either<DomainError, Unit> {
        return try {
            val request = mapper.toUpdateRequest(user)
            api.updateUser(user.id, request)
            storage.saveUser(mapper.toEntity(user))
            Either.Right(Unit)
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }

    override suspend fun deleteUser(id: String): Either<DomainError, Unit> {
        return try {
            api.deleteUser(id)
            storage.deleteUser(id)
            Either.Right(Unit)
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }

    override suspend fun searchUsers(query: String): Either<DomainError, List<User>> {
        return try {
            val response = api.searchUsers(query)
            val entities = response.map { mapper.toEntity(it) }
            storage.saveUsers(entities)
            Either.Right(entities.map { mapper.toDomain(it) })
        } catch (e: Exception) {
            Either.Left(DomainError.Unknown(e.message ?: "Unknown error"))
        }
    }
}
```

### Cross-Platform DI with Koin

```kotlin
// MARK: - Shared DI Module (commonMain/di/)

val sharedModule = module {
    // Use cases
    factory { GetUserProfileUseCase(get(), get()) }
    factory { UpdateUserProfileUseCase(get(), get()) }
    factory { DeleteUserUseCase(get(), get()) }
    factory { SearchUsersUseCase(get()) }

    // Mappers
    factory { UserMapper() }
    factory { AuthMapper() }

    // Network client (expect/actual)
    single { createHttpClient() }

    // API client
    single { UserApiImpl(get()) }
}

// MARK: - Android DI Module (androidMain/di/)

val androidPlatformModule = module {
    single<UserRepository> {
        AndroidUserRepository(
            api = get(),
            database = get(),
            mapper = get()
        )
    }

    single<AuthRepository> {
        AndroidAuthRepository(
            api = get(),
            secureStorage = get(),
            mapper = get()
        )
    }

    single { provideRoomDatabase(get()) }
    single { get<AppDatabase>().userDao() }
    single { SecureStorage() }  // Android implementation
}

// MARK: - iOS DI Module (iosMain/di/)

val iosPlatformModule = module {
    single<UserRepository> {
        IosUserRepository(
            api = get(),
            storage = get(),
            mapper = get()
        )
    }

    single<AuthRepository> {
        IosAuthRepository(
            api = get(),
            secureStorage = get(),
            mapper = get()
        )
    }

    single { IosUserStorage() }
    single { SecureStorage() }  // iOS implementation
}

// MARK: - DI Initialization

// Android
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(sharedModule, androidPlatformModule)
        }
    }
}

// iOS
class DIContainer {
    companion object {
        fun initialize() {
            startKoin {
                modules(sharedModule, iosPlatformModule)
            }
        }
    }
}

// Swift usage
// DIContainer.Companion.initialize()
// let userRepository = KoinHelper().getUserRepository()
```

### Architecture Tests

```kotlin
// Compile-time architecture enforcement via source set dependencies

// build.gradle.kts — enforce layer boundaries
kotlin {
    sourceSets {
        val commonMain by getting {
            dependencies {
                // Only allow pure Kotlin libraries
                api(libs.kotlinx.coroutines.core)
                api(libs.koin.core)
                api(libs.kotlinx.serialization.json)
                // NO Android or iOS dependencies here
            }
        }

        val androidMain by getting {
            dependencies {
                // Android-specific dependencies only
                api(libs.androidx.room.runtime)
                api(libs.retrofit)
                // Can depend on commonMain
            }
        }
    }
}

// Runtime architecture test (commonTest/)
class ArchitectureTest {

    @Test
    fun `domain layer has no platform dependencies`() {
        val domainPackage = "com.example.shared.domain"
        val forbiddenImports = listOf(
            "android.",
            "kotlinx.android.",
            "io.ktor.client.engine.android",
            "io.ktor.client.engine.darwin",
            "platform."
        )

        // Scan domain classes for forbidden imports
        // This is typically done via detekt or custom Gradle plugin
        val violations = scanPackage(domainPackage, forbiddenImports)
        assertTrue(
            violations.isEmpty(),
            "Domain layer has platform dependencies: $violations"
        )
    }

    @Test
    fun `all expect declarations have actual implementations`() {
        val expectDeclarations = findExpectDeclarations()
        val actualImplementations = findActualImplementations()

        expectDeclarations.forEach { expect ->
            assertTrue(
                actualImplementations.containsKey(expect),
                "Missing actual implementation for: ${expect.name}"
            )
            val actuals = actualImplementations[expect]!!
            assertTrue(
                actuals.size >= 2,  // At least Android + iOS
                "Incomplete actual implementations for: ${expect.name} (found ${actuals.size})"
            )
        }
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Clean Architecture with KMP. Layer boundaries, shared domain scope, and platform adapter contracts defined.
- **Stage 4 (Implementation Plan):** Architecture tasks include: shared module setup, domain layer design, platform adapter contracts, DI module composition.
- **Stage 5 (Development):** Primary skill for KMP architecture implementation. All shared domain code, platform adapters, and DI modules.
- **Stage 6 (Code Review):** Architecture review: layer boundary compliance, expect/actual completeness, DI module correctness, platform adapter thinness.
- **Stage 8 (Integrity Verification):** Architecture tests run on both platforms. Shared domain behavior verified to be identical across platforms.

## Quality Standards

- **Zero** platform imports in commonMain/domain — compile-time enforced
- **100%** domain use cases testable on JVM — no platform dependencies
- Repository interfaces defined in domain — **implemented** in platform adapters
- Platform adapters are **thin wrappers** — no business logic in adapters
- DI modules composed per platform — **sharedModule + platformModule** pattern
- Either type used for error handling — **no exceptions** crossing layer boundaries
- All domain entities are **Serializable** — for cross-platform data transfer
- Use cases have **single responsibility** — one use case per file
- Architecture tests run on **CI** — layer violations caught automatically
- Shared module **>70% code sharing** ratio for business logic
- Platform-specific code limited to: UI, storage, networking engine, cryptography
