object SecureHttpClient {
    private const val PIN_TYPE = "sha256/"
    private const val BACKUP_PIN_EXPIRY_DAYS = 90

    fun createPinnedClient(
        hostname: String,
        pins: Set<String>,
        backupPins: Set<String>
    ): OkHttpClient {
        val certificatePinner = CertificatePinner.Builder().apply {
            pins.forEach { pin -> add(hostname, "$PIN_TYPE$pin") }
            backupPins.forEach { pin -> add(hostname, "$PIN_TYPE$pin") }
        }.build()

        return OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            .sslSocketFactory(
                TlsConfiguration.createSslSocketFactory(),
                TlsConfiguration.createTrustManager()
            )
            .connectionSpecs(listOf(ConnectionSpec.RESTRICTED_TLS))
            .addInterceptor(NetworkSecurityInterceptor())
            .build()
    }
}

// Network Security Config (res/xml/network_security_config.xml)
/*
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set pin-set-expiration="2026-07-01" android:backupPinSet="true">
            <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
            <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
*/