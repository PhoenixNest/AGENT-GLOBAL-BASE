# Execution Guidance

## Execution Guidance

### Consumer-Side Pact Tests

**1. JavaScript Consumer Test (Node.js + Jest)**

```javascript
const {
  PactV4,
  MatchersV3,
  SpecificationVersion,
} = require("@pact-foundation/pact");
const path = require("path");
const axios = require("axios");

const { somethingLike, eachLike, regex, integer, string } = MatchersV3;

// Product API consumer test — mobile app consuming product service
const productApiPact = new PactV4({
  consumer: "MobileApp",
  provider: "ProductService",
  dir: path.resolve(process.cwd(), "pacts"),
  spec: SpecificationVersion.SPECIFICATION_VERSION_V3,
  log: path.resolve(process.cwd(), "logs", "pact.log"),
  logLevel: "info",
  host: "127.0.0.1",
});

describe("Product Service API Contract", () => {
  describe("GET /products", () => {
    it("returns a list of products", async () => {
      // Define the expected interaction
      await productApiPact
        .given("products exist in the database")
        .uponReceiving("a request for products")
        .withRequest({
          method: "GET",
          path: "/v1/products",
          headers: {
            Authorization: regex("Bearer [a-zA-Z0-9_-]+", "Bearer valid-token"),
            Accept: "application/json",
          },
          query: {
            page: "1",
            pageSize: "20",
          },
        })
        .willRespondWith({
          status: 200,
          headers: { "Content-Type": "application/json" },
          body: {
            data: eachLike(
              {
                id: string("prod-abc123"),
                name: string("Test Product"),
                price: integer(2999), // Price in cents
                currency: regex("[A-Z]{3}", "USD"),
                inStock: somethingLike(true),
                category: somethingLike("electronics"),
              },
              { min: 1 },
            ),
            total: integer(150),
            page: integer(1),
            pageSize: integer(20),
            hasNext: somethingLike(true),
          },
        })
        .executeTest(async (mockServer) => {
          // Make the actual request to the mock server
          const response = await axios.get(`${mockServer.url}/v1/products`, {
            headers: {
              Authorization: "Bearer valid-token",
              Accept: "application/json",
            },
            params: { page: 1, pageSize: 20 },
          });

          expect(response.status).toBe(200);
          expect(response.data.data).toHaveLength(1);
          expect(response.data.data[0]).toHaveProperty("id");
          expect(response.data.data[0]).toHaveProperty("name");
          expect(response.data.data[0]).toHaveProperty("price");
        });
    });
  });

  describe("POST /products", () => {
    it("creates a new product", async () => {
      await productApiPact
        .given("user has admin permissions")
        .uponReceiving("a request to create a product")
        .withRequest({
          method: "POST",
          path: "/v1/products",
          headers: {
            Authorization: regex("Bearer [a-zA-Z0-9_-]+", "Bearer admin-token"),
            "Content-Type": "application/json",
          },
          body: {
            name: string("New Product"),
            price: integer(4999),
            currency: string("USD"),
          },
        })
        .willRespondWith({
          status: 201,
          headers: { "Content-Type": "application/json" },
          body: {
            id: string("prod-new123"),
            name: string("New Product"),
            price: integer(4999),
            currency: string("USD"),
            inStock: somethingLike(false),
          },
        })
        .ExecuteTest(async (mockServer) => {
          const response = await axios.post(
            `${mockServer.url}/v1/products`,
            {
              name: "New Product",
              price: 4999,
              currency: "USD",
            },
            {
              headers: {
                Authorization: "Bearer admin-token",
                "Content-Type": "application/json",
              },
            },
          );

          expect(response.status).toBe(201);
          expect(response.data).toHaveProperty("id");
        });
    });
  });

  describe("GET /products/:id — Not Found", () => {
    it("returns 404 for non-existent product", async () => {
      await productApiPact
        .given("product does not exist")
        .uponReceiving("a request for a non-existent product")
        .withRequest({
          method: "GET",
          path: "/v1/products/non-existent-id",
          headers: { Authorization: regex("Bearer .+", "Bearer token") },
        })
        .willRespondWith({
          status: 404,
          headers: { "Content-Type": "application/json" },
          body: {
            code: string("PRODUCT_NOT_FOUND"),
            message: string("Product not found"),
            requestId: regex(
              "[a-f0-9-]{36}",
              "550e8400-e29b-41d4-a716-446655440000",
            ),
          },
        })
        .ExecuteTest(async (mockServer) => {
          try {
            await axios.get(`${mockServer.url}/v1/products/non-existent-id`, {
              headers: { Authorization: "Bearer token" },
            });
            fail("Expected 404 error");
          } catch (error) {
            expect(error.response.status).toBe(404);
            expect(error.response.data.code).toBe("PRODUCT_NOT_FOUND");
          }
        });
    });
  });
});
```

**2. Publishing Pacts to Broker**

