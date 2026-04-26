# Changelog

## Changelog

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| v1.0    | 2026-01-15 | Initial release                                     |
| v1.1    | 2026-03-01 | Added `fields` query parameter for sparse fieldsets |

````

### Code Example Generation

#### Multi-Language Example Standards

| Language | Audience | Framework/Library | Style Guide |
|----------|----------|------------------|-------------|
| Kotlin | Android engineers | Retrofit + Coroutines + kotlinx.serialization | Kotlin Official Coding Conventions |
| Swift | iOS engineers | URLSession + Codable (or async/await in Swift 5.5+) | Swift API Design Guidelines |
| Dart | Flutter engineers | http package + json_annotation / freezed | Effective Dart |

#### Example Quality Requirements

- **Compilable:** Every code example compiles against the current SDK version. Examples are validated by CI on every API spec change.
- **Complete:** Examples include error handling, not just the happy path. Show how to handle 401, 404, 500 responses.
- **Annotated:** Non-obvious patterns are explained with inline comments. Reference related documentation where applicable.
- **Current:** Examples are updated within 5 business days of any API change. Deprecation notices are added to examples using deprecated patterns.
- **Tested:** Examples are executed against a staging environment as part of CI pipeline. Test results reported in the example's metadata.

#### Example Template per Language

Each endpoint's code example section follows this pattern:

```markdown
### [Language] ([Platform])

#### Prerequisites
- [Required SDK/library version]
- [Authentication setup steps if not covered elsewhere]

#### Basic Usage
[Minimal example showing the simplest successful call]

#### With Error Handling
[Example showing proper error handling for common failure modes]

#### With Advanced Options
[Example showing pagination, filtering, or other advanced features]
````

### SDK Documentation

#### SDK Reference Structure

```
sdk-docs/
├── getting-started.md
├── authentication.md
├── configuration.md
├── reference/
│   ├── client.md              # Client class initialization and configuration
│   ├── models/
│   │   ├── resource.md        # Resource model class
│   │   ├── error.md           # Error model class
│   │   └── pagination.md      # Pagination model class
│   ├── services/
│   │   ├── resource-service.md # Resource API service methods
│   │   └── auth-service.md     # Authentication service methods
│   └── utilities/
│       ├── retry-policy.md     # Retry policy configuration
│       └── logging.md          # Logging configuration
├── guides/
│   ├── migration-v1-to-v2.md
│   ├── error-handling.md
│   ├── pagination.md
│   └── testing.md
└── changelog.md
```

#### SDK Reference Page Template

```markdown
# ResourceService

**Package:** `com.company.api.services` (Kotlin) / `CompanyAPI` (Swift) / `company_api` (Dart)
**Since:** SDK v1.0.0
```
