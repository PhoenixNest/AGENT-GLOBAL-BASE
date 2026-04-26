class MockApiServer {

    private val server = MockWebServer()

    fun start() {
        server.start()
    }

    fun shutdown() {
        server.shutdown()
    }

    fun baseUrl(): String = server.url("/").toString()

    fun enqueueResponse(
        fileName: String,
        responseCode: Int = 200,
        headers: Map<String, String> = emptyMap()
    ) {
        val inputStream = javaClass.classLoader?.getResourceAsStream("api-responses/$fileName")
        val body = inputStream?.bufferedReader()?.use { it.readText() } ?: ""

        val mockResponse = MockResponse()
            .setResponseCode(responseCode)
            .setBody(body)

        headers.forEach { (key, value) ->
            mockResponse.setHeader(key, value)
        }

        server.enqueue(mockResponse)
    }

    fun takeRequest(): RecordedRequest = server.takeRequest(5, TimeUnit.SECONDS)
        ?: throw AssertionError("No request received")
}

// Test fixture JSON files in src/test/resources/api-responses/
// user-success.json, user-not-found.json, server-error.json, etc.