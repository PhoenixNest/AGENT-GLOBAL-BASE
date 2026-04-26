object SecureStorage {
    private const val PREFS_NAME = "secure_prefs"
    private const val MASTER_KEY_ALIAS = "_androidx_security_master_key_"

    private lateinit var sharedPreferences: SharedPreferences

    fun initialize(context: Context) {
        val masterKey = MasterKey.Builder(context, MASTER_KEY_ALIAS)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        sharedPreferences = EncryptedSharedPreferences.create(
            context,
            PREFS_NAME,
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    fun saveToken(token: String) {
        sharedPreferences.edit()
            .putString("auth_token", token)
            .apply()
    }

    fun getToken(): String? {
        return sharedPreferences.getString("auth_token", null)
    }

    fun clearToken() {
        sharedPreferences.edit()
            .remove("auth_token")
            .apply()
    }

    fun clearAll() {
        sharedPreferences.edit().clear().apply()
    }
}