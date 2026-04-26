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