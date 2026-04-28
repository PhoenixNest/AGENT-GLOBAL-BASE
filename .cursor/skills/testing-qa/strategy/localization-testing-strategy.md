---
name: localization-testing-strategy
description: Localization testing ensures the application behaves correctly with localized content regardless of language, script direction, or regional formatting, validating behavioral correctness under all target market conditions.
---

# Localization Testing Strategy

## 1. Overview

### Why Localization Testing Matters

Localization testing ensures that the application behaves correctly when presented with localized content, regardless of language, script direction, or regional formatting conventions. Unlike linguistic quality assurance — which validates translation accuracy, tone, and cultural appropriateness — localization testing validates **behavioral correctness** under localized conditions.

A single hardcoded string, an unmirrored icon, or a missing resource key can cause runtime crashes, layout overflow, or silent data corruption in target markets. These are engineering defects, not translation defects.

### Distinction: CTO-L vs. VP Quality Responsibilities

| Responsibility                    | Owner                                | Validates                                                 |
| --------------------------------- | ------------------------------------ | --------------------------------------------------------- |
| **Translation content accuracy**  | CTO-L (Dr. Amara Osei-Mensah)        | Correct terminology, tone, cultural fit per language      |
| **TMS pipeline integrity**        | CTO-L                                | Translation Memory, glossary enforcement, version control |
| **Lingu QA sign-off**             | CTO-L                                | Translation Verification Report (Stage 9 output)          |
| **Runtime localization behavior** | VP Quality (Aisha Patel) / Test Lead | Resource bundling, layout adaptation, RTL support, parity |
| **Automated l10n test execution** | Test Lead (Priscilla Oduya)          | Espresso/XCTest suites, CI gates, defect classification   |
| **Cross-platform string parity**  | Test Lead                            | Key set completeness across iOS and Android               |

**Rule of thumb:** If the string is _wrong_, that's CTO-L. If the string is _missing, overflowing, or crashes the app_, that's VP Quality / Test Lead.

### Pipeline Integration

Localization testing spans **Stage 9** (i18n Engineering) and **Stage 10** (Release Readiness):

- **Stage 9:** Pseudo-localization runs as a pre-translation gate. Asset verification runs after R&D extracts strings into platform resource files. Cross-platform parity checks execute after all platforms complete i18n engineering.
- **Stage 10:** Localization testing evidence feeds into Release Checklist item #6 ("Localisation — all target languages complete") alongside the CTO-L's Translation Verification Report.

### Scope of This Strategy

This strategy defines five pillars of localization testing, their automation approach, CI/CD gate configuration, and defect classification. It complements the CTO-L's linguistic validation workflow.

---

## 2. Pillar A: Pseudo-Localization Testing

### Purpose

Pseudo-localization generates fake "translated" strings from source text to detect hardcoded strings and layout overflow **before** real translation begins. This is the cheapest point in the pipeline to find localization defects.

### Pseudo-Localization Algorithm

Pseudo-localized strings follow these transformation rules:

1. **Bracket delimiters** — Wrap strings in `[!! ... !!]` to identify unlocalized text
2. **Character expansion** — Expand ASCII characters by ~30% to simulate languages with longer text (German, Finnish)
3. **Accent injection** — Replace ASCII with accented variants to verify font glyph coverage
4. **Special character injection** — Insert Unicode edge cases (RTL marks, combining characters, zero-width spaces)

### Generation Implementation

```python
#!/usr/bin/env python3
"""Pseudo-localization string generator for pre-translation gate."""

import re
import unicodedata

ACCENT_MAP = {
    'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú',
    'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú',
    'c': 'ç', 'n': 'ñ', 'y': 'ÿ',
}

def pseudo_localize(source_string: str) -> str:
    """Generate pseudo-localized version of a source string."""
    # Step 1: Accent substitution with expansion
    result = []
    for char in source_string:
        if char in ACCENT_MAP:
            result.append(ACCENT_MAP[char] * 2)  # Double for expansion
        elif char.isalpha():
            result.append(char + char)  # Repeat for expansion
        else:
            result.append(char)

    expanded = ''.join(result)

    # Step 2: Add bracket delimiters
    return f"[!! {expanded} !!]"

def process_strings_file(input_path: str, output_path: str) -> dict:
    """Process a strings.xml or Localizable.strings file."""
    stats = {'total': 0, 'processed': 0, 'skipped': 0}

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            stats['total'] += 1

            # Skip comments, XML declarations, empty lines
            if line.strip().startswith(('<', '//', '#')) or not line.strip():
                outfile.write(line)
                stats['skipped'] += 1
                continue

            # Extract string value and pseudo-localize
            match = re.match(r'(\s*<string name="[^"]*">)(.*?)(</string>\s*)', line)
            if match:
                prefix, value, suffix = match.groups()
                pseudo_value = pseudo_localize(value)
                outfile.write(f"{prefix}{pseudo_value}{suffix}\n")
                stats['processed'] += 1
                continue

            # iOS Localizable.strings format: "key" = "value";
            match = re.match(r'(\s*"[^"]*"\s*=\s*")(.+?)("\s*;\s*)', line)
            if match:
                prefix, value, suffix = match.groups()
                pseudo_value = pseudo_localize(value)
                outfile.write(f"{prefix}{pseudo_value}{suffix}\n")
                stats['processed'] += 1
                continue

            outfile.write(line)
            stats['skipped'] += 1

    return stats
```

