# Go Testing

**Category:** Backend Quality Engineering (Go)
**Owner:** Backend Engineer (Omar Hassan)

## Overview

Implements comprehensive testing strategies for Go applications using table-driven tests, interface mocking with gomock and testify, integration testing with testcontainers, HTTP handler testing with httptest, and test coverage analysis. Ensures tests are deterministic, fast, and provide meaningful failure output.

## Competency Dimensions

| Dimension            | Description                                                   | Proficiency Indicators                                                                                                                    |
| -------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Table-Driven Tests   | Subtests with t.Run(), test case structs, descriptive naming  | Writes tests with descriptive subtest names; uses meaningful test case names for failure output; handles error expectations per test case |
| Interface Mocking    | gomock code generation, testify mock assertions, matchers     | Generates mocks with mockgen; writes explicit expectation sequences; uses matchers for flexible argument validation                       |
| Integration Testing  | testcontainers-go, real database setup, migration application | Spins up real PostgreSQL/Redis containers for tests; applies migrations before test execution; cleans up after tests                      |
| HTTP Handler Testing | httptest.ResponseRecorder, httptest.Server, request builders  | Tests handlers without starting real server; validates response status, headers, and body; tests middleware chains                        |
| Test Coverage        | go test -cover, coverage profiles, threshold enforcement      | Achieves > 80% coverage on business logic; identifies untested paths via coverage profiles; enforces coverage thresholds in CI            |

## Execution Guidance

### Table-Driven Tests

```go
func TestUserService_CreateUser(t *testing.T) {
    tests := []struct {
        name        string
        input       CreateUserInput
        mockSetup   func(m *MockUserRepository)
        wantID      string
        wantErr     bool
        wantErrType error
    }{
        {
            name: "valid input creates user",
            input: CreateUserInput{
                Name:  "John Doe",
                Email: "john@example.com",
                Role:  "user",
            },
            mockSetup: func(m *MockUserRepository) {
                m.EXPECT().
                    GetByEmail(gomock.Any(), "john@example.com").
                    Return(nil, sql.ErrNoRows)
                m.EXPECT().
                    Create(gomock.Any(), gomock.Any()).
                    DoAndReturn(func(ctx context.Context, u *User) error {
                        u.ID = "user-123"
                        return nil
                    })
            },
            wantID:  "user-123",
            wantErr: false,
        },
        {
            name: "duplicate email rejected",
            input: CreateUserInput{
                Name:  "John Doe",
                Email: "existing@example.com",
                Role:  "user",
            },
            mockSetup: func(m *MockUserRepository) {
                m.EXPECT().
                    GetByEmail(gomock.Any(), "existing@example.com").
                    Return(&User{ID: "existing-user"}, nil)
            },
            wantErr:     true,
            wantErrType: ErrDuplicate,
        },
        {
            name: "invalid email rejected",
            input: CreateUserInput{
                Name:  "John Doe",
                Email: "not-an-email",
                Role:  "user",
            },
            mockSetup:   func(m *MockUserRepository) {}, // No DB call expected
            wantErr:     true,
            wantErrType: ErrInvalidInput,
        },
        {
            name: "database error propagated",
            input: CreateUserInput{
                Name:  "John Doe",
                Email: "john@example.com",
                Role:  "user",
            },
            mockSetup: func(m *MockUserRepository) {
                m.EXPECT().
                    GetByEmail(gomock.Any(), "john@example.com").
                    Return(nil, sql.ErrNoRows)
                m.EXPECT().
                    Create(gomock.Any(), gomock.Any()).
                    Return(errors.New("connection refused"))
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            ctrl := gomock.NewController(t)
            defer ctrl.Finish()

            mockRepo := NewMockUserRepository(ctrl)
            tt.mockSetup(mockRepo)

            service := NewUserService(mockRepo)
            user, err := service.CreateUser(context.Background(), tt.input)

            if tt.wantErr {
                assert.Error(t, err)
                if tt.wantErrType != nil {
                    assert.ErrorIs(t, err, tt.wantErrType)
                }
                return
            }

            assert.NoError(t, err)
            assert.Equal(t, tt.wantID, user.ID)
        })
    }
}
```

### Interface Mocking with gomock

**Generate mocks:**

```bash
# Generate mock from interface
mockgen -source=internal/repository/user.go \
    -destination=internal/repository/mock_user_repository.go \
    -package=repository \
    -mock_names=UserRepository=MockUserRepository
```

**Advanced mock patterns:**

