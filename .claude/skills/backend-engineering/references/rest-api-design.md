---
name: rest-api-design
description: Design RESTful APIs with OpenAPI 3.0 specifications, including resource modeling, request validation, pagination, versioning, and error handling.
version: "1.0.0"
---

# REST API Design

| Competency         | Description                                                           | Quality Criteria                                                                                                                             |
| ------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Resource Modeling  | URI design, noun-based resources, sub-resource relationships          | Uses plural nouns, not verbs; sub-resources express ownership (e.g. `/orders/{id}/items`); avoids deeply nested paths beyond 2 levels        |
| HTTP Semantics     | Correct method assignment, idempotency guarantees, status code usage  | GET is safe and idempotent; PUT/DELETE are idempotent; PATCH is partial; status codes match RFC 7231 semantics; no 200 with error body       |
| OpenAPI 3.0 Spec   | Schema authoring, component reuse, security scheme definition         | All schemas in `components/schemas`; no inline schema duplication; `$ref` used throughout; spec passes `spectral` linting without errors     |
| Request Validation | Input validation at the boundary before business logic                | All path/query/body params validated before handler logic runs; 400 returned with field-level error details; schema validation is exhaustive |
| Pagination         | Cursor-based and offset pagination patterns, response envelope design | Cursor pagination for large/live datasets; offset for stable datasets; Link header (RFC 5988) provided; total count optional not mandatory   |
| Error Handling     | RFC 7807 Problem Details format, consistent error taxonomy            | All errors return `application/problem+json`; `type` URI is stable; `detail` is human-readable; machine-readable `code` field present        |
| API Versioning     | URL versioning, header versioning, deprecation lifecycle              | Breaking changes require a new major version; v1 sunset date published ≥ 6 months before removal; `Deprecation` header emitted on old paths  |

## Execution Guidance

### Resource Naming and URI Design

**Core rules:**

| Rule                                | Correct                    | Incorrect                              |
| ----------------------------------- | -------------------------- | -------------------------------------- |
| Use nouns, not verbs                | `POST /orders`             | `POST /createOrder`                    |
| Use plural forms                    | `/users/{id}`              | `/user/{id}`                           |
| Sub-resources for ownership         | `/orders/{id}/items`       | `/order-items?orderId={id}`            |
| Nest max 2 levels deep              | `/users/{id}/addresses`    | `/users/{id}/orders/{oid}/items/{iid}` |
| Use kebab-case for multi-word paths | `/payment-methods`         | `/paymentMethods`                      |
| IDs are opaque                      | `/users/01HW3XKPZ8`        | `/users/1` (avoid sequential)          |
| Filter via query params, not path   | `/products?category=shoes` | `/products/category/shoes`             |

**Collection actions** (when REST verbs are insufficient):

Use a sub-resource named after the action as a last resort:

```
POST /orders/{id}/cancel     ← acceptable for actions with no resource equivalent
POST /accounts/{id}/activate
POST /invoices/{id}/send
```

**Relationship resources** (many-to-many):

```
GET  /users/{id}/roles          ← get all roles for user
PUT  /users/{id}/roles/{roleId} ← assign role to user
DELETE /users/{id}/roles/{roleId} ← remove role from user
```

### HTTP Method Semantics

| Method   | Semantics       | Idempotent | Safe | Request Body | Response Body    |
| -------- | --------------- | ---------- | ---- | ------------ | ---------------- |
| `GET`    | Read resource   | Yes        | Yes  | Never        | Resource         |
| `POST`   | Create / action | No         | No   | Required     | Created resource |
| `PUT`    | Full replace    | Yes        | No   | Required     | Updated resource |
| `PATCH`  | Partial update  | No\*       | No   | Required     | Updated resource |
| `DELETE` | Remove resource | Yes        | No   | Optional     | 204 No Content   |
| `HEAD`   | Metadata only   | Yes        | Yes  | Never        | Headers only     |

\*PATCH can be made idempotent with conditional requests (`If-Match`).

