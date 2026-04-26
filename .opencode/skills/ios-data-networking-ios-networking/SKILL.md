---
name: ios-data-networking-ios-networking
description: "iOS networking with URLSession — session configuration, URLRequest, HTTP caching strategies, retry with exponential backoff, circuit breaker, reachability monitoring, and async/await migration. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for network layer implementation and Stage 6 (Code Review) for reliability audits. Trigger: urlsession, urlrequest, http caching, etag, retry, exponential backoff, circuit breaker, reachability, nwpathmonitor, api client, token refresh."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
---

# iOS Networking

**Category:** Mobile Engineering — iOS Networking
**Owner:** Senior iOS Engineer (Amara Diallo)

## Overview

This skill implements production-grade iOS networking covering URLSession architecture, URLRequest configuration, data task management, HTTP caching strategies, and retry mechanisms with exponential backoff. It applies to Stage 5 (Development) where all network communication is implemented using native iOS APIs, Stage 6 (Code Review) where network reliability and error handling are audited, and Stage 7 (Automated Testing) where network-dependent tests use mocked responses.

## Competency Dimensions

| Dimension                | Description                                                                                     | Proficiency Indicators                                                                                                                              |
| ------------------------ | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| URLSession Architecture  | Session configuration, delegate pattern, background sessions, upload/download tasks, WebSocket  | Session configuration matches use case (default/ephemeral/background); delegates handle auth challenges; background sessions survive app suspension |
| URLRequest Configuration | HTTP methods, headers, body encoding, timeout, cache policy, network service type               | Requests properly configured with method, headers, body; timeout values set per endpoint type; cache policy appropriate for data freshness          |
| Data Task Management     | DataTask, UploadTask, DownloadTask, async/await migration, task cancellation, task priority     | All tasks use modern async/await APIs; tasks cancellable via Task cancellation; priority set appropriately for user-initiated vs background work    |
| HTTP Caching             | URLCache configuration, cache policies, ETag handling, conditional requests, cache invalidation | URLCache properly sized; conditional requests use If-None-Match; cache invalidation on mutations; stale-while-revalidate pattern                    |
| Retry Strategies         | Exponential backoff, retry predicates, idempotency, circuit breaker, reachability monitoring    | Transient errors retried with jitter; non-idempotent mutations never auto-retried; circuit breaker prevents cascade failures                        |

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs define networking stack (URLSession vs Alamofire), caching strategy, and retry patterns.
- **Stage 5 (Development):** Primary skill for network layer implementation. All API clients, request/response handling, caching, and retry logic.
- **Stage 6 (Code Review):** Network review: timeout configuration, error handling completeness, cache policy correctness, retry idempotency, token refresh atomicity.
- **Stage 7 (Automated Testing):** Network tests with URLProtocol mocking; error handling tests for all HTTP status codes; retry logic tests.

## Quality Standards

- **Zero** Alamofire dependency — native URLSession exclusively (per ADR)
- All requests have explicit **timeout configuration**: default 30s, critical endpoints 15s
- **100%** HTTP errors mapped to domain error types with user-friendly messages
- Auth token refresh is **atomic** — synchronized to prevent concurrent refresh
- Retry uses **exponential backoff with jitter** — no fixed-delay retries
- **Zero** non-idempotent mutations (POST) auto-retried — only GET/PUT/DELETE retried
- URLCache configured with **50MB memory / 200MB disk** limits
- ETag/Last-Modified headers used for **conditional requests** on cacheable GET endpoints
- Circuit breaker implemented for **all external service calls**
- Network reachability monitored via **NWPathMonitor** — no Reachability framework
- All network operations use **async/await** — no completion handler APIs in new code

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
