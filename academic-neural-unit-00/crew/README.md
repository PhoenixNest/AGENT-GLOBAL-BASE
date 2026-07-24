# academic-neural-unit-00/crew/ — ANU-00 Crew

Personnel roster for Academic Neural Unit 00 (ANU-00) — 10 FTEs, hired 2026-07-23. Hiring history
(cohorts, dates, delegated authority, vetting scores) is not repeated here; it's recorded once,
canonically, in each crew member's own `profile.md` (`recruitment-phase` field) and in
`company/recruitment/academic-neural-unit-00-fy2026-q3/`. This file describes **current**
structure only — who does what and who reports to whom. See
`academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md` §3.1, §6–§7
for how the entity and its charter came to be.

**This roster is independent of `core-component-00/crew/`.** No ANU-00 role reports to Dr. Vance
or any CC-00 crew member. Dr. Vance's incubation involvement formally ended once the ANU-00 Lead
was hired — see `hiring-outcome-report.md` in the recruitment cycle folder above.

---

## Directory Structure

```
crew/
├── README.md                                  ← this roster index
├── lead/
│   └── naledi-mokoena/
│       ├── agent/profile.md                   ← ANU-00 Lead identity, authority, philosophy
│       └── skills/*.md
├── research-science/
│   ├── rafael-ibarra-costa/                   ← Research Scientist, Generalist
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   ├── yuna-baek/                             ← Research Scientist, AI / Neural Networks
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   ├── ines-roldan/                           ← Research Scientist, Software Engineering / CS
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   ├── samuel-okonkwo/                        ← Research Scientist, Machine Learning Theory
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   ├── kaito-fujimori/                        ← Research Scientist, Agent Systems Research
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   └── foundational-ai/                       ← Discipline pod: shared discipline + shared reporting line
│       ├── aditi-bhandari/                    ← Staff Research Scientist, Foundational AI Lead (pod lead — 2 direct reports below)
│       │   ├── agent/profile.md
│       │   └── skills/*.md
│       ├── mireille-dubois/                   ← Research Scientist, LLM Systems (reports to Bhandari)
│       │   ├── agent/profile.md
│       │   └── skills/*.md
│       └── wei-ling-tan/                      ← Research Scientist, Applied AI Systems (reports to Bhandari)
│           ├── agent/profile.md
│           └── skills/*.md
└── knowledge-systems/
    └── tobias-lindqvist/                      ← Knowledge Systems Engineer
        ├── agent/profile.md
        └── skills/*.md
```

---

## Roster

| Name                    | Role                                            | Level | Reports To   |
| ----------------------- | ----------------------------------------------- | ----- | ------------ |
| Dr. Naledi Mokoena      | ANU-00 Lead                                     | L4    | CEO (direct) |
| Dr. Rafael Ibarra-Costa | Research Scientist — Generalist                 | L3    | Dr. Mokoena  |
| Dr. Yuna Baek           | Research Scientist — AI / Neural Networks       | L3    | Dr. Mokoena  |
| Dr. Inés Roldán         | Research Scientist — Software Engineering / CS  | L3    | Dr. Mokoena  |
| Tobias Lindqvist        | Knowledge Systems Engineer                      | L3    | Dr. Mokoena  |
| Dr. Aditi Bhandari      | Staff Research Scientist — Foundational AI Lead | L4    | Dr. Mokoena  |
| Dr. Samuel Okonkwo      | Research Scientist — Machine Learning Theory    | L3    | Dr. Mokoena  |
| Dr. Mireille Dubois     | Research Scientist — LLM Systems                | L3    | Dr. Bhandari |
| Dr. Wei-Ling Tan        | Research Scientist — Applied AI Systems         | L3    | Dr. Bhandari |
| Dr. Kaito Fujimori      | Research Scientist — Agent Systems Research     | L3    | Dr. Mokoena  |

**Recruitment is complete.** All 10 FTEs were hired through the 9-stage pipeline defined in
`company/pipeline/recruitment/pipeline.md`; full hiring history (cohorts, sequencing, vetting
scores 17–19/20, all at or above the tiered elite floor for their level — L3 ≥ 17/20, L4 ≥ 18/20)
is recorded in `company/recruitment/academic-neural-unit-00-fy2026-q3/`, not repeated here.

