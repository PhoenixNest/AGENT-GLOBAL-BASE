---
name: web-application-security
description: "Assess web applications and APIs against OWASP Top 10 (2021) and OWASP API Top 10; design WAF rules, conduct manual secure code review, and produce code-level remediation guidance for all identified vulnerabilities."
version: "1.0.0"
---

# Web Application Security

| Competency                      | Description                                                  | Quality Criteria                                                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OWASP Top 10 (2021) Mastery     | Deep understanding of all 10 web application risk categories | Identifies every OWASP Top 10 category in code review; produces remediation guidance that eliminates entire classes of vulnerabilities; tracks OWASP 2021 changes from 2017 edition    |
| API Security (OWASP API Top 10) | Specialized knowledge of API-specific attack vectors         | Designs API security controls for all API1:2023 through API10:2023 categories; implements BOLA/BFLA detection; secures GraphQL endpoints                                               |
| WAF Engineering                 | Designing and tuning Web Application Firewall rules          | Writes custom ModSecurity/Cloudflare WAF rules with <1% false positive rate; implements virtual patching for zero-day vulnerabilities; tunes WAF to block OWASP Top 10 attack patterns |
| Secure Code Review              | Manual and automated review of backend source code           | Reviews 500+ LOC/hour with ≥90% vulnerability detection rate; identifies business logic flaws that automated tools miss; produces actionable findings with code-level remediation      |
| Authentication Bypass Detection | Identifying and exploiting authentication weaknesses         | Discovers authentication bypass vectors in OAuth 2.0, JWT, session management; tests for JWT algorithm confusion, signature stripping, token replay                                    |
| Threat Modeling for APIs        | Systematic identification of API attack surfaces             | Produces STRIDE-based threat models for all API endpoints; identifies trust boundary violations; maps data flow from mobile client through API to database                             |

## Execution Guidance

### 1. OWASP Top 10 (2021) — Assessment & Remediation

| Rank    | Category                           | Mobile Backend Relevance                       | Key Controls                                                                                               |
| ------- | ---------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **A01** | Broken Access Control              | **CRITICAL** — APIs are primary attack surface | Enforce authorization on every endpoint; implement RBAC/ABAC; deny by default; log access control failures |
| **A02** | Cryptographic Failures             | **CRITICAL** — Data in transit/storage         | TLS 1.2+ everywhere; AES-256-GCM for data at rest; proper key management; no sensitive data in logs        |
| **A03** | Injection                          | **HIGH** — SQL, NoSQL, command injection       | Parameterized queries; input validation; ORM usage; WAF rules for SQLi patterns                            |
| **A04** | Insecure Design                    | **HIGH** — Architecture-level flaws            | Threat modeling; secure design patterns; abuse case modeling; reference architectures                      |
| **A05** | Security Misconfiguration          | **HIGH** — Cloud and server configs            | Hardened baselines; automated config scanning; disable verbose errors; remove default accounts             |
| **A06** | Vulnerable Components              | **HIGH** — Dependency management               | SBOM; automated dependency scanning; patch SLAs; component inventory                                       |
| **A07** | Identification & Auth Failures     | **CRITICAL** — Mobile auth flows               | MFA; rate limiting; credential stuffing protection; secure session management; OAuth 2.0 PKCE              |
| **A08** | Software & Data Integrity Failures | **HIGH** — CI/CD and update integrity          | Code signing; SBOM verification; secure update mechanisms; integrity checks                                |
| **A09** | Security Logging & Monitoring      | **MEDIUM** — Detection capability              | Structured logging; SIEM integration; alerting on security events; log integrity protection                |
| **A10** | Server-Side Request Forgery        | **MEDIUM** — Mobile callback/webhook URLs      | URL allowlisting; disable HTTP redirects; validate all user-supplied URLs                                  |

#### A01: Broken Access Control — Deep Dive

**Most Common API Access Control Failures:**

1. **IDOR (Insecure Direct Object Reference)**: `GET /api/users/{userId}/transactions` — user can change `userId` to access others' data
2. **Missing Function-Level Access Control**: Admin endpoints accessible to regular users
3. **Privilege Escalation via JWT**: Modifying `role` claim in JWT token

**Detection Methodology:**

```bash
# Automated IDOR detection with Nuclei
nuclei -t nuclei-templates/idor/ -u https://api.example.com \
  -H "Authorization: Bearer $USER_TOKEN" \
  -var user_id=12345 -var target_id=67890

# Manual testing workflow:
# 1. Create two test accounts (User A, User B)
# 2. Authenticate as User A, capture all API requests
# 3. Replay User A's requests, substituting User B's resource IDs
# 4. Verify server returns 403, not User B's data
```

