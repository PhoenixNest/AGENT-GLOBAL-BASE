---
version: "1.0.0"
---

# Flutter I18n

| Competency       | Description                                                                                            | Quality Criteria                                                                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flutter intl     | flutter_localizations setup, Intl.message, Intl.plural, Intl.select, date/number formatting            | All user-facing strings use Intl or AppLocalizations; date/number formatting respects locale; no hardcoded strings in widgets                        |
| ARB Files        | ARB structure, placeholder metadata, attribute annotations, gen_l10n configuration, ARB validation     | ARB files follow consistent structure; placeholders have proper metadata; gen_l10n generates type-safe localization class                            |
| Pluralization    | Intl.plural with all forms, zero/one/two/few/many/other, locale-specific rules, gender-based selection | All plural forms implemented per CLDR rules; zero form handled for languages that require it; gender selection for languages with grammatical gender |
| RTL Support      | Directionality widget, RTL-aware layouts, mirror icons, text alignment, RTL testing                    | Full RTL layout support for Arabic/Hebrew; icons mirrored appropriately; text alignment adapts to direction; no hardcoded LTR assumptions            |
| Locale Switching | Runtime locale change, persistence, system locale detection, locale fallback, supported locales list   | Locale persists across app restarts; fallback to closest supported locale; system locale detected on first launch; locale switch is seamless         |

## Pipeline Integration

- **Stage 5 (Development):** All user-facing strings externalized via ARB files. No hardcoded strings in widget code. RTL-aware layouts from the start.
- **Stage 9 (i18n Engineering):** Primary stage for this skill. Phase 1: R&D extracts strings and validates ARB files. Phase 2: Localization Department translates via TMS.
- **Stage 10 (Release Readiness):** Translation completeness verified. All target languages must have 100% translation coverage before release.

## Quality Standards

- **Zero** hardcoded user-facing strings in widget code — all strings in ARB files
- **100%** ARB files pass `flutter gen-l10n` compilation without errors
- All ARB placeholders have **metadata** (description, type, example)
- Pluralization uses **CLDR-compliant** forms — all required forms per language
- RTL layouts tested for **all RTL-supported languages** (Arabic, Hebrew)
- **DirectionalEdgeInsets** used instead of EdgeInsets (start/end vs left/right)
- Icons that imply direction are **mirrored in RTL** mode
- Locale preference **persists** across app restarts via SharedPreferences
- Runtime locale switching **rebuilds** the MaterialApp with new locale
- `untranslated-messages-file` checked on CI — **zero** untranslated messages for release
- Translation Verification Report **signed off** by CTO-L before Stage 10 release
- Date and number formatting **respects locale** — DateFormat and NumberFormat with locale parameter
- ARB files validated for **key consistency** across all locales — no missing keys

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
