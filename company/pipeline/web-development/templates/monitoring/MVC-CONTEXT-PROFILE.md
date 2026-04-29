# Minimum Viable Context (MVC) Profile Template

> **Addresses Gap:** #8 (MVC Enforcement)
> **Usage:** Append this section to each agent profile in `.gemini/agents/*.md`

---

## Purpose

The MVC Profile defines **exactly what context each agent needs** for each pipeline stage they participate in. This prevents context dumping (sending everything) and context starvation (missing critical info).

When dispatching a task to an agent, the orchestrator **must** consult the agent's MVC Profile to assemble only the required context.

---

## Template — Add to Agent Profiles

Copy the following section into each agent's `.md` profile file, filling in only the stages that agent participates in.

```markdown
## MVC Context Profile

> What context this agent needs, organized by pipeline stage.
> Orchestrator: include ONLY the items marked ✅ when dispatching to this agent.

### Stage [N] — [Stage Name]

| Context Item                  | Required? | Format | Source                        |
| :---------------------------- | :-------: | :----- | :---------------------------- |
| Agent identity (this profile) |    ✅     | Zone A | This file                     |
| Non-negotiable rules          |    ✅     | Zone A | AGENTS.md § Rules             |
| Task objective                |    ✅     | Zone A | Dispatch message              |
| [Stage-specific item 1]       |    ✅     | Zone B | [Source path]                 |
| [Stage-specific item 2]       |    ✅     | Zone B | [Source path]                 |
| [Stage-specific item 3]       |    ❌     | —      | Not needed                    |
| Gate criteria for Stage [N]   |    ✅     | Zone C | pipeline.md § Stage N         |
| Output schema                 |    ✅     | Zone C | STAGE-TRANSITION-SCHEMAS.md   |
| Anti-pattern constraints      |    ✅     | Zone C | Context Engineering guideline |
```

---

## Pre-Filled Examples

### Example: CTO (Dr. Kenji Nakamura) — Stage 3

```markdown
## MVC Context Profile

### Stage 3 — UML Engineering Package

| Context Item                  | Required? | Format | Source                        |
| :---------------------------- | :-------: | :----- | :---------------------------- |
| Agent identity                |    ✅     | Zone A | cto-dr-kenji-nakamura.md      |
| Non-negotiable rules          |    ✅     | Zone A | AGENTS.md § Rules             |
| Task objective                |    ✅     | Zone A | Dispatch message              |
| PRD (full)                    |    ✅     | Zone B | Stage 1 artifact              |
| SRD (full)                    |    ✅     | Zone B | Stage 1 artifact              |
| Web Prototype reference       |    ✅     | Zone B | Stage 2 artifact (link only)  |
| IDS (full)                    |    ✅     | Zone B | Stage 2 artifact              |
| Schema 2→3 transition summary |    ✅     | Zone B | Stage 2 JSON output           |
| Architecture skill guidelines |    ✅     | Zone B | skills/architecture/          |
| Previous ADR history (if any) |    ❌     | —      | First project — none          |
| Gate criteria for Stage 3     |    ✅     | Zone C | pipeline.md § Stage 3         |
| Output schema 3→4             |    ✅     | Zone C | STAGE-TRANSITION-SCHEMAS.md   |
| Anti-patterns                 |    ✅     | Zone C | Context Engineering guideline |
```

### Example: CDO (Yuki Tanaka-Chen) — Stage 2

```markdown
### Stage 2 — Web Prototype + IDS

| Context Item                        | Required? | Format | Source                      |
| :---------------------------------- | :-------: | :----- | :-------------------------- |
| Agent identity                      |    ✅     | Zone A | cdo-yuki-tanaka-chen.md     |
| Non-negotiable rules                |    ✅     | Zone A | AGENTS.md § Rules           |
| Task objective                      |    ✅     | Zone A | Dispatch message            |
| PRD (full)                          |    ✅     | Zone B | Stage 1 artifact            |
| SRD (security UI requirements only) |    ✅     | Zone B | Stage 1 artifact (filtered) |
| Schema 1→2 transition summary       |    ✅     | Zone B | Stage 1 JSON output         |
| Design skill guidelines             |    ✅     | Zone B | skills/design/              |
| Full pipeline definition            |    ❌     | —      | Not needed                  |
| All agent profiles                  |    ❌     | —      | Not needed                  |
| Gate criteria for Stage 2           |    ✅     | Zone C | pipeline.md § Stage 2       |
| Output schema 2→3                   |    ✅     | Zone C | STAGE-TRANSITION-SCHEMAS.md |
```

### Example: CSO (Dr. Sarah Chen) — Stage 6 Red Team

```markdown
### Stage 6 — Red Team Review

| Context Item                       | Required? | Format | Source                         |
| :--------------------------------- | :-------: | :----- | :----------------------------- |
| Agent identity                     |    ✅     | Zone A | cso-dr-sarah-chen.md           |
| Non-negotiable rules               |    ✅     | Zone A | AGENTS.md § Rules              |
| Task objective: adversarial review |    ✅     | Zone A | Dispatch message               |
| SRD (full)                         |    ✅     | Zone B | Stage 1 artifact               |
| Security Architecture ADRs         |    ✅     | Zone B | Stage 3 artifacts              |
| SIS (full)                         |    ✅     | Zone B | Stage 5 artifact               |
| Codebase access                    |    ✅     | Zone B | Stage 5 output                 |
| Schema 5→6 transition summary      |    ✅     | Zone B | Stage 5 JSON output            |
| PRD (full)                         |    ❌     | —      | Not needed for security review |
| IDS (full)                         |    ❌     | —      | Not needed for security review |
| Red Team Review template           |    ✅     | Zone C | RED-TEAM-REVIEW.md             |
| Gate criteria for Stage 6          |    ✅     | Zone C | pipeline.md § Stage 6          |
| Output format: Red Team Report     |    ✅     | Zone C | RED-TEAM-REVIEW.md § Report    |
```

---

## Adoption Plan

1. **Immediate:** The orchestrator (lead agent) uses these examples as a reference when dispatching tasks.
2. **Week 4–6:** Add MVC Profile sections to all 79 agent profiles in `.gemini/agents/`.
3. **Ongoing:** When a new agent is added, MVC Profile is a mandatory section in their profile.

---

## Validation Checklist

Before dispatching context to any agent:

- [ ] Consulted the agent's MVC Profile for the target stage
- [ ] Included only ✅ items
- [ ] Placed items in correct zones (A/B/C) per context-engineering guideline
- [ ] Context size is < 50% of model's window (if not, summarize Zone B)
- [ ] No stale artifacts included (all references are current versions)
