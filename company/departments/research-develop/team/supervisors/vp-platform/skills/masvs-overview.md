---
name: masvs-overview
description: OWASP MASVS executive overview for a platform engineer — understanding the eight verification categories, how MASVS gates interact with the CI/CD pipeline David owns, and how to interpret security scan results at Stage 6 (Code Review) and Stage 8 (Integrity Verification). Use when reviewing pipeline security outputs or participating in Stage 8 Integrity Verification panels.
version: "1.0.0"
---

# MASVS Overview

## Purpose

Equip David Okonkwo (VP Platform) with sufficient MASVS fluency to: (1) configure CI/CD pipeline security gates that enforce MASVS-relevant checks, (2) interpret automated security scan results at Stage 6, and (3) participate meaningfully in Stage 8 Integrity Verification panels. David is not expected to conduct MASVS assessments — that is Sana Khoury's (Security Engineer) and Ingrid Solberg's (Compliance Analyst) domain. His role is to ensure the platform enables MASVS compliance, not to verify it.

## MASVS in One Paragraph

The OWASP Mobile Application Security Verification Standard (MASVS) defines security requirements for mobile applications across 8 categories. It has two assessment levels: L1 (baseline, required for all apps) and L2 (defence-in-depth, required for apps handling sensitive data). The company applies MASVS L1 to all releases and L2 to any feature touching authentication, payments, or health data. Compliance is verified by Sana Khoury (penetration testing) and Ingrid Solberg (compliance audit) at Stage 6 and Stage 8.

## The Eight MASVS Categories — Platform Relevance

| Category                | What It Covers                                                                  | Platform Engineering Impact                                                       |
| ----------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **V1 — Storage**        | Sensitive data at rest: Keychain/Keystore, no sensitive data in logs or backups | CI/CD: SAST rules (Semgrep) scan for hardcoded keys and insecure storage patterns |
| **V2 — Crypto**         | Correct cryptographic algorithms; no broken crypto (MD5, SHA1, DES)             | CI/CD: Semgrep rules block PRs using deprecated crypto APIs                       |
| **V3 — Authentication** | Secure auth, session management, biometrics                                     | CI/CD: Dynamic DAST scan against staging auth endpoints                           |
| **V4 — Network**        | TLS certificate pinning, no cleartext traffic                                   | CI/CD: Network security config linting; cleartext traffic lint rule blocks PRs    |
| **V5 — Platform APIs**  | Safe use of platform APIs; no exported components leaking data                  | CI/CD: Android `AndroidManifest.xml` exported-component scanner                   |
| **V6 — Code Quality**   | No memory bugs, no debug code in release, code obfuscation                      | CI/CD: Release build strip rules; debug logging lint; ProGuard/R8 config check    |
| **V7 — Resilience**     | Anti-tampering, anti-debugging, root/jailbreak detection (L2 only)              | CI/CD: Release build validation that integrity checks are active                  |
| **V8 — Privacy**        | Data minimization, consent, privacy controls                                    | Not directly in CI/CD — reviewed manually at Stage 6                              |

## CI/CD Gates David Configures for MASVS

David's pipeline owns the following MASVS-supporting security gates:

```yaml
# .github/workflows/security-gates.yml (excerpt)
jobs:
  sast-masvs:
    name: SAST — MASVS V1/V2/V5/V6
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep MASVS rules
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/android
            p/secrets
          # MASVS V1: no hardcoded credentials
          # MASVS V2: no broken crypto
          # MASVS V6: no debug code in source

  network-security-lint:
    name: Android Network Security Config — MASVS V4
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check cleartext traffic disabled
        run: |
          # Fail if cleartextTrafficPermitted="true" in release config
          grep -r 'cleartextTrafficPermitted="true"' app/src/release/ && exit 1 || exit 0

  release-build-validation:
    name: Release Build Validation — MASVS V6/V7
    runs-on: ubuntu-latest
    steps:
      - name: Verify ProGuard/R8 obfuscation active
        run: |
          grep -q 'minifyEnabled true' app/build.gradle.kts || (echo "Obfuscation not enabled in release" && exit 1)
      - name: Verify debug logging stripped
        run: |
          ! grep -rn "Log\.d\|Log\.v\|println" app/src/main/ || (echo "Debug logs found in main source" && exit 1)
```

## Stage 6 and Stage 8 Panel Participation

At Stage 6 (Code Review) and Stage 8 (Integrity Verification), David reviews the security scan outputs and confirms:

**Stage 6 checklist (David's scope):**

- [ ] SAST scan passed (zero MASVS V1/V2/V6 findings)
- [ ] Network security config lint passed (MASVS V4)
- [ ] Release build config validated — obfuscation active, debug code absent (MASVS V6)
- [ ] SBOM generated and artifact signed (supply chain — MASVS V6 supplementary)

**Stage 8 checklist (David's scope):**

- [ ] All Stage 6 pipeline gates green in the release candidate build
- [ ] Sana Khoury's penetration test report reviewed — any MASVS findings relating to the CI/CD pipeline (e.g., secrets exposed in build logs) are David's remediation responsibility
- [ ] Certificate pinning configuration validated for release build (MASVS V4)

## What David Defers to the Security Team

David does not attempt to assess MASVS compliance manually. Any of the following are immediately escalated to Sana Khoury (Security Engineer) or the CSO:

- Dynamic analysis findings (DAST results, network interception results)
- Reverse engineering findings (binary analysis)
- Authentication flow security decisions
- Cryptographic implementation choices
- Privacy control assessments (MASVS V8)

## Quality Standards

- All MASVS-relevant CI/CD gates are active and blocking in the release pipeline before Stage 5 begins
- Zero MASVS V1/V2/V4/V6 violations in SAST output before Stage 6 sign-off
- David can accurately interpret any SAST finding and route it to the correct owner within 4 hours of Stage 6 panel notification
