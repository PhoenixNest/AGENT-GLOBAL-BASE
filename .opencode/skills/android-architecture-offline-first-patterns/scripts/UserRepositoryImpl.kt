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