# Execution Guidance

## Execution Guidance

### k6 Test Script Structure

**1. Basic Load Test**

```javascript
// checkout-load-test.js
import http from "k6/http";
import { check, sleep, group } from "k6";
import { Rate, Trend } from "k6/metrics";

// Custom metrics
const checkoutDuration = new Trend("checkout_duration", true);
const errorRate = new Rate("checkout_errors");

// Thresholds — CI gates
export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500", "p(99)<1000"],
    http_req_failed: ["rate<0.01"], // < 1% error rate
    checkout_duration: ["p(95)<2000"],
    checkout_errors: ["rate<0.05"],
    checks: ["rate>0.95"], // > 95% check pass rate
  },

  // Scenario: ramp from 1 to 50 VUs over 5 minutes, hold for 10 minutes
  scenarios: {
    checkout_flow: {
      executor: "ramping-vus",
      startVUs: 1,
      stages: [
        { duration: "5m", target: 50 }, // Ramp up
        { duration: "10m", target: 50 }, // Sustained load
        { duration: "3m", target: 0 }, // Ramp down
      ],
      gracefulRampDown: "30s",
      exec: "checkoutFlow",
    },
  },
};

// Shared data — loaded once in init context
const testUsers = JSON.parse(open("./testdata/users.json"));
const products = JSON.parse(open("./testdata/products.json"));

export function checkoutFlow() {
  const user = testUsers[__VU % testUsers.length];
  const product = products[Math.floor(Math.random() * products.length)];

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${user.token}`,
  };

  group("Checkout Flow", function () {
    // Step 1: Get product
    const productRes = http.get(
      `https://api.staging.company.com/v1/products/${product.id}`,
      {
        headers,
        tags: { step: "get_product" },
      },
    );

    check(productRes, {
      "product status is 200": (r) => r.status === 200,
      "product response < 300ms": (r) => r.timings.duration < 300,
      "product has price": (r) => JSON.parse(r.body).price > 0,
    });

    sleep(1);

    // Step 2: Create order
    const orderPayload = JSON.stringify({
      productId: product.id,
      quantity: 1,
      shippingAddress: user.address,
    });

    const orderStart = Date.now();
    const orderRes = http.post(
      "https://api.staging.company.com/v1/orders",
      orderPayload,
      {
        headers,
        tags: { step: "create_order" },
      },
    );
    const orderDuration = Date.now() - orderStart;
    checkoutDuration.add(orderDuration);

    check(orderRes, {
      "order status is 201": (r) => r.status === 201,
      "order response < 800ms": (r) => r.timings.duration < 800,
      "order has ID": (r) => JSON.parse(r.body).orderId !== undefined,
    });

    errorRate.add(orderRes.status >= 400);

    sleep(2);

    // Step 3: Process payment
    const orderId = JSON.parse(orderRes.body).orderId;
    const paymentPayload = JSON.stringify({
      orderId: orderId,
      paymentMethod: {
        type: "card",
        token: user.paymentToken,
      },
    });

    const paymentStart = Date.now();
    const paymentRes = http.post(
      "https://api.staging.company.com/v1/payments",
      paymentPayload,
      {
        headers,
        tags: { step: "process_payment" },
      },
    );
    const paymentDuration = Date.now() - paymentStart;

    check(paymentRes, {
      "payment status is 200": (r) => r.status === 200,
      "payment response < 1500ms": (r) => r.timings.duration < 1500,
      "payment confirmed": (r) => JSON.parse(r.body).status === "confirmed",
    });

    sleep(1);
  });
}

export function teardown() {
  console.log(`Test completed. Total VUs: ${__VUS}`);
}
```

**2. Multi-Scenario Test — Realistic Workload Mix**

```javascript
// mixed-workload-test.js
import http from "k6/http";
import { check, sleep, group } from "k6";
import { Trend, Counter } from "k6/metrics";

const apiLatency = new Trend("api_latency", true);
const activeUsers = new Counter("active_users");

