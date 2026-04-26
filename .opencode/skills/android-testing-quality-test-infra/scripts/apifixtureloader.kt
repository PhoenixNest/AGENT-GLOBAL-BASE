object ApiFixtureLoader {
    inline fun <reified T> loadResponse(fileName: String): T {
        val inputStream = javaClass.classLoader
            ?.getResourceAsStream("api-responses/$fileName")
            ?: throw IllegalArgumentException("Fixture not found: $fileName")

        val json = inputStream.bufferedReader().use { it.readText() }
        return Json.decodeFromString(json)
    }
}

// Usage in tests
@Test
fun `given success response, when fetch orders, then returns mapped orders`() = runTest {
    // Given
    val mockResponse = ApiFixtureLoader.loadResponse<OrderApiResponse>("orders-success.json")
    every { orderApi.getOrders(any()) } returns mockResponse

    // When
    val result = repository.fetchOrders("user-123")

    // Then
    // Assertions...
}