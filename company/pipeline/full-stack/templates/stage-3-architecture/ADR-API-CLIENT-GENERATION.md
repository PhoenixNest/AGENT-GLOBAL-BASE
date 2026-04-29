# ADR: API Client Generation Strategy (Cross-Platform)

| Field         | Value                                                               |
| ------------- | ------------------------------------------------------------------- |
| **Status**    | Proposed                                                            |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)                   |
| **Decision**  | OpenAPI Generator for TypeScript/Swift/Kotlin with CI/CD publishing |
| **Date**      | YYYY-MM-DD                                                          |
| **Authors**   | CIO (primary), Backend Lead, All Platform Leads                     |
| **Reviewers** | CTO (technology)                                                    |

---

## Decision

We will use **OpenAPI 3.0 YAML** as the single source of truth and generate type-safe API client SDKs using OpenAPI Generator for TypeScript (web/Axios), Swift (iOS/Alamofire), and Kotlin (Android/Retrofit).

## Rationale

Full-stack cross-platform products require consistent API client implementations across web (TypeScript), iOS (Swift), Android (Kotlin), and backend services. Manual client implementation leads to inconsistencies: different error handling patterns, mismatched request/response types, divergent authentication logic. This creates bugs that are platform-specific and difficult to diagnose. This ADR establishes a unified API client generation strategy using OpenAPI specifications as the single source of truth.

### 1. API Specification Format: OpenAPI 3.0 (YAML)

**Primary Format:** OpenAPI 3.0 YAML specification

**Rationale:**

- **Language-agnostic** — Single spec generates clients for TypeScript, Swift, Kotlin, Go, Python
- **Rich ecosystem** — Extensive tooling (Swagger UI, Postman, code generators)
- **Validation** — Automated spec linting catches errors before client generation
- **Documentation** — Auto-generated interactive docs (Swagger UI, Redoc)

**Specification Structure:**

```yaml
openapi: 3.0.3
info:
  title: Company API
  version: 1.2.3
  description: Unified API for web, iOS, Android platforms

servers:
  - url: https://api.company.com/v1
    description: Production
  - url: https://staging-api.company.com/v1
    description: Staging

paths:
  /users/{id}:
    get:
      summary: Get user profile
      operationId: getUserById
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: User profile
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          description: User not found
        "401":
          description: Unauthorized

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
          nullable: true
```

**Spec Validation (CI Gate):**

```bash
# Validate OpenAPI spec syntax
npx @stoplight/spectral lint api-spec/openapi.yaml

# Check for breaking changes vs. previous version
npx openapi-diff api-spec/openapi-v1.2.2.yaml api-spec/openapi-v1.2.3.yaml --fail-on-incompatible
```

---

### 2. Client Generation Tool: OpenAPI Generator

**Technology:** OpenAPI Generator (official OpenAPI project tooling)

**Supported Languages:**

- **Web:** `typescript-axios` (TypeScript + Axios HTTP client)
- **iOS:** `swift5` (Swift 5 + Alamofire HTTP client)
- **Android:** `kotlin` (Kotlin + Retrofit HTTP client)
- **Backend:** `go` (Go + native net/http), `python` (Python + requests)

**Generation Configuration:**

#### Web (TypeScript)

```yaml
# generators/typescript-axios/config.yaml
generatorName: typescript-axios
outputDir: clients/typescript
additionalProperties:
  npmName: "@company/api-client"
  npmVersion: "1.2.3"
  supportsES6: true
  withInterfaces: true
  withSeparateModelsAndApi: true
```

#### iOS (Swift)

```yaml
# generators/swift5/config.yaml
generatorName: swift5
outputDir: clients/swift
additionalProperties:
  projectName: "CompanyAPIClient"
  podAuthors: "Company Engineering"
  podSummary: "Auto-generated API client for Company services"
  responseAs: "Combine" # Use Combine framework for async/await
```

#### Android (Kotlin)

```yaml
# generators/kotlin/config.yaml
generatorName: kotlin
outputDir: clients/kotlin
additionalProperties:
  groupId: "com.company.api"
  artifactId: "client"
  artifactVersion: "1.2.3"
  library: "jvm-retrofit2"
  useCoroutines: true
```

---

### 3. Version Synchronization Strategy

**Challenge:** Backend API updates to v1.2.3, but mobile apps still use v1.2.2 client → incompatibility.

**Solution:** Strict version synchronization with automated checks.

**Version Alignment Policy:**

| Component         | Version | Update Trigger                |
| ----------------- | ------- | ----------------------------- |
| OpenAPI Spec      | 1.2.3   | Backend endpoint changes      |
| TypeScript Client | 1.2.3   | Auto-generated on spec change |
| Swift Client      | 1.2.3   | Auto-generated on spec change |
| Kotlin Client     | 1.2.3   | Auto-generated on spec change |
| Backend Service   | 1.2.3   | Deployment with new endpoints |

**Breaking Change Detection:**

CI pipeline compares current spec against previous version:

