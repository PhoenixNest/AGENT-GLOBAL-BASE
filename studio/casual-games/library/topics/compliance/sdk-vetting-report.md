# SDK Vetting Report

**Studio:** Casual Games  
**Audit Condition:** C2 (SDK Vetting)  
**Date:** April 10, 2026 (Week 3)  
**Conducted By:** CSO Office (Dr. Sarah Chen) + CIO Office (Dr. Priya Mehta)  
**Scope:** 7 third-party SDKs evaluated for privacy, COPPA compliance, network security, permissions, auditability, and provider reputation  
**Classification:** INTERNAL — COMPLIANCE RECORD

---

## 1. Executive Summary

This report documents the completion of third-party SDK vetting for the Casual Games studio, fulfilling **Audit Condition C2**. Seven (7) SDKs were evaluated across six security and compliance dimensions: Privacy Policy Review, COPPA Compliance, Network Endpoints, Permissions, Auditability, and Provider Reputation.

| Metric      | Count |
| ----------- | ----- |
| SDKs Vetted | 7     |
| **PASS**    | 5     |
| **WARNING** | 1     |
| **FAIL**    | 1     |

**Overall Determination:**

- **5 SDKs** passed all vetting criteria without reservation: **PlayFab**, **Firebase**, **Unity Engine**, **Google Play Games**, **Apple Game Center**.
- **1 SDK** received a **WARNING** determination: **AdMob** — collects device ID for ad targeting; requires COPPA-compliant ad mediation configuration before deployment.
- **1 SDK** received a **FAIL** determination: **Unity Ads** — collects behavioral data without parental consent mechanism, rendering it incompatible with COPPA requirements for child-directed products.

**Gate Status:** Condition C2 is **CLOSED** upon completion of remediation actions for AdMob (configuration update) and Unity Ads (replacement). Remediation is scheduled for Week 4 and tracked separately.

---

## 2. SDK Vetting Results Table

| #   | SDK Name          | Version | Provider           | Privacy Policy Review | COPPA Compliance | Network Endpoints | Permissions | Auditability | Provider Reputation | **Overall** |
| --- | ----------------- | ------- | ------------------ | --------------------- | ---------------- | ----------------- | ----------- | ------------ | ------------------- | ----------- |
| 1   | PlayFab           | 2.14.3  | Microsoft          | PASS                  | PASS             | PASS              | PASS        | PASS         | PASS                | **PASS**    |
| 2   | Firebase          | 11.8.0  | Google             | PASS                  | PASS             | PASS              | PASS        | PASS         | PASS                | **PASS**    |
| 3   | Unity Engine      | 2023.3  | Unity Technologies | PASS                  | PASS             | PASS              | PASS        | PASS         | PASS                | **PASS**    |
| 4   | Google Play Games | 2.4.1   | Google             | PASS                  | PASS             | PASS              | PASS        | PASS         | PASS                | **PASS**    |
| 5   | Apple Game Center | N/A     | Apple Inc.         | PASS                  | PASS             | PASS              | PASS        | PASS         | PASS                | **PASS**    |
| 6   | AdMob             | 23.2.0  | Google             | PASS                  | WARN             | PASS              | PASS        | PASS         | PASS                | **WARNING** |
| 7   | Unity Ads         | 4.12.2  | Unity Technologies | PASS                  | FAIL             | PASS              | WARN        | PASS         | PASS                | **FAIL**    |

**Evaluation Criteria Definitions:**

| Criterion             | What Was Evaluated                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | SDK provider's public privacy policy adequacy, transparency, and alignment with our product's user base.                     |
| COPPA Compliance      | SDK's ability to operate without collecting personal information from children under 13 without verifiable parental consent. |
| Network Endpoints     | All network destinations use TLS 1.2+, certificate pinning support, and no hardcoded secrets.                                |
| Permissions           | SDK's declared permissions are minimal, justified, and do not exceed the principle of least privilege.                       |
| Auditability          | SDK provides logging, version pinning, dependency transparency, and can be included in our SBOM.                             |
| Provider Reputation   | Provider's track record with security incidents, regulatory compliance, and industry standing.                               |

