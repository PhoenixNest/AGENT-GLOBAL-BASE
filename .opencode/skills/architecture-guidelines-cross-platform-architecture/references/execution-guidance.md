# Execution Guidance

## Execution Guidance

### 1. Mobile Architecture Pattern Selection

#### 1.1 Pattern Comparison Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ MOBILE ARCHITECTURE PATTERN COMPARISON                                               │
├────────────────────┬──────────┬──────────────┬──────────┬────────────┬──────────────┤
│ Criterion          │ Native   │ KMP Shared   │ Flutter  │ React      │ PWA          │
│                    │ (Swift/  │ Core         │          │ Native     │              │
│                    │ Kotlin)  │ + Native UI  │          │            │              │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Performance        │ ★★★★★    │ ★★★★☆        │ ★★★★☆    │ ★★★☆☆      │ ★★☆☆☆       │
│ (60fps, native     │          │              │          │            │              │
│  animations)       │          │              │          │            │              │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Platform API       │ ★★★★★    │ ★★★★☆        │ ★★★☆☆    │ ★★★☆☆      │ ★☆☆☆☆       │
│ Access (camera,    │          │ (via         │ (plugins │ (bridges   │ (limited to  │
│ sensors, biometric)│          │ expect/       │ available │ to native  │ browser APIs)│
│                    │          │ actual)       │ but       │ modules)   │              │
│                    │          │              │ third-    │            │              │
│                    │          │              │ party)    │            │              │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Dev Velocity       │ ★★☆☆☆    │ ★★★★☆        │ ★★★★☆    │ ★★★★☆      │ ★★★★★       │
│ (single codebase,  │ (2x code)│ (shared      │ (single   │ (single    │ (single     │
│  hot reload)       │          │ logic,       │ codebase, │ codebase,  │ codebase,   │
│                    │          │ native UI)   │ hot       │ fast       │ instant     │
│                    │          │              │ reload)   │ refresh)   │ deploy)     │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Code Sharing       │ 0%       │ 60-80%       │ 90-95%   │ 70-85%     │ 100%        │
│ (business logic +  │          │              │          │            │             │
│  UI)               │          │              │          │            │             │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Hiring Market      │ ★★★★★    │ ★★★☆☆        │ ★★★★☆    │ ★★★★★      │ ★★★★☆      │
│ (available talent) │          │ (growing)    │          │            │             │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ App Store          │ ★★★★★    │ ★★★★★        │ ★★★★☆    │ ★★★★☆      │ N/A         │
│ Compliance         │          │ (native      │ (minor    │ (minor     │ (no store   │
│                    │          │ binaries)     │ review    │ review     │ submission) │
│                    │          │              │ friction) │ friction)  │             │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ Offline-First      │ ★★★★★    │ ★★★★☆        │ ★★★☆☆    │ ★★★☆☆      │ ★★☆☆☆       │
│ (local DB, sync)   │ (SQLite, │ (SQLDelight, │ (SQLite  │ (SQLite    │ (IndexedDB  │
│                    │ CoreData)│ Room)        │ via       │ via        │ limited     │
│                    │          │              │ plugins)  │ plugins)   │ capacity)   │
├────────────────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┤
│ WHEN TO CHOOSE     │ Best     │ Best when    │ Best      │ Best when  │ Best for    │
│                    │ UX/      │ team has     │ for       │ team has   │ internal    │
│                    │ perf     │ strong       │ startup   │ strong web │ tools,      │
│                    │ critical │ Android +    │ speed     │ team;      │ marketing   │
│                    │          │ iOS expertise│ + good    │ large JS   │ sites,      │
│                    │          │              │ UX needed │ ecosystem  │ progressive │
│                    │          │              │           │            │ enhancement │
└────────────────────┴──────────┴──────────────┴──────────┴────────────┴──────────────┘
```

#### 1.2 Decision Rules

```
PATTERN SELECTION DECISION TREE:

  Does the product require platform-specific hardware access?
  (LiDAR, ARKit, CoreML on-device, Android NNAPI)
  ├── YES → NATIVE or KMP Shared Core + Native UI
  │    └── If team has both Android + iOS expertise → KMP
  │    └── If team is single-platform → NATIVE (accept 2x code)
  └── NO
       │
       Is 60fps UI with complex animations a core requirement?
       ├── YES → NATIVE or FLUTTER
       │    └── If custom painting/animations dominate → FLUTTER
       │    └── If platform-native look/feel dominates → NATIVE or KMP
       └── NO
            │
            Is the team primarily web/JavaScript developers?
            ├── YES → REACT NATIVE
            │    └── If web team can learn Dart → FLUTTER (better perf)
            └── NO
                 │
                 Is time-to-market the primary constraint (< 3 months)?
                 ├── YES → FLUTTER or REACT NATIVE
                 └── NO
                      │
                      DEFAULT → KMP SHARED CORE + NATIVE UI
                      (best long-term maintainability for mobile products)
