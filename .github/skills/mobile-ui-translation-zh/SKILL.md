---
name: mobile-ui-translation-zh
description: Mobile UI string translation and quality assurance for Chinese (Simplified). Covers Language Translation Module workflow, character limit compliance, platform writing conventions (iOS HIG, Android Material Design), register calibration, MT post-editing, and linguistic QA gate before Translation Verification Report.
---

# Mobile UI Translation (Chinese Simplified)

## Purpose

Translate mobile UI strings from the EN-source handoff package into Chinese Simplified (ZH-CN), produce correctly structured platform resource files, and pass the linguistic QA gate before delivery to the Chief Translation Officer for the Translation Verification Report.

All translation work operates within the **Language Translation Module** — the governing framework owned by the Chief Translation Officer (CTO-L). This skill defines the linguist's execution workflow within that framework.

## Workflow

### Phase 1: String Intake and Analysis

Receive from the CTO-L:

- EN-source `strings.xml` (Android) with translator context comments
- EN-source `Localizable.strings` + `Localizable.stringsdict` (iOS) with context comments
- `key-index.csv` — full key list with context, character limits, and platform
- Any JSON content datasets requiring localization
- Project style guide and glossary (if available)

Before beginning translation:

1. Read all context comments — never translate without context
2. Review the character limit column in `key-index.csv` — flag any source string that will be impossible to translate within the limit and notify the CTO-L before starting
3. Review the project glossary — identify terminology that must be used consistently
4. Identify strings requiring plural form handling — confirm plural rule coverage for your language

### Phase 2: Translation

**Character limit compliance:**

- Translate within the character limit specified for each key
- Chinese characters are typically more compact than English — use this advantage for UI labels

**Register consistency:**

- Determine the appropriate formality register at the start of the project — do not switch register mid-project
- Button labels: use imperative form in the target language convention
- Error messages: direct but non-alarming; avoid technical jargon visible to end users
- Onboarding: conversational and welcoming, consistent with the product's tone

**Platform conventions:**

- iOS: respect Apple's localization guidelines for Chinese
- Android: respect Material Design writing guidelines for Chinese
- Do not translate interface element names where the English term is the established convention

**MT post-editing:**
If the CTO-L provides a machine-translated first-pass:

1. Read every string — never accept MT output without review
2. Fix: gender agreement, false cognates, register drift, idiomatic errors, named entity mistranslation
3. Apply the project glossary — override MT output where it contradicts agreed terminology
4. Mark any string where MT was substantially rewritten (>50% changed) — flag for CTO-L awareness

### Phase 3: Plural Form Coverage

Chinese (ZH-CN) has no grammatical plurals — only the `other` quantity form is required.

### Phase 4: Self-Review QA

Before submitting to the CTO-L, perform a self-review pass:

**Consistency check:**

- [ ] All instances of the same term use the same translation (cross-reference with glossary)
- [ ] Register is consistent across all strings in the batch
- [ ] Plural forms are complete for all quantity-sensitive strings

**Technical check:**

- [ ] Format specifiers preserved exactly: `%1$s`, `%@`, `{count}` — never translated or reordered
- [ ] Character limits respected for all strings
- [ ] No machine-translated strings left unreviewed

**Platform check:**

- [ ] Android: `strings.xml` structure valid; context comments preserved
- [ ] iOS: `Localizable.strings` key names unchanged; `.stringsdict` plural entries complete

### Phase 5: Delivery to CTO-L

Deliver to the Chief Translation Officer:

- Translated resource files in the correct format for the target platform(s)
- A brief QA note: total string count, plural strings count, any strings flagged for CTO-L review, any character limit escalations
- Confirmation that self-review QA checklist is complete

The CTO-L conducts the final Translation Verification review. The linguist is available for follow-up questions during the CTO-L's review cycle.

## Quality Standards

| Dimension                     | Standard                                                      |
| ----------------------------- | ------------------------------------------------------------- |
| Terminology accuracy          | 100% — zero incorrect technical terms                         |
| Register consistency          | 100% — no register switching within a project                 |
| Character limit compliance    | 100% — zero strings exceeding their limit                     |
| Format specifier preservation | 100% — zero format specifier errors (these cause app crashes) |
| Plural form coverage          | 100% — all required forms present                             |
