---
version: "1.0.0"
---

# Android Security Basics

| Competency          | Description                                                                                            | Quality Criteria                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| OWASP MASVS L1      | Understanding of baseline MASVS controls, storage, cryptography, authentication, network communication | All MASVS L1 controls implemented; security requirements from SRD mapped to specific controls; zero critical findings in security audit |
| Secure Storage      | EncryptedSharedPreferences, Android Keystore, internal storage, external storage restrictions          | All sensitive data stored encrypted; no sensitive data in SharedPreferences plaintext; file permissions restricted to app-only          |
| Certificate Pinning | OkHttp CertificatePinner, pin rotation strategy, backup pins, pin expiry management                    | Certificate pinning deployed for production endpoints; backup pins prevent lockout; pin rotation tested                                 |
| Input Validation    | Whitelist validation, sanitization, SQL injection prevention, XSS prevention in WebViews               | All user input validated before processing; parameterized queries exclusively; WebView JavaScript disabled unless required              |
| Security Hygiene    | Debug flags, log sanitization, screenshot protection, intent security, deep link validation            | `debuggable=false` in release; no sensitive data in logs; FLAG_SECURE on sensitive screens; deep links validated against allowlist      |

## Execution Guidance

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
| V5-1          | No sensitive data in logs                  | Proguard logging removal in release                            | Logcat inspection                  |
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
```

**Internal storage for files — never external storage for sensitive data:**

```kotlin
class SecureFileManager(private val context: Context) {

    // Internal storage — only accessible by this app
    fun saveSensitiveFile(fileName: String, data: ByteArray) {
        context.openFileOutput(fileName, Context.MODE_PRIVATE).use { outputStream ->
            outputStream.write(data)
        }
    }

    fun readSensitiveFile(fileName: String): ByteArray {
        return context.openFileInput(fileName).use { inputStream ->
            inputStream.readBytes()
        }
    }

    fun deleteSensitiveFile(fileName: String) {
        // Secure delete — overwrite before deletion
        val file = File(context.filesDir, fileName)
        if (file.exists()) {
            // Overwrite with random data
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
    // getExternalFilesDir() is acceptable for non-sensitive cached data
    fun saveNonSensitiveCache(fileName: String, data: ByteArray) {
        val cacheDir = context.getExternalFilesDir(null)
        File(cacheDir, fileName).writeBytes(data)
    }
}
```

### Certificate Pinning — Implementation

```kotlin
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
```

### Input Validation — Defense in Depth

```kotlin
object InputValidator {

    // Email validation — RFC 5322 simplified
    private val EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    )

    // Name validation — Unicode letters, spaces, hyphens, apostrophes
    private val NAME_PATTERN = Pattern.compile("^[\\p{L}\\s\\-']{1,100}$")

    // Username validation — alphanumeric, underscores, 3-20 chars
    private val USERNAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_]{3,20}$")

    fun validateEmail(email: String): Result<String> {
        return when {
            email.isBlank() -> Result.failure(ValidationError("Email is required"))
            !EMAIL_PATTERN.matcher(email).matches() ->
                Result.failure(ValidationError("Invalid email format"))
            else -> Result.success(email.trim().lowercase())
        }
    }

    fun validateName(name: String): Result<String> {
        return when {
            name.isBlank() -> Result.failure(ValidationError("Name is required"))
            !NAME_PATTERN.matcher(name).matches() ->
                Result.failure(ValidationError("Name contains invalid characters"))
            else -> Result.success(name.trim())
        }
    }

    fun validateUsername(username: String): Result<String> {
        return when {
            username.isBlank() -> Result.failure(ValidationError("Username is required"))
            !USERNAME_PATTERN.matcher(username).matches() ->
                Result.failure(ValidationError("Username must be 3-20 alphanumeric characters or underscores"))
            else -> Result.success(username.trim().lowercase())
        }
    }

    // Sanitize HTML to prevent XSS in WebViews
    fun sanitizeHtml(input: String): String {
        return input
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#x27;")
    }

    // Validate URL for deep links — prevent open redirect
    private val ALLOWED_SCHEMES = setOf("https")
    private val ALLOWED_HOSTS = setOf("example.com", "www.example.com")

    fun validateDeepLink(uri: Uri): Result<Uri> {
        return when {
            uri.scheme !in ALLOWED_SCHEMES ->
                Result.failure(ValidationError("Invalid scheme: ${uri.scheme}"))
            uri.host !in ALLOWED_HOSTS ->
                Result.failure(ValidationError("Untrusted host: ${uri.host}"))
            else -> Result.success(uri)
        }
    }
}

// Sealed error type
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

        <!-- Prevent screenshot on sensitive screens -->
        <activity
            android:name=".ui.payment.PaymentActivity"
            android:windowSoftInputMode="adjustResize">
            <!-- FLAG_SECURE set programmatically in onCreate -->
        </activity>

        <!-- Deep link validation -->
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
    <!-- Block all cleartext traffic by default -->
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

**Screenshot protection for sensitive screens:**

```kotlin
class SecurityActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Prevent screenshots and screen recording
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )

        setContentView(R.layout.activity_payment)
    }

    override fun onPause() {
        super.onPause()
        // Clear sensitive data from clipboard
        val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.clearPrimaryClip()
    }
}
```

**ProGuard/R8 — Remove logging in release:**

```proguard
# Remove all Log.d and Log.v calls in release builds
-assumenosideeffects class android.util.Log {
    public static int d(...);
    public static int v(...);
    public static java.lang.String getStackTraceString(java.lang.Throwable);
}
```

## Pipeline Integration

- **Stage 1 (Requirements):** SRD defines security requirements mapped to MASVS L1 controls.
- **Stage 3 (Architecture):** ADRs specify cryptographic choices, certificate pinning strategy, and storage architecture.
- **Stage 5 (Development):** Primary skill for secure implementation. All data handling, input validation, and storage follow these patterns.
- **Stage 6 (Code Review):** Security review: input validation completeness, storage encryption, certificate pinning configuration, manifest security settings.
- **Stage 8 (Integrity Verification):** CSO validates MASVS L1 compliance. All security controls from SRD verified against implementation.

## Quality Standards

- **100%** OWASP MASVS L1 controls implemented and verified
- **Zero** cleartext HTTP traffic (enforced by Network Security Config)
- **Zero** hardcoded secrets in source code, resources, or build files
- **100%** sensitive data encrypted at rest using EncryptedSharedPreferences or Android Keystore
- **Zero** sensitive data in application logs (verified via automated log scanning)
- Certificate pinning deployed for all production API endpoints with backup pins
- **100%** user input validated before processing — no raw input passed to database or network
- `android:allowBackup="false"` and `android:fullBackupContent="false"` set in manifest
- `debuggable=false` in all release builds
- Deep links validated against allowlist — no open redirects
- Screenshot protection (FLAG_SECURE) on all screens displaying payment or PII data