```

### 2. Platform Layering Strategy

#### 2.1 KMP Shared Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│ KMP SHARED CORE — LAYERED ARCHITECTURE                                  │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  iOS App (Swift)                    Android App (Kotlin)          │  │
│  │  ┌─────────────┐                    ┌─────────────┐               │  │
│  │  │ UI Layer    │                    │ UI Layer    │               │  │
│  │  │ (SwiftUI/   │                    │ (Jetpack    │               │  │
│  │  │  UIKit)     │                    │  Compose)   │               │  │
│  │  └──────┬──────┘                    └──────┬──────┘               │  │
│  │         │ expect interfaces                │ expect interfaces    │  │
│  └─────────┼──────────────────────────────────┼──────────────────────┘  │
│            │                                  │                         │
│  ┌─────────▼──────────────────────────────────▼──────────────────────┐  │
│  │  shared/ (Kotlin Multiplatform)                                   │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │  Presentation Layer (ViewModel, State, UseCases)            │  │  │
│  │  │  — Platform-agnostic UI state and business orchestration    │  │  │
│  │  └────────────────────────┬────────────────────────────────────┘  │  │
│  │                           │                                       │  │
│  │  ┌────────────────────────▼────────────────────────────────────┐  │  │
│  │  │  Domain Layer (Entities, UseCases, Repository Interfaces)   │  │  │
│  │  │  — Pure Kotlin, zero platform dependencies                 │  │  │
│  │  └────────────────────────┬────────────────────────────────────┘  │  │
│  │                           │                                       │  │
│  │  ┌────────────────────────▼────────────────────────────────────┐  │  │
│  │  │  Data Layer (Repository Implementations, Data Sources)      │  │  │
│  │  │  — Ktor (HTTP), SQLDelight (DB), Koin (DI)                 │  │  │
│  │  └────────────────────────┬────────────────────────────────────┘  │  │
│  │                           │                                       │  │
│  │  ┌────────────────────────▼────────────────────────────────────┐  │  │
│  │  │  Platform Abstractions (expect/actual)                      │  │  │
│  │  │  — expect interface → actual implementation per platform    │  │  │
│  │  │  — SecureStorage, PlatformInfo, NetworkConnectivity         │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  DEPENDENCY RULE: Inner layers NEVER depend on outer layers.            │
│  Domain → nothing. Data → Domain. Presentation → Domain + Data.         │
│  Platform apps → shared (Presentation layer).                           │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2.2 Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MODULE DEPENDENCY GRAPH (Maximum Depth: 4)                              │
│                                                                         │
│  app-ios / app-android        (Depth 4 — Platform Apps)                │
│       │                                                                 │
│       ▼                                                                 │
│  :feature:<name>              (Depth 3 — Feature Modules)               │
│       │                                                                 │
│       ▼                                                                 │
│  :shared-presentation         (Depth 2 — Shared Presentation)           │
│       │                                                                 │
│       ▼                                                                 │
│  :shared-domain               (Depth 1 — Domain / UseCases)             │
│       │                                                                 │
│       ▼                                                                 │
│  :shared-data                 (Depth 0 — Data / Repositories)           │
│       │                                                                 │
│       ▼                                                                 │
│  :shared-common               (Depth 0 — Models, Extensions, Utils)     │
│                                                                         │
│  RULES:                                                                  │
│  1. No module may depend on a module at a higher depth level            │
│  2. :shared-domain depends ONLY on :shared-common                        │
│  3. :shared-data depends on :shared-domain and :shared-common           │
│  4. :shared-presentation depends on :shared-domain and :shared-data     │
│  5. Feature modules depend on :shared-presentation                       │
│  6. Platform apps depend on feature modules                              │
│  7. Maximum dependency depth = 4 (app → feature → presentation → data)  │
│  8. Violations are CI gate failures (detected by dependency graph tool)  │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2.3 expect/actual Interface Design

```kotlin
// shared/common/src/main/kotlin/platform/SecureStorage.kt
// EXPECT interface — defines contract, no implementation
package com.company.app.platform

expect class SecureStorage {
    fun getString(key: String): String?
    fun setString(key: String, value: String)
    fun delete(key: String)
}

