# Localization Department

Responsible for all translation and internationalization pipeline operations. The department is activated mid-way through Stage 9, after the R&D Department delivers the string extraction handoff package. It governs all translation work through the Language Translation Module and issues the Translation Verification Report upon completion.

> Reports to the Chief Translation Officer (CTO-L).

---

## Supervisor

| Name | Role | Seniority | Profile |
| --- | --- | --- | --- |
| Dr. Amara Osei-Mensah | Chief Translation Officer (CTO-L) | C-suite | [`profile.md`](../../departments/localization/supervisor/chief-translation-officer/agent/profile.md) |

**CTO-L Skills:**

| Skill File | Purpose |
| --- | --- |
| [`language-translation-module.md`](../../departments/localization/supervisor/chief-translation-officer/skills/language-translation-module.md) | Governs all translation work: TMS intake, quality standards, translation verification, report issuance |

---

## Team

### Linguists

| Name | Role | Language Pairs | Profile |
| --- | --- | --- | --- |
| Amelia Hartington | English Linguist | EN-US / EN-GB | [`profile.md`](../../departments/localization/team/teammates/english-linguist/agent/profile.md) |
| Wei-Chen Liu | Chinese Linguist | ZH-CN / ZH-TW | [`profile.md`](../../departments/localization/team/teammates/chinese-linguist/agent/profile.md) |
| Haruki Yoshimoto | Japanese Linguist | JA | [`profile.md`](../../departments/localization/team/teammates/japanese-linguist/agent/profile.md) |
| Ji-Hyun Bae | Korean Linguist | KO | [`profile.md`](../../departments/localization/team/teammates/korean-linguist/agent/profile.md) |
| Isabelle Moreau-Leclerc | French Linguist | FR-FR / FR-CA | [`profile.md`](../../departments/localization/team/teammates/french-linguist/agent/profile.md) |

All linguists share the same skill: [`mobile-ui-translation.md`](../../departments/localization/team/teammates/english-linguist/skills/mobile-ui-translation.md) — mobile UI string translation within the TMS.

### Localization Engineer

| Name | Role | Profile |
| --- | --- | --- |
| Dario Esposito | Localization Engineer | [`profile.md`](../../departments/localization/team/teammates/localization-engineer/agent/profile.md) |

| Skill File | Purpose |
| --- | --- |
| [`localization-pipeline-engineering.md`](../../departments/localization/team/teammates/localization-engineer/skills/localization-pipeline-engineering.md) | TMS pipeline: string intake, push, pull, validation linting |

---

## Pipeline Stages

| Stage | Role |
| --- | --- |
| **Stage 9** — Integrity Verification → i18n Engineering | **Responsible Producer.** CTO-L takes ownership of all extracted strings and datasets from R&D, manages TMS pipeline (Localization Engineer), directs linguists to translate into all target languages. Issues the Translation Verification Report confirming accuracy across all target languages. |
| **Stage 10** — Release Readiness Check | **Sign-off authority.** CTO-L certifies: all target languages complete and verified. |

---

## Division of Responsibility in Stage 9

| Responsibility | Owner |
| --- | --- |
| String extraction and resource file creation | R&D / Internationalization Specialist (Tomas Dvoracek) |
| TMS pipeline operations (intake, push, pull, linting) | Localization Engineer (Dario Esposito) |
| Translation accuracy | Linguist Team |
| Structural completeness review (strings extracted, files structured, no untranslated UI) | CPO, CDO, CTO (joint review — structure only, not accuracy) |
| Translation Verification Report | CTO-L |

---

## Key Artifacts Produced

- **Localised codebase** — All hardcoded strings replaced with resource file references; all resource files populated for every target language.
- **Translation Verification Report** — CTO-L certification of translation accuracy across all target languages.

For cross-cutting localization guidance, see [`topics/localization.md`](../topics/localization.md).
