---
name: security-architecture-mobile-security-architecture
description: Mobile security architecture for iOS and Android — Secure Enclave, Keychain, Android Keystore, SafetyNet, ATS, certificate pinning, encryption, biometric authentication, OWASP MASVS compliance. Owned by Dr. Sarah Chen (CSO). Use during Stage 1 (Requirements) for SRD authoring and Stage 3 (UML Engineering) for security architecture ADRs. Trigger: mobile security architecture, Secure Enclave, Keychain, Android Keystore, SafetyNet, ATS, certificate pinning, biometric auth, MASVS compliance, platform security.
prerequisites:
  - security-overview

version: "1.0.0"
---

# Mobile Security Architecture

## Purpose

Design comprehensive security architectures for mobile applications that leverage platform-specific security features while maintaining cross-platform consistency. Balance security rigor with user experience and performance constraints inherent to mobile platforms.

## Core Responsibilities

### 1. Platform Security Model Expertise

**iOS Security Architecture:**

- Secure Enclave integration for cryptographic operations
- Keychain Services for credential storage
- App Transport Security (ATS) configuration
- Code signing and provisioning profiles
- Data Protection API (file encryption classes)
- Biometric authentication (Face ID, Touch ID)
- App Sandbox and entitlements management

**Android Security Architecture:**

- Hardware-backed Keystore for key management
- SafetyNet Attestation API for device integrity
- SELinux policy enforcement
- Android Keystore System
- Biometric authentication (BiometricPrompt API)
- App signing and Play App Signing
- Scoped storage and permission models

### 2. Cryptographic Implementation

**Encryption Standards:**

- End-to-end encryption design for sensitive data
- At-rest encryption using platform APIs
- In-transit encryption (TLS 1.3, certificate pinning)
- Key derivation and rotation strategies
- Secure random number generation

**Implementation Patterns:**

- AES-256-GCM for symmetric encryption
- RSA-4096 or ECDSA P-256 for asymmetric operations
- PBKDF2/Argon2 for password-based key derivation
- Perfect forward secrecy for communication protocols

### 3. Secure Data Storage

**Storage Security Layers:**

- Encrypted databases (SQLCipher, Realm encryption)
- Secure file storage with Data Protection API (iOS) or EncryptedFile (Android)
- Keychain/Keystore for credentials and tokens
- Memory protection for sensitive data in RAM
- Secure deletion and data lifecycle management

**Anti-Patterns to Prevent:**

- Storing secrets in SharedPreferences/UserDefaults
- Hardcoded API keys or credentials
- Logging sensitive information
- Insecure backup configurations

### 4. Authentication & Authorization

**Authentication Mechanisms:**

- OAuth 2.0 / OpenID Connect implementation
- Biometric authentication with fallback strategies
- Multi-factor authentication (MFA) flows
- Session management and token refresh
- Certificate-based authentication

**Authorization Patterns:**

- JWT validation and claims verification
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- API authorization headers and token handling

### 5. Network Security

**Secure Communication:**

- TLS 1.3 enforcement
- Certificate pinning (public key pinning preferred)
- Certificate transparency validation
- Network Security Configuration (Android)
- App Transport Security (iOS)

**API Security:**

- Request signing and verification
- Rate limiting and throttling
- API key rotation strategies
- Secure WebSocket connections

## Security Architecture Review Process

### Phase 1: Threat Modeling

1. Identify assets (user data, credentials, business logic)
2. Map attack surface (network, local storage, IPC)
3. Enumerate threats (STRIDE methodology)
4. Assess risk severity (CVSS scoring)
5. Define security requirements

### Phase 2: Architecture Design

1. Select platform security features
2. Design encryption strategy
3. Define authentication flows
4. Establish secure storage patterns
5. Document security controls

### Phase 3: Implementation Guidance

1. Provide code examples and patterns
2. Define security testing requirements
3. Establish security review checkpoints
4. Create security documentation

### Phase 4: Validation

1. Security architecture review
2. Threat model validation
3. Penetration testing coordination
4. Compliance verification (OWASP MASVS)

## Collaboration Points

**With CTO (Dr. Nakamura):**

- Integrate security architecture into overall system design
- Review architecture decision records (ADRs) for security implications
- Ensure security patterns align with development velocity

**With CIO (Dr. Mehta):**

- Evaluate security implications of emerging technologies
- Assess vendor security capabilities
- Align security architecture with infrastructure strategy

**With Development Teams:**

- Provide security implementation guidance
- Review security-critical code
- Conduct security training and knowledge transfer

## Key Deliverables

1. **Security Architecture Documents** — comprehensive security design covering all layers
2. **Threat Models** — STRIDE-based threat analysis with mitigation strategies
3. **Security Implementation Guides** — platform-specific security patterns and code examples
4. **Security Review Reports** — assessment of architecture against OWASP MASVS and industry standards

## Success Metrics

- Zero critical security vulnerabilities in production
- 100% of sensitive data encrypted at rest and in transit
- All authentication flows implement MFA
- Security architecture review completed before feature launch
- Compliance with OWASP MASVS Level 2 or higher