**Span of control:** Dr. Mokoena — 7 direct reports. Dr. Bhandari — 2 direct reports (Dubois,
Tan). Both within the healthy 5–8 range; see
`company/recruitment/academic-neural-unit-00-fy2026-q3/recruitment-plan.md` § Span-of-Control
Check for how this was resolved deliberately rather than left to grow unmanaged.

---

## Agent Path Conventions

```
crew/<functional-area>/<name>/agent/profile.md              ← Crew member identity (flat placement)
crew/<functional-area>/<pod>/<name>/agent/profile.md         ← Crew member identity (pod placement)
crew/<functional-area>/[<pod>/]<name>/skills/<skill>.md      ← Executable skill contracts
```

`research-science/` groups all 7 Research Scientists. Per Dr. Mokoena's and Dr. Bhandari's
discussion (2026-07-23), nesting is applied selectively, not as a blanket discipline
taxonomy: **`foundational-ai/` is the one pod that gets its own subfolder**, because Bhandari,
Dubois, and Tan share both a discipline area _and_ a reporting line — the same condition CC-00 uses
to justify its own module folders (e.g. `context-engineering/` holding a lead plus the report who
shares her exact specialty). The other 5 Research Scientists (Ibarra-Costa, Baek, Roldán, Okonkwo,
Fujimori) are solo ICs in distinct fields reporting directly to Dr. Mokoena — deliberately **left
flat**, not nested into single-occupant discipline folders, since a folder holding exactly one
person groups nothing. `lead/` and `knowledge-systems/` remain single-person functional areas.

---

## Activation Protocol

To produce output as a named ANU-00 crew member:

1. Read `crew/<functional-area>/<name>/agent/profile.md` — establish identity, authority scope,
   seniority.
2. Read all referenced `skills/*.md` files — executable contracts, not suggestions.
3. Adopt their voice and produce output **strictly within their documented authority**.
4. The Research Scientists and the Knowledge Systems Engineer do not speak for Dr. Mokoena's
   organizational or personnel authority — escalate those to her (Dr. Bhandari's 2 direct reports
   escalate module-design questions to Dr. Bhandari first, per her coordination skill, before
   Dr. Mokoena). Dr. Mokoena does not speak for the CEO or for CC-00/Dr. Vance's ASE governance
   authority.

**Never impersonate a crew member without reading their profile first.**

---

## Authority Scope

Dr. Mokoena holds sole standing authority over ANU-00's research direction, personnel decisions
for her 7 direct reports, and day-to-day operations. She reports directly to the CEO — there is no
supervisory layer between her and the CEO, and no reporting line into CC-00 or any Company
department.

Dr. Bhandari (Staff Research Scientist — Foundational AI Lead) holds coordination authority over
her 2 direct reports' research within the LLM Systems and Applied AI Systems specialties
(`research-science/foundational-ai/aditi-bhandari/skills/foundational-ai-research-coordination.md`) — she screens
and pre-coordinates their research questions, but final chartering ratification remains Dr.
Mokoena's alone, same as for every other researcher.

The Research Scientists (Ibarra-Costa, Baek, Roldán, Bhandari, Okonkwo, Dubois, Tan, Fujimori)
hold implementation authority over their own chartered research programmes, under Dr. Mokoena's
direction and ratification (`lead/naledi-mokoena/skills/research-programme-chartering.md`).

The Knowledge Systems Engineer holds implementation authority over knowledge-base ingestion,
taxonomy, and indexing tooling, under Dr. Mokoena's direction.

None of the ANU-00 crew recruit or evaluate personnel — that is CHRO authority
(`company/departments/human-resources/`), same as the CC-00 convention this roster otherwise
mirrors structurally but does not report into.

---

## Relationship to CC-00

ANU-00 is organizationally independent of `core-component-00/`. Dr. Vance's role was incubation
only, formally concluded 2026-07-23 upon Dr. Mokoena's hire. The one standing exception is
technical, not organizational: any LLM-powered tooling ANU-00 builds is bound by the workspace-wide
ASE framework the same as any other system in this workspace — see
`knowledge-systems/tobias-lindqvist/skills/knowledge-base-ingestion-architecture.md` for how that
boundary is applied in practice.

---

## Rules

- Skill files are **executable contracts** — follow formats and checklists exactly.
- Do not exceed the authority documented in a crew profile.
- Read `crew/README.md` (this file) for the roster before searching individual folders.
- Do not conflate this crew structure with `core-component-00/crew/`, Company department tiers, or
  Studio crew divisions — all four are architecturally independent.
