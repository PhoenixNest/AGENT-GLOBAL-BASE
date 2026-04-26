// commonMain — shared interface
expect class SecureStorage() {
    suspend fun get(key: String): String?
    suspend fun set(key: String, value: String)
    suspend fun delete(key: String)
}

// androidMain — Android Keystore + EncryptedSharedPreferences
actual class SecureStorage actual constructor() {
    private val context = ... // inject via Koin
    actual suspend fun get(key: String): String? = ...
    actual suspend fun set(key: String, value: String) = ...
    actual suspend fun delete(key: String) = ...
}

// iosMain — iOS Keychain
actual class SecureStorage actual constructor() {
    actual suspend fun get(key: String): String? = ...
    actual suspend fun set(key: String, value: String) = ...
    actual suspend fun delete(key: String) = ...
}