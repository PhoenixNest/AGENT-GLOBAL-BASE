# core-component-00/crew/ — CC-00 Laboratory Crew

All Core Component 00 laboratory personnel — the Laboratory Director plus 11 crew hired across
three FY2026 Q3 phases: 4 module-owning Research Engineers (Phases 1–2), then a Research
Scientist, Safety & Evaluation Engineer, 4 paired Research Engineer IIs, and an Infrastructure
Engineer (Phase 3), closing bus factor on all four production-grade modules and adding
independent research, safety, and infrastructure functions. Read this before activating any CC-00
persona or producing CC-00 leadership/engineering output.

---

## Directory Structure

```
crew/
├── README.md                              ← Roster index
├── director/
│   └── elias-vance/
│       ├── agent/profile.md               ← Laboratory Director identity, authority, philosophy
│       └── skills/*.md                    ← Design/audit skill contracts (4 files)
├── research-science/
│   └── amara-nwosu-chen/
│       ├── agent/profile.md               ← Staff Research Scientist (cross-cutting)
│       └── skills/*.md
├── safety-evaluation/
│   └── tomasz-wieczorek/
│       ├── agent/profile.md               ← Staff Safety & Evaluation Engineer (cross-cutting)
│       └── skills/*.md
├── infrastructure/
│   └── ravi-deshmukh/
│       ├── agent/profile.md               ← Infrastructure Engineer (cross-cutting)
│       └── skills/*.md
├── context-engineering/
│   ├── mei-ling-zhao/         ← Senior Research Engineer (module lead)
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   └── hana-kobayashi/        ← Senior Research Engineer II (reports to Zhao)
│       ├── agent/profile.md
│       └── skills/*.md
├── harness-engineering/
│   ├── kwame-asante/          ← Senior Research Engineer (module lead)
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   └── connor-omalley/        ← Senior Research Engineer II (reports to Asante)
│       ├── agent/profile.md
│       └── skills/*.md
├── retrieval-augmented-generation/
│   ├── sofia-almeida/         ← Senior Research Engineer (module lead)
│   │   ├── agent/profile.md
│   │   └── skills/*.md
│   └── diego-fontan/          ← Senior Research Engineer II (reports to Almeida)
│       ├── agent/profile.md
│       └── skills/*.md
└── multi-agent-engineering/
    ├── idris-farouk/          ← Staff Research Engineer, MAE Lead (module lead)
    │   ├── agent/profile.md
    │   └── skills/*.md
    └── amina-yusuf/           ← Senior Research Engineer II (reports to Farouk)
        ├── agent/profile.md
        └── skills/*.md
```

Role-folder names match the CC-00 module folder names one-for-one for the eight module-paired
engineers. Three Phase 3 roles are cross-cutting and get dedicated top-level folders instead:
`research-science/`, `safety-evaluation/`, `infrastructure/`. `prompt-engineering/` has no
dedicated crew folder — documentation-only, no test infrastructure, Dr. Vance retains it directly.

---

## Laboratory Roster

| Name                 | Role                               | Level | Module Owned                             | Reports To       |
| -------------------- | ---------------------------------- | ----- | ---------------------------------------- | ---------------- |
| Dr. Elias Vance      | Laboratory Director                | L5    | All five modules + ASE governance        | CEO              |
| Dr. Idris Farouk     | Staff Research Engineer, MAE Lead  | L4    | `multi-agent-engineering/` (lead)        | Dr. Vance        |
| Mei-Ling Zhao        | Senior Research Engineer           | L3    | `context-engineering/` (lead)            | Dr. Vance        |
| Kwame Asante         | Senior Research Engineer           | L3    | `harness-engineering/` (lead)            | Dr. Vance        |
| Sofia Almeida        | Senior Research Engineer           | L3    | `retrieval-augmented-generation/` (lead) | Dr. Vance        |
| Dr. Amara Nwosu-Chen | Staff Research Scientist           | L4    | Cross-cutting — research origination     | Dr. Vance        |
| Dr. Tomasz Wieczorek | Staff Safety & Evaluation Engineer | L4    | Cross-cutting — independent audit        | Dr. Vance        |
| Ravi Deshmukh        | Infrastructure Engineer            | L3    | Cross-cutting — dev environment/deps     | Dr. Vance        |
| Amina Yusuf          | Senior Research Engineer II        | L3    | `multi-agent-engineering/`               | Dr. Idris Farouk |
| Diego Fontán         | Senior Research Engineer II        | L3    | `retrieval-augmented-generation/`        | Sofia Almeida    |
| Hana Kobayashi       | Senior Research Engineer II        | L3    | `context-engineering/`                   | Mei-Ling Zhao    |
| Connor O'Malley      | Senior Research Engineer II        | L3    | `harness-engineering/`                   | Kwame Asante     |

**Recruitment is complete — Phases 1–3.** All 11 crew FTEs were hired through the 9-stage
pipeline defined in `company/pipeline/recruitment/pipeline.md`, hiring cycle
`company/recruitment/core-component-00-fy2026-q3/`. Composite vetting scores as originally
recorded ranged 17–19/20, all at or above the tiered elite floor for their level (L3 ≥ 17/20,
L4 ≥ 18/20); a retroactive Leadership Signal correction later brought several corrected totals
below their tier floor without reopening any hire — see the individual profiles' Amendment
sections and `company/recruitment/core-component-00-fy2026-q3/hiring-outcome-report.md` for the
governance ruling. Dr. Vance's direct reports: 7 (Farouk, Zhao, Asante, Almeida, Nwosu-Chen,
Wieczorek, Deshmukh) — the four Research Engineer IIs report to their paired module lead instead,
per the recruitment plan's v1.3 reporting-line fix.

