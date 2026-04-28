# 3. Network Issues

## 3. Network Issues

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
