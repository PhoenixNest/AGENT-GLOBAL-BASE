interface ItemRepository {
    suspend fun getItems(): Result<List<Item>>
    fun observeItems(): Flow<List<Item>>
}

class ItemRepositoryImpl @Inject constructor(
    private val remoteSource: ItemRemoteDataSource,
    private val localSource: ItemLocalDataSource
) : ItemRepository {
    // Implementation: local-first with remote sync
}