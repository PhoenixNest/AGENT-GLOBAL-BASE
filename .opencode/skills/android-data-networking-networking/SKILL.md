---
name: android-data-networking-networking
description: Android networking stack — Retrofit service interfaces, OkHttp interceptor chains (auth, caching, retry), GraphQL with Apollo Kotlin, error handling with domain error hierarchies, exponential backoff with jitter, and circuit breaker pattern. Owned by Kwame Osei (Android Engineer). Use during Stage 5 (Development) for network layer implementation and Stage 7 (Automated Testing) for MockWebServer tests. Trigger: android networking, Retrofit, OkHttp, interceptor, GraphQL, Apollo, error handling, retry logic, circuit breaker, exponential backoff.
prerequisites:
  - android-data-networking-data-layer

version: "1.0.0"
---

# Android Networking

**Category:** Mobile Engineering — Android Networking
**Owner:** Android Engineer (Kwame Osei)

## Overview

This skill implements production-grade Android networking covering Retrofit client architecture, OkHttp interceptor chains, GraphQL client integration, error handling strategies, and retry logic with exponential backoff. It applies to Stage 5 (Development) where all network communication is implemented, Stage 6 (Code Review) where network reliability and security are audited, and Stage 7 (Automated Testing) where network-dependent tests use mock servers.

## Competency Dimensions

| Dimension             | Description                                                                                              | Proficiency Indicators                                                                                                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retrofit Architecture | Service interface design, call adapters, response wrapping, dynamic base URLs, multipart uploads         | Interfaces are cohesive and versioned; response types are domain-specific; multipart uploads handle large files with progress callbacks            |
| OkHttp Interceptors   | Request/response interceptors, network interceptors, authentication flow, logging, header management     | Interceptor chain is ordered correctly; auth interceptor handles token refresh atomically; logging interceptor redacts sensitive data              |
| GraphQL Clients       | Apollo Kotlin, query/mutation generation, normalized cache, subscription handling, fragment usage        | GraphQL queries are type-safe; normalized cache reduces redundant network calls; subscriptions handle reconnection gracefully                      |
| Error Handling        | HTTP error mapping, network exception classification, user-friendly error messages, error recovery flows | All HTTP status codes mapped to domain error types; network errors classified (connectivity, timeout, server); user sees actionable error messages |
| Retry Logic           | Exponential backoff, jitter, retry predicates, idempotency guarantees, circuit breaker pattern           | Transient errors retried with backoff; non-idempotent mutations never auto-retried; circuit breaker prevents cascade failures                      |

## Execution Guidance

### Retrofit Service Interface — Production Design

**Cohesive, versioned API interfaces:**

```kotlin
interface UserApi {
    @GET("users/{id}")
    suspend fun getUser(
        @Path("id") userId: String
    ): ApiResponse<UserDto>

    @GET("users")
    suspend fun getUsers(
        @Query("page") page: Int = 1,
        @Query("pageSize") pageSize: Int = 20,
        @Query("sort") sort: String = "created_at",
        @Query("order") order: String = "desc"
    ): ApiResponse<PaginatedResponse<UserDto>>

    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") userId: String,
        @Body request: UpdateUserRequest
    ): ApiResponse<UserDto>

    @DELETE("users/{id}")
    suspend fun deleteUser(
        @Path("id") userId: String
    ): ApiResponse<Unit>

    @Multipart
    @POST("users/{id}/avatar")
    suspend fun uploadAvatar(
        @Path("id") userId: String,
        @Part avatar: MultipartBody.Part,
        @Part("metadata") metadata: RequestBody
    ): ApiResponse<AvatarUploadResponse>
}

// Unified API response wrapper
@Serializable
data class ApiResponse<T>(
    @SerialName("data") val data: T? = null,
    @SerialName("error") val error: ApiError? = null,
    @SerialName("meta") val meta: ResponseMeta? = null
) {
    fun getOrThrow(): T {
        if (data != null) return data
        throw ApiException(
            code = error?.code ?: -1,
            message = error?.message ?: "Unknown error",
            details = error?.details
        )
    }

    fun toResult(): Result<T> {
        return if (data != null) Result.success(data)
        else Result.failure(
            ApiException(
                code = error?.code ?: -1,
                message = error?.message ?: "Unknown error"
            )
        )
    }
}

@Serializable
data class ApiError(
    @SerialName("code") val code: Int,
    @SerialName("message") val message: String,
    @SerialName("details") val details: Map<String, String>? = null
)

@Serializable
data class ResponseMeta(
    @SerialName("request_id") val requestId: String,
    @SerialName("timestamp") val timestamp: Long
)
```

### OkHttp Interceptor Chain — Production Order

**Interceptor ordering matters. Each interceptor has a specific responsibility:**

