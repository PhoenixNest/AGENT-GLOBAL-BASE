# 2. Server Errors (5xx)

## 2. Server Errors (5xx)

### 500 Internal Server Error

**Symptom:** `{"error": {"code": "INTERNAL_ERROR", "message": "...", "status": 500}}`

**Resolution Steps:**

1. Retry the request with exponential backoff (this may be transient)
2. If the error persists, note the `X-Request-ID` header value
3. [Contact Support](/support/contact/) with the request ID and error details
4. Check the [Status Page](https://status.company.com) for known incidents

### 503 Service Unavailable

**Symptom:** HTTP 503 response or connection refused

**Resolution Steps:**

1. Check the [Status Page](https://status.company.com) for maintenance or outages
2. Implement retry logic with exponential backoff
3. If the outage is prolonged, subscribe to status notifications
