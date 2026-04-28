# 1. Client Errors (4xx)

## 1. Client Errors (4xx)

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
