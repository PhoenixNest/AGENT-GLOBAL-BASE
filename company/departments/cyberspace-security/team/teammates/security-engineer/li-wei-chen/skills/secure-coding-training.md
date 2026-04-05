# Secure Coding Training & Security Champions Program

**Category:** Developer Education & Security Culture
**Owner:** Security Engineer #3 — Li Wei Chen (Supply Chain Security Specialist)

## Overview

Design, implement, and manage comprehensive secure coding education programs that embed security competency into the engineering organization. This skill covers secure coding curriculum design for mobile platforms (Kotlin/Android, Swift/iOS, Dart/Flutter, Kotlin Multiplatform), Security Champions program management, gamified learning strategies, completion tracking, and effectiveness measurement. The objective is to reduce developer-introduced vulnerabilities at the source by building security awareness and competency across all engineering teams, measured by a target reduction of 76% in developer-introduced vulnerabilities (based on Dr. Chen's Square benchmark).

## Competency Dimensions

| Dimension | Description | Proficiency Indicators |
|-----------|-------------|----------------------|
| Curriculum Design | Creating platform-specific secure coding training materials | Develops training modules for Kotlin, Swift, Dart, and KMP with real-world vulnerability examples; achieves ≥90% trainee comprehension on post-training assessments |
| Security Champions Program | Recruiting, training, and managing security advocates within engineering teams | Establishes Security Champions in 100% of engineering teams; Champions identify ≥30% of vulnerabilities before formal security review; retention rate ≥80% annually |
| Gamification & Engagement | Designing motivational learning experiences that drive participation | Achieves ≥85% course completion rate; CTF-style challenges with ≥50% participation; recognition program with quarterly awards |
| Effectiveness Measurement | Quantifying training impact on code quality and vulnerability rates | Tracks vulnerability density (vulns/KLOC) pre- and post-training; measures reduction in repeat findings; produces quarterly effectiveness reports |
| Developer Education Strategy | Aligning training with engineering workflows and tools | Integrates training into onboarding; provides just-in-time learning via IDE plugins; maintains training wiki with searchable remediation patterns |
| Completion Tracking | Managing training compliance and certification | 100% of engineers complete baseline training within 30 days of hire; annual refresher completion ≥95%; maintains training certification registry |

## Execution Guidance

### 1. Secure Coding Curriculum — Module Architecture

**Core Curriculum Structure:**

| Module | Target Audience | Duration | Format | Assessment |
|--------|----------------|----------|--------|------------|
| **SEC-101**: Security Fundamentals | All engineers | 2 hours | Self-paced video + quiz | Quiz ≥80% to pass |
| **SEC-201**: Mobile Security (Android) | Android devs | 4 hours | Workshop + CTF | CTF completion + code review |
| **SEC-202**: Mobile Security (iOS) | iOS devs | 4 hours | Workshop + CTF | CTF completion + code review |
| **SEC-203**: Cross-Platform Security | Flutter/KMP devs | 3 hours | Workshop + CTF | CTF completion + code review |
| **SEC-301**: API Security | Backend devs | 3 hours | Workshop | Vulnerable API challenge |
| **SEC-302**: Cryptography for Developers | All engineers | 2 hours | Self-paced + lab | Lab completion |
| **SEC-401**: Threat Modeling | Senior devs, architects | 4 hours | Facilitated workshop | Threat model deliverable |
| **SEC-402**: Secure Code Review | All engineers | 3 hours | Paired review sessions | Review accuracy assessment |

#### SEC-201: Mobile Security (Android) — Detailed Syllabus

```markdown
# SEC-201: Secure Coding for Android

## Module 1: Platform Security Model (30 min)
- Android sandbox and permission model
- SELinux enforcement and app domain confinement
- Play Integrity API and SafetyNet attestation
- Hardware-backed Keystore and StrongBox

## Module 2: Secure Data Storage (45 min)
- SharedPreferences → EncryptedSharedPreferences migration
- Room Database with SQLCipher encryption
- External storage dangers — scoped storage (Android 10+)
- Keychain-equivalent: Android Keystore System
- Hands-on: Encrypt sensitive data at rest

## Module 3: Secure Network Communication (45 min)
- Network Security Configuration (network_security_config.xml)
- Certificate pinning with OkHttp
- TLS configuration best practices
- Cleartext traffic prevention
- Hands-on: Implement certificate pinning with pin rotation

## Module 4: Authentication & Session (30 min)
- BiometricPrompt with CryptoObject binding
- OAuth 2.0 PKCE for mobile apps
- Token storage — EncryptedSharedPreferences vs Keystore
- Session management and token refresh
- Hands-on: Implement biometric authentication with cryptographic binding

## Module 5: WebView & Content Providers (30 min)
- WebView security: JS disabled, no file access, URL allowlisting
- ContentProvider permissions and URI permissions
- Intent security — explicit vs implicit, permission grants
- Deep link validation and App Links verification
- Hands-on: Secure WebView configuration audit

## Module 6: Code Hardening (30 min)
- ProGuard/R8 configuration for release builds
- Native library obfuscation and stripping
- Anti-tampering and root detection patterns
- Debug feature removal for release builds
- Hands-on: Configure R8 rules for production APK

## CTF Challenge (60 min)
Participants receive a deliberately vulnerable Android app and must:
1. Find and fix 5 hardcoded secrets
2. Implement certificate pinning
3. Encrypt local database
4. Fix exported ContentProvider vulnerability
5. Configure R8 obfuscation
```

#### SEC-202: Mobile Security (iOS) — Detailed Syllabus

```markdown
# SEC-202: Secure Coding for iOS

## Module 1: iOS Security Architecture (30 min)
- iOS sandbox and entitlements
- Secure Enclave and hardware key management
- App Transport Security (ATS) enforcement
- Code signing and provisioning profiles

## Module 2: Keychain & Secure Storage (45 min)
- Keychain Services API — access groups, accessibility attributes
- Secure Enclave key generation and usage
- CoreData encryption strategies
- UserDefaults dangers for sensitive data
- Hands-on: Store cryptographic keys in Secure Enclave-backed Keychain

## Module 3: Network Security (45 min)
- ATS configuration and exception management
- URLSession with certificate pinning
- Trust evaluation with SecTrust
- TLS 1.3 adoption
- Hands-on: Implement TLS certificate pinning with TrustKit

## Module 4: Authentication & Biometrics (30 min)
- LocalAuthentication framework (Face ID / Touch ID)
- CryptoTokenKit for hardware tokens
- Sign in with Apple implementation
- Keychain-based session management
- Hands-on: Biometric authentication with LAContext

## Module 5: WKWebView & Universal Links (30 min)
- WKWebView security model (no JS bridge to native by default)
- Content Security Policy for web content
- Universal Links configuration and validation
- Handoff security considerations
- Hands-on: Secure WKWebView configuration

## Module 6: App Hardening (30 min)
- Release build optimization and symbol stripping
- Anti-debugging (ptrace, sysctl)
- Jailbreak detection patterns
- Obfuscation strategies
- Hands-on: Implement jailbreak detection

## CTF Challenge (60 min)
Participants receive a deliberately vulnerable iOS app and must:
1. Move secrets from UserDefaults to Keychain
2. Implement ATS enforcement
3. Configure certificate pinning
4. Fix insecure Universal Links
5. Enable all release build hardening flags
```

### 2. Security Champions Program

**Program Structure:**

```
Security Champions Program
│
├── Program Lead: Li Wei Chen
│   └── Deputy: Sana Khoury (pen testing perspective)
│
├── Champions (1 per team, minimum)
│   ├── Android Team Champion
│   ├── iOS Team Champion
│   ├── Flutter Team Champion
│   ├── Backend API Champion
│   └── DevOps/Infrastructure Champion
│
└── Program Activities
    ├── Monthly Security Champions Meeting (1 hour)
    ├── Quarterly Security Workshop (half-day)
    ├── Weekly Security Tips (Slack #security-tips channel)
    ├── Ad-hoc Security Consultation (as needed)
    └── Annual Security Champions Retreat (2 days)
```

**Champion Responsibilities:**
1. **First-line security reviewer**: Review PRs for security issues before they reach formal security review
2. **Team security advocate**: Promote security best practices within their team
3. **Vulnerability triage**: Help prioritize and understand security findings for their team's code
4. **Training facilitator**: Deliver team-level secure coding sessions using provided materials
5. **Threat modeling participant**: Participate in threat modeling sessions for their team's features
6. **Security tool champion**: Be the team expert on SAST/DAST tools and help colleagues interpret results

**Champion Selection Criteria:**
- Minimum 1 year of engineering experience at the company
- Demonstrated interest in security (self-identified or nominated by team lead)
- Strong communication skills (must teach and advocate)
- Commitment to 4 hours/month for security activities
- Endorsement from team supervisor

**Champion Training Path:**
1. Complete all core curriculum modules (SEC-101 through SEC-402)
2. Attend Security Champions onboarding workshop (4 hours)
3. Shadow Sana Khoury on one penetration testing engagement
4. Complete first independent security code review (mentored)
5. Deliver one team-level secure coding session

**Champion Recognition:**
- Quarterly "Security Champion of the Quarter" award
- Annual bonus consideration for exceptional security contributions
- Conference attendance budget (Black Hat, DEF CON, OWASP Global AppSec)
- Public recognition in company-wide communications
- Career development track toward security engineering roles

### 3. Gamification Strategy

**Capture The Flag (CTF) Platform:**

| Challenge Category | Difficulty | Points | Example |
|-------------------|------------|--------|---------|
| **Crypto** | Easy | 100 | Identify weak encryption in code snippet |
| **Crypto** | Medium | 250 | Decrypt message with known-plaintext attack |
| **Web** | Easy | 100 | Find SQL injection in API endpoint |
| **Web** | Hard | 500 | Chain multiple vulns to achieve RCE |
| **Mobile** | Easy | 150 | Extract hardcoded API key from APK |
| **Mobile** | Medium | 300 | Bypass SSL pinning and intercept traffic |
| **Mobile** | Hard | 600 | Reverse engineer and patch native library |
| **Reverse Engineering** | Medium | 350 | Analyze obfuscated binary for logic flaw |
| **Forensics** | Easy | 100 | Analyze memory dump for leaked keys |
| **Supply Chain** | Medium | 400 | Identify typosquatted dependency |

**Leaderboard & Recognition:**

```markdown
# Security CTF Leaderboard — Q1 2026

| Rank | Engineer | Team | Points | Badges |
|------|----------|------|--------|--------|
| 🥇 | 1st | @engineer1 | Android | 1,850 | 🔐 Crypto Master, 📱 Mobile Ninja |
| 🥈 | 2nd | @engineer2 | iOS | 1,620 | 🛡️ Defense Expert |
| 🥉 | 3rd | @engineer3 | Backend | 1,480 | 🔍 Bug Hunter |

## Badges Earned This Quarter
- 🔐 Crypto Master: Complete all crypto challenges
- 📱 Mobile Ninja: Complete all mobile challenges
- 🛡️ Defense Expert: Submit 3+ vulnerability fixes
- 🔍 Bug Hunter: Find 5+ unique vulnerabilities
- 🏆 First Blood: First to solve a new challenge
- 🎯 Perfect Score: 100% on security assessment
```

**Additional Gamification Elements:**
- **Security Sprint Goals**: Each sprint includes at least one security-related story
- **Vulnerability Bounty**: Internal bounty program for engineers who find vulnerabilities in their own codebase before security review
- **Security Streaks**: Track consecutive weeks with zero security findings in PRs
- **Achievement Unlocks**: IDE plugin notifications when engineers write secure patterns (e.g., "🏆 You used EncryptedSharedPreferences — +10 security points!")

### 4. Completion Tracking & Certification

**Training Registry:**

```yaml
# security-training-registry.yml
engineers:
  - name: "Jane Doe"
    team: "Android"
    hire_date: "2025-06-15"
    training:
      SEC-101:
        completed: "2025-06-20"
        score: 92
        status: certified
      SEC-201:
        completed: "2025-07-10"
        score: 88
        status: certified
        ctf_completed: true
      SEC-302:
        completed: "2025-08-01"
        score: 95
        status: certified
      SEC-401:
        completed: "2025-09-15"
        deliverable_submitted: true
        status: certified
    annual_refresher:
      2026:
        due_date: "2026-06-20"
        status: pending

compliance:
  baseline_completion_rate: 96%  # Target: 100%
  annual_refresher_rate: 94%     # Target: ≥95%
  avg_assessment_score: 89%      # Target: ≥80%
```

**Automated Tracking:**

```yaml
# .github/workflows/training-compliance.yml
name: Security — Training Compliance Check
on:
  schedule:
    - cron: '0 9 1 * *'  # First of every month at 9 AM
  pull_request:
    paths: ['company/project/**']

jobs:
  check-compliance:
    runs-on: ubuntu-latest
    steps:
      - name: Check Training Compliance
        run: |
          # Check if all engineers on PR have completed baseline training
          # Query training registry for PR authors and reviewers
          # Block merge if baseline training not complete
```

**Effectiveness Measurement — Quarterly Report:**

| Metric | Q4 2025 | Q1 2026 | Target | Trend |
|--------|---------|---------|--------|-------|
| **Training Completion Rate** | 92% | 96% | 100% | 📈 |
| **Vulnerability Density (per KLOC)** | 2.3 | 1.8 | <1.0 | 📈 |
| **Repeat Finding Rate** | 34% | 22% | <10% | 📈 |
| **Mean Time to Remediate (P0)** | 18 hours | 12 hours | <8 hours | 📈 |
| **Security Champions Active** | 4 | 6 | 8 | 📈 |
| **CTF Participation Rate** | 45% | 58% | 75% | 📈 |
| **Developer-Introduced Vulns (reduction from baseline)** | -42% | -61% | -76% | 📈 |

### 5. Just-in-Time Learning — IDE Integration

**VS Code / Android Studio / Xcode Extensions:**

Provide inline security guidance when engineers write potentially vulnerable code:

```
⚠️ Security Warning: Using Cipher.getInstance("AES/ECB/PKCS5Padding")
AES in ECB mode is cryptographically insecure.

💡 Suggested fix:
  Cipher.getInstance("AES/GCM/NoPadding")

📖 Learn more: SEC-201 Module 3 (Network & Crypto)
   Internal wiki: security.company.com/encryption-guide

[Dismiss] [Fix Automatically] [Mark as False Positive]
```

**IDE Plugin Configuration:**
- Integrate Semgrep IDE plugin for real-time static analysis
- Configure security rule packs to highlight issues as you type
- Link each warning to relevant training module for just-in-time learning
- Track security warnings resolved vs. dismissed for effectiveness metrics

## Pipeline Integration

| Pipeline Stage | Application |
|----------------|-------------|
| **Stage 4** (Implementation Plan) | Secure coding training plan is part of the implementation plan; training schedule aligned with development timeline |
| **Stage 5** (Development) | Engineers apply secure coding practices learned in training; Security Champions provide first-line review on PRs; IDE plugins provide real-time guidance |
| **Stage 6** (Code Review) | Training effectiveness measured by reduction in developer-introduced vulnerabilities; repeat findings indicate training gaps that must be addressed |
| **Stage 10** (Release Readiness) | Training compliance report provided to CSO — confirms all engineers on the project have completed required training modules |

## Quality Standards

| Metric | Standard |
|--------|----------|
| **Baseline Training Completion** | 100% of engineers complete SEC-101 + platform-specific module within 30 days of hire |
| **Annual Refresher Completion** | ≥95% of engineers complete annual refresher training |
| **Assessment Pass Rate** | ≥80% score required on all training assessments |
| **Vulnerability Reduction** | 76% reduction in developer-introduced vulnerabilities from baseline (Dr. Chen's Square benchmark) |
| **Repeat Finding Rate** | <10% of findings are repeat vulnerabilities (same class found multiple times) |
| **Security Champions Coverage** | 100% of engineering teams have an active Security Champion |
| **CTF Participation** | ≥75% of engineers participate in quarterly CTF challenges |
| **Training Satisfaction** | ≥4.0/5.0 average rating on training effectiveness surveys |
