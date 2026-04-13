# Localization-Ready Content Architecture

## Description

Specialized skill in structuring game content for efficient multi-language deployment. Covers string key taxonomy design, context annotation standards, text expansion budgeting, localization handoff workflows, and TMS (Translation Management System) integration. Ensures that every piece of player-facing text is written with translation efficiency in mind from the moment it is authored.

## Tools & Frameworks

| Tool / Framework                     | Version Context                     | Usage Scenario                                                                         |
| ------------------------------------ | ----------------------------------- | -------------------------------------------------------------------------------------- |
| Smartling                            | v2026+ (current)                    | TMS for translation workflow management, string key tracking, translator collaboration |
| Phrase (formerly PhraseApp)          | v2026+ (current)                    | Alternative TMS — key management, screenshot context, translation memory               |
| XLIFF 2.0                            | OASIS standard                      | Standardized localization file format for developer handoff                            |
| Figma + Locofy / Anima               | v120+ (2026)                        | Design-to-code handoff with localization-aware component exports                       |
| CLDR (Common Locale Data Repository) | v44+ (2026)                         | Plural rules, date/time formats, number formatting per locale                          |
| Custom String Key Taxonomy           | module.screen.element.state pattern | Organized key structure that maps to game architecture                                 |

## Real-World Production Scenarios

### Scenario 1: String Key Taxonomy Design

**Context:** A game with 5,000+ strings has no organized key structure. Translators receive flat lists of strings with no context, leading to mistranslations and excessive queries.
**Approach:** Design a hierarchical key taxonomy: `module.screen.element.state`. Example: `ftue.tutorial.welcome.title`, `ftue.tutorial.welcome.body`, `ftue.tutorial.gem_collection.instruction`, `shop.purchase.confirm.button`. Each key maps to a specific game location and UI element.
**Outcome:** Translator query volume reduced by 35%. Translation memory reuse increased by 22% because consistent key naming enables better TM matching.

### Scenario 2: Context Annotation Standards

**Context:** Translators receive strings like "Tap" without knowing what they're tapping, leading to incorrect translations (e.g., translating "tap" as a beer tap in German).
**Approach:** Every string includes a context annotation with: (1) Screenshot of the string in context, (2) Character limit, (3) Text expansion budget, (4) Notes for translators (e.g., "This is a verb, not a noun" / "Refers to gem collection, not water tap"). Annotations are stored in the TMS alongside the source string.
**Outcome:** Mistranslation rate reduced to < 1%. First-pass translation accuracy increased from 78% to 94%.

### Scenario 3: Text Expansion Budget Management

**Context:** English text is translated into German (+40% character expansion), and the UI breaks because buttons overflow, labels truncate, and layouts break.
**Approach:** During content design, every string is written with explicit text expansion budgets: DE/FR +40%, ES +25%, JA +15%, ZH-CN +10% (characters are denser). Figma components are tested with expanded text to verify layout integrity before translation begins. Strings that cannot accommodate expansion are rewritten for brevity.
**Outcome:** Zero UI breakage incidents post-localization. No emergency re-translation needed for layout fixes.

## Trade-Off Analysis

| Trade-Off                                           | Decision Framework                                                                                                                                                                                          | Example                                                               |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Descriptive Keys vs. Brevity**                    | Keys should be human-readable but not excessively long. `shop.purchase.confirm.button` (good) vs. `s_p_c_b` (bad) vs. `the_button_that_appears_when_the_user_is_about_to_make_a_purchase_in_the_shop` (bad) | Balance readability with maintainability                              |
| **Context Detail vs. Overhead**                     | Every string needs context, but annotating 5,000 strings manually is impractical. Automate screenshot capture and context generation from Figma components.                                                 | Screenshot auto-capture + manual notes for ambiguous strings only     |
| **Early Localization Planning vs. Iteration Speed** | Plan localization architecture early (key taxonomy, expansion budgets) but don't freeze copy until content passes playtest. Iterate in English first, then lock for translation.                            | English iteration → Playtest validation → Lock → Annotate → Translate |
| **TMS Investment vs. Manual Workflow**              | For < 500 strings, spreadsheet-based workflow is viable. For 5,000+ strings across 14 languages, TMS investment is non-negotiable.                                                                          | Smartling/Phrase pays for itself at ~2,000 strings × 5+ languages     |

## Measurable Quality Standards

| Metric                          | Target                            | Measurement Method                         |
| ------------------------------- | --------------------------------- | ------------------------------------------ |
| Localization Query Rate         | ≤ 2 queries per 100 strings       | TMS query tracking                         |
| First-Pass Translation Accuracy | ≥ 90%                             | Post-translation QA review                 |
| UI Breakage Post-Localization   | 0 incidents                       | Visual QA on all localized builds          |
| Translation Memory Reuse Rate   | ≥ 20%                             | TMS TM analytics                           |
| String Extraction Audit Pass    | 0 hardcoded strings               | Automated grep + manual spot-check         |
| Text Expansion Compliance       | 100% of strings fit within budget | Figma component testing with expanded text |

## Industry Best Practice References

| Reference                                       | Source                        | Application                                      |
| ----------------------------------------------- | ----------------------------- | ------------------------------------------------ |
| CLDR (Common Locale Data Repository)            | Unicode Consortium            | Plural rules, formatting standards per locale    |
| XLIFF 2.0 Specification                         | OASIS Standard                | Localization interchange format                  |
| "The Localizer's Handbook"                      | Esselink (2000, updated 2024) | Foundational localization engineering principles |
| Smartling Documentation                         | Smartling                     | TMS best practices, API integration              |
| Google's Localization Style Guides              | Google                        | Per-language style conventions                   |
| W3C Internationalization Best Practices         | W3C                           | Web/mobile i18n architecture patterns            |
| GDC Talk: "Localization as a Design Constraint" | Various speakers (2023–2025)  | Game-specific localization integration           |
