---
name: frontend-security
description: This skill establishes the frontend security engineering discipline that enforces the CSO's Security Requirements Document (SRD) at the application layer.
---

# Frontend Security

**Category:** Frontend Engineering / Security
**Owner:** Frontend Chapter Lead (Amira Voss)

## Overview

This skill establishes the frontend security engineering discipline that enforces the CSO's Security Requirements Document (SRD) at the application layer. It covers Content Security Policy implementation, cross-site scripting (XSS) prevention through DOMPurify and sanitization patterns, secure authentication flows including OAuth 2.0 PKCE, secure storage of sensitive data, and the security review protocols that feed into Stage 6 Code Review and Stage 8 Integrity Verification. Frontend security is the last line of defense before user data reaches the browser — and it must be treated with the same rigor as backend security controls.

## Competency Dimensions

| Dimension                   | Description                                                                             | Proficiency Indicators                                                                          |
| --------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Content Security Policy** | CSP header design, nonce generation, hash-based allowlisting, violation reporting       | Zero `unsafe-inline` in production; CSP violation monitoring with < 1% false positive rate      |
| **XSS Prevention**          | DOMPurify configuration, sanitization pipelines, template safety, innerHTML elimination | Zero `dangerouslySetInnerHTML` without DOMPurify; all user input sanitized before DOM insertion |
| **Secure Authentication**   | OAuth 2.0 PKCE, token lifecycle, secure storage, session management                     | PKCE flow with S256 code challenge; tokens never in localStorage; refresh token rotation        |
| **Secure Data Handling**    | Sensitive data in transit/at rest, PII masking, clipboard security, form autocomplete   | Zero PII in URLs, logs, or analytics; autocomplete attributes set correctly on all forms        |
| **Third-Party Risk**        | Subresource integrity, dependency auditing, supply chain security                       | All third-party scripts loaded with SRI hashes; `npm audit` clean; lockfile pinned              |
| **Security Testing**        | Automated security linting, CSP testing, XSS penetration testing                        | eslint-plugin-security integrated; CSP test suite; quarterly XSS pen test pass                  |

## Execution Guidance

### Content Security Policy — Production Implementation

**CSP is not optional.** It is the single most effective defense against XSS and must be implemented from Stage 2 prototype through Stage 10 release.

**Progressive CSP strategy** — start restrictive, loosen only with documented justification:

```
Report-Only Phase (Weeks 1-2)
  └─ Deploy Content-Security-Policy-Report-Only header
  └─ Monitor violation reports at /csp-violation endpoint
  └─ Identify all legitimate sources that need allowlisting
  └─ No blocking — just observation
       ↓
Enforcement Phase (Week 3+)
  └─ Switch to Content-Security-Policy header
  └─ All sources explicitly allowlisted
  └─ Violations logged and alerted
```

**Production CSP template** (adapt per application needs):

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{RANDOM}' https://cdn.example.com;
  style-src 'self' 'nonce-{RANDOM}';
  img-src 'self' data: https://cdn.example.com https://images.example.com;
  font-src 'self' https://fonts.example.com;
  connect-src 'self' https://api.example.com https://analytics.example.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  upgrade-insecure-requests;
  report-uri /csp-violation;
  report-to csp-endpoint
```

**Critical CSP rules:**

- **NEVER use `unsafe-inline`** for scripts or styles in production — if you must inline, use nonces or hashes
- **NEVER use `unsafe-eval`** — this defeats the entire purpose of CSP; if your framework requires it (some do in dev), strip it from production builds
- **`default-src 'self'`** is the baseline — every other directive inherits from this, so it must be restrictive
- **`object-src 'none'`** — Flash/Java plugins have no legitimate use case in modern web apps
- **`frame-src 'none'`** — unless you explicitly need iframes, block them entirely
- **`base-uri 'self'`** — prevents attackers from changing the base URL for relative links

**Nonce generation** (server-side, per request):

```js
// Express middleware example
const crypto = require('crypto');

