---
name: android_security
version: "1.0.0"
---

# Android Security

| Competency                          | Description                                                                                                               | Quality Criteria                                                                                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OWASP MASVS Compliance              | Understanding of MASVS V1-V8 control families, L1 vs L2 certification levels, L1 control checklist, verification evidence | Maps every security requirement from SRD to specific MASVS control IDs; achieves L1 baseline for all production releases; achieves L2 for sensitive features; documents verification evidence       |
| Secure Storage                      | EncryptedSharedPreferences, Android Keystore, internal storage, external storage restrictions                             | All sensitive data stored encrypted; no sensitive data in SharedPreferences plaintext; file permissions restricted to app-only                                                                      |
| Android Keystore & Cryptography     | Key generation, hardware-backed storage (StrongBox), key attestation, encryption/decryption lifecycle, key rotation       | Uses Android Keystore for all cryptographic keys; implements key rotation; handles key invalidation gracefully (KeyPermanentlyInvalidatedException, UserNotAuthenticatedException)                  |
| Secure Networking & Cert Pinning    | TLS configuration, certificate pinning, network security configuration, MITM protection, pin rotation strategy            | Certificate pinning with backup pins on all production endpoints; Network Security Config disables cleartext; OkHttp configured with RESTRICTED_TLS; pin rotation tested                            |
| Input Validation                    | Whitelist validation, sanitization, SQL injection prevention, XSS prevention in WebViews, deep link validation            | All user input validated before processing; parameterized queries exclusively; WebView JavaScript disabled unless required; deep links validated against allowlist                                  |
| Security Hygiene & Data Protection  | Debug flags, log sanitization, screenshot protection, clipboard protection, intent security, data leakage prevention      | `debuggable=false` in release; no sensitive data in logs; FLAG_SECURE on sensitive screens; clipboard cleared on background; no PII in recent tasks                                                 |
| Code Obfuscation & Tamper Detection | R8/ProGuard rules, integrity checks, root/jailbreak detection, debugger detection                                         | R8 shrinking removes 40%+ unused code; anti-tampering checks trigger graceful degradation; `debuggable=false` in all release builds; SafetyNet/Play Integrity API integrated with graceful fallback |

## L1 Baseline Controls

### OWASP MASVS L1 — Control Checklist

| MASVS Control | Description                                | Android Implementation                                         | Verification                       |
| ------------- | ------------------------------------------ | -------------------------------------------------------------- | ---------------------------------- |
| V1-1          | Device security requirements met           | minSdkVersion 24+; requires screen lock for sensitive features | Device policy check                |
| V1-2          | Data protected via screen lock             | BiometricPrompt for sensitive operations                       | Manual test with/without biometric |
| V2-1          | All traffic uses TLS                       | Network Security Config blocks cleartext                       | Network traffic analysis           |
| V2-2          | TLS settings follow best practices         | OkHttp with RESTRICTED_TLS spec                                | SSL Labs scan                      |
| V2-4          | Certificate pinning for critical endpoints | OkHttp CertificatePinner                                       | MITM proxy test                    |
| V3-1          | No sensitive data in keyboard cache        | `textNoSuggestions` input type                                 | Manual keyboard inspection         |
| V3-2          | No sensitive data in clipboard             | Clipboard cleared on background                                | Clipboard inspection               |
| V4-1          | System credential storage for secrets      | Android Keystore for all keys                                  | KeyStore inspection                |
| V4-4          | Sensitive data encrypted at rest           | EncryptedSharedPreferences                                     | File system hex dump               |
| V5-1          | No sensitive data in logs                  | ProGuard logging removal in release                            | Logcat inspection                  |
| V5-2          | No sensitive data in UI snapshot           | FLAG_SECURE on sensitive screens                               | Recent tasks inspection            |
| V6-1          | Code obfuscated and optimized              | R8 full mode enabled                                           | APK decompilation                  |
| V6-3          | App resists reverse engineering            | R8 obfuscation + integrity checks                              | Decompilation analysis             |
| V7-1          | No hardcoded secrets                       | BuildConfig + CI secrets                                       | Source code scan                   |
| V7-2          | No hardcoded credentials                   | Token-based auth only                                          | Source code scan                   |
| V8-1          | Biometric authentication implemented       | BiometricPrompt API                                            | Manual biometric test              |