**Status code decision tree:**

```
Success:
  Created new resource        → 201 Created + Location header
  Action with no response     → 204 No Content
  Async operation started     → 202 Accepted + Location of status endpoint
  Normal read/update          → 200 OK

Client Error:
  Malformed request           → 400 Bad Request (+ Problem Details)
  Authentication required     → 401 Unauthorized
  Authorized but forbidden    → 403 Forbidden
  Resource not found          → 404 Not Found
  Method not allowed          → 405 Method Not Allowed
  Conflict (e.g. duplicate)   → 409 Conflict
  Precondition failed (ETag)  → 412 Precondition Failed
  Payload too large           → 413 Content Too Large
  Unprocessable entity        → 422 Unprocessable Content
  Rate limited                → 429 Too Many Requests + Retry-After

Server Error:
  Unexpected failure          → 500 Internal Server Error
  Upstream dependency failed  → 502 Bad Gateway
  Overloaded                  → 503 Service Unavailable + Retry-After
  Timeout to upstream         → 504 Gateway Timeout
```

### OpenAPI 3.0 Specification Authoring

**File structure (multi-file for large APIs):**

```
api/
├── openapi.yaml          ← root document
├── components/
│   ├── schemas/          ← all reusable schemas
│   │   ├── Order.yaml
│   │   ├── OrderItem.yaml
│   │   └── Problem.yaml
│   ├── responses/        ← common responses (400, 401, 404, 429, 500)
│   ├── parameters/       ← reusable path/query/header params
│   └── security/         ← security schemes
└── paths/
    ├── orders.yaml
    └── users.yaml
```

**Well-formed path definition:**

```yaml
# paths/orders.yaml
/orders:
  get:
    operationId: listOrders
    summary: List orders for the authenticated user
    tags: [Orders]
    security:
      - bearerAuth: []
    parameters:
      - $ref: "../components/parameters/cursor.yaml"
      - $ref: "../components/parameters/limit.yaml"
      - name: status
        in: query
        schema:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
    responses:
      "200":
        description: Paginated list of orders
        content:
          application/json:
            schema:
              $ref: "../components/schemas/OrderListResponse.yaml"
      "400":
        $ref: "../components/responses/BadRequest.yaml"
      "401":
        $ref: "../components/responses/Unauthorized.yaml"

  post:
    operationId: createOrder
    summary: Create a new order
    tags: [Orders]
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "../components/schemas/CreateOrderRequest.yaml"
    responses:
      "201":
        description: Order created
        headers:
          Location:
            schema:
              type: string
            description: URL of the created order
        content:
          application/json:
            schema:
              $ref: "../components/schemas/Order.yaml"
      "422":
        $ref: "../components/responses/UnprocessableEntity.yaml"
```

**Schema authoring guidelines:**

```yaml
# components/schemas/Order.yaml
type: object
required: [id, status, createdAt, items]
properties:
  id:
    type: string
    format: ulid
    readOnly: true
    example: "01HW3XKPZ8ABCDEF012345"
  status:
    type: string
    enum: [pending, confirmed, shipped, delivered, cancelled]
  totalAmount:
    type: integer
    description: Total in minor currency units (cents)
    minimum: 0
    example: 4999
  currency:
    type: string
    pattern: "^[A-Z]{3}$"
    example: "USD"
  createdAt:
    type: string
    format: date-time
    readOnly: true
  items:
    type: array
    minItems: 1
    items:
      $ref: "./OrderItem.yaml"
additionalProperties: false
```

**Linting with Spectral:**

```yaml
# .spectral.yaml
extends: ["spectral:oas"]
rules:
  operation-operationId: error
  operation-tags: error
  no-$ref-siblings: error
  oas3-unused-component: warn
  operation-description: warn
```

### Request Validation

**Python / Pydantic v2:**

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated
import re

