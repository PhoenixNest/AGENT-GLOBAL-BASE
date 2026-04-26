class RetryInterceptor(
    private val maxRetries: Int = 3,
    private val baseDelayMs: Long = 1000,
    private val maxDelayMs: Long = 30000
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        var response: Response? = null
        var lastException: IOException? = null

        for (attempt in 0..maxRetries) {
            try {
                response = chain.proceed(request)

                // Success or non-retryable error
                if (response.isSuccessful || !isRetryable(response.code)) {
                    return response
                }

                // Close response body before retry
                response.close()

            } catch (e: IOException) {
                lastException = e
            }

            if (attempt < maxRetries) {
                val delay = calculateBackoff(attempt)
                Log.d(TAG, "Retry attempt ${attempt + 1}/$maxRetries after ${delay}ms")
                Thread.sleep(delay)
            }
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exceeded")
    }

    private fun isRetryable(statusCode: Int): Boolean {
        return when (statusCode) {
            408, // Request Timeout
            429, // Too Many Requests
            500, // Internal Server Error
            502, // Bad Gateway
            503, // Service Unavailable
            504  // Gateway Timeout
            -> true
            else -> false
        }
    }

    private fun calculateBackoff(attempt: Int): Long {
        // Exponential backoff with jitter
        val exponentialDelay = minOf(
            baseDelayMs * 2.0.pow(attempt.toDouble()).toLong(),
            maxDelayMs
        )
        // Jitter: random value between 0 and exponentialDelay
        return (Math.random() * exponentialDelay).toLong()
    }

    companion object {
        private const val TAG = "RetryInterceptor"
    }
}