### Secure Storage — Production Implementation

**EncryptedSharedPreferences for sensitive user data:**

```kotlin
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
        sharedPreferences.edit().putString("auth_token", token).apply()
    }

    fun getToken(): String? = sharedPreferences.getString("auth_token", null)

    fun clearToken() {
        sharedPreferences.edit().remove("auth_token").apply()
    }

    fun clearAll() {
        sharedPreferences.edit().clear().apply()
    }
}
```

**Internal storage for files — never external storage for sensitive data:**

```kotlin
class SecureFileManager(private val context: Context) {

    fun saveSensitiveFile(fileName: String, data: ByteArray) {
        context.openFileOutput(fileName, Context.MODE_PRIVATE).use { it.write(data) }
    }

    fun readSensitiveFile(fileName: String): ByteArray {
        return context.openFileInput(fileName).use { it.readBytes() }
    }

    fun deleteSensitiveFile(fileName: String) {
        val file = File(context.filesDir, fileName)
        if (file.exists()) {
            FileOutputStream(file).use { fos ->
                val randomData = ByteArray(file.length().toInt())
                SecureRandom().nextBytes(randomData)
                fos.write(randomData)
                fos.flush()
            }
            file.delete()
        }
    }

    // NEVER use external storage for sensitive data
    fun saveNonSensitiveCache(fileName: String, data: ByteArray) {
        val cacheDir = context.getExternalFilesDir(null)
        File(cacheDir, fileName).writeBytes(data)
    }
}
```

### Certificate Pinning — L1 Implementation

```kotlin
object CertificatePinning {
    private const val CURRENT_PIN = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
    private const val BACKUP_PIN = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="

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
    // 1. Generate new key pair and get certificate signed by CA
    // 2. Add new pin as backup pin; deploy app update
    // 3. Wait for 95%+ adoption
    // 4. Switch old pin to backup, new pin to current; deploy app update
    // 5. Remove old pin after full adoption
}
```

### Input Validation — Defense in Depth

```kotlin
object InputValidator {

    private val EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    )
    private val NAME_PATTERN = Pattern.compile("^[\\p{L}\\s\\-']{1,100}$")
    private val USERNAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_]{3,20}$")

    fun validateEmail(email: String): Result<String> = when {
        email.isBlank() -> Result.failure(ValidationError("Email is required"))
        !EMAIL_PATTERN.matcher(email).matches() ->
            Result.failure(ValidationError("Invalid email format"))
        else -> Result.success(email.trim().lowercase())
    }

    fun validateName(name: String): Result<String> = when {
        name.isBlank() -> Result.failure(ValidationError("Name is required"))
        !NAME_PATTERN.matcher(name).matches() ->
            Result.failure(ValidationError("Name contains invalid characters"))
        else -> Result.success(name.trim())
    }

    fun validateUsername(username: String): Result<String> = when {
        username.isBlank() -> Result.failure(ValidationError("Username is required"))
        !USERNAME_PATTERN.matcher(username).matches() ->
            Result.failure(ValidationError("Username must be 3-20 alphanumeric characters or underscores"))
        else -> Result.success(username.trim().lowercase())
    }

    fun sanitizeHtml(input: String): String = input
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&#x27;")

    private val ALLOWED_SCHEMES = setOf("https")
    private val ALLOWED_HOSTS = setOf("example.com", "www.example.com")

    fun validateDeepLink(uri: Uri): Result<Uri> = when {
        uri.scheme !in ALLOWED_SCHEMES ->
            Result.failure(ValidationError("Invalid scheme: ${uri.scheme}"))
        uri.host !in ALLOWED_HOSTS ->
            Result.failure(ValidationError("Untrusted host: ${uri.host}"))
        else -> Result.success(uri)
    }
}

@JvmInline
value class ValidationError(val message: String) : Exception(message)
```

### Security Hygiene — Production Configuration

