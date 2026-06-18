# company/ — The Company

Entry point for The Company system. Read this before doing any company-related work.

---

## What This Is

The Company is a mobile product company — a fully staffed organizational simulation with C-suite
agents, department teams, development pipelines, and a recruitment process. All artifacts here are
Markdown documents: agent profiles, skill files, pipeline definitions, and knowledge resources.

There is no application code under `company/`. Runnable code lives exclusively in
`core-component-00/`.

---

## Where to Start

| I need…                                | Go to                           |
| -------------------------------------- | ------------------------------- |
| Company overview, org chart, personnel | `library/overview/company.md`   |
| All pipeline stages + stage ownership  | `library/overview/pipeline.md`  |
| Full personnel roster                  | `library/overview/personnel.md` |
| A department's agents and skills       | `departments/<dept>/`           |
| The active development pipeline        | `pipeline/<pipeline-type>/`     |
| Hiring plans and recruitment           | `recruitment/`                  |
| Past optimization records              | `optimization-history/`         |

**Start with `library/README.md`** — it is the central knowledge hub index for the entire company.

---

## Directory Structure

```
company/
├── library/               ← Central knowledge hub (START HERE)
│   ├── overview/          ← company.md · pipeline.md · personnel.md
│   ├── departments/       ← One summary .md per department
│   ├── topics/            ← architecture · localization · monitoring · security · testing
│   └── reference/         ← External link collections
├── departments/           ← Agent profiles + skill files (canonical source of agent identity)
│   ├── brand-design/
│   ├── cyberspace-security/
│   ├── human-resources/
│   ├── legal/
│   ├── localization/
│   ├── product-management/
│   └── research-develop/
├── pipeline/              ← Full pipeline definitions
│   ├── _base/             ← Shared 10-stage skeleton + templates
│   ├── mobile-development/
│   ├── web-development/
│   ├── backend-api/
│   ├── full-stack/
│   └── recruitment/       ← Standalone 9-stage process
├── recruitment/           ← Active hiring cycles + templates
├── optimization-history/  ← Append-only archive
└── project/               ← Active project dashboard
```

---

## The 13-Stage Development Pipeline

| #   | Stage                                            | User Approval? |
| --- | ------------------------------------------------ | -------------- |
| 0   | Problem Validation                               | ❌             |
| 1   | Requirements → PRD + SRD                         | ✅             |
| 2   | PRD → Web Prototype + IDS                        | ✅             |
| 3   | Prototype → UML Engineering Package              | ✅             |
| 4   | UML → Implementation Plan + Gantt                | ✅             |
| 5   | Plan → Software Development                      | ❌             |
| 6   | Development → Arch. & Conformance Review         | ✅             |
| 7   | Arch. Review → Automated Testing                 | ✅             |
| 8   | Testing → Integrity Verification                 | ❌             |
| 9   | Integrity Verification → Translation Production  | ❌             |
| 9.5 | Internal Dogfood                                 | ❌             |
| 10  | Translation Production → Release Readiness Check | ✅             |
| 11  | Live Operations (continuous)                     | ⚠️ QBR         |

**Stages marked ✅ are hard stops** — present the deliverable and wait for user sign-off.

---

## Departments & C-Suite Owners

| Department             | Supervisor                                   | Key Pipeline Stages  |
| ---------------------- | -------------------------------------------- | -------------------- |
| Brand Design           | CDO — Yuki Tanaka-Chen                       | 2, 6, 8, 10          |
| Cyberspace Security    | CIO — Dr. Priya Mehta · CSO — Dr. Sarah Chen | 3, 6, 8, 10          |
| Human Resources        | CHRO — Dr. Evelyn Hartwell                   | Recruitment pipeline |
| Legal                  | CLO — Dr. Victoria Svensson-Park             | 1, 3, 6, 8, 10       |
| Localization           | CTO-L — Dr. Amara Osei-Mensah                | 9, 10                |
| Product Management     | CPO — Marcus Tran-Yoshida                    | 0, 1, 6, 8, 10       |
| Research & Development | CTO — Dr. Kenji Nakamura                     | 3, 4, 5, 6, 7, 8, 10 |

---

## Personnel Tier System

| Tier             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| C-suite          | Placed before recruitment; own pipeline stage outputs |
| Team Supervisors | Recruited after C-suite; own sub-department execution |
| Teammates        | Individual contributors                               |

---

## Non-Negotiable Rules

- **Stage 3 locks the tech stack.** ADRs and TSD are immutable after user approval. Any change
  requires a new ADR and full Stage 3 re-entry.
- **P0/P1 defects block release.** These classifications cannot be overridden by any agent.
- **Trim-to-Pass is a P0 defect.** Removing features or security to pass Stage 6/8 is forbidden.
- **PRD + SRD travel as a pair** from Stage 1 onward.
- **Stage 4+ projects require** `progress.md`, `session-log.md`, and `checkpoint.json`.
- **optimization-history/ is append-only.** Never edit or delete past entries.

---

## Agent Activation Protocol

To produce output as a named company agent:

1. Read `departments/<dept>/<tier>/<role>/agent/profile.md`
2. Read all referenced `skills/*.md` files
3. Adopt their voice and authority scope
4. Conform the artifact to the stage spec in `pipeline/<type>/pipeline.md`

Never impersonate an agent without reading their profile first.

---

## Document Authority (when sources conflict)

1. `pipeline.md` inside a pipeline folder — canonical truth
2. `agent/profile.md` — canonical agent identity
3. `library/overview/*.md` — authoritative summaries
4. `library/departments/*.md` — may lag canonical source