**Remediation Pattern — Authorization Middleware:**

```kotlin
// Spring Boot — Authorization middleware
@Component
class ResourceAuthorizationFilter(
    private val authService: AuthService,
    private val resourceOwnerService: ResourceOwnerService
) : OncePerRequestFilter() {

    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain
    ) {
        val userId = request.pathVariables["userId"]
        val authenticatedUser = authService.getCurrentUser(request)

        if (userId != null && !resourceOwnerService.isOwner(authenticatedUser.id, userId)) {
            response.status = HttpStatus.FORBIDDEN.value()
            response.writer.write("{\"error\": \"access_denied\"}")
            return
        }

        filterChain.doFilter(request, response)
    }
}
```

#### A02: Cryptographic Failures — Mobile Backend Focus

**Critical Checks:**

- TLS termination happens at load balancer; verify backend-to-backend communication is also encrypted
- API keys and secrets are never logged (implement request/response log scrubbing)
- Database encryption at rest (AES-256) with separate key management (KMS)
- Password hashing uses bcrypt (cost ≥ 12), scrypt, or Argon2id — never MD5, SHA1, or unsalted hashes
- JWT signing uses RS256 or ES256 — never HS256 with a weak secret

#### A07: Identification & Authentication Failures

**Mobile-Specific Auth Flow Security:**

```
Mobile App                    Backend API                    Auth Provider
    │                              │                              │
    │── POST /auth/login ─────────>│                              │
    │   {email, password}          │                              │
    │                              │── Verify credentials ───────>│
    │                              │<── Auth result ──────────────│
    │<── 200 {access_token,        │                              │
    │     refresh_token}           │                              │
    │                              │                              │
    │── POST /api/resource ───────>│                              │
    │   {Authorization: Bearer}    │── Validate JWT signature     │
    │                              │── Check expiration           │
    │                              │── Verify scope/claims        │
    │<── 200 {resource data}       │                              │
```

**Security Controls at Each Step:**

1. **Login endpoint**: Rate limiting (5 attempts/min/IP), account lockout (10 attempts/15min), CAPTCHA after 3 failures
2. **Token generation**: JWT with RS256, 15-min access token expiry, 7-day refresh token expiry, refresh token rotation
3. **Token validation**: Signature verification, expiration check, issuer validation, audience validation, revocation check
4. **Refresh token rotation**: Each refresh invalidates the previous token; detects token theft

### 2. OWASP API Security Top 10 (2023)

| Rank      | Category                                        | Description                              | Mobile Impact                                        |
| --------- | ----------------------------------------------- | ---------------------------------------- | ---------------------------------------------------- |
| **API1**  | Broken Object Level Authorization               | IDOR — accessing other users' resources  | HIGH — Mobile apps expose resource IDs in URLs       |
| **API2**  | Broken Authentication                           | Credential stuffing, weak token security | CRITICAL — Mobile auth tokens are high-value targets |
| **API3**  | Broken Object Property Level Auth               | Mass assignment, excessive data exposure | HIGH — Mobile APIs often over-respond with data      |
| **API4**  | Unrestricted Resource Consumption               | DoS, rate limiting bypass                | MEDIUM — Mobile apps can be weaponized for DDoS      |
| **API5**  | Broken Function Level Authorization             | Vertical privilege escalation            | HIGH — Admin APIs accessible from mobile             |
| **API6**  | Unrestricted Access to Sensitive Business Flows | Bot abuse, scraping                      | MEDIUM — Mobile API endpoints can be scraped         |
| **API7**  | Server Side Request Forgery                     | SSRF via user-supplied URLs              | MEDIUM — Webhook/callback URLs                       |
| **API8**  | Security Misconfiguration                       | Missing security headers, CORS misconfig | HIGH — CORS can expose APIs to unauthorized origins  |
| **API9**  | Improper Inventory Management                   | Shadow APIs, deprecated endpoints        | HIGH — Old API versions left active                  |
| **API10** | Unsafe Consumption of APIs                      | Trusting third-party API responses       | MEDIUM — Mobile SDKs consuming external APIs         |

#### API3: Broken Object Property Level Authorization — Mass Assignment

**Vulnerability:** API accepts and processes object properties that the client should not control.

```json
// Malicious request — user attempts privilege escalation
PUT /api/users/me
{
  "name": "Attacker",
  "email": "attacker@example.com",
  "role": "admin",           // ← Should not be user-controllable
  "isVerified": true,        // ← Should not be user-controllable
  "accountBalance": 999999   // ← Should not be user-controllable
}
```