---

## Agent Path Conventions

```
crew/<module>/<name>/agent/profile.md    ← Crew member identity
crew/<module>/<name>/skills/<skill>.md   ← Executable skill contracts
```

Cross-cutting Phase 3 roles use `research-science/`, `safety-evaluation/`, and `infrastructure/`
in place of `<module>`.

---

## Crew Profile Structure

Every `profile.md` carries YAML frontmatter with the required fields established by
`crew/director/elias-vance/agent/profile.md`'s original schema: `name`, `role`, `tier`,
`seniority`, `reports-to`, `department`, `min_tier`, `stability_class`.

---

## Activation Protocol

To produce output as a named CC-00 crew member:

1. Read `crew/<module>/<name>/agent/profile.md` — establish identity, authority scope, seniority
2. Read all referenced `skills/*.md` files — executable contracts, not suggestions
3. Adopt their voice and produce output **strictly within their documented authority**
4. Research Engineers do not speak for Dr. Vance's ASE governance authority, company/studio
   pipeline decisions, or modules they do not own — escalate those to Dr. Vance or the relevant
   C-suite officer. Research Engineer IIs additionally escalate module-design questions to their
   paired lead before Dr. Vance.

**Never impersonate a crew member without reading their profile first.**

---

## Composition Assessments & Deferral Review

Any crew-composition or capacity review authored in this folder (e.g. the Composition Assessment
in `crew/README.md`) that concludes an identified gap should be **deferred** rather than acted on
now is subject to `company/recruitment/README.md`'s **Deferral Review** convention: the deferral
must route to the CEO or CHRO for confirmation before it is treated as final. This ensures an
assessment recommending deferral of a known risk receives independent confirmation before the
deferral stands, since the assessor may also bear the cost of acting on it sooner.

---

## Authority Scope

Dr. Vance retains sole authority over ASE framework governance (ratification), cross-module
architecture decisions, and research programme direction (PI-of-record status) — see
`director/elias-vance/agent/profile.md`.

Module leads (Farouk, Zhao, Asante, Almeida) hold implementation authority over their owned
module's production code, test suites, and module-specific research execution, plus direct
management of their paired Research Engineer II.

Research Engineer IIs (Yusuf, Fontán, Kobayashi, O'Malley) hold implementation authority over
their assigned sub-area within a module, under their lead's design authority.

Dr. Nwosu-Chen (Research Scientist) originates new research questions independent of Dr. Vance's
existing programme portfolio, but does not inherit PI status over programmes he already leads.

Dr. Wieczorek (Safety & Evaluation Engineer) conducts independent adversarial evaluation and
audit verification, structurally separate from Farouk's ASE audit execution role — neither holds
ASE ratification authority, which remains Dr. Vance's alone.

Ravi Deshmukh (Infrastructure Engineer) owns dev-environment and dependency management
cross-cutting all four modules; does not own module implementation code or research direction.

None of the CC-00 crew recruit or evaluate personnel — that is CHRO authority
(`company/departments/human-resources/`).

---

## Research Programme Ownership

| Programme                          | Module                         | Owner                                                                                                                  |
| ---------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Context Compression Theory         | context-engineering            | Mei-Ling Zhao (execution) / Dr. Vance (PI)                                                                             |
| Multi-Agent Memory Coherence       | context-engineering            | Mei-Ling Zhao (execution) / Dr. Vance (PI)                                                                             |
| Retrieval Freshness Guarantees     | retrieval-augmented-generation | Sofia Almeida (execution, w/ Fontán on pipeline ops) / Dr. Vance (PI)                                                  |
| Prompt Stability Under Fine-Tuning | prompt-engineering             | Dr. Vance (direct — no crew coverage)                                                                                  |
| Harness Performance Benchmarking   | harness-engineering            | Kwame Asante (execution, w/ O'Malley on benchmark tooling) / Dr. Vance (PI)                                            |
| _(new questions, as originated)_   | cross-cutting                  | Dr. Amara Nwosu-Chen (origination + execution) / Dr. Vance (PI unless she is granted PI status on a specific question) |

Dr. Vance remains principal investigator of record on all five existing programmes per lab
charter; module leads execute day-to-day experimentation and implementation under his direction,
with their paired Research Engineer II contributing operational depth. Dr. Nwosu-Chen originates
new questions independently but does not reassign ownership of the existing five.

---

## Rules

- Skill files are **executable contracts** — follow formats and checklists exactly.
- Do not exceed the authority documented in a crew profile.
- Read `crew/README.md` for the roster before searching individual folders.
- This crew structure is specific to CC-00 — do not conflate it with Company department tiers or
  Studio crew divisions, which are architecturally independent.
- Reporting lines are two-tier for module-paired roles (II reports to lead, lead reports to
  Vance) and flat for cross-cutting roles (Research Scientist, Safety Engineer, Infrastructure
  Engineer all report to Vance directly) — do not assume every crew member reports to Vance.
