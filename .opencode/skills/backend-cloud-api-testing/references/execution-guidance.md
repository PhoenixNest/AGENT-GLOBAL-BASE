# Execution Guidance

## Execution Guidance

### REST API Testing — Core Patterns

**1. Standard Test Suite (Python + pytest + httpx)**

```python
import pytest
import httpx
from pydantic import BaseModel
from typing import List, Optional

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    currency: str
    in_stock: bool
    category: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List[ProductResponse]
    total: int
    page: int
    page_size: int
    has_next: bool

BASE_URL = "https://api.staging.company.com/v1"

@pytest.fixture
def client(auth_token: str):
    return httpx.Client(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=10.0
    )

class TestProductAPI:
    """REST API test suite for Product endpoints."""

    def test_get_products_default_pagination(self, client):
        """Verify default pagination behavior."""
        response = client.get("/products")
        assert response.status_code == 200

        body = PaginatedResponse.model_validate(response.json())
        assert body.page == 1
        assert body.page_size == 20
        assert body.total >= 0
        assert isinstance(body.data, list)
        assert len(body.data) <= body.page_size

        # Verify schema for each item
        for product in body.data:
            assert product.id is not None
            assert product.name is not None
            assert product.price > 0
            assert product.currency in ["USD", "EUR", "GBP"]

    def test_get_products_custom_page_size(self, client):
        """Verify custom page size within bounds."""
        response = client.get("/products", params={"page_size": 5})
        assert response.status_code == 200

        body = response.json()
        assert body["page_size"] == 5
        assert len(body["data"]) <= 5

    def test_get_products_page_size_exceeds_max(self, client):
        """Verify server enforces maximum page size."""
        response = client.get("/products", params={"page_size": 1000})
        assert response.status_code in [200, 400]

        if response.status_code == 200:
            # Server silently caps — verify capped value
            assert response.json()["page_size"] <= 100
        else:
            # Server rejects — verify error schema
            error = response.json()
            assert "code" in error
            assert "message" in error
            assert error["code"] == "INVALID_PAGE_SIZE"

    def test_get_product_by_id_exists(self, client):
        """Verify single product retrieval."""
        # First get a valid product ID
        products = client.get("/products").json()
        product_id = products["data"][0]["id"]

        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200

        product = ProductResponse.model_validate(response.json())
        assert product.id == product_id

    def test_get_product_by_id_not_found(self, client):
        """Verify 404 for non-existent product."""
        response = client.get("/products/non-existent-id")
        assert response.status_code == 404

        error = response.json()
        assert error["code"] == "PRODUCT_NOT_FOUND"
        assert error["message"] is not None
        assert error["requestId"] is not None

    def test_create_product_valid_payload(self, client):
        """Verify product creation with valid data."""
        payload = {
            "name": "Test Product",
            "price": 29.99,
            "currency": "USD",
            "category": "electronics",
        }
        response = client.post("/products", json=payload)
        assert response.status_code == 201

        product = ProductResponse.model_validate(response.json())
        assert product.name == "Test Product"
        assert product.price == 29.99
        assert product.id is not None

    def test_create_product_invalid_payload(self, client):
        """Verify 422 for invalid product data."""
        payload = {
            "name": "",  # Empty name
            "price": -10,  # Negative price
        }
        response = client.post("/products", json=payload)
        assert response.status_code == 422

        error = response.json()
        assert error["code"] == "VALIDATION_ERROR"
        assert len(error["details"]) >= 2  # Both fields should have errors

    def test_create_product_unauthorized(self):
        """Verify 401 for missing auth token."""
        unauthenticated_client = httpx.Client(base_url=BASE_URL, timeout=10.0)
        response = unauthenticated_client.post(
            "/products",
            json={"name": "Test", "price": 10.0}
        )
        assert response.status_code == 401

    def test_delete_product_as_admin(self, client, admin_token):
        """Verify product deletion with admin role."""
        admin_client = httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {admin_token}"},
            timeout=10.0
        )

        # Create then delete
        create_resp = admin_client.post("/products", json={
            "name": "Delete Me", "price": 1.0, "currency": "USD"
        })
        product_id = create_resp.json()["id"]

        response = admin_client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # Verify deletion
        get_resp = admin_client.get(f"/products/{product_id}")
        assert get_resp.status_code == 404

    def test_filter_by_category(self, client):
        """Verify category filter returns matching products only."""
        response = client.get("/products", params={"category": "electronics"})
        assert response.status_code == 200

        products = response.json()["data"]
        for product in products:
            assert product["category"] == "electronics"
```

