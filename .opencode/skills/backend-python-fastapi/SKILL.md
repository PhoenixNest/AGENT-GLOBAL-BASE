---
name: backend-python-fastapi
description: FastAPI backend service development in Python — async route handlers, Pydantic v2 models, dependency injection, SQLAlchemy ORM, JWT auth, Celery background tasks, and OpenAPI schema generation. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 5 (Backend Development) for Python API implementation and Stage 7 (Automated Testing) for API test infrastructure. Trigger: fastapi, python backend, async api, pydantic, sqlalchemy, jwt auth, openapi schema, celery tasks.
prerequisites:
  - backend-overview

version: "1.0.0"
---

# Python FastAPI Development

**Category:** Backend Development (Python)
**Owner:** Backend Engineer (Ingrid Nilsen)

## Overview

Builds production-grade REST APIs using Python FastAPI framework, leveraging its dependency injection system, Pydantic v2 data models, async endpoint patterns, background task processing with Celery, middleware configuration, and automatic OpenAPI documentation generation. Emphasizes type safety, async-first design, and developer productivity.

## Competency Dimensions

| Dimension                | Description                                                                | Proficiency Indicators                                                                                                                            |
| ------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dependency Injection     | FastAPI Depends(), sub-dependencies, lifespan scope, override patterns     | Designs dependency graph with proper scoping; uses lifespan for startup/shutdown; overrides dependencies in tests                                 |
| Pydantic v2 Models       | Model validation, field types, validators, serialization, model_config     | Uses Pydantic v2 (not v1); configures model serialization properly; implements custom validators; uses root validators for cross-field validation |
| Async Endpoints          | async/await patterns, event loop management, blocking call avoidance       | Writes truly async endpoints; offloads blocking I/O to thread pools; avoids mixing sync and async incorrectly                                     |
| Background Tasks         | Celery task queues, retry policies, result backends, monitoring            | Designs Celery tasks with idempotency; configures retry with exponential backoff; monitors task queues; handles task failures gracefully          |
| Middleware Configuration | CORSMiddleware, custom middleware, middleware ordering, performance impact | Configures CORS correctly; writes custom middleware with proper error handling; understands middleware performance implications                   |
| OpenAPI Auto-Generation  | Response models, schema customization, documentation, examples             | Leverages FastAPI's automatic OpenAPI; customizes schemas for complex types; adds examples and descriptions; generates client SDKs                |

## Pipeline Integration

**Stage 5 (Development):** All endpoints implemented with Pydantic models for validation. Async patterns used for all I/O. Background tasks for long-running operations. OpenAPI documentation auto-generated and reviewed.

**Stage 6 (Code Review):** Review Pydantic model completeness (all fields validated). Check async correctness (no blocking calls in async functions). Validate dependency injection scoping. Verify Celery task idempotency.

**Stage 7 (Testing):** Unit tests for Pydantic validators. Integration tests for endpoint request/response cycles. Celery task tests with mock brokers. Async test fixtures for database.

**Stage 8 (Integrity Verification):** Panel validates OpenAPI spec matches implementation. Background task processing verified. Dependency injection tested in production-like configuration.

## Quality Standards

| Metric                           | Target                               | Measurement               |
| -------------------------------- | ------------------------------------ | ------------------------- |
| Pydantic validation coverage     | 100% of request/response models      | Model audit               |
| Async correctness                | 0 blocking calls in async functions  | Code review + profiling   |
| OpenAPI spec accuracy            | 100% match with implementation       | Automated drift detection |
| Celery task idempotency          | 100% of tasks idempotent             | Task design review        |
| Dependency injection testability | All dependencies overridable         | Test coverage             |
| Response validation              | 100% responses match Pydantic models | Runtime validation        |
| Middleware performance overhead  | < 5ms per request                    | Benchmarking              |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
