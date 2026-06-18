# company/library/ — Company Knowledge Hub

Central knowledge repository for The Company. This is the **START HERE** location for any
company-related research, orientation, or cross-department navigation.

---

## What Lives Here

This folder contains curated, human-readable summaries and reference documents. Note that some
documents here — particularly in `departments/` — may lag behind the canonical sources in
`company/departments/`. When sources conflict, canonical sources win (see authority hierarchy below).

---

## Directory Structure

```
library/
├── README.md              ← Master index — start here
├── overview/
│   ├── company.md         ← Org chart, departments, tier system, authority hierarchy
│   ├── pipeline.md        ← 13-stage development pipeline summary + stage ownership
│   └── personnel.md       ← Full personnel roster with roles and pipeline stage ownership
├── departments/           ← One summary .md per department (may lag canonical profiles)
├── topics/
│   ├── architecture.md    ← ADR conventions, UML standards, tech selection
│   ├── localization.md    ← i18n pipeline, TMS, translation workflow
│   ├── monitoring.md      ← Progress monitoring, session recovery, Stage 4+ tracking
│   ├── security.md        ← OWASP MASVS, security architecture, threat modelling
│   └── testing.md         ← Defect severity system, test pyramid, QA pipeline
└── reference/             ← External link collections (design, development)
```

---

## Navigation Guide

| I need…                                  | Go to                    |
| ---------------------------------------- | ------------------------ |
| Company overview and org structure       | `overview/company.md`    |
| Full 13-stage pipeline with stage owners | `overview/pipeline.md`   |
| Who is responsible for which stage       | `overview/personnel.md`  |
| A specific department's summary          | `departments/<dept>.md`  |
| Architecture and ADR conventions         | `topics/architecture.md` |
| i18n / localization pipeline             | `topics/localization.md` |
| Progress monitoring (Stage 4+ projects)  | `topics/monitoring.md`   |
| Security standards and threat modelling  | `topics/security.md`     |
| Testing standards and defect severity    | `topics/testing.md`      |

---

## Document Authority Hierarchy

When sources in this library conflict with sources elsewhere, apply this precedence:

1. `company/pipeline/<type>/pipeline.md` — canonical truth for that pipeline
2. `company/departments/<dept>/<tier>/<role>/agent/profile.md` — canonical agent identity
3. `library/overview/*.md` — authoritative summaries (here)
4. `library/departments/*.md` — readable summaries (may lag — lowest authority)

**Never treat a `library/departments/` summary as equal to a canonical profile.** If they differ,
the profile wins and the summary should be noted as stale.

---

## Rules

- Read `library/README.md` first for any company knowledge task — it provides the master index.
- Do not modify `library/departments/` summaries to reflect changes made in `company/departments/`
  without verifying the canonical profile first.
- Topic files in `library/topics/` are authoritative for cross-cutting concerns (architecture,
  security, testing, localization, monitoring) across all company pipelines.
