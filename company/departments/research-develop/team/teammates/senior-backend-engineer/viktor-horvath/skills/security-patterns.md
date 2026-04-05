# Security Patterns

**Category:** Backend Security
**Owner:** Senior Backend Engineer (Viktor Horvath)

## Overview

Implements comprehensive security controls across backend services, addressing OWASP Top 10 (2021) vulnerabilities, API-specific threats from OWASP API Top 10, input validation pipelines, JWT security best practices, and security header enforcement. Covers the full spectrum from input sanitization to token lifecycle management with production-grade defense-in-depth patterns.

## Competency Dimensions

| Dimension                       | Description                                                                                                                                                                                                            | Proficiency Indicators                                                                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| OWASP Top 10 (2021)             | Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Authentication Failures, Data Integrity Failures, Logging Failures, SSRF                  | Implements controls for all 10 categories; conducts threat modeling using STRIDE; can demonstrate each vulnerability and its mitigation  |
| API Security (OWASP API Top 10) | BOLA, Broken Authentication, Excessive Data Exposure, Lack of Resources, Broken Function Level Authorization, Mass Assignment, Security Misconfiguration, Injection, Improper Inventory Management, Unsafe Consumption | Designs API security posture addressing all 10 API-specific risks; implements object-level and function-level authorization consistently |
| Input Validation Pipelines      | Schema validation, sanitization, allowlist patterns, content-type enforcement                                                                                                                                          | Builds multi-layer validation (gateway → service → data access); uses allowlist-based validation over blocklist                          |
| JWT Best Practices              | Algorithm selection, key management, token revocation, claim design, algorithm confusion prevention                                                                                                                    | Implements HS256/RS256 correctly; prevents algorithm confusion attacks; designs token revocation with acceptable performance trade-offs  |
| Security Headers                | CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy                                                                                                                                | Configures complete header set; validates with security scanning tools; understands header interactions                                  |

## Execution Guidance

### OWASP Top 10 (2021) — Implementation Controls

| Rank | Vulnerability             | Primary Control                                           | Implementation Example                                                               |
| ---- | ------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| A01  | Broken Access Control     | Enforce authorization at every endpoint                   | Middleware that validates resource ownership before handler execution                |
| A02  | Cryptographic Failures    | Use vetted crypto libraries, never roll your own          | libsodium for symmetric, RSA-2048+ for asymmetric, bcrypt/argon2 for passwords       |
| A03  | Injection                 | Parameterized queries, input validation, ORM              | `db.Query("SELECT * FROM users WHERE id = $1", userID)` — never string concatenation |
| A04  | Insecure Design           | Threat modeling, security patterns, secure defaults       | STRIDE analysis during design phase; deny-by-default network policies                |
| A05  | Security Misconfiguration | Infrastructure as Code, automated config validation       | Terraform with policy-as-code (OPA); CIS benchmark scanning                          |
| A06  | Vulnerable Components     | SBOM, dependency scanning, patch SLAs                     | Snyk/Dependabot with 72-hour critical patch SLA                                      |
| A07  | Authentication Failures   | MFA, rate limiting, credential stuffing protection        | Argon2id password hashing, account lockout after 5 failures, TOTP MFA                |
| A08  | Data Integrity Failures   | Digital signatures, immutable audit logs, CI/CD integrity | Signed container images (cosign), append-only audit log tables                       |
| A09  | Logging Failures          | Structured logging, sensitive data exclusion, alerting    | Log all auth decisions, no PII in logs, alerts on auth anomalies                     |
| A10  | SSRF                      | URL allowlisting, metadata endpoint protection            | Validate all URLs against allowlist; block 169.254.169.254 and internal ranges       |

### OWASP API Top 10 — Defense Patterns

**API1: Broken Object Level Authorization (BOLA)**

```go
// BOLA prevention: always validate resource ownership
func RequireResourceOwnership(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        userID := GetUserIDFromToken(r.Context())
        resourceID := chi.URLParam(r, "id")

        // Check ownership — NEVER trust client to only request their own resources
        owner, err := db.GetResourceOwner(r.Context(), resourceID)
        if err != nil {
            http.Error(w, "Not Found", http.StatusNotFound) // Don't leak existence
            return
        }
        if owner != userID {
            http.Error(w, "Forbidden", http.StatusForbidden)
            return
        }

        next(w, r)
    }
}
```

**API3: Broken Object Property Level Authorization (Excessive Data Exposure)**

