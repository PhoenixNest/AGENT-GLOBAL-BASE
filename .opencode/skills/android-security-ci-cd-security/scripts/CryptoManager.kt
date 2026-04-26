class CryptoManager(
    private val context: Context,
    private val keyManager: SecureKeyManager
) {
    fun decryptOrHandleError(encryptedData: EncryptedData): Result<ByteArray> = runCatching {
        try {
            keyManager.decrypt(encryptedData)
        } catch (e: KeyPermanentlyInvalidatedException) {
            // User changed lock screen — data is unrecoverable
            // Must re-authenticate and re-encrypt
            handleKeyInvalidation()
            throw SecurityException("Key invalidated. Re-authentication required.")
        } catch (e: UserNotAuthenticatedException) {
            // Biometric authentication needed — show BiometricPrompt
            throw AuthenticationRequiredException()
        }
    }

    private fun handleKeyInvalidation() {
        // Clear corrupted encrypted data
        // Notify user to re-authenticate and re-sync
        // Log security event for audit
    }
}