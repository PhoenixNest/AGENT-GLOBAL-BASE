# Localization

Cross-cutting reference for all internationalization (i18n) and localization (L10n) concerns: string extraction, resource file engineering, TMS pipeline operations, and translation management. This topic spans the R&D and Localization departments and is the focus of Stage 9.

---

## Owners

| Role                              | Name                  | Department   | Profile                                                                                                              |
| --------------------------------- | --------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------- |
| Chief Translation Officer (CTO-L) | Dr. Amara Osei-Mensah | Localization | [`profile.md`](company/departments/localization/supervisor/chief-translation-officer/agent/profile.md)               |
| Internationalization Specialist   | Tomas Dvoracek        | R&D          | [`profile.md`](company/departments/research-develop/team/teammates/internationalization-specialist/agent/profile.md) |
| Localization Engineer             | Dario Esposito        | Localization | [`profile.md`](company/departments/localization/team/teammates/localization-engineer/agent/profile.md)               |

---

## Pipeline Stage: Stage 9

Stage 9 activates after the Integrity Verification Sign-off (Stage 8). It has two sequential phases:

### Phase A — i18n Engineering (R&D)

Owned by Internationalization Specialist (Tomas Dvoracek):

1. Scans the integrity-verified codebase for all hardcoded strings
2. Extracts strings into platform-appropriate resource files:
   - Android: `strings.xml`
   - iOS: `Localizable.strings` + `Localizable.stringsdict`
   - Cross-platform: JSON datasets (where applicable)
3. Flags additional datasets requiring localization (e.g., JSON content files)
4. Delivers the **string extraction handoff package** to the CTO-L

### Phase B — Translation (Localization Department)

Owned by CTO-L (Dr. Amara Osei-Mensah):

1. CTO-L takes ownership of all extracted strings and datasets
2. Localization Engineer (Dario Esposito) manages TMS pipeline: string intake, push, pull, validation linting
3. Linguists translate all strings into target languages within the TMS
4. CTO-L issues the **Translation Verification Report** confirming accuracy across all languages

### Structural Completeness Review

CPO, CDO, and CTO conduct a joint structural completeness review:

- All hardcoded strings extracted ✓
- All resource files correctly structured ✓
- No UI component contains untranslated text ✓

> This review covers **structure only** — translation accuracy is the sole responsibility of the CTO-L.

---

## Target Languages

| Language | Code(s)       | Linguist                | Profile                                                                                            |
| -------- | ------------- | ----------------------- | -------------------------------------------------------------------------------------------------- |
| English  | EN-US / EN-GB | Amelia Hartington       | [`profile.md`](company/departments/localization/team/teammates/english-linguist/agent/profile.md)  |
| Chinese  | ZH-CN / ZH-TW | Wei-Chen Liu            | [`profile.md`](company/departments/localization/team/teammates/chinese-linguist/agent/profile.md)  |
| Japanese | JA            | Haruki Yoshimoto        | [`profile.md`](company/departments/localization/team/teammates/japanese-linguist/agent/profile.md) |
| Korean   | KO            | Ji-Hyun Bae             | [`profile.md`](company/departments/localization/team/teammates/korean-linguist/agent/profile.md)   |
| French   | FR-FR / FR-CA | Isabelle Moreau-Leclerc | [`profile.md`](company/departments/localization/team/teammates/french-linguist/agent/profile.md)   |

> Target languages are determined by user specification at project start (PRD Stage 1).

---

## Key Artifacts

- **String extraction handoff package** — Resource files (`strings.xml`, `Localizable.strings`, etc.) with all extracted strings; delivered by R&D to CTO-L
- **Localised codebase** — All hardcoded strings replaced with resource references; all resource files populated for every target language
- **Translation Verification Report** — CTO-L certification of translation accuracy across all target languages; archived at Stage 9 close

---

## Relevant Skills

| Skill File                                                                                                                                                                      | Owner                           | Purpose                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------- |
| [`string-extraction-and-resource-files.md`](company/departments/research-develop/team/teammates/internationalization-specialist/skills/string-extraction-and-resource-files.md) | Internationalization Specialist | String scanning, extraction, and resource file production   |
| [`localization-pipeline-engineering.md`](company/departments/localization/team/teammates/localization-engineer/skills/localization-pipeline-engineering.md)                     | Localization Engineer           | TMS pipeline: string intake, push, pull, validation linting |
| [`language-translation-module.md`](company/departments/localization/supervisor/chief-translation-officer/skills/language-translation-module.md)                                 | CTO-L                           | Governs all translation work and report issuance            |
| [`mobile-ui-translation.md`](company/departments/localization/team/teammates/english-linguist/skills/mobile-ui-translation.md)                                                  | All linguists                   | Mobile UI string translation within the TMS                 |

---

## Gate Criteria (Stage 9)

- [ ] Zero hardcoded strings remain in the codebase
- [ ] All resource files and datasets updated for all target languages
- [ ] CPO, CDO, CTO structural completeness review passed
- [ ] CTO-L Translation Verification Report issued and archived
