---
name: localization-guidelines-string-extraction-and-resource-files
description: 'Localization skill: String Extraction And Resource Files'
---

# String Extraction and Resource Files

## Purpose

Scan the integrity-verified codebase (Stage 9 input) to identify every hardcoded string and localizable dataset, extract them into correctly structured platform resource files, and produce a complete handoff package for the Chief Translation Officer. The output must satisfy the zero-hardcoded-strings gate criterion before Stage 9 can close.

## Platform Resource File Standards

### Android

**Primary string file:** `res/values/strings.xml`

```xml
<!-- Simple string -->
<string name="feature_button_label">Continue</string>

<!-- String with format specifier — always use named arguments for translator clarity -->
<string name="welcome_message">Hello, %1$s!</string>

<!-- Plural strings — cover ALL required quantities for every target language -->
<plurals name="item_count">
    <item quantity="zero">No items</item>
    <item quantity="one">%d item</item>
    <item quantity="other">%d items</item>
</plurals>

<!-- String array -->
<string-array name="day_names">
    <item>Monday</item>
    <item>Tuesday</item>
</string-array>
```

**Translator context comments:** Every string must have a preceding comment explaining context:

```xml
<!-- Button label on the checkout screen. Appears after payment method is selected. -->
<string name="checkout_confirm_button">Confirm Purchase</string>
```

**RTL considerations:** Mark any string containing directional text:

```xml
<string name="phone_number" tools:ignore="TypographyDashes">+1-555-0123</string>
```

### iOS

**Primary string file:** `Localizable.strings` (per locale: `en.lproj/`, `zh-Hans.lproj/`, etc.)

```
/* Button label on the checkout screen. Appears after payment method is selected. */
"checkout.confirm.button" = "Confirm Purchase";

/* Welcome message. %@ is replaced with the user's first name. */
"welcome.message" = "Hello, %@!";
```

**Plural forms:** `Localizable.stringsdict` for any string with quantity variation:

```xml
<key>item.count</key>
<dict>
    <key>NSStringLocalizedFormatKey</key>
    <string>%#@items@</string>
    <key>items</key>
    <dict>
        <key>NSStringFormatSpecTypeKey</key>
        <string>NSStringPluralRuleType</string>
        <key>NSStringFormatValueTypeKey</key>
        <string>d</string>
        <key>zero</key>  <string>No items</string>
        <key>one</key>   <string>%d item</string>
        <key>other</key> <string>%d items</string>
    </dict>
</dict>
```

**App metadata:** `InfoPlist.strings` for app name, permission descriptions, and other system-presented strings.

## Extraction Workflow

### Step 1: Codebase Scan

Scan all source files systematically:

**Android (Kotlin/Java):**

- Search for string literals in `.kt` and `.java` files not referenced via `R.string.*`
- Flag: `Text("any literal")`, `"literal".toText()`, `Toast.makeText(context, "literal", ...)`, Logcat messages visible to users
- Exclude: Log statements, test strings, developer-only debug text

**iOS (Swift):**

- Search for string literals not wrapped in `NSLocalizedString()` or `String(localized:)`
- Flag: `Text("literal")`, `Label("literal")`, `.navigationTitle("literal")`, alert messages
- Exclude: System API keys, internal identifiers, test fixtures

Produce a **Hardcoded String Inventory** listing every identified string, its file path, line number, and proposed resource key.

### Step 2: Key Naming Convention

All resource keys follow a hierarchical dot-notation pattern:

```
{feature}.{screen}.{component}.{property}

Examples:
  auth.login.email_field.placeholder
  checkout.confirmation.total_label.text
  settings.notifications.push_toggle.label
```

### Step 3: Resource File Production

- Create all `strings.xml` files with translator context comments
- Create all `Localizable.strings` and `Localizable.stringsdict` files
- Identify any JSON content files requiring localisation — flag and extract
- Verify: every key referenced in code exists in the resource file

### Step 4: Code Refactoring

Replace all hardcoded strings in code with resource references:

- Android: `getString(R.string.key_name)` / `stringResource(R.string.key_name)` (Compose)
- iOS: `String(localized: "key.name")` / `Text("key.name")` (SwiftUI)

### Step 5: Zero-Hardcoded-String Verification

After refactoring:

1. Re-run the codebase scan from Step 1
2. Confirm zero hardcoded strings remain
3. Build the app and verify it compiles cleanly

### Step 6: Structural Completeness Review

With CTO, CPO, and CDO:

- Verify all resource files are correctly structured
- Verify all UI components reference resource keys (no untranslated text visible in the base locale build)
- Sign off: structural review is complete. **Note:** Translation accuracy review belongs to CTO-L only.

### Step 7: CTO-L Handoff Package

Deliver to the Chief Translation Officer:

```
i18n-handoff/
  README.md                    ← extraction summary, key count per language, known edge cases
  android/
    strings.xml                ← base English strings with context comments
    plurals-reference.md       ← notes on plural forms required per target language
  ios/
    en.lproj/
      Localizable.strings      ← base English strings with context comments
      Localizable.stringsdict  ← plural string definitions
      InfoPlist.strings        ← app metadata strings
  datasets/
    [name].json                ← any localizable JSON content files
  key-index.csv                ← full key list: key | platform | context | character limit
```

## Stage 9 Gate Checklist

- [ ] Hardcoded String Inventory produced and reviewed
- [ ] Zero hardcoded strings remain in the codebase (scan confirmed)
- [ ] All resource files correctly structured per platform conventions
- [ ] All JSON datasets identified and included in handoff
- [ ] CPO, CDO, CTO structural completeness review signed off
- [ ] CTO-L handoff package delivered
