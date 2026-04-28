---
name: graphql-apis
description: Designs and implements GraphQL APIs with optimized schema design using types, interfaces, and unions, resolver optimization techniques, DataLoader pattern for N+1 query prevention.
---

# GraphQL APIs

**Category:** Backend Development (GraphQL)
**Owner:** Backend Engineer (Thabo Mokoena)

## Overview

Designs and implements GraphQL APIs with optimized schema design using types, interfaces, and unions, resolver optimization techniques, DataLoader pattern for N+1 query prevention, Apollo Federation for schema composition across services, subscription implementation for real-time updates, and comprehensive error handling with extensions.

## Competency Dimensions

| Dimension                      | Description                                                            | Proficiency Indicators                                                                                                                                       |
| ------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Schema Design                  | Object types, interfaces, unions, enums, input types, directives       | Designs schema following GraphQL best practices; uses interfaces for polymorphic types; selects unions vs interfaces correctly; implements custom directives |
| Resolver Optimization          | Resolver execution order, batching, caching, parallel execution        | Identifies N+1 patterns; implements DataLoader for batch loading; configures resolver parallelism; avoids over-fetching in resolvers                         |
| DataLoader Pattern             | Request batching, caching per request, custom cache keys               | Implements DataLoader for all database lookups in resolvers; understands per-request cache lifecycle; handles batch function error cases                     |
| Apollo Federation              | Subgraph composition, entity resolution, @key directives, shared types | Designs federated schema across services; implements entity resolvers for cross-service references; handles federation gateway configuration                 |
| Subscriptions                  | WebSocket transport, event filtering, subscription lifecycle           | Implements subscriptions with pub/sub backend; handles client disconnection; filters events per-subscriber                                                   |
| Error Handling with Extensions | GraphQLError, extensions field, error codes, field-level errors        | Returns structured errors with extensions; implements field-level error reporting; maps domain errors to GraphQL errors                                      |

## Execution Guidance

### Schema Design

```graphql
# Type system fundamentals
type User {
  id: ID!
  name: String!
  email: String!
  role: UserRole!
  orders(first: Int = 10, after: String): OrderConnection!
  createdAt: DateTime!
}

# Enum for constrained values
enum UserRole {
  USER
  MODERATOR
  ADMIN
}

# Interface for polymorphic types
interface Node {
  id: ID!
}

interface Orderable {
  id: ID!
  totalAmount: Float!
  status: OrderStatus!
}

# Union for mutually exclusive types
union SearchResult = User | Order | Product

# Input types for mutations
input CreateUserInput {
  name: String!
  email: String!
  password: String!
  role: UserRole = USER
}

input OrderFilterInput {
  status: OrderStatus
  dateFrom: DateTime
  dateTo: DateTime
  minAmount: Float
  maxAmount: Float
}

# Connection type for pagination (Relay-style)
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Order implements Orderable & Node {
  id: ID!
  user: User!
  items: [OrderItem!]!
  totalAmount: Float!
  status: OrderStatus!
  createdAt: DateTime!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  unitPrice: Float!
}

# Root query type
type Query {
  user(id: ID!): User
  users(first: Int = 10, after: String): UserConnection!
  order(id: ID!): Order
  search(query: String!, types: [SearchType!]): [SearchResult!]!
}

# Root mutation type
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateOrderStatus(orderId: ID!, status: OrderStatus!): UpdateOrderPayload!
}

# Payload types for mutations (allow future expansion)
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type UpdateOrderPayload {
  order: Order
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

# Custom scalar
scalar DateTime

# Custom directive
directive @auth(requires: UserRole = USER) on FIELD_DEFINITION
directive @rateLimit(max: Int = 100, window: Int = 60) on FIELD_DEFINITION
directive @cacheControl(maxAge: Int, scope: CacheControlScope) on FIELD_DEFINITION | OBJECT

enum CacheControlScope {
  PUBLIC
  PRIVATE
}
```

**Interface vs Union decision:**

| Use Case                                   | Pattern   | Example                                             |
| ------------------------------------------ | --------- | --------------------------------------------------- |
| Shared fields + type-specific fields       | Interface | `Orderable` — all have `totalAmount`, `status`      |
| Mutually exclusive types, no shared fields | Union     | `SearchResult` — User, Order, Product share nothing |
| Type narrowing with common contract        | Interface | `Node` — all implement `id: ID!`                    |