**2. Response Schema Validation with JSON Schema**

```python
import jsonschema

PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "currency", "in_stock"],
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "name": {"type": "string", "minLength": 1, "maxLength": 255},
        "price": {"type": "number", "minimum": 0},
        "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
        "in_stock": {"type": "boolean"},
        "category": {"type": ["string", "null"], "maxLength": 100},
    },
    "additionalProperties": False
}

def test_product_response_schema_compliance(client):
    """Verify all product responses match the declared schema."""
    response = client.get("/products")
    products = response.json()["data"]

    for product in products:
        jsonschema.validate(instance=product, schema=PRODUCT_SCHEMA)
```

### GraphQL Testing

**1. Query Testing with Variables**

```python
import pytest
import httpx

GRAPHQL_URL = "https://api.staging.company.com/graphql"

class TestProductGraphQL:
    def test_products_query_with_variables(self, auth_token):
        """Test paginated products query with variable injection."""
        query = """
        query GetProducts($page: Int!, $pageSize: Int!, $category: String) {
          products(page: $page, pageSize: $pageSize, category: $category) {
            data { id name price currency inStock }
            total
            page
            pageSize
            hasNext
          }
        }
        """
        variables = {"page": 1, "pageSize": 5, "category": "electronics"}

        response = httpx.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0
        )

        assert response.status_code == 200
        body = response.json()
        assert "errors" not in body

        data = body["data"]["products"]
        assert data["page"] == 1
        assert data["pageSize"] == 5
        assert len(data["data"]) <= 5

        for product in data["data"]:
            assert all(k in product for k in ["id", "name", "price", "currency", "inStock"])

    def test_mutation_create_product(self, auth_token):
        """Test product creation mutation."""
        mutation = """
        mutation CreateProduct($input: CreateProductInput!) {
          createProduct(input: $input) {
            id name price currency
          }
        }
        """
        variables = {
            "input": {
                "name": "GraphQL Product",
                "price": 49.99,
                "currency": "USD"
            }
        }

        response = httpx.post(
            GRAPHQL_URL,
            json={"query": mutation, "variables": variables},
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0
        )

        assert response.status_code == 200
        body = response.json()
        assert "errors" not in body

        product = body["data"]["createProduct"]
        assert product["name"] == "GraphQL Product"
        assert product["price"] == 49.99

    def test_partial_error_response(self, auth_token):
        """Test GraphQL returns partial data with errors for field-level failures."""
        query = """
        query {
          products(page: 1, pageSize: 1) {
            data {
              id
              name
              restrictedField  # This field requires admin scope
            }
          }
        }
        """

        response = httpx.post(
            GRAPHQL_URL,
            json={"query": query},
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10.0

```

        )

        body = response.json()
        # GraphQL returns partial data + errors
        assert "errors" in body
        assert body["data"] is not None  # Partial data still returned
        assert any("restrictedField" in err.get("path", []) for err in body["errors"])

    def test_introspection_schema_completeness(self):
        """Verify GraphQL schema exposes expected types."""
        introspection_query = """
        {
          __schema {
            types { name kind }
            queryType { name }
            mutationType { name }
          }
        }
        """

        response = httpx.post(GRAPHQL_URL, json={"query": introspection_query}, timeout=10.0)
        assert response.status_code == 200

        schema = response.json()["data"]["__schema"]
        type_names = [t["name"] for t in schema["types"]]

        assert "Product" in type_names
        assert "CreateProductInput" in type_names
        assert "Query" in type_names
        assert "Mutation" in type_names

````

**2. Subscription Testing (WebSocket)**

