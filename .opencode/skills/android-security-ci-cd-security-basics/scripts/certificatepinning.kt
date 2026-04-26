object CertificatePinning {
    // Current production certificate pin (SHA-256 of SubjectPublicKeyInfo)
    private const val CURRENT_PIN = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

    // Backup pin — for rotation and emergency fallback
    private const val BACKUP_PIN = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="

    // Pin expiry date — rotate before this date
    private const val PIN_EXPIRY = "2026-07-01"

    fun createPinnedClient(): OkHttpClient {
        val certificatePinner = CertificatePinner.Builder()
            .add("api.example.com", "sha256/$CURRENT_PIN")
            .add("api.example.com", "sha256/$BACKUP_PIN")
            .add("cdn.example.com", "sha256/$CURRENT_PIN")
            .build()

        return OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            .connectionSpecs(listOf(ConnectionSpec.RESTRICTED_TLS))
            .build()
    }

    // Pin rotation checklist:
    // 1. Generate new key pair
    // 2. Get certificate signed by CA
    // 3. Add new pin as backup pin
    // 4. Deploy app update with new backup pin
    // 5. Wait for 95%+ adoption
    // 6. Switch old pin to backup, new pin to current
    // 7. Deploy app update
    // 8. Remove old pin after full adoption
}