---
inclusion: manual
description: Testing/QA patterns, defect classification, and quality standards
---

# Quality Assurance Steering

This steering file provides testing and quality assurance guidance for the workspace. Activate manually when writing tests, conducting QA reviews, or classifying defects.

## QA Context

- **Testing Frameworks:** Jest, Vitest, Pytest, JUnit, XCTest, Espresso
- **E2E Testing:** Playwright, Cypress, Selenium
- **Test Coverage Target:** 80%+ for business logic
- **Defect Severity:** P0 (Critical) → P3 (Low)
- **Quality Gates:** Automated checks before merge and release

## Defect Severity Classification

### P0 — Critical (Blocks Release)

**Definition:** Crash, data loss, security breach, or complete feature failure

**Examples:**

- Application crashes on launch
- Data corruption or loss
- Security vulnerability (SQL injection, XSS)
- Payment processing failure
- Authentication bypass
- Complete loss of core functionality

**Response Time:** Immediate (within 1 hour)  
**Fix Timeline:** Same day  
**Approval Required:** User + CTO + CPO

### P1 — High (Blocks Release)

**Definition:** Core feature broken, major functionality impaired

**Examples:**

- Login fails for specific user types
- Critical user flow broken (checkout, signup)
- Major performance degradation (>5s load time)
- Data sync failures
- Push notifications not working

**Response Time:** Within 4 hours  
**Fix Timeline:** Within 24 hours  
**Approval Required:** User + relevant VP

### P2 — Medium (User Decides)

**Definition:** Non-critical feature broken, workaround exists

**Examples:**

- Minor UI glitches
- Non-critical feature not working
- Cosmetic issues
- Minor performance issues
- Edge case failures

**Response Time:** Within 1 business day  
**Fix Timeline:** Within 1 week  
**Approval Required:** User

### P3 — Low (User Decides)

**Definition:** Minor issues, nice-to-have improvements

**Examples:**

- Typos in UI text
- Minor visual inconsistencies
- Feature enhancement requests
- Documentation issues
- Non-critical logging issues

**Response Time:** Within 1 week  
**Fix Timeline:** Next sprint  
**Approval Required:** User

## Testing Strategy

### 1. Test Pyramid

```
        /\
       /E2E\         10% - End-to-End Tests
      /------\
     /Integr-\       20% - Integration Tests
    /----------\
   /   Unit     \    70% - Unit Tests
  /--------------\
```

### 2. Unit Testing

**What to Test:**

- Business logic
- Utility functions
- Data transformations
- Edge cases and error handling

**Best Practices:**

- Test one thing per test
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Aim for 80%+ coverage

**Example (Jest/TypeScript):**

```typescript
describe("calculateTotal", () => {
  it("should calculate total with tax", () => {
    // Arrange
    const items = [{ price: 100 }, { price: 200 }];
    const taxRate = 0.1;

    // Act
    const total = calculateTotal(items, taxRate);

    // Assert
    expect(total).toBe(330); // (100 + 200) * 1.1
  });

  it("should handle empty items array", () => {
    expect(calculateTotal([], 0.1)).toBe(0);
  });

  it("should throw error for negative tax rate", () => {
    expect(() => calculateTotal([{ price: 100 }], -0.1)).toThrow(
      "Tax rate must be non-negative",
    );
  });
});
```

### 3. Integration Testing

**What to Test:**

- API endpoints
- Database interactions
- External service integrations
- Component interactions

**Best Practices:**

- Use test databases
- Clean up test data after each test
- Test happy path and error scenarios
- Verify side effects

**Example (API Testing):**

```typescript
describe("POST /api/users", () => {
  beforeEach(async () => {
    await cleanDatabase();
  });

  it("should create a new user", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ name: "John Doe", email: "john@example.com" })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      name: "John Doe",
      email: "john@example.com",
    });

    // Verify in database
    const user = await db.users.findById(response.body.id);
    expect(user).toBeDefined();
  });

  it("should return 400 for invalid email", async () => {
    await request(app)
      .post("/api/users")
      .send({ name: "John Doe", email: "invalid-email" })
      .expect(400);
  });
});
```

### 4. End-to-End Testing

**What to Test:**

- Critical user flows
- Cross-browser compatibility
- Mobile responsiveness
- Real user scenarios

**Best Practices:**

- Test critical paths only
- Use page object pattern
- Run in CI/CD pipeline
- Test on real devices/browsers

**Example (Playwright):**

```typescript
test("user can complete checkout", async ({ page }) => {
  // Navigate to product page
  await page.goto("/products/123");

  // Add to cart
  await page.click('[data-testid="add-to-cart"]');

  // Go to checkout
  await page.click('[data-testid="cart-icon"]');
  await page.click('[data-testid="checkout-button"]');

  // Fill shipping info
  await page.fill('[name="address"]', "123 Main St");
  await page.fill('[name="city"]', "New York");
  await page.fill('[name="zip"]', "10001");

  // Complete purchase
  await page.click('[data-testid="place-order"]');

  // Verify success
  await expect(
    page.locator('[data-testid="order-confirmation"]'),
  ).toBeVisible();
});
```

