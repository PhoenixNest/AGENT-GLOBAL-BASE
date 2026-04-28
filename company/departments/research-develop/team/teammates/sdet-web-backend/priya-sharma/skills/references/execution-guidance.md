---
version: "1.0.0"
---

---------|-----------|------------------|-----------|---------

# MobileApp | 1.5.0 | ProductService | 2.3.1 | true

# MobileApp | 1.5.0 | OrderService | 1.8.0 | true

# If any verification fails:

# Computer says no ҉*\(°*°)\_/

# CONSUMER | C.VERSION | PROVIDER | P.VERSION | SUCCESS?

# ---------------|-----------|------------------|-----------|---------

# MobileApp | 1.5.0 | ProductService | 2.3.0 | VERIFICATION FAILED

#

# Verification failures:

# 1) ProductService with MobileApp

# GET /v1/products — Expected status 200 but received 500

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
````

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