```kotlin
fun createOkHttpClient(
    authInterceptor: AuthInterceptor,
    loggingInterceptor: HttpLoggingInterceptor,
    cacheSize: Long = 10 * 1024 * 1024 // 10MB
): OkHttpClient {
    val cache = Cache(
        directory = File(context.cacheDir, "http_cache"),
        maxSize = cacheSize
    )

    return OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        // 1. Request interceptor — adds common headers
        .addInterceptor(CommonHeadersInterceptor())
        // 2. Auth interceptor — attaches JWT token
        .addInterceptor(authInterceptor)
        // 3. Logging interceptor — logs request/response (debug only)
        .addInterceptor(loggingInterceptor)
        // 4. Cache interceptor — controls caching behavior
        .addNetworkInterceptor(CacheInterceptor())
        // 5. Retry interceptor — retries transient failures
        .addNetworkInterceptor(RetryInterceptor())
        .cache(cache)
        .build()
}

// Common headers interceptor
class CommonHeadersInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .header("Accept", "application/json")
            .header("Content-Type", "application/json")
            .header("X-App-Version", BuildConfig.VERSION_NAME)
            .header("X-Platform", "android")
            .header("X-Device-Model", Build.MODEL)
            .header("X-OS-Version", Build.VERSION.RELEASE)
            .build()
        return chain.proceed(request)
    }
}

// Auth interceptor with atomic token refresh
class AuthInterceptor(
    private val tokenManager: TokenManager,
    private val refreshApi: RefreshApi
) : Interceptor {

    private val lock = Any() // For thread-safe token refresh

    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        val accessToken = tokenManager.getAccessToken()

        val authenticatedRequest = request.newBuilder()
            .header("Authorization", "Bearer $accessToken")
            .build()

        val response = chain.proceed(authenticatedRequest)

        if (response.code == 401) {
            response.close()
            return synchronized(lock) {
                val newAccessToken = tokenManager.refreshAccessToken(refreshApi)
                val retryRequest = request.newBuilder()
                    .header("Authorization", "Bearer $newAccessToken")
                    .build()
                chain.proceed(retryRequest)
            }
        }

        return response
    }
}

// Cache interceptor — network-level caching
class CacheInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val response = chain.proceed(chain.request())

        val cacheControl = CacheControl.Builder()
            .maxAge(5, TimeUnit.MINUTES)
            .build()

        return response.newBuilder()
            .header("Cache-Control", cacheControl.toString())
            .build()
    }
}
```

### Error Handling — Comprehensive Classification

```kotlin
// Domain error hierarchy
sealed interface NetworkError {
    data class ConnectionError(val message: String) : NetworkError
    data class TimeoutError(val message: String) : NetworkError
    data class ServerError(val code: Int, val message: String) : NetworkError
    data class ClientError(val code: Int, val message: String, val details: Map<String, String>? = null) : NetworkError
    data class AuthError(val message: String) : NetworkError
    object UnknownError : NetworkError
}

// Error mapper — converts HTTP responses to domain errors
object ErrorMapper {
    fun fromException(exception: Throwable): NetworkError {
        return when (exception) {
            is UnknownHostException -> NetworkError.ConnectionError("No internet connection")
            is SocketTimeoutException -> NetworkError.TimeoutError("Request timed out. Please try again.")
            is SSLHandshakeException -> NetworkError.ConnectionError("Secure connection failed")
            is ApiException -> when (exception.code) {
                401 -> NetworkError.AuthError("Session expired. Please log in again.")
                in 400..499 -> NetworkError.ClientError(exception.code, exception.message, exception.details)
                in 500..599 -> NetworkError.ServerError(exception.code, "Server error. Please try again later.")
                else -> NetworkError.UnknownError
            }
            else -> NetworkError.UnknownError
        }
    }

    fun toUserMessage(error: NetworkError): String {
        return when (error) {
            is NetworkError.ConnectionError -> "Check your internet connection and try again."
            is NetworkError.TimeoutError -> "The request took too long. Please try again."
            is NetworkError.ServerError -> "We're experiencing technical difficulties. Please try again later."
            is NetworkError.ClientError -> error.message
            is NetworkError.AuthError -> "Your session has expired. Please log in again."
            NetworkError.UnknownError -> "An unexpected error occurred. Please try again."
        }
    }
}

// Repository error handling
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(userId: String): Result<User> {
        return try {
            val response = api.getUser(userId)
            Result.success(response.getOrThrow().toDomain())
        } catch (e: Exception) {
            val networkError = ErrorMapper.fromException(e)
            Log.e(TAG, "Failed to fetch user $userId: ${ErrorMapper.toUserMessage(networkError)}", e)
            Result.failure(networkError.toException())
        }
    }
}
```

### Retry Logic — Exponential Backoff with Jitter

