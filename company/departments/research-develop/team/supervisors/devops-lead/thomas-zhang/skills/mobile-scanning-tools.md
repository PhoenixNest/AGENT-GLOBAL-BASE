---
name: mobile-scanning-tools
description: Mobile application security scanning toolchain — MobSF (static analysis), Frida-based dynamic analysis, network traffic interception (mitmproxy), and the integration of mobile-specific SAST/DAST results into the CI/CD pipeline and Stage 6/8 security gates. Covers how Thomas Zhang operates these tools in coordination with the CSO's pen testing scope. Use when setting up mobile security scanning, when triaging MobSF findings, or when preparing the mobile security scan results for Stage 8 Integrity Verification.
version: "1.0.0"
---

# Mobile Scanning Tools

## Purpose

Integrate mobile-specific security scanning into the company's CI/CD pipeline. Generic web SAST tools (Semgrep, Snyk) do not catch mobile-specific vulnerabilities: insecure data storage in SharedPreferences, exposed deep link handlers, APK/IPA manifest misconfigurations, and certificate pinning bypass vectors. Thomas Zhang operates the mobile security scanning toolchain and delivers results to the CSO for Stage 8 sign-off.

## Tool Stack

| Tool                       | Type     | Platform      | Purpose                                                            |
| -------------------------- | -------- | ------------- | ------------------------------------------------------------------ |
| **MobSF**                  | SAST     | Android + iOS | Static analysis of APK/IPA/source; MASVS-aligned findings          |
| **Semgrep (mobile rules)** | SAST     | Android + iOS | Source-level pattern matching; runs in CI on every PR              |
| **mitmproxy**              | DAST     | Android       | Network traffic interception; verifies TLS and certificate pinning |
| **Frida**                  | DAST     | Android + iOS | Runtime analysis; tests anti-tampering and SSL pinning bypass      |
| **jadx**                   | Analysis | Android       | APK decompilation for manual verification of MobSF findings        |
| **objection**              | Runtime  | Android + iOS | Frida-based runtime exploration; used by CSO pen test team         |

## MobSF — Static Analysis

MobSF is the primary static analysis tool. Thomas runs it on every release candidate APK/IPA, not on every PR (too slow; PR scanning uses Semgrep source rules).

### Automated MobSF Run (Release Candidate)

```bash
# Start MobSF server (Docker)
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest

# Upload and scan APK
curl -F "file=@app-release.apk" http://localhost:8000/api/v1/upload \
  -H "Authorization: $MOBSF_API_KEY" \
  | python scripts/mobsf-check-score.py --fail-below 70
```

### MobSF Scoring Threshold

| MobSF Security Score | Action                                                                         |
| -------------------- | ------------------------------------------------------------------------------ |
| ≥ 80                 | Pass — include in Stage 8 compliance package                                   |
| 70–79                | Warning — Thomas reviews all findings with CSO; proceed only with CSO sign-off |
| < 70                 | Block release — P0 security issue; Thomas notifies CSO within 2 hours          |

### MobSF Finding Categories (MASVS alignment)

| MobSF Category             | MASVS Control    | Common Findings                                   |
| -------------------------- | ---------------- | ------------------------------------------------- |
| Insecure Data Storage      | MASVS-STORAGE-1  | WorldReadable files, unencrypted SQLite databases |
| Insecure Communication     | MASVS-NETWORK-1  | HTTP traffic, missing certificate pinning         |
| Manifest Misconfigurations | MASVS-PLATFORM-1 | Exported components, debuggable flag in release   |
| Hardcoded Secrets          | MASVS-CODE-1     | API keys, passwords in source                     |
| Insecure Cryptography      | MASVS-CRYPTO-1   | MD5/SHA1 usage, ECB mode                          |
| Insecure Authentication    | MASVS-AUTH-1     | Weak session token storage                        |

### False Positive Management

MobSF produces false positives, especially for third-party SDKs. Thomas maintains a `mobsf-suppressions.json`:

```json
{
  "suppressions": [
    {
      "finding_id": "android_detect_tapjacking",
      "reason": "filterTouchesWhenObscured = true is set in the layout XML — MobSF does not detect this",
      "cso_approved": "2026-03-15",
      "review_date": "2026-09-15"
    }
  ]
}
```

All suppressions require CSO written approval. Thomas reviews the list quarterly and removes outdated suppressions.

## Network Traffic Interception (mitmproxy)

Thomas runs mitmproxy tests on the staging build to verify TLS enforcement and certificate pinning:

```bash
# Set up mitmproxy as proxy for Android emulator
mitmproxy --mode transparent --ssl-insecure

# Configure emulator to use mitmproxy proxy
adb shell settings put global http_proxy 192.168.1.100:8080

# Attempt HTTPS interception — should FAIL if cert pinning is active
curl https://api.company.com/health --proxy http://192.168.1.100:8080

# Expected: connection refused / SSL error (pinning working)
# Fail condition: 200 OK response (pinning not working)
```

**Certificate pinning verification is mandatory before Stage 8 for any release that includes payment or auth endpoints.** Results are documented in the Stage 8 compliance package.

## Coordination with CSO Pen Test

The CSO (Dr. Sarah Chen) runs a full penetration test on the release candidate for major releases. Thomas's role in supporting the pen test:

| Phase               | Thomas's Responsibility                                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pre-pen-test**    | Provide build with debugging enabled (special pen-test build); share network architecture diagram; grant access to test environment         |
| **During pen-test** | Monitor staging infrastructure; be on-call for environment questions; do not deploy any changes during pen-test window                      |
| **Post-pen-test**   | Receive findings report from CSO; triage infrastructure/pipeline findings (Jira); coordinate fixes for infrastructure-layer vulnerabilities |
| **Stage 8**         | Include pen test results summary in compliance package; confirm infrastructure findings remediated                                          |

## CI Integration Summary

| Stage                   | Tool                         | Trigger            | Action on Failure                        |
| ----------------------- | ---------------------------- | ------------------ | ---------------------------------------- |
| Every PR                | Semgrep (mobile rules)       | PR to main/release | Block merge                              |
| Release candidate build | MobSF static scan            | Release tag        | Block release if score < 70              |
| Release candidate build | mitmproxy cert pinning check | Release tag        | Block release if pinning bypass succeeds |
| Pre-Stage 8             | Full CSO pen test            | Manual trigger     | P0 findings block Stage 8                |

## Quality Standards

- MobSF run on every release candidate APK/IPA; results included in Stage 8 compliance package
- Certificate pinning verification completed before every major release containing auth or payment endpoints
- All MobSF suppressions have CSO written approval; reviewed quarterly
- CSO pen test results delivered to Thomas within 5 business days of the pen-test window close
- Thomas delivers mobile security scan report to CSO 48 hours before Stage 8 review