**Remediation — DTO Pattern:**

```kotlin
// Kotlin — Use DTOs to control what properties are accepted
data class UserUpdateRequest(
    val name: String?,
    val email: String?,
    val avatarUrl: String?
    // Note: role, isVerified, accountBalance are NOT in the DTO
)

@PostMapping("/api/users/me")
fun updateUser(
    @RequestBody request: UserUpdateRequest,
    authentication: Authentication
): UserResponse {
    val user = userService.getCurrentUser(authentication)
    request.name?.let { user.name = it }
    request.email?.let { user.email = it }
    request.avatarUrl?.let { user.avatarUrl = it }
    return userService.save(user).toResponse()
}
```

#### API8: Security Misconfiguration — CORS

**Dangerous CORS Configuration:**

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Credentials: true
```

**Secure CORS Configuration:**

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 3600
Access-Control-Allow-Credentials: true
```

### 3. WAF Engineering

**ModSecurity Rule Engine — Custom Rules for Mobile API Protection:**

```apache
# OWASP CRS — Custom rules for mobile API
# Rule 1: Block requests with suspicious JWT manipulation
SecRule ARGS:token "@rx (eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*)" \
    "id:10001,\
    phase:2,\
    deny,\
    status:403,\
    msg:'JWT token in URL parameter detected — possible token manipulation',\
    tag:'API_SECURITY',\
    log"

# Rule 2: Block IDOR patterns (numeric ID substitution)
SecRule REQUEST_URI "@rx /api/users/\d+/(transactions|profile|settings)" \
    "id:10002,\
    phase:1,\
    pass,\
    nolog,\
    setvar:'tx.idor_check=1'"

SecRule &TX:IDOR_CHECK "@eq 1" \
    "id:10003,\
    phase:2,\
    chain,\
    deny,\
    status:403,\
    msg:'Potential IDOR attempt — user accessing another user\'s resource'"
    SecRule REMOTE_USER "@streq %{MATCHED_VAR}" "!chain"
    SecRule TX:RESOURCE_OWNER_ID "!@streq %{REMOTE_USER}"

# Rule 3: Rate limiting per IP per endpoint
SecRule IP:REQUEST_RATE "@gt 100" \
    "id:10004,\
    phase:1,\
    deny,\
    status:429,\
    msg:'Rate limit exceeded',\
    setvar:'ip.request_rate=0',\
    expirevar:'ip.request_rate=60'"

SecRule REQUEST_URI "@beginsWith /api/" \
    "id:10005,\
    phase:1,\
    pass,\
    nolog,\
    setvar:'ip.request_rate=+1'"

# Rule 4: Block mass assignment attempts
SecRule REQUEST_BODY "@rx (role|isAdmin|isVerified|accountBalance)" \
    "id:10006,\
    phase:2,\
    deny,\
    status:403,\
    msg:'Attempted mass assignment of restricted property',\
    tag:'API_SECURITY'"
```

**WAF Tuning Process:**

1. Deploy WAF in **Detection Mode** (log only, no blocking) for 2 weeks
2. Analyze logs to identify false positive patterns
3. Create whitelist rules for legitimate traffic patterns
4. Switch to **Prevention Mode** incrementally — enable one rule category at a time
5. Monitor false positive rate; target <1% after tuning
6. Implement virtual patching for zero-day vulnerabilities within 24 hours of disclosure

### 4. Secure Code Review — Backend Services

**Review Checklist per OWASP Top 10:**

| Category                      | What to Look For                | Code Patterns                                                     |
| ----------------------------- | ------------------------------- | ----------------------------------------------------------------- |
| **A01 Access Control**        | Missing authorization checks    | Endpoints without `@PreAuthorize`, `@Secured`, or middleware auth |
| **A02 Crypto**                | Weak algorithms, hardcoded keys | `MD5`, `SHA1`, `DES`, hardcoded secrets, missing TLS              |
| **A03 Injection**             | Unparameterized queries         | String concatenation in SQL, `eval()`, `exec()`                   |
| **A04 Insecure Design**       | Missing security controls       | No rate limiting, no input validation, no audit logging           |
| **A05 Misconfiguration**      | Default configs, verbose errors | Stack traces in responses, default passwords, debug mode          |
| **A06 Vulnerable Components** | Outdated dependencies           | `package-lock.json` / `pom.xml` with known CVEs                   |
| **A07 Auth Failures**         | Weak auth flows                 | No MFA, no rate limiting on login, predictable tokens             |
| **A08 Integrity**             | Unsigned artifacts, no SBOM     | Missing code signing, no dependency verification                  |
| **A09 Logging**               | Missing security events         | No auth failure logs, no access logs, no audit trail              |
| **A10 SSRF**                  | User-controlled URLs            | `fetch(userUrl)`, `HttpClient.get(input)` without validation      |