```bash
# Detect breaking changes
openapi-diff old-spec.yaml new-spec.yaml --json > diff-report.json

# Parse report, fail CI if breaking changes detected
if jq '.breakings | length > 0' diff-report.json; then
  echo "❌ Breaking changes detected!"
  cat diff-report.json
  exit 1
fi
```

**Breaking Change Examples:**

- Remove endpoint or operation
- Change field type (string → integer)
- Make optional field required
- Remove enum value
- Change authentication mechanism

**Non-Breaking Changes (Safe):**

- Add new endpoint
- Add optional field to response
- Add new enum value
- Improve documentation

---

### 4. Client SDK Consistency Enforcement

**Problem:** Generated clients have inconsistent error handling, retry logic, authentication.

**Solution:** Wrapper libraries that standardize common patterns.

#### Web: TypeScript Wrapper

```typescript
// clients/typescript/src/ApiClient.ts
import { Configuration, DefaultApi } from "./generated";

export class ApiClient {
  private api: DefaultApi;

  constructor(token: string) {
    const config = new Configuration({
      basePath: process.env.API_BASE_URL,
      accessToken: token,
    });
    this.api = new DefaultApi(config);
  }

  // Standardized error handling
  async getUser(id: string): Promise<User> {
    try {
      return await this.api.getUserById(id);
    } catch (error) {
      if (error.response?.status === 404) {
        throw new NotFoundError(`User ${id} not found`);
      } else if (error.response?.status === 401) {
        throw new AuthenticationError("Invalid token");
      } else {
        throw new ApiError("Unknown error", error);
      }
    }
  }

  // Automatic retry with exponential backoff
  async retryableRequest<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await sleep(Math.pow(2, i) * 1000); // 1s, 2s, 4s
      }
    }
    throw new Error("Unreachable");
  }
}
```

#### iOS: Swift Wrapper

```swift
// clients/swift/Sources/CompanyAPIClient/ApiClient.swift
import Foundation
import Combine

public class ApiClient {
    private let api: DefaultAPI
    private let token: String

    public init(token: String) {
        self.token = token
        let configuration = Configuration(basePath: ProcessInfo.processInfo.environment["API_BASE_URL"] ?? "")
        configuration.apiKey = token
        self.api = DefaultAPI(configuration: configuration)
    }

    // Standardized error handling
    public func getUser(id: String) -> AnyPublisher<User, ApiError> {
        return api.getUserByIdWithResponse(id: id)
            .mapError { error in
                if let httpError = error as? ErrorResponse {
                    switch httpError.code {
                    case 404: return NotFoundError(message: "User \(id) not found")
                    case 401: return AuthenticationError(message: "Invalid token")
                    default: return ApiError(message: "Unknown error", underlying: error)
                    }
                }
                return ApiError(message: "Unknown error", underlying: error)
            }
            .map { $0.body }
            .eraseToAnyPublisher()
    }
}
```

#### Android: Kotlin Wrapper

```kotlin
// clients/kotlin/src/main/java/com/company/api/ApiClient.kt
class ApiClient(private val token: String) {
    private val api: DefaultApi by lazy {
        Retrofit.Builder()
            .baseUrl(System.getenv("API_BASE_URL"))
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(DefaultApi::class.java)
    }

    // Standardized error handling
    suspend fun getUser(id: String): User {
        return try {
            api.getUserById(id, "Bearer $token")
        } catch (e: HttpException) {
            when (e.code()) {
                404 -> throw NotFoundError("User $id not found")
                401 -> throw AuthenticationError("Invalid token")
                else -> throw ApiError("Unknown error", e)
            }
        }
    }

    // Automatic retry with exponential backoff
    suspend fun <T> retryableRequest(maxRetries: Int = 3, block: suspend () -> T): T {
        repeat(maxRetries) { attempt ->
            try {
                return block()
            } catch (e: Exception) {
                if (attempt == maxRetries - 1) throw e
                delay(2L.pow(attempt).toLong() * 1000) // 1s, 2s, 4s
            }
        }
        throw IllegalStateException("Unreachable")
    }
}
```

---

### 5. CI/CD Integration: Automated Client Publishing

**Workflow:** `.github/workflows/generate-api-clients.yml`

