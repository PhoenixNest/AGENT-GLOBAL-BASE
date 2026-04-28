---
name: hr-recruiting-guidelines-recruit-translation
description: "Recruits translation and localization roles — Translator, Senior Translator, Localization Engineer, Localization Manager, Head of Localization, CTO-L — using seniority rubrics covering scope of impact, technical depth in CAT tools and TM systems, leadership, and certified language pair declarations, with interview simulation protocols and elite vetting gate. Owned by Dr. Evelyn Hartwell (CHRO). Use when recruiting for translators, localization engineers, localization managers, or chief translation officer roles. Trigger: recruit translator, hire localization engineer, localization recruitment, translation recruitment, CTO-L, linguist recruitment, hire CAT specialist."
prerequisites:
  - hr-recruiting-overview

version: "1.0.0"
---

# Translation & Localization Recruitment Skill

## Roles Covered

Translator (Junior/Mid), Senior Translator, Localization Engineer,
Localization Manager, Head of Localization, Chief Translation Officer (CTO-L).

## Seniority Rubric

Score the candidate against each criterion. Use this to assign seniority level.

| Criterion       | Translator                      | Senior Translator                | Localization Engineer               | Localization Manager   | Head of Localization             | CTO-L (Chief Translation Officer)         |
| --------------- | ------------------------------- | -------------------------------- | ----------------------------------- | ---------------------- | -------------------------------- | ----------------------------------------- |
| Scope of impact | Single language pair            | Multiple language pairs          | Platform/tooling                    | Team delivery          | Multi-team / multi-language      | Company-wide                              |
| Technical depth | Source → target translation     | Style guide authorship           | TM/CAT tooling, string engineering  | Pipeline design        | Localization strategy            | Technology vision + linguistic governance |
| Leadership      | Self                            | Mentors 1–2                      | Cross-functional contributor        | Manages 3–6 linguists  | Manages 10–30                    | C-suite exec                              |
| Track record    | 1+ shipped translation projects | 2+ projects with quality metrics | Platform-level localization tooling | Team health + delivery | Org scaling + language expansion | Company-wide localization outcomes        |

## Interview Simulation Protocol

When recruiting a translation/localization role, the CHRO must generate a candidate profile covering:

1. **Identity block**
   - Full name (realistic, diverse)
   - Current title and company
   - Years of experience
   - Education (Linguistics, Translation Studies, Computational Linguistics — required; adjacent fields such as Computer Science or Modern Languages accepted if accompanied by professional translation certification from ATA, ITI, or equivalent accreditation body)
   - Native language(s) and professional language pairs

2. **Track record** (3 bullet points, each with a specific outcome)
   - Format: "[Action verb] [what] at [company], resulting in [quantified outcome]"
   - Example: "Reduced post-release translation bug rate by 71% at Microsoft by introducing automated linguistic QA tooling integrated into the CI/CD pipeline"

3. **Technical strengths** (2–3, each with a concrete example)
   - Must reference specific CAT tools (SDL Trados, memoQ, Phrase/Memsource), MT engines (DeepL, Google Neural MT), or platform-specific localization conventions (iOS Localizable.strings, Android strings.xml, stringsdict pluralisation)

4. **Honest gaps** (1–2)
   - Be direct. Example: "Has not managed a localization team larger than 4 linguists. Scaling to 15+ would be an open question."

5. **Language pair declaration**
   - List all certified language pairs with evidence of professional certification (ATA, ITI, JLPT, TOPIK, HSK, CEFR level)

6. **Seniority score** — apply the rubric table above, assign a level

7. **Vetting result** — apply `vet-candidate.md` and paste the full scoring output

8. **Placement recommendation**
   - Recommended tier: `company/departments/localization/supervisors/` or `company/departments/localization/teammates/`
   - Recommended directory name (kebab-case)
   - Rationale (2 sentences)

## Output Contract

After user confirms placement:

1. Create `company/departments/localization/[tier]/[role-name]/agent/profile.md` — where `[tier]` is either `supervisors` or `teammates` based on seniority (see CHRO Seniority → Tier Mapping table) — using the Recruited Agent Profile Template from the CHRO profile
2. Create at least one `company/departments/localization/[tier]/[role-name]/skills/[skill-name].md` covering their primary translation capability
3. Confirm to the user: "Recruited and placed: [Name], [Title] → company/departments/localization/[tier]/[role-name]/"
