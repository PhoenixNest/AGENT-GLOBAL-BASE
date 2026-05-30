---
name: offline_first_patterns
version: "1.0.0"
---

# Offline First Patterns

| Competency                        | Description                                                                                              | Quality Criteria                                                                                                                                       |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Repository Pattern                | Single data access abstraction, cache-then-network strategy, error propagation, data source coordination | ViewModel depends only on repository interface; repository coordinates multiple data sources transparently; error types are domain-specific            |
| Room Database                     | Entity design, DAO queries, TypeConverters, migrations, relations with junction tables, FTS search       | Normalized schema with appropriate denormalization; migrations tested for every schema change; complex queries use EXPLAIN; no N+1 query patterns      |
| Retrofit & API Clients            | Interface definition, interceptors, call adapters, response wrapping, error parsing                      | API interfaces are sealed and versioned; error responses properly deserialized; retry logic for transient failures; timeout configuration per endpoint |
| Serialization                     | Kotlinx Serialization, JSON parsing, protobuf for performance, custom serializers                        | Zero Gson usage (kotlinx.serialization only); custom serializers for edge cases; protobuf for high-throughput endpoints                                |
| WorkManager Scheduling            | One-time vs periodic work, constraints, chaining, input/output data                                      | Work executes reliably across device reboots; constraints correctly applied; work chaining handles partial failures                                    |
| Sync Strategies                   | Pull-based vs push-based sync, delta synchronization, exponential backoff                                | Sync completes within budgeted time window; backoff handles prolonged outages; battery impact <2% daily                                                |
| Conflict Resolution               | Last-write-wins, operational transformation, merge strategies, vector clocks                             | Conflicts detected and resolved deterministically; user notified when manual resolution required; conflict rate tracked as telemetry                   |
| Cache Invalidation                | Cache freshness, time-to-live, stale-while-revalidate, cache-busting                                     | Cache serves data within freshness budget; stale data clearly indicated to user; cache eviction follows LRU or priority-based policy                   |
| Data Synchronization & Pagination | Delta sync, Paging 3, cursor-based navigation, cache invalidation, background sync coordination          | Pagination handles large datasets efficiently; cache TTL enforced; sync conflicts resolved deterministically                                           |

---

## Sync Mechanics

### Offline-First Architecture — Single Source of Truth

**The database is the single source of truth.** UI observes database; repository syncs database with remote. Network is an optimization, not a requirement.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Compose   │────▶│  ViewModel   │────▶│  Repository  │
│    UI Layer  │◀────│  (StateFlow) │◀────│  Interface   │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    ▼                           ▼
                           ┌──────────────┐           ┌──────────────┐
                           │ Room Database│◀─────────▶│   Remote API │
                           │  (Local SSOT)│  Sync     │  (Network)   │
                           └──────────────┘           └──────────────┘
