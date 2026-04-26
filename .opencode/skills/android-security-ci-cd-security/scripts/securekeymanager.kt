object SecureKeyManager {
    private const val KEY_ALIAS = "app_master_key"
    private const val KEYSTORE_PROVIDER = "AndroidKeyStore"
    private const val ALGORITHM = KeyProperties.KEY_ALGORITHM_AES
    private const val BLOCK_MODE = KeyProperties.BLOCK_MODE_GCM
    private const val PADDING = KeyProperties.ENCRYPTION_PADDING_NONE

    fun generateMasterKey(context: Context) {
        val keyStore = KeyStore.getInstance(KEYSTORE_PROVIDER).apply { load(null) }

        if (keyStore.containsAlias(KEY_ALIAS)) return

        val keyGenerator = KeyGenerator.getInstance(ALGORITHM, KEYSTORE_PROVIDER)
        keyGenerator.init(
            KeyGenParameterSpec.Builder(KEY_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(BLOCK_MODE)
                .setEncryptionPaddings(PADDING)
                .setKeySize(256)
                .setUserAuthenticationRequired(true)
                .setUserAuthenticationValidityDurationSeconds(30)
                .setIsStrongBoxBacked(true)  // Hardware-backed on supported devices
                .build()
        )
        keyGenerator.generateKey()
    }

    fun encrypt(plaintext: ByteArray): EncryptedData {
        val keyStore = KeyStore.getInstance(KEYSTORE_PROVIDER).apply { load(null) }
        val secretKey = keyStore.getKey(KEY_ALIAS, null) as SecretKey

        val cipher = Cipher.getInstance("$ALGORITHM/$BLOCK_MODE/$PADDING")
        cipher.init(Cipher.ENCRYPT_MODE, secretKey)

        val ciphertext = cipher.doFinal(plaintext)
        return EncryptedData(ciphertext, cipher.iv)
    }

    fun decrypt(encryptedData: EncryptedData): ByteArray {
        val keyStore = KeyStore.getInstance(KEYSTORE_PROVIDER).apply { load(null) }
        val secretKey = keyStore.getKey(KEY_ALIAS, null) as SecretKey

        val cipher = Cipher.getInstance("$ALGORITHM/$BLOCK_MODE/$PADDING")
        val spec = GCMParameterSpec(128, encryptedData.iv)
        cipher.init(Cipher.DECRYPT_MODE, secretKey, spec)

        return cipher.doFinal(encryptedData.ciphertext)
    }
}

data class EncryptedData(val ciphertext: ByteArray, val iv: ByteArray)