---

## 3. Detailed Findings

### 3.1 PlayFab — PASS

| Dimension             | Result | Notes                                                                                                                                                                                 |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS   | Microsoft's privacy policy is comprehensive, transparent, and publicly accessible.                                                                                                    |
| COPPA Compliance      | PASS   | PlayFab includes built-in parental consent support. Title-level configuration can enforce COPPA mode, disabling data collection features not appropriate for child-directed products. |
| Network Endpoints     | PASS   | All endpoints use TLS 1.2+. Certificate pinning is supported via custom HTTP handler. No hardcoded secrets detected in SDK binaries.                                                  |
| Permissions           | PASS   | Permissions are limited to network access and storage for cached data. No sensitive device permissions requested.                                                                     |
| Auditability          | PASS   | SDK version is explicitly pinned in dependency manifest. Full SBOM entry created. Logging hooks available for telemetry audit.                                                        |
| Provider Reputation   | PASS   | Microsoft is a Tier-1 provider with established compliance certifications (SOC 2, ISO 27001, COPPA Safe Harbor).                                                                      |

**Verdict:** No findings. Approved for production use.

---

### 3.2 Firebase — PASS

| Dimension             | Result | Notes                                                                                                                                                                                                                                                                                                               |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS   | Google's Firebase privacy documentation is comprehensive. Data processing addendum available for enterprise use.                                                                                                                                                                                                    |
| COPPA Compliance      | PASS   | Firebase Analytics can be configured for COPPA compliance by disabling Advertising ID collection (`firebase_analytics_collection_enabled = false` for ad-related events). Crashlytics and Remote Config operate without personal data collection. Firebase's Tagged for Child-Directed Treatment flag is supported. |
| Network Endpoints     | PASS   | All Firebase endpoints use TLS 1.2+ with certificate pinning support. No unencrypted fallback paths detected.                                                                                                                                                                                                       |
| Permissions           | PASS   | Default permissions are minimal: `INTERNET`, `ACCESS_NETWORK_STATE`. Optional features (e.g., Crashlytics) add only `RECEIVE_BOOT_COMPLETED`.                                                                                                                                                                       |
| Auditability          | PASS   | Firebase SDK version pinned. Bill of Materials (BOM) mechanism ensures consistent dependency versions. SBOM entry created.                                                                                                                                                                                          |
| Provider Reputation   | PASS   | Google maintains industry-leading security posture with regular third-party audits and transparent security advisories.                                                                                                                                                                                             |

**Verdict:** No findings. Approved for production use with COPPA configuration confirmed (advertising ID collection disabled).

---

### 3.3 Unity Engine — PASS

| Dimension             | Result | Notes                                                                                                                                                                                                                                                                                      |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Privacy Policy Review | PASS   | Unity Technologies' privacy policy covers engine-level data handling. No runtime telemetry enabled by default for child-directed builds.                                                                                                                                                   |
| COPPA Compliance      | PASS   | Unity Engine itself does not perform external data collection. Runtime services (e.g., Unity Analytics) are opt-in modules and were evaluated separately. The base engine is COPPA-safe when configured with `PlayerSettings.SetIl2CppCompilerConfiguration` for child-directed treatment. |
| Network Endpoints     | PASS   | Engine core makes no outbound network calls. Network functionality is developer-controlled.                                                                                                                                                                                                |
| Permissions           | PASS   | Unity Engine declares no permissions beyond those required by the target platform manifest.                                                                                                                                                                                                |
| Auditability          | PASS   | Unity version explicitly locked at 2023.3 LTS. SBOM entry includes engine version and installed packages.                                                                                                                                                                                  |
| Provider Reputation   | PASS   | Unity Technologies is the dominant mobile game engine provider with established security practices.                                                                                                                                                                                        |

**Verdict:** No findings. Approved for production use.

---

### 3.4 Google Play Games Services — PASS

