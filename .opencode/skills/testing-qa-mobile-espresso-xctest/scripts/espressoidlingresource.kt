object EspressoIdlingResource {
    private const val RESOURCE = "network_call"

    @JvmField
    val countingIdlingResource = CountingIdlingResource(RESOURCE)

    fun increment() { countingIdlingResource.increment() }
    fun decrement() { countingIdlingResource.decrement() }

    init {
        check(!countingIdlingResource.isIdleNow) { "Should not be idle at init" }
    }
}

// In your Retrofit/OkHttp interceptor:
class IdlingResourceInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        EspressoIdlingResource.increment()
        return try {
            chain.proceed(chain.request())
        } finally {
            EspressoIdlingResource.decrement()
        }
    }
}