// ANDROID actual implementation
// androidApp/src/main/kotlin/platform/SecureStorage.android.kt
package com.company.app.platform

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

actual class SecureStorage actual constructor(
    private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    actual fun getString(key: String): String? = prefs.getString(key, null)
    actual fun setString(key: String, value: String) {
        prefs.edit().putString(key, value).apply()
    }
    actual fun delete(key: String) {
        prefs.edit().remove(key).apply()
    }
}

// iOS actual implementation
// iosApp/SecureStorage.ios.kt
package com.company.app.platform

import platform.Foundation.NSUserDefaults
import platform.Security.*

actual class SecureStorage {
    // Uses Keychain for sensitive data, NSUserDefaults for non-sensitive
    actual fun getString(key: String): String? {
        val query = mapOf(
            kSecClass to kSecClassGenericPassword,
            kSecAttrAccount to key,
            kSecReturnData to true
        )
        // ... Keychain query implementation
    }

    actual fun setString(key: String, value: String) {
        val data = value.encodeToByteArray()
        val query = mapOf(
            kSecClass to kSecClassGenericPassword,
            kSecAttrAccount to key,
            kSecValueData to data
        )
        // ... Keychain set implementation
    }

    actual fun delete(key: String) {
        val query = mapOf(
            kSecClass to kSecClassGenericPassword,
            kSecAttrAccount to key
        )
        // ... Keychain delete implementation
    }
}
```

### 3. API Design for Mobile Clients

#### 3.1 API Protocol Comparison

| Criterion            | REST                             | GraphQL                                     | gRPC-Web                                   |
| -------------------- | -------------------------------- | ------------------------------------------- | ------------------------------------------ |
| **Over-fetching**    | Common (fixed response shape)    | Eliminated (client requests exact fields)   | None (proto-defined, fixed shape)          |
| **Under-fetching**   | Common (N+1 requests)            | Eliminated (single query, nested resolvers) | Common (multiple RPC calls)                |
| **Caching**          | HTTP cache (CDN-friendly)        | Complex (requires Apollo Cache, normalized) | No HTTP cache (binary protocol)            |
| **Real-time**        | WebSockets (additional infra)    | Subscriptions (WebSocket/SSE)               | Server streaming (limited browser support) |
| **Tooling**          | OpenAPI/Swagger (mature)         | GraphQL Playground, introspection           | Protobuf, codegen (strong typing)          |
| **Mobile Bandwidth** | Moderate (JSON overhead)         | Low (only requested fields)                 | Lowest (binary protobuf)                   |
| **Error Handling**   | HTTP status codes + error body   | 200 OK always, errors in response body      | HTTP status + gRPC status codes            |
| **File Upload**      | Multipart/form-data (mature)     | Complex (multipart + GraphQL spec)          | Not directly supported (base64 overhead)   |
| **Best For**         | Simple CRUD, cacheable resources | Complex nested queries, variable clients    | High-throughput internal services          |

**Recommendation for mobile products:**

```
API PROTOCOL SELECTION:

  Primary client-facing API → GRAPHQL
    Reason: Mobile clients have variable data needs based on screen size,
    network conditions, and feature flags. GraphQL's field-level selection
    eliminates over-fetching on constrained mobile networks.

  File upload/download → REST
    Reason: Multipart uploads, resumable downloads, and CDN integration
    are mature and simple with REST.

  Internal service-to-service → gRPC
    Reason: High throughput, strong typing, code generation. Not exposed
    to mobile clients directly.

  Real-time notifications → WebSocket
    Reason: Persistent connection for push notifications, live updates.
    Mobile clients maintain a single WebSocket connection.
```

#### 3.2 Mobile-Optimized API Design Patterns

```graphql
# GRAPHQL: Pagination with cursor (mobile-friendly)

