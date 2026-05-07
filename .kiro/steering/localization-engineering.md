---
inclusion: manual
description: i18n/l10n engineering patterns and best practices
---

# Localization Engineering Steering

This steering file provides internationalization (i18n) and localization (l10n) guidance for the workspace. Activate manually when working on multi-language features.

## Localization Context

- **i18n Framework:** ICU MessageFormat, i18next, react-intl, Flutter Intl
- **Translation Management:** TMS (Translation Management System)
- **Supported Languages:** As defined in project-specific configuration
- **Text Direction:** LTR (Left-to-Right), RTL (Right-to-Left)
- **Locale Format:** BCP 47 (e.g., en-US, ar-SA, zh-CN)

## Internationalization (i18n) Principles

### 1. Externalize All Strings

**Never hardcode user-facing text:**

```typescript
// ❌ Bad
<button>Submit</button>

// ✅ Good
<button>{t('common.submit')}</button>
```

### 2. Use ICU MessageFormat

**Support plurals, gender, and variables:**

```json
{
  "items_count": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

### 3. Support RTL Languages

**Use logical properties:**

```css
/* ❌ Bad */
margin-left: 10px;

/* ✅ Good */
margin-inline-start: 10px;
```

### 4. Locale-Aware Formatting

**Format dates, numbers, and currencies:**

```typescript
// Date formatting
const date = new Date();
const formatted = new Intl.DateTimeFormat("en-US").format(date);

// Number formatting
const number = 1234567.89;
const formatted = new Intl.NumberFormat("en-US").format(number);

// Currency formatting
const amount = 1234.56;
const formatted = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
}).format(amount);
```

## Translation File Structure

### 1. Namespace Organization

```
locales/
├── en/
│   ├── common.json       # Shared strings
│   ├── auth.json         # Authentication
│   ├── dashboard.json    # Dashboard
│   └── errors.json       # Error messages
├── es/
│   ├── common.json
│   ├── auth.json
│   └── ...
└── ar/
    ├── common.json
    ├── auth.json
    └── ...
```

### 2. Translation Key Naming

```json
{
  "auth.login.title": "Sign In",
  "auth.login.email_label": "Email Address",
  "auth.login.password_label": "Password",
  "auth.login.submit_button": "Sign In",
  "auth.login.forgot_password_link": "Forgot password?",

  "errors.validation.required": "This field is required",
  "errors.validation.email_invalid": "Please enter a valid email",
  "errors.network.timeout": "Request timed out. Please try again."
}
```

### 3. Pluralization

```json
{
  "notifications.count": {
    "zero": "No notifications",
    "one": "{{count}} notification",
    "other": "{{count}} notifications"
  }
}
```

### 4. Interpolation

```json
{
  "welcome.greeting": "Hello, {{name}}!",
  "order.confirmation": "Your order #{{orderId}} has been confirmed",
  "profile.last_login": "Last login: {{date, datetime}}"
}
```

## Platform-Specific Implementation

### React (react-i18next)

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t, i18n } = useTranslation();

  return (
    <div>
      <h1>{t('welcome.title')}</h1>
      <p>{t('welcome.greeting', { name: 'John' })}</p>
      <button onClick={() => i18n.changeLanguage('es')}>
        Español
      </button>
    </div>
  );
}
```

### Vue (vue-i18n)

```vue
<template>
  <div>
    <h1>{{ $t("welcome.title") }}</h1>
    <p>{{ $t("welcome.greeting", { name: "John" }) }}</p>
    <button @click="changeLanguage('es')">Español</button>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();

function changeLanguage(lang) {
  locale.value = lang;
}
</script>
```

### Android (Kotlin)

```kotlin
// strings.xml
<resources>
    <string name="welcome_title">Welcome</string>
    <string name="welcome_greeting">Hello, %1$s!</string>
    <plurals name="notifications_count">
        <item quantity="zero">No notifications</item>
        <item quantity="one">%d notification</item>
        <item quantity="other">%d notifications</item>
    </plurals>
</resources>

// Usage
val greeting = getString(R.string.welcome_greeting, userName)
val count = resources.getQuantityString(R.plurals.notifications_count, count, count)
```

### iOS (Swift)

```swift
// Localizable.strings
"welcome.title" = "Welcome";
"welcome.greeting" = "Hello, %@!";

// Usage
let title = NSLocalizedString("welcome.title", comment: "Welcome screen title")
let greeting = String(format: NSLocalizedString("welcome.greeting", comment: ""), userName)
```

### Flutter

