---
name: mobile-penetration-testing
description: Execute structured mobile penetration tests against Android and iOS applications — covering authentication bypass, insecure data storage, network interception, and runtime manipulation — and produce findings that map to MASVS controls and CVSS scores.
version: "1.0.0"
---

# Mobile Penetration Testing

| Competency               | Description                                                       | Quality Criteria                                                                                                                    |
| ------------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Authentication Bypass    | Testing for session fixation, token forgery, and biometric bypass | Tests brute force controls, token replay, and Frida-based biometric hook; documents successful bypass paths with reproduction steps |
| Insecure Storage Testing | Runtime verification of data-at-rest controls                     | Uses adb shell to inspect app data directory; checks SharedPreferences and SQLite for plaintext secrets in production builds        |
| Network Interception     | Man-in-the-middle testing via mitmproxy / Burp Suite              | Tests with and without certificate pinning bypass; verifies TLS version and cipher suite negotiation; captures API traffic          |
| Runtime Manipulation     | Frida-based dynamic analysis and code injection                   | Hooks security-critical functions; attempts to disable root/jailbreak detection; documents all successfully bypassed controls       |
| Pentest Report           | Structured penetration test report with CVSS-scored findings      | Report: Executive Summary, Methodology, Findings (CVSS score, MASVS ID, PoC steps, remediation), Remediation Tracking Table         |

## Execution Guidance

### Pentest Engagement Phases

| Phase        | Activities                                                | Deliverable                     |
| ------------ | --------------------------------------------------------- | ------------------------------- |
| Recon        | APK/IPA decompilation, component mapping, API enumeration | Attack surface map              |
| Static       | jadx/MobSF analysis, hardcoded secret search              | Static findings list            |
| Dynamic      | Runtime instrumentation, traffic interception             | Dynamic findings list           |
| Exploitation | Chaining vulnerabilities for impact demonstration         | PoC with severity justification |
| Reporting    | CVSS-scored findings, remediation recommendations         | Final pentest report            |

### CVSS Scoring Quick Reference

| CVSS Score | Severity | Mobile Context Example                                  |
| ---------- | -------- | ------------------------------------------------------- |
| 9.0–10.0   | Critical | Unauthenticated RCE via WebView JS bridge               |
| 7.0–8.9    | High     | Token stored in plaintext, extractable without root     |
| 4.0–6.9    | Medium   | Weak PIN brute-forceable within lock policy limits      |
| 0.1–3.9    | Low      | Debug flag active in release; no exploitable path found |

### Root/Jailbreak Detection Bypass

Test whether security controls depend solely on root/jailbreak detection (fragile baseline):

```javascript
// Frida script — bypass common root detection
Java.perform(function () {
  var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
  RootBeer.isRooted.implementation = function () {
    return false;
  };
});
```

If root detection is the only defence for a security control, classify the underlying vulnerability at its actual CVSS severity — not reduced for the detection layer.
