@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class SharedPreferencesStorageTest {

    private lateinit var storage: SharedPreferencesStorage

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        storage = SharedPreferencesStorage(context)
    }

    @Test
    fun `given key exists, when get, then returns value`() {
        // Given
        storage.save("test_key", "test_value")

        // When
        val result = storage.get("test_key")

        // Then
        assertEquals("test_value", result)
    }

    @Test
    fun `given key does not exist, when get, then returns null`() {
        // When
        val result = storage.get("nonexistent_key")

        // Then
        assertNull(result)
    }

    @Test
    fun `when delete, then key is removed`() {
        // Given
        storage.save("test_key", "test_value")

        // When
        storage.delete("test_key")

        // Then
        assertNull(storage.get("test_key"))
    }
}