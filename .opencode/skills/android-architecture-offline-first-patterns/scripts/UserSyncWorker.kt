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