```

**Offline-first repository implementation:**

```kotlin
class UserRepositoryImpl(
    private val userDao: UserDao,
    private val userApi: UserApi,
    private val workManager: WorkManager,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) : UserRepository {

    // UI observes local database — always returns immediately
    override fun observeUser(userId: String): Flow<User> =
        userDao.observeUser(userId).map { entity -> entity.toDomain() }

    // Network fetch updates database; UI gets updated via Flow
    override suspend fun refreshUser(userId: String): Result<Unit> = withContext(ioDispatcher) {
        try {
            val remoteUser = userApi.getUser(userId)
            userDao.upsert(remoteUser.toEntity())
            Result.success(Unit)
        } catch (e: IOException) {
            Result.failure(NetworkUnavailableException(e))
        } catch (e: Exception) {
            Result.failure(SyncException(e))
        }
    }

    // Write operations go to database first, then sync to remote
    override suspend fun updateUser(user: User): Result<Unit> = withContext(ioDispatcher) {
        try {
            userDao.update(user.toEntity().copy(syncStatus = SyncStatus.PENDING))
            enqueueUserSyncWork(user.id)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(LocalWriteException(e))
        }
    }

    private fun enqueueUserSyncWork(userId: String) {
        val workRequest = OneTimeWorkRequestBuilder<UserSyncWorker>()
            .setInputData(workDataOf("userId" to userId))
            .setConstraints(Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()
            )
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 10, TimeUnit.SECONDS)
            .build()

        workManager.enqueueUniqueWork(
            "user_sync_$userId",
            ExistingWorkPolicy.REPLACE,
            workRequest
        )
    }
}
```

### Room Database — Production Schema Design

**Entity design with proper indices and relationships:**

```kotlin
@Entity(
    tableName = "users",
    indices = [
        Index(value = ["email"], unique = true),
        Index(value = ["lastSyncedAt"])
    ],
    foreignKeys = [
        ForeignKey(
            entity = OrderEntity::class,
            parentColumns = ["id"],
            childColumns = ["orderId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    val orderId: String?,
    val syncStatus: SyncStatus = SyncStatus.SYNCED,
    val lastSyncedAt: Long = 0L,
    val createdAt: Long = System.currentTimeMillis()
)

class Converters {
    @TypeConverter fun fromSyncStatus(value: SyncStatus): String = value.name
    @TypeConverter fun toSyncStatus(value: String): SyncStatus = SyncStatus.valueOf(value)
    @TypeConverter fun fromTimestamp(value: Long?): Date? = value?.let { Date(it) }
    @TypeConverter fun dateToTimestamp(date: Date?): Long? = date?.time
}

@Dao
abstract class UserDao {

    @Query("SELECT * FROM users WHERE id = :userId")
    abstract fun observeUser(userId: String): Flow<UserEntity>

    @Query("SELECT * FROM users WHERE syncStatus = :status ORDER BY lastSyncedAt ASC")
    abstract suspend fun getPendingSync(status: SyncStatus = SyncStatus.PENDING): List<UserEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract suspend fun upsert(user: UserEntity)

    @Transaction
    open suspend fun updateUserWithConflictDetection(user: UserEntity) {
        val existing = getUserById(user.id)
        if (existing != null && existing.lastSyncedAt > user.lastSyncedAt) {
            throw ConflictException(localVersion = user, remoteVersion = existing)
        }
        upsert(user)
    }

    @Query("SELECT * FROM users WHERE id = :id")
    abstract suspend fun getUserById(id: String): UserEntity?
}

enum class SyncStatus { SYNCED, PENDING, CONFLICT, ERROR }
```

### WorkManager — Reliable Background Sync

**SyncWorker with conflict resolution and exponential backoff:**

```kotlin
class UserSyncWorker(
    context: Context,
    params: WorkerParameters,
    private val userRepository: UserRepository,
    private val userApi: UserApi,
    private val userDao: UserDao
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val userId = inputData.getString("userId") ?: return@withContext Result.failure()

        try {
            val pendingUsers = userDao.getPendingSync()

            pendingUsers.forEach { userEntity ->
                try {
                    val response = userApi.updateUser(userEntity.id, userEntity.toUpdateRequest())
                    userDao.update(
                        userEntity.copy(
                            syncStatus = SyncStatus.SYNCED,
                            lastSyncedAt = response.serverTimestamp
                        )
                    )
                } catch (e: ConflictException) {
                    val resolution = resolveConflict(userEntity, e.remoteVersion)
                    userDao.update(resolution)
                }
            }

            val latestUser = userApi.getUser(userId)
            userDao.upsert(latestUser.toEntity().copy(syncStatus = SyncStatus.SYNCED))

            Result.success()
        } catch (e: IOException) {
            Result.retry()
        } catch (e: Exception) {
            Log.e(TAG, "Sync failed for user $userId", e)
            Result.failure(workDataOf("error" to e.message))
        }
    }

    private suspend fun resolveConflict(local: UserEntity, remote: UserEntity): UserEntity {
        return if (remote.lastSyncedAt > local.lastSyncedAt) {
            remote.copy(syncStatus = SyncStatus.SYNCED)
        } else {
            local.copy(syncStatus = SyncStatus.PENDING)
        }
    }

    companion object { private const val TAG = "UserSyncWorker" }
}
```

### Conflict Resolution Strategies — Decision Matrix

| Strategy                           | When to Use                            | Implementation Complexity | User Impact                  |
| ---------------------------------- | -------------------------------------- | ------------------------- | ---------------------------- |
| Last-Write-Wins (Server Timestamp) | Simple CRUD, low conflict probability  | Low                       | User may lose recent changes |
| Last-Write-Wins (Client Timestamp) | Clock-synced environments, single-user | Low                       | Risk with clock skew         |
| Merge (Field-Level)                | Documents with independent fields      | Medium                    | Changes preserved per-field  |
| Operational Transform              | Real-time collaborative editing        | High                      | Best UX for collaboration    |
| Manual Resolution                  | Financial transactions, critical data  | Medium                    | User must resolve conflict   |

**Production recommendation:** Last-Write-Wins (server timestamp) for 90% of entities. Merge strategy for user profiles (name, avatar, preferences are independent fields). Manual resolution for financial/transactional data.

### Delta Synchronization

```kotlin
data class SyncRequest(
    val since: Long,
    val clientChecksum: String
)

data class SyncResponse(
    val updated: List<Entity>,
    val deleted: List<String>,
    val serverTimestamp: Long,
    val hasMore: Boolean,
    val nextCursor: String?
)

suspend fun deltaSync(since: Long): SyncResult {
    val request = SyncRequest(since, computeLocalChecksum())
    val response = api.sync(request)

    transaction {
        response.updated.forEach { entity -> dao.upsert(entity) }
        response.deleted.forEach { id -> dao.deleteById(id) }
    }

    return SyncResult(
        appliedCount = response.updated.size + response.deleted.size,
        serverTimestamp = response.serverTimestamp,
        hasMore = response.hasMore
    )
}
```

### Database Migration — Production Discipline

**Every schema change requires a migration. No `fallbackToDestructiveMigration` in production.**

```kotlin
@Database(
    entities = [UserEntity::class, OrderEntity::class],
    version = 3,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {

    companion object {
        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("ALTER TABLE users ADD COLUMN lastSyncedAt INTEGER NOT NULL DEFAULT 0")
            }
        }

        private val MIGRATION_2_3 = object : Migration(2, 3) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("CREATE INDEX IF NOT EXISTS index_users_email ON users(email)")
            }
        }

        fun build(context: Context): AppDatabase {
            return Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
                .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
                .build()
        }
    }
}
```

**Migration testing (required in Stage 7):**

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    private val TEST_DB = "migration-test.db"

    @Test
    fun migrate2To3_containsCorrectData() {
        val helper = MigrationTestHelper(
            InstrumentationRegistry.getInstrumentation(),
            AppDatabase::class.java
        )
        helper.createDatabase(TEST_DB, 2).apply {
            execSQL("INSERT INTO users (id, name, email) VALUES ('1', 'Test', 'test@example.com')")
            close()
        }

        val db3 = helper.runMigrationsAndValidate(TEST_DB, 3, true, MIGRATION_2_3)
        val cursor = db3.query("SELECT lastSyncedAt FROM users WHERE id = '1'")
        assertTrue(cursor.moveToFirst())
        assertEquals(0, cursor.getLong(0))
    }
}
```