function generateNonce(req, res, next) {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.nonce = nonce;
  res.setHeader(
    'Content-Security-Policy',
    `script-src 'self' 'nonce-${nonce}'; style-src 'self' 'nonce-${nonce}'`
  );
  next();
}
```

**CSP violation reporting endpoint:**

```js
app.post('/csp-violation', express.json({ type: 'application/csp-report' }), (req, res) => {
  const violation = req.body['csp-report'];
  // Log to monitoring system
  logger.warn('CSP Violation', {
    blockedURI: violation['blocked-uri'],
    violatedDirective: violation['violated-directive'],
    sourceFile: violation['source-file'],
    lineNumber: violation['line-number'],
    userAgent: req.headers['user-agent'],
  });
  // Alert if pattern suggests active attack (not just misconfiguration)
  if (isSuspiciousPattern(violation)) {
    securityTeam.alert(violation);
  }
  res.status(204).send(); // No content
});
```

### XSS Prevention — Defense in Depth

**The XSS prevention hierarchy** — multiple layers, each independently effective:

```
Layer 1: Framework Auto-Escaping (React, Vue auto-escape by default)
  ├─ ✅ Use framework templating for all user data
  ├─ ❌ NEVER bypass with dangerouslySetInnerHTML / v-html without sanitization
  └─ Exception: Rich text editors require explicit sanitization
       ↓
Layer 2: DOMPurify Sanitization (when HTML output is required)
  ├─ Configure with strict allowlist
  ├─ Strip all event handlers (onclick, onerror, onload, etc.)
  ├─ Strip javascript: URLs
  └─ Strip SVG script elements and event handlers
       ↓
Layer 3: Content Security Policy (catches what Layers 1-2 miss)
  ├─ Blocks inline script execution
  ├─ Blocks eval() execution
  └─ Reports violations for investigation
       ↓
Layer 4: HTTP-Only, Secure, SameSite Cookies (protects session tokens)
  ├─ Session cookies inaccessible to JavaScript
  ├─ Secure flag prevents transmission over HTTP
  └─ SameSite=Strict/Lax prevents CSRF
```

**DOMPurify configuration** — production settings:

```js
import DOMPurify from 'dompurify';

const SANITIZE_CONFIG = Object.freeze({
  ALLOWED_TAGS: [
    'p',
    'br',
    'strong',
    'em',
    'u',
    's',
    'blockquote',
    'code',
    'pre',
    'ul',
    'ol',
    'li',
    'a',
    'img',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'table',
    'thead',
    'tbody',
    'tr',
    'th',
    'td',
    'figure',
    'figcaption',
    'details',
    'summary',
    'del',
    'ins',
    'sub',
    'sup',
  ],
  ALLOWED_ATTR: [
    'href',
    'title',
    'alt',
    'src',
    'width',
    'height',
    'class',
    'id',
    'target',
    'rel',
    'colspan',
    'rowspan',
    'align',
    'valign',
  ],
  ALLOWED_URI_REGEXP:
    /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i,
  ADD_ATTR: ['rel'],
  ADD_DATA_ATTR: false, // Block all data-* attributes (can be vectors)
  FORBID_ATTR: ['style', 'onerror', 'onload', 'onclick', 'onmouseover', 'onfocus', 'onblur'],
  FORBID_TAGS: [
    'script',
    'style',
    'iframe',
    'object',
    'embed',
    'form',
    'input',
    'button',
    'textarea',
    'select',
  ],
  KEEP_CONTENT: true, // Strip tag but keep text content
  RETURN_DOM: false,
  RETURN_DOM_FRAGMENT: false,
  RETURN_TRUSTED_TYPE: false,
  WHOLE_DOCUMENT: false,
  SANITIZE_DOM: true, // Protect against DOM Clobbering
  SANITIZE_NAMED_PROPS: true, // Sanitize name attributes
});

