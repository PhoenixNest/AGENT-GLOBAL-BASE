---
name: mobile-threat-modeling
description: Produce STRIDE-based threat models specifically for mobile applications — Android and iOS — covering client-side, API communication, and backend trust boundaries, with output structured for Stage 3 UML Engineering Package inclusion.
version: "1.0.0"
---

# Mobile Threat Modeling

| Competency              | Description                                                         | Quality Criteria                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------------- | -------- | ------------- | ---------- | ------ |
| Mobile DFD Construction | Data Flow Diagram for mobile apps across client, API, and backend   | DFD covers all actors (user, device OS, backend), data stores (local DB, keychain), and trust boundaries (device, network, server) |
| STRIDE for Mobile       | Applying STRIDE categories to mobile-specific attack surfaces       | Each DFD element has a STRIDE analysis; findings include threat ID, affected component, attack vector, and mitigation control      |
| Trust Boundary Analysis | Identifying and documenting trust boundary crossings in mobile apps | All client→API, client→OS, and inter-process communication crossings are enumerated; each has a documented verification mechanism  |
| Risk Register           | Structured risk register linking threats to MASVS controls          | Risk register follows: Threat ID                                                                                                   | Description | STRIDE Category | Severity | MASVS Control | Mitigation | Status |

## Execution Guidance

### Mobile Data Flow Diagram Elements

A mobile app DFD must enumerate:

- **External entities:** End user, push notification service (APNs/FCM), third-party SDKs (analytics, ads)
- **Processes:** App business logic, authentication module, local encryption layer, background sync worker
- **Data stores:** Keychain/Keystore, local SQLite database, SharedPreferences, device file system
- **Data flows:** User input → app, app → API (HTTPS), API response → local cache, background sync → server

### STRIDE Mobile Threat Catalog

| Threat Category        | Mobile Example                                                 | Mitigation Control                            |
| ---------------------- | -------------------------------------------------------------- | --------------------------------------------- |
| Spoofing               | Repackaged app with modified signing certificate               | Certificate pinning + APK signing validation  |
| Tampering              | Hooking biometric API with Frida to bypass authentication      | Anti-tampering + integrity checks at runtime  |
| Repudiation            | No audit trail for in-app purchase transactions                | Server-side transaction logging + receipts    |
| Information Disclosure | Sensitive data in Android logcat in release builds             | ProGuard + logging stripped in release builds |
| Denial of Service      | Flooding push notification endpoint to drain device battery    | Server-side rate limiting per device token    |
| Elevation of Privilege | Exploiting exported ContentProvider to access other apps' data | Remove export; enforce `android:permission`   |

### Stage 3 Deliverable

The threat model must be attached to the Stage 3 UML Engineering Package as a security annex with:

1. Complete DFD (Level 0 and Level 1)
2. STRIDE threat table for all trust boundary crossings
3. Risk register with severity ratings (Critical/High/Medium/Low)
4. Recommended ADR entries for each Critical/High threat