---

## Data Access Layer

### Repository Pattern — Cache-Then-Network

**The repository is the single source of truth coordinator. It decides when to read from cache vs network, how to handle errors, and what data shape to return to the domain layer.**

```kotlin
class OrderRepositoryImpl(
    private val orderApi: OrderApi,
    private val orderDao: OrderDao,
    private val orderMapper: OrderMapper,
    private val dtoMapper: DtoMapper,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) : OrderRepository {

    override fun observeOrders(userId: String): Flow<List<Order>> =
        orderDao.observeOrdersByUser(userId)
            .map { entities -> entities.map(orderMapper::toDomain) }
            .flowOn(ioDispatcher)

    // Cache-then-network: emit cache first, then refresh from network
    override fun fetchOrders(userId: String): Flow<Resource<List<Order>>> = flow {
        val cachedOrders = orderDao.getOrdersByUser(userId)
        emit(Resource.Success(cachedOrders.map(orderMapper::toDomain())))

        try {
            val response = orderApi.getOrders(userId)
            val entities = response.orders.map(dtoMapper::toEntity)
            orderDao.upsertAll(entities)
            val freshOrders = orderDao.getOrdersByUser(userId)
            emit(Resource.Success(freshOrders.map(orderMapper::toDomain())))
        } catch (e: IOException) {
            emit(Resource.Error(NetworkException("Failed to refresh orders", e)))
        } catch (e: HttpException) {
            emit(Resource.Error(ApiException(e.code(), e.message())))
        }
    }.flowOn(ioDispatcher)

    override suspend fun createOrder(order: CreateOrderRequest): Result<Order> =
        withContext(ioDispatcher) {
            try {
                val tempOrder = order.toTempEntity()
                orderDao.insert(tempOrder)
                val response = orderApi.createOrder(order)
                val persistedEntity = response.toEntity()
                orderDao.upsert(persistedEntity)
                Result.success(orderMapper.toDomain(persistedEntity))
            } catch (e: Exception) {
                orderDao.markPendingSync(order.toTempEntity().copy(syncStatus = SyncStatus.PENDING))
                Result.failure(SyncPendingException(e))
            }
        }
}

sealed class Resource<out T> {
    data class Success<T>(val data: T) : Resource<T>()
    data class Error(val exception: Exception, val data: Any? = null) : Resource<Nothing>()
    object Loading : Resource<Nothing>()
}
```

