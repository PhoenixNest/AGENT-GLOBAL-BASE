# API Error Troubleshooting — Reference Example

> **Purpose:** Demonstrates the standard structure for developer-facing API error troubleshooting documentation. Each error includes symptom, common causes, resolution steps, and escalation path.

---

## Client Errors (4xx)

### 401 Unauthorized

**Symptom:** `{"error": {"code": "UNAUTHORIZED", "message": "...", "status": 401}}`

**Common Causes:**

1. API key not included in request
2. API key expired or revoked
3. JWT access token expired
4. Incorrect `Authorization` header format

**Resolution Steps:**

1. Verify `Authorization: Bearer <token>` header is present
2. Check token expiration: JWT tokens expire after 1 hour
3. Refresh your token using the refresh token endpoint
4. If using an API key, verify it's active in the Developer Dashboard

**Still stuck?** [Contact Support](/support/contact/) with your request ID.

### 403 Forbidden

**Symptom:** `{"error": {"code": "FORBIDDEN", "message": "...", "status": 403}}`

**Common Causes:**

1. API key lacks required scope
2. Account permissions insufficient

**Resolution Steps:**

1. Check the required scopes for the endpoint (listed in the API reference)
2. Verify your API key has the required scopes in the Developer Dashboard
3. Request additional scopes from your account administrator

### 404 Not Found

**Symptom:** `{"error": {"code": "NOT_FOUND", "message": "...", "status": 404}}`

**Common Causes:**

1. Resource ID is incorrect or malformed
2. Resource has been deleted
3. Endpoint URL is wrong

**Resolution Steps:**

1. Verify the resource ID format (UUID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
2. Check if the resource exists using the list endpoint
3. Verify the endpoint URL matches the API reference

### 429 Too Many Requests

**Symptom:** `{"error": {"code": "RATE_LIMITED", "message": "...", "status": 429}}` with `Retry-After` header

**Resolution Steps:**

1. Read the `Retry-After` header value (seconds to wait)
2. Implement exponential backoff in your client
3. Review your rate limit tier in the Developer Dashboard
4. Consider requesting a rate limit increase if your use case requires it

---

## Server Errors (5xx)

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

---

## Network Issues

### Connection Timeout

**Symptom:** Request times out after 30 seconds with no response

**Resolution Steps:**

1. Verify your internet connection
2. Check if `api.company.com` is reachable: `curl -I https://api.company.com/v1/`
3. Verify no firewall or proxy is blocking the connection
4. Check the [Status Page](https://status.company.com) for regional outages

### SSL/TLS Errors

**Symptom:** `SSL handshake failed` or `certificate verify failed`

**Resolution Steps:**

1. Verify your system's CA certificate bundle is up to date
2. Check that your system clock is accurate (SSL validation is time-sensitive)
3. Ensure you're connecting to `api.company.com` (not a typo or old endpoint)

---

## Timeout Issues

### Request Timeout

**Symptom:** Request completes but returns a timeout error after >30 seconds

**Resolution Steps:**

1. For list endpoints, reduce the `limit` parameter to return fewer results
2. Use the `fields` parameter to request only the fields you need
3. For large data exports, use the async export endpoint (if available)
4. Implement pagination to process results in smaller batches
