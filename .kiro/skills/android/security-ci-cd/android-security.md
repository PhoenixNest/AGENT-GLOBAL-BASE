---
name: android-security
description: This skill implements OWASP Mobile Application Security Verification Standard (MASVS) compliance on Android, covering Keystore integration, secure networking, data protection.
---

# Android Security

**Category:** Mobile Engineering — Android Security
**Owner:** Senior Android Engineer (Priya Narayanan)

## Overview

This skill implements OWASP Mobile Application Security Verification Standard (MASVS) compliance on Android, covering Keystore integration, secure networking, data protection, and code obfuscation with ProGuard/R8. It applies to Stage 5 (Development) for secure implementation, Stage 6 (Code Review) for security audit, and Stage 8 (Integrity Verification) where CSO validates SRD compliance against the MASVS baseline.

## Competency Dimensions

| Dimension                           | Description                                                                                               | Proficiency Indicators                                                                                                                                      |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OWASP MASVS Compliance              | Understanding of MASVS V1-V8 control families, L1 vs L2 certification levels, and verification procedures | Maps every security requirement from SRD to specific MASVS control IDs; achieves L1 baseline for all production releases; documents verification evidence   |
| Android Keystore & Cryptography     | Key generation, hardware-backed storage, key attestation, encryption/decryption lifecycle                 | Uses Android Keystore for all cryptographic keys; implements key rotation; handles key invalidation gracefully (BIOMETRIC_ERROR, device lock screen change) |
| Secure Networking                   | TLS configuration, certificate pinning, network security configuration, MITM protection                   | Implements certificate pinning with backup pins; Network Security Config disables cleartext; OkHttp configured with modern TLS 1.2+ cipher suites           |
| Data Protection                     | EncryptedSharedPreferences, SQLCipher, secure file storage, clipboard/data leakage prevention             | All PII encrypted at rest; no sensitive data in logs, clipboard, or recent tasks; secure file deletion with overwrite                                       |
| Code Obfuscation & Tamper Detection | R8/ProGuard rules, integrity checks, root/jailbreak detection, debugger detection                         | R8 shrinking removes 40%+ unused code; anti-tampering checks trigger graceful degradation; debuggable=false in release builds                               |

## Execution Guidance

### OWASP MASVS Mapping to Android Implementation

**SRD → MASVS Control → Android Implementation traceability:**

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

### Android Keystore — Production Implementation

**Key generation with hardware backing and attestation:**

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
```

### Secure Networking — Certificate Pinning

```kotlin
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
```

### R8/ProGuard — Production Rules

**Critical keep rules for reflection-based libraries:**

```proguard
# app/proguard-rules.pro

# Keep domain models (used by serialization)
-keep class com.example.domain.model.** { *; }
-keepclassmembers class com.example.domain.model.** {
    <fields>;
}

# Keep Room entities and DAOs
-keep class com.example.data.local.entity.** { *; }
-keep class com.example.data.local.dao.** { *; }
-keep class * extends androidx.room.RoomDatabase

# Keep Hilt generated classes
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep class * extends dagger.hilt.android.internal.managers.ViewComponentManager { *; }

# Keep Kotlin coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembers class kotlinx.coroutines.** {
    volatile <fields>;
}

# Obfuscate everything else
-allowaccessmodification
-optimizations !code/simplification/arithmetic,!code/allocation/variable
-optimizationpasses 5
-dontusemixedcaseclassnames
```

**Verify R8 output:**

```bash
# Analyze APK after build
./gradlew :app:analyzeReleaseBundle

# Check method count reduction
apkanalyzer apk summary app-release.apk

# Verify sensitive classes are obfuscated
apkanalyzer apk classes app-release.apk | grep -i "password\|token\|secret"
# Should return zero results
```

### Data Leakage Prevention

**Clipboard, Recents, and Screenshot protection:**

```kotlin
class SecurityWindowManager(private val window: Window) {

    fun preventScreenshots() {
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }

    fun preventRecentsSnapshot() {
        // In Activity.onCreate():
        // this.setRecentsScreenshotEnabled(false)  // API 33+
    }

    fun clearClipboardOnBackground() {
        // Register LifecycleObserver to clear clipboard when app backgrounds
    }
}

// Prevent sensitive data in logs
@Suppress("PrintStackTrace")
class SecureLogger {
    companion object {
        private const val TAG = "App"
        private const val IS_DEBUG = BuildConfig.DEBUG

        fun d(message: String, throwable: Throwable? = null) {
            if (IS_DEBUG) {
                Log.d(TAG, message, throwable)
            }
        }

        fun e(message: String, throwable: Throwable? = null) {
            // Always log errors but sanitize PII
            Log.e(TAG, sanitize(message), throwable?.sanitize())
        }

        private fun sanitize(message: String): String {
            // Remove tokens, emails, phone numbers from log messages
            return message
                .replace(Regex("Bearer [\\w.-]+"), "Bearer [REDACTED]")
                .replace(Regex("[\\w.+-]+@[\\w-]+\\.[\\w.]+"), "[EMAIL REDACTED]")
        }
    }
}
```

## Pipeline Integration

- **Stage 1 (Requirements):** SRD defines security requirements mapped to MASVS controls. This skill implements those controls.
- **Stage 3 (Architecture):** ADRs specify cryptographic choices, key management strategy, and network security architecture.
- **Stage 5 (Development):** Secure implementation of all data handling, networking, and storage. Security is built in, not bolted on.
- **Stage 6 (Code Review):** Security-focused code review: credential handling, encryption correctness, certificate pinning configuration, R8 rule completeness.
- **Stage 8 (Integrity Verification):** CSO validates MASVS compliance. All security controls from SRD are verified against implementation. Root detection, tamper checks, and data protection validated.

## Quality Standards

- **100%** OWASP MASVS L1 controls implemented and verified
- **Zero** cleartext HTTP traffic (enforced by Network Security Config)
- **Zero** hardcoded secrets, API keys, or tokens in source code or resources
- **100%** sensitive user data encrypted at rest using Android Keystore-backed keys
- **Zero** sensitive data in application logs (verified via automated log scanning in CI)
- **100%** release builds use R8 obfuscation with verified keep rules
- Certificate pinning deployed for all production API endpoints with backup pins
- Root/jailbreak detection implemented with graceful degradation (not hard crash)
- All cryptographic operations use hardware-backed Keystore when available (StrongBox)
- Security code review completed by CSO before Stage 8 sign-off