**AndroidManifest.xml security settings:**

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="false"
        android:fullBackupContent="false"
        android:networkSecurityConfig="@xml/network_security_config"
        android:usesCleartextTraffic="false">

        <!-- FLAG_SECURE set programmatically in onCreate for sensitive screens -->
        <activity android:name=".ui.payment.PaymentActivity"
            android:windowSoftInputMode="adjustResize" />

        <!-- Deep link validation via Digital Asset Links -->
        <activity android:name=".ui.deeplink.DeepLinkActivity"
            android:exported="true">
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" android:host="example.com" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

**Network Security Configuration:**

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Debug overrides — only in debug builds -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

**Screenshot protection and clipboard hygiene:**

```kotlin
class SecurityActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
        setContentView(R.layout.activity_payment)
    }

    override fun onPause() {
        super.onPause()
        val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.clearPrimaryClip()
    }
}
```

**ProGuard/R8 — Remove logging in release:**

```proguard
-assumenosideeffects class android.util.Log {
    public static int d(...);
    public static int v(...);
    public static java.lang.String getStackTraceString(java.lang.Throwable);
}
```

---

## L2 Advanced Controls

### OWASP MASVS Traceability — SRD → Control → Verification

| MASVS Control | Requirement                                | Android Implementation                                        | Verification Method                                                   |
| ------------- | ------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------------------------- |
| V2-1          | All app traffic uses TLS                   | Network Security Config + OkHttp TLS 1.2+                     | Network traffic analysis; `adb shell cmd connectivity detect-network` |
| V2-4          | Certificate pinning for critical endpoints | OkHttp CertificatePinner with backup pins                     | MITM proxy test; pin rotation drill                                   |
| V3-1          | No sensitive data in keyboard cache        | `inputType="textNoSuggestions"` + `importantForAutofill="no"` | Manual inspection; automated accessibility scan                       |
| V4-1          | Keystore-backed cryptographic keys         | `KeyGenerator` with `setIsStrongBoxBacked(true)`              | KeyStore inspection; StrongBox availability check                     |
| V4-4          | All sensitive data encrypted at rest       | EncryptedSharedPreferences + SQLCipher                        | File system inspection; hex dump of database files                    |
| V5-2          | Root detection with graceful degradation   | SafetyNet/Play Integrity API + heuristic checks               | Rooted emulator test; SafetyNet CTS profile verification              |
| V6-1          | All code obfuscated and optimized          | R8 with custom `-keep` rules                                  | APK decompilation; class/method count comparison                      |
| V8-1          | Biometric authentication with fallback     | BiometricPrompt with device credential fallback               | Biometric enrollment/revocation tests                                 |

### Android Keystore — Hardware-Backed Key Management

**Key generation with StrongBox backing and attestation:**

```kotlin
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
        return EncryptedData(cipher.doFinal(plaintext), cipher.iv)
    }

    fun decrypt(encryptedData: EncryptedData): ByteArray {
        val keyStore = KeyStore.getInstance(KEYSTORE_PROVIDER).apply { load(null) }
        val secretKey = keyStore.getKey(KEY_ALIAS, null) as SecretKey
        val cipher = Cipher.getInstance("$ALGORITHM/$BLOCK_MODE/$PADDING")
        cipher.init(Cipher.DECRYPT_MODE, secretKey, GCMParameterSpec(128, encryptedData.iv))
        return cipher.doFinal(encryptedData.ciphertext)
    }
}

data class EncryptedData(val ciphertext: ByteArray, val iv: ByteArray)
```

**Key invalidation handling — critical for user experience:**

```kotlin
class CryptoManager(
    private val context: Context,
    private val keyManager: SecureKeyManager
) {
    fun decryptOrHandleError(encryptedData: EncryptedData): Result<ByteArray> = runCatching {
        try {
            keyManager.decrypt(encryptedData)
        } catch (e: KeyPermanentlyInvalidatedException) {
            // User changed lock screen — data is unrecoverable; must re-authenticate and re-encrypt
            handleKeyInvalidation()
            throw SecurityException("Key invalidated. Re-authentication required.")
        } catch (e: UserNotAuthenticatedException) {
            // Biometric authentication needed — show BiometricPrompt
            throw AuthenticationRequiredException()
        }
    }

    private fun handleKeyInvalidation() {
        // Clear corrupted encrypted data, notify user to re-authenticate and re-sync,
        // and log security event for audit
    }
}
```

### Secure Networking — Advanced Certificate Pinning

