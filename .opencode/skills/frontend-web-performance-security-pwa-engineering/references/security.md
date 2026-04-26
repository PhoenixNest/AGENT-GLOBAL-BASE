# Security

## Security

### PWA Security Checklist

| Security Control               | Implementation                                           | Priority |
| ------------------------------ | -------------------------------------------------------- | -------- |
| **HTTPS Only**                 | HSTS header, redirect HTTP to HTTPS                      | P0       |
| **Content Security Policy**    | CSP header restricting resource sources                  | P0       |
| **Subresource Integrity**      | SRI hashes for external scripts                          | P1       |
| **X-Frame-Options**            | Prevent clickjacking via SAMEORIGIN                      | P1       |
| **X-Content-Type-Options**     | Prevent MIME sniffing with nosniff                       | P1       |
| **Referrer-Policy**            | Limit referrer info with strict-origin-when-cross-origin | P2       |
| **Permissions-Policy**         | Restrict browser features                                | P2       |
| **Service Worker Scope**       | Limit SW scope to minimum required                       | P1       |
| **No Sensitive Data in Cache** | Never cache authentication tokens, PII                   | P0       |

### Content Security Policy for PWA

```html
<meta
  http-equiv="Content-Security-Policy"
  content="
    default-src 'self';
    script-src 'self' 'wasm-unsafe-eval';
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: blob: https:;
    font-src 'self' https://fonts.gstatic.com;
    connect-src 'self' https://api.weather.example.com;
    media-src 'self';
    object-src 'none';
    frame-src 'none';
    worker-src 'self';
    manifest-src 'self';
    base-uri 'self';
    form-action 'self';
    upgrade-insecure-requests;
"
/>
```

---
