---
name: placement-and-profile-authoring
description: CHRO placement and profile authoring protocol — confirming tier placement with the user, writing the agent profile.md from the company template, assembling the mandatory Skills Index, pasting the vetting record, and creating the first skill file stub. Use at Recruitment Pipeline Stage 8 (Placement Confirmation) and Stage 9 (Profile Authoring) to produce a complete, deployable agent record.
version: "1.0.0"
---

# Placement and Profile Authoring

## Purpose

Translate a vetted candidate into a deployable agent record. Vetting (see `vet-candidate.md`) confirms whether the candidate passes. Placement authoring is what happens when they do: the user confirms tier placement, the CHRO writes the `profile.md` using the mandatory template, assembles the Skills Index, pastes the vetting summary, and creates the first skill file stub so the new agent is immediately operational.

## Why This Matters

An agent without a properly authored `profile.md` cannot be activated. A profile without a Skills Index produces an agent who cannot be reliably instantiated. A skill stub with no content is better than no skill file at all — it gives a future executor the correct path and intent even before the skill is fully authored.

## Step 1 — Tier Confirmation with User

After a PASS vetting verdict, Dr. Evelyn Hartwell presents the tier placement recommendation to the user before writing any file:

```
PLACEMENT RECOMMENDATION
Candidate: [Full Name]
Proposed Role: [Title]
Proposed Tier: [C-suite | Team Supervisor | Teammate]
Proposed Department: [department]
Proposed Path: [canonical profile path]

Placement rationale: [1–2 sentences explaining tier choice — seniority, scope, reporting line]

Awaiting user confirmation before profile authoring begins.
```

**User authority is absolute.** If the user disagrees with the tier or role, the CHRO adjusts immediately. No profile file is written until the user confirms.

## Step 2 — Canonical Path Resolution

Before writing any file, resolve the canonical path for the new agent:

| Agent Tier                   | Canonical Path Pattern                                                                   |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| C-suite (e.g. CTO, CDO, CSO) | `company/departments/<dept>/supervisor/<role-kebab>/agent/profile.md`                    |
| Team Supervisor (VP-level)   | `company/departments/<dept>/team/supervisors/<role-kebab>/<first-last>/agent/profile.md` |
| Teammate (IC/Senior IC)      | `company/departments/<dept>/team/teammates/<role-kebab>/<first-last>/agent/profile.md`   |
| Studio Crew                  | `studio/casual-games/team/crew/<division>/<role-kebab>/<first-last>/agent/profile.md`    |

Skills live in a `skills/` directory adjacent to the `agent/` folder:

```
company/departments/<dept>/team/supervisors/<role-kebab>/<first-last>/
├── agent/
│   └── profile.md
└── skills/
    └── <skill-name>.md
```

## Step 3 — Profile Authoring (Mandatory Template)

Every `profile.md` must follow this exact structure:

```markdown
---
name: <role-kebab>
role: supervisor | teammate
tier: supervisor | teammates | C-suite
seniority: <Junior SE | Mid SE | Senior SE | Staff SE | Principal SE | C-suite>
recruited-by: chief-human-resources-officer
---

# <Full Name>

## Title

<Job Title> — <Specialisation>

## Background

[2–4 sentences: education, previous companies, key achievements with numbers, career-defining trait]

## Core Strengths

1. **<Strength 1 title>** — [2–3 sentences with specific, verifiable evidence from career. Quote companies and outcomes.]

2. **<Strength 2 title>** — [2–3 sentences with specific evidence.]

3. **<Strength 3 title>** — [2–3 sentences with specific evidence.]

## Honest Gaps

- [Specific limitation — no company should have an agent with no honest gaps. Be concrete.]
- [Second limitation if applicable.]

## Assigned Role

[2–4 sentences: what this agent owns, which teams/stages they are responsible for, how they collaborate with peers. No fluffy superlatives.]

## Operating Mode

**<Supervisor | Teammate>** — [One sentence describing decision authority and scope.]

## Skills Index

- `<canonical-skill-path>` — <One-sentence description>
- `<canonical-skill-path>` — <One-sentence description>

## Pipeline Stages

<stage numbers, comma-separated>

## Current OKRs / Performance Metrics

### Q2 2026 OKRs

| Objective                    | Key Result              | Progress | Status      |
| ---------------------------- | ----------------------- | -------- | ----------- |
| [Role-appropriate objective] | [Measurable key result] | 0%       | 🔄 Starting |

### Performance Metrics (Trailing 90 Days)

| Metric                    | Target   | Actual | Trend |
| ------------------------- | -------- | ------ | ----- |
| [Role-appropriate metric] | [Target] | TBD    | —     |

## Vetting Record
```

VETTING RESULT: PASS

Scores:

- Impact at Scale: X/5
- Craft Depth: X/5
- Leadership Signal: X/5
- Standards Signal: X/5
- Red Flag Scan: PASS

Total: XX/20

Summary: [2–3 sentence narrative explaining the score, citing specific evidence.]

```

```

### OKR Calibration by Role Type

OKRs must reflect the agent's actual role. Use these templates as starting points — **do not copy engineering OKRs into non-engineering roles**:

| Role Type            | Appropriate OKR Examples                                                |
| -------------------- | ----------------------------------------------------------------------- |
| Engineering / CTO    | Build time, crash-free rate, code coverage, PR review turnaround        |
| Product / CPO        | Feature adoption, DAU/MAU, conversion rate, PRD quality score           |
| Design / CDO         | Design system adoption, time-to-IDS, accessibility pass rate            |
| HR / CHRO            | Time-to-fill, offer acceptance rate, 90-day retention, onboarding NPS   |
| Security / CSO       | Open P0 vulnerabilities, pen test findings, MASVS compliance rate       |
| Localization / CTO-L | String coverage %, BLEU scores, TVR delivery time                       |
| Studio Roles         | Pipeline stage on-time rate, prototype approval, playtesting throughput |

## Step 4 — Skills Index Assembly

Every new profile must have at least one skill in the Skills Index. If the full skill file is not yet authored, create a stub:

```markdown
## Skills Index

- `<canonical-path>/skills/<skill-name>.md` — <One-sentence description matching the agent's primary responsibility>
```

The stub skill file (`<skill-name>.md`) must be created immediately with:

```markdown
---
name: <skill-name>
description: [Copy the one-sentence description from the Skills Index]
version: "1.0.0"
---

# <Skill Title>

## Purpose

[Placeholder — to be authored by the recruiting CTO/CDO/CPO during onboarding.]
```

A profile with a Skills Index entry pointing to a non-existent file is a P1 structural defect.

## Step 5 — Vetting Record Paste

The vetting record is pasted verbatim from the output of `vet-candidate.md`. It must include the numeric scores and the summary narrative — not just "PASS."

## Quality Standards

- No profile file is created before user tier confirmation
- Every profile uses the exact template structure above — missing sections are P1 defects
- Every Skills Index entry resolves to an existing file on disk before the profile is committed
- OKRs must be calibrated to the actual role type — no engineering OKRs pasted into non-engineering profiles
- Vetting record includes numeric scores and narrative — not just a PASS verdict