```python
import asyncio
from websockets import connect

async def test_order_status_subscription(auth_token):
    """Test real-time order status updates via GraphQL subscription."""
    subscription = """
    subscription OnOrderStatusChange($orderId: ID!) {
      orderStatusChanged(orderId: $orderId) {
        orderId
        status
        updatedAt
      }
    }
    """

    uri = "wss://api.staging.company.com/graphql"
    async with connect(uri, additional_headers={
        "Authorization": f"Bearer {auth_token}",
        "Sec-WebSocket-Protocol": "graphql-ws"
    }) as websocket:
        # Init subscription
        await websocket.send(json.dumps({
            "type": "connection_init",
            "payload": {"Authorization": f"Bearer {auth_token}"}
        }))

        # Wait for ack
        ack = await websocket.recv()
        assert json.loads(ack)["type"] == "connection_ack"

        # Send subscription
        await websocket.send(json.dumps({
            "id": "1",
            "type": "subscribe",
            "payload": {
                "query": subscription,
                "variables": {"orderId": "ORD-12345"}
            }
        }))

        # In production: trigger order status change via API, then wait for event
        # For test purposes, verify subscription was accepted
        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
        data = json.loads(response)
        assert data["type"] in ["next", "error", "complete"]
````

### OAuth 2.0 & JWT Testing

**1. OAuth 2.0 Authorization Code with PKCE**

```python
import hashlib
import base64
import secrets
import httpx

def generate_pkce_pair():
    """Generate PKCE code verifier and challenge."""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()
    return code_verifier, code_challenge

class TestOAuthFlow:
    def test_authorization_code_with_pkce(self):
        """Test complete OAuth 2.0 Authorization Code flow with PKCE."""
        code_verifier, code_challenge = generate_pkce_pair()
        state = secrets.token_urlsafe(16)

        # Step 1: Authorization request
        auth_url = (
            f"https://auth.staging.company.com/authorize?"
            f"response_type=code&"
            f"client_id=test_client&"
            f"redirect_uri=https://app.staging.company.com/callback&"
            f"scope=read write&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256&"
            f"state={state}"
        )

        # In automated test: use test user credentials to complete auth
        # This assumes a test identity provider endpoint
        token_response = httpx.post(
            "https://auth.staging.company.com/oauth/token",
            json={
                "grant_type": "authorization_code",
                "client_id": "test_client",
                "code": "test_auth_code",  # From test IdP
                "redirect_uri": "https://app.staging.company.com/callback",
                "code_verifier": code_verifier,
            },
            timeout=10.0
        )

        assert token_response.status_code == 200
        tokens = token_response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "expires_in" in tokens
        assert tokens["scope"] == "read write"

    def test_scope_enforcement(self):
        """Verify read-scoped token cannot access write endpoints."""
        read_token = get_token_with_scope("read")

        # Read endpoint — should work
        read_resp = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {read_token}"}
        )
        assert read_resp.status_code == 200

        # Write endpoint — should fail with 403
        write_resp = httpx.post(
            "https://api.staging.company.com/v1/products",
            json={"name": "Test", "price": 10.0},
            headers={"Authorization": f"Bearer {read_token}"}
        )
        assert write_resp.status_code == 403

    def test_token_revocation(self):
        """Verify revoked token is immediately rejected."""
        token = get_valid_token()

        # Revoke token
        revoke_resp = httpx.post(
            "https://auth.staging.company.com/oauth/revoke",
            json={"token": token},
            auth=("test_client", "client_secret")
        )
        assert revoke_resp.status_code == 200

        # Use revoked token — should get 401
        api_resp = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert api_resp.status_code == 401

    def test_jwt_algorithm_confusion_attack(self):
        """Verify server rejects HS256 when RS256 is expected."""
        import jwt

        # Get the public key (normally used for RS256 verification)
        public_key = get_auth_public_key()

        # Forge a token using HS256 with the public key as secret
        forged_payload = {"sub": "admin", "scope": "admin:all", "exp": 9999999999}
        forged_token = jwt.encode(forged_payload, public_key, algorithm="HS256")

        # Server should reject this
        response = httpx.get(
            "https://api.staging.company.com/v1/admin/users",
            headers={"Authorization": f"Bearer {forged_token}"}
        )
        assert response.status_code == 401

    def test_jwt_expired_token(self):
        """Verify expired JWT is rejected."""
        import jwt

        expired_payload = {
            "sub": "user123",
            "scope": "read",
            "exp": 1000000000,  # Expired timestamp
            "iss": "https://auth.staging.company.com",
            "aud": "https://api.staging.company.com"
        }
        expired_token = jwt.encode(expired_payload, get_signing_key(), algorithm="RS256")

        response = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
        assert response.json()["code"] == "TOKEN_EXPIRED"
```

### Rate Limiting Validation

```python
import time
import concurrent.futures

