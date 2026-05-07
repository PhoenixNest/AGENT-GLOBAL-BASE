---
name: localization-testing-strategy
description: Localization testing strategy for mobile and web products — pseudo-localization validation, TMS string verification, i18n layout regression testing, character expansion budgets, and RTL/bidirectional layout QA. Integrates with the Stage 9 i18n Engineering pipeline owned by CTO-L. Use at Stage 7 (Automated Testing) and Stage 8 (Integrity Verification).
version: "1.0.0"
---

# Localization Testing Strategy

## Purpose

Ensure that every localized build passes engineering quality gates before the CTO-L's Stage 9 i18n sign-off. Localization testing is not the same as translation quality review — that is CTO-L's domain. Aisha Patel owns the engineering side: string ingestion integrity, layout regression under expansion, RTL correctness, and automated detection of broken placeholders, missing strings, and truncation defects.

## Why This Matters

A translation escape to production — a UI element truncating Korean text, a broken Arabic RTL layout, or a missing `%s` placeholder in a French error message — is classified as a P1 localization defect and triggers the Stage 9 re-entry process. The testing strategy below catches all three categories before they reach CTO-L's Translation Verification Report.

## Pseudo-Localization: Catch Layout Bugs Before Translation

Pseudo-localization replaces all source strings with expanded, accented approximations that stress-test UI layouts without requiring real translations.

### Implementation

```typescript
// i18n/pseudo-localize.ts
export function pseudoLocalize(text: string): string {
  const charMap: Record<string, string> = {
    a: "à",
    b: "ƀ",
    c: "ć",
    d: "ď",
    e: "è",
    f: "ƒ",
    g: "ĝ",
    h: "ĥ",
    i: "ì",
    // ... full map
  };
  const expanded =
    "[!! " +
    text
      .split("")
      .map((c) => charMap[c.toLowerCase()] || c)
      .join("") +
    " !!]";
  return expanded; // ~40% character expansion applied
}
```

**Pseudo-locale build:** Add `pseudo` to the supported locales list. CI runs the pseudo-locale build and runs Playwright visual regression tests on all critical routes. Any text truncation, layout overflow, or clipped element is a P1 defect.

### Character Expansion Budgets

UI elements must accommodate expansion without truncation. Minimum budgets (enforced in Playwright layout tests):

| String Length (EN) | Minimum Expansion Budget |
| ------------------ | ------------------------ |
| 1–10 chars         | 100% (double the width)  |
| 11–20 chars        | 80%                      |
| 21–50 chars        | 60%                      |
| 51+ chars          | 40%                      |

```typescript
// Playwright test: verify no text truncation in pseudo-locale
test("no truncation in pseudo-locale — navigation menu", async ({ page }) => {
  await page.goto("/?locale=pseudo");
  const menuItems = await page.locator("nav a").all();
  for (const item of menuItems) {
    const box = await item.boundingBox();
    const scrollWidth = await item.evaluate((el) => el.scrollWidth);
    const clientWidth = await item.evaluate((el) => el.clientWidth);
    expect(scrollWidth, `Truncation detected in nav item`).toBeLessThanOrEqual(
      clientWidth + 1,
    ); // 1px tolerance
  }
});
```

## TMS String Integrity Verification

After strings are exported from the TMS and imported into the codebase, automated tests verify:

### Placeholder Integrity

Every source string with a placeholder must have a corresponding valid placeholder in every translation:

```typescript
// tests/i18n/placeholder-integrity.spec.ts
import { sourceStrings, allLocaleStrings } from "../i18n";

describe("Placeholder integrity", () => {
  const PLACEHOLDER_REGEX = /%[sd]|\{\{[^}]+\}\}|\{[0-9]+\}/g;

  for (const [key, enValue] of Object.entries(sourceStrings)) {
    const enPlaceholders = enValue.match(PLACEHOLDER_REGEX) || [];
    if (enPlaceholders.length === 0) continue;

    for (const [locale, strings] of Object.entries(allLocaleStrings)) {
      test(`${locale}/${key} — all placeholders present`, () => {
        const localePlaceholders =
          (strings[key] || "").match(PLACEHOLDER_REGEX) || [];
        expect(localePlaceholders.sort()).toEqual(enPlaceholders.sort());
      });
    }
  }
});
```

### Missing String Detection

```typescript
test("no missing strings in any supported locale", () => {
  const supportedLocales = ["fr", "de", "ja", "ko", "zh-TW", "pt-BR", "ar"];
  for (const locale of supportedLocales) {
    const missingKeys = Object.keys(sourceStrings).filter(
      (key) => !allLocaleStrings[locale]?.[key],
    );
    expect(missingKeys, `Missing strings in ${locale}`).toHaveLength(0);
  }
});
```

## RTL / Bidirectional Layout Testing

For Arabic (ar) and Hebrew (he) locales:

```typescript
test("Arabic locale — RTL layout is correct", async ({ page }) => {
  await page.goto("/?locale=ar");

  // Verify html[dir=rtl] is set
  const dir = await page.locator("html").getAttribute("dir");
  expect(dir).toBe("rtl");

  // Verify text alignment is right-justified on key elements
  const heading = page.locator("h1").first();
  const textAlign = await heading.evaluate(
    (el) => window.getComputedStyle(el).textAlign,
  );
  expect(["right", "start"]).toContain(textAlign);

  // Verify navigation order is reversed (last item in DOM is leftmost visually)
  const navItems = await page.locator("nav a").all();
  const firstItemX = (await navItems[0].boundingBox())!.x;
  const lastItemX = (await navItems[navItems.length - 1].boundingBox())!.x;
  expect(firstItemX).toBeGreaterThan(lastItemX);
});
```

## Localization Test Execution in CI/CD

| Stage                       | Tests Run                                  | Gate                      |
| --------------------------- | ------------------------------------------ | ------------------------- |
| PR (UI-touching)            | Pseudo-locale layout tests                 | Blocks merge              |
| Nightly                     | Full pseudo-locale + placeholder integrity | Blocks Stage 9 if failing |
| Stage 7 (Automated Testing) | All localization tests + RTL tests         | Blocks Stage 8            |
| Stage 9 (i18n Engineering)  | CTO-L's Translation Verification Report    | Blocks Stage 10           |

## Quality Standards

- Zero pseudo-locale truncation defects before Stage 7 sign-off
- 100% placeholder integrity across all supported locales before Stage 9 entry
- Zero missing strings in any supported locale before Stage 9 entry
- RTL layout tests pass for all RTL-targeted locales (ar, he) before Stage 7 sign-off
- All localization tests run in ≤10 minutes as part of the nightly build