### 5. Authentication Bypass Detection

**JWT Attack Vectors:**

| Attack                  | Description                                            | Detection                                                      |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| **Algorithm Confusion** | Change `alg` from RS256 to HS256, sign with public key | Backend must enforce algorithm; reject HS256 if RS256 expected |
| **Signature Stripping** | Remove signature, set `alg: none`                      | Backend must reject `alg: none` in production                  |
| **Token Replay**        | Reuse expired or revoked tokens                        | Implement token revocation list; check `jti` claim             |
| **Claim Manipulation**  | Modify `sub`, `role`, `exp` claims                     | Verify signature before trusting any claim                     |
| **Key Confusion**       | Use public key as HMAC secret                          | Use separate keys for signing and verification                 |

**OAuth 2.0 / OIDC Attack Vectors:**

| Attack                              | Description                          | Prevention                                              |
| ----------------------------------- | ------------------------------------ | ------------------------------------------------------- |
| **Authorization Code Interception** | Intercept auth code in redirect      | Enforce PKCE for all OAuth clients (RFC 7636)           |
| **Redirect URI Manipulation**       | Register malicious redirect URI      | Exact match redirect URI validation; no wildcards       |
| **State Parameter Omission**        | CSRF on OAuth flow                   | Always include and validate `state` parameter           |
| **Token Leakage via Referrer**      | Access token exposed in HTTP Referer | Use fragment identifier for tokens; set Referrer-Policy |
| **Refresh Token Rotation Bypass**   | Steal refresh token                  | Implement automatic old-token revocation on rotation    |

**Testing Authentication Bypass:**

```bash
# JWT Algorithm Confusion Test
# 1. Obtain valid JWT with RS256
# 2. Decode header, change alg to HS256
# 3. Sign with the public key (treated as HMAC secret)
# 4. Send modified token — should be rejected

# Using jwt_tool:
python3 jwt_tool.py <original_jwt> -X a -pk public.pem

# "alg: none" Test
python3 jwt_tool.py <original_jwt> -X a -n

# Token Replay Test
# 1. Obtain valid token
# 2. Wait for expiration
# 3. Attempt to use expired token — should get 401
# 4. Attempt to use revoked token — should get 401

# OAuth PKCE Test
# 1. Initiate auth flow WITHOUT code_challenge
# 2. Attempt to exchange code for token — should fail
# 3. Initiate auth flow WITH code_challenge
# 4. Exchange with wrong code_verifier — should fail
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** (SRD)                    | Identifies web API security requirements that complement mobile SRD; defines backend security controls that mobile app depends on |
| **Stage 5** (Development)            | Conducts secure code review of backend services as they are developed; provides real-time feedback to backend developers          |
| **Stage 6** (Code Review)            | Reviews backend API code for OWASP Top 10 and API Top 10 vulnerabilities; findings included in Defect Report                      |
| **Stage 7** (Automated Testing)      | Ensures DAST scanning covers all API endpoints; validates that authentication bypass vectors are tested                           |
| **Stage 8** (Integrity Verification) | Re-tests all previously identified API vulnerabilities; verifies WAF rules are deployed and functional                            |
| **Stage 10** (Release Readiness)     | Provides backend API security sign-off to CSO for release checklist item #4                                                       |

## Quality Standards

| Metric                      | Standard                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **OWASP Top 10 Coverage**   | 100% of OWASP Top 10 (2021) controls assessed for all backend services                                       |
| **API Top 10 Coverage**     | 100% of OWASP API Top 10 (2023) controls assessed for all API endpoints                                      |
| **Code Review Throughput**  | ≥500 LOC/hour with ≥90% vulnerability detection rate (validated against known-vulnerable codebases)          |
| **WAF Effectiveness**       | ≥95% of OWASP Top 10 attack patterns blocked; <1% false positive rate                                        |
| **Authentication Security** | Zero authentication bypass vulnerabilities in production (validated by pen testing)                          |
| **Remediation SLA**         | P0/P1 API vulnerabilities remediated within 24 hours; P2 within current sprint                               |
| **Security Headers**        | 100% of API responses include required security headers (HSTS, X-Content-Type-Options, X-Frame-Options, CSP) |