### Resolver Optimization and DataLoader

**N+1 problem and solution:**

```python
# Without DataLoader — N+1 problem
async def resolve_user_orders(user, info):
    # This is called ONCE PER USER in a list query
    # If querying 100 users, this makes 100 database queries!
    return await db.execute(
        select(Order).where(Order.user_id == user.id)
    )

# With DataLoader — batched into single query
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        # Single query for ALL users
        result = await db.execute(
            select(User).where(User.id.in_(user_ids))
        )
        users = result.scalars().all()

        # Return in same order as input keys
        user_map = {u.id: u for u in users}
        return [user_map.get(uid) for uid in user_ids]

class OrderByUserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        result = await db.execute(
            select(Order).where(Order.user_id.in_(user_ids))
        )
        orders = result.scalars().all()

        # Group orders by user_id
        orders_by_user = {}
        for order in orders:
            orders_by_user.setdefault(order.user_id, []).append(order)

        # Return in same order as input keys
        return [orders_by_user.get(uid, []) for uid in user_ids]

# Create loaders per request (important: cache is per-request)
def create_loaders():
    return {
        "user": UserLoader(),
        "orders_by_user": OrderByUserLoader(),
    }

# Resolvers using DataLoader
async def resolve_users(root, info, first=10, after=None):
    loaders = info.context["loaders"]

    users = await get_users_paginated(first, after)

    # Orders will be batched across ALL users in the response
    for user in users:
        user.orders = loaders["orders_by_user"].load(user.id)

    return users

async def resolve_order_user(order, info):
    loaders = info.context["loaders"]
    return loaders["user"].load(order.user_id)
```

**Resolver execution order understanding:**

```
Query: {
  users(first: 10) {
    name
    orders {
      totalAmount
      items {
        productName
      }
    }
  }
}

Execution order (depth-first):
1. Query.users → returns [User1, User2, ..., User10]
2. For each user (in parallel):
   a. user.name → scalar, immediate
   b. user.orders → DataLoader batched across all 10 users
3. For each order (in parallel):
   a. order.totalAmount → scalar, immediate
   b. order.items → DataLoader batched across all orders

Key: Resolvers at the same depth execute in parallel.
     DataLoader batches calls across parallel resolvers.
```

### Apollo Federation

**Subgraph schema (User Service):**

```python
from strawberry.federation.schema_directives import Key

@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    name: str
    email: str
    role: UserRole

    @strawberry.federation.reference_resolver
    async def resolve_reference(cls, id: strawberry.ID, info: strawberry.types.Info) -> "User | None":
        return await info.context["db"].get(User, id)

@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info: strawberry.types.Info, first: int = 10) -> list[User]:
        return await get_users(info.context["db"], first)
```

**Subgraph schema (Order Service):**

```python
# Reference to User from User service
@strawberry.federation.type(extend=True, keys=["id"])
class User:
    id: strawberry.ID = strawberry.federation.external()

    @strawberry.field
    async def orders(self, info: strawberry.types.Info, first: int = 10) -> list[Order]:
        return await get_orders_by_user(info.context["db"], self.id, first)

@strawberry.federation.type(keys=["id"])
class Order:
    id: strawberry.ID
    user_id: strawberry.ID
    total_amount: float
    status: OrderStatus
    created_at: datetime

    user: User  # Resolved by federation gateway
```

**Federation gateway configuration:**

```javascript
// gateway.js
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://user-service:4001/graphql' },
      { name: 'orders', url: 'http://order-service:4002/graphql' },
      { name: 'products', url: 'http://product-service:4003/graphql' },
    ],
  }),
});

const server = new ApolloServer({
  gateway,
  // Subgraphs handle their own auth
  // Gateway can add request context
  context: ({ req }) => ({
    authHeader: req.headers.authorization,
    requestId: req.headers['x-request-id'],
  }),
});
```

### Subscriptions Implementation

