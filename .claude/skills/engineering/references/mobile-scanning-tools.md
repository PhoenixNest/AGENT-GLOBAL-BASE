---
name: mobile-scanning-tools
description: Operate and interpret output from mobile security scanning tools — MobSF, Drozer, Frida, apktool — to perform static and dynamic analysis of Android and iOS applications and translate findings into actionable remediation items for the Stage 6 Architecture & Conformance Review.
version: "1.0.0"
---

# Mobile Scanning Tools

| Competency      | Description                                                       | Quality Criteria                                                                                                               |
| --------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| MobSF           | Mobile Security Framework — automated static and dynamic analysis | Runs MobSF against APK/IPA; interprets CVSS scores; filters false positives; produces findings report with MASVS mapping       |
| Drozer          | Android component attack surface analysis                         | Enumerates exported components; tests for intent injection; verifies content provider access controls                          |
| Frida           | Dynamic instrumentation for runtime security analysis             | Hooks SSL certificate validation to detect pinning bypass; inspects runtime API calls for secrets exposure                     |
| apktool / jadx  | APK decompilation and source analysis                             | Decompiles APK; searches for hardcoded keys, endpoints, and debug flags; verifies ProGuard/R8 obfuscation is active            |
| Findings Report | Structured security report integrating all tool outputs           | Report maps every finding to a MASVS control ID with severity, evidence (tool output excerpt), and a concrete remediation step |

## Execution Guidance

### MobSF Static Analysis Workflow

1. Upload APK/IPA to MobSF and run full static analysis.
2. Review the security score breakdown — focus on Critical and High severity items.
3. For each finding, validate against the actual decompiled source (use jadx to confirm it is not a false positive).
4. Export findings as JSON; filter to confirmed vulnerabilities for inclusion in the Stage 6 report.

### Dynamic Analysis with Frida

```bash
# Attach Frida to target app process
frida -U -n com.example.app -l ssl-pinning-bypass.js

# Hook and log all file write operations
frida -U -n com.example.app -l file-monitor.js
```

Capture all network traffic through a proxy (mitmproxy / Burp Suite) after bypassing certificate pinning to identify unencrypted transmissions and missing certificate validation.

### Reporting Standard

Every finding must include:

| Field         | Content                                                     |
| ------------- | ----------------------------------------------------------- |
| Tool          | Which scanner identified it                                 |
| MASVS Control | e.g., MASVS-STORAGE-1 or MASVS-NETWORK-2                    |
| Severity      | Critical / High / Medium / Low                              |
| Evidence      | Screenshot or code excerpt from the tool output             |
| Remediation   | Specific code change or configuration fix, not vague advice |
