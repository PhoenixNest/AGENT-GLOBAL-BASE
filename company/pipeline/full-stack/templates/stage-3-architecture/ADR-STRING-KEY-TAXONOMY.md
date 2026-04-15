# ADR-NNN: String Key Taxonomy for Localization

| Metadata          | Value                                                   |
| ----------------- | ------------------------------------------------------- |
| **ADR Number**    | ADR-NNN                                                 |
| **Title**         | String Key Taxonomy for Localization                    |
| **Status**        | Proposed                                                |
| **Decision Date** | YYYY-MM-DD                                              |
| **Authors**       | CTO (Dr. Kenji Nakamura), CTO-L (Dr. Amara Osei-Mensah) |
| **Reviewers**     | CSO (Dr. Sarah Chen), CPO (Marcus Tran-Yoshida)         |
| **Stage**         | 3 — Architecture                                        |
| **Category**      | Localization / Naming Convention                        |

---

## Context

Consistent string key naming is foundational to the localization pipeline. Without a standardized naming convention:

- **Stage 9 extraction** becomes a manual, error-prone process where the Internationalization Specialist must reverse-engineer developer naming choices.
- **Translation quality** suffers because keys provide no semantic context for translators reviewing TM matches.
- **Maintenance overhead** grows exponentially — with 300+ strings per app, ad-hoc naming makes it impossible to locate, audit, or update specific strings.
- **Cross-platform parity** cannot be verified without a common key namespace to diff Android `strings.xml` against iOS `Localizable.strings`.

This ADR establishes a single, authoritative naming convention that all developers must follow during Stage 5 implementation.

---

## Decision

Adopt the **dot-notation hierarchical convention**:

```
{feature}.{screen}.{component}.{property}
```

### Examples

| Key                                       | Purpose                          |
| ----------------------------------------- | -------------------------------- |
| `auth.login.title.text`                   | Login screen title text          |
| `auth.login.email.label`                  | Email field label                |
| `auth.login.email.placeholder`            | Email field placeholder          |
| `auth.login.password.label`               | Password field label             |
| `auth.login.submit.label`                 | Submit button label              |
| `auth.login.error.invalid_email`          | Invalid email error message      |
| `auth.login.error.invalid_password`       | Invalid password error message   |
| `subscription.paywall.title.text`         | Paywall screen title             |
| `subscription.paywall.plan.monthly.label` | Monthly plan option label        |
| `subscription.paywall.plan.annual.label`  | Annual plan option label         |
| `subscription.paywall.submit.label`       | Subscribe button label           |
| `profile.settings.logout.label`           | Logout button label              |
| `profile.settings.theme.dark.label`       | Dark mode toggle label           |
| `common.button.cancel.label`              | Cancel button (shared component) |
| `common.error.network.message`            | Network error message (shared)   |

### Naming Rules

1. **All lowercase** — no camelCase, no PascalCase, no underscores.
2. **Dot-separated hierarchy** — exactly 4 levels: feature → screen → component → property.
3. **Descriptive, not abbreviated** — `submit.label` not `btn.lbl`.
4. **`common` feature namespace** — for shared components used across screens (buttons, error messages, dialogs).
5. **`property` vocabulary restricted** — use only: `text`, `label`, `placeholder`, `hint`, `message`, `title`, `description`, `error`, `success`, `warning`, `count`, `items`.

---

### Pluralisation Key Naming

Pluralisation requires platform-specific supplemental files that share the base key namespace.

| Platform       | Base Key Pattern                       | Pluralisation File             | Pluralisation Entry                                                                          |
| -------------- | -------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| Web Frontend   | `{feature}.{screen}.{component}.count` | `messages.json` (inline)       | ICU Message Format: `"{count, plural, one {# month} other {# months}}"`                      |
| iOS            | `{feature}.{screen}.{component}.count` | `Localizable.stringsdict`      | Same key name with `NSStringFormatSpecTypeKey` and `NSStringFormatValueTypeKey` entries      |
| Android        | `{feature}.{screen}.{component}.count` | `res/plurals/strings.xml`      | `<plurals name="{feature}.{screen}.{component}.count">` with `<item quantity="...">` entries |

**Example:**

```
Key: subscription.paywall.plan.count
iOS stringsdict: subscription.paywall.plan.count → one: "%d month", other: "%d months"
Android plurals: subscription.paywall.plan.count → one: "%d month", other: "%d months"
```

### Locale Variant Handling

| Scenario                        | Approach                                                                                                                                                                                                                                                              |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **zh-CN vs zh-TW**              | Same key namespace. Separate value files (`values-zh-rCN/strings.xml`, `zh_CN.lproj/Localizable.strings`, `locales/zh-CN/messages.json`).                                                                                                                             |
| **RTL languages (ar, fa, he)**  | Same key namespace. Keys used in RTL layouts flagged in `key-index.csv` with `rtl_review: true` for layout review.                                                                                                                                                    |
| **Locale-specific expressions** | If a string requires completely different wording per locale (not just translation), create separate keys: `greeting.morning.en`, `greeting.morning.ja`. Document rationale in `key-index.csv`.                                                                       |

### String-Array Key Conventions

For ordered lists and enum-backed string arrays:

```
{feature}.{screen}.{list}.items    — Base array key
Individual items accessed by index
```

**Example:**

```
settings.language.items[] = ["English", "Chinese", "Japanese", "Korean", "French"]
settings.theme.items[] = ["Light", "Dark", "System"]
```

Android: `<string-array name="settings.language.items">` with `<item>` entries.
iOS: Not natively supported — use `Localizable.strings` with indexed keys: `settings.language.items.0`, `settings.language.items.1`, etc.
Web Frontend: JSON array in `messages.json`: `"settings.language.items": ["English", "Chinese", "Japanese", "Korean", "French"]`

---

## Key Generation Workflow

During Stage 5 development:

1. **Developer creates a new UI string** → generates key following the `{feature}.{screen}.{component}.{property}` convention.
2. **Developer adds the key** to `strings.xml` (Android), `Localizable.strings` (iOS), AND `locales/en/messages.json` (Web Frontend) with the English value.
3. **Developer updates `key-index.csv`** (created during Stage 4 per the Implementation Plan) with: key, source string, feature, screen, status.
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
2. **Developer fixes the key** to match the convention — this is the expected path (>95% of cases).
3. **OR Developer files an exception request** with the CTO-L via `key-index.csv`:
   - Adds the key with `exception: true` flag
   - Includes `exception_rationale` column explaining why the convention cannot be followed
4. **CTO-L reviews within 24 hours:**
   - **Approve** → key added to allowed exceptions list, build passes
   - **Reject** → developer must rename the key
5. **All exceptions are logged** in `key-index.csv` with `exception`, `exception_rationale`, and `exception_reviewer` columns.

### key-index.csv Column Schema

The `key-index.csv` file is the single source of truth for all localizable strings. Column schema:

| Column                | Description                     | Example                                                                                                             |
| --------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `key`                 | Full dot-notation key           | `subscription.paywall.title.text`                                                                                   |
| `source_string`       | English source text             | "Subscribe to Premium"                                                                                              |
| `feature`             | Feature namespace               | `subscription`                                                                                                      |
| `screen`              | Screen namespace                | `paywall`                                                                                                           |
| `component`           | Component namespace             | `title`                                                                                                             |
| `property`            | Property type                   | `text`                                                                                                              |
| `status`              | Key lifecycle status            | `active` / `deprecated` / `pending_removal`                                                                         |
| `translation_status`  | Translation pipeline state      | `extracted` → `tm_analyzed` → `translated` → `post_edited` → `qa_pass` / `needs_review` → `validated` → `completed` |
| `exception`           | Convention exception flag       | `true` / `false`                                                                                                    |
| `exception_rationale` | Why convention was not followed | "Legacy key from previous project"                                                                                  |
| `exception_reviewer`  | CTO-L who approved exception    | [Name]                                                                                                              |
| `rtl_review`          | RTL layout review needed        | `true` / `false`                                                                                                    |

---

## Downstream Implications

| Stage       | Impact                                                                                                                                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** | `key-index.csv` template created using this taxonomy. Columns: `key`, `source_string`, `feature`, `screen`, `component`, `property`, `status`, `translation_status`, `exception`, `exception_rationale`, `exception_reviewer`, `rtl_review` |
| **Stage 5** | All new UI strings must follow this convention. Platform Leads verify during code review.                                                                                                                                                   |
| **Stage 6** | Code review checks key naming compliance. Violations classified as P2 defects.                                                                                                                                                              |
| **Stage 9** | R&D extraction relies on consistent key structure. The Internationalization Specialist uses `key-index.csv` as the single source of truth for string extraction into platform resource files.                                               |

---

## Alternatives Considered

| Alternative             | Description                                 | Why Rejected                                                                                                         |
| ----------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Flat naming**         | `login_button_text`, `profile_logout_label` | No hierarchy, impossible to audit at scale, no automated grouping by feature/screen                                  |
| **Nested JSON keys**    | `{"auth": {"login": {"title": "Login"}}}`   | Not compatible with Android `strings.xml` or iOS `Localizable.strings` native formats; requires transformation layer |
| **Auto-generated keys** | `s_001`, `s_002`, `s_003`                   | No semantic meaning, impossible to audit, translators have zero context, merge conflicts guaranteed                  |
| **File-based grouping** | Keys grouped by source file name            | Breaks down with shared components, inconsistent across platforms, no cross-platform parity verification             |
| **Web-only format**     | i18next JSON only                           | Android/iOS require their native formats; no single format works for all platforms                                   |

---

## Compliance

**This decision is locked at Stage 3 gate approval.** Any deviation requires a new ADR and Stage 3 re-entry.

| Enforcement Layer | Mechanism                                                               |
| ----------------- | ----------------------------------------------------------------------- |
| Policy            | Stage 3 ADR lock — cannot be changed without Stage 3 re-entry           |
| CI/CD             | Automated key format validation on every PR (after 2-week grace period) |
| Code Review       | Platform Leads verify key naming during Stage 6 Tier 1 review           |
| Stage 9 Audit     | CTO-L verifies all extracted keys conform to taxonomy                   |

**Non-compliance classification:** Key naming violations discovered during Stage 6 are classified as **P2 defects** (minor feature degraded) unless they affect core user flows, in which case they are **P1**.