```bash
# Publish pacts after consumer tests pass
npx pact-broker publish pacts/ \
  --consumer-app-version 1.5.0 \
  --branch main \
  --tag main \
  --tag prod \
  --broker-base-url https://pact-broker.company.com \
  --broker-username $PACT_BROKER_USERNAME \
  --broker-password $PACT_BROKER_PASSWORD

# Tag a specific version for release
npx pact-broker create-version-tag \
  --pacticipant MobileApp \
  --version 1.5.0 \
  --tag release-candidate \
  --broker-base-url https://pact-broker.company.com \
  --broker-username $PACT_BROKER_USERNAME \
  --broker-password $PACT_BROKER_PASSWORD
```

### Provider-Side Verification

**1. Provider Verification Test (Node.js)**

```javascript
const { Verifier } = require("@pact-foundation/pact");
const path = require("path");

// Provider state handlers
const stateHandlers = {
  "products exist in the database": async () => {
    // Seed test database with products
    await db.products.insertMany([
      {
        id: "prod-abc123",
        name: "Test Product",
        price: 2999,
        currency: "USD",
        inStock: true,
        category: "electronics",
      },
    ]);
    return { productCount: 1 };
  },
  "user has admin permissions": async () => {
    // Set up admin user context
    await db.users.upsert({ id: "admin-1", role: "admin" });
    return { userId: "admin-1", role: "admin" };
  },
  "product does not exist": async () => {
    // Ensure product is not in database
    await db.products.deleteOne({ id: "non-existent-id" });
    return {};
  },
};

describe("ProductService Provider", () => {
  it("validates pact with MobileApp consumer", async () => {
    const config = {
      provider: "ProductService",
      providerBaseUrl: "http://localhost:3000",
      pactBrokerUrl: "https://pact-broker.company.com",
      pactBrokerUsername: process.env.PACT_BROKER_USERNAME,
      pactBrokerPassword: process.env.PACT_BROKER_PASSWORD,

      // Verify only pacts from main branch of consumer
      consumerVersionSelectors: [
        { tag: "main", latest: true },
        { tag: "prod", latest: true },
      ],

      // Provider version tracking
      providerVersion: process.env.PROVIDER_VERSION || "1.0.0",
      providerVersionBranch: process.env.GIT_BRANCH || "main",

      // State handlers
      stateHandlers,

      // Request filters (e.g., add auth middleware for provider verification)
      requestFilter: (req, res, next) => {
        // Add test auth bypass
        req.headers["x-test-mode"] = "true";
        next();
      },

      // Enable pending pacts (consumer tests written before provider implementation)
      enablePending: true,
      includeWipPactsSince: "2026-01-01",
    };

    const output = await new Verifier(config).verifyProvider();
    expect(output).toBeTruthy();
  });
});
```

**2. Provider Verification (Java/Spring Boot)**