### Pre-Translation Gate Criteria

| Criterion                       | Pass Condition                           | Failure Action                              |
| ------------------------------- | ---------------------------------------- | ------------------------------------------- |
| All UI strings pseudo-localized | 100% of extractable strings transformed  | Investigate skipped strings                 |
| App builds with pseudo-locale   | No compilation errors                    | Fix resource format errors                  |
| No hardcoded strings detected   | Zero strings rendered in source language | Extract hardcoded strings to resource files |
| No layout overflow crashes      | App runs without ClipBounds violations   | Fix constrained layouts                     |

### Hardcoded String Detection

After deploying a pseudo-localized build, any string that renders in the **source language** (not bracketed/expanded) is hardcoded. The Test Lead catalogs these as **P1 defects** — hardcoded strings are release blockers because they bypass the entire translation pipeline.

```kotlin
// Android: Espresso test for hardcoded string detection
@Test
fun detectHardcodedStrings_onAllScreens() {
    val sourceStrings = loadSourceStringKeys() // From strings.xml
    val hardcodedFound = mutableListOf<String>()

    // Iterate through all UI text views
    onView(isAssignableFrom(TextView::class.java))
        .perform(object : ViewAction {
            override fun getConstraints() = isAssignableFrom(TextView::class.java)
            override fun getDescription() = "Check for hardcoded strings"
            override fun perform(uiController: UiController, view: View) {
                val textView = view as TextView
                val text = textView.text.toString()
                // If text doesn't contain pseudo-localization markers
                if (!text.contains("[!!") && !text.contains("á")) {
                    hardcodedFound.add(text)
                }
            }
        })

    assertTrue(
        "Hardcoded strings detected: ${hardcodedFound.joinToString(", ")}",
        hardcodedFound.isEmpty()
    )
}
```

### Layout Overflow Detection

Pseudo-localized strings expand by ~30%. This exposes layouts with fixed widths, insufficient padding, or truncation logic.

```swift
// iOS: XCTest for layout overflow detection
func testNoTextClippingWithPseudoLocale() {
    let app = XCUIApplication()
    app.launchArguments = ["-AppleLanguages", "(pseudo)"]
    app.launch()

    // Check all static text elements for clipping
    let textElements = app.staticTexts.allElementsBoundByIndex
    for textElement in textElements {
        XCTAssertTrue(
            textElement.isHittable,
            "Text element '\(textElement.label)' is clipped or overflowed"
        )

        // Verify the element's frame fits within its superview
        let frame = textElement.frame
        let parentFrame = textElement.parent?.frame ?? .zero
        XCTAssertFalse(
            frame.width > parentFrame.width,
            "Text overflow detected: '\(textElement.label)' (width: \(frame.width) > \(parentFrame.width))"
        )
    }
}
```

---

## 3. Pillar B: L10n Asset Verification

### Purpose

Verify that all localization resource files are correctly bundled into the application binary and that no runtime `MissingResourceException` or `NSLocalizedString` fallback failures occur.

### Android: Resource File Verification

