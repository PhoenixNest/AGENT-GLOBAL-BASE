# Accessibility Scanner Tools

## Accessibility Scanner Tools

Automated and semi-automated tools identify accessibility issues that may be missed during manual testing.

### Android Accessibility Scanner

| Feature                    | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| Touch target size          | Flags elements below 48x48dp minimum                  |
| Contrast                   | Measures foreground/background contrast ratio         |
| Content labeling           | Identifies images/buttons without contentDescription  |
| Clickable element labeling | Flags clickable elements missing contentDescription   |
| Implementation             | Install from Play Store; overlay scans current screen |

#### Using Android Accessibility Scanner

1. Install Android Accessibility Scanner from Google Play Store
2. Enable the service in Settings > Accessibility > Android Accessibility Scanner
3. Navigate to the screen to test in the target application
4. Tap the scanner floating action button
5. Review reported issues — tap each suggestion for details
6. Document findings in the accessibility audit report

### iOS Accessibility Inspector

| Feature             | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Element inspection  | Hover over elements to see accessibility properties          |
| Traits verification | Verify label, traits, value, and hints                       |
| Color contrast      | Built-in contrast checker                                    |
| Smart invert        | Test inverted color rendering                                |
| Implementation      | Built into Xcode > Developer Tools > Accessibility Inspector |

#### Using iOS Accessibility Inspector

1. Launch Xcode > Developer Tools > Accessibility Inspector
2. Select the running application or device
3. Use the inspection pointer to hover over elements
4. Review accessibility properties: label, traits, value, hints
5. Use the contrast checker to verify color ratios
6. Document findings in the accessibility audit report

### Automated Audit Checklist

| Tool                          | Platform | Checks Performed                                         | Limitations                                     |
| ----------------------------- | -------- | -------------------------------------------------------- | ----------------------------------------------- |
| Android Accessibility Scanner | Android  | Touch target, contrast, content labels, clickable labels | Does not check reading order, logical structure |
| iOS Accessibility Inspector   | iOS      | Element properties, contrast, traits                     | Manual inspection required; not batch scanning  |
| Lint (accessibility checks)   | Android  | Missing contentDescription, labelFor, autofill hints     | Static analysis only; no runtime checking       |
| SwiftLint + SwiftLint rules   | iOS      | accessibilityLabel presence, trait checks                | Static analysis only; no runtime checking       |
| Espresso accessibility checks | Android  | Programmatic verification during automated tests         | Requires writing test code                      |
| XCTest accessibility checks   | iOS      | Programmatic verification during automated tests         | Requires writing test code                      |

### Scanner Findings Template

```markdown

```
