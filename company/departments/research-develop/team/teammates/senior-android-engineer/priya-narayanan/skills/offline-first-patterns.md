---
version: "1.0.0"
---

------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Room Database Design | Entity relationships, type converters, indices, migrations, FTS full-text search | Normalized schema with appropriate denormalization for read patterns; migration paths tested for every schema change; query performance <50ms for P95 |
| WorkManager Scheduling | One-time vs periodic work, constraints, chaining, input/output data | Work executes reliably across device reboots; constraints (network type, charging) correctly applied; work chaining handles partial failures |
| Sync Strategies | Pull-based vs push-based sync, delta synchronization, exponential backoff | Sync completes within budgeted time window; backoff handles prolonged outages gracefully; battery impact <2% daily |
| Conflict Resolution | Last-write-wins, operational transformation, merge strategies, vector clocks | Conflicts detected and resolved deterministically; user notified when manual resolution required; conflict rate tracked as telemetry |
| Cache Invalidation & TTL | Cache freshness, time-to-live, stale-while-revalidate, cache-busting | Cache serves data within freshness budget; stale data clearly indicated to user; cache eviction follows LRU or priority-based policy |

## Execution Guidance

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

**Repository implementation:**

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
            // Network unavailable — database still serves cached data
            Result.failure(NetworkUnavailableException(e))
        } catch (e: Exception) {
            Result.failure(SyncException(e))
        }
    }

    // Write operations go to database first, then sync to remote
    override suspend fun updateUser(user: User): Result<Unit> = withContext(ioDispatcher) {
        try {
            // 1. Optimistic write to local database
            userDao.update(user.toEntity().copy(syncStatus = SyncStatus.PENDING))

            // 2. Enqueue sync work
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

// Type converters for complex types
class Converters {
    @TypeConverter
    fun fromSyncStatus(value: SyncStatus): String = value.name

    @TypeConverter
    fun toSyncStatus(value: String): SyncStatus = SyncStatus.valueOf(value)

    @TypeConverter
    fun fromTimestamp(value: Long?): Date? = value?.let { Date(it) }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? = date?.time
}

// DAO with Flow-based observation and conflict detection
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
            // Remote version is newer — conflict detected
            throw ConflictException(
                localVersion = user,
                remoteVersion = existing
            )
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
                    // Push local changes to remote
                    val response = userApi.updateUser(userEntity.id, userEntity.toUpdateRequest())

                    // Update local sync status
                    userDao.update(
                        userEntity.copy(
                            syncStatus = SyncStatus.SYNCED,
                            lastSyncedAt = response.serverTimestamp
                        )
                    )
                } catch (e: ConflictException) {
                    // Server has newer version — resolve conflict
                    val resolution = resolveConflict(userEntity, e.remoteVersion)
                    userDao.update(resolution)
                }
            }

            // Pull latest from server
            val latestUser = userApi.getUser(userId)
            userDao.upsert(latestUser.toEntity().copy(syncStatus = SyncStatus.SYNCED))

            Result.success()
        } catch (e: IOException) {
            // Network error — retry with backoff
            Result.retry()
        } catch (e: Exception) {
            // Non-retryable error
            Log.e(TAG, "Sync failed for user $userId", e)
            Result.failure(workDataOf("error" to e.message))
        }
    }

    private suspend fun resolveConflict(
        local: UserEntity,
        remote: UserEntity
    ): UserEntity {
        // Strategy: Last-write-wins with server timestamp
        // Alternative: Merge strategy for non-overlapping fields
        return if (remote.lastSyncedAt > local.lastSyncedAt) {
            remote.copy(syncStatus = SyncStatus.SYNCED)
        } else {
            local.copy(syncStatus = SyncStatus.PENDING) // Retry sync
        }
    }

    companion object {
        private const val TAG = "UserSyncWorker"
    }
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

**For bandwidth-constrained environments, sync only changes:**

```kotlin
data class SyncRequest(
    val since: Long,          // Last known server timestamp
    val clientChecksum: String // Hash of local state for integrity
)

data class SyncResponse(
    val updated: List<Entity>,
    val deleted: List<String>,
    val serverTimestamp: Long,
    val hasMore: Boolean,
    val nextCursor: String?
)

// Repository delta sync
suspend fun deltaSync(since: Long): SyncResult {
    val request = SyncRequest(since, computeLocalChecksum())
    val response = api.sync(request)

    transaction {
        response.updated.forEach { entity ->
            dao.upsert(entity)
        }
        response.deleted.forEach { id ->
            dao.deleteById(id)
        }
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
    exportSchema = true  // Exports schema to build output for diff verification
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
                // NEVER use fallbackToDestructiveMigration in production
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
        // Create database at version 2
        val helper = MigrationTestHelper(
            InstrumentationRegistry.getInstrumentation(),
            AppDatabase::class.java
        )
        val db2 = helper.createDatabase(TEST_DB, 2).apply {
            execSQL("INSERT INTO users (id, name, email) VALUES ('1', 'Test', 'test@example.com')")
            close()
        }

        // Migrate to version 3
        val db3 = helper.runMigrationsAndValidate(TEST_DB, 3, true, MIGRATION_2_3)

        // Verify data preserved
        val cursor = db3.query("SELECT lastSyncedAt FROM users WHERE id = '1'")
        assertTrue(cursor.moveToFirst())
        assertEquals(0, cursor.getLong(0))
    }
}
```

## Pipeline Integration

- **Stage 4 (Implementation Plan):** Informs data layer task breakdown, migration sequencing, and sync strategy selection in implementation plan.
- **Stage 5 (Development):** Primary skill for data layer implementation. Room entities, DAOs, sync workers, and conflict resolution logic.
- **Stage 6 (Code Review):** Review checklist: database migration completeness, offline behavior correctness, sync worker idempotency, conflict resolution determinism.
- **Stage 7 (Automated Testing):** Offline scenario tests, migration tests, sync worker tests with mock network conditions, conflict resolution unit tests.
- **Stage 8 (Integrity Verification):** Process death recovery with pending sync work; data consistency after conflict resolution; database schema matches exported schema files.

## Quality Standards

- **100%** UI functionality available offline (read from cache at minimum)
- **Zero** `fallbackToDestructiveMigration` in production database configuration
- **100%** schema changes have explicit Migration objects with test coverage
- Sync workers are **idempotent** — safe to retry on failure without data corruption
- Conflict resolution is **deterministic** — same inputs always produce same resolution
- Database queries P95 latency **<50ms** for screens with <1000 records
- Room schema export enabled — every build's schema diff-able against previous version
- WorkManager constraints correctly reflect battery and network budget
- Offline write queue survives process death and device reboot
- Delta sync payload size **<50KB** for typical sync intervals (5 minutes)