```kotlin
class RetryInterceptor(
    private val maxRetries: Int = 3,
    private val baseDelayMs: Long = 1000,
    private val maxDelayMs: Long = 30000
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        var response: Response? = null
        var lastException: IOException? = null

        for (attempt in 0..maxRetries) {
            try {
                response = chain.proceed(request)

                // Success or non-retryable error
                if (response.isSuccessful || !isRetryable(response.code)) {
                    return response
                }

                // Close response body before retry
                response.close()

            } catch (e: IOException) {
                lastException = e
            }

            if (attempt < maxRetries) {
                val delay = calculateBackoff(attempt)
                Log.d(TAG, "Retry attempt ${attempt + 1}/$maxRetries after ${delay}ms")
                Thread.sleep(delay)
            }
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exceeded")
    }

    private fun isRetryable(statusCode: Int): Boolean {
        return when (statusCode) {
            408, // Request Timeout
            429, // Too Many Requests
            500, // Internal Server Error
            502, // Bad Gateway
            503, // Service Unavailable
            504  // Gateway Timeout
            -> true
            else -> false
        }
    }

    private fun calculateBackoff(attempt: Int): Long {
        // Exponential backoff with jitter
        val exponentialDelay = minOf(
            baseDelayMs * 2.0.pow(attempt.toDouble()).toLong(),
            maxDelayMs
        )
        // Jitter: random value between 0 and exponentialDelay
        return (Math.random() * exponentialDelay).toLong()
    }

    companion object {
        private const val TAG = "RetryInterceptor"
    }
}
```

### Circuit Breaker Pattern

**Prevent cascade failures when backend is down:**

```kotlin
class CircuitBreaker(
    private val failureThreshold: Int = 5,
    private val recoveryTimeoutMs: Long = 60_000
) {
    private var failureCount = 0
    private var lastFailureTime: Long = 0
    private var state: State = State.CLOSED

    enum class State { CLOSED, OPEN, HALF_OPEN }

    @Synchronized
    fun canExecute(): Boolean {
        return when (state) {
            State.CLOSED -> true
            State.OPEN -> {
                if (System.currentTimeMillis() - lastFailureTime > recoveryTimeoutMs) {
                    state = State.HALF_OPEN
                    true
                } else {
                    false
                }
            }
            State.HALF_OPEN -> true
        }
    }

    @Synchronized
    fun recordSuccess() {
        failureCount = 0
        state = State.CLOSED
    }

    @Synchronized
    fun recordFailure() {
        failureCount++
        lastFailureTime = System.currentTimeMillis()
        if (failureCount >= failureThreshold) {
            state = State.OPEN
        }
    }
}

// Usage in repository
class OrderRepositoryImpl(
    private val api: OrderApi,
    private val circuitBreaker: CircuitBreaker = CircuitBreaker()
) : OrderRepository {

    override suspend fun getOrders(userId: String): Result<List<Order>> {
        if (!circuitBreaker.canExecute()) {
            return Result.failure(CircuitBreakerOpenException())
        }

        return try {
            val response = api.getOrders(userId)
            circuitBreaker.recordSuccess()
            Result.success(response.data ?: emptyList())
        } catch (e: Exception) {
            circuitBreaker.recordFailure()
            Result.failure(e)
        }
    }
}
```

### GraphQL with Apollo Kotlin

```kotlin
// build.gradle.kts
plugins {
    id("com.apollographql.apollo3") version "3.8.2"
}

apollo {
    service("api") {
        packageName.set("com.example.app.graphql")
        schemaFile.set(file("src/main/graphql/schema.graphqls"))
        srcDir("src/main/graphql/")
    }
}

// Apollo client setup
object GraphQlClient {
    private val apolloClient = ApolloClient.Builder()
        .serverUrl("https://api.example.com/graphql")
        .addHttpInterceptor(AuthInterceptor())
        .normalizedCache(
            MemoryCacheFactory(maxSizeBytes = 10 * 1024 * 1024)
        )
        .build()

    suspend fun getUserProfile(userId: String): Result<UserProfile> {
        return try {
            val response = apolloClient.query(GetUserProfileQuery(userId)).execute()
            response.dataAssertNoErrors.let { data ->
                Result.success(data.user.toDomain())
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs define networking stack choices (Retrofit vs Ktor, OkHttp vs native, GraphQL vs REST). API contract specifications defined.
- **Stage 4 (Implementation Plan):** Network layer tasks: API client setup, interceptor chain, error handling, retry logic, GraphQL integration.
- **Stage 5 (Development):** Primary skill for network layer implementation. All Retrofit interfaces, OkHttp interceptors, error mappers, and retry logic.
- **Stage 6 (Code Review):** Network review: interceptor ordering, timeout configuration, error handling completeness, token refresh atomicity, retry idempotency.
- **Stage 7 (Automated Testing):** Network tests with MockWebServer; error handling tests for all HTTP status codes; retry logic tests with simulated failures.

## Quality Standards

- **Zero** hardcoded base URLs — use BuildConfig or remote config
- All API clients have explicit **timeout configuration**: connect 15s, read 30s, write 30s
- **100%** HTTP error responses mapped to domain error types — no raw exceptions to UI
- Auth interceptor handles **atomic token refresh** — synchronized to prevent concurrent refresh
- Retry logic uses **exponential backoff with jitter** — no fixed-delay retries
- **Zero** non-idempotent mutations auto-retried (POST/DELETE never auto-retried)
- Logging interceptor **redacts sensitive data** (tokens, passwords, PII) in release builds
- Circuit breaker implemented for **all external service calls** — prevents cascade failures
- MockWebServer used for **all network-dependent tests** — zero real network calls in tests
- GraphQL queries use **normalized cache** — redundant queries served from cache
- API response wrapper includes **request ID** for server-side correlation