| Dimension             | Result | Notes                                                                                                                                                                                                                |
| --------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS   | Google Play Games Services privacy documentation is clear. Data usage limited to gameplay features (achievements, leaderboards, cloud saves).                                                                        |
| COPPA Compliance      | PASS   | Google Play Games Services supports COPPA compliance through Google's parental consent framework. Child-directed app designation in Google Play Console automatically restricts data collection and social features. |
| Network Endpoints     | PASS   | All Play Games Services endpoints use TLS 1.2+. Google's infrastructure supports certificate transparency.                                                                                                           |
| Permissions           | PASS   | Required permissions: `INTERNET`, `ACCESS_NETWORK_STATE`. No sensitive permissions requested.                                                                                                                        |
| Auditability          | PASS   | SDK version pinned via Play Services BOM. SBOM entry created.                                                                                                                                                        |
| Provider Reputation   | PASS   | Google's Play Services infrastructure is the industry standard for Android game services.                                                                                                                            |

**Verdict:** No findings. Approved for production use.

---

### 3.5 Apple Game Center — PASS

| Dimension             | Result | Notes                                                                                                                                                                                                                                                                               |
| --------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS   | Apple's privacy policy and App Store privacy nutrition labels provide full transparency for Game Center data handling.                                                                                                                                                              |
| COPPA Compliance      | PASS   | Apple's parental consent framework covers COPPA requirements. Game Center features (achievements, leaderboards) are restricted for child-directed apps through Apple's App Store designation. Apple's App Tracking Transparency (ATT) framework provides additional consent gating. |
| Network Endpoints     | PASS   | All Game Center endpoints use TLS 1.2+ with Apple-managed certificate pinning.                                                                                                                                                                                                      |
| Permissions           | PASS   | No additional permissions beyond standard GameKit framework access.                                                                                                                                                                                                                 |
| Auditability          | PASS   | GameKit framework version locked to iOS 17+ deployment target. SBOM entry created.                                                                                                                                                                                                  |
| Provider Reputation   | PASS   | Apple maintains the strongest privacy posture in the mobile industry, with COPPA compliance built into App Store review guidelines.                                                                                                                                                 |

**Verdict:** No findings. Approved for production use.

---

### 3.6 AdMob — WARNING

| Dimension             | Result   | Notes                                                                                                                                                                                                    |
| --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS     | Google's AdMob privacy policy is comprehensive and publicly documented.                                                                                                                                  |
| COPPA Compliance      | **WARN** | **FINDING:** AdMob collects device identifiers (GAID/IDFA) for ad targeting by default. Without configuration, this constitutes personal information collection under COPPA for child-directed products. |
| Network Endpoints     | PASS     | All AdMob endpoints use TLS 1.2+. Certificate pinning supported via SafetyNet/Play Integrity integration.                                                                                                |
| Permissions           | PASS     | Permissions are standard for ad SDKs: `INTERNET`, `ACCESS_NETWORK_STATE`, `ACCESS_WIFI_STATE`. No excessive permissions detected.                                                                        |
| Auditability          | PASS     | AdMob SDK version pinned. SBOM entry created. Ad request logging available for compliance audit.                                                                                                         |
| Provider Reputation   | PASS     | Google's ad platform is industry-standard with established compliance frameworks.                                                                                                                        |

**Finding Detail:**

AdMob's default configuration collects the Google Advertising ID (GAID) on Android and IDFA on iOS for ad personalization and targeting. Under COPPA, device identifiers that can be used to track a child across services constitute personal information, requiring verifiable parental consent before collection.

**Remediation Required:**

1. Enable **"Designed for Families"** ad mediation configuration in AdMob console, which automatically serves child-safe ads without personalized targeting.
2. Set `tagForChildDirectedTreatment(true)` in the AdMob SDK initialization code on both Android and iOS platforms.
3. Disable ad personalization signals at the ad request level.
4. Verify that mediated ad networks also respect child-directed treatment flags.

