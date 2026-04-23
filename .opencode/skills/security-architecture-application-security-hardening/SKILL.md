---
name: security-architecture-application-security-hardening
description: "Security skill: Application Security Hardening"
---

# Application Security Hardening

## Purpose

Protect mobile applications from reverse engineering, tampering, and runtime attacks through multi-layered defense strategies. Implement security controls that detect and respond to threats while maintaining app performance and user experience.

## Core Protection Layers

### 1. Code Obfuscation

**iOS Obfuscation:**

- Symbol stripping and name mangling
- Control flow obfuscation
- String encryption
- Dead code injection
- Swift/Objective-C interop obfuscation

**Android Obfuscation:**

- ProGuard/R8 configuration
- DexGuard for advanced protection
- Native code obfuscation (C/C++)
- Resource obfuscation
- Class encryption

### 2. Anti-Tampering Controls

**Integrity Verification:**

- Code signature validation
- Checksum verification of critical code
- Resource integrity checks
- Debug detection
- Emulator/simulator detection

**Tamper Response:**

- Graceful degradation
- Feature disabling
- Data wiping
- Server-side notification
- Crash with obfuscated error

### 3. Root/Jailbreak Detection

**Detection Techniques:**

- File system checks (Cydia, Magisk, su binary)
- API availability checks
- Sandbox integrity verification
- System property inspection
- Known jailbreak/root app detection

**Response Strategy:**

- Risk-based approach (warn vs. block)
- Server-side device trust scoring
- Conditional feature access
- Enhanced monitoring for rooted devices

### 4. Runtime Application Self-Protection (RASP)

**Runtime Monitoring:**

- Method hooking detection (Frida, Xposed)
- Debugger attachment detection
- Memory manipulation detection
- SSL pinning bypass detection
- Screen recording/screenshot detection

**Active Defense:**

- Anti-debugging techniques
- Anti-instrumentation
- Environment validation
- Behavioral anomaly detection

### 5. Network Security Hardening

**Certificate Pinning:**

- Public key pinning (preferred)
- Certificate pinning
- Pin backup strategy
- Pin rotation process
- Pinning failure handling

**API Protection:**

- Request/response encryption
- API key obfuscation
- Token binding
- Replay attack prevention
- Man-in-the-middle detection

## Implementation Strategy

### Phase 1: Threat Assessment

1. Identify high-value assets
2. Determine threat actors and motivations
3. Assess attack vectors
4. Define protection priorities
5. Establish acceptable risk levels

### Phase 2: Protection Selection

1. Choose obfuscation tools
2. Select anti-tampering techniques
3. Define detection vs. prevention balance
4. Plan performance impact mitigation
5. Design fallback strategies

### Phase 3: Implementation

1. Integrate protection tools into build pipeline
2. Implement runtime checks
3. Add server-side validation
4. Configure monitoring and alerting
5. Test protection effectiveness

### Phase 4: Validation

1. Penetration testing
2. Reverse engineering attempts
3. Performance benchmarking
4. False positive analysis
5. User experience validation

## Tools and Technologies

**iOS Protection:**

- iXGuard, Arxan, Promon SHIELD
- Custom LLVM obfuscation passes
- Swift obfuscation techniques
- Native code protection

**Android Protection:**

- DexGuard, Guardsquare, Arxan
- ProGuard/R8 optimization
- Native library protection (UPX, custom packers)
- SafetyNet Attestation API

**Cross-Platform:**

- TrustKit for certificate pinning
- Custom RASP frameworks
- Threat intelligence integration
- Device fingerprinting

## Collaboration Requirements

**With CTO:** Integrate protection into CI/CD pipeline, balance security with development velocity

**With Development Teams:** Provide implementation guidance, review security-critical code, minimize false positives

**With QA:** Define security testing requirements, validate protection effectiveness

## Key Deliverables

1. **Protection Strategy Document** — comprehensive hardening plan
2. **Implementation Guide** — step-by-step integration instructions
3. **Threat Response Playbook** — incident response procedures
4. **Performance Impact Report** — benchmarking results

## Success Metrics

- 90%+ reduction in successful reverse engineering attempts
- Zero critical tampering incidents in production
- <5% performance overhead from protection measures
- <0.1% false positive rate for threat detection