```kotlin
// Android: Verify all string resources exist for each locale
@RunWith(AndroidJUnit4::class)
class LocalizationAssetVerificationTest {

    @Test
    fun allLocalesHaveRequiredStringKeys() {
        val contexts = mapOf(
            "en" to createConfigurationContext("en"),
            "zh" to createConfigurationContext("zh"),
            "ja" to createConfigurationContext("ja"),
            "ko" to createConfigurationContext("ko"),
            "ar" to createConfigurationContext("ar"),
            "fr" to createConfigurationContext("fr"),
            "de" to createConfigurationContext("de"),
        )

        val requiredKeys = getRequiredStringKeys(contexts["en"]!!)
        val missingKeys = mutableMapOf<String, List<String>>()

        contexts.forEach { (locale, context) ->
            val localeKeys = getStringKeys(context)
            val missing = requiredKeys - localeKeys
            if (missing.isNotEmpty()) {
                missingKeys[locale] = missing.toList()
            }
        }

        assertTrue(
            "Missing string keys in locales: ${missingKeys.mapValues { it.value.size }}",
            missingKeys.isEmpty()
        )
    }

    @Test
    fun allPluralsHaveAllLocales() {
        val requiredPlurals = getRequiredPluralKeys(getConfigurationContext("en"))
        val locales = listOf("en", "zh", "ja", "ko", "ar", "fr", "de")

        locales.forEach { locale ->
            val context = createConfigurationContext(locale)
            requiredPlurals.forEach { pluralKey ->
                try {
                    context.resources.getQuantityString(
                        getIdentifier(pluralKey, "plurals", context.packageName),
                        1
                    )
                } catch (e: Resources.NotFoundException) {
                    fail("Missing plural resource '$pluralKey' for locale '$locale'")
                }
            }
        }
    }

    private fun createConfigurationContext(locale: String): Context {
        val config = Configuration()
        config.setLocale(Locale(locale))
        return ApplicationProvider.getApplicationContext<Context>()
            .createConfigurationContext(config)
    }

    private fun getStringKeys(context: Context): Set<String> {
        val keys = mutableSetOf<String>()
        val resIdField = R.string::class.java.fields
        resIdField.forEach { field ->
            try {
                val resId = field.getInt(null)
                context.resources.getString(resId)
                keys.add(field.name)
            } catch (e: Resources.NotFoundException) {
                // Key exists but has no value for this locale
            }
        }
        return keys
    }
}
```

### iOS: Asset Bundle Verification

```swift
// iOS: Verify all localization bundles contain required keys
import XCTest

class LocalizationAssetVerificationTests: XCTestCase {

    func testAllBundlesHaveRequiredKeys() {
        let supportedLocales = ["en", "zh-Hans", "ja", "ko", "ar", "fr", "de"]
        let requiredKeys = requiredStringKeys(for: "en")

        var missingKeysReport: [String: [String]] = [:]

        for locale in supportedLocales {
            guard let bundle = Bundle(path: Bundle.main.path(
                forResource: locale, ofType: "lproj")!)
            else {
                missingKeysReport[locale] = requiredKeys
                continue
            }

            let localeKeys = stringKeys(in: bundle)
            let missing = requiredKeys.filter { !localeKeys.contains($0) }
            if !missing.isEmpty {
                missingKeysReport[locale] = missing
            }
        }

        XCTAssertTrue(
            missingKeysReport.isEmpty,
            "Missing keys in locales: \(missingKeysReport)"
        )
    }

    func testNoMissingResourceFallbacks() {
        // Verify NSLocalizedString never falls back to development language
        let app = XCUIApplication()
        app.launchArguments = ["-AppleLanguages", "(zh-Hans)"]
        app.launch()

        // Snapshot the entire UI and check for English text
        let textElements = app.staticTexts.allElementsBoundByIndex
        let englishPatterns = ["Welcome", "Settings", "Cancel", "Save", "Delete"]

        for element in textElements {
            let label = element.label
            for pattern in englishPatterns {
                XCTAssertFalse(
                    label.contains(pattern),
                    "Found English fallback '\(pattern)' in Chinese UI: '\(label)'"
                )
            }
        }
    }

    private func requiredStringKeys(for locale: String) -> [String] {
        guard let bundle = Bundle(path: Bundle.main.path(
            forResource: locale, ofType: "lproj")!)
        else { return [] }
        return stringKeys(in: bundle)
    }

    private func stringKeys(in bundle: Bundle) -> [String] {
        guard let path = bundle.path(forResource: "Localizable", ofType: "strings"),
              let content = try? String(contentsOfFile: path, encoding: .utf8)
        else { return [] }

        return content.components(separatedBy: .newlines)
            .compactMap { line -> String? in
                let parts = line.components(separatedBy: "\" = \"")
                guard parts.count >= 2 else { return nil }
                return parts[0].replacingOccurrences(of: "\"", with: "")
            }
    }
}
```

### Device Farm Execution

Asset verification runs on a device farm covering the full locale matrix:

| Platform | Minimum Devices                        | Locales               | Execution Mode                 |
| -------- | -------------------------------------- | --------------------- | ------------------------------ |
| Android  | 4 devices (API 24, 28, 31, 34)         | All supported locales | Parallel via Firebase Test Lab |
| iOS      | 3 devices (iPhone SE, iPhone 15, iPad) | All supported locales | Parallel via Xcode Cloud       |

---

## 4. Pillar C: Cross-Platform String Parity

### Purpose

Ensure that the set of localization keys is **identical** across iOS and Android platforms. Key drift between platforms causes feature gaps where one platform displays translated text and the other displays raw keys or fallback strings.

### Automated Diff Script

