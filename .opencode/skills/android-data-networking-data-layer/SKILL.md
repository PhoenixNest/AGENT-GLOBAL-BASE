---
name: android-data-networking-data-layer
description: Android data layer implementation — repository pattern with cache-then-network strategy, Room database entities and DAOs, Retrofit API clients, kotlinx.serialization, Paging 3 integration, and data synchronization mechanisms. Owned by Nina Bergström (Android Engineer). Use during Stage 5 (Development) for data layer implementation and Stage 6 (Code Review) for data flow correctness. Trigger: android data layer, repository pattern, room database, Retrofit, kotlinx serialization, paging, data sync, cache then network, DAO.
prerequisites:
  - android-language-core-implementation

version: "1.0.0"
---

# Android Data Layer

**Category:** Mobile Engineering — Android Data Architecture
**Owner:** Android Engineer (Nina Bergström)

## Overview

This skill implements the Android data layer covering the Repository pattern, Room database operations, Retrofit API clients, serialization strategies, and data synchronization mechanisms. It applies to Stage 5 (Development) where the data layer is the foundation for all platform code, Stage 6 (Code Review) where data flow correctness and error handling are audited, and Stage 7 (Automated Testing) where data layer tests validate repository contracts.

## Competency Dimensions

| Dimension              | Description                                                                                              | Proficiency Indicators                                                                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Repository Pattern     | Single data access abstraction, cache-then-network strategy, error propagation, data source coordination | ViewModel depends only on repository interface; repository coordinates multiple data sources transparently; error types are domain-specific            |
| Room Database          | Entity design, DAO queries, TypeConverters, migrations, relations with junction tables, FTS search       | Schema properly indexed; migrations tested; complex queries use EXPLAIN for optimization; no N+1 query patterns                                        |
| Retrofit & API Clients | Interface definition, interceptors, call adapters, response wrapping, error parsing                      | API interfaces are sealed and versioned; error responses properly deserialized; retry logic for transient failures; timeout configuration per endpoint |
| Serialization          | Kotlinx Serialization, JSON parsing, protobuf for performance, custom serializers                        | Zero Gson usage (kotlinx.serialization only); custom serializers for edge cases; protobuf for high-throughput endpoints                                |
| Data Synchronization   | Delta sync, pagination, cursor-based navigation, cache invalidation, background sync coordination        | Pagination handles large datasets efficiently; cache TTL enforced; sync conflicts resolved deterministically                                           |

## Execution Guidance

### Repository Pattern — Production Implementation

**The repository is the single source of truth coordinator. It decides when to read from cache vs network, how to handle errors, and what data shape to return to the domain layer.**