export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500"],
    api_latency: ["p(95)<400"],
    http_req_failed: ["rate<0.01"],
  },

  scenarios: {
    // 70% of traffic: browsing products
    browse_products: {
      executor: "constant-vus",
      vus: 70,
      duration: "15m",
      exec: "browseProducts",
      gracefulStop: "10s",
    },

    // 20% of traffic: searching
    search: {
      executor: "constant-vus",
      vus: 20,
      duration: "15m",
      exec: "searchProducts",
      startTime: "1m", // Start 1 minute after browse
      gracefulStop: "10s",
    },

    // 10% of traffic: checkout (most resource-intensive)
    checkout: {
      executor: "ramping-vus",
      startVUs: 5,
      stages: [
        { duration: "5m", target: 10 },
        { duration: "5m", target: 10 },
      ],
      exec: "checkoutFlow",
      startTime: "2m",
      gracefulRampDown: "30s",
    },
  },

  // Global settings
  noVUConnectionReuse: false,
  discardResponseBodies: true, // Don't store response bodies in memory
  batch: 20,
  batchPerHost: 20,
};

export function browseProducts() {
  activeUsers.add(1);
  const res = http.get(
    "https://api.staging.company.com/v1/products?page=1&pageSize=20",
  );
  check(res, { "browse: status 200": (r) => r.status === 200 });
  apiLatency.add(res.timings.duration);
  sleep(Math.random() * 3 + 2); // 2-5 second think time
}

export function searchProducts() {
  activeUsers.add(1);
  const queries = ["phone", "laptop", "headphones", "tablet", "camera"];
  const query = queries[Math.floor(Math.random() * queries.length)];

  const res = http.get(
    `https://api.staging.company.com/v1/products/search?q=${query}`,
  );
  check(res, { "search: status 200": (r) => r.status === 200 });
  apiLatency.add(res.timings.duration);
  sleep(Math.random() * 2 + 1);
}

export function checkoutFlow() {
  activeUsers.add(1);
  // Full checkout flow (see checkout-load-test.js)
  const token = `Bearer test-token-vu-${__VU}`;
  const headers = { "Content-Type": "application/json", Authorization: token };

  const orderRes = http.post(
    "https://api.staging.company.com/v1/orders",
    JSON.stringify({ productId: "prod-test", quantity: 1 }),
    { headers },
  );
  check(orderRes, { "checkout: order created": (r) => r.status === 201 });
  apiLatency.add(orderRes.timings.duration);
  sleep(3);
}
```

**3. Spike Testing — Sudden Load Increase**

```javascript
// spike-test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  thresholds: {
    http_req_duration: ["p(95)<1000", "p(99)<2000"],
    http_req_failed: ["rate<0.05"], // Allow higher error rate during spike
  },

  scenarios: {
    spike: {
      executor: "ramping-vus",
      startVUs: 10,
      stages: [
        { duration: "2m", target: 10 }, // Normal load
        { duration: "30s", target: 200 }, // SPIKE — 20x increase
        { duration: "2m", target: 200 }, // Sustained spike
        { duration: "2m", target: 10 }, // Recovery
        { duration: "2m", target: 10 }, // Verify recovery
      ],
      gracefulRampDown: "30s",
      exec: "spikeTest",
    },
  },
};

export function spikeTest() {
  const res = http.get("https://api.staging.company.com/v1/products");
  check(res, {
    "status 200 or 429": (r) => r.status === 200 || r.status === 429,
  });
  sleep(1);
}
```

**4. Soak/Endurance Testing — Long-Running Load**

```javascript
// soak-test.js
import http from "k6/http";
import { check, sleep } from "k6";
import { Gauge } from "k6/metrics";

const memoryUsage = new Gauge("memory_usage_mb");

