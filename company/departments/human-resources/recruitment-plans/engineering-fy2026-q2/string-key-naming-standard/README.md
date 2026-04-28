# String Key Naming Standard

**Document Type:** i18n Naming Convention Standard
**Version:** 1.0
**Date:** April 3, 2026
**Authors:** Tomas Dvoracek (Internationalization Specialist) + Chapter Leads
**Purpose:** Enforce consistent string key naming across Android, iOS, and Cross-platform teams to prevent duplication, ambiguity, and translation errors.
**Status:** ✅ Approved — Ready for Engineering Use

---

## Naming Convention

All string keys MUST follow the dot-notation pattern:

```
{feature}.{screen}.{component}.{property}
```

### Examples

| Key                                    | Value                       | Context                           |
| -------------------------------------- | --------------------------- | --------------------------------- |
| `auth.login.button.submit`             | "Sign In"                   | Submit button on login screen     |
| `auth.login.label.email`               | "Email Address"             | Email input label on login screen |
| `auth.login.error.invalid_credentials` | "Invalid email or password" | Error message on login failure    |
| `home.welcome.message`                 | "Hello, %1$s!"              | Welcome greeting on home screen   |
| `settings.profile.button.edit`         | "Edit Profile"              | Edit button on profile screen     |
| `checkout.confirm.button`              | "Confirm Purchase"          | Confirm button on checkout screen |
| `checkout.summary.label.total`         | "Total"                     | Total label on order summary      |

---

## Platform-Specific Rules

### Android (strings.xml)

```xml
<!-- Submit button on the login screen. Appears below the email and password fields. -->
<string name="auth_login_button_submit">Sign In</string>

<!-- Welcome message. %1$s is replaced with the user's first name. -->
<string name="home_welcome_message">Hello, %1$s!</string>
```

**Rules:**

- Use underscores as separators in XML `name` attribute (dots are not valid in Android resource names)
- Key in code: `R.string.auth_login_button_submit`
- Format specifiers MUST be indexed: `%1$s`, `%2$d` (never `%s`, `%d`)

### iOS (Localizable.strings)

```
/* Submit button on the login screen. Appears below the email and password fields. */
"auth.login.button.submit" = "Sign In";

/* Welcome message. %@ is replaced with the user's first name. */
"auth.login.welcome.message" = "Hello, %@!";
```

**Rules:**

- Use dots as separators in the key string
- Key in code: `NSLocalizedString("auth.login.button.submit", comment: "...")`
- Format specifiers: `%@` for objects, `%d` for integers, `%f` for floats

### Cross-Platform (KMP/Flutter)

**KMP shared module:**

```kotlin
// Keys use dot-notation; platform adapters convert to platform-specific format
object StringKeys {
    const val AUTH_LOGIN_BUTTON_SUBMIT = "auth.login.button.submit"
    const val HOME_WELCOME_MESSAGE = "home.welcome.message"
}
```

**Flutter (.arb files):**

```json
{
  "auth_login_button_submit": "Sign In",
  "@auth_login_button_submit": {
    "description": "Submit button on the login screen"
  }
}
```

---

## Format Specifier Rules

### Android

| Type       | Format   | Example             |
| ---------- | -------- | ------------------- |
| String     | `%1$s`   | `"Hello, %1$s!"`    |
| Integer    | `%1$d`   | `"%1$d items"`      |
| Float      | `%1$.2f` | `"Price: %1$.2f"`   |
| Percentage | `%1$d%%` | `"%1$d%% complete"` |

**NEVER use:** `%s`, `%d`, `%f` (non-indexed specifiers are ambiguous for translators)

### iOS

| Type    | Format | Example         |
| ------- | ------ | --------------- |
| String  | `%@`   | `"Hello, %@!"`  |
| Integer | `%d`   | `"%d items"`    |
| Float   | `%.2f` | `"Price: %.2f"` |

---

## Character Limit Annotations

All keys in the `key-index.csv` MUST include character limit annotations:

```csv
key,android_resource,ios_resource,cross_platform_resource,character_limit,context,platforms
auth.login.button.submit,auth_login_button_submit,auth.login.button.submit,auth_login_button_submit,20,Submit button on login screen,android,ios,kmp
home.welcome.message,home_welcome_message,auth.login.welcome.message,home_welcome_message,100,Welcome greeting with user name,android,ios,kmp
```

---

## CI/CD Enforcement

### Lint Rules (enforced by DevOps Lead + Tomas)

| Rule                                    | Severity            | Grace Period       |
| --------------------------------------- | ------------------- | ------------------ |
| Hardcoded string detection              | Error after 2 weeks | Weeks 1–2: Warning |
| Non-indexed format specifiers (Android) | Error after 2 weeks | Weeks 1–2: Warning |
| Key naming convention violation         | Error after 2 weeks | Weeks 1–2: Warning |
| Missing context comment                 | Warning             | Ongoing            |
| Duplicate key detection                 | Error               | Immediate          |

### Pre-Merge Gate

The CI/CD pipeline blocks any PR that:

- Contains string literals not wrapped in `R.string.*` (Android) or `NSLocalizedString`/`String(localized:)` (iOS)
- Uses non-indexed format specifiers in Android `strings.xml`
- Introduces keys that don't match the `{feature}.{screen}.{component}.{property}` pattern
- Contains duplicate keys in any resource file

---

## Cross-Platform Parity

The `key-index.csv` file maps every string key across all platforms:

| Column                    | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| `key`                     | Canonical key name (dot-notation)            |
| `android_resource`        | Android resource name (underscore-separated) |
| `ios_resource`            | iOS key string (dot-separated)               |
| `cross_platform_resource` | KMP/Flutter key name                         |
| `character_limit`         | Maximum display length for UI                |
| `context`                 | Description for translators                  |
| `platforms`               | Comma-separated list of target platforms     |

**Parity check:** Every key MUST exist in all target platform resource files. Missing keys are flagged during Stage 9 handoff.

**Note (v1.6):** The parity check will be fully automated — generated from resource files at build time by a script owned by DevOps Lead + Tomas. The CSV will NOT be manually maintained.

---

## Review Authority

- **Tomas Dvoracek** owns this standard and resolves naming disputes
- **Chapter Leads** enforce compliance within their teams
- **CI/CD gate** enforces automatically (no manual review needed after grace period)