```kotlin
class OrderRepositoryImpl(
    private val orderApi: OrderApi,
    private val orderDao: OrderDao,
    private val orderMapper: OrderMapper,
    private val dtoMapper: DtoMapper,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) : OrderRepository {

    // Observe local database — always returns immediately (offline-first)
    override fun observeOrders(userId: String): Flow<List<Order>> =
        orderDao.observeOrdersByUser(userId)
            .map { entities -> entities.map(orderMapper::toDomain) }
            .flowOn(ioDispatcher)

    // Cache-then-network: emit cache first, then refresh from network
    override fun fetchOrders(userId: String): Flow<Resource<List<Order>>> = flow {
        // 1. Emit cached data immediately
        val cachedOrders = orderDao.getOrdersByUser(userId)
        emit(Resource.Success(cachedOrders.map(orderMapper::toDomain())))

        // 2. Fetch from network and update cache
        try {
            val response = orderApi.getOrders(userId)
            val entities = response.orders.map(dtoMapper::toEntity)
            orderDao.upsertAll(entities)

            // 3. Emit fresh data
            val freshOrders = orderDao.getOrdersByUser(userId)
            emit(Resource.Success(freshOrders.map(orderMapper::toDomain())))
        } catch (e: IOException) {
            // Network error — cache is still valid
            emit(Resource.Error(NetworkException("Failed to refresh orders", e)))
        } catch (e: HttpException) {
            emit(Resource.Error(ApiException(e.code(), e.message())))
        }
    }.flowOn(ioDispatcher)

    // Write-through: save locally first, then sync to remote
    override suspend fun createOrder(order: CreateOrderRequest): Result<Order> =
        withContext(ioDispatcher) {
            try {
                // Optimistic local write
                val tempOrder = order.toTempEntity()
                orderDao.insert(tempOrder)

                // Network call
                val response = orderApi.createOrder(order)
                val persistedEntity = response.toEntity()

                // Replace temp with server-confirmed entity
                orderDao.upsert(persistedEntity)

                Result.success(orderMapper.toDomain(persistedEntity))
            } catch (e: Exception) {
                // Mark as pending sync for retry
                orderDao.markPendingSync(order.toTempEntity().copy(
                    syncStatus = SyncStatus.PENDING
                ))
                Result.failure(SyncPendingException(e))
            }
        }
}

// Resource wrapper for cache-then-network flows
sealed class Resource<out T> {
    data class Success<T>(val data: T) : Resource<T>()
    data class Error(val exception: Exception, val data: Any? = null) : Resource<Nothing>()
    object Loading : Resource<Nothing>()
}
```

### Room Database — Advanced Patterns

**Entity with relations and junction tables:**

```kotlin
@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    val userId: String,
    val status: OrderStatus,
    val totalAmount: Long,  // Store as Long (cents) to avoid floating point issues
    val createdAt: Long,
    val updatedAt: Long,
    val syncStatus: SyncStatus = SyncStatus.SYNCED
)

@Entity(tableName = "order_items")
data class OrderItemEntity(
    @PrimaryKey val id: String,
    val orderId: String,
    val productId: String,
    val productName: String,
    val quantity: Int,
    val unitPrice: Long
)

// Relation with junction — one order has many items
data class OrderWithItems(
    @Embedded val order: OrderEntity,
    @Relation(
        parentColumn = "id",
        entityColumn = "orderId"
    )
    val items: List<OrderItemEntity>
)

// DAO with optimized queries
@Dao
abstract class OrderDao {

    @Query("""
        SELECT * FROM orders
        WHERE userId = :userId
        ORDER BY createdAt DESC
        LIMIT :limit OFFSET :offset
    """)
    abstract suspend fun getOrdersByUser(
        userId: String,
        limit: Int = 50,
        offset: Int = 0
    ): List<OrderEntity>

    @Query("SELECT * FROM orders WHERE userId = :userId ORDER BY createdAt DESC")
    abstract fun observeOrdersByUser(userId: String): Flow<List<OrderEntity>>

    @Transaction
    @Query("SELECT * FROM orders WHERE id = :orderId")
    abstract suspend fun getOrderWithItems(orderId: String): OrderWithItems?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract suspend fun upsert(order: OrderEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract suspend fun upsertAll(orders: List<OrderEntity>)

    @Transaction
    open suspend fun replaceOrdersForUser(
        userId: String,
        newOrders: List<OrderEntity>,
        newItems: List<OrderItemEntity>
    ) {
        // Delete old orders and items in single transaction
        deleteOrdersByUser(userId)
        upsertAll(newOrders)
        upsertAllItems(newItems)
    }

    @Query("DELETE FROM orders WHERE userId = :userId")
    abstract suspend fun deleteOrdersByUser(userId: String)

    @Query("DELETE FROM order_items WHERE orderId IN (SELECT id FROM orders WHERE userId = :userId)")
    abstract suspend fun deleteItemsByUser(userId: String)

    @Query("""
        SELECT COUNT(*) FROM orders
        WHERE syncStatus = :status
    """)
    abstract suspend fun getPendingSyncCount(status: SyncStatus = SyncStatus.PENDING): Int
}
```

**Query optimization with EXPLAIN:**