```java
package com.company.productservice.pact;

import au.com.dius.pact.provider.junit5.PactVerificationContext;
import au.com.dius.pact.provider.junit5.PactVerificationInvocationContextProvider;
import au.com.dius.pact.provider.junitsupport.Provider;
import au.com.dius.pact.provider.junitsupport.loader.PactBroker;
import au.com.dius.pact.provider.junitsupport.loader.PactBrokerAuth;
import au.com.dius.pact.provider.junitsupport.State;
import au.com.dius.pact.provider.junitsupport.StateChangeAction;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestTemplate;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.boot.test.web.server.LocalServerPort;

@Provider("ProductService")
@PactBroker(
    url = "${pact.broker.url:https://pact-broker.company.com}",

```

    authentication = @PactBrokerAuth(
        username = "${pact.broker.username}",
        password = "${pact.broker.password}"
    )

)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class ProductServicePactTest {

    @LocalServerPort
    private int port;

    @DynamicPropertySource
    static void properties(DynamicPropertyRegistry registry) {
        registry.add("server.port", () -> 0);
    }

    @BeforeEach
    void setup(PactVerificationContext context) {
        context.setTarget(new HttpsTestTarget("localhost", port, "/"));
    }

    @State("products exist in the database")
    public void productsExist() {
        // Seed database
        productRepository.save(new Product("prod-abc123", "Test Product", 2999, "USD", true));
    }

    @State("user has admin permissions")
    public void userHasAdminPermissions() {
        // Set up admin context
        securityContext.setAuthentication(new AdminAuthentication());
    }

    @State("product does not exist")
    public void productDoesNotExist() {
        productRepository.deleteById("non-existent-id");
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void pactVerificationTestTemplate(PactVerificationContext context) {
        context.verifyInteraction();
    }

}

````

### can-i-deploy Gate

```bash
# Check if consumer version is safe to deploy
npx pact-broker can-i-deploy \
  --pacticipant MobileApp \
  --version 1.5.0 \
  --to-environment production \
  --broker-base-url https://pact-broker.company.com \
  --broker-username $PACT_BROKER_USERNAME \
  --broker-password $PACT_BROKER_PASSWORD

# Output:
# Computer says yes \o/
# CONSUMER       | C.VERSION | PROVIDER         | P.VERSION | SUCCESS?
# ---------------|-----------|------------------|-----------|---------
# MobileApp      | 1.5.0     | ProductService   | 2.3.1     | true
# MobileApp      | 1.5.0     | OrderService     | 1.8.0     | true

# If any verification fails:
# Computer says no ҉_\(°_°)_/
# CONSUMER       | C.VERSION | PROVIDER         | P.VERSION | SUCCESS?
# ---------------|-----------|------------------|-----------|---------
# MobileApp      | 1.5.0     | ProductService   | 2.3.0     | VERIFICATION FAILED
#
# Verification failures:
# 1) ProductService with MobileApp
#    GET /v1/products — Expected status 200 but received 500
````

### Pending Pacts Workflow

Pending pacts enable consumer-driven development where the consumer team writes contract tests before the provider has implemented the changes:

```bash
# Consumer publishes a pact that the provider cannot yet satisfy
npx pact-broker publish pacts/ \
  --consumer-app-version 1.6.0 \
  --branch feature/new-endpoint \
  --tag feature/new-endpoint \
  --broker-base-url https://pact-broker.company.com

# Provider verification runs but pact is marked as "pending"
# (not blocking the build) because:
# 1. The pact was published from a non-main branch
# 2. enablePending: true is configured in provider verification

# When provider implements the change:
# 1. Provider verification passes
# 2. Pact status changes from "pending" to "verified"
# 3. Consumer can safely merge feature branch to main
```

### CI/CD Integration — GitHub Actions

**Consumer Pipeline:**

```yaml
name: Consumer Pact Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  pact-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Run Pact consumer tests
        run: npm run test:pact

      - name: Publish pacts to Broker
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker publish pacts/ \
            --consumer-app-version ${{ github.sha }} \
            --branch main \
            --tag main \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-username ${{ secrets.PACT_BROKER_USERNAME }} \
            --broker-password ${{ secrets.PACT_BROKER_PASSWORD }}

      - name: Can I Deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant MobileApp \
            --version ${{ github.sha }} \
            --to-environment production \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-username ${{ secrets.PACT_BROKER_USERNAME }} \
            --broker-password ${{ secrets.PACT_BROKER_PASSWORD }}
```

**Provider Pipeline:**

```yaml
name: Provider Pact Verification
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  # Triggered by webhook when consumer publishes new pact
  repository_dispatch:
    types: [pact_changed]

jobs:
  verify-pacts:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Seed test database
        run: npm run db:seed:test

      - name: Start provider service
        run: npm start &
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/test_db
          NODE_ENV: test

      - name: Verify pacts
        run: npm run test:pact:verify
        env:
          PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_USERNAME: ${{ secrets.PACT_BROKER_USERNAME }}
          PACT_BROKER_PASSWORD: ${{ secrets.PACT_BROKER_PASSWORD }}
          PROVIDER_VERSION: ${{ github.sha }}
          GIT_BRANCH: ${{ github.head_ref || github.ref_name }}
```

### Pact Broker Webhooks

Configure webhooks to notify teams when contracts change:

```bash
# Webhook: Notify provider team when consumer publishes new pact
npx pact-broker create-webhook \
  --request POST \
  --url https://hooks.slack.com/services/xxx/provider-contract-changes \
  --header 'Content-Type: application/json' \
  --data '{"text": "New pact published: ${pactbroker.consumerName} v${pactbroker.consumerVersionNumber} → ${pactbroker.providerName}"}' \
  --description "Slack notification for new consumer pacts" \
  --contract-content-type json \
  --broker-base-url https://pact-broker.company.com

# Webhook: Trigger provider CI verification
npx pact-broker create-webhook \
  --request POST \
  --url https://api.github.com/repos/company/product-service/dispatches \
  --header 'Content-Type: application/json' \
  --header 'Authorization: token $GITHUB_TOKEN' \
  --data '{"event_type": "pact_changed", "client_payload": {"consumer": "${pactbroker.consumerName}", "version": "${pactbroker.consumerVersionNumber}"}}' \
  --description "Trigger provider verification on pact change" \
  --contract-content-type json \
  --broker-base-url https://pact-broker.company.com
```

### Matching Rules Reference

| Matcher                          | Use Case                                     | Example                                   |
| -------------------------------- | -------------------------------------------- | ----------------------------------------- |
| `somethingLike(value)`           | Match type and value, allow different values | `somethingLike(2999)` matches any integer |
| `like(value)`                    | Match type only, allow different values      | `like("USD")` matches any string          |
| `regex(pattern, example)`        | Match against regex pattern                  | `regex('[A-Z]{3}', 'USD')`                |
| `eachLike(template, {min, max})` | Validate array item structure                | `eachLike({id: string()}, {min: 1})`      |
| `integer(example)`               | Match integer type                           | `integer(2999)`                           |
| `string(example)`                | Match string type                            | `string("product-name")`                  |
| `boolean()`                      | Match boolean type                           | `boolean()`                               |
| `decimal(example)`               | Match float/decimal type                     | `decimal(29.99)`                          |
