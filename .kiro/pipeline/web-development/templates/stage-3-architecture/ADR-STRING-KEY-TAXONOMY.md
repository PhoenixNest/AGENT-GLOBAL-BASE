# ADR: String Key Taxonomy

| Field         | Value                                                                               |
| ------------- | ----------------------------------------------------------------------------------- |
| **Status**    | Proposed                                                                            |
| **Context**   | Stage 3 — Web Application Pipeline (P1)                                             |
| **Decision**  | `{feature}.{screen}.{component}.{property}` dot-notation for all web UI string keys |
| **Date**      | YYYY-MM-DD                                                                          |
| **Authors**   | CTO (primary), Internationalization Specialist (Tomas Dvoracek)                     |
| **Reviewers** | CTO-L, Frontend Lead, Backend Lead                                                  |

---

## Decision

All UI strings in the web application use the naming convention `{feature}.{screen}.{component}.{property}` in dot-notation. Strings are stored in JSON message files (`locales/{lang}/messages.json`) keyed by this convention.

## Rationale

- **Consistency:** A single naming convention prevents duplicates and conflicts across the web codebase
- **Discoverability:** Developers can find strings by navigating the namespace hierarchy
- **Cross-platform parity** cannot be verified without a common key namespace to diff web messages against other platform message files
- **Tooling compatibility:** JSON format is natively supported by all modern i18n libraries (i18next, react-intl, vue-i18n)
- **Developer experience:** Dot-notation is intuitive for JavaScript developers and works with object property access

## Naming Convention

Format: `{feature}.{screen}.{component}.{property}`

| Segment     | Description                    | Example                                                        | Constraints                          |
| ----------- | ------------------------------ | -------------------------------------------------------------- | ------------------------------------ |
| `feature`   | Top-level feature/module       | `auth`, `dashboard`, `settings`                                | lowercase, kebab-case for multi-word |
| `screen`    | Screen/page within feature     | `login`, `profile`, `billing`                                  | lowercase                            |
| `component` | UI component or section        | `form`, `header`, `footer`, `modal`                            | lowercase                            |
| `property`  | Semantic purpose of the string | `title`, `label`, `placeholder`, `error`, `description`, `cta` | lowercase                            |

### Examples

```
auth.login.form.title = "Sign In"
auth.login.form.emailLabel = "Email address"
auth.login.form.emailPlaceholder = "you@example.com"
auth.login.form.submitCta = "Sign In"
auth.login.form.forgotPasswordLink = "Forgot your password?"
auth.login.form.emailError.invalid = "Please enter a valid email address"
auth.login.form.emailError.required = "Email is required"

dashboard.welcome.header.title = "Welcome back, {name}"
dashboard.welcome.header.subtitle = "Here's what's happening today"

settings.profile.form.displayNameLabel = "Display name"
settings.profile.form.saveCta = "Save changes"
```

## Pluralisation

Use ICU Message Format for plural rules. Keys remain the same; the message value contains plural logic.

```
// messages.json (English)
{
  "subscription.paywall.plan.count": "{count, plural, one {# month} other {# months}}"
}

// messages.json (French)
{
  "subscription.paywall.plan.count": "{count, plural, one {# mois} other {# mois}}"
}
```

## String Arrays / Lists

For ordered or unordered lists, use indexed keys:

```
{
  "settings.language.items.0": "English",
  "settings.language.items.1": "Français",
  "settings.language.items.2": "日本語"
}
```

## Lifecycle

1. **Developer identifies need** for a new UI string.
2. **Developer adds the key** to `locales/en/messages.json` with the English value, following the naming convention.
3. **Developer updates** `key-index.csv` with the new key, location, and default value.
4. **CI/CD gate** (after 2-week grace period) enforces key naming convention. Keys that don't match the pattern fail the build.
5. **CTO-L** validates during Stage 9 i18n engineering that all keys are present and correctly formatted.

## key-index.csv Structure

| Column            | Description                                                    | Example                                |
| ----------------- | -------------------------------------------------------------- | -------------------------------------- |
| `key`             | String key in dot-notation                                     | `auth.login.form.title`                |
| `source_value`    | English default value                                          | `Sign In`                              |
| `source_file`     | Source code location                                           | `src/components/auth/LoginForm.tsx:42` |
| `extraction_date` | Date string was extracted                                      | `2026-04-13`                           |
| `context`         | Usage notes for translators                                    | `Button text, max 20 chars`            |
| `status`          | extracted → tm_analyzed → translated → post_edited → validated | `extracted`                            |

## Alternatives Considered

| Alternative                                                      | Assessment                                                                |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Flat keys** (`login_title`, `dashboard_welcome`)               | Ambiguous at scale, no hierarchy, hard to organize                        |
| **Nested JSON keys** (`{"auth": {"login": {"title": "Login"}}}`) | Not easily diffable, requires transformation layer, harder to grep/search |
| **UUID-based keys** (`"k_12345"`)                                | Zero discoverability, requires lookup table, error-prone                  |
| **Sentence keys** (`"Sign in to your account"`)                  | Breaks when English text changes, no structure                            |

## Enforcement

After 2-week grace period:

1. **CI/CD gate** (Thomas Zhang): Regex validation on all keys in `locales/*/messages.json`
2. **PR review**: Automated check that new keys follow the convention
3. **key-index.csv**: Must be updated with every new string

### Regex Pattern

```regex
^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z][a-z0-9]*(-[a-z0-9]+)*(\.[a-z][a-z0-9]*(-[a-z0-9]+)*)*$
```

---

**Lock-down:** Once approved at Stage 3 gate, this naming convention is locked — changing the taxonomy requires Stage 3 re-entry.