class TestRateLimiting:
    def test_rate_limit_headers(self, auth_token):
        """Verify rate limit headers are present and accurate."""
        response = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers

        limit = int(response.headers["X-RateLimit-Limit"])
        remaining = int(response.headers["X-RateLimit-Remaining"])
        assert remaining == limit - 1  # First request consumed

    def test_rate_limit_enforcement(self, auth_token):
        """Verify 429 returned when rate limit exceeded."""
        # Get rate limit from headers
        initial = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        remaining = int(initial.headers["X-RateLimit-Remaining"])

        # Exhaust remaining requests
        for _ in range(remaining):
            httpx.get(
                "https://api.staging.company.com/v1/products",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

        # Next request should be rate limited
        response = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 429
        assert "Retry-After" in response.headers

        retry_after = int(response.headers["Retry-After"])
        assert retry_after > 0

        error = response.json()
        assert error["code"] == "RATE_LIMIT_EXCEEDED"

    def test_rate_limit_reset(self, auth_token):
        """Verify rate limit resets after window expires."""
        # Exhaust rate limit
        exhaust_rate_limit(auth_token)

        # Wait for reset window
        time.sleep(61)  # Assuming 60-second window

        # Should be allowed again
        response = httpx.get(
            "https://api.staging.company.com/v1/products",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
```

### Performance Benchmarking

```python
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

class TestAPIPerformance:
    """Performance benchmarks for critical API endpoints."""

    WARMUP_REQUESTS = 5
    BENCHMARK_REQUESTS = 50
    CONCURRENT_USERS = 10

    def benchmark_endpoint(self, method, url, headers, json_body=None):
        """Run benchmark and return latency statistics."""
        latencies = []

        # Warmup
        for _ in range(self.WARMUP_REQUESTS):
            httpx.request(method, url, headers=headers, json=json_body, timeout=10.0)

        # Benchmark
        for _ in range(self.BENCHMARK_REQUESTS):
            start = time.perf_counter()
            response = httpx.request(method, url, headers=headers, json=json_body, timeout=10.0)
            elapsed = (time.perf_counter() - start) * 1000  # ms
            latencies.append(elapsed)
            assert response.status_code < 500

        return {
            "p50": statistics.median(latencies),
            "p95": sorted(latencies)[int(len(latencies) * 0.95)],
            "p99": sorted(latencies)[int(len(latencies) * 0.99)],
            "min": min(latencies),
            "max": max(latencies),
            "mean": statistics.mean(latencies),
            "total_requests": len(latencies),
        }

    def test_get_products_performance(self, auth_token):
        """Benchmark GET /products endpoint."""
        stats = self.benchmark_endpoint(
            "GET",
            "https://api.staging.company.com/v1/products",
            {"Authorization": f"Bearer {auth_token}"}
        )

        # Performance gates (CI will fail if exceeded)
        assert stats["p95"] < 500, f"p95 latency {stats['p95']:.0f}ms exceeds 500ms gate"
        assert stats["p99"] < 1000, f"p99 latency {stats['p99']:.0f}ms exceeds 1000ms gate"

        print(f"GET /products — p50: {stats['p50']:.0f}ms, p95: {stats['p95']:.0f}ms, p99: {stats['p99']:.0f}ms")

    def test_create_product_performance(self, auth_token):
        """Benchmark POST /products endpoint."""
        stats = self.benchmark_endpoint(
            "POST",
            "https://api.staging.company.com/v1/products",
            {"Authorization": f"Bearer {auth_token}"},
            {"name": "Benchmark Product", "price": 9.99, "currency": "USD"}
        )

        assert stats["p95"] < 800, f"p95 latency {stats['p95']:.0f}ms exceeds 800ms gate"

    def test_concurrent_users_performance(self, auth_token):
        """Benchmark under concurrent load."""
        def make_request():
            start = time.perf_counter()
            response = httpx.get(
                "https://api.staging.company.com/v1/products",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=10.0
            )
            return (time.perf_counter() - start) * 1000, response.status_code

        with ThreadPoolExecutor(max_workers=self.CONCURRENT_USERS) as executor:
            results = list(executor.map(lambda _: make_request(), range(50)))

        latencies = [r[0] for r in results]
        status_codes = [r[1] for r in results]

        assert all(code < 500 for code in status_codes), "Some requests returned 5xx"
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        assert p95 < 2000, f"Concurrent p95 latency {p95:.0f}ms exceeds 2000ms gate"
```