```python
import strawberry
from strawberry.types import Info
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def order_updated(
        self,
        info: Info,
        order_id: strawberry.ID
    ) -> AsyncGenerator[Order, None]:
        """Subscribe to updates for a specific order."""
        user_id = info.context["user_id"]

        # Subscribe to Redis channel
        pubsub = info.context["pubsub"]
        channel = f"order:{order_id}"

        async with pubsub.subscribe(channel) as subscriber:
            async for message in subscriber:
                order_data = json.loads(message["data"])

                # Authorization check: only notify if user is involved
                if (order_data.get("user_id") == user_id or
                    order_data.get("assigned_to") == user_id):
                    yield Order(
                        id=order_data["id"],
                        status=order_data["status"],
                        total_amount=order_data["total_amount"],
                    )

    @strawberry.subscription
    async def new_orders(
        self,
        info: Info,
    ) -> AsyncGenerator[Order, None]:
        """Subscribe to all new orders (admin only)."""
        if info.context["user_role"] != "admin":
            raise Exception("Admin access required")

        pubsub = info.context["pubsub"]
        async with pubsub.subscribe("orders:new") as subscriber:
            async for message in subscriber:
                yield Order.from_dict(json.loads(message["data"]))
```

### Error Handling with Extensions

```python
from graphql import GraphQLError, extend_schema
from typing import Any

class ValidationError(GraphQLError):
    """Custom error with structured extensions."""

    def __init__(
        self,
        message: str,
        code: str,
        field: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        extensions = {
            "code": code,
            "field": field,
        }
        if details:
            extensions["details"] = details

        super().__init__(
            message,
            extensions=extensions,
        )

# Usage in resolver
async def resolve_create_user(root, info, input):
    # Validation
    if not is_valid_email(input.email):
        raise ValidationError(
            message="Invalid email address",
            code="VALIDATION_ERROR",
            field="email",
            details={"expected": "valid email format"},
        )

    # Business rule
    existing = await db.get_user_by_email(input.email)
    if existing:
        raise ValidationError(
            message="Email already registered",
            code="DUPLICATE_EMAIL",
            field="email",
        )

    # ... create user ...

# Error response format:
# {
#   "data": null,
#   "errors": [
#     {
#       "message": "Invalid email address",
#       "locations": [{"line": 2, "column": 3}],
#       "path": ["createUser"],
#       "extensions": {
#         "code": "VALIDATION_ERROR",
#         "field": "email",
#         "details": {"expected": "valid email format"}
#       }
#     }
#   ]
# }

# Field-level errors in mutation payloads (alternative approach)
@strawberry.type
class CreateUserPayload:
    user: User | None = None
    errors: list[FieldError] = strawberry.field(default_factory=list)

@strawberry.type
class FieldError:
    field: str
    message: str
    code: str
```

## Pipeline Integration

**Stage 3 (Architecture):** GraphQL schema must be documented with type relationships and resolver dependencies. ADR required for GraphQL vs REST selection. Federation strategy documented if multi-service.

**Stage 5 (Development):** Schema implemented with DataLoader for all database lookups. Subscriptions use pub/sub backend. Error handling returns structured extensions.

**Stage 6 (Code Review):** Review schema for N+1 vulnerabilities. Validate DataLoader usage in all resolvers. Check subscription authorization. Verify error extension format consistency.

**Stage 7 (Testing):** Query complexity analysis prevents DoS. DataLoader batching validated under load. Subscription lifecycle tests (connect, receive, disconnect). Error response format tests.

## Quality Standards

| Metric                       | Target                                       | Measurement                          |
| ---------------------------- | -------------------------------------------- | ------------------------------------ |
| N+1 query prevention         | 100% of list resolvers use DataLoader        | Code review + query count monitoring |
| Query complexity limit       | < 1000 complexity per query                  | Complexity analysis middleware       |
| Resolver error handling      | 100% errors return structured extensions     | Error response audit                 |
| Subscription authorization   | 100% subscriptions check permissions         | Code review                          |
| Schema documentation         | 100% types and fields have descriptions      | Schema linting                       |
| Federation entity resolution | All @key directives have reference resolvers | Federation gateway validation        |
| DataLoader cache hits        | > 80% of batch loads hit cache               | DataLoader metrics                   |
