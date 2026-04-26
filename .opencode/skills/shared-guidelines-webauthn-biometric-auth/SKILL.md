---
name: shared-guidelines-webauthn-biometric-auth
description: "WebAuthn standard implementation, biometric authentication integration, and passkey management for mobile and web applications — covering WebAuthn registration and authentication flows, Android BiometricPrompt + Keystore integration, iOS LocalAuthentication framework, passkey cryptography and phishing resistance, and security considerations (cryptographic challenges, rate limiting, accessibility fallbacks). Use during Stage 5 (Development) for secure authentication features and Stage 6 (Code Review) for security conformance. Trigger: WebAuthn, biometric authentication, passkey, Face ID, Touch ID, BiometricPrompt, LocalAuthentication, fingerprint auth, face auth, passkey integration, secure authentication."
prerequisites:
  - shared-overview

version: "1.0.0"
---

# WebAuthn & Biometric Authentication

## Overview

This skill covers WebAuthn standard implementation, biometric authentication integration, and passkey management for mobile and web applications. It is used by full-stack engineers during Stage 5 (Development) for secure authentication features and Stage 6 (Code Review) for security conformance.

## WebAuthn Fundamentals

**WebAuthn registration flow**:

1. Client requests registration challenge from server.
2. Server generates cryptographic challenge (random bytes, 32+ bytes).
3. Client calls `navigator.credentials.create()` with public key options.
4. Authenticator generates key pair.
5. Client sends attestation object to server.
6. Server verifies attestation, stores credential ID and public key.

**WebAuthn authentication flow**:

1. Client requests authentication challenge from server.
2. Server generates challenge, looks up allowed credentials for user.
3. Client calls `navigator.credentials.get()` with allowed credentials.
4. Authenticator signs challenge with private key (user verification: fingerprint, face, PIN).
5. Client sends assertion to server.
6. Server verifies signature using stored public key.

## Biometric Authentication on Mobile

**Android (BiometricPrompt + Keystore)**:

```kotlin
val biometricPrompt = BiometricPrompt(activity, executor, callback)
val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authenticate")
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .build()
biometricPrompt.authenticate(promptInfo)
```

**iOS (LocalAuthentication framework)**:

```swift
let context = LAContext()
if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
    context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
                          localizedReason: "Authenticate to continue") { success, error in }
}
```

## Passkey Integration

- Passkeys use public-key cryptography — no shared secret, no server-side password storage.
- Phishing-resistant: credentials bound to relying party origin (domain/app association).
- Sync-enabled: passkeys sync via iCloud Keychain or Google Password Manager.

## Security Considerations

- Challenge must be cryptographically random and single-use.
- Timeout: authentication attempts expire after 5 minutes.
- Rate limiting: maximum 5 failed attempts per 15-minute window.
- Backup authentication: always provide fallback (password, OTP, or support contact).
- Accessibility: biometric authentication must have non-biometric fallback.
