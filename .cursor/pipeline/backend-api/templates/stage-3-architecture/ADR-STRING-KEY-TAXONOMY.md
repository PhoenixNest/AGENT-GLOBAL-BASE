# ADR-NNN: String Key Taxonomy for Localization

| Metadata          | Value                                                   |
| ----------------- | ------------------------------------------------------- |
| **ADR Number**    | ADR-NNN                                                 |
| **Title**         | String Key Taxonomy for Localization                    |
| **Status**        | Proposed                                                |
| **Decision Date** | YYYY-MM-DD                                              |
| **Authors**       | CTO (Dr. Kenji Nakamura), CTO-L (Dr. Amara Osei-Mensah) |
| **Reviewers**     | CSO (Dr. Sarah Chen), CPO (Marcus Tran-Yoshida)         |
| **Stage**         | 3 -- Architecture                                       |
| **Category**      | Localization / Naming Convention                        |

---

## Context

Consistent string key naming is foundational to the localization pipeline. Without a standardized naming convention:

- **Stage 9 extraction** becomes a manual, error-prone process where the Internationalization Specialist must reverse-engineer developer naming choices.
- **Translation quality** suffers because keys provide no semantic context for translators reviewing TM matches.
- **Maintenance overhead** grows exponentially -- with 300+ strings for error messages, developer portal content, and API documentation, ad-hoc naming makes it impossible to locate, audit, or update specific strings.
- **Cross-locale parity** cannot be verified without a common key namespace to diff English error messages against localized versions.

This ADR establishes a single, authoritative naming convention that all developers must follow during Stage 5 implementation.

---

## Decision

Adopt the **dot-notation hierarchical convention**:

```
{domain}.{category}.{component}.{property}
```

### Examples

| Key                                   | Purpose                                |
| ------------------------------------- | -------------------------------------- |
| `auth.login.error.invalid_email`      | Login invalid email error message      |
| `auth.login.error.invalid_password`   | Login invalid password error message   |
| `auth.login.error.account_locked`     | Account locked error message           |
| `auth.token.error.expired`            | Token expired error message            |
| `auth.token.error.revoked`            | Token revoked error message            |
| `api.rate_limit.error.exceeded`       | Rate limit exceeded error message      |
| `api.resource.error.not_found`        | Resource not found error message       |
| `api.validation.error.required_field` | Required field validation error        |
| `portal.docs.getting_started.title`   | Developer portal getting started title |
| `portal.docs.auth_guide.oauth_flow`   | OAuth flow documentation section       |
| `email.welcome.subject`               | Welcome email subject line             |
| `email.password_reset.body.intro`     | Password reset email intro             |
| `common.error.internal.message`       | Generic internal error message         |
| `common.error.network.message`        | Network error message                  |

### Naming Rules

1. **All lowercase** -- no camelCase, no PascalCase, no underscores.
2. **Dot-separated hierarchy** -- 4 levels: domain -> category -> component -> property.
3. **Descriptive, not abbreviated** -- `invalid_email` not `inv_email` or `bad_email`.
4. **`common` domain namespace** -- for shared error messages used across domains.
5. **`property` vocabulary restricted** -- use only: `message`, `title`, `description`, `hint`, `label`, `subject`, `body`.

---

### Pluralisation Key Naming

Pluralisation in API error messages and developer portal content uses locale-specific handling within the JSON structure.

| Context          | Pattern                                               | Example                                                                    |
| ---------------- | ----------------------------------------------------- | -------------------------------------------------------------------------- |
| API error msgs   | Base key with count property in message template      | `api.resource.error.items_count` -> `"You have {count} item(s)"`           |
| Developer portal | Separate keys for singular/plural if language differs | `portal.docs.resource.count_singular`, `portal.docs.resource.count_plural` |

**Example:**

```json
{
  "api.resource.error.items_count": "You have {count} item(s) remaining",
  "portal.docs.quota.count_singular": "1 request remaining",
  "portal.docs.quota.count_plural": "{count} requests remaining"
}
```

### Locale Variant Handling

| Scenario                        | Approach                                                                                                                                                                                        |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **zh-CN vs zh-TW**              | Same key namespace. Separate locale files (`locales/zh_CN/errors.json`, `locales/zh_TW/errors.json`).                                                                                           |
| **RTL languages (ar, fa, he)**  | Same key namespace. Keys used in developer portal UI flagged in `key-index.csv` with `rtl_review: true` for layout review.                                                                      |
| **Locale-specific expressions** | If a string requires completely different wording per locale (not just translation), create separate keys: `greeting.morning.en`, `greeting.morning.ja`. Document rationale in `key-index.csv`. |

---

## Key Generation Workflow

During Stage 5 development:

1. **Developer creates a new localizable string** (error message, portal content, email template) -> generates key following the `{domain}.{category}.{component}.{property}` convention.
2. **Developer adds the key** to the English source JSON file (`locales/en/errors.json`, `docs/locales/en/portal.json`, etc.).
3. **Developer updates `key-index.csv`** (created during Stage 4 per the Implementation Plan) with: key, source string, domain, category, status.
4. **CI/CD gate validates** the key format on every PR (after the 2-week grace period).

