---
version: "1.0.0"
---

------ | ----------------------------- | ------- | --------------------------------- |
| p50 (median) | Typical user experience | < 100ms | Investigate common code paths |
| p95 | Power user / complex requests | < 300ms | Identify slow query patterns |
| p99 | Worst-case scenarios | < 500ms | Profile outliers, check GC pauses |
| p99.9 | Edge cases, cold starts | < 1s | Check connection pool exhaustion |

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