```go
// Response filtering: never return raw domain objects
type UserResponse struct {
    ID        string    `json:"id"`
    Name      string    `json:"name"`
    Role      string    `json:"role"`
    // Password, MFA secret, internal flags NEVER exposed
}

func ToUserResponse(user *User, requesterRole string) *UserResponse {
    resp := &UserResponse{
        ID:   user.ID,
        Name: user.Name,
    }
    // Role-based field exposure
    if requesterRole == "admin" {
        resp.Role = user.Role
    }
    return resp
}
```

**API5: Broken Function Level Authorization**

```go
// Function-level authorization middleware
func RequireRole(requiredRoles ...string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            userRole := GetUserRoleFromContext(r.Context())
            for _, role := range requiredRoles {
                if userRole == role {
                    next.ServeHTTP(w, r)
                    return
                }
            }
            http.Error(w, "Forbidden", http.StatusForbidden)
        })
    }
}

// Usage
r.With(RequireRole("admin", "super-admin")).Delete("/users/{id}", deleteUserHandler)
```

### Input Validation Pipeline

**Multi-layer validation architecture:**

```
Client Request → Gateway (schema validation) → Service (business validation) → Data Access (type safety)
```

```go
// Layer 1: Gateway-level schema validation (OpenAPI)
// Layer 2: Service-level business validation
type CreateUserValidator struct {
    Name     string `validate:"required,min=2,max=100,alphanumspace"`
    Email    string `validate:"required,email,max=255"`
    Password string `validate:"required,min=12,max=128"`
    Role     string `validate:"required,oneof=user moderator admin"`
}

func (v *CreateUserValidator) Validate() error {
    val := validator.New()

    // Struct tags validation
    if err := val.Struct(v); err != nil {
        return &ValidationError{Fields: parseValidationErrors(err)}
    }

    // Business rule validation
    if exists, _ := db.EmailExists(context.Background(), v.Email); exists {
        return &ValidationError{Fields: map[string]string{
            "email": "Email address already registered",
        }}
    }

    // Password strength check
    if err := checkPasswordStrength(v.Password); err != nil {
        return &ValidationError{Fields: map[string]string{
            "password": err.Error(),
        }}
    }

    return nil
}

// Layer 3: Data access — parameterized queries (type-safe)
func (r *UserRepository) Create(ctx context.Context, user *User) error {
    _, err := r.db.ExecContext(ctx,
        `INSERT INTO users (name, email, password_hash, role, created_at)
         VALUES ($1, $2, $3, $4, $5)`,
        user.Name,
        strings.ToLower(user.Email),    // Normalize
        user.PasswordHash,
        user.Role,
        time.Now().UTC(),
    )
    return err
}
```

### JWT Best Practices

**Algorithm confusion prevention:**

```go
// CRITICAL: Explicitly specify expected algorithm — NEVER accept algorithm from token header
func VerifyJWT(tokenString string, publicKey *rsa.PublicKey) (*Claims, error) {
    claims := &Claims{}

    // ParseWithClaims with explicit key function that ONLY returns RSA key
    // This prevents algorithm confusion attacks (HS256 with public key as HMAC secret)
    parsed, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
        // CRITICAL: Verify the algorithm is what we expect
        if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return publicKey, nil
    })

    if err != nil {
        return nil, err
    }
    if !parsed.Valid {
        return nil, ErrInvalidToken
    }

    return claims, nil
}
```

**Token revocation strategy (Redis-backed blocklist):**