class CreateOrderRequest(BaseModel):
    items: Annotated[list["OrderItemInput"], Field(min_length=1, max_length=50)]
    shipping_address_id: str = Field(pattern=r"^[0-9A-Z]{26}$")
    coupon_code: str | None = Field(default=None, max_length=32)

    @field_validator("coupon_code")
    @classmethod
    def normalize_coupon(cls, v: str | None) -> str | None:
        return v.upper().strip() if v else None

class OrderItemInput(BaseModel):
    product_id: str = Field(pattern=r"^[0-9A-Z]{26}$")
    quantity: int = Field(ge=1, le=100)

# FastAPI automatically returns 422 with Pydantic validation errors
# Map to RFC 7807 in a custom exception handler:
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        media_type="application/problem+json",
        content={
            "type": "https://api.company.com/problems/validation-error",
            "title": "Validation Error",
            "status": 422,
            "detail": "Request body failed validation",
            "errors": exc.errors(include_url=False),
        },
    )
```

**Go / validator:**

```go
import "github.com/go-playground/validator/v10"

type CreateOrderRequest struct {
    Items            []OrderItemInput `json:"items" validate:"required,min=1,max=50,dive"`
    ShippingAddrID   string           `json:"shipping_address_id" validate:"required,ulid"`
    CouponCode       *string          `json:"coupon_code,omitempty" validate:"omitempty,max=32"`
}

type OrderItemInput struct {
    ProductID string `json:"product_id" validate:"required,ulid"`
    Quantity  int    `json:"quantity" validate:"required,min=1,max=100"`
}

var validate = validator.New()

func (h *OrderHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateOrderRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeProblem(w, http.StatusBadRequest, "invalid-json", "Request body is not valid JSON")
        return
    }
    if err := validate.Struct(req); err != nil {
        writeValidationProblem(w, err.(validator.ValidationErrors))
        return
    }
    // ... handler logic
}
```

### Pagination Strategies

**Cursor-based pagination** (recommended for large, live datasets):

```json
// Response envelope
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6IjAxSFczWEtQWjgifQ==",
    "has_next": true,
    "limit": 20
  }
}
```

```python
# Cursor encodes the last-seen sort key (opaque to client)
import base64, json

def encode_cursor(order_id: str) -> str:
    return base64.b64encode(json.dumps({"id": order_id}).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.b64decode(cursor).decode())

# Query using cursor
async def list_orders(cursor: str | None, limit: int = 20) -> tuple[list[Order], str | None]:
    query = select(Order).order_by(Order.id.asc()).limit(limit + 1)
    if cursor:
        last_id = decode_cursor(cursor)["id"]
        query = query.where(Order.id > last_id)

    rows = await db.fetch_all(query)
    has_next = len(rows) > limit
    items = rows[:limit]
    next_cursor = encode_cursor(str(items[-1].id)) if has_next else None
    return items, next_cursor
```

**Offset pagination** (only for stable, bounded datasets):

```
GET /reports?offset=40&limit=20
```

```
Link: <https://api.company.com/reports?offset=60&limit=20>; rel="next",
      <https://api.company.com/reports?offset=20&limit=20>; rel="prev",
      <https://api.company.com/reports?offset=0&limit=20>; rel="first"