### 5. Mobile Testing

**Android (Espresso):**

```kotlin
@Test
fun testLoginFlow() {
    // Enter email
    onView(withId(R.id.email_input))
        .perform(typeText("test@example.com"))

    // Enter password
    onView(withId(R.id.password_input))
        .perform(typeText("password123"))

    // Click login
    onView(withId(R.id.login_button))
        .perform(click())

    // Verify navigation to home
    onView(withId(R.id.home_screen))
        .check(matches(isDisplayed()))
}
```

**iOS (XCTest):**

```swift
func testLoginFlow() {
    let app = XCUIApplication()
    app.launch()

    // Enter email
    let emailField = app.textFields["email_input"]
    emailField.tap()
    emailField.typeText("test@example.com")

    // Enter password
    let passwordField = app.secureTextFields["password_input"]
    passwordField.tap()
    passwordField.typeText("password123")

    // Click login
    app.buttons["login_button"].tap()

    // Verify navigation
    XCTAssertTrue(app.otherElements["home_screen"].exists)
}
```

### 6. Performance Testing

**Load Testing (k6):**

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  stages: [
    { duration: "2m", target: 100 }, // Ramp up to 100 users
    { duration: "5m", target: 100 }, // Stay at 100 users
    { duration: "2m", target: 0 }, // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests under 500ms
    http_req_failed: ["rate<0.01"], // Error rate under 1%
  },
};

export default function () {
  let response = http.get("https://api.example.com/users");

  check(response, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

### 7. Security Testing

**SAST (Static Analysis):**

- Run SonarQube, Semgrep, or Checkmarx
- Scan for security vulnerabilities
- Enforce security rules in CI/CD

**DAST (Dynamic Analysis):**

- Run OWASP ZAP or Burp Suite
- Test running applications
- Scan for runtime vulnerabilities

**Dependency Scanning:**

- Run npm audit, Snyk, or Dependabot
- Check for known vulnerabilities
- Update vulnerable dependencies

## Test Automation

### 1. CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 2. Pre-commit Hooks

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm run test:unit && npm run lint",
      "pre-push": "npm run test:all"
    }
  }
}
```

## Quality Gates

### 1. Code Review Checklist

- [ ] All tests pass
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] No security vulnerabilities
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Accessibility standards met (WCAG 2.1 AA)

### 2. Release Checklist

- [ ] All P0/P1 defects resolved
- [ ] Regression testing complete
- [ ] Performance testing complete
- [ ] Security scan complete
- [ ] Accessibility audit complete
- [ ] User acceptance testing (UAT) complete
- [ ] Release notes prepared
- [ ] Rollback plan documented

## Test Data Management

### 1. Test Data Strategy

- **Synthetic Data:** Generate fake data for testing
- **Anonymized Data:** Use production data with PII removed
- **Fixtures:** Predefined test data sets
- **Factories:** Generate test data programmatically

### 2. Test Data Example

```typescript
// User factory
function createUser(overrides = {}) {
  return {
    id: faker.datatype.uuid(),
    name: faker.name.fullName(),
    email: faker.internet.email(),
    createdAt: faker.date.past(),
    ...overrides,
  };
}

// Usage
const user = createUser({ email: "test@example.com" });
```

## Defect Management

### 1. Defect Report Template

```markdown
## Defect Summary

Brief description of the issue

## Severity

P0 / P1 / P2 / P3

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## Expected Behavior

What should happen

## Actual Behavior

What actually happens

## Environment

- OS: Windows 11
- Browser: Chrome 120
- App Version: 1.2.3

## Screenshots/Logs

[Attach screenshots or logs]

## Impact

Who is affected and how
```

### 2. Defect Lifecycle

```
New → Assigned → In Progress → Fixed → Testing → Verified → Closed
                                    ↓
                                Reopened (if not fixed)
```

## Related Resources

- **Company Testing Standards:** `company/library/topics/testing.md`
- **Company Security Standards:** `company/library/topics/security.md`
- **Quality Assurance Skills:** `.kiro/skills/quality-assurance/`
- **Test Lead Profile:** `company/departments/research-develop/team/supervisors/test-lead/agent/profile.md`
- **Pipeline Stage 7:** Automated Testing
- **Pipeline Stage 8:** Integrity Verification

## When to Activate

Activate this steering file when:

- Writing unit, integration, or E2E tests
- Conducting QA reviews
- Classifying defect severity
- Reviewing test coverage
- Preparing for release (Stage 7-8)
- Investigating test failures
