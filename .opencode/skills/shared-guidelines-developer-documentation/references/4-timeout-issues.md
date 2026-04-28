# 4. Timeout Issues

## 4. Timeout Issues

### Request Timeout

**Symptom:** Request completes but returns a timeout error after >30 seconds

**Resolution Steps:**

1. For list endpoints, reduce the `limit` parameter to return fewer results
2. Use the `fields` parameter to request only the fields you need
3. For large data exports, use the async export endpoint (if available)
4. Implement pagination to process results in smaller batches
