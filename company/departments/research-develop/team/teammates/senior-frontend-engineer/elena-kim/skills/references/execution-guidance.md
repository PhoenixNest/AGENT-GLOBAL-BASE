---
version: "1.0.0"
---

-------------------------- | ------------------------------- | ---------------------------------- |
| Script is static (never changes) | ✅ Suitable | ❌ Overkill |
| Script is dynamic (per-request) | ❌ Not possible | ✅ Required |
| Multiple inline scripts | ❌ Each needs separate hash | ✅ Single nonce covers all |
| Build-time generation | ✅ Hash computed during build | ❌ Nonce must be runtime |
| CDN-cached HTML | ✅ Hash works with cached pages | ❌ Nonce requires edge computation |

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
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;");
}

// HTML attribute context — additionally encode spaces
function encodeHTMLAttribute(str) {
  return encodeHTML(str).replace(/\s/g, "&#x20;");
}

// JavaScript string context
function encodeJSString(str) {
  return str
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'")
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r")
    .replace(/<\/script>/gi, "<\\/script>");
}

// URL context
function encodeURL(str) {
  // Only encode the value, not the entire URL
  return encodeURIComponent(str);
}

// CSS value context
function encodeCSSValue(str) {
  return str.replace(/[\\()]/g, "\\$&");
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