**Residual Risk:** LOW — Once configured, AdMob operates in a COPPA-compliant mode. However, misconfiguration during development or updates could revert to default behavior. Automated configuration tests will be added to the CI/CD pipeline to detect regression.

**Verdict:** **WARNING** — Approved for production use **only after** remediation actions are completed and verified.

---

### 3.7 Unity Ads — FAIL

| Dimension             | Result   | Notes                                                                                                                                                                                                                                                                                                    |
| --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Privacy Policy Review | PASS     | Unity Technologies' privacy policy covers Unity Ads data practices.                                                                                                                                                                                                                                      |
| COPPA Compliance      | **FAIL** | **FINDING:** Unity Ads collects behavioral data (device identifiers, browsing patterns, ad interaction history) without a parental consent mechanism. This data is used for ad targeting and profiling, which is prohibited under COPPA for child-directed products without verifiable parental consent. |
| Network Endpoints     | PASS     | Endpoints use TLS 1.2+. No unencrypted paths detected.                                                                                                                                                                                                                                                   |
| Permissions           | **WARN** | Unity Ads requests `ACCESS_FINE_LOCATION` on Android for ad targeting. This exceeds the principle of least privilege for a child-directed product and is unnecessary for ad serving.                                                                                                                     |
| Auditability          | PASS     | SDK version pinned. SBOM entry created.                                                                                                                                                                                                                                                                  |
| Provider Reputation   | PASS     | Unity Technologies is a reputable provider, but Unity Ads' data collection practices are not designed for child-directed audiences.                                                                                                                                                                      |

**Finding Detail (P0 — COPPA Non-Compliance):**

Unity Ads' SDK architecture is built around behavioral targeting. The SDK collects:

- **Device identifiers** (GAID, IDFA, Unity Device ID) for cross-app tracking.
- **Ad interaction history** (impressions, clicks, dwell time) for profiling.
- **Approximate location** derived from IP address and, on Android, GPS when `ACCESS_FINE_LOCATION` permission is granted.
- **Application usage patterns** including session duration and in-app behavior.

None of these data collection practices include a parental consent gating mechanism. The SDK's "child-directed" flag is advisory only and does not prevent data transmission to Unity's ad servers. This makes Unity Ads **fundamentally incompatible** with COPPA requirements for products targeting children under 13.

**Remediation Required:**

Unity Ads **cannot be remediated through configuration**. The SDK must be **replaced** with a COPPA-compliant alternative.

**Recommended Replacement:** **AppLovin MAX Mediation** with COPPA mode enabled.

| Criterion                | AppLovin MAX (COPPA Mode)                            |
| ------------------------ | ---------------------------------------------------- |
| COPPA-compliant          | ✅ Yes — enforces data minimization                  |
| Parental consent support | ✅ Yes — integrates with existing consent frameworks |
| No behavioral targeting  | ✅ Yes — serves contextual ads only                  |
| Mediation capability     | ✅ Yes — supports multiple ad networks               |
| Migration effort         | Medium — 2–3 engineering days                        |

**Verdict:** **FAIL** — Unity Ads must be removed from the product. Replacement with AppLovin MAX (or equivalent COPPA-compliant ad SDK) is required before Stage 10 Release Readiness.

---

## 4. Remediation Actions

The following remediation actions have been scheduled and assigned. Completion is required before Stage 10 Release Readiness gate.

| #   | Action                                             | SDK Affected | Owner                | Priority | Target Date     | Status        |
| --- | -------------------------------------------------- | ------------ | -------------------- | -------- | --------------- | ------------- |
| 1   | Replace Unity Ads with AppLovin MAX (COPPA mode)   | Unity Ads    | R&D (Android + iOS)  | **P0**   | Week 4 (Apr 17) | **Scheduled** |
| 2   | Remove Unity Ads SDK from project dependencies     | Unity Ads    | R&D (Platform Leads) | **P0**   | Week 4 (Apr 17) | **Scheduled** |
| 3   | Enable AdMob "Designed for Families" mode          | AdMob        | R&D (Platform Leads) | **P1**   | Week 4 (Apr 17) | **Scheduled** |
| 4   | Set `tagForChildDirectedTreatment(true)` in code   | AdMob        | R&D (Android + iOS)  | **P1**   | Week 4 (Apr 17) | **Scheduled** |
| 5   | Add CI/CD configuration validation for AdMob       | AdMob        | CTO Office           | **P2**   | Week 5 (Apr 24) | **Scheduled** |
| 6   | Verify AppLovin MAX COPPA configuration in staging | AppLovin MAX | CSO Office           | **P0**   | Week 5 (Apr 24) | **Scheduled** |

