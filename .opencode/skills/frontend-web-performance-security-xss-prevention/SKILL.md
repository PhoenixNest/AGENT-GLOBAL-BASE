---
name: frontend-web-performance-security-xss-prevention
description: XSS prevention engineering — DOMPurify extension patterns, Content Security Policy refinement, nonce-based inline script management, and sanitization pipeline architecture. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for XSS-safe implementation and Stage 6 (Code Review) for security pattern validation. Trigger: xss prevention, dompurify, content security policy, nonce script, sanitization, cross-site scripting, csp refinement.
prerequisites:
  - frontend-web-performance-security-frontend-security

version: "1.0.0"
---

# XSS Prevention Engineering

**Category:** Frontend Engineering / Security
**Owner:** Senior Frontend Engineer (Elena Kim)

## Overview

This skill provides deep expertise in cross-site scripting (XSS) prevention at the frontend application layer, complementing the Frontend Chapter Lead's broader security posture with specialized focus on DOMPurify extension, Content Security Policy refinement, nonce-based inline script management, and sanitization pipeline architecture. XSS remains the most prevalent web application vulnerability (consistently #7 in OWASP Top 10) and is the primary attack vector against single-page applications where user-controlled data flows directly into the DOM. This skill ensures that every data flow from untrusted source to DOM insertion is secured through multiple, independently effective defense layers.

## Competency Dimensions

| Dimension                              | Description                                                                                            | Proficiency Indicators                                                                               |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **DOMPurify Extension**                | Custom hook development, configuration hardening, extension API usage for domain-specific sanitization | Custom sanitization rules for rich text, markdown, and data URI content; zero bypass vulnerabilities |
| **Content Security Policy Refinement** | Nonce-based CSP, hash-based allowlisting, violation analysis, policy optimization                      | Zero `unsafe-inline` in production; CSP violation analysis with < 5 minute triage time               |
| **Nonce-Based Inline Scripts**         | Server-side nonce generation, build-time nonce injection, CSP-compliant third-party integration        | All inline scripts use nonces; third-party scripts integrated without CSP relaxation                 |
| **Sanitization Pipeline Architecture** | Multi-stage input sanitization, output encoding, context-aware escaping                                | Every data flow traced from input to output; context-specific encoding (HTML, JS, URL, CSS)          |
| **XSS Vector Enumeration**             | Knowledge of all XSS variants (reflected, stored, DOM-based, mutation XSS, mXSS)                       | Penetration test coverage of all XSS vectors; mXSS-specific DOMPurify configuration                  |
| **Security Code Review**               | Systematic XSS vulnerability identification in PRs, pattern recognition for dangerous APIs             | Zero XSS vulnerabilities missed in code review; review checklist covering 15+ dangerous patterns     |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                       | Deliverable                           |
| ------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------- |
| **Stage 1** (Requirements)           | Map XSS requirements from SRD to frontend implementation needs                       | XSS threat model                      |
| **Stage 2** (Web Prototype + IDS)    | Document XSS constraints in IDS for components accepting user content                | Security notes in IDS                 |
| **Stage 3** (Architecture)           | Define sanitization pipeline architecture; register ADRs for DOMPurify configuration | Sanitization ADRs                     |
| **Stage 5** (Development)            | Implement sanitization pipeline, DOMPurify extension, CSP nonce management           | Production-hardened sanitization code |
| **Stage 6** (Code Review)            | Systematic XSS vector review across all data flows; validate DOMPurify test coverage | XSS section in DEFECT-REPORT.md       |
| **Stage 8** (Integrity Verification) | Verify SRD XSS controls are enforced; penetration test all data flows                | XSS verification report               |
| **Stage 10** (Release Readiness)     | Confirm security sign-off for XSS controls                                           | Security compliance contribution      |

## Quality Standards

| Metric                         | Target                                          | Enforcement                                                              |
| ------------------------------ | ----------------------------------------------- | ------------------------------------------------------------------------ |
| **XSS vectors blocked**        | 100% of known XSS vectors mitigated             | Test suite with 50+ XSS vectors; zero bypasses                           |
| **DOMPurify coverage**         | 100% of HTML sinks protected                    | Grep audit: zero `innerHTML`/`dangerouslySetInnerHTML` without DOMPurify |
| **CSP compliance**             | Zero `unsafe-inline` in production              | CSP header audit; Lighthouse check                                       |
| **Nonce usage**                | 100% of inline scripts use nonces or hashes     | HTML audit; CI check for inline scripts without nonce                    |
| **URL sanitization**           | 100% of user-provided URLs validated            | Code review; grep audit for `href={userInput}`                           |
| **Context encoding**           | Correct encoding for every data sink            | Code review against context encoding matrix                              |
| **DOM Clobbering protection**  | DOMPurify SANITIZE_DOM enabled on all instances | Configuration audit                                                      |
| **mXSS protection**            | DOMPurify tested against mutation XSS vectors   | Test suite includes mXSS vectors                                         |
| **Code review coverage**       | 100% of PRs reviewed for XSS patterns           | PR checklist; automated grep in CI                                       |
| **Sanitization test coverage** | ≥ 95% of sanitization functions tested          | Unit test coverage report                                                |
| **Third-party script risk**    | All third-party scripts reviewed for XSS risk   | Third-party security assessment                                          |
| **Security debt**              | Zero XSS defects older than 1 sprint            | Defect tracking with security tag                                        |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
