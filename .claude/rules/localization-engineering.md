---
description: i18n/l10n engineering patterns — invoke manually when working on multi-language features
---

# Localization Engineering

Internationalization and localization guidance. See `.claude/skills/localization/` for deep sub-skills.

---

## Core Principles

- **Externalize all strings** — never hardcode user-facing text
- **ICU MessageFormat** — support plurals, gender, and variables
- **Logical CSS properties** — `margin-inline-start` not `margin-left`
- **Locale-aware formatting** — `Intl.DateTimeFormat`, `Intl.NumberFormat`

## Translation Key Naming

```json
{
  "auth.login.title": "Sign In",
  "errors.validation.required": "This field is required",
  "notifications.count": "{count, plural, =0 {No notifications} one {# notification} other {# notifications}}"
}
```

## RTL Support

- Set `dir="auto"` or `dir="rtl"` at document level
- Use CSS logical properties throughout
- Flip directional icons: `transform: scaleX(-1)`
- Isolate bidirectional text with `<span dir="auto">`

## Platform Implementations

- **React:** `react-i18next`, `useTranslation()` hook
- **Vue:** `vue-i18n`, `$t()` method
- **Android:** `strings.xml`, `getQuantityString()` for plurals
- **iOS:** `NSLocalizedString()`, `Localizable.strings`
- **Flutter:** `Intl.message()`, ARB files

## Translation Workflow

1. Extract → send to TMS with context and screenshots
2. Translate → return XLIFF/JSON files
3. Import → validate completeness and formatting
4. QA → completeness, accuracy, context, length, RTL

---

## Related Rules

- `company-pipeline-overview.md` — Stage 9 Translation Production
