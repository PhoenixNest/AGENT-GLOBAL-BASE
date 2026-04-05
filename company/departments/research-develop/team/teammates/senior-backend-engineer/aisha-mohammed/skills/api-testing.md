# API Testing

**Category:** Backend Quality Engineering
**Owner:** Senior Backend Engineer (Aisha Mohammed)

## Overview

Designs and implements comprehensive API testing strategies covering contract validation, integration testing patterns, performance benchmarking with percentile analysis, API documentation validation against OpenAPI specifications, and systematic negative testing. Ensures APIs meet functional correctness, performance, and documentation accuracy standards before advancing through pipeline gates.

## Competency Dimensions

| Dimension                    | Description                                                                          | Proficiency Indicators                                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contract Testing             | OpenAPI/Swagger validation, schema conformance, backward compatibility checks        | Implements automated contract tests that run on every PR; detects breaking changes before merge; validates request/response against OpenAPI schema |
| Integration Testing          | Service-to-service testing, database integration, external dependency mocking        | Tests full request lifecycle through all service layers; uses testcontainers for real database dependencies; mocks external services with wiremock |
| Performance Benchmarking     | p50/p95/p99 latency analysis, throughput measurement, resource utilization profiling | Designs benchmarks that reflect production traffic patterns; identifies latency outliers; profiles CPU/memory under load                           |
| API Documentation Validation | OpenAPI spec accuracy, example correctness, endpoint completeness                    | Validates documentation matches actual API behavior; ensures all endpoints are documented with accurate request/response examples                  |
| Negative Testing             | Error path coverage, boundary condition testing, malformed input handling            | Tests all error responses return correct status codes and error bodies; validates input rejection for edge cases                                   |

## Execution Guidance

### Contract Testing with OpenAPI Validation

**Automated contract test suite (Go):**

```go
func TestAPIContract(t *testing.T) {
    // Load OpenAPI spec
    spec, err := os.ReadFile("../../architecture/specs/openapi.yaml")
    require.NoError(t, err)

    schema, err := openapi3.NewLoader().LoadFromData(spec)
    require.NoError(t, err)
    require.NoError(t, schema.Validate(context.Background()))

    // Start test server
    srv := startTestServer()
    defer srv.Close()

    client := &http.Client{Timeout: 10 * time.Second}

    tests := []struct {
        name       string
        method     string
        path       string
        body       interface{}
        headers    map[string]string
        wantStatus int
        wantSchema string  // JSON Schema path in OpenAPI
    }{
        {
            name:       "GET /users/{id} - success",
            method:     "GET",
            path:       "/users/test-user-id",
            headers:    map[string]string{"Authorization": "Bearer valid-token"},
            wantStatus: http.StatusOK,
            wantSchema: "#/components/schemas/UserResponse",
        },
        {
            name:       "POST /users - success",
            method:     "POST",
            path:       "/users",
            body:       CreateUserRequest{Name: "Test User", Email: "test@example.com"},
            wantStatus: http.StatusCreated,
            wantSchema: "#/components/schemas/UserResponse",
        },
        {
            name:       "POST /users - validation error",
            method:     "POST",
            path:       "/users",
            body:       CreateUserRequest{Name: "", Email: "invalid"},
            wantStatus: http.StatusBadRequest,
            wantSchema: "#/components/schemas/ErrorResponse",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := newRequest(t, tt.method, srv.URL+tt.path, tt.body, tt.headers)
            resp, err := client.Do(req)
            require.NoError(t, err)
            defer resp.Body.Close()

            // Validate status code
            assert.Equal(t, tt.wantStatus, resp.StatusCode)

            // Validate response schema against OpenAPI
            if tt.wantSchema != "" {
                body, err := io.ReadAll(resp.Body)
                require.NoError(t, err)

                schemaRef := resolveSchemaRef(schema, tt.wantSchema)
                require.NotNil(t, schemaRef)

                validator := jsonschema.NewCompiler()
                err = validator.AddResource("schema", schemaRef)
                require.NoError(t, err)

                jsonSchema, _ := validator.Compile("schema")
                err = jsonSchema.Validate(bytes.NewReader(body))
                assert.NoError(t, err, "Response body does not match schema %s", tt.wantSchema)
            }

            // Validate Content-Type
            assert.Contains(t, resp.Header.Get("Content-Type"), "application/json")
        })
    }
}
```