```

query GetFeed($first: Int!, $after: String, $filter: FeedFilter) {
feed(first: $first, after: $after, filter: $filter) {
edges {
node {
id
title
thumbnailUrl(width: 300, height: 200, quality: 75)
createdAt
author {
name
avatarUrl
}
}
cursor
}
pageInfo {
hasNextPage
endCursor
} # Mobile-specific: total count is EXPENSIVE — omit unless needed # totalCount # ← Do NOT include; requires full table scan
}
}

# DELTA SYNC: Only fetch changes since last sync

query DeltaSync($sinceToken: String!, $entityTypes: [EntityType!]!) {
deltaSync(sinceToken: $sinceToken, entityTypes: $entityTypes) {
newToken
changes {
entityType
entityId
operation # CREATED | UPDATED | DELETED
payload # Full entity for CREATED/UPDATED; null for DELETED
} # Conflict detection: server returns serverVersion for each entity
conflicts {
entityId
clientVersion
serverVersion
serverPayload
}
}
}

# BATCH MUTATION: Multiple operations in single request

mutation BatchUpdate($operations: [BatchOperation!]!) {
batchUpdate(operations: $operations) {
results {
entityId
success
error
} # Single network round-trip for multiple operations # Reduces battery impact vs. individual requests
}
}

````

#### 3.3 Error Response Standard

```json
{
  "errors": [
    {
      "code": "NETWORK_UNSTABLE",
      "message": "Request may not have been processed. Retry with idempotency key.",
      "retryable": true,
      "retryAfterMs": 5000,
      "mobileAction": "SHOW_RETRY_DIALOG"
    },
    {
      "code": "STALE_DATA",
      "message": "Your data is outdated. Pull latest from server.",
      "retryable": true,
      "mobileAction": "BACKGROUND_SYNC"
    },
    {
      "code": "CONFLICT",
      "message": "Another device modified this resource.",
      "retryable": false,
      "mobileAction": "SHOW_CONFLICT_RESOLUTION_UI",
      "conflictDetails": {
        "entityId": "order-123",
        "serverVersion": 5,
        "clientVersion": 3,
        "serverPayload": { "status": "shipped" },
        "clientPayload": { "status": "cancelled" }
      }
    }
  ]
}
````

### 4. Offline-First Architecture

#### 4.1 Local Database Synchronization

```
┌─────────────────────────────────────────────────────────────────────────┐
│ OFFLINE-FIRST SYNC ENGINE ARCHITECTURE                                  │
│                                                                         │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐    │
│  │  Local DB    │◄───────►│  Sync Engine │◄───────►│  Remote API  │    │
│  │  (SQLite/    │  pending│  (queue,     │  delta  │  (GraphQL/   │    │
│  │   Room/      │  ops    │   conflict   │  sync   │   REST)      │    │
│  │   SQLDelight)│         │   resolver)  │         │              │    │
│  └──────┬───────┘         └──────┬───────┘         └──────┬───────┘    │
│         │                        │                        │            │
│         ▼                        ▼                        ▼            │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐    │
│  │  Optimistic  │         │  Conflict    │         │  Server-Side │    │
│  │  UI Updates  │         │  Queue       │         │  Merge       │    │
│  │  (immediate  │         │  (pending    │         │  Logic       │    │
│  │   feedback)  │         │   resolution)│         │  (versioned) │    │
│  └──────────────┘         └──────────────┘         └──────────────┘    │
│                                                                         │
│  SYNC TRIGGERS:                                                         │
│  1. App foreground → immediate sync                                     │
│  2. Network connectivity change → sync after 2s debounce                │
│  3. Background fetch (iOS) / WorkManager (Android) → periodic sync      │
│  4. User-initiated pull-to-refresh → immediate sync                     │
│  5. Push notification (data change) → targeted sync for affected entity │
│                                                                         │
│  SYNC STRATEGY:                                                         │
│  - Outgoing mutations: queued locally, sent in order, retried on fail   │
│  - Incoming changes: delta sync using sync_token (last known state)     │
│  - Conflicts: detected by version mismatch; resolved per entity policy  │
│  - Sync is bidirectional and idempotent (safe to repeat)                │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 4.2 Conflict Resolution Strategies

| Strategy                                      | Description                                                     | Use When                                            | Complexity             |
| --------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------- | ---------------------- |
| **Last-Write-Wins (LWW)**                     | Server timestamp determines winner; loser's change is discarded | Non-critical data (preferences, drafts, read state) | Low                    |
| **Field-Level Merge**                         | Each field is independently merged; conflicting fields use LWW  | User profiles, settings with independent fields     | Medium                 |
| **Operational Transform (OT)**                | Transform operations to achieve convergence                     | Collaborative editing (docs, whiteboards)           | High                   |
| **CRDT (Conflict-free Replicated Data Type)** | Mathematically guaranteed convergence without coordination      | Real-time collaboration, shared state               | High                   |
| **Manual Resolution**                         | Present both versions to user; user chooses                     | Financial data, order modifications, critical state | Medium (UX complexity) |

```kotlin
// Conflict Resolution Implementation (KMP shared)
sealed class ConflictResolution {
    object ServerWins : ConflictResolution()
    object ClientWins : ConflictResolution()
    data class FieldMerge(val mergedFields: Map<String, Any?>) : ConflictResolution()
    data class ManualResolution(val serverVersion: Any, val clientVersion: Any) : ConflictResolution()
}

