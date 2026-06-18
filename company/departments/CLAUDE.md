# company/departments/ — Agent Profiles & Skills

Canonical source of identity for all company organizational agents (Type A personas). Read this
before activating or creating any company agent.

---

## What Lives Here

Each department folder contains the agent profiles and skill files that define a company agent's
identity, authority scope, and operational behaviour. These are **executable contracts** — not
suggestions. When a skill file specifies a format or checklist, follow it exactly.

---

## Departments

| Folder                 | Department             | Supervisor                                   |
| ---------------------- | ---------------------- | -------------------------------------------- |
| `brand-design/`        | Brand Design           | CDO — Yuki Tanaka-Chen                       |
| `cyberspace-security/` | Cyberspace Security    | CIO — Dr. Priya Mehta · CSO — Dr. Sarah Chen |
| `human-resources/`     | Human Resources        | CHRO — Dr. Evelyn Hartwell                   |
| `legal/`               | Legal                  | CLO — Dr. Victoria Svensson-Park             |
| `localization/`        | Localization           | CTO-L — Dr. Amara Osei-Mensah                |
| `product-management/`  | Product Management     | CPO — Marcus Tran-Yoshida                    |
| `research-develop/`    | Research & Development | CTO — Dr. Kenji Nakamura                     |

---

## Path Conventions

```
departments/<dept>/supervisor/<role>/agent/profile.md         ← C-suite
departments/<dept>/supervisor/<role>/skills/<skill>.md

departments/<dept>/team/supervisors/<role>/agent/profile.md   ← Team supervisors
departments/<dept>/team/supervisors/<role>/skills/<skill>.md

departments/<dept>/team/teammates/<role>/agent/profile.md     ← Teammates
departments/<dept>/team/teammates/<role>/skills/<skill>.md
```

---

## Profile Structure

Every `profile.md` carries YAML frontmatter with six required fields:

```yaml
role: <job title>
tier: <c-suite | supervisor | teammate>
seniority: <level>
department: <department name>
agent_id: <unique ID>
hire_date: <YYYY-MM-DD>
```

Missing any of these fields is a structural defect.

---

## Activation Protocol

When the user requests output from a named agent:

1. Read `agent/profile.md` — establish identity, authority, and pipeline stage ownership
2. Read every skill file listed in the profile — these are executable contracts
3. Adopt the agent's voice and perspective
4. Produce output **strictly within their documented authority**
5. Conform the artifact to the stage spec in the relevant `pipeline.md`

**Never impersonate an agent without reading their profile first.**

---

## Personnel Tiers

| Tier             | Placement                                    | Authority                                          |
| ---------------- | -------------------------------------------- | -------------------------------------------------- |
| C-suite          | Pre-recruitment (placed by founding charter) | Own pipeline stage outputs                         |
| Team Supervisors | Recruited after C-suite confirmation         | Own sub-department execution                       |
| Teammates        | Individual contributors                      | Produce stage artifacts under supervisor direction |

---

## Rules

- Skills files are **executable contracts** — follow formats and checklists exactly.
- Do not exceed the authority documented in a profile — state conflicts explicitly.
- Do not create agent profiles without the six required frontmatter fields.
- Department summary files in `company/library/departments/` may lag the canonical profiles here —
  when they conflict, the profile in this folder wins.
