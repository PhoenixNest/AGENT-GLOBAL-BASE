# Minimum Viable Context (MVC) Profile — Casual Games Studio

> **Usage:** Append this section to each crew agent profile under
> `studio/casual-games/team/crew/<division>/<role>/<name>/agent/profile.md`
>
> **ASE Compliance:** CC-00 Layer 2 — Context Engineering (Mandatory)
> **Reference:** `core-component-00/context-engineering/CONCEPTS.md`

---

## Purpose

The MVC Profile defines **exactly what context each crew agent needs** for each pipeline stage they participate in. This prevents context dumping (sending everything to every agent) and context starvation (missing critical game design or kill-gate data).

When dispatching a task to a crew member, the orchestrating agent **must** consult the crew member's MVC Profile to assemble only the required context for that stage.

---

## Token Budget Allocation (CC-00 L2 Compliance)

> Mandatory per `core-component-00/agent-systems-engineering/governance/compliance-standard.md` — Layer 2 Context Engineering.

| CC-00 Slot       | Zone (this doc) | Contents                                                     | Budget Cap |       Sacred?        |
| :--------------- | :-------------- | :----------------------------------------------------------- | :--------: | :------------------: |
| **System**       | Zone A          | Crew identity, non-negotiable rules, task objective          |   ≤ 15%    | Yes — never compress |
| **Retrieved**    | Zone B          | GDD, kill gate thresholds, playtest metrics, stage artifacts |   ≤ 30%    |          No          |
| **History**      | Zone C          | Gate decisions, prior stage outputs, kill gate history       |   ≤ 40%    |    Compress first    |
| **Tool Outputs** | _(in-session)_  | Validation results, build reports, CSO gate feedback         |   ≤ 15%    |          No          |

**Prune trigger:** At 85% of model context window, invoke
`core-component-00/context-engineering/implementations/context_compressor.py`.
Compression priority order: Zone C → Zone B → **never Zone A**.

> **Sacred Context rule:** Zone A items (crew identity, pipeline constraints, task objective,
> active kill gate criteria) are excluded from all compression passes and travel whole
> through every stage transition.

---

## Long-Session Compression (CC-00 L2 Required)

For sessions exceeding **10 turns**, apply compression before assembling the next context window:

1. Invoke `core-component-00/context-engineering/implementations/context_compressor.py`
2. Target Zone C (History slot) first — summarise completed stage outputs, retain only kill gate decisions and user sign-offs
3. Target Zone B (Retrieved slot) second — collapse GDD summaries, retain only active feature references and live playtest data
4. **Never compress Zone A** — Sacred Context items travel whole in every handoff
5. After compression, validate total context remains below 85% of model context window

> Reference: `core-component-00/context-engineering/CONCEPTS.md` §compression

---

## Template — Add to Crew Agent Profiles

Copy the following section into each crew member's `profile.md`, filling in only the stages that crew member participates in.

```markdown
## MVC Context Profile

> What context this crew member needs, organised by pipeline stage.
> Orchestrator: include ONLY the items marked ✅ when dispatching to this crew member.

### Stage [N] — [Stage Name]

| Context Item                       | Required? | Zone | Source                             |
| :--------------------------------- | :-------: | :--- | :--------------------------------- |
| Crew identity (this profile)       |    ✅     | A    | This file                          |
| Non-negotiable rules               |    ✅     | A    | `AGENT-BEHAVIORAL-CONSTRAINTS.md`  |
| Task objective                     |    ✅     | A    | Dispatch message                   |
| GDD (full or relevant chapters)    |    ✅     | B    | Stage 1 artifact                   |
| Kill gate thresholds for Stage [N] |    ✅     | B    | casual-games-pipeline.md § Stage N |
| [Stage-specific item 1]            |    ✅     | B    | [Source path]                      |
| [Stage-specific item 2]            |    ✅     | B    | [Source path]                      |
| [Irrelevant item]                  |    ❌     | —    | Not needed                         |
| Prior kill gate decisions          |    ✅     | C    | kill-gate-report.md (prior gates)  |
| Output schema for Stage [N]        |    ✅     | C    | stage-transition-schemas.md        |
| Anti-pattern constraints           |    ✅     | C    | AGENT-BEHAVIORAL-CONSTRAINTS.md    |
```

