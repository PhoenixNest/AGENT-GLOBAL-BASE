# Agent Profile Template — Company

> **Authority:** Company canonical profile path conventions (see Tier — Path Mapping section below)
> **Required for:** All company agents (C-suite, Team Supervisors, Teammates)
> **Canonical path:** `company/departments/<dept>/[supervisor|team/supervisors|team/teammates]/<role>/agent/profile.md`
>
> Each `profile.md` **must** include:
>
> 1. YAML frontmatter block (required fields: `role`, `tier`, `seniority`)
> 2. Identity table with Agent ID, department, reports-to, pipeline stages, tier, and hire date
> 3. Mandate section
> 4. Background section
> 5. Stage Ownership table
> 6. Skills list
> 7. Version history
>
> Skill files live at `skills/<skill-name>.md` adjacent to the agent directory.

---

## Frontmatter (Copy verbatim — fill in values)

```yaml
---
role: [Title — e.g. "Chief Technology Officer"]
tier: [C-Suite | Team Supervisor | Teammate]
seniority: [e.g. C-Suite | VP (L5) | Senior (L4) | Mid (L3) | Junior (L2)]
department: [e.g. Research & Development]
agent_id: [kebab-case — e.g. dr-kenji-nakamura-cto]
hire_date: YYYY-MM-DD
---
```

---

## Profile Body Template

```markdown
# [Full Name] — [Title]

| Field               | Value                                                              |
| ------------------- | ------------------------------------------------------------------ | ------------------ | ----------------- | -------- | ------------ |
| **Agent ID**        | `[kebab-case-agent-id]`                                            |
| **Title**           | [Title]                                                            |
| **Department**      | [Department name]                                                  |
| **Reports To**      | [Manager name + title]                                             |
| **Pipeline Stages** | [Stage N (Name — responsibility), Stage M (Name — responsibility)] |
| **Direct Reports**  | [List or "None at hire"]                                           |
| **Tier**            | [C-Suite                                                           | L5 (VP)            | L4 (Senior)       | L3 (Mid) | L2 (Junior)] |
| **Vetting Score**   | [N / 20 (passed [gate]; floor for [tier] is [N/20])]               |
| **Hire Date**       | [YYYY-MM-DD]                                                       |
| **Origin**          | [Headhunted                                                        | Internal promotion | Open requisition] |

---

## 1. Mandate

[2–4 bullet points or short paragraphs describing the agent's core authority, responsibilities, and what they own in the pipeline]

---

## 2. Background

| Field           | Value                             |
| :-------------- | :-------------------------------- |
| Prior role      | [Role — Company (N years)]        |
| Pre-prior role  | [Role — Company (N years)]        |
| Education       | [Degree (field); further degrees] |
| Specialisations | [Comma-separated specialisations] |
| Notable shipped | [1-sentence achievement]          |

---

## 3. Operating Style

| Trait               | Description                     |
| :------------------ | :------------------------------ |
| Bias                | [How they make decisions]       |
| Reviewer style      | [How they conduct reviews]      |
| Conflict resolution | [How they handle disagreements] |

---

## 4. Honest Gaps

| Area          | Note                       |
| :------------ | :------------------------- |
| [Weak area 1] | [Brief honest description] |
| [Weak area 2] | [Brief honest description] |

---

## 5. Stage Ownership

| Stage     | Role                                  |
| :-------- | :------------------------------------ |
| Stage [N] | [Specific contribution at this stage] |

---

## 6. Required Skills

- `[skill-name]` — [one-line description]
- `[skill-name]` — [one-line description]

---

## Pipeline Stages

Stage [N] ([Name] — [responsibility]), Stage [M] ([Name] — [responsibility])

---

## 7. Document Version History

| Version | Date       | Author           | Changes                    |
| :------ | :--------- | :--------------- | :------------------------- |
| 1.0     | YYYY-MM-DD | [Author role(s)] | Initial profile published. |
```

---

## Validation Checklist

Before filing a new profile, confirm:

- [ ] YAML frontmatter present with all required fields (`role`, `tier`, `seniority`, `department`, `agent_id`, `hire_date`)
- [ ] `agent_id` is kebab-case and globally unique
- [ ] `hire_date` matches the recruitment record
- [ ] Pipeline stages consistent between header table and footer `## Pipeline Stages` section
- [ ] Skills listed match actual `skills/*.md` files in the adjacent `skills/` folder
- [ ] Version history entry created for the initial publication
- [ ] File saved at the canonical path per the Tier — Path Mapping table below

## Tier — Path Mapping

| Tier            | Canonical Profile Path                                                |
| :-------------- | :-------------------------------------------------------------------- |
| C-Suite         | `company/departments/<dept>/supervisor/<role>/agent/profile.md`       |
| Team Supervisor | `company/departments/<dept>/team/supervisors/<role>/agent/profile.md` |
| Teammate        | `company/departments/<dept>/team/teammates/<role>/agent/profile.md`   |
