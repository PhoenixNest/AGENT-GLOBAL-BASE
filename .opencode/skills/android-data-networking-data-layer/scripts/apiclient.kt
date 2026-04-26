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

// Auth interceptor — attaches JWT token
class AuthInterceptor(private val tokenProvider: TokenProvider) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenProvider.getAccessToken()
        val request = chain.request().newBuilder().apply {
            token?.let { header("Authorization", "Bearer $it") }
        }.build()

        val response = chain.proceed(request)

        if (response.code == 401) {
            // Token expired — refresh and retry
            return handleTokenRefresh(chain, request)
        }

        return response
    }

    private fun handleTokenRefresh(
        chain: Interceptor.Chain,
        originalRequest: Request
    ): Response {
        val newToken = tokenProvider.refreshAccessToken()
        val retryRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer $newToken")
            .build()
        return chain.proceed(retryRequest)
    }
}

// Offline interceptor — return cached response when offline
class OfflineInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()

        return try {
            chain.proceed(request)
        } catch (e: IOException) {
            // Network unavailable — try cache
            val cacheRequest = request.newBuilder()
                .header("Cache-Control", "only-if-cached, max-stale=604800")
                .build()
            chain.proceed(cacheRequest)
        }
    }
}

// Retry interceptor — exponential backoff for transient errors
class RetryInterceptor(private val maxRetries: Int = 3) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var retryCount = 0
        var response: Response? = null
        var lastException: IOException? = null

        while (retryCount < maxRetries) {
            try {
                response = chain.proceed(chain.request())
                if (response.isSuccessful) return response

                // Retry on 5xx server errors
                if (response.code !in 500..599) return response

                response.close()
            } catch (e: IOException) {
                lastException = e
            }

            retryCount++
            Thread.sleep((2L.pow(retryCount) * 1000).toLong()) // Exponential backoff
        }

        throw lastException ?: IOException("Max retries ($maxRetries) exceeded")
    }
}