fun resolveConflict(
    entityType: String,
    entityId: String,
    serverPayload: Map<String, Any?>,
    clientPayload: Map<String, Any?>,
    serverVersion: Long,
    clientVersion: Long
): ConflictResolution {
    return when (entityType) {
        "user_preferences" -> {
            // Field-level merge: each preference is independent
            val merged = serverPayload.toMutableMap()
            clientPayload.forEach { (key, value) ->
                if (merged[key] != value) {
                    // Different values — use client version (user's device is source of truth)
                    merged[key] = value
                }
            }
            ConflictResolution.FieldMerge(merged)
        }
        "order" -> {
            // Critical data — manual resolution required
            ConflictResolution.ManualResolution(serverPayload, clientPayload)
        }
        "draft_post" -> {
            // Non-critical — client wins (user is editing on their device)
            ConflictResolution.ClientWins
        }
        "read_receipt" -> {
            // Server wins (server has authoritative view of all devices)
            ConflictResolution.ServerWins
        }
        else -> ConflictResolution.ServerWins
    }
}
```

#### 4.3 CRDT Primer for Mobile

```
CRDT TYPES FOR MOBILE USE CASES:

  G-Counter (Grow-only Counter):
    - Use: Analytics events, view counts, "likes" (only increment)
    - Merge: max(local, remote) per replica
    - Mobile: Each device is a replica; server sums all replicas

  PN-Counter (Positive-Negative Counter):
    - Use: Inventory adjustments, point balances (increment + decrement)
    - Merge: merge P-counter and N-counter separately
    - Mobile: Track increments and decrements per device

  LWW-Register (Last-Writer-Wins Register):
    - Use: User profile fields, settings
    - Merge: highest timestamp wins
    - Mobile: Simple; use wall-clock time with logical clock fallback

  OR-Set (Observed-Remove Set):
    - Use: Tags, labels, group memberships
    - Merge: union of adds, remove only if add was observed
    - Mobile: Handles concurrent add/remove of same element

  LWW-Map:
    - Use: Key-value store with concurrent updates
    - Merge: LWW-Register per key
    - Mobile: Good general-purpose CRDT for settings/config

  IMPLEMENTATION NOTE:
    For most mobile products, LWW-Register + OR-Set cover 90% of cases.
    Full CRDT libraries (Yjs, Automerge) add significant bundle size.
    Prefer implementing only the CRDT types your product needs.
```

### 5. Cross-Platform Security Patterns

#### 5.1 Security Pattern Matrix

| Pattern                        | iOS Implementation                                 | Android Implementation                        | Verification                                            |
| ------------------------------ | -------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------- |
| **Certificate Pinning**        | `URLSessionDelegate` with pinned public key hashes | `OkHttpClient` with `CertificatePinner`       | Pin test endpoint returns 403 if pin fails              |
| **Secure Storage**             | Keychain (`kSecAttrAccessibleAfterFirstUnlock`)    | EncryptedSharedPreferences / Keystore         | Storage is encrypted at rest; verify with device backup |
| **JWT Refresh**                | Silent refresh in background; rotate on 401        | WorkManager background refresh; rotate on 401 | Token rotation is atomic; old token is invalidated      |
| **Biometric Auth**             | `LocalAuthentication` (FaceID/TouchID)             | `BiometricPrompt` (fingerprint/face)          | Fallback to passcode; max 3 attempts before lockout     |
| **Jailbreak/Root Detection**   | `stat("/")` checks, sandbox escape detection       | SafetyNet Attestation / Play Integrity API    | Detection is passive (no blocking on false positive)    |
| **Secure Enclave / StrongBox** | Secure Enclave for key generation (iOS 9+)         | StrongBox Keymaster (Android 9+, Pixel 3+)    | Key never leaves hardware; verify with debug build      |

```swift
// iOS Certificate Pinning Implementation
class PinningDelegate: NSObject, URLSessionDelegate {
    private let pinnedKeys: [String] = [
        "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
    ]

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard let serverTrust = challenge.protectionSpace.serverTrust,
              let secTrust = serverTrust as SecTrust,
              let leafCert = SecTrustCopyCertificateChain(secTrust)?.last as? SecCertificate,
              let leafData = SecCertificateCopyData(leafCert) as Data?
        else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        let leafHash = SHA256.hash(data: leafData).base64EncodedString()
        let pinnedHash = "sha256/\(leafHash)"

