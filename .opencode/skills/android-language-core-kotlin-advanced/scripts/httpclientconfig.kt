fun httpClientConfig(block: HttpClientConfig.() -> Unit): HttpClientConfig {
    return HttpClientConfig().apply(block)
}

class HttpClientConfig {
    var baseUrl: String = ""
    var timeout: Long = 30_000
    val interceptors = mutableListOf<Interceptor>()

    fun interceptor(interceptor: Interceptor) {
        interceptors += interceptor
    }
}

// Usage
val config = httpClientConfig {
    baseUrl = "https://api.example.com"
    timeout = 15_000
    interceptor(AuthInterceptor(tokenProvider))
    interceptor(LoggingInterceptor())
}