---
name: localization-engineering-and-cicd-gates
description: Localization engineering pipeline for Stage 9 — string freeze protocol, CI/CD hardcoded-string scanning, TMS integration with the codebase, XLIFF/ARB export/import automation, and the Translation Verification Report (TVR) production process. Use at Stage 9 (i18n Engineering) to execute the localization engineering workflow or when setting up CI gates to prevent i18n regressions.
version: "1.0.0"
---

# Localization Engineering and CI/CD Gates

## Purpose

Execute the engineering side of Stage 9 (i18n Engineering). Dr. Amara Osei-Mensah owns the full Stage 9 pipeline: extraction, TMS handoff, machine translation + post-editing, linguist review, re-integration, automated QA, and Translation Verification Report (TVR). This skill covers the **engineering mechanics** — the CI/CD gates, tooling, and automation that turn a source codebase into a localized build with traceable, auditable quality.

## Why This Matters

Localization that is not automated is localization that regresses. A string hardcoded in a release build, a missing XLIFF key, or an unreviewed machine translation that reaches production is a P1 defect that triggers Stage 9 re-entry. Engineering gates catch these before Dr. Osei-Mensah's linguists ever see the file.

## Stage 9 Workflow

```
Source Code (Stage 5 complete) → String Freeze → Extraction → TMS Import → MT + Review →
Re-integration → Automated QA (Aisha Patel, see localization-testing-strategy.md) →
TVR (Dr. Osei-Mensah) → Stage 10
```

## String Freeze Protocol

A string freeze means: **no new user-visible strings may be merged into the release branch after this date.** String freeze is declared by Dr. Osei-Mensah in coordination with the CTO after Stage 5 development is complete.

**String freeze enforcement in CI:**

```yaml
# .github/workflows/string-freeze.yml
on:
  push:
    branches: [release/**]
jobs:
  enforce-string-freeze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Check for new localizable strings since freeze commit
        run: |
          FREEZE_COMMIT=$(cat .string-freeze-sha)
          NEW_STRINGS=$(git diff $FREEZE_COMMIT HEAD -- '**/strings.xml' '**/*.strings' '**/*.arb' | grep '^+' | grep -v '^+++' | wc -l)
          if [ "$NEW_STRINGS" -gt 0 ]; then
            echo "String freeze violation: $NEW_STRINGS new string entries added after freeze"
            exit 1
          fi
```

**Who can override:** String freeze violations require joint approval from Dr. Osei-Mensah + CTO. Every override is logged in the Stage 9 audit trail with justification.

## Hardcoded String CI Gate

No user-visible string may be hardcoded in production source code. The CI/CD pipeline runs a hardcoded-string scanner on every PR:

```yaml
# .github/workflows/hardcoded-strings.yml
jobs:
  hardcoded-string-scan:
    steps:
      - name: Scan for hardcoded strings (Android)
        run: |
          # Flag any hardcoded String literals in UI-layer files
          rg --type kotlin --type java '"[A-Z][a-z]{3,}"' app/src/main/ \
            --glob '!**/strings.xml' \
            --glob '!**/*Test*' \
            --glob '!**/BuildConfig*' \
            -l | while read f; do
              echo "Potential hardcoded string in: $f"
            done

      - name: Scan for hardcoded strings (iOS)
        run: |
          rg --type swift '"[A-Z][a-z]{3,}"' ios/ \
            --glob '!**/*Tests*' \
            --glob '!**/Localizable.strings' \
            -l | while read f; do
              echo "Potential hardcoded string in: $f"
            done
```

False positives are suppressed with an inline comment: `// i18n-ignore: technical identifier, not user-visible`. Every suppression is reviewed by Dr. Osei-Mensah before Stage 9 begins.

## TMS Integration

The company uses a Translation Management System (TMS) integrated with the source repository.

### String Export (Source → TMS)