**Breaking change detection in CI:**

```yaml
# .github/workflows/contract-check.yml
- name: Check API Compatibility
  uses: oasdiff/oasdiff-action/breaking@main
  with:
    base: ./openapi/base.yaml
    revision: ./openapi/current.yaml
    fail-on: BREAKING

  # Breaking changes detected:
  # - Removed endpoint
  # - Removed required field from request
  # - Changed field type
  # - Removed required header
  # - Changed auth requirement
  # - Narrowed enum values
```

### Integration Testing with Testcontainers

```go
func TestUserRepository_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test in short mode")
    }

    ctx := context.Background()

    // Start PostgreSQL container
    pgContainer, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:16-alpine"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("testuser"),
        postgres.WithPassword("testpass"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections").
                WithOccurrence(2).WithStartupTimeout(30*time.Second)),
    )
    require.NoError(t, err)
    defer pgContainer.Terminate(ctx)

    // Get connection string
    connStr, err := pgContainer.ConnectionString(ctx, "sslmode=disable")
    require.NoError(t, err)

    // Run migrations
    db, err := sql.Open("postgres", connStr)
    require.NoError(t, err)
    defer db.Close()

    // Apply migrations
    runner, err := migrate.NewWithDatabaseInstance("file://../../migrations", "testdb", db)
    require.NoError(t, err)
    require.NoError(t, runner.Up())

    // Run tests
    repo := NewUserRepository(db)

    t.Run("Create and Retrieve User", func(t *testing.T) {
        user := &User{
            Name:  "Integration Test User",
            Email: "integration@test.com",
            Role:  "user",
        }

        err := repo.Create(ctx, user)
        require.NoError(t, err)
        assert.NotEmpty(t, user.ID)

        retrieved, err := repo.GetByID(ctx, user.ID)
        require.NoError(t, err)
        assert.Equal(t, user.Name, retrieved.Name)
        assert.Equal(t, user.Email, retrieved.Email)
    })

    t.Run("Duplicate Email Rejected", func(t *testing.T) {
        user1 := &User{Name: "User 1", Email: "dup@test.com", Role: "user"}
        require.NoError(t, repo.Create(ctx, user1))

        user2 := &User{Name: "User 2", Email: "dup@test.com", Role: "user"}
        err := repo.Create(ctx, user2)
        assert.Error(t, err)
        assert.Contains(t, err.Error(), "duplicate")
    })
}
```

**Test service topology with Docker Compose:**

```yaml
# docker-compose.test.yml
version: "3.8"
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U testuser"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
    depends_on:
      zookeeper:
        condition: service_healthy

  wiremock:
    image: wiremock/wiremock:2.35.0
    volumes:
      - ./testdata/wiremock:/home/wiremock
    ports:
      - "8089:8080"

  app:
    build: .
    environment:
      DATABASE_URL: postgres://testuser:testpass@postgres:5432/testdb
      REDIS_URL: redis://redis:6379
      KAFKA_BROKERS: kafka:9092
      EXTERNAL_API_URL: http://wiremock:8080
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_started
      wiremock:
        condition: service_started
```

### Performance Benchmarking

**k6 load test script:**