export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
    // Memory should not grow unbounded
    memory_usage_mb: ["value<512"],
  },

  scenarios: {
    soak: {
      executor: "constant-vus",
      vus: 30,

```

      duration: "4h", // 4-hour sustained load
      exec: "soakTest",
    },

},
};

export function soakTest() {
const res = http.get("https://api.staging.company.com/v1/products");
check(res, { "soak: status 200": (r) => r.status === 200 });

// Track response time trend over time
if (res.timings.duration > 1000) {
console.warn(
`Slow response detected: ${res.timings.duration}ms at iteration ${__ITER}`,
);
}

sleep(2);
}

````

### Distributed Execution

**1. k6 Cloud Execution**

```javascript
// Add to options for cloud execution
export const options = {
  ext: {
    loadimpact: {
      projectID: 123456,
      name: "Checkout Load Test — Staging",
      distribution: {
        "amazon:us:ashburn": { loadZone: "amazon:us:ashburn", percent: 50 },
        "amazon:ie:dublin": { loadZone: "amazon:ie:dublin", percent: 50 },
      },
    },
  },
  // ... rest of options
};
````

```bash
# Run on k6 Cloud
k6 cloud checkout-load-test.js

# Run with environment variables
k6 cloud checkout-load-test.js \
  --env BASE_URL=https://api.staging.company.com \
  --env ENVIRONMENT=staging
```

**2. Self-Hosted Distributed Mode**

```bash
# Coordinator node
k6 run --out json=results.json checkout-load-test.js \
  --execution-segment "0:1/3" \
  --execution-segment-sequence "0,1/3,2/3,1"

# Worker node 1
k6 run --out json=results-worker1.json checkout-load-test.js \
  --execution-segment "1/3:2/3" \
  --execution-segment-sequence "0,1/3,2/3,1"

# Worker node 2
k6 run --out json=results-worker2.json checkout-load-test.js \
  --execution-segment "2/3:1" \
  --execution-segment-sequence "0,1/3,2/3,1"

# Merge results
cat results.json results-worker1.json results-worker2.json | \
  k6 summarize --summary-export=merged-summary.json
```

### Result Analysis — InfluxDB + Grafana

**1. k6 Output to InfluxDB**

```bash
k6 run --out influxdb=http://localhost:8086/k6 checkout-load-test.js
```

**2. Grafana Dashboard Queries**

```
# p95 Response Time by Endpoint
SELECT percentile("value", 95) FROM "http_req_duration"
WHERE $timeFilter
GROUP BY "name", time(1m)

# Error Rate Over Time
SELECT mean("value") FROM "http_req_failed"
WHERE $timeFilter
GROUP BY time(1m)

# Requests Per Second
SELECT count("value") FROM "http_reqs"
WHERE $timeFilter
GROUP BY time(1m)

# Active Virtual Users
SELECT last("value") FROM "vus"
WHERE $timeFilter
GROUP BY time(1m)

# Custom Metric: Checkout Duration p95
SELECT percentile("value", 95) FROM "checkout_duration"
WHERE $timeFilter
GROUP BY time(1m)
```

**3. JSON Output Analysis (Python)**

```python
#!/usr/bin/env python3
"""Analyze k6 JSON output for performance regression detection."""

import json
import sys
from collections import defaultdict

def analyze_k6_results(json_file, baseline_file=None):
    """Parse k6 JSON output and produce summary statistics."""
    metrics = defaultdict(list)

    with open(json_file) as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'Point' and data.get('metric') == 'http_req_duration':
                    tags = data.get('data', {}).get('tags', {})
                    endpoint = tags.get('name', 'unknown')
                    duration = data.get('data', {}).get('value', 0)
                    metrics[endpoint].append(duration)
            except json.JSONDecodeError:
                continue

    summary = {}
    for endpoint, durations in metrics.items():
        durations.sort()
        n = len(durations)
        summary[endpoint] = {
            'count': n,
            'min': durations[0],
            'p50': durations[n // 2],
            'p95': durations[int(n * 0.95)],
            'p99': durations[int(n * 0.99)],
            'max': durations[-1],
            'mean': sum(durations) / n,
        }

    if baseline_file:
        with open(baseline_file) as f:
            baseline = json.load(f)

        print("\n=== Performance Regression Analysis ===\n")
        for endpoint, stats in summary.items():
            if endpoint in baseline:
                bl = baseline[endpoint]
                p95_change = ((stats['p95'] - bl['p95']) / bl['p95']) * 100
                p99_change = ((stats['p99'] - bl['p99']) / bl['p99']) * 100

                flag = "⚠️ REGRESSION" if p95_change > 20 else "✅ OK"
                print(f"{endpoint}:")
                print(f"  p95: {stats['p95']:.0f}ms (baseline: {bl['p95']:.0f}ms, change: {p95_change:+.1f}%) {flag}")
                print(f"  p99: {stats['p99']:.0f}ms (baseline: {bl['p99']:.0f}ms, change: {p99_change:+.1f}%)")
                print()

                if p95_change > 20:
                    print(f"  🚨 P1 DEFECT: p95 latency regression >20% on {endpoint}")
    else:
        print("\n=== Performance Summary ===\n")
        for endpoint, stats in summary.items():
            print(f"{endpoint}:")
            print(f"  count={stats['count']}, p50={stats['p50']:.0f}ms, "
                  f"p95={stats['p95']:.0f}ms, p99={stats['p99']:.0f}ms")

    return summary

if __name__ == '__main__':
    json_file = sys.argv[1]
    baseline = sys.argv[2] if len(sys.argv) > 2 else None
    analyze_k6_results(json_file, baseline)
```

### CI/CD Integration

```yaml
name: k6 Performance Tests
on:
  schedule:
    - cron: "0 2 * * *" # Daily at 02:00 UTC
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        default: "staging"

jobs:
  k6-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: performance/checkout-load-test.js
          flags: >
            --out json=k6-results.json
            --env BASE_URL=${{ github.event.inputs.environment == 'staging' && 'https://api.staging.company.com' || 'https://api.company.com' }}
        env:
          K6_CLOUD_TOKEN: ${{ secrets.K6_CLOUD_TOKEN }}

      - name: Analyze results against baseline
        run: |
          python3 scripts/analyze_k6_results.py \
            k6-results.json \
            performance/baselines/${{ github.event.inputs.environment || 'staging' }}-baseline.json

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: k6-results-${{ github.event.inputs.environment || 'staging' }}
          path: |
            k6-results.json
            k6-summary.json

      - name: Update baseline (on main branch)
        if: github.ref == 'refs/heads/main' && success()
        run: |
          python3 scripts/update_baseline.py \
            k6-results.json \
            performance/baselines/${{ github.event.inputs.environment || 'staging' }}-baseline.json
          git add performance/baselines/
          git commit -m "Update performance baseline" || true
          git push
```

### Bottleneck Identification Checklist

When performance regression is detected, systematically investigate:

| Area                | Diagnostic Command/Query               | What to Look For                                              |
| ------------------- | -------------------------------------- | ------------------------------------------------------------- |
| **Database**        | `EXPLAIN ANALYZE <query>` during load  | Sequential scans, missing indexes, high execution time        |
| **Connection Pool** | HikariCP/PgBouncer metrics             | Pool exhaustion, wait time > 100ms, active connections at max |
| **Memory**          | `heap dump` + MAT analysis during load | Growing heap, object retention, GC frequency increase         |
| **CPU**             | `top`, `pidstat`, `perf` during load   | CPU saturation > 80%, context switching, lock contention      |
| **Thread Pool**     | Tomcat/Undertow thread metrics         | Thread pool exhaustion, queue depth growth, rejected requests |
| **N+1 Queries**     | Query count per request ratio          | > 5 queries per request for simple endpoint                   |
| **Cache**           | Redis/Memcached hit rate during load   | Hit rate dropping below 80% under load                        |
| **Network**         | `netstat`, `ss` during load            | Connection queue overflow, TIME_WAIT accumulation             |
| **External APIs**   | Dependency response times during load  | Third-party API latency increase propagating to our endpoints |

### Performance Regression Detection Protocol

1. **Baseline Establishment**: Run k6 tests against stable production/staging environment; store results as baseline JSON
2. **Threshold Gates**: CI enforces p95 < SLA for every endpoint; thresholds defined per endpoint based on baseline
3. **Trend Analysis**: Weekly trend report shows latency trajectory; gradual degradation flagged before it breaches threshold
4. **Statistical Significance**: Regression confirmed with 3 consecutive runs showing >20% p95 increase
5. **Root Cause Assignment**: Regression assigned to team responsible for the code change (git blame + deployment timeline)
6. **Remediation SLA**: P1 performance regression (p95 > 2x baseline) must be fixed within 2 business days
7. **Verification**: Fix verified with k6 test showing p95 within 10% of baseline