```bash
# Android: extract from strings.xml to XLIFF 1.2
xliff-tool export \
  --source app/src/main/res/values/strings.xml \
  --output ./localization/export/android-strings-v{VERSION}.xliff \
  --source-language en-US \
  --target-languages fr,de,ja,ko,zh-TW,pt-BR,ar

# iOS: export from Localizable.strings to XLIFF 1.2
xcodebuild \
  -exportLocalizations \
  -localizationPath ./localization/export/ \
  -exportLanguage en
```

Each export package is version-stamped with the release candidate SHA and uploaded to the TMS project.

### Machine Translation + Post-Editing

Dr. Osei-Mensah manages the MT + post-editing pipeline:

1. MT provider translates the XLIFF package (DeepL API for high-quality languages; GPT-4o for lower-resource languages)
2. Professional linguists perform post-editing using the company-specific glossary and tone guide
3. All segments flagged as `needs-review` by the MT provider are human-reviewed before export

**MT quality gate (per language pair):**

| Quality Threshold              | Action                                           |
| ------------------------------ | ------------------------------------------------ |
| BLEU ≥ 45 (sentence-level avg) | Accept MT + spot-check human review (20% sample) |
| BLEU 30–44                     | Accept MT + full human review                    |
| BLEU < 30                      | Reject MT; full human translation required       |

### String Re-integration (TMS → Repository)

```bash
# Android: import XLIFF translations back to values-{locale}/strings.xml
xliff-tool import \
  --xliff ./localization/import/android-strings-v{VERSION}-{LOCALE}.xliff \
  --output app/src/main/res/values-{LOCALE}/strings.xml

# iOS: import to Localizable.strings per locale
xcodebuild \
  -importLocalizations \
  -localizationPath ./localization/import/ios-v{VERSION}/
```

After import, the automated QA suite (owned by VP Quality Aisha Patel — see `localization-testing-strategy.md`) runs before the TVR is issued.

## Translation Verification Report (TVR)

The TVR is the Stage 9 gate artifact. Dr. Osei-Mensah issues the TVR only after:

1. All strings imported and automated QA passes (Aisha Patel sign-off)
2. All linguist reviews complete
3. Platform store metadata localized and reviewed

**TVR structure:**

```markdown
# Translation Verification Report — [Project Name] v[VERSION]

**Date:** YYYY-MM-DD
**Issued by:** Dr. Amara Osei-Mensah, CTO-L
**Build SHA:** [commit hash]

## Localization Coverage

| Locale | Strings Total | Translated | Review Complete | Issues       |
| ------ | ------------- | ---------- | --------------- | ------------ |
| fr     | 847           | 847 (100%) | ✅              | 0            |
| de     | 847           | 847 (100%) | ✅              | 0            |
| ja     | 847           | 847 (100%) | ✅              | 0            |
| ko     | 847           | 847 (100%) | ✅              | 0            |
| zh-TW  | 847           | 847 (100%) | ✅              | 2 resolved   |
| pt-BR  | 847           | 847 (100%) | ✅              | 0            |
| ar     | 847           | 847 (100%) | ✅              | RTL verified |

## Automated QA Status

| Check                    | Result  |
| ------------------------ | ------- |
| Placeholder integrity    | ✅ PASS |
| Missing strings          | ✅ PASS |
| Pseudo-locale truncation | ✅ PASS |
| RTL layout (ar)          | ✅ PASS |

## Store Metadata

| Locale | App Name | Subtitle | Description | Keywords |
| ------ | -------- | -------- | ----------- | -------- |
| fr     | ✅       | ✅       | ✅          | ✅       |

## Verdict

**[APPROVED / BLOCKED — reason]**

Dr. Amara Osei-Mensah's signature: \***\*\_\_\_\*\***
```

## Quality Standards

- String freeze CI gate active before Stage 9 begins; zero freeze violations on the release branch
- Zero hardcoded user-visible strings in any release build
- 100% translation coverage for all supported locales before TVR is issued
- BLEU thresholds respected for all MT segments; no sub-threshold MT accepted without full human review
- TVR delivered to CTO and CTO-L within 5 business days of string freeze
- All automated QA checks (owned by VP Quality) pass before TVR sign-off
