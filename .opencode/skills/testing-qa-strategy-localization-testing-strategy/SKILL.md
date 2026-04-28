---
name: testing-qa-strategy-localization-testing-strategy
description: Localization testing strategy for mobile apps — string extraction validation, text expansion/contraction testing, plural form coverage, RTL layout validation, locale-specific formatting (dates, numbers, currencies), and translation quality verification. Owned by Aisha Patel (VP Quality). Use during Stage 9 (i18n Engineering) for localization test execution and Stage 10 (Release Readiness) for localization sign-off. Trigger: localization testing, string extraction validation, text expansion, plural forms, RTL layout, locale formatting, translation quality, i18n testing.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
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

## Defect Detail

[All P0/P1 defects listed with remediation status]

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`3.-pillar-b:-l10n-asset-verification.md`](references/3.-pillar-b:-l10n-asset-verification.md) — 3. Pillar B: L10n Asset Verification
- [`4.-pillar-c:-cross-platform-string-parity.md`](references/4.-pillar-c:-cross-platform-string-parity.md) — 4. Pillar C: Cross-Platform String Parity
- [`5.-pillar-d:-rtl-layout-testing.md`](references/5.-pillar-d:-rtl-layout-testing.md) — 5. Pillar D: RTL Layout Testing
- [`6.-pillar-e:-dynamic-content-localization.md`](references/6.-pillar-e:-dynamic-content-localization.md) — 6. Pillar E: Dynamic Content Localization
- [`7.-test-automation.md`](references/7.-test-automation.md) — 7. Test Automation
- [`executive-summary.md`](references/executive-summary.md) — Executive Summary
- [`gate-decision.md`](references/gate-decision.md) — Gate Decision
- [`9.-references.md`](references/9.-references.md) — 9. References
```
