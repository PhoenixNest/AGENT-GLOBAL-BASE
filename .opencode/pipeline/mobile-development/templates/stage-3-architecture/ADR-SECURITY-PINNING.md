# ADR-NNN: Certificate Pinning Strategy

| Metadata          | Value                                          |
| ----------------- | ---------------------------------------------- |
| **ADR Number**    | ADR-NNN                                        |
| **Title**         | Certificate Pinning Strategy                   |
| **Status**        | Proposed                                       |
| **Decision Date** | YYYY-MM-DD                                     |
| **Authors**       | Security Architect (Natalia Petrova)           |
| **Reviewers**     | CSO (Dr. Sarah Chen), CTO (Dr. Kenji Nakamura) |
| **Stage**         | 3 — Architecture                               |
| **Category**      | Security / Network                             |

---

## Context

Standard TLS certificate validation trusts any certificate signed by a trusted Certificate Authority (CA). However, CAs have been compromised in the past, and any trusted CA can issue a certificate for our domain. Without certificate pinning, an attacker with a fraudulently issued CA-signed certificate can perform a man-in-the-middle (MITM) attack, intercepting and modifying all network traffic between the app and our servers.

---

## Decision

### Pinning Mechanism

| Platform | Mechanism                | Notes                                                                    |
| -------- | ------------------------ | ------------------------------------------------------------------------ |
| iOS      | TrustKit                 | Open-source, actively maintained, supports report-only and enforce modes |
| Android  | OkHttp CertificatePinner | Built into OkHttp, SHA-256 pin hashes                                    |
| KMP      | Platform adapter         | Shared module delegates to platform-specific pinning                     |
| Flutter  | Platform channel         | Native pinning via platform channels; do not implement in Dart           |

### Pin Targets

| Pin Type    | Target                                       | Hash Algorithm | Purpose                               |
| ----------- | -------------------------------------------- | -------------- | ------------------------------------- |
| **Primary** | Leaf certificate public key                  | SHA-256        | Main pin for production certificate   |
| **Backup**  | Backup certificate public key (different CA) | SHA-256        | Fallback if primary CA is compromised |

**Critical:** The backup pin MUST use a certificate from a **different CA** than the primary. Using the same CA for both pins defeats the purpose — a single CA compromise would invalidate both pins.

### Pin Update Frequency

| Pin Type | Rotation Schedule                                       | Notes                             |
| -------- | ------------------------------------------------------- | --------------------------------- |
| Primary  | Every certificate rotation (maximum 12 months)          | Align with cert renewal cycle     |
| Backup   | Rotated independently from primary (staggered schedule) | Never rotate both simultaneously  |
| Overlap  | Minimum 30 days between old and new pin deployment      | Allows for app update propagation |

### Fallback Mechanism

| Mechanism                 | Detail                                                           |
| ------------------------- | ---------------------------------------------------------------- |
| Remote config             | Firebase Remote Config or server-hosted pin configuration        |
| Startup behavior          | App fetches latest pin config before making API calls            |
| Emergency updates         | Pin updates possible without app store release via remote config |
| Remote config unreachable | Fall back to bundled pins with warning logged to analytics       |
| Both unreachable          | Block all network requests — fail closed, not open               |

### Report-Only Mode

| Phase          | Duration                                        | Behavior                                                                  |
| -------------- | ----------------------------------------------- | ------------------------------------------------------------------------- |
| Report-only    | 2 weeks                                         | Pins validated but connections NOT blocked on mismatch; mismatches logged |
| Enforcement    | After 2 weeks with zero false positives         | Connections blocked on pin mismatch                                       |
| False positive | If any pin mismatch detected during report-only | Immediate investigation, resolve before switching to enforce              |

### Pin Validation Strictness

- **Full certificate chain validation** — not just leaf certificate
- **Reject on ANY pin mismatch** — no soft failures, no user override
- **Pin validation before data transmission** — validate during TLS handshake, not after
- **No user bypass** — users cannot override pin validation errors

---

## Network Security Configuration

### iOS (TrustKit)

Configure in `Info.plist` under `TSKConfiguration`:

```xml
<key>TSKConfiguration</key>
<dict>
    <key>TSKPinningValidatorPublicKeyHashes</key>
    <array>
        <string>sha256/PRIMARY_PIN_HASH=</string>
        <string>sha256/BACKUP_PIN_HASH=</string>
    </array>
    <key>TSKEnforcePinning</key>
    <true/> <!-- false during report-only, true for enforce -->
    <key>TSKIncludeSubdomains</key>
    <true/>
</dict>
```

### Android (OkHttp)

Configure via `OkHttpClient.Builder`:

```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/PRIMARY_PIN_HASH=")
    .add("api.example.com", "sha256/BACKUP_PIN_HASH=")
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

Also configure `res/xml/network_security_config.xml` for defense-in-depth.

### KMP/Flutter

| Platform | Approach                                                                                          |
| -------- | ------------------------------------------------------------------------------------------------- |
| KMP      | Shared module defines `PinningConfig` interface; platform adapters implement with TrustKit/OkHttp |
| Flutter  | Platform channel to native pinning implementation; never implement pin validation in Dart code    |

---

## Emergency Pin Rotation Procedure

| Step | Action                                                                        | Timeline                  |
| ---- | ----------------------------------------------------------------------------- | ------------------------- |
| 1    | New certificate provisioned on server                                         | T-30 days before rotation |
| 2    | Remote config updated with new pin hash                                       | T-30 days                 |
| 3    | Apps download updated config on next startup                                  | T-30 to T-1 days          |
| 4    | Pins validated on subsequent connections                                      | Ongoing                   |
| 5    | Server switches to new certificate                                            | T-0 (rotation day)        |
| 6    | Old pins removed from remote config                                           | T+7 days                  |
| 7    | If remote config unreachable: emergency app release with updated bundled pins | As needed                 |

---

## STRIDE Threat Reference

| STRIDE Category            | Threat                                                     | Mitigation                                    |
| -------------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| **Spoofing**               | Attacker with forged certificate (MITM)                    | Dual-pin requirement, full chain validation   |
| **Tampering**              | CA compromise issuing valid-but-unauthorized certificates  | Backup pin from different CA                  |
| **Information Disclosure** | Intercepted traffic due to missing pin validation          | Enforce mode after report-only period         |
| **Denial of Service**      | Pins expire without rotation, blocking all network traffic | Remote config fallback, 30-day overlap window |

---

## MASVS Compliance

| MASVS ID        | Requirement                                                          | Compliance Evidence                             |
| --------------- | -------------------------------------------------------------------- | ----------------------------------------------- |
| MASVS-NETWORK-1 | App configures TLS to accept only trusted certificates               | Network security config, ATS settings           |
| MASVS-NETWORK-2 | App validates TLS certificate chain and performs certificate pinning | This ADR, pin configuration, CI/CD verification |

---

## Alternatives Considered

| Alternative                     | Why Rejected                                                           |
| ------------------------------- | ---------------------------------------------------------------------- |
| No pinning (CA validation only) | CA compromise risk — multiple CAs have been compromised historically   |
| HPKP (HTTP Public Key Pinning)  | Deprecated by IETF RFC 7469; not supported by mobile browsers          |
| Full CA whitelist               | Too restrictive — limits server flexibility, high maintenance overhead |
| Certificate Transparency only   | Useful defense-in-depth but does not prevent real-time MITM            |

---

## Compliance

**This decision is locked at Stage 3 gate approval.** Any deviation requires a new ADR and Stage 3 re-entry with CSO approval.

| Enforcement Layer | Mechanism                                                        |
| ----------------- | ---------------------------------------------------------------- |
| Policy            | Stage 3 ADR lock                                                 |
| Runtime           | Pin validation enforced at TLS handshake                         |
| CI/CD             | Pin configuration included in build verification                 |
| Code Review       | Security team reviews pin configuration during Stage 6           |
| Stage 8 Integrity | Anti-trim verification includes pinning presence and correctness |

**Non-compliance classification:** Absence of certificate pinning is a **P1 defect** (core security feature missing). Pinning with a single pin (no backup) is a **P2 defect**. Pinning with backup from same CA is a **P1 defect**.
