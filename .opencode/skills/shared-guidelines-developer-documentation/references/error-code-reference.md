# Error Code Reference

## Error Code Reference

| Error Code            | HTTP Status | Description                     | Documentation Link                            |
| --------------------- | ----------- | ------------------------------- | --------------------------------------------- |
| `UNAUTHORIZED`        | 401         | Authentication required         | [Auth Guide](/guides/authentication/)         |
| `FORBIDDEN`           | 403         | Insufficient permissions        | [Scopes Reference](/api-reference/scopes/)    |
| `NOT_FOUND`           | 404         | Resource not found              | —                                             |
| `BAD_REQUEST`         | 400         | Invalid request body            | [API Reference](/api-reference/)              |
| `CONFLICT`            | 409         | Resource conflict               | —                                             |
| `RATE_LIMITED`        | 429         | Too many requests               | [Rate Limiting Guide](/guides/rate-limiting/) |
| `INTERNAL_ERROR`      | 500         | Server error                    | —                                             |
| `SERVICE_UNAVAILABLE` | 503         | Service temporarily unavailable | [Status Page](https://status.company.com)     |

````

#### Troubleshooting Documentation Standards

| Standard | Requirement |
|----------|-------------|
| **Symptom-first organization** | Developers start with what they see (error message, status code), not with the root cause. Organize by symptom. |
| **Actionable resolution** | Every troubleshooting entry includes specific, sequential steps to resolve the issue. No "contact support" as the first step. |
| **Decision trees** | Use Mermaid flowcharts for multi-branch diagnostic paths. Developers can follow the tree to their specific issue. |
| **Request ID emphasis** | Every error resolution that requires support interaction tells the developer to include the `X-Request-ID` header value. |
| **Self-service prioritized** | ≥70% of troubleshooting entries should be resolvable without contacting support. |
| **Support ticket linkage** | Troubleshooting content is updated based on support ticket analysis. Top 5 ticket categories get troubleshooting entries within 5 business days. |

### Changelog Management

#### Changelog Structure

```markdown
# Changelog

All notable changes to the API are documented in this changelog.

**Format:** [Keep a Changelog](https://keepachangelog.com/)
**Versioning:** [Semantic Versioning](https://semver.org/)
````
