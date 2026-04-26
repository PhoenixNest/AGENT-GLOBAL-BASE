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