```kotlin
object SecureHttpClient {
    private const val PIN_TYPE = "sha256/"

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

// Network Security Config with expiring pin-set (res/xml/network_security_config.xml)
/*
<domain-config>
    <domain includeSubdomains="true">api.example.com</domain>
    <pin-set pin-set-expiration="2026-07-01" android:backupPinSet="true">
        <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
        <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
    </pin-set>
</domain-config>
*/
```

### R8/ProGuard — Production Rules

**Critical keep rules for reflection-based libraries:**

```proguard
# app/proguard-rules.pro

-keep class com.example.domain.model.** { *; }
-keepclassmembers class com.example.domain.model.** { <fields>; }

-keep class com.example.data.local.entity.** { *; }
-keep class com.example.data.local.dao.** { *; }
-keep class * extends androidx.room.RoomDatabase

-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep class * extends dagger.hilt.android.internal.managers.ViewComponentManager { *; }

-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembers class kotlinx.coroutines.** { volatile <fields>; }

-allowaccessmodification
-optimizations !code/simplification/arithmetic,!code/allocation/variable
-optimizationpasses 5
-dontusemixedcaseclassnames
```

**Verify R8 output:**

```bash
./gradlew :app:analyzeReleaseBundle
apkanalyzer apk summary app-release.apk
# Sensitive class names should be obfuscated
apkanalyzer apk classes app-release.apk | grep -i "password\|token\|secret"
# Should return zero results
```

### Data Leakage Prevention

```kotlin
class SecurityWindowManager(private val window: Window) {

    fun preventScreenshots() {
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
}

class SecureLogger {
    companion object {
        private const val TAG = "App"
        private const val IS_DEBUG = BuildConfig.DEBUG

        fun d(message: String, throwable: Throwable? = null) {
            if (IS_DEBUG) Log.d(TAG, message, throwable)
        }

        fun e(message: String, throwable: Throwable? = null) {
            Log.e(TAG, sanitize(message), throwable?.sanitize())
        }

        private fun sanitize(message: String): String = message
            .replace(Regex("Bearer [\\w.-]+"), "Bearer [REDACTED]")
            .replace(Regex("[\\w.+-]+@[\\w-]+\\.[\\w.]+"), "[EMAIL REDACTED]")
    }
}
```

---

## Pipeline Integration

- **Stage 1 (Requirements):** SRD defines security requirements mapped to MASVS L1 controls; L2 requirements identified for sensitive features.
- **Stage 3 (Architecture):** ADRs specify cryptographic choices, key management strategy, certificate pinning strategy, and network security architecture.
- **Stage 5 (Development):** Primary skill for secure implementation. All data handling, input validation, storage, and networking follow these patterns. Security is built in, not bolted on.
- **Stage 6 (Code Review):** Security review: input validation completeness, storage encryption, certificate pinning configuration, manifest security settings, R8 rule completeness, credential handling.
- **Stage 8 (Integrity Verification):** CSO validates MASVS L1 (all production releases) and applicable L2 (sensitive features). Root detection, tamper checks, and data protection validated. All security controls from SRD verified against implementation.

## Quality Standards

- **100%** OWASP MASVS L1 controls implemented and verified for all production releases
- **Zero** cleartext HTTP traffic (enforced by Network Security Config)
- **Zero** hardcoded secrets, API keys, or tokens in source code or resources
- **100%** sensitive user data encrypted at rest using EncryptedSharedPreferences or Android Keystore-backed keys
- **Zero** sensitive data in application logs (verified via automated log scanning in CI)
- **100%** release builds use R8 obfuscation with verified keep rules
- **100%** user input validated before processing — no raw input passed to database or network
- `android:allowBackup="false"` and `android:fullBackupContent="false"` set in manifest
- `debuggable=false` in all release builds
- Deep links validated against allowlist — no open redirects
- Screenshot protection (FLAG_SECURE) on all screens displaying payment or PII data
- Certificate pinning with backup pins on all production API endpoints; pin rotation tested
- Root/jailbreak detection implemented with graceful degradation (not hard crash)
- All cryptographic operations use hardware-backed Keystore (StrongBox) when available
- Security code review completed by CSO before Stage 8 sign-off