```yaml
name: Generate & Publish API Clients

on:
  push:
    paths:
      - "api-spec/openapi.yaml"

jobs:
  validate-spec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint OpenAPI spec
        run: npx @stoplight/spectral lint api-spec/openapi.yaml
      - name: Check for breaking changes
        run: |
          git fetch origin main
          openapi-diff api-spec/openapi.yaml origin/main:api-spec/openapi.yaml --json > diff.json
          if jq '.breakings | length > 0' diff.json; then
            echo "Breaking changes detected! Review diff.json"
            exit 1
          fi

  generate-clients:
    needs: validate-spec
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate TypeScript client
        run: |
          openapi-generator generate \
            -i api-spec/openapi.yaml \
            -g typescript-axios \
            -o clients/typescript \
            -c generators/typescript-axios/config.yaml

      - name: Generate Swift client
        run: |
          openapi-generator generate \
            -i api-spec/openapi.yaml \
            -g swift5 \
            -o clients/swift \
            -c generators/swift5/config.yaml

      - name: Generate Kotlin client
        run: |
          openapi-generator generate \
            -i api-spec/openapi.yaml \
            -g kotlin \
            -o clients/kotlin \
            -c generators/kotlin/config.yaml

      - name: Run client tests
        run: |
          cd clients/typescript && npm test
          cd ../swift && swift test
          cd ../kotlin && ./gradlew test

      - name: Publish TypeScript package
        run: |
          cd clients/typescript
          npm version patch
          npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Publish Swift pod
        run: |
          cd clients/swift
          pod trunk push CompanyAPIClient.podspec --allow-warnings
        env:
          COCOAPODS_TRUNK_TOKEN: ${{ secrets.COCOAPODS_TOKEN }}

      - name: Publish Kotlin package
        run: |
          cd clients/kotlin
          ./gradlew publish
        env:
          ORG_GRADLE_PROJECT_mavenCentralUsername: ${{ secrets.MAVEN_USERNAME }}
          ORG_GRADLE_PROJECT_mavenCentralPassword: ${{ secrets.MAVEN_PASSWORD }}
```

---

## Alternatives Considered

### Alternative 1: Manual Client Implementation

**Pros:** Full control over client behavior, no code generation complexity  
**Cons:** Inconsistent error handling across platforms, duplicated effort, spec-client drift  
**Rejected because:** Three platform teams implementing same API independently leads to inconsistencies; maintenance burden scales linearly with endpoint count.

### Alternative 2: Swagger Codegen (Legacy Tool)

**Pros:** Mature tooling, wide language support  
**Cons:** Less active development, fewer customization options, inferior template engine  
**Rejected because:** OpenAPI Generator is the actively maintained successor with better community support and more frequent updates.

### Alternative 3: GraphQL Code Generator

**Pros:** Type-safe GraphQL queries, excellent TypeScript support  
**Cons:** Only works for GraphQL (not REST), requires GraphQL schema instead of OpenAPI spec  
**Rejected because:** Primary API is REST (per ADR-API-STRATEGY); GraphQL used only for aggregation endpoints.

---

## Consequences

### Positive

- **Consistency** — All platforms use identical request/response types, error handling, authentication
- **Speed** — New endpoint added to spec → all clients updated in <5 minutes (automated)
- **Type safety** — Compile-time errors catch API mismatches before runtime
- **Documentation** — Swagger UI auto-generated from spec, always up-to-date

### Negative

- **Learning curve** — Engineers must understand OpenAPI spec syntax, code generation workflow (1-week ramp-up)
- **Customization limits** — Generated code may not match team's preferred patterns (mitigated by wrapper libraries)
- **Build time** — Client generation adds ~2 minutes to CI pipeline

### Risks & Mitigations

| Risk                               | Likelihood | Impact   | Mitigation                                                                                           |
| ---------------------------------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------- |
| Generated code has bugs            | Low        | Medium   | Comprehensive integration tests for each client, manual review of generated code on first generation |
| Spec-client version mismatch       | Medium     | High     | CI gate enforces version alignment, automated alerts if client version lags spec                     |
| Breaking changes slip through      | Medium     | Critical | openapi-diff CI gate, mandatory peer review for spec changes, staging environment testing            |
| Vendor lock-in (OpenAPI Generator) | Low        | Low      | OpenAPI is open standard; switching code generators is straightforward (same spec format)            |

---

## Implementation Plan

**Phase 1 (Week 1-2):** OpenAPI spec creation

- Document existing REST endpoints in OpenAPI 3.0 YAML format
- Set up Spectral linting for spec validation
- Create Swagger UI documentation portal

**Phase 2 (Week 3-4):** Client generation pipeline

- Configure OpenAPI Generator for TypeScript, Swift, Kotlin
- Create wrapper libraries for standardized error handling, retry logic
- Set up CI/CD workflow for automated generation + publishing

**Phase 3 (Week 5-6):** Migration from manual clients

- Replace hand-written API clients with generated clients in web, iOS, Android apps
- Run integration tests to verify parity
- Deprecate old client libraries

**Phase 4 (Week 7-8):** Governance & training

- Document spec update workflow (who can modify spec, review process)
- Train engineers on OpenAPI best practices
- Establish quarterly spec audit (remove deprecated endpoints, update documentation)

---

## Compliance Alignment

- **SOC 2 Type II:** API client version tracking, changelog maintained
- **SRD Section 6.3:** "Unified auth flow with consistent token handling across all platforms"
- **SRD Section 9.1:** "API contract verification via automated client generation from OpenAPI spec"

---

## References

- [OpenAPI Specification 3.0](https://swagger.io/specification/)
- [OpenAPI Generator Documentation](https://openapi-generator.tech/)
- [Spectral Linting Rules](https://meta.stoplight.io/docs/spectral/)
- SRD.md Section 6.3 (Cross-Platform Authentication), Section 9.1 (API Contract Verification)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