X-Total-Count: 247
```

**Pagination decision matrix:**

| Scenario                              | Strategy | Reason                                    |
| ------------------------------------- | -------- | ----------------------------------------- |
| Live data (rows inserted during page) | Cursor   | Offset skips rows when new items inserted |
| Stable reports / exports              | Offset   | Simpler, allows jump-to-page              |
| Infinite scroll feed                  | Cursor   | Consistent user experience                |
| Admin tool with page numbers          | Offset   | Page number UX requires total count       |

### Error Response Format (RFC 7807)

All error responses use `Content-Type: application/problem+json`:

```json
{
  "type": "https://api.company.com/problems/insufficient-inventory",
  "title": "Insufficient Inventory",
  "status": 422,
  "detail": "Product SKU-12345 has only 3 units available; 10 were requested.",
  "instance": "/orders/01HW3XKPZ8",
  "code": "INSUFFICIENT_INVENTORY",
  "context": {
    "product_id": "01HVZ9KX3P",
    "requested": 10,
    "available": 3
  }
}
```

**Problem type registry** (maintain in `api/problems/` folder):

| `code`                   | `status` | `type` URI suffix                  |
| ------------------------ | -------- | ---------------------------------- |
| `VALIDATION_ERROR`       | 422      | `/problems/validation-error`       |
| `RESOURCE_NOT_FOUND`     | 404      | `/problems/resource-not-found`     |
| `DUPLICATE_RESOURCE`     | 409      | `/problems/duplicate-resource`     |
| `INSUFFICIENT_INVENTORY` | 422      | `/problems/insufficient-inventory` |
| `RATE_LIMIT_EXCEEDED`    | 429      | `/problems/rate-limit-exceeded`    |
| `INTERNAL_ERROR`         | 500      | `/problems/internal-error`         |

**Never leak:**

- Stack traces in production responses
- Internal service names or IP addresses
- Database error messages
- Secrets or tokens in error detail

### API Versioning

**URL versioning** (recommended for most APIs):

```
/v1/orders
/v2/orders  ← breaking change: field renamed, resource restructured
```

**Header versioning** (for stable client contracts):

```
API-Version: 2024-11-01
```

**Deprecation lifecycle:**

```
1. Announce sunset date in docs ≥ 6 months ahead
2. Add `Deprecation` and `Sunset` headers to deprecated endpoints
3. Log every request to deprecated endpoint (for migration tracking)
4. Email registered API consumers 60 days before sunset
5. Return 410 Gone after sunset date
```

```python
from datetime import datetime, timezone
from fastapi import Response

SUNSET_DATE = "2026-06-01T00:00:00Z"

def add_deprecation_headers(response: Response) -> None:
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = '<https://docs.company.com/api/v2/migration>; rel="successor-version"'
```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** API contract (OpenAPI 3.0 spec) is a required deliverable. ADR documents versioning strategy, error format, pagination approach. Tech selection for validation library (Pydantic vs Joi vs go-validator) locked in TSD.

**Stage 5 (Development):** Implementation follows the OpenAPI spec as the source of truth. Request validation implemented at the boundary (middleware or handler entry). Spec changes during Stage 5 require updated ADR if breaking.

**Stage 6 (Architecture & Conformance Review):** OpenAPI spec reviewed against implementation for drift. Checklist — (1) All endpoints have `operationId`; (2) All error responses reference Problem Details schema; (3) No inline schemas (all use `$ref`); (4) Pagination envelope consistent across all list endpoints; (5) No sequential integer IDs exposed; (6) Deprecation headers emitted on all v1 endpoints if v2 exists.

**Stage 7 (Testing):** Contract tests validate implementation against OpenAPI spec (Schemathesis, Dredd). Validation tests cover boundary values, missing required fields, extra fields. Pagination tests cover empty sets, single-page sets, cursor decoding errors.

**Stage 8 (Integrity Verification):** Panel verifies error responses never leak internals. Rate limiting headers (`X-RateLimit-*`) present on all endpoints. Versioning strategy implemented and sunset headers active on deprecated routes.

## Quality Standards

| Metric                           | Target                                   | Measurement                          |
| -------------------------------- | ---------------------------------------- | ------------------------------------ |
| OpenAPI spec lint errors         | 0 errors, 0 warnings in CI               | Spectral in CI pipeline              |
| Schema coverage                  | 100% of responses defined in spec        | Schemathesis conformance report      |
| Validation rejection rate        | < 0.5% of production requests (expected) | 400/422 rate on monitoring dashboard |
| Cursor pagination correctness    | Zero duplicate/skipped items under load  | Pagination integration tests         |
| Error response RFC 7807 coverage | 100% of non-2xx responses                | Code review + contract tests         |
| Deprecation lead time            | ≥ 6 months before sunset                 | API lifecycle registry               |