```python
#!/usr/bin/env python3
"""Cross-platform string parity checker for CI/CD gate."""

import re
import sys
import json
from pathlib import Path

def parse_android_strings_xml(xml_path: str) -> dict:
    """Parse Android strings.xml into {key: value} dict."""
    keys = {}
    pattern = re.compile(r'<string\s+name="([^"]+)">\s*(.*?)\s*</string>', re.DOTALL)
    with open(xml_path, 'r', encoding='utf-8') as f:
        for match in pattern.finditer(f.read()):
            keys[match.group(1)] = match.group(2)
    return keys

def parse_ios_strings_plist(strings_path: str) -> dict:
    """Parse iOS Localizable.strings into {key: value} dict."""
    keys = {}
    pattern = re.compile(r'"([^"]+)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;')
    with open(strings_path, 'r', encoding='utf-8') as f:
        for match in pattern.finditer(f.read()):
            keys[match.group(1)] = match.group(2)
    return keys

def compute_parity_diff(android_keys: dict, ios_keys: dict) -> dict:
    """Compute key set differences between platforms."""
    android_set = set(android_keys.keys())
    ios_set = set(ios_keys.keys())

    return {
        "only_in_android": sorted(android_set - ios_set),
        "only_in_ios": sorted(ios_set - android_set),
        "common_keys": sorted(android_set & ios_set),
        "total_android": len(android_set),
        "total_ios": len(ios_set),
        "parity_percentage": round(
            len(android_set & ios_set) / max(len(android_set), len(ios_set)) * 100, 2
        ) if max(len(android_set), len(ios_set)) > 0 else 0
    }

def main():
    android_path = Path(sys.argv[1])  # e.g., platforms/android/res/values/strings.xml
    ios_path = Path(sys.argv[2])      # e.g., platforms/ios/en.lproj/Localizable.strings

    android_keys = parse_android_strings_xml(android_path)
    ios_keys = parse_ios_strings_plist(ios_path)

    diff = compute_parity_diff(android_keys, ios_keys)

    # Write report
    report_path = Path(sys.argv[3])  # e.g., reviews/release/l10n-parity-report.json
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(diff, f, indent=2, ensure_ascii=False)

    print(f"Android keys: {diff['total_android']}")
    print(f"iOS keys:     {diff['total_ios']}")
    print(f"Parity:       {diff['parity_percentage']}%")

    if diff['only_in_android']:
        print(f"\nOnly in Android ({len(diff['only_in_android'])}):")
        for key in diff['only_in_android'][:20]:
            print(f"  - {key}")

    if diff['only_in_ios']:
        print(f"\nOnly in iOS ({len(diff['only_in_ios'])}):")
        for key in diff['only_in_ios'][:20]:
            print(f"  - {key}")

    # Exit non-zero if parity below threshold
    if diff['parity_percentage'] < 100.0:
        print(f"\nPARITY CHECK FAILED: {diff['parity_percentage']}% < 100%")
        sys.exit(1)
    else:
        print("\nPARITY CHECK PASSED: 100% key parity")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### CI Gate Configuration

```yaml
# .github/workflows/l10n-parity-check.yml
name: L10n Cross-Platform Parity Check

