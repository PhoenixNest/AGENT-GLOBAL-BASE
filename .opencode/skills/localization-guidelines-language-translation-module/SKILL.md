---
name: localization-guidelines-language-translation-module
description: "Localization skill: Language Translation Module"
---

# Language Translation Module

## Purpose

This module governs every translation request submitted to the Localization Department. It is invoked by the CTO-L whenever the R&D Department delivers extracted strings and datasets for translation during Stage 9 (Internationalization Engineering) of the development pipeline. No translation work proceeds outside this module.

---

## Phase 1: String Extraction Validation

Before any translation begins, the CTO-L validates that the R&D Department's extraction is complete.

**Checklist — must be fully satisfied before proceeding to Phase 2:**

- [ ] All UI string resource files are present and correctly structured:
  - Android: `res/values/strings.xml` (default), `res/values-<lang>/strings.xml` (per language: `res/values-zh/strings.xml`, `res/values-ja/strings.xml`, etc.)
  - iOS: `Localizable.strings`, `Localizable.stringsdict` (for pluralisation rules)
- [ ] Zero hardcoded strings remain in the codebase (verified by CTO-L review of R&D's extraction report)
- [ ] All additional datasets requiring localisation (JSON files, onboarding content, in-app help text) are included in the handoff package
- [ ] String keys follow a consistent naming convention (e.g., `screen_name.component.description`)
- [ ] Strings with dynamic variables are correctly formatted using platform conventions:
  - Android: `%1$s`, `%2$d` positional format specifiers
  - iOS: `%@`, `%d` format specifiers

If any checklist item fails, the CTO-L returns the handoff package to the R&D Department with a written list of deficiencies. Phase 2 does not begin until all items pass.

---

## Phase 2: Translation Workflow

**Step 1: Translation Memory (TM) Leverage Analysis**

Before dispatching strings for translation, the CTO-L runs a TM leverage analysis against the department's translation memory database to identify:

- **100% matches** — identical strings translated in previous projects; reuse directly.
- **Fuzzy matches (75–99%)** — similar strings; route to linguist for light post-editing.
- **No match (0–74%)** — new strings; route to full translation workflow.

**Step 2: Machine Translation First Pass**

All no-match strings are passed through the approved neural MT pipeline (DeepL primary, Google Neural MT fallback) to produce a first-pass translation for each target language.

**Step 3: Native-Speaker Linguist Post-Editing**

All MT output is reviewed and corrected by certified native-speaker linguists for each target language:

| Language                   | Linguist Standard                                             |
| -------------------------- | ------------------------------------------------------------- |
| English (EN)               | Source language — no translation required                     |
| Chinese Simplified (ZH-CN) | Native Mandarin speaker, HSK-equivalent professional literacy |
| Japanese (JA)              | Native Japanese speaker, JLPT N1 certified                    |
| Korean (KO)                | Native Korean speaker, TOPIK Level 6 certified                |
| French (FR)                | Native French speaker, C2 CEFR or equivalent                  |

Additional languages specified by the user follow the same native-speaker standard. The CTO-L maintains an active roster of certified linguists per language pair.

**Step 4: Style Guide Compliance Review**

Each translation is reviewed against the platform-specific style guide for:

- Tone and register (formal vs. casual per app context)
- Brand terminology consistency (product names, feature names must not be translated unless explicitly specified)
- Character count constraints (UI labels have display length limits on mobile — linguists flag any translation exceeding the source string length by >40%; flagged strings are returned to the linguist for condensation or, if condensation is not linguistically possible, escalated to the CDO for UI layout adjustment before Phase 4)

---

## Phase 3: Platform-Specific Formatting Validation

After translation, the CTO-L validates locale-specific formatting correctness across all target languages:

| Format Type   | Validation Rule                                                                                                                                                                                                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Date/time     | Verify locale-correct formats (e.g., `MM/DD/YYYY` for EN-US, `YYYY年MM月DD日` for JA)                                                                                                                                                                                                                           |
| Currency      | Verify locale-correct symbol placement and decimal separators                                                                                                                                                                                                                                                   |
| Numbers       | Verify thousand separators and decimal notation per locale                                                                                                                                                                                                                                                      |
| Pluralisation | Verify `stringsdict` (iOS) and `plurals` (Android) rules are correctly implemented for each language's plural form count                                                                                                                                                                                        |
| RTL support   | If any target language is RTL (e.g., Arabic, Hebrew — if added by user), verify: (1) `android:supportsRtl="true"` is set in `AndroidManifest.xml`; (2) iOS `UISemanticContentAttribute` is configured; (3) visual spot-check of mirrored layouts on a device or emulator confirms correct directional rendering |

---

## Phase 4: Linguistic QA Gate

Before issuing the Translation Verification Report, the CTO-L runs a final linguistic QA pass:

- [ ] No untranslated source-language strings remain in any target language resource file
- [ ] No placeholder strings (e.g., `TODO`, `FIXME`, `[TRANSLATE]`) remain in any resource file
- [ ] All dynamic variable placeholders are preserved correctly in translated strings
- [ ] Brand names and product feature names are correctly preserved (not mistranslated)
- [ ] No truncation issues flagged by linguists remain unresolved
- [ ] All plural form rules are correctly implemented for each target language

---

## Phase 5: Translation Verification Report

Upon passing all four phases, the CTO-L issues the **Translation Verification Report** — a structured sign-off document confirming:

1. **String coverage:** Total strings extracted vs. total strings translated (must be 100%)
2. **Language coverage:** List of all target languages with completion status (must be 100% for all)
3. **TM leverage summary:** Percentage of strings that were 100% matches, fuzzy matches, and new translations
4. **Linguist attestation:** Names and certification credentials of native-speaker linguists who reviewed each language
5. **Outstanding issues:** Any P2/P3 issues (e.g., minor style guide deviations) flagged for future improvement — these do not block release
6. **CTO-L sign-off:** Dated signature confirming the localized codebase meets the Language Translation Module standard

This report is archived alongside the localized codebase and presented as evidence for the **Localisation** checklist item (item #6) in the Stage 10 Release Readiness Check.