```kotlin
// Before adding index — check query plan
// Run in Android Studio Database Inspector:
// EXPLAIN QUERY PLAN SELECT * FROM orders WHERE userId = '123' ORDER BY createdAt DESC

// If output shows "SCAN TABLE orders", add index:
@Entity(
    tableName = "orders",
    indices = [
        Index(value = ["userId", "createdAt"], unique = false)  // Composite index
    ]
)
data class OrderEntity(...)

// After index — EXPLAIN should show "SEARCH TABLE orders USING INDEX ..."
```

### Retrofit API Client — Production Configuration

```kotlin
object ApiClient {
    private const val BASE_URL = "https://api.example.com/v2/"
    private const val CONNECT_TIMEOUT = 15L
    private const val READ_TIMEOUT = 30L
    private const val WRITE_TIMEOUT = 30L

    fun create(
        authInterceptor: AuthInterceptor,
        loggingInterceptor: HttpLoggingInterceptor
    ): Retrofit {
        val okHttpClient = OkHttpClient.Builder()
            .connectTimeout(CONNECT_TIMEOUT, TimeUnit.SECONDS)
            .readTimeout(READ_TIMEOUT, TimeUnit.SECONDS)
            .writeTimeout(WRITE_TIMEOUT, TimeUnit.SECONDS)
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .addInterceptor(OfflineInterceptor())
            .addNetworkInterceptor(RetryInterceptor(maxRetries = 3))
            .build()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
            .build()
    }
}

// Auth interceptor — attaches JWT token
class AuthInterceptor(private val tokenProvider: TokenProvider) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenProvider.getAccessToken()
        val request = chain.request().newBuilder().apply {
            token?.let { header("Authorization", "Bearer $it") }
        }.build()

        val response = chain.proceed(request)

        if (response.code == 401) {
            // Token expired — refresh and retry
            return handleTokenRefresh(chain, request)
        }

        return response
    }

    private fun handleTokenRefresh(
        chain: Interceptor.Chain,
        originalRequest: Request
    ): Response {
        val newToken = tokenProvider.refreshAccessToken()
        val retryRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer $newToken")
            .build()
        return chain.proceed(retryRequest)
    }
}

// Offline interceptor — return cached response when offline
class OfflineInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()

        return try {
            chain.proceed(request)
        } catch (e: IOException) {
            // Network unavailable — try cache
            val cacheRequest = request.newBuilder()
                .header("Cache-Control", "only-if-cached, max-stale=604800")
                .build()
            chain.proceed(cacheRequest)
        }
    }
}

// Retry interceptor — exponential backoff for transient errors
class RetryInterceptor(private val maxRetries: Int = 3) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var retryCount = 0
        var response: Response? = null
        var lastException: IOException? = null

        while (retryCount < maxRetries) {
            try {
                response = chain.proceed(chain.request())
                if (response.isSuccessful) return response

                // Retry on 5xx server errors
                if (response.code !in 500..599) return response

                response.close()
            } catch (e: IOException) {
                lastException = e
            }

            retryCount++
            Thread.sleep((2L.pow(retryCount) * 1000).toLong()) // Exponential backoff
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exceeded")
    }
}
```

### Kotlinx Serialization — Production Setup

**Replace Gson with kotlinx.serialization:**