on:
  push:
    branches: [main, release/**]
  pull_request:
    branches: [main]

jobs:
  parity-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check string key parity
        run: |
          python3 scripts/l10n-parity-check.py \
            company/project/${{ github.event.repository.name }}/platforms/android/res/values/strings.xml \
            company/project/${{ github.event.repository.name }}/platforms/ios/en.lproj/Localizable.strings \
            company/project/${{ github.event.repository.name }}/reviews/release/l10n-parity-report.json

      - name: Upload parity report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: l10n-parity-report
          path: company/project/*/reviews/release/l10n-parity-report.json

      - name: Fail on parity below 100%
        if: failure()
        run: |
          echo "String parity check failed. Android and iOS have different localization keys."
          echo "This is a P1 defect — both platforms must have identical key sets."
          exit 1
```

### Parity Threshold

| Metric                     | Required                              | Classification if Below           |
| -------------------------- | ------------------------------------- | --------------------------------- |
| Key set parity             | 100%                                  | P1 (release blocker)              |
| Value presence (non-empty) | 100% for target locales               | P1 if any locale has empty values |
| Plural form coverage       | All CLDR plural categories per locale | P2 per missing category           |

---

## 5. Pillar D: RTL Layout Testing

### Purpose

Right-to-Left (RTL) languages (Arabic, Hebrew) require layout mirroring: navigation flows reverse, icons flip, text alignment changes, and scroll directions invert. This pillar validates RTL behavior through automated and manual spot-checks.

### Android RTL Configuration

```xml
<!-- AndroidManifest.xml: Enable RTL support -->
<manifest ...>
    <application
        android:supportsRtl="true"
        ...>
        <!-- All activities inherit RTL support -->
    </application>
</manifest>
```

```xml
<!-- layout/main_activity.xml: Use start/end instead of left/right -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginStart="16dp"
    android:layout_marginEnd="16dp">

    <ImageView
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:layout_gravity="start"
        android:autoMirrored="true"
        android:src="@drawable/ic_arrow_forward" />

    <TextView
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:layout_marginStart="8dp"
        android:textAlignment="viewStart"
        android:text="@string/welcome_message" />
</LinearLayout>
```

### iOS RTL Configuration

```swift
// iOS: Semantic content attribute for RTL
class RTLLayoutHelper {

    static func configureForRTL(view: UIView) {
        if UIView.userInterfaceLayoutDirection(for: view.semanticContentAttribute) == .rightToLeft {
            // Apply RTL-specific layout adjustments
            view.semanticContentAttribute = .forceRightToLeft
        }
    }

    static func isRTL() -> Bool {
        return UIApplication.shared.userInterfaceLayoutDirection == .rightToLeft
    }
}

// In view controllers:
override func viewDidLoad() {
    super.viewDidLoad()
    // Use leading/trailing instead of left/right in constraints
    NSLayoutConstraint.activate([
        iconImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
        titleLabel.trailingAnchor.constraint(equalTo: iconImageView.trailingAnchor, constant: 8),
    ])
}
```

### RTL Automated Tests

```kotlin
// Android: Espresso RTL layout test
@Test
fun rtlLayout_navigationIsMirrored() {
    // Force RTL locale
    val context = ApplicationProvider.getApplicationContext<Context>()
    val config = Configuration(context.resources.configuration)
    config.setLocale(Locale("ar"))
    config.setLayoutDirection(Locale("ar"))
    val rtlContext = context.createConfigurationContext(config)

    // Launch activity with RTL configuration
    val scenario = ActivityScenario.launch<MainActivity>(
        Intent(rtlContext, MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
    )

    // Verify navigation icon is mirrored
    onView(withId(R.id.navigationIcon))
        .check(matches(isCompletelyDisplayed()))
        .check(matches(withContentDescription(containsString("arrow"))))

    // Verify text alignment is right
    onView(withId(R.id.toolbarTitle))
        .check(matches(withEffectiveVisibility(Visibility.VISIBLE)))
        .perform(object : ViewAction {
            override fun getConstraints() = isAssignableFrom(TextView::class.java)
            override fun getDescription() = "Check text alignment"
            override fun perform(uiController: UiController, view: View) {
                val tv = view as TextView
                assertEquals(
                    "Text not aligned to end (right) in RTL",
                    Gravity.END,
                    tv.gravity and Gravity.RELATIVE_HORIZONTAL_GRAVITY_MASK
                )
            }
        })
}
```

```swift
// iOS: XCTest RTL layout verification
func testRTLLayout_navigationIsMirrored() {
    let app = XCUIApplication()
    app.launchArguments = ["-AppleLanguages", "(ar)"]
    app.launch()

    // Verify the back button points right (mirrored from left)
    let backButton = app.buttons["Back"]
    XCTAssertTrue(backButton.exists, "Back button should exist in RTL")

    // Verify navigation bar layout direction
    let navBar = app.navigationBars.element(boundBy: 0)
    XCTAssertTrue(navBar.exists)

    // Check that the first element is on the right side
    let firstElement = navBar.buttons.element(boundBy: 0)
    let frame = firstElement.frame
    XCTAssertTrue(
        frame.origin.x > 0,
        "First navigation element should be on the right in RTL layout"
    )
}
```

### RTL Icon Mirroring Matrix

| Icon Category              | Mirror in RTL? | Examples                                           |
| -------------------------- | -------------- | -------------------------------------------------- |
| **Directional — temporal** | YES            | Back arrow, forward arrow, next/previous           |
| **Directional — spatial**  | YES            | Left/right chevron, slide indicators               |
| **Directional — media**    | YES            | Play (triangle pointing right stays right), rewind |
| **Non-directional**        | NO             | Home, search, settings, user avatar                |
| **Cultural**               | NO             | Currency symbols, brand logos                      |
| **Progress indicators**    | NO             | Checkmarks, close (X), info (i)                    |

**Implementation:** Use `android:autoMirrored="true"` on Android and `UIImageOrientation` semantic attributes on iOS. The Test Lead validates mirroring during RTL spot-checks.

---

## 6. Pillar E: Dynamic Content Localization

### Purpose

Server-driven strings (feature flags, remote config, API responses, A/B test variants) bypass the static resource file pipeline. This pillar ensures dynamic content degrades gracefully when localization is missing.

### Language Detection and Fallback Chain

```kotlin
// Android: Dynamic content localization with fallback chain
object DynamicContentLocalizer {

    // Fallback chain: current locale → base locale → English → key itself
    private val fallbackChain = listOf(
        Locale.getDefault(),                    // e.g., zh-Hans-CN
        Locale.getDefault().stripVariants(),     // e.g., zh-Hans
        Locale.getDefault().language,            // e.g., zh
        Locale.ENGLISH,                          // English fallback
    )

    private val remoteTranslations = mutableMapOf<String, Map<String, String>>()

    /**
     * Resolve a server-provided key to a localized string.
     * Falls back through the chain gracefully.
     */
    fun resolve(key: String): String {
        for (locale in fallbackChain) {
            val localeKey = locale.toLanguageTag()
            remoteTranslations[localeKey]?.let { translations ->
                translations[key]?.let { value ->
                    if (value.isNotBlank()) return value
                }
            }
        }
        // Final fallback: return the key itself (debugging aid)
        Log.w("DynamicContentLocalizer", "Unresolved key: $key")
        return "[$key]"
    }

    /**
     * Fetch remote translations for current locale.
     * Called during app initialization.
     */
    suspend fun fetchTranslations() {
        for (locale in fallbackChain) {
            val localeKey = locale.toLanguageTag()
            try {
                val response = api.fetchTranslations(localeKey)
                remoteTranslations[localeKey] = response.translations
            } catch (e: Exception) {
                Log.e("DynamicContentLocalizer", "Failed to fetch $localeKey: ${e.message}")
                // Continue to next fallback — don't crash
            }
        }
    }
}
```

```swift
// iOS: Dynamic content localization with fallback
class DynamicContentLocalizer {

    static let shared = DynamicContentLocalizer()

    private var translations: [String: [String: String]] = [:]

    // Fallback chain: current locale → base language → English → key
    private var fallbackChain: [String] {
        let current = Locale.preferredLanguages.first ?? "en"
        let components = current.components(separatedBy: "-")
        var chain = [current]
        if components.count > 1 {
            chain.append(components[0])
        }
        chain.append("en")
        return chain
    }

    func resolve(key: String) -> String {
        for locale in fallbackChain {
            if let value = translations[locale]?[key], !value.isEmpty {
                return value
            }
        }
        // Final fallback: bracketed key (indicates missing translation)
        os_log(.error, "DynamicContentLocalizer: unresolved key %@", key)
        return "[\(key)]"
    }

    func fetchTranslations(completion: @escaping (Result<Void, Error>) -> Void) {
        for locale in fallbackChain {
            APIClient.shared.fetchTranslations(for: locale) { result in
                switch result {
                case .success(let response):
                    self.translations[locale] = response.translations
                case .failure(let error):
                    os_log(.error, "Failed to fetch %{public}@: %{public}@", locale, error.localizedDescription)
                }
            }
        }
    }
}
```

### Graceful Degradation Tests

```kotlin
// Android: Verify dynamic content falls back gracefully
@Test
fun dynamicContent_fallbackChain_resolvesToBracketedKey() {
    // When no translations exist for any locale in the chain
    DynamicContentLocalizer.remoteTranslations.clear()

    // Should return bracketed key (not crash, not show null)
    val result = DynamicContentLocalizer.resolve("feature_promo_title")
    assertEquals("[feature_promo_title]", result)
}

@Test
fun dynamicContent_partialTranslations_fallbackWorks() {
    // English translation exists, Chinese does not
    DynamicContentLocalizer.remoteTranslations["en"] = mapOf(
        "feature_promo_title" to "New Feature Available!"
    )

    // When Chinese locale is active but missing translation
    // Should fall back to English
    val result = DynamicContentLocalizer.resolve("feature_promo_title")
    assertEquals("New Feature Available!", result)
}

@Test
fun dynamicContent_networkFailure_doesNotCrash() {
    // Simulate network failure during translation fetch
    // App should still function with fallback keys
    runBlocking {
        // fetchTranslations should not throw
        assertDoesNotThrow {
            DynamicContentLocalizer.fetchTranslations()
        }
    }
}
```

### Defect Classification for Dynamic Content Failures

| Failure Mode                             | Severity | Rationale                                             |
| ---------------------------------------- | -------- | ----------------------------------------------------- |
| App crash on missing dynamic key         | P0       | Runtime crash is always P0                            |
| Blank/empty UI element (no fallback)     | P1       | Core content area shows nothing                       |
| Bracketed key displayed `[key_name]`     | P2       | Degraded UX but functional; debug aid visible to user |
| Wrong language in fallback chain         | P2       | User sees translation in unexpected language          |
| Slight delay while fetching translations | P3       | Performance polish issue                              |

---

## 7. Test Automation

### CI/CD Pipeline Gate Configuration

```yaml
# .github/workflows/l10n-testing-gate.yml
name: Localization Testing Gate

on:
  push:
    branches: [release/**]
  pull_request:
    branches: [main]

jobs:
  # Pillar A: Pseudo-localization
  pseudo-localization:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate pseudo-localized resources
        run: python3 scripts/pseudo-localize.py \
          --input platforms/android/res/values/strings.xml \
          --output platforms/android/res/values-pseudo/strings.xml
      - name: Build with pseudo-locale
        run: ./gradlew assemblePseudoDebug
      - name: Run pseudo-localization tests
        run: ./gradlew connectedPseudoDebugAndroidTest
        continue-on-error: false

  # Pillar B: Asset verification
  asset-verification-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run asset verification tests
        run: ./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.example.l10n.LocalizationAssetVerificationTest
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: android-asset-verification
          path: '**/build/outputs/androidTest-results/**/*.xml'

  asset-verification-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run iOS asset verification
        run: xcodebuild test \
          -project CompanyApp.xcodeproj \
          -scheme CompanyApp \
          -destination 'platform=iOS Simulator,name=iPhone 15' \
          -only-testing:CompanyAppTests/LocalizationAssetVerificationTests
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ios-asset-verification
          path: '**/test-results/**/*.xml'

  # Pillar C: Cross-platform parity
  cross-platform-parity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check string key parity
        run: |
          python3 scripts/l10n-parity-check.py \
            platforms/android/res/values/strings.xml \
            platforms/ios/en.lproj/Localizable.strings \
            reviews/release/l10n-parity-report.json

  # Pillar D: RTL layout
  rtl-layout-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run RTL layout tests
        run: ./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.example.l10n.RTLLayoutTest

  rtl-layout-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run iOS RTL tests
        run: xcodebuild test \
          -project CompanyApp.xcodeproj \
          -scheme CompanyApp \
          -destination 'platform=iOS Simulator,name=iPhone 15' \
          -only-testing:CompanyAppTests/RTLLayoutTests

  # Pillar E: Dynamic content
  dynamic-content-localization:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run dynamic content localization tests
        run: ./gradlew testDebugUnitTest --tests "com.example.l10n.DynamicContentLocalizationTest"

  # Aggregate results
  l10n-gate-result:
    needs:
      [
        pseudo-localization,
        asset-verification-android,
        asset-verification-ios,
        cross-platform-parity,
        rtl-layout-android,
        rtl-layout-ios,
        dynamic-content-localization,
      ]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check all l10n gates passed
        run: |
          if [ "${{ needs.pseudo-localization.result }}" != "success" ] || \
             [ "${{ needs.asset-verification-android.result }}" != "success" ] || \
             [ "${{ needs.asset-verification-ios.result }}" != "success" ] || \
             [ "${{ needs.cross-platform-parity.result }}" != "success" ] || \
             [ "${{ needs.rtl-layout-android.result }}" != "success" ] || \
             [ "${{ needs.rtl-layout-ios.result }}" != "success" ] || \
             [ "${{ needs.dynamic-content-localization.result }}" != "success" ]; then
            echo "Localization testing gate FAILED"
            exit 1
          fi
          echo "Localization testing gate PASSED"
```

### P0-P3 Defect Classification for Localization Failures

| Level  | Localization Defect Example                                                 | Classification  |
| ------ | --------------------------------------------------------------------------- | --------------- |
| **P0** | App crashes on launch due to missing resource bundle                        | Release blocker |
| **P0** | Security breach from locale-aware string comparison (e.g., Turkish `i`/`I`) | Release blocker |
| **P1** | Core feature screen shows blank/unlocalized content                         | Release blocker |
| **P1** | 100% string parity failure between platforms                                | Release blocker |
| **P1** | RTL layout completely broken (navigation unusable)                          | Release blocker |
| **P2** | Single screen has overflow/truncation in one locale                         | User decides    |
| **P2** | Dynamic content shows bracketed key `[feature_name]`                        | User decides    |
| **P2** | One platform missing a plural form category                                 | User decides    |
| **P3** | Icon not mirrored in RTL (non-critical decorative icon)                     | User decides    |
| **P3** | Minor date/number format discrepancy in edge locale                         | User decides    |

---

## 8. Stage 9/10 Integration

### Execution Alongside LTM (Localization Team Manager)

During Stage 9, the Test Lead executes localization testing **in parallel** with the CTO-L's translation pipeline:

```
Stage 9 Timeline:
─────────────────────────────────────────────────────────
  R&D extracts strings → Platform resource files created
       │
       ├──→ CTO-L: Sends to TMS → Translators → LTM reviews → TVR
       │
       └──→ Test Lead: Pseudo-localization → Asset verification
                  → Cross-platform parity → RTL tests → Dynamic content
       │
       └──→ Both converge: Translation Verification Report +
                  Localization Test Results → Combined evidence package
```

### Evidence for Release Checklist Item #6

Release Checklist item #6 ("Localisation — all target languages complete") requires **two independent sign-offs**:

| Sign-off                  | Owner                  | Evidence                                                                                                                 |
| ------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Linguistic validation** | CTO-L                  | Translation Verification Report (translation accuracy, glossary compliance, cultural appropriateness)                    |
| **Behavioral validation** | VP Quality / Test Lead | Localization Test Results Report (asset integrity, layout correctness, parity, RTL compliance, dynamic content fallback) |

Both sign-offs must be present before item #6 is marked complete.

### Localization Test Results Report Template

```markdown
# Localization Test Results Report

**Project:** [Project Name]
**Stage:** 9 (i18n Engineering)
**Date:** [YYYY-MM-DD]
**Test Lead:** Priscilla Oduya

## Executive Summary

| Pillar                   | Status      | Defects Found              |
| ------------------------ | ----------- | -------------------------- |
| A: Pseudo-Localization   | PASS / FAIL | P0: _, P1: _, P2: _, P3: _ |
| B: Asset Verification    | PASS / FAIL | P0: _, P1: _, P2: _, P3: _ |
| C: Cross-Platform Parity | PASS / FAIL | P0: _, P1: _, P2: _, P3: _ |
| D: RTL Layout            | PASS / FAIL | P0: _, P1: _, P2: _, P3: _ |
| E: Dynamic Content       | PASS / FAIL | P0: _, P1: _, P2: _, P3: _ |

## Defect Detail

[All P0/P1 defects listed with remediation status]

## Gate Decision

- [ ] All localization tests passed — proceed to Stage 10
- [ ] P0/P1 defects remain — Stage 9 incomplete
- [ ] P2/P3 defects deferred — listed for Stage 10 user decision

**Sign-off:** \***\*\*\*\*\*\*\***\_\***\*\*\*\*\*\*\***
**Test Lead, Priscilla Oduya**
```

---

## 9. References

### Related Skills

| Skill          | Category      | Relationship                                            |
| -------------- | ------------- | ------------------------------------------------------- |
| `testing-qa`   | Test Lead     | Parent skill — test automation framework, defect triage |
| `android`      | Android Lead  | Espresso test execution, resource file structure        |
| `ios`          | iOS Lead      | XCTest execution, .lproj bundle structure               |
| `localization` | CTO-L         | Linguistic validation, TMS pipeline, i18n engineering   |
| `shared`       | Cross-cutting | TDD practices, WCAG mobile compliance                   |

### CTO-L Input

The CTO-L (Dr. Amara Osei-Mensah) provides the following inputs to this testing strategy:

- **Supported locale list** — defines which languages are in scope for testing
- **Translation priority order** — if phased rollout, Test Lead prioritizes testing accordingly
- **Glossary and style guide** — Test Lead verifies that formatting conventions (date, time, number formats) are applied correctly
- **TMS version tags** — Test Lead correlates resource file versions with TMS export versions

### External Documentation

| Reference                                       | Description                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------ |
| Google Android i18n Guidelines                  | developer.android.com/guide/topics/resources/internationalization  |
| Apple Human Interface Guidelines — Localization | developer.apple.com/design/human-interface-guidelines/localization |
| Unicode CLDR                                    | cldr.unicode.org — Plural rules, locale data, bidirectional text   |
| OWASP MASVS L1/L2                               | mas.owasp.org — Security implications of locale handling           |
| Firebase Test Lab                               | firebase.google.com/docs/test-lab — Device farm execution          |
| Xcode Cloud                                     | developer.apple.com/documentation/xcode-cloud — CI/CD for iOS      |

### Pipeline Artifacts

| Artifact                                | Location                                          | Stage |
| --------------------------------------- | ------------------------------------------------- | ----- |
| Pseudo-localization test results        | `testing/results/pseudo-l10n-results/`            | 9     |
| Asset verification report               | `testing/results/asset-verification/`             | 9     |
| Cross-platform parity report            | `reviews/release/l10n-parity-report.json`         | 9     |
| RTL layout test results                 | `testing/results/rtl-layout/`                     | 9     |
| Dynamic content test results            | `testing/results/dynamic-content/`                | 9     |
| Localization Test Results Report        | `testing/results/localization-test-report.md`     | 9     |
| Translation Verification Report (CTO-L) | `localization/translation-verification-report.md` | 9     |
| Release Checklist item #6 sign-off      | `reviews/release/release-checklist.md`            | 10    |
