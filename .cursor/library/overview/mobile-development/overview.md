# Mobile Development Pipeline — Overview

**Pipeline:** Mobile Development (P0 — Original)
**Full Definition:** [`pipeline.md`](../../pipeline/mobile-development/pipeline.md)
**Monitoring:** [`monitoring.md`](../../pipeline/mobile-development/monitoring.md)

---

## Platform Focus

Android, iOS, KMP Cross-Platform, Flutter Cross-Platform. The original pipeline from which the standardized governance framework was derived.

---

## Platform Strategy Matrix

Five mutually exclusive scenarios — a project selects exactly one:

| Dimension             | Android-Only           | iOS-Only             | Both Native                | KMP Cross-Platform                     | Flutter Cross-Platform                     |
| --------------------- | ---------------------- | -------------------- | -------------------------- | -------------------------------------- | ------------------------------------------ |
| **Stage 3 ADR**       | N/A                    | N/A                  | Native dual-track          | KMP shared module                      | Flutter single codebase                    |
| **Stage 5 Tracks**    | Track A only           | Track B only         | Track A + B                | Track C (KMP) + A/B (light)            | Track C (Flutter) + A/B (light)            |
| **Stage 5 Team Size** | 7                      | 7                    | 13                         | 11                                     | 11                                         |
| **Stage 6 Review**    | Android Lead only      | iOS Lead only        | Android ↔ iOS cross-review | KMP Lead + Android/iOS review adapters | Flutter Lead + Android/iOS review channels |
| **Stage 7 Testing**   | Espresso + device farm | XCTest + device farm | Both platforms separately  | KMP shared (JVM) + platform adapters   | Flutter widget + platform channel tests    |
| **Stage 10**          | Google Play            | App Store            | Both stores                | Both stores                            | Both stores                                |

---

## Stage-Specific Highlights

### Stage 2: Prototype + IDS

- Platform-specific prototype (iOS simulator / Android emulator)
- IDS with HIG (iOS) / Material Design 3 (Android) conventions
- Platform-specific accessibility specs (VoiceOver / TalkBack)

### Stage 3: ADRs (6 total)

- `ADR-PLATFORM-STRATEGY.md` — Native vs KMP vs Flutter decision
- `ADR-SECURITY-CRYPTO.md` — Cryptography per platform
- `ADR-SECURITY-PINNING.md` — Certificate pinning (ATS / Keystore)
- `ADR-SECURITY-STORAGE.md` — Keychain / Keystore / EncryptedSharedPreferences
- `ADR-SECURITY-PLATFORM-PATTERNS.md` — Deep links, push notifications, biometric auth
- `ADR-STRING-KEY-TAXONOMY.md` — String key naming across platforms

### Stage 5: Development

- Three tracks: Track A (Android), Track B (iOS), Track C (KMP/Flutter)
- Design Fidelity Checkpoint at ~60%: CDO reviews against IDS
- Contract Verification Reports at 30%/70% for KMP/Flutter

### Stage 6: Code Review

- Live demonstration: running app on device/simulator
- Three-Layer Defense: Platform Lead attestation → Elena Rostova audit → CI/CD gates
- IDS Conformance Matrix ≥ 95%

### Stage 7: Testing

- OWASP MASVS manual penetration testing
- Espresso (Android) / XCTest (iOS) UI tests
- Firebase Test Lab / AWS Device Farm device matrix
- Performance profiling: cold start <2s, 60fps, memory <150MB

### Stage 8: Stealthy Weakening Examples (P0)

- Weakened certificate pinning, removed jailbreak detection, relaxed Keychain/Keystore encryption

---

## Monitoring

Three-layer architecture with mobile-specific fields:

- Track A/B/C structure with Gradle/Xcode/KMP build tree
- Performance SLA: cold start <2s, 60fps, memory <150MB
- Security state: MASVS compliance, certificate pinning, Play Integrity

---

_For complete stage definitions, gate criteria, and artifact lists, see the [full pipeline definition](../../pipeline/mobile-development/pipeline.md)._
