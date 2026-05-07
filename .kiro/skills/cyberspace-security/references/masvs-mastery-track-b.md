---
name: masvs-mastery-track-b
description: OWASP MASVS Track B (MASVS-NETWORK, MASVS-PLATFORM, MASVS-CODE) mastery — audit mobile applications for network security controls, platform API misuse, and code-level vulnerability patterns, producing Stage 3 ADR input and Stage 6 conformance findings.
version: "1.0.0"
---

# MASVS Mastery Track B

| Competency         | Description                                                               | Quality Criteria                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MASVS-NETWORK      | TLS configuration, certificate pinning, and API security                  | Verifies TLS 1.2+ enforcement; confirms certificate pinning with backup pins; identifies cleartext HTTP usage and missing HSTS headers                   |
| MASVS-PLATFORM     | Platform API misuse — WebView, IPC, clipboard, intent handling            | Audits WebView for `setJavaScriptEnabled(true)` + `addJavascriptInterface`; checks exported components; verifies clipboard auto-clear for sensitive data |
| MASVS-CODE         | Binary protections — obfuscation, anti-tampering, anti-debugging          | Confirms ProGuard/R8 is enabled; verifies certificate verification is not disabled; identifies debug flags in release builds                             |
| ADR Security Input | Translating MASVS-B findings into Stage 3 security architecture decisions | Produces ADR security annexes that cite specific MASVS-B controls as the rationale for chosen security patterns                                          |

## Execution Guidance

### MASVS-NETWORK Checklist

| Control                 | Check Method                                                       | Pass Condition                             |
| ----------------------- | ------------------------------------------------------------------ | ------------------------------------------ |
| TLS version             | SSL Labs / local proxy inspection                                  | TLS 1.2 minimum; TLS 1.3 preferred         |
| Certificate pinning     | Frida SSL pinning bypass script — should fail if pinning is active | Pinning active with backup pins configured |
| Cleartext traffic       | `android:usesCleartextTraffic` in AndroidManifest.xml              | Set to `false` in release build            |
| Network Security Config | `network-security-config.xml` review                               | No `<debug-overrides>` in release config   |

### MASVS-PLATFORM: WebView Security

WebViews combining `setJavaScriptEnabled(true)` with `addJavascriptInterface` create XSS-to-native code execution paths — always Critical severity. Required remediations:

1. Remove `addJavascriptInterface` unless absolutely necessary; if required, annotate with `@JavascriptInterface` only on explicitly intended methods.
2. Load only trusted URLs; validate scheme (`https://`) before loading.
3. Disable file access: `setAllowFileAccess(false)`.

### Stage 3 ADR Security Input Format

When producing ADR security annexes, use the following structure:

```markdown
### Security Annex — MASVS-B Controls

| Control          | Decision                     | Rationale                                |
| ---------------- | ---------------------------- | ---------------------------------------- |
| MASVS-NETWORK-1  | Enforce TLS 1.3 with pinning | Prevents MITM on sensitive API endpoints |
| MASVS-PLATFORM-2 | Disable WebView JS interface | Eliminates XSS-to-native attack surface  |
```
