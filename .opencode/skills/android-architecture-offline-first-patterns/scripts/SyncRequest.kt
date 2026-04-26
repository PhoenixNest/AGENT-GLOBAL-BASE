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