### CI/CD Enforcement

| Phase            | Duration                 | Behavior                                                     |
| ---------------- | ------------------------ | ------------------------------------------------------------ |
| **Grace Period** | First 2 weeks of Stage 5 | CI/CD logs warnings on key naming violations; builds succeed |
| **Enforcement**  | After grace period       | CI/CD fails the build on any key naming violation            |

---

## Exception Handling Protocol

When a developer creates a key that violates the convention:

1. **CI/CD gate fails the build** (after grace period) with a descriptive error message showing the expected key format.
2. **Developer fixes the key** to match the convention -- this is the expected path (>95% of cases).
3. **OR Developer files an exception request** with the CTO-L via `key-index.csv`:
   - Adds the key with `exception: true` flag
   - Includes `exception_rationale` column explaining why the convention cannot be followed
4. **CTO-L reviews within 24 hours:**
   - **Approve** -> key added to allowed exceptions list, build passes
   - **Reject** -> developer must rename the key
5. **All exceptions are logged** in `key-index.csv` with `exception`, `exception_rationale`, and `exception_reviewer` columns.

### key-index.csv Column Schema

The `key-index.csv` file is the single source of truth for all localizable strings. Column schema:

| Column                | Description                     | Example                                                                                                                   |
| --------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `key`                 | Full dot-notation key           | `api.validation.error.required_field`                                                                                     |
| `source_string`       | English source text             | "This field is required"                                                                                                  |
| `domain`              | Domain namespace                | `api`                                                                                                                     |
| `category`            | Category namespace              | `validation`                                                                                                              |
| `component`           | Component namespace             | `error`                                                                                                                   |
| `property`            | Property type                   | `message`                                                                                                                 |
| `file`                | Target locale file              | `locales/en/errors.json`                                                                                                  |
| `status`              | Key lifecycle status            | `active` / `deprecated` / `pending_removal`                                                                               |
| `translation_status`  | Translation pipeline state      | `extracted` -> `tm_analyzed` -> `translated` -> `post_edited` -> `qa_pass` / `needs_review` -> `validated` -> `completed` |
| `exception`           | Convention exception flag       | `true` / `false`                                                                                                          |
| `exception_rationale` | Why convention was not followed | "Legacy key from previous project"                                                                                        |
| `exception_reviewer`  | CTO-L who approved exception    | [Name]                                                                                                                    |
| `rtl_review`          | RTL layout review needed        | `true` / `false`                                                                                                          |

---

## Downstream Implications

| Stage       | Impact                                                                                                                                                                                                                                               |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** | `key-index.csv` template created using this taxonomy. Columns: `key`, `source_string`, `domain`, `category`, `component`, `property`, `file`, `status`, `translation_status`, `exception`, `exception_rationale`, `exception_reviewer`, `rtl_review` |
| **Stage 5** | All new localizable strings must follow this convention. Backend leads verify during code review.                                                                                                                                                    |
| **Stage 6** | Code review checks key naming compliance. Violations classified as P2 defects.                                                                                                                                                                       |
| **Stage 9** | R&D extraction relies on consistent key structure. The Internationalization Specialist uses `key-index.csv` as the single source of truth for string extraction into locale JSON files.                                                              |

---

## Alternatives Considered

| Alternative             | Description                             | Why Rejected                                                                                                   |
| ----------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Flat naming**         | `login_error_text`, `portal_auth_guide` | No hierarchy, impossible to audit at scale, no automated grouping by domain/category                           |
| **Nested JSON keys**    | `{"auth": {"login": {"error": "..."}}}` | Not compatible with CSV index tracking; difficult to diff between locales; CI/CD validation harder             |
| **Auto-generated keys** | `s_001`, `s_002`, `s_003`               | No semantic meaning, impossible to audit, translators have zero context, merge conflicts guaranteed            |
| **File-based grouping** | Keys grouped by source file name        | Breaks down with shared error messages, inconsistent across content types, no cross-locale parity verification |

---

## Compliance

**This decision is locked at Stage 3 gate approval.** Any deviation requires a new ADR and Stage 3 re-entry.

| Enforcement Layer | Mechanism                                                               |
| ----------------- | ----------------------------------------------------------------------- |
| Policy            | Stage 3 ADR lock -- cannot be changed without Stage 3 re-entry          |
| CI/CD             | Automated key format validation on every PR (after 2-week grace period) |
| Code Review       | Backend leads verify key naming during Stage 6 Tier 1 review            |
| Stage 9 Audit     | CTO-L verifies all extracted keys conform to taxonomy                   |

**Non-compliance classification:** Key naming violations discovered during Stage 6 are classified as **P2 defects** (minor feature degraded) unless they affect core user flows, in which case they are **P1**.