**Remediation Tracking:**

- Actions #1–#4 are on the critical path and must be completed before Stage 6 Code Review.
- Action #5 is a defensive control to prevent configuration regression.
- Action #6 provides independent CSO verification of the replacement SDK's COPPA posture.

---

## 5. Audit Trail

| Event                             | Date         | Actor                   | Notes                                                                                                |
| --------------------------------- | ------------ | ----------------------- | ---------------------------------------------------------------------------------------------------- |
| SDK inventory compiled            | Apr 7, 2026  | CSO Office              | 7 SDKs identified across Android and iOS platforms.                                                  |
| Privacy policy reviews completed  | Apr 8, 2026  | CIO Office              | All 7 SDK providers' privacy policies reviewed against COPPA baseline.                               |
| Network endpoint analysis         | Apr 8, 2026  | CSO Office              | TLS 1.2+ verification, certificate pinning assessment, endpoint enumeration.                         |
| Permissions audit                 | Apr 9, 2026  | CSO Office              | Manifest-level and runtime permission review for all 7 SDKs.                                         |
| COPPA compliance deep-dive        | Apr 9, 2026  | CSO Office + CIO Office | Joint review of data collection practices, consent mechanisms, and child-directed treatment support. |
| AdMob WARNING finding documented  | Apr 10, 2026 | CSO Office              | Configuration gap identified; remediation plan drafted.                                              |
| Unity Ads FAIL finding documented | Apr 10, 2026 | CSO Office + CIO Office | Structural COPPA non-compliance confirmed; replacement recommended.                                  |
| Report finalized and signed off   | Apr 10, 2026 | CSO Office + CIO Office | This document.                                                                                       |

---

## 6. Sign-Off

This SDK Vetting Report has been reviewed and approved by the undersigned officers. The findings and remediation actions documented herein are authoritative and binding for the Casual Games studio.

| Role                          | Name            | Signature         | Date           |
| ----------------------------- | --------------- | ----------------- | -------------- |
| **Chief Security Officer**    | Dr. Sarah Chen  | _Dr. Sarah Chen_  | April 10, 2026 |
| **Chief Information Officer** | Dr. Priya Mehta | _Dr. Priya Mehta_ | April 10, 2026 |

**Attestation:**

> We attest that the SDK vetting documented in this report was conducted in accordance with the company's Security Requirements Document (SRD), OWASP Mobile Application Security Verification Standard (MASVS), and the Children's Online Privacy Protection Act (COPPA) Rule (16 CFR Part 312). The findings reflect our professional assessment as of the date of signing.

---

## 7. Status

**COMPLETED** — April 10, 2026

Audit Condition C2 (SDK Vetting) is **CLOSED** pending completion of remediation actions (#1–#6) tracked in Section 4. All remediation actions are scheduled for Weeks 4–5 and will be verified by the CSO Office before Stage 6 Code Review gate entry.

| Condition           | Status    | Closure Date   | Notes                                                |
| ------------------- | --------- | -------------- | ---------------------------------------------------- |
| **C2: SDK Vetting** | ✅ CLOSED | April 10, 2026 | Remediation actions scheduled. Verification pending. |

---

_Document generated by CSO Office (Dr. Sarah Chen) in collaboration with CIO Office (Dr. Priya Mehta)._  
_Classification: INTERNAL — COMPLIANCE RECORD. Retention: 7 years._
