---
name: frontend-web-react-fastapi
description: React + FastAPI full-stack integration — React Query for async state, Celery/Redis task queues, multipart file uploads with presigned URLs, and WebAuthn biometric authentication flows. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for Python-React integration. Trigger: react fastapi, react query, celery redis, file upload react, webauthn, python react integration.
prerequisites:
  - frontend-web-react-state-management

version: "1.0.0"
---

# React + FastAPI Integration

**Category:** Full-Stack Engineering (Python/React)
**Owner:** Full-Stack Engineer (Sora Kim)

## Overview

Integrates React frontends with Python FastAPI backends, leveraging React Query for async state management, async task queues with Celery and Redis, file upload handling with multipart forms and presigned URLs, and biometric authentication flows with WebAuthn. Bridges Python backend capabilities with modern React frontend patterns.

## Competency Dimensions

| Dimension                 | Description                                                                                   | Proficiency Indicators                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| React Query               | Query caching, mutations, optimistic updates, query invalidation, infinite queries            | Configures React Query with appropriate stale times; implements optimistic updates with rollback; uses query invalidation for data consistency |
| FastAPI Integration       | CORS configuration, authentication headers, error response mapping, OpenAPI client generation | Configures FastAPI CORS for React origin; maps FastAPI error responses to React error states; generates TypeScript clients from OpenAPI spec   |
| Async Task Queues         | Celery task management, task status polling, progress reporting, result retrieval             | Implements task status polling with React Query; handles task failure states; displays progress indicators for long-running tasks              |
| File Upload               | Multipart form data, presigned S3 URLs, upload progress, chunked uploads                      | Implements direct-to-S3 upload with presigned URLs; displays upload progress; handles upload retry on failure                                  |
| Biometric Auth (WebAuthn) | Registration ceremony, authentication ceremony, credential management, fallback flows         | Implements WebAuthn registration and authentication; handles platform authenticator (Touch ID/Face ID); provides fallback to password auth     |

## Pipeline Integration

**Stage 5 (Development):** React Query configured with appropriate caching. Celery tasks implement progress reporting. File uploads use presigned URLs for direct S3 upload. WebAuthn registration and authentication flows complete.

**Stage 6 (Code Review):** Review React Query invalidation patterns. Validate Celery task idempotency. Check presigned URL security (expiration, bucket policy). Verify WebAuthn challenge lifecycle.

**Stage 7 (Testing):** React Query mock testing. Celery task integration tests. File upload end-to-end tests. WebAuthn flow tests (with mock credentials).

## Quality Standards

| Metric                          | Target  | Measurement          |
| ------------------------------- | ------- | -------------------- |
| React Query cache hit rate      | > 70%   | React Query devtools |
| Celery task success rate        | > 99%   | Celery monitoring    |
| File upload success rate        | > 99.5% | Upload monitoring    |
| WebAuthn registration success   | > 95%   | Registration metrics |
| API response time (p95)         | < 200ms | Application metrics  |
| Optimistic update rollback rate | < 1%    | Error tracking       |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