```javascript
// load-test.js
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const errorRate = new Rate("errors");

export const options = {
  stages: [
    { duration: "2m", target: 100 }, // Ramp up to 100 VUs
    { duration: "5m", target: 100 }, // Stay at 100 VUs
    { duration: "2m", target: 500 }, // Spike to 500 VUs
    { duration: "5m", target: 500 }, // Stay at 500 VUs (stress test)
    { duration: "2m", target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ["p(50)<100", "p(95)<300", "p(99)<500"],
    http_req_failed: ["rate<0.01"], // < 1% error rate
    errors: ["rate<0.05"], // < 5% custom error rate
  },
};

export default function () {
  const params = {
    headers: {
      Authorization: `Bearer ${__ENV.AUTH_TOKEN}`,
      "Content-Type": "application/json",
    },
  };

  // GET /users/{id}
  const userId = Math.floor(Math.random() * 10000);
  const res = http.get(`http://api:8080/users/${userId}`, params);

  const checkRes = check(res, {
    "status is 200": (r) => r.status === 200,
    "response time < 200ms": (r) => r.timings.duration < 200,
    "has user data": (r) => JSON.parse(r.body).id !== undefined,
  });

  errorRate.add(!checkRes);
  sleep(0.5);

  // POST /orders
  const orderPayload = JSON.stringify({
    userId: userId,
    items: [{ productId: "prod-123", quantity: 2 }],
  });

  const orderRes = http.post("http://api:8080/orders", orderPayload, params);

  check(orderRes, {
    "order status is 201": (r) => r.status === 201,
    "order response time < 500ms": (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

**Performance benchmark interpretation:**

| Percentile   | Meaning                       | Target  | Action if Exceeded                |
| ------------ | ----------------------------- | ------- | --------------------------------- |
| p50 (median) | Typical user experience       | < 100ms | Investigate common code paths     |
| p95          | Power user / complex requests | < 300ms | Identify slow query patterns      |
| p99          | Worst-case scenarios          | < 500ms | Profile outliers, check GC pauses |
| p99.9        | Edge cases, cold starts       | < 1s    | Check connection pool exhaustion  |

### Negative Testing Framework

```go
func TestAPI_NegativeCases(t *testing.T) {
    srv := startTestServer()
    defer srv.Close()

    tests := []struct {
        name       string
        setup      func(t *testing.T, req *http.Request)
        wantStatus int
        wantError  string
    }{
        {
            name: "Missing auth token",
            setup: func(t *testing.T, req *http.Request) {
                // No Authorization header
            },
            wantStatus: http.StatusUnauthorized,
            wantError:  "missing_authorization",
        },
        {
            name: "Expired auth token",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Authorization", "Bearer expired-token")
            },
            wantStatus: http.StatusUnauthorized,
            wantError:  "token_expired",
        },
        {
            name: "Invalid JSON body",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Content-Type", "application/json")
                req.Body = io.NopCloser(strings.NewReader("{invalid json"))
            },
            wantStatus: http.StatusBadRequest,
            wantError:  "invalid_json",
        },
        {
            name: "Missing required field",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Content-Type", "application/json")
                req.Body = io.NopCloser(strings.NewReader(`{"email":"test@test.com"}`)) // missing "name"
            },
            wantStatus: http.StatusBadRequest,
            wantError:  "validation_error",
        },
        {
            name: "Rate limit exceeded",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Authorization", "Bearer valid-token")
                req.Header.Set("Content-Type", "application/json")
                req.Body = io.NopCloser(strings.NewReader(`{"name":"test","email":"test@test.com"}`))
                // Simulate rate limit by calling 100 times first
            },
            wantStatus: http.StatusTooManyRequests,
            wantError:  "rate_limit_exceeded",
        },
        {
            name: "Non-existent resource",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Authorization", "Bearer valid-token")
            },
            wantStatus: http.StatusNotFound,
            wantError:  "resource_not_found",
        },
        {
            name: "Method not allowed",
            setup: func(t *testing.T, req *http.Request) {},
            wantStatus: http.StatusMethodNotAllowed,
            wantError:  "method_not_allowed",
        },
        {
            name: "Oversized payload",
            setup: func(t *testing.T, req *http.Request) {
                req.Header.Set("Content-Type", "application/json")
                largePayload := strings.Repeat("a", 11*1024*1024) // 11MB (limit is 10MB)
                req.Body = io.NopCloser(strings.NewReader(fmt.Sprintf(`{"data":"%s"}`, largePayload)))
            },
            wantStatus: http.StatusRequestEntityTooLarge,
            wantError:  "payload_too_large",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req, _ := http.NewRequest("POST", srv.URL+"/users", nil)
            tt.setup(t, req)

            resp, err := http.DefaultClient.Do(req)
            require.NoError(t, err)
            defer resp.Body.Close()

            assert.Equal(t, tt.wantStatus, resp.StatusCode)

            var errResp ErrorResponse
            json.NewDecoder(resp.Body).Decode(&errResp)
            assert.Equal(t, tt.wantError, errResp.Code)
        })
    }
}
```

### API Documentation Validation

**Automated documentation drift detection:**

```go
func TestAPIDocumentationDrift(t *testing.T) {
    // 1. Load OpenAPI spec
    spec := loadOpenAPISpec(t)

    // 2. Start server and enumerate all routes
    srv := startTestServer()
    defer srv.Close()

    routes := getRegisteredRoutes(srv)

    // 3. Check every route is documented
    for _, route := range routes {
        t.Run(fmt.Sprintf("Route %s %s is documented", route.Method, route.Path), func(t *testing.T) {
            found := findOperation(spec, route.Method, route.Path)
            assert.NotNil(t, found, "Route %s %s not found in OpenAPI spec", route.Method, route.Path)
        })
    }

    // 4. Check every documented endpoint exists
    for path, pathItem := range spec.Paths.Map() {
        for method := range pathItem.Operations() {
            t.Run(fmt.Sprintf("Documented endpoint %s %s exists", method, path), func(t *testing.T) {
                found := routeExists(routes, method, path)
                assert.True(t, found, "Documented endpoint %s %s not found in server", method, path)
            })
        }
    }

    // 5. Validate example responses match schema
    for path, pathItem := range spec.Paths.Map() {
        for method, op := range pathItem.Operations() {
            if op.Responses != nil {
                for code, response := range op.Responses.Map() {
                    t.Run(fmt.Sprintf("Example for %s %s %s", method, path, code), func(t *testing.T) {
                        if response.Value.Content != nil {
                            for mimeType, mediaType := range response.Value.Content {
                                if mediaType.Value.Example != nil {
                                    // Validate example against schema
                                    schema := mediaType.Value.Schema
                                    assertValidExample(t, mediaType.Value.Example, schema)
                                }
                            }
                        }
                    })
                }
            }
        }
    }
}
```

## Pipeline Integration

**Stage 5 (Development):** Contract tests written alongside endpoint implementation. Integration tests added for each new service interaction. Performance benchmarks established for new endpoints.

**Stage 6 (Code Review):** Code review validates test coverage includes contract, integration, and negative tests. All endpoints must have corresponding OpenAPI documentation entries.

**Stage 7 (Testing):** Full contract test suite runs against staging environment. Performance benchmarks executed with production-like load. Negative test results reviewed for completeness.

**Stage 8 (Integrity Verification):** Panel validates test coverage meets quality standards. Documentation drift check passes. Performance benchmarks within threshold.

## Quality Standards

| Metric                     | Target                      | Measurement                          |
| -------------------------- | --------------------------- | ------------------------------------ |
| Contract test coverage     | 100% of endpoints           | OpenAPI endpoint count vs test count |
| Integration test pass rate | 100%                        | CI/CD pipeline results               |
| Performance (p95)          | Within defined thresholds   | k6/Gatling benchmark results         |
| Performance (p99)          | Within defined thresholds   | k6/Gatling benchmark results         |
| Error rate under load      | < 1%                        | Load test error metrics              |
| Documentation accuracy     | 100% match (zero drift)     | Automated drift detection            |
| Negative test coverage     | All error paths tested      | Error code coverage analysis         |
| Test execution time        | < 10 minutes for full suite | CI pipeline duration                 |