### Room Database — Advanced Query Patterns

**Entity with relations and junction tables:**

```kotlin
@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    val userId: String,
    val status: OrderStatus,
    val totalAmount: Long,
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

data class OrderWithItems(
    @Embedded val order: OrderEntity,
    @Relation(parentColumn = "id", entityColumn = "orderId")
    val items: List<OrderItemEntity>
)

@Dao
abstract class OrderDao {

    @Query("""
        SELECT * FROM orders
        WHERE userId = :userId
        ORDER BY createdAt DESC
        LIMIT :limit OFFSET :offset
    """)
    abstract suspend fun getOrdersByUser(userId: String, limit: Int = 50, offset: Int = 0): List<OrderEntity>

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
        deleteOrdersByUser(userId)
        upsertAll(newOrders)
        upsertAllItems(newItems)
    }

    @Query("DELETE FROM orders WHERE userId = :userId")
    abstract suspend fun deleteOrdersByUser(userId: String)
}
```

**Query optimization with EXPLAIN:**

```kotlin
// Before adding index — check query plan in Android Studio Database Inspector:
// EXPLAIN QUERY PLAN SELECT * FROM orders WHERE userId = '123' ORDER BY createdAt DESC
// If output shows "SCAN TABLE orders", add a composite index:

@Entity(
    tableName = "orders",
    indices = [Index(value = ["userId", "createdAt"], unique = false)]
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

class AuthInterceptor(private val tokenProvider: TokenProvider) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenProvider.getAccessToken()
        val request = chain.request().newBuilder().apply {
            token?.let { header("Authorization", "Bearer $it") }
        }.build()

        val response = chain.proceed(request)
        if (response.code == 401) return handleTokenRefresh(chain, request)
        return response
    }

    private fun handleTokenRefresh(chain: Interceptor.Chain, originalRequest: Request): Response {
        val newToken = tokenProvider.refreshAccessToken()
        return chain.proceed(
            originalRequest.newBuilder().header("Authorization", "Bearer $newToken").build()
        )
    }
}

class OfflineInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        return try {
            chain.proceed(chain.request())
        } catch (e: IOException) {
            val cacheRequest = chain.request().newBuilder()
                .header("Cache-Control", "only-if-cached, max-stale=604800")
                .build()
            chain.proceed(cacheRequest)
        }
    }
}

class RetryInterceptor(private val maxRetries: Int = 3) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var retryCount = 0
        var response: Response? = null
        var lastException: IOException? = null

        while (retryCount < maxRetries) {
            try {
                response = chain.proceed(chain.request())
                if (response.isSuccessful) return response
                if (response.code !in 500..599) return response
                response.close()
            } catch (e: IOException) {
                lastException = e
            }
            retryCount++
            Thread.sleep((2L.pow(retryCount) * 1000).toLong())
        }
        throw lastException ?: IOException("Max retries ($maxRetries) exceeded")
    }
}
```