function sanitizeUserHTML(html) {
  if (typeof html !== 'string') return '';
  return DOMPurify.sanitize(html, SANITIZE_CONFIG);
}
```

**Dangerous patterns to eliminate in code review:**

```tsx
// ❌ NEVER DO THIS
<div dangerouslySetInnerHTML={{ __html: userComment }} />
element.innerHTML = userInput
document.write(userInput)
new Function(userInput)
eval(userInput)
setTimeout(userInput, 1000)
setInterval(userInput, 1000)
<iframe src={userProvidedUrl} />
<a href={userProvidedUrl}>click</a>  // javascript: URL risk

// ✅ CORRECT
<div dangerouslySetInnerHTML={{ __html: sanitizeUserHTML(userComment) }} />
element.textContent = userInput // Use textContent, not innerHTML
// Avoid document.write entirely — use DOM APIs
// Avoid eval/Function/setTimeout with strings — pass function references
<iframe src={sanitizeUrl(userProvidedUrl)} sandbox="allow-scripts" />
<a href={sanitizeUrl(userProvidedUrl)} rel="noopener noreferrer">click</a>
```

**URL sanitization** — prevent `javascript:` and `data:` URL injection:

```js
function sanitizeUrl(url) {
  if (!url) return '';
  // Normalize and check protocol
  try {
    const parsed = new URL(url, window.location.origin);
    const allowedProtocols = ['http:', 'https:', 'mailto:', 'tel:'];
    if (!allowedProtocols.includes(parsed.protocol)) {
      console.warn(`Blocked URL with protocol: ${parsed.protocol}`);
      return '#';
    }
    return parsed.href;
  } catch {
    // Invalid URL — could be relative path, allow it
    return url;
  }
}
```

### Secure Authentication — OAuth 2.0 PKCE

**PKCE (Proof Key for Code Exchange) is mandatory for all SPAs.** The implicit flow is deprecated and must not be used.

**PKCE flow sequence:**

```
1. Client generates code_verifier (43-128 char random string)
   └─ crypto.getRandomValues() → base64url encode
2. Client derives code_challenge from code_verifier
   └─ SHA-256(code_verifier) → base64url encode
3. Client redirects to authorization server
   └─ /authorize?response_type=code&client_id=...&code_challenge=...&code_challenge_method=S256&redirect_uri=...&state=...
4. User authenticates and authorizes
5. Authorization server redirects back with authorization code
   └─ callback?code=AUTH_CODE&state=STATE
6. Client exchanges code for tokens
   └─ POST /token with: grant_type=authorization_code&code=AUTH_CODE&client_id=...&code_verifier=ORIGINAL_VERIFIER&redirect_uri=...
7. Authorization server validates code_verifier matches code_challenge and returns tokens
   └─ { access_token, refresh_token, id_token, expires_in }
```

**Token storage strategy:**

| Storage Method    | XSS Risk                | CSRF Risk       | Recommendation                               |
| ----------------- | ----------------------- | --------------- | -------------------------------------------- |
| `localStorage`    | ❌ Accessible to any JS | ✅ No CSRF risk | **NEVER** for tokens                         |
| `sessionStorage`  | ❌ Accessible to any JS | ✅ No CSRF risk | **NEVER** for tokens                         |
| HTTP-Only Cookie  | ✅ Inaccessible to JS   | ❌ CSRF risk    | **RECOMMENDED** (with SameSite + CSRF token) |
| Memory (variable) | ✅ Lost on refresh      | ✅ No CSRF risk | **Acceptable** for short-lived access tokens |

**Recommended approach: HTTP-Only cookies with refresh token rotation:**

```
Access Token:
  ├─ Stored in memory (JavaScript variable)
  ├─ Short-lived (5-15 minutes)
  └─ Sent in Authorization: Bearer header
       ↓
Refresh Token:
  ├─ Stored in HTTP-Only, Secure, SameSite=Strict cookie
  ├─ Long-lived (7-30 days)
  ├─ Rotated on each use (new refresh token issued)
  └─ Old refresh token invalidated immediately
       ↓