```go
// Using gomock matchers
func TestComplexScenario(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := NewMockUserRepository(ctrl)

    // Match any context
    mockRepo.EXPECT().
        GetByID(gomock.Any(), "user-123").
        Return(&User{ID: "user-123"}, nil)

    // Match specific values with custom matcher
    emailMatcher := gomock.Cond(func(x any) bool {
        email := x.(string)
        return strings.HasSuffix(email, "@company.com")
    })
    mockRepo.EXPECT().
        GetByEmail(gomock.Any(), emailMatcher).
        Return(nil, sql.ErrNoRows)

    // DoAndReturn for dynamic responses
    mockRepo.EXPECT().
        Create(gomock.Any(), gomock.Any()).
        DoAndReturn(func(ctx context.Context, user *User) error {
            user.ID = uuid.New().String()
            user.CreatedAt = time.Now()
            return nil
        })

    // Call order enforcement (InOrder)
    gomock.InOrder(
        mockRepo.EXPECT().BeginTx(gomock.Any()).Return(tx, nil),
        mockRepo.EXPECT().Create(gomock.Any(), gomock.Any()).Return(nil),
        mockRepo.EXPECT().CommitTx(gomock.Any()).Return(nil),
    )
}
```

**testify mock alternative (simpler, less type-safe):**

```go
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) GetByID(ctx context.Context, id string) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Create(ctx context.Context, user *User) error {
    args := m.Called(ctx, user)
    return args.Error(0)
}

// Usage
func TestWithTestify(t *testing.T) {
    mockRepo := new(MockUserRepository)

    mockRepo.On("GetByEmail", mock.Anything, "test@test.com").
        Return(nil, sql.ErrNoRows)
    mockRepo.On("Create", mock.Anything, mock.MatchedBy(func(u *User) bool {
        return u.Email == "test@test.com"
    })).Return(nil)

    service := NewUserService(mockRepo)
    result, err := service.CreateUser(context.Background(), CreateUserInput{
        Email: "test@test.com",
    })

    assert.NoError(t, err)
    mockRepo.AssertExpectations(t)
    mockRepo.AssertNumberOfCalls(t, "Create", 1)
}
```

### HTTP Handler Testing

```go
func TestUserHandler_GetUser(t *testing.T) {
    tests := []struct {
        name         string
        userID       string
        mockSetup    func(m *MockUserService)
        wantStatus   int
        wantBody     string
    }{
        {
            name:   "existing user returns 200",
            userID: "user-123",
            mockSetup: func(m *MockUserService) {
                m.EXPECT().
                    GetUser(gomock.Any(), "user-123").
                    Return(&User{ID: "user-123", Name: "Test User", Email: "test@test.com"}, nil)
            },
            wantStatus: http.StatusOK,
            wantBody:   `"id":"user-123"`,
        },
        {
            name:   "missing user returns 404",
            userID: "nonexistent",
            mockSetup: func(m *MockUserService) {
                m.EXPECT().
                    GetUser(gomock.Any(), "nonexistent").
                    Return(nil, ErrNotFound)
            },
            wantStatus: http.StatusNotFound,
            wantBody:   `"code":"not_found"`,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            ctrl := gomock.NewController(t)
            defer ctrl.Finish()

            mockService := NewMockUserService(ctrl)
            tt.mockSetup(mockService)

            handler := NewUserHandler(mockService, zap.NewNop())

            // Create test request
            req := httptest.NewRequest("GET", "/users/"+tt.userID, nil)
            rec := httptest.NewRecorder()

            handler.GetUser(rec, req)

            // Assert response
            assert.Equal(t, tt.wantStatus, rec.Code)
            assert.Contains(t, rec.Body.String(), tt.wantBody)
            assert.Equal(t, "application/json", rec.Header().Get("Content-Type"))
        })
    }
}

// Test with httptest.Server (for middleware chains)
func TestMiddlewareChain(t *testing.T) {
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := GetRequestID(r.Context())
        w.Header().Set("X-Request-ID", requestID)
        w.WriteHeader(http.StatusOK)
    })

    chain := RequestIDMiddleware(handler)

    server := httptest.NewServer(chain)
    defer server.Close()

    resp, err := http.Get(server.URL + "/test")
    require.NoError(t, err)
    defer resp.Body.Close()

    assert.Equal(t, http.StatusOK, resp.StatusCode)
    assert.NotEmpty(t, resp.Header.Get("X-Request-ID"))
}

// Test middleware in isolation
func TestAuthMiddleware_Unauthorized(t *testing.T) {
    nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        t.Error("Next handler should not be called")
    })

    middleware := AuthMiddleware(nextHandler, &Authenticator{})

    req := httptest.NewRequest("GET", "/users", nil)
    rec := httptest.NewRecorder()

    middleware.ServeHTTP(rec, req)

    assert.Equal(t, http.StatusUnauthorized, rec.Code)
    assert.Contains(t, rec.Body.String(), "missing_token")
}
```

### Integration Testing with Testcontainers

