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