---

## Pre-Filled Examples

### Example: Studio Director (Dr. Marcus Vogel) — Stage 1 (Concept)

```markdown
## MVC Context Profile

### Stage 1 — Concept (GDD + PRD + SRD)

| Context Item                    | Required? | Zone | Source                                   |
| :------------------------------ | :-------: | :--- | :--------------------------------------- |
| Crew identity                   |    ✅     | A    | leadership/studio-director/marcus-vogel/ |
| Non-negotiable rules            |    ✅     | A    | `AGENT-BEHAVIORAL-CONSTRAINTS.md`        |
| Task objective: GDD + PRD + SRD |    ✅     | A    | Dispatch message                         |
| Studio charter & scope          |    ✅     | B    | library/overview/casual-games-studio.md  |
| Stage 0 art direction output    |    ✅     | B    | Stage 0 artifact                         |
| Market research brief           |    ✅     | B    | Stage 0 artifact                         |
| Kill Gate 1 criteria            |    ✅     | B    | casual-games-pipeline.md § Kill Gate 1   |
| Full crew roster                |    ❌     | —    | Not needed at Concept stage              |
| Prior kill gate decisions       |    ❌     | —    | No prior gates at Stage 1                |
| Stage 1 output schema           |    ✅     | C    | stage-transition-schemas.md § Stage 1    |
| Anti-pattern constraints        |    ✅     | C    | AGENT-BEHAVIORAL-CONSTRAINTS.md          |
```

### Example: Lead Engineer — Stage 5 (Full Production)

```markdown
### Stage 5 — Full Production

| Context Item                      | Required? | Zone | Source                                      |
| :-------------------------------- | :-------: | :--- | :------------------------------------------ |
| Crew identity                     |    ✅     | A    | engineering/gameplay-engineer/...           |
| Non-negotiable rules              |    ✅     | A    | `AGENT-BEHAVIORAL-CONSTRAINTS.md`           |
| Task objective: sprint milestone  |    ✅     | A    | Dispatch message                            |
| TSD (technology decisions)        |    ✅     | B    | Stage 3 artifact                            |
| ADR-GAME-ARCHITECTURE.md          |    ✅     | B    | Stage 3 artifact                            |
| Production plan + Gantt           |    ✅     | B    | Stage 4 artifact                            |
| Kill Gate 4 criteria              |    ✅     | B    | casual-games-pipeline.md § Kill Gate 4      |
| Full GDD (features not in sprint) |    ❌     | —    | Too large — reference chapter headings only |
| Prior kill gate decisions 1–3     |    ✅     | C    | checkpoint.json § kill_gates                |
| Anti-pattern constraints          |    ✅     | C    | AGENT-BEHAVIORAL-CONSTRAINTS.md             |
```

---

## Adoption Plan

1. **Immediate:** The orchestrating agent (Studio Director or designated lead) uses these examples when dispatching tasks.
2. **Before Stage 1:** Add MVC Profile sections to all 38+ crew agent profiles under `studio/casual-games/team/crew/`.
3. **Ongoing:** When a new crew member is onboarded, the MVC Profile section is a mandatory part of their `profile.md`.

---

## Validation Checklist

Before dispatching context to any crew agent:

- [ ] Consulted the crew member's MVC Profile for the target stage
- [ ] Included only ✅ items
- [ ] Placed items in correct zones (A/B/C) per CC-00 slot model
- [ ] Context size is < 50% of model's window (if not, summarise Zone B first)
- [ ] No stale artifacts included (all references are current stage versions)
- [ ] Kill gate criteria for the current stage are included in Zone B