CSRF Protection:
  ├─ SameSite=Strict cookie attribute
  ├─ Custom X-CSRF-Token header for state-changing requests
  └─ Double-submit cookie pattern for forms
```

**PKCE implementation** (using `@auth0/auth0-spa-js` or similar):

```ts
import createAuth0Client from '@auth0/auth0-spa-js';

const auth0 = await createAuth0Client({
  domain: 'your-domain.auth0.com',
  client_id: 'your-client-id',
  authorizationParams: {
    redirect_uri: window.location.origin,
    audience: 'https://api.example.com',
    scope: 'openid profile email',
  },
  cacheLocation: 'memory', // NEVER 'localstorage'
  useRefreshTokens: true,
  useRefreshTokensFallback: false,
});

// Login — PKCE handled automatically
await auth0.loginWithRedirect();

// Get token — access token in memory only
const token = await auth0.getTokenSilently();
```

### Third-Party Security Controls

**Subresource Integrity (SRI)** — every third-party script must have an integrity hash:

```html
<script
  src="https://cdn.example.com/library.min.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous"
></script>
```

**Generate SRI hashes:**

```bash
curl -s https://cdn.example.com/library.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```

**Dependency security:**

- `npm audit` runs on every CI build — blocks on `high` or `critical` vulnerabilities
- Use `overrides` in `package.json` to force patched versions of transitive dependencies
- Pin exact versions in `package-lock.json` — never use `^` or `~` for production dependencies in the lockfile
- Quarterly dependency audit: remove unused packages, update to latest stable, verify no new vulnerabilities

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                           | Deliverable                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Stage 1** (Requirements)           | Review SRD for frontend-specific security requirements                                   | Security requirements mapping document                 |
| **Stage 2** (Web Prototype + IDS)    | Embed CSP headers in prototype; document security constraints in IDS                     | Prototype with security headers, security notes in IDS |
| **Stage 3** (Architecture)           | Define authentication architecture in UML; register ADRs for auth flow and token storage | Auth UML diagrams, security ADRs                       |
| **Stage 5** (Development)            | Implement CSP, DOMPurify, PKCE auth flow, secure token storage                           | Production-secure frontend codebase                    |
| **Stage 6** (Code Review)            | Security-focused code review: XSS vectors, CSP compliance, token handling                | Security section in DEFECT-REPORT.md                   |
| **Stage 8** (Integrity Verification) | Verify SRD enforcement at frontend layer; validate CSP, auth, and XSS controls           | Frontend security verification report                  |
| **Stage 10** (Release Readiness)     | Confirm security sign-off (Stage 10, Item 4: "SRD enforced, OWASP MASVS compliant")      | Security sign-off contribution                         |

## Quality Standards

| Metric                            | Target                                                | Enforcement                                   |
| --------------------------------- | ----------------------------------------------------- | --------------------------------------------- |
| **CSP compliance**                | Zero `unsafe-inline` or `unsafe-eval` in production   | CSP header audit; Lighthouse `csp-xss` audit  |
| **XSS vectors**                   | Zero un-sanitized DOM insertions                      | `eslint-plugin-security` + manual code review |
| **dangerouslySetInnerHTML usage** | 100% wrapped with DOMPurify                           | Grep audit; CI blocks on unprotected usage    |
| **Token storage**                 | Zero tokens in localStorage/sessionStorage            | Code review; automated grep in CI             |
| **PKCE implementation**           | 100% OAuth flows use PKCE with S256                   | Architecture review; auth flow test           |
| **Cookie security**               | 100% cookies have Secure + SameSite + HTTP-Only flags | Response header audit                         |
| **SRI coverage**                  | 100% third-party scripts have integrity attribute     | HTML audit; Lighthouse `sri` audit            |
| **Dependency vulnerabilities**    | Zero high/critical in production                      | `npm audit --production` in CI                |
| **Form security**                 | All forms have correct autocomplete, CSRF protection  | Manual audit; automated form attribute check  |
| **CSP violation rate**            | < 1% of page views                                    | Violation endpoint monitoring                 |
