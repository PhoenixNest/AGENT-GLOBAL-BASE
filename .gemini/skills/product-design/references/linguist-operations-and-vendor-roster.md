---
name: linguist-operations-and-vendor-roster
description: Linguist operations and vendor management for the localization department — LSP (Language Service Provider) selection and governance, translator briefing and style guide delivery, linguistic QA coordinator assignments, and the internal linguist bench structure. Use when onboarding a new language, evaluating LSP performance, resolving a translation quality dispute, or briefing translators on a new game product.
version: "1.0.0"
---

# Linguist Operations and Vendor Roster

## Purpose

Manage the people side of localization: the human translators, post-editors, and linguistic QA reviewers who turn source strings into quality target-language text. Dr. Amara Osei-Mensah is not just a pipeline engineer — she is responsible for selecting, briefing, and maintaining relationships with the language professionals who execute the work. A technically perfect CI/CD localization pipeline with poorly briefed translators will still produce bad translations.

## Vendor Roster Structure

The company works with a tiered roster of Language Service Providers (LSPs) and freelance linguists:

| Tier                             | Type                                  | Languages                    | Use Case                                                | Selection Criteria                                                                             |
| -------------------------------- | ------------------------------------- | ---------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Tier 1 — Preferred LSP**       | Agency with PM + translator + LQA     | FR, DE, JA, KO, ZH-TW, PT-BR | All production releases; highest quality bar            | BLEU ≥45, <1 critical LQA finding per 1000 words, 3+ year relationship, mobile game experience |
| **Tier 2 — Certified Freelance** | Individual post-editor or translator  | All languages                | MT post-editing; overflow capacity                      | Tested in-house; native speaker; proven game localization experience                           |
| **Tier 3 — Evaluated Freelance** | Individual                            | New/emerging languages       | Pilot languages; lower-priority markets                 | Sample test completed; not yet proven in production                                            |
| **MT-only**                      | Machine translation (no human review) | Low-priority languages       | Internal testing, soft launch pilot in non-core markets | Not used for production global releases                                                        |

### Tier 1 LSP Governance

For each Tier 1 LSP, Dr. Osei-Mensah maintains a **Vendor Record** in Confluence:

```markdown
# Vendor Record — [LSP Name]

Languages: [list]
Contract type: [frame agreement / project-based]
Contact: [PM name + email]
SLA: [turnaround time per word count]

Quality history (trailing 12 months):

- Projects delivered: [N]
- On-time rate: [%]
- LQA finding rate (critical): [per 1000 words]
- BLEU average: [score]

Status: Active / Under review / Deactivated
Last review date: [YYYY-MM-DD]
```

### Annual LSP Review

Every January, Dr. Osei-Mensah reviews each Tier 1 LSP against their trailing 12-month quality data. Vendors falling below tier thresholds are downgraded to Tier 2 and replaced. This review is documented and accessible to the CTO and CPO on request.

## Translator Briefing Protocol

No translator — agency or freelance — begins work on a new project without a **Translator Brief**. Briefs that are missing or incomplete are the single largest driver of avoidable translation quality failures.

### Translator Brief Template

```markdown
# Translator Brief — [Game/Product Name]

**Date:** YYYY-MM-DD
**Issued by:** Dr. Amara Osei-Mensah, CTO-L
**Target languages:** [list]
**Project type:** [Game localization / Marketing copy / Store metadata / UI strings]

## Product Overview (2 paragraphs)

[What is the product? Who is the player/user? What is the tone?]

## Audience Profile

- Age: [range]
- Gaming experience: [casual / midcore / hardcore]
- Regional context: [any cultural notes per language]

## Tone-of-Voice Guidelines

[Key adjectives: e.g., "Warm, Direct, Playful — never formal, never condescending"]
[Link to full Studio Style Guide if applicable]

## Controlled Vocabulary (Glossary)

[Link to the project glossary in the TMS — all glossary terms are mandatory; do not translate with synonyms]

Key terms:
| Source (EN) | [FR] | [DE] | [JA] | Notes |
| --- | --- | --- | --- | --- |
| Coins | Pièces | Münzen | コイン | Always use — not "monnaie" or "Geld" |
| Lives | Vies | Leben | ライフ | |
| Level | Niveau | Level | レベル | Keep "Level" in German (no translation) |

## Format Rules

- Placeholder format: `{variable_name}` — do not translate placeholders
- Max character limits: [link to expansion budget table]
- Date/number format: [YYYY-MM-DD / locale-specific]
- Do not add or remove punctuation from source

## What to Escalate (Do Not Decide Alone)

- Any string with cultural sensitivity concerns
- Any string where the source text appears ambiguous or incorrect
- Any controlled vocabulary term that is grammatically incompatible in the target language
- Any string that would require different translations for male/female grammatical gender
```

### Brief Delivery Timeline

| Event              | Action                                                       | Timing                     |
| ------------------ | ------------------------------------------------------------ | -------------------------- |
| New project starts | Translator Brief written and delivered to all active vendors | Before string export       |
| Glossary updated   | Notify all active vendors of changes                         | Within 24 hours of update  |
| New language added | Full brief + language-specific cultural notes                | Before first string export |

## Linguistic QA (LQA) Process

After translation and MT post-editing, every production release goes through an LQA review. Dr. Osei-Mensah assigns a separate linguist (not the original translator) as the LQA reviewer.

### LQA Severity Classification

| Severity       | Definition                                              | Example                                                           | Impact                          |
| -------------- | ------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------- |
| **Critical**   | Meaning error, offensive content, placeholder broken    | Wrong pronoun changes meaning; profanity                          | Block — reopen translation      |
| **Major**      | Terminology violation, grammar error visible to players | Wrong controlled vocabulary term; subject-verb disagreement in UI | Fix before TVR sign-off         |
| **Minor**      | Style inconsistency, punctuation deviation              | Comma placement inconsistent with style guide                     | Fix in next localization sprint |
| **Suggestion** | Better phrasing available                               | More natural colloquial option                                    | Translator's discretion         |

### LQA Acceptance Thresholds

| Quality Level    | Critical | Major               | Release Decision                                     |
| ---------------- | -------- | ------------------- | ---------------------------------------------------- |
| Pass             | 0        | ≤2 per 1,000 words  | Proceed to TVR                                       |
| Conditional pass | 0        | 3–5 per 1,000 words | Fix majors; re-review affected strings before TVR    |
| Fail             | ≥1       | Any                 | Full re-translation of affected segments; LQA repeat |

## Language Expansion Process

When the company adds a new supported language:

1. **Tier assignment:** Dr. Osei-Mensah evaluates available LSPs and freelancers for the language; runs a sample test (250 strings from an existing product); scores against the BLEU and LQA criteria
2. **Brief creation:** Writes the language-specific addition to the Translator Brief (cultural notes, register, any known localization challenges)
3. **Pilot:** First release in the new language uses Tier 2 (certified freelance) with full LQA; escalates to Tier 1 if LSP is available and passes the test
4. **Glossary seeding:** Translates the base glossary into the new language before string export

## Quality Standards

- Every production release has a Translator Brief on file before any translation work begins
- LQA assigned to a reviewer different from the translator — no self-review
- Annual LSP review completed every January; all records updated
- Zero Critical LQA findings at TVR sign-off
- Language expansion pilot always completed before a new language is included in a production global release
