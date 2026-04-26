// MARK: - commonMain

// Storage abstraction — platform-specific implementation
expect class SecureStorage() {
    suspend fun put(key: String, value: String)
    suspend fun get(key: String): String?
    suspend fun delete(key: String)
    suspend fun clear()
}

// Network client abstraction
expect fun createHttpClient(): HttpClient

// Platform info
expect object PlatformInfo {
    val name: String
    val version: String
    val osVersion: String
}

// MARK: - androidMain

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

actual class SecureStorage actual constructor() {
    private lateinit var preferences: EncryptedSharedPreferences

    actual suspend fun put(key: String, value: String) {
        ensureInitialized()
        preferences.edit().putString(key, value).apply()
    }

    actual suspend fun get(key: String): String? {
        ensureInitialized()
        return preferences.getString(key, null)
    }

    actual suspend fun delete(key: String) {
        ensureInitialized()
        preferences.edit().remove(key).apply()
    }

    actual suspend fun clear() {
        ensureInitialized()
        preferences.edit().clear().apply()
    }

    private fun ensureInitialized() {
        if (::preferences.isInitialized) return
        val context = getAppContext()  // Provided via DI
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
        preferences = EncryptedSharedPreferences.create(
            context,
            "secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        ) as EncryptedSharedPreferences
    }
}

actual fun createHttpClient(): HttpClient {
    return HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 15_000
        }
    }
}

actual object PlatformInfo {
    actual val name: String = "Android"
    actual val version: String = BuildConfig.VERSION_NAME
    actual val osVersion: String = Build.VERSION.RELEASE
}

// MARK: - iosMain

import platform.Foundation.NSUserDefaults
import platform.Foundation.NSKeyedArchiver

actual class SecureStorage actual constructor() {
    private val userDefaults = NSUserDefaults.standardUserDefaults

    actual suspend fun put(key: String, value: String) {
        userDefaults.setObject(value, key)
        userDefaults.synchronize()
    }

    actual suspend fun get(key: String): String? {
        return userDefaults.stringForKey(key)
    }

    actual suspend fun delete(key: String) {
        userDefaults.removeObjectForKey(key)
        userDefaults.synchronize()
    }

    actual suspend fun clear() {
        val dictionary = userDefaults.dictionaryRepresentation()
        dictionary.keys.forEach { key ->
            userDefaults.removeObjectForKey(key as String)
        }
        userDefaults.synchronize()
    }
}

actual fun createHttpClient(): HttpClient {
    return HttpClient(Darwin) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 15_000
        }
        engine {
            configureRequest {
                setAllowsCellularAccess(true)
            }
        }
    }
}

actual object PlatformInfo {
    actual val name: String = "iOS"
    actual val version: String = NSBundle.mainBundle.infoDictionary?.getValue("CFBundleShortVersionString") as? String ?: "unknown"
    actual val osVersion: String = UIDevice.currentDevice.systemVersion
}