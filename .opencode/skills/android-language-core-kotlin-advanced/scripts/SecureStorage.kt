// shared/src/commonMain/kotlin/
expect class SecureStorage() {
    suspend fun put(key: String, value: String)
    suspend fun get(key: String): String?
    suspend fun delete(key: String)
}

// androidMain/kotlin/
actual class SecureStorage actual constructor() {
    private val preferences = EncryptedSharedPreferences(...)
    actual suspend fun put(key: String, value: String) = ...
    actual suspend fun get(key: String): String? = ...
    actual suspend fun delete(key: String) = ...
}

// iosMain/kotlin/
actual class SecureStorage actual constructor() {
    actual suspend fun put(key: String, value: String) = ...
    actual suspend fun get(key: String): String? = ...
    actual suspend fun delete(key: String) = ...
}