### Kotlinx Serialization — Production Setup

```kotlin
// build.gradle.kts
plugins { kotlin("plugin.serialization") version "1.9.22" }
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
}

@Serializable
data class OrderResponse(
    @SerialName("id") val id: String,
    @SerialName("user_id") val userId: String,
    @SerialName("status") val status: String,
    @SerialName("total_amount") val totalAmount: Long,
    @SerialName("items") val items: List<OrderItemDto> = emptyList()
)

@Serializable
enum class OrderStatus {
    @SerialName("pending") PENDING,
    @SerialName("processing") PROCESSING,
    @SerialName("delivered") DELIVERED,
    @SerialName("cancelled") CANCELLED
}

val Json = kotlinx.serialization.json.Json {
    ignoreUnknownKeys = true
    coerceInputValues = true
    encodeDefaults = false
    explicitNulls = false
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

class OrderListViewModel(private val orderApi: OrderApi, private val userId: String) : ViewModel() {

    val orders: Flow<PagingData<OrderDisplayModel>> = Pager(
        config = PagingConfig(pageSize = 20, enablePlaceholders = false, initialLoadSize = 40)
    ) {
        OrderPagingSource(orderApi, userId)
    }.flow.map { pagingData -> pagingData.map { it.toDisplayModel() } }
     .cachedIn(viewModelScope)
}
```

---

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs define data layer architecture: Room vs SQLite, Retrofit vs Ktor, serialization library, sync strategy selection.
- **Stage 4 (Implementation Plan):** Informs data layer task breakdown, migration sequencing, entity design, Paging 3 integration, and sync strategy in the implementation plan.
- **Stage 5 (Development):** Primary skill for data layer implementation. All repository implementations, Room entities/DAOs, Retrofit clients, serialization, and sync workers follow these patterns.
- **Stage 6 (Code Review):** Review checklist: database migration completeness, offline behavior correctness, sync worker idempotency, conflict resolution determinism, API client timeout configuration.
- **Stage 7 (Automated Testing):** Offline scenario tests, migration tests, sync worker tests with mock network conditions, conflict resolution unit tests, Paging 3 integration tests.
- **Stage 8 (Integrity Verification):** Process death recovery with pending sync work; data consistency after conflict resolution; database schema matches exported schema files.

## Quality Standards

- **100%** UI functionality available offline (read from cache at minimum)
- **Zero** `fallbackToDestructiveMigration` in production database configuration
- **100%** schema changes have explicit Migration objects with test coverage
- **100%** ViewModels depend on repository interfaces — no direct data source access
- **Zero** Gson usage — kotlinx.serialization exclusively for JSON parsing
- **100%** database operations run on `Dispatchers.IO` — no main-thread database access
- All API clients have explicit **timeout configuration** (connect, read, write)
- Sync workers are **idempotent** — safe to retry on failure without data corruption
- Conflict resolution is **deterministic** — same inputs always produce same resolution
- Database queries P95 latency **<50ms** for screens with <1000 records
- Room schema export enabled — every build's schema diff-able against previous version
- WorkManager constraints correctly reflect battery and network budget
- Offline write queue survives process death and device reboot
- Delta sync payload size **<50KB** for typical sync intervals (5 minutes)
- Pagination implemented for all list endpoints with **>50 items** potential
- Monetary values stored as **Long (smallest currency unit)** — never Float/Double