```go
func TestUserRepository_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test in short mode")
    }

    ctx := context.Background()

    // Start PostgreSQL container
    pg, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("testuser"),
        postgres.WithPassword("testpass"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections").
                WithOccurrence(2).WithStartupTimeout(30*time.Second)),
    )
    require.NoError(t, err)
    t.Cleanup(func() {
        require.NoError(t, pg.Terminate(ctx))
    })

    // Get connection string
    connStr, err := pg.ConnectionString(ctx, "sslmode=disable")
    require.NoError(t, err)

    // Connect and run migrations
    db, err := sql.Open("postgres", connStr)
    require.NoError(t, err)
    defer db.Close()

    // Run migrations
    require.NoError(t, runMigrations(db))

    // Create repository
    repo := NewUserRepository(db)

    t.Run("Create and Retrieve", func(t *testing.T) {
        // Truncate before test
        _, err := db.ExecContext(ctx, "TRUNCATE users CASCADE")
        require.NoError(t, err)

        user := &User{
            Name:  "Integration Test",
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
}

// Helper: run migrations
func runMigrations(db *sql.DB) error {
    runner, err := migrate.NewWithDatabaseInstance(
        "file://migrations",
        "postgres",
        db,
    )
    if err != nil {
        return err
    }
    return runner.Up()
}
```

### Test Coverage Analysis

```bash
# Run tests with coverage
go test ./... -coverprofile=coverage.out

# View coverage in terminal
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# Coverage by package
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total

# Enforce coverage threshold in CI
go test ./... -coverprofile=coverage.out
TOTAL=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
if (( $(echo "$TOTAL < 80" | bc -l) )); then
    echo "Coverage $TOTAL% is below threshold of 80%"
    exit 1
fi
```

**Coverage CI configuration:**

```yaml
# .github/workflows/test.yml
- name: Run Tests with Coverage
  run: |
    go test ./... -coverprofile=coverage.out -covermode=atomic -race -v

- name: Check Coverage Threshold
  uses: vladopajic/go-test-coverage@v2
  with:
    config: ./.testcoverage.yml
    # Fail if coverage below threshold
    threshold-total: 80
    threshold-file: 70
```

**.testcoverage.yml:**

```yaml
threshold:
  file: 70
  package: 75
  total: 80

exclude:
  paths:
    - "mock_.*\\.go$"
    - ".*_test\\.go$"
    - "cmd/"
```

### Test Best Practices

```go
// 1. Use t.Cleanup instead of defer in tests
func TestWithCleanup(t *testing.T) {
    dir := t.TempDir() // Automatically cleaned up
    db := setupTestDB(t)
    t.Cleanup(func() {
        db.Close()
    })

    // Test logic...
}

// 2. Parallel tests (when no shared state)
func TestParallel(t *testing.T) {
    t.Parallel()
    // This test runs in parallel with other t.Parallel() tests
}

// 3. Golden file testing for complex outputs
func TestGoldenFile(t *testing.T) {
    result := GenerateComplexReport()

    goldenPath := "testdata/golden/report.json"
    if *update {
        os.WriteFile(goldenPath, result, 0644)
    }

    expected, _ := os.ReadFile(goldenPath)
    assert.JSONEq(t, string(expected), string(result))
}

// 4. Benchmark tests
func BenchmarkUserService_CreateUser(b *testing.B) {
    ctrl := gomock.NewController(b)
    mockRepo := NewMockUserRepository(ctrl)
    mockRepo.EXPECT().
        GetByEmail(gomock.Any(), gomock.Any()).
        Return(nil, sql.ErrNoRows).
        AnyTimes()
    mockRepo.EXPECT().
        Create(gomock.Any(), gomock.Any()).
        Return(nil).
        AnyTimes()

    service := NewUserService(mockRepo)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        service.CreateUser(context.Background(), CreateUserInput{
            Name:  "Benchmark User",
            Email: fmt.Sprintf("bench-%d@test.com", i),
        })
    }
}
```

## Pipeline Integration

**Stage 5 (Development):** Tests written alongside implementation. Table-driven tests for all business logic. HTTP handler tests for all endpoints. Integration tests for repository layer.

**Stage 6 (Code Review):** Review validates test coverage meets threshold. Mock usage is correct (no over-mocking). Integration tests cover critical database interactions. Test names are descriptive.

**Stage 7 (Testing):** Full test suite runs in CI with coverage reporting. Race detector enabled (`-race`). Benchmarks establish performance baselines.

## Quality Standards

| Metric                              | Target                                         | Measurement                       |
| ----------------------------------- | ---------------------------------------------- | --------------------------------- |
| Unit test coverage (total)          | > 80%                                          | go test -cover                    |
| Unit test coverage (business logic) | > 90%                                          | Per-package coverage analysis     |
| Test execution time                 | < 5 minutes (unit), < 15 minutes (integration) | CI pipeline duration              |
| Flaky test rate                     | 0%                                             | Test retry analysis               |
| Race detector findings              | 0                                              | go test -race                     |
| Mock expectation violations         | 0                                              | gomock/testify assertion failures |
| Benchmark regression                | < 10% degradation                              | Benchmark comparison              |
