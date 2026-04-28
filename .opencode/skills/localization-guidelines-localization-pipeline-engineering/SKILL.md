---
name: localization-guidelines-localization-pipeline-engineering
description: Localization pipeline design and operation — TMS integration (Phrase/Lokalise), extraction validation, string push/pull, format specifier linting, character limit validation, plural form coverage checks, XML/HTML tag preservation validation, and platform resource file generation for iOS and Android. Owned by the Localization Engineer. Use during Stage 9 (i18n Engineering) for localization pipeline setup and string resource management. Trigger: localization pipeline, TMS integration, string extraction validation, format specifier linting, plural form coverage, resource file generation.
prerequisites:
  - localization-overview

version: "1.0.0"
---

# Localization Pipeline Engineering

## Purpose

Build and maintain the technical infrastructure that moves strings from the R&D handoff package through the translation workflow and back into production-ready platform resource files. This role is engineering — not linguistic. All linguistic decisions belong to the linguists and the CTO-L.

## Pipeline Architecture

The localization pipeline has four phases:

```
[R&D Handoff Package]
        ↓
[Phase 1: Extraction Validation]   ← verify handoff package is complete
        ↓
[Phase 2: TMS Push]                ← push source strings to translation management system
        ↓
[Phase 3: Translation]             ← linguists work in TMS (not in this skill)
        ↓
[Phase 4: Pull + Validation]       ← pull translated strings, run validation linting
        ↓
[Phase 5: Resource File Generation]← produce platform-ready output files
        ↓
[CTO-L Translation Verification Review]
```

## Phase 1: Extraction Validation

Receive the i18n handoff package from the Internationalization Specialist.

Validate before pushing to TMS:

- [ ] `strings.xml` is well-formed XML — parse and verify
- [ ] `Localizable.strings` is valid UTF-8 (or UTF-16 for Xcode compat)
- [ ] `Localizable.stringsdict` is valid plist XML
- [ ] All format specifiers are indexed (`%1$s` not `%s`) — non-indexed specifiers are ambiguous for translators and error-prone
- [ ] All keys in code references exist in resource files (cross-reference with key-index.csv)
- [ ] No duplicate keys in any resource file
- [ ] Character limit annotations are present in key-index.csv for all strings

Report any validation failures to the CTO-L before proceeding.

## Phase 2: TMS Push

Push source strings to the TMS (Phrase/Lokalise/other per project configuration):

**Via Phrase CLI (example):**

```bash
phrase push \
  --access-token $PHRASE_ACCESS_TOKEN \
  --project-id $PROJECT_ID \
  --locale-id en \
  --file "i18n-handoff/android/strings.xml" \
  --file-format xml \
  --update-translations \
  --skip-upload-tags
```

Verify after push:

- [ ] String count in TMS matches string count in source file
- [ ] No strings were rejected by TMS validation
- [ ] Translation jobs are created and assigned to the correct linguist team

## Phase 3: Translation (Linguist-owned)

During active translation, the Localization Engineer monitors TMS status and is available for technical questions:

- Format specifier clarification (what does `%1$s` refer to in this string?)
- Character limit confirmation
- Plural form structure questions
- Key naming questions

Does NOT make linguistic decisions. Escalate all linguistic questions to the CTO-L.

## Phase 4: Pull + Validation Linting

Pull translated files from TMS when linguists mark batches complete:

```bash
phrase pull \
  --access-token $PHRASE_ACCESS_TOKEN \
  --project-id $PROJECT_ID \
  --locale-id zh-Hans \
  --output "translated/android/zh-Hans/strings.xml" \
  --file-format xml
```

Run the validation linter on all pulled files:

### Format Specifier Validation

For every translated string containing a format specifier:

- Verify the same specifiers are present in the translation (no added, removed, or changed specifiers)
- Verify indexed specifiers use the correct index (`%1$s` stays `%1$s`)
- Android: flag any `%s` or `%d` without index — these crash on some locales
- iOS: flag any `%@` converted to `%s` — type mismatch

### Character Limit Validation

Cross-reference each translated string against key-index.csv:

- Flag any string exceeding its character limit
- Report: key name, limit, actual character count, exceeded by N characters
- Do NOT silently truncate — report and escalate to CTO-L

### Plural Form Validation

Verify plural form coverage per language:

- ZH, JA, KO: must have `other` quantity; no other forms required
- EN, FR: must have `one` and `other`
- Confirm all `<plurals>` elements in Android XML and all stringsdict entries in iOS are complete

### XML/HTML Tag Preservation

For any string containing `<b>`, `<i>`, `<u>`, or `<xliff:g>` tags:

- Verify all tags are present and correctly closed in the translation
- Flag any tag added or removed by the translator (common MT error)

### Validation Report

After running all checks, produce a Validation Report for the CTO-L:

```markdown
# Validation Report — {Language} — {Date}

## Summary

- Total strings validated: {N}
- Passed: {N}
- Warnings (non-blocking): {N}
- Errors (blocking — must fix before delivery): {N}

## Errors

[Table: key | error type | description]

## Warnings

[Table: key | warning type | description]

## Recommendation

[ ] All errors resolved — ready for CTO-L linguistic review
[ ] N errors remain — not ready; awaiting linguist correction
```

## Phase 5: Resource File Generation

After validation passes, produce the final platform resource files:

**Android:**

- `res/values-zh-rCN/strings.xml` (ZH-CN Simplified)
- `res/values-zh-rTW/strings.xml` (ZH-TW Traditional)
- `res/values-ja/strings.xml` (Japanese)
- `res/values-ko/strings.xml` (Korean)
- `res/values-fr/strings.xml` (French)

**iOS:**

- `zh-Hans.lproj/Localizable.strings` + `Localizable.stringsdict`
- `zh-Hant.lproj/Localizable.strings` + `Localizable.stringsdict`
- `ja.lproj/Localizable.strings` + `Localizable.stringsdict`
- `ko.lproj/Localizable.strings` + `Localizable.stringsdict`
- `fr.lproj/Localizable.strings` + `Localizable.stringsdict`

Verify all files build cleanly in a test app build before delivering to CTO-L.

## Delivery to CTO-L

Deliver:

- All platform resource files in the correct directory structure
- Validation Report confirming all checks passed (or listing outstanding issues)
- A brief pipeline run summary: string counts per language, any anomalies noted

The CTO-L then conducts the final linguistic Translation Verification review.