```dart
// app_localizations.dart
class AppLocalizations {
  static String welcomeTitle(BuildContext context) {
    return Intl.message('Welcome', name: 'welcomeTitle');
  }

  static String welcomeGreeting(BuildContext context, String name) {
    return Intl.message('Hello, $name!', name: 'welcomeGreeting', args: [name]);
  }
}

// Usage
Text(AppLocalizations.welcomeTitle(context))
```

## RTL (Right-to-Left) Support

### 1. Layout Mirroring

```typescript
// Detect RTL
const isRTL = document.dir === 'rtl' ||
              document.documentElement.getAttribute('dir') === 'rtl';

// Set direction
<html dir={isRTL ? 'rtl' : 'ltr'}>
```

### 2. CSS for RTL

```css
/* Use logical properties */
.container {
  padding-inline-start: 20px; /* left in LTR, right in RTL */
  padding-inline-end: 10px; /* right in LTR, left in RTL */
  margin-block-start: 10px; /* top */
  margin-block-end: 10px; /* bottom */
}

/* RTL-specific styles */
[dir="rtl"] .icon {
  transform: scaleX(-1); /* Flip icons */
}
```

### 3. Bidirectional Text

```html
<!-- Isolate bidirectional text -->
<span dir="auto">{{userInput}}</span>

<!-- Force LTR for numbers/codes -->
<span dir="ltr">+1-555-1234</span>
```

## Translation Workflow

### 1. Extract Strings

```bash
# Extract translatable strings
npm run i18n:extract

# Output: locales/en/extracted.json
```

### 2. Send to Translation

- Export to TMS (Translation Management System)
- Use XLIFF, JSON, or CSV format
- Include context and screenshots
- Set translation deadlines

### 3. Import Translations

```bash
# Import translated files
npm run i18n:import

# Validate translations
npm run i18n:validate
```

### 4. Quality Assurance

- **Completeness:** All keys translated
- **Accuracy:** Correct meaning preserved
- **Context:** Appropriate for UI context
- **Length:** Fits in UI layout
- **Formatting:** Proper use of variables and plurals

## Best Practices

### 1. Context for Translators

```json
{
  "auth.login.submit_button": {
    "message": "Sign In",
    "description": "Button text for login form submission",
    "context": "Appears on the login page below the password field"
  }
}
```

### 2. Avoid String Concatenation

```typescript
// ❌ Bad
const message = t("hello") + " " + userName + "!";

// ✅ Good
const message = t("hello_user", { name: userName });
```

### 3. Handle Missing Translations

```typescript
// Fallback to key or default language
const t = (key: string, fallback?: string) => {
  return i18n.t(key) || fallback || key;
};
```

### 4. Locale Detection

```typescript
// Detect user locale
const userLocale =
  navigator.language || // Browser language
  navigator.userLanguage || // IE
  "en-US"; // Fallback

// Normalize locale
const normalizedLocale = userLocale.split("-")[0]; // 'en-US' -> 'en'
```

### 5. Performance

- **Lazy load translations:** Load only needed namespaces
- **Cache translations:** Store in memory or localStorage
- **Bundle splitting:** Separate translations by route
- **CDN delivery:** Serve translations from CDN

## Testing

### 1. Pseudo-Localization

```typescript
// Generate pseudo-localized strings for testing
function pseudoLocalize(text: string): string {
  return `[${text.replace(/[a-z]/gi, (c) =>
    String.fromCharCode(c.charCodeAt(0) + 0x1d00),
  )}]`;
}

// "Hello" -> "[Ⱨⱻłłⱺ]"
```

### 2. Visual Testing

- Test with longest translations (German, Finnish)
- Test with RTL languages (Arabic, Hebrew)
- Test with CJK languages (Chinese, Japanese, Korean)
- Verify text doesn't overflow or truncate

### 3. Automated Testing

```typescript
// Test translation keys exist
test("all translation keys exist", () => {
  const keys = ["auth.login.title", "auth.login.submit"];
  keys.forEach((key) => {
    expect(i18n.exists(key)).toBe(true);
  });
});
```

## Related Resources

- **Company Localization Standards:** `company/library/topics/localization.md`
- **Localization Skills:** `.kiro/skills/localization/`
- **CTO-L Profile:** `company/departments/localization/supervisor/chief-translation-officer/agent/profile.md`
- **Pipeline Stage 9:** Translation Production (see pipeline documentation)

## When to Activate

Activate this steering file when:

- Implementing multi-language support
- Adding new translatable strings
- Reviewing localization implementation
- Debugging translation issues
- Preparing for translation handoff (Stage 9)