        if pinnedKeys.contains(pinnedHash) {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            // PIN FAILURE — log for monitoring, reject connection
            Logger.security.error("Certificate pin mismatch: \(pinnedHash)")
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

```kotlin
// Android Certificate Pinning Implementation
object CertificatePinning {
    private val PINNED_HASHES = listOf(
        "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
    )

    fun createPinnedClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .certificatePinner(
                CertificatePinner.Builder().apply {
                    PINNED_HASHES.forEach { hash ->
                        add("api.company.com", hash)
                    }
                }.build()
            )
            .build()
    }
}

// CRITICAL: Include backup pins for key rotation
// Without backup pins, a server key rotation will brick all app installations
// until the next app update is deployed and installed by all users.
```

#### 5.2 JWT Refresh Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ JWT LIFECYCLE — MOBILE CLIENT                                           │
│                                                                         │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Login  │───►│  Store   │───►│  Attach  │───►│  Request │          │
│  │  (auth  │    │  access  │    │  to all  │    │  with    │          │
│  │  server)│    │  +       │    │  API     │    │  Bearer  │          │
│  │         │    │  refresh │    │  calls   │    │  token   │          │
│  └─────────┘    │  token   │    └────┬─────┘    └────┬─────┘          │
│                 │  (secure │         │               │                 │
│                 │   store) │         │               │                 │
│                 └──────────┘         │               ▼                 │
│                                      │         ┌──────────┐           │
│                                      │         │ 401      │           │
│                                      │         │ expired  │           │
│                                      │         └────┬─────┘           │
│                                      │              │                  │
│                                      │              ▼                  │
│                                      │    ┌──────────────────┐        │
│                                      │    │ Silent Refresh:   │        │
│                                      │    │ POST /auth/refresh│        │
│                                      │    │ { refresh_token } │        │
│                                      │    └────┬────────┬────┘        │
│                                      │         │        │              │
│                                      │    200 OK│        │ 401/403    │
│                                      │    + new │        │ (refresh   │
│                                      │    tokens│        │  expired)  │
│                                      │         ▼        │              │
│                                      │    ┌──────────┐  │  ┌────────┐ │
│                                      │    │ Retry    │  │  │ Force  │ │
│                                      │    │ original │  │  │ logout │ │
│                                      │    │ request  │  │  │ +      │ │
│                                      │    │ with new │  │  │ re-auth│ │
│                                      │    │ token    │  │  └────────┘ │
│                                      │    └──────────┘                │
│                                      │                                 │
│  TOKEN LIFETIMES:                                                        │
│  - Access token:  15 minutes (short-lived, limits exposure)             │
│  - Refresh token: 30 days (rotated on each use)                        │
│  - Max refresh:   90 days of inactivity → force re-auth                 │
│                                                                         │
│  ROTATION RULE: Each refresh invalidates the previous refresh token.     │
│  If two refreshes happen concurrently (race condition), the second       │
│  fails and the client must re-authenticate. This detects token theft.    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6. Build System Architecture

#### 6.1 Monorepo Structure (KMP)

```
project-root/
├── shared/                          # KMP shared module
│   ├── common/                      # Shared across all platforms
│   │   └── src/main/kotlin/
│   ├── android/                     # Android-specific actuals
│   │   └── src/main/kotlin/
│   ├── ios/                         # iOS-specific actuals
│   │   └── src/main/kotlin/
│   └── build.gradle.kts
├── androidApp/
│   ├── app/
│   │   └── src/main/
│   ├── feature-home/
│   ├── feature-profile/
│   └── build.gradle.kts
├── iosApp/
│   ├── iosApp.xcodeproj
│   ├── FeatureHome/
│   ├── FeatureProfile/
│   └── Podfile (if using CocoaPods for KMP)
├── build-logic/                     # Convention plugins (DRY Gradle)
│   ├── convention/
│   └── settings.gradle.kts
├── ci/
│   ├── android-build.sh
│   ├── ios-build.sh
│   ├── shared-test.sh
│   └── dangerfile.ts                # PR risk analysis
└── gradle/
    ├── libs.versions.toml           # Version catalog (single source of truth)
    └── wrapper/
```

#### 6.2 CI/CD Pipeline (Shared)

```yaml
# .github/workflows/mobile-ci.yml
name: Mobile CI
on:
  pull_request:
    paths:
      - "shared/**"
      - "androidApp/**"
      - "iosApp/**"
      - "build-logic/**"
      - "ci/**"

jobs:
  shared-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run shared JVM tests
        run: ./gradlew :shared:common:jvmTest
      - name: Run shared Android tests
        run: ./gradlew :shared:android:testDebugUnitTest

  android-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Android
        run: ./gradlew :androidApp:app:assembleDebug :androidApp:app:testDebugUnitTest
      - name: Lint
        run: ./gradlew :androidApp:app:lintDebug

  ios-build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build iOS
        run: xcodebuild -project iosApp/iosApp.xcodeproj -scheme iosApp -sdk iphonesimulator build
      - name: Run iOS tests
        run: xcodebuild test -project iosApp/iosApp.xcodeproj -scheme iosApp -sdk iphonesimulator

  architecture-conformance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check module dependency graph
        run: ./gradlew :shared:checkModuleDependencies
      - name: Verify ADR compliance
        run: ./ci/check-adr-compliance.sh
      # Fails CI if any module violates the dependency rules defined in Section 2.2
```

#### 6.3 Feature Flag Orchestration

```
FEATURE FLAG CROSS-PLATFORM SYNC:

  Source of Truth: Remote config service (Firebase Remote Config / LaunchDarkly)

  Flag Definition:
  {
    "flag_key": "enable_new_checkout",
    "default_value": false,
    "platform_overrides": {
      "ios": { "min_version": "3.2.0", "value": true },
      "android": { "min_version": "3.2.0", "value": true }
    },
    "rollout": {
      "percentage": 25,
      "seed": "checkout-v2-rollout"
    },
    "kill_switch": false
  }

  Sync Rules:
  1. Flags are fetched on app launch + every 4 hours in background
  2. Flags are cached locally (encrypted storage)
  3. If fetch fails, use cached values; if no cache, use defaults
  4. Flag evaluation is deterministic (same user + same seed = same result)
  5. Kill switch overrides all rollout and platform settings
  6. Flag changes are logged for audit (who changed, when, why)

  Platform Consistency:
  - Both platforms MUST evaluate the same flag the same way
  - Use shared flag evaluation logic in KMP shared module
  - Platform-specific overrides are configured server-side, not client-side
```

### 7. Performance Budgets and Platform Constraints

#### 7.1 Platform-Specific Constraints

| Constraint               | iOS                                  | Android                            | Enforcement                                                       |
| ------------------------ | ------------------------------------ | ---------------------------------- | ----------------------------------------------------------------- |
| **Background Execution** | ~30s (BGTaskScheduler)               | ~10min (WorkManager)               | BG tasks must complete within budget; checkpoint state for resume |
| **Memory Limit**         | ~1/3 of device RAM (varies by model) | ~25% of available heap             | OOM kills are P1 defects; profile with Instruments/Profiler       |
| **App Launch (cold)**    | < 2s to first frame                  | < 2s to first frame                | Measured in CI with Xcode metrics / Baseline Profiles             |
| **App Launch (warm)**    | < 400ms                              | < 400ms                            | Tracked via performance monitoring SDK                            |
| **Network Timeout**      | 10s (cellular), 5s (Wi-Fi)           | 10s (cellular), 5s (Wi-Fi)         | Hardcoded timeout; never exceed 30s for any request               |
| **Battery Budget**       | < 5% per hour of active use          | < 5% per hour of active use        | Measured with Xcode Energy Log / Battery Historian                |
| **Binary Size**          | < 150 MB (App Store limit)           | < 150 MB (Play limit for base APK) | CI fails if binary exceeds 120 MB (20% buffer)                    |
| **Startup Memory**       | < 100 MB                             | < 120 MB                           | Measured at app launch; regression detected in CI                 |

#### 7.2 Performance Budget Enforcement

```
PERFORMANCE BUDGET ENFORCEMENT IN CI:

  ┌─────────────────────────────────────────────────────────────────────┐
  │ PERFORMANCE GATE (runs on every PR)                                 │
  ├──────────────────────┬──────────────┬──────────────┬───────────────┤
  │ Metric               │ Budget       │ Current      │ Status        │
  ├──────────────────────┼──────────────┼──────────────┼───────────────┤
  │ Cold launch (iOS)    │ < 2000ms     │ 1450ms       │ ✅ PASS       │
  │ Cold launch (Android)│ < 2000ms     │ 1680ms       │ ✅ PASS       │
  │ Binary size (iOS)    │ < 120 MB     │ 89 MB        │ ✅ PASS       │
  │ Binary size (Android)│ < 120 MB     │ 76 MB        │ ✅ PASS       │
  │ Startup memory (iOS) │ < 100 MB     │ 72 MB        │ ✅ PASS       │
  │ Startup memory (And) │ < 120 MB     │ 95 MB        │ ✅ PASS       │
  │ Method count (And)   │ < 65,536     │ 42,108       │ ✅ PASS       │
  │ Shared test coverage │ > 80%        │ 87%          │ ✅ PASS       │
  └──────────────────────┴──────────────┴──────────────┴───────────────┘

  REGRESSION RULE: If any metric degrades by > 10% from the previous
  baseline, the PR is blocked. The author must either:
  1. Fix the regression, or
  2. Document a justified exception in the ADR with CTO approval
```

### 8. Architecture-to-Implementation Traceability

#### 8.1 UML to Code Mapping

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TRACEABILITY MATRIX: UML COMPONENT → CODE MODULE                        │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ UML Component            │ Code Module              │ Verification     │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ UserAuthenticationService│ :shared-data:auth        │ CI: module       │
│                          │                          │ dependency check │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ UserProfileRepository    │ :shared-data:repository  │ CI: interface    │
│                          │                          │ compliance test  │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ SyncEngine               │ :shared-data:sync        │ CI: integration  │
│                          │                          │ test             │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ UserSessionViewModel     │ :shared-presentation:    │ CI: unit test    │
│                          │   session                │ + screenshot     │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ LoginScreen (iOS)        │ iosApp/LoginFeature/     │ Manual +         │
│                          │   LoginScreen.swift      │ UI test          │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ LoginScreen (Android)    │ androidApp/feature-      │ Manual +         │
│                          │   auth/LoginScreen.kt    │ UI test          │
└──────────────────────────┴──────────────────────────┴──────────────────┘

AUTOMATED VERIFICATION:
  - Module dependency graph is checked against UML component diagram
  - If code imports a module not shown in the UML diagram → CI failure
  - If UML shows a dependency not present in code → stale UML → update required
  - This is enforced by the Architecture Conformance Test (see below)
```

#### 8.2 Architecture Conformance Testing

```kotlin
// Architecture conformance test (runs in CI)
// Uses ArchUnit (Java) or a custom module graph validator

@Test
fun `domain layer must not depend on data layer`() {
    val domainClasses = classes().that().resideInAPackage("..domain..")
    val dataClasses = classes().that().resideInAPackage("..data..")

    val violation = domainClasses.should().onlyDependOnClassesThat()
        .resideInAnyPackage("..domain..", "..common..", "kotlin..", "java..")
        .check(sharedModule)

    assertTrue(violation.violations.isEmpty()) {
        "Domain layer violates clean architecture:\n" +
            violation.violations.joinToString("\n") { it.description }
    }
}

@Test
fun `all repository implementations must match UML interface`() {
    // Load UML-defined interfaces from architecture/decisions/
    val umlInterfaces = loadUmlInterfaces("component-diagrams.md")

    umlInterfaces.forEach { umlInterface ->
        val codeImplementation = findImplementation(umlInterface.name)
        assertNotNull(codeImplementation) {
            "UML interface ${umlInterface.name} has no code implementation"
        }

        umlInterface.methods.forEach { method ->
            assertTrue(codeImplementation.hasMethod(method)) {
                "Implementation of ${umlInterface.name} is missing method: ${method.signature}"
            }
        }
    }
}

@Test
fun `no module may exceed maximum dependency depth`() {
    val graph = ModuleDependencyGraph.build(sharedModule)
    val maxDepth = graph.maximumDepth

    assertTrue(maxDepth <= 4) {
        "Module dependency depth is $maxDepth (max allowed: 4). " +
            "Violating chain: ${graph.longestChain.joinToString(" -> ")}"
    }
}
```

#### 8.3 ADR Enforcement in Code Review

```
ADR COMPLIANCE CHECKLIST (applied at Stage 6 Code Review):

  For each accepted ADR:
  ☐ ADR-NNN: <Title>
    ☐ Decision implemented in code (link to PR / commit)
    ☐ No violations of decision constraints
    ☐ If decision was "use X instead of Y", no Y imports in codebase
    ☐ Success criteria are measurable (if not yet measurable → P2 defect)
    ☐ Related UML diagrams are updated if code diverged

  DEFECT CLASSIFICATION:
  - ADR violated without documented exception → P1 (major architecture violation)
  - ADR success criteria not measurable → P2 (documentation gap)
  - UML diagram out of sync with code → P2 (documentation drift)
  - ADR referenced but not implemented → P1 (missing functionality)
```