```go
type TokenRevoker struct {
    redis *redis.Client
}

// Revoke token — add JTI to blocklist until expiry
func (r *TokenRevoker) Revoke(ctx context.Context, jti string, expiresAt time.Time) error {
    ttl := time.Until(expiresAt)
    if ttl <= 0 {
        return nil // Already expired
    }
    key := fmt.Sprintf("token:blocklist:%s", jti)
    return r.redis.Set(ctx, key, "revoked", ttl).Err()
}

// Check if token is revoked
func (r *TokenRevoker) IsRevoked(ctx context.Context, jti string) bool {
    key := fmt.Sprintf("token:blocklist:%s", jti)
    _, err := r.redis.Get(ctx, key).Result()
    return err == nil // Key exists = revoked
}

// Claims with JTI
type Claims struct {
    jwt.RegisteredClaims
    UserID string   `json:"sub"`
    Role   string   `json:"role"`
    JTI    string   `json:"jti"` // JWT ID — unique per token
}

// Token generation with short expiry + refresh tokens
func GenerateTokenPair(userID string, role string) (*TokenPair, error) {
    now := time.Now()

    // Access token: short-lived (15 min)
    accessToken := jwt.NewWithClaims(jwt.SigningMethodRS256, Claims{
        RegisteredClaims: jwt.RegisteredClaims{
            Subject:   userID,
            ExpiresAt: jwt.NewNumericDate(now.Add(15 * time.Minute)),
            IssuedAt:  jwt.NewNumericDate(now),
            ID:        uuid.New().String(),
        },
        UserID: userID,
        Role:   role,
        JTI:    uuid.New().String(),
    })

    // Refresh token: longer-lived (7 days), stored in HttpOnly cookie
    refreshToken := jwt.NewWithClaims(jwt.SigningMethodRS256, Claims{
        RegisteredClaims: jwt.RegisteredClaims{
            Subject:   userID,
            ExpiresAt: jwt.NewNumericDate(now.Add(7 * 24 * time.Hour)),
            IssuedAt:  jwt.NewNumericDate(now),
            ID:        uuid.New().String(),
        },
        UserID: userID,
        Role:   role,
        JTI:    uuid.New().String(),
    })

    // ... sign tokens ...
    return &TokenPair{AccessToken: accessSigned, RefreshToken: refreshSigned}, nil
}
```

**JWT security checklist:**

| Check                          | Requirement                          | Risk if Missing                 |
| ------------------------------ | ------------------------------------ | ------------------------------- |
| Algorithm explicitly specified | RS256/ES256, never accept from token | Algorithm confusion attack      |
| Short access token expiry      | ≤ 15 minutes                         | Long window for token theft     |
| Refresh token rotation         | New refresh token on each use        | Token theft persistence         |
| JTI claim present              | Unique per token                     | Cannot revoke individual tokens |
| Issuer validated               | Check `iss` claim                    | Cross-service token confusion   |
| Audience validated             | Check `aud` claim                    | Token reuse across services     |
| Signature verified             | With correct public key              | Forgery                         |

### Security Headers

**Complete security header middleware:**

```go
func SecurityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        h := w.Header()

        // Transport security
        h.Set("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
        h.Set("X-Content-Type-Options", "nosniff")
        h.Set("X-Frame-Options", "DENY")

        // Content security
        h.Set("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://api.company.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")

        // Referrer control
        h.Set("Referrer-Policy", "strict-origin-when-cross-origin")

        // Feature control
        h.Set("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(self)")

        // Remove server identification
        h.Del("Server")
        h.Del("X-Powered-By")

        // Cache control for API responses
        h.Set("Cache-Control", "no-store, no-cache, must-revalidate")
        h.Set("Pragma", "no-cache")

        next.ServeHTTP(w, r)
    })
}
```

## Pipeline Integration

**Stage 1 (Requirements → SRD):** CSO defines security requirements that map to OWASP Top 10 controls. Input validation requirements derived from PRD data sensitivity analysis.

**Stage 3 (Architecture):** Component diagrams must show security control placement (gateway WAF, service auth middleware, data encryption). ADR required for JWT algorithm selection and token lifecycle strategy.

**Stage 5 (Development):** All security controls implemented per SRD. Input validation at every layer. JWT verification uses explicit algorithm. Security headers applied globally.

**Stage 6 (Code Review):** Security-focused review validates OWASP controls, input validation completeness, JWT implementation correctness, and security header configuration.

**Stage 7 (Testing):** DAST scanning (OWASP ZAP) validates runtime security. SAST scanning (Semgrep, SonarQube) validates static code security. Penetration testing validates defense-in-depth.

**Stage 8 (Integrity Verification):** CSO verifies all SRD requirements implemented. No security control gaps. No sensitive data in logs. Cryptographic implementations use vetted libraries.

## Quality Standards

| Metric                     | Target                                   | Measurement                                       |
| -------------------------- | ---------------------------------------- | ------------------------------------------------- |
| OWASP Top 10 coverage      | 100% of controls implemented             | Security audit checklist                          |
| DAST scan findings         | 0 critical, 0 high                       | OWASP ZAP scan results                            |
| Input validation coverage  | 100% of external inputs validated        | Code review + SAST                                |
| JWT algorithm confusion    | 0 vulnerabilities                        | Explicit algorithm enforcement + penetration test |
| Security header compliance | A+ rating                                | securityheaders.com scan                          |
| Dependency vulnerabilities | 0 critical, 0 high (72h SLA for patches) | Snyk/Dependabot                                   |
| Auth decision logging      | 100% of auth decisions logged            | Log audit                                         |
| PII in logs                | 0 occurrences                            | Log scanning + code review                        |