```kotlin
// build.gradle.kts
plugins {
    kotlin("plugin.serialization") version "1.9.22"
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
    implementation("io.ktor:ktor-client-serialization:2.3.7")
}

// DTO with serialization annotations
@Serializable
data class OrderResponse(
    @SerialName("id") val id: String,
    @SerialName("user_id") val userId: String,
    @SerialName("status") val status: String,
    @SerialName("total_amount") val totalAmount: Long,
    @SerialName("created_at") val createdAt: Long,
    @SerialName("items") val items: List<OrderItemDto> = emptyList()
)

@Serializable
data class OrderItemDto(
    @SerialName("id") val id: String,
    @SerialName("product_id") val productId: String,
    @SerialName("product_name") val productName: String,
    @SerialName("quantity") val quantity: Int,
    @SerialName("unit_price") val unitPrice: Long
)

// Custom serializer for enum
@Serializable
@SerialName("order_status")
enum class OrderStatus {
    @SerialName("pending") PENDING,
    @SerialName("processing") PROCESSING,
    @SerialName("shipped") SHIPPED,
    @SerialName("delivered") DELIVERED,
    @SerialName("cancelled") CANCELLED
}

// Custom serializer for complex types
object DateSerializer : KSerializer<Long> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("Date", PrimitiveKind.LONG)

    override fun serialize(encoder: Encoder, value: Long) {
        encoder.encodeLong(value)
    }

    override fun deserialize(decoder: Decoder): Long {
        return decoder.decodeLong()
    }
}

// JSON configuration
val Json = kotlinx.serialization.json.Json {
    ignoreUnknownKeys = true        // Forward-compatible with API additions
    coerceInputValues = true        // Handle null for non-nullable fields
    encodeDefaults = false          // Don't serialize default values
    explicitNulls = false           // Don't serialize null values
}
```

### Pagination — Paging 3 Integration

```kotlin
class OrderPagingSource(
    private val orderApi: OrderApi,
    private val userId: String
) : PagingSource<Int, OrderDto>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, OrderDto> {
        val page = params.key ?: 1

        return try {
            val response = orderApi.getOrders(userId, page = page, pageSize = params.loadSize)

            LoadResult.Page(
                data = response.orders,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (response.orders.isEmpty()) null else page + 1
            )
        } catch (e: IOException) {
            LoadResult.Error(e)
        } catch (e: HttpException) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, OrderDto>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            state.closestPageToPosition(anchorPosition)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchorPosition)?.nextKey?.minus(1)
        }
    }
}

// ViewModel integration
class OrderListViewModel(
    private val orderApi: OrderApi,
    private val userId: String
) : ViewModel() {

    val orders: Flow<PagingData<OrderDisplayModel>> = Pager(
        config = PagingConfig(
            pageSize = 20,
            enablePlaceholders = false,
            initialLoadSize = 40
        )
    ) {
        OrderPagingSource(orderApi, userId)
    }.flow.map { pagingData ->
        pagingData.map { dto -> dto.toDisplayModel() }
    }.cachedIn(viewModelScope)
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs define data layer architecture: Room vs SQLite, Retrofit vs Ktor, serialization library choice. Repository interfaces defined in domain layer.
- **Stage 4 (Implementation Plan):** Data layer tasks include: entity design, DAO implementation, API client setup, mapper creation, synchronization logic.
- **Stage 5 (Development):** Primary skill for data layer implementation. All repository implementations, Room entities/DAOs, Retrofit clients, and serialization follow these patterns.
- **Stage 6 (Code Review):** Data layer review: repository contract adherence, error propagation correctness, database migration completeness, API client timeout configuration.
- **Stage 7 (Automated Testing):** Repository unit tests with fake data sources; Room migration tests; Retrofit client tests with MockWebServer.

## Quality Standards

- **100%** ViewModels depend on repository interfaces — no direct data source access
- **Zero** Gson usage — kotlinx.serialization exclusively for JSON parsing
- **100%** database operations run on `Dispatchers.IO` — no main-thread database access
- All API clients have explicit **timeout configuration** (connect, read, write)
- **100%** API error responses properly deserialized and mapped to domain error types
- Database queries use **composite indices** for multi-column WHERE clauses
- **Zero** N+1 query patterns — use `@Relation` or JOIN queries for related data
- Pagination implemented for all list endpoints with **>50 items** potential
- Monetary values stored as **Long (smallest currency unit)** — never Float/Double
- Repository methods return `Flow` for observable data, `suspend` for one-shot operations
- All mappers are pure functions — no side effects in DTO ↔ Entity ↔ Domain transformations
