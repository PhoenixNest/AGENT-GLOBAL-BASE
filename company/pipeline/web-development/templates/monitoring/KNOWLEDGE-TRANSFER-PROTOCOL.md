# Knowledge Transfer Protocol — Cross-Project Learning System

> **Addresses Gap:** #7 (No cross-project knowledge transfer)

---

## 1. Purpose

This protocol defines how **knowledge generated during one project** is captured, distilled, and made available to **future projects** — creating an organizational learning loop that improves with every pipeline execution.

Without this protocol, each new project starts from zero. With it, agents build on accumulated institutional knowledge.

---

## 2. The Three Knowledge Tiers

```
┌─────────────────────────────────────────────────────┐
│  Tier 3 — INSTITUTIONAL MEMORY                      │
│  Long-lived, cross-project patterns and heuristics  │
│  Updated: Quarterly review                          │
├─────────────────────────────────────────────────────┤
│  Tier 2 — PROJECT RETROSPECTIVE                     │
│  Project-scoped lessons learned + performance data  │
│  Updated: At project completion (Stage 10)          │
├─────────────────────────────────────────────────────┤
│  Tier 1 — SESSION ARTIFACTS                         │
│  Raw stage outputs, schemas, transition summaries   │
│  Updated: Continuously during pipeline execution    │
└─────────────────────────────────────────────────────┘
```

---

## 3. Tier 1 — Session Artifacts (Raw)

**What:** Every artifact produced during pipeline execution.

**Storage:** `company/project/<project-id>/stages/`

**Lifecycle:** Retained for the duration of the project + 1 quarter after release.

**Index File:** Each project maintains a `PROJECT-ARTIFACT-INDEX.md`:

```markdown
# Project Artifact Index

## Stage 1

- PRD v1.2 → stages/1-requirements/prd-v1.2.md
- SRD v1.0 → stages/1-requirements/srd-v1.0.md
- Transition Schema → stages/1-requirements/schema-1-to-2.json

## Stage 2

- Prototype → stages/2-design/prototype/index.html
- IDS v1.0 → stages/2-design/ids-v1.0.md
  ...
```

---

## 4. Tier 2 — Project Retrospective (Distilled)

**What:** A structured post-mortem capturing what worked, what didn't, and measurable outcomes.

**Produced By:** CTO (convenes retrospective panel at Stage 10 completion)

**Storage:** `company/project/<project-id>/retrospective.md`

**Template:**

```markdown
# Project Retrospective — [Project Name]

## Metadata

- Project ID: [ID]
- Duration: [Start Date] → [End Date]
- Team Size: [N agents]
- Platform Strategy: [native_dual | kmp | flutter]
- Final Release Decision: [approved | rejected | deferred]

## Pipeline Performance

| Stage | Estimated Duration | Actual Duration | Variance | Notes |
| :---: | :----------------- | :-------------- | :------: | :---- |
|   1   | [N days]           | [N days]        | [+/-N%]  |       |
|   2   | [N days]           | [N days]        | [+/-N%]  |       |
|  ...  |                    |                 |          |       |

## Defect Metrics

| Metric                          | Value |
| :------------------------------ | :---- |
| Total defects found (Stage 6)   | [N]   |
| P0 defects                      | [N]   |
| P1 defects                      | [N]   |
| P2/P3 deferred                  | [N]   |
| Review rounds (Stage 6)         | [N]   |
| Test pass rate (Stage 7)        | [N%]  |
| Integrity regressions (Stage 8) | [N]   |

## What Worked Well

1. [Practice/tool/process] — [measurable impact]
2. ...

## What Didn't Work

1. [Issue] — [root cause] — [recommended fix]
2. ...

## ADR Effectiveness

| ADR ID  | Decision   | Outcome  | Would Repeat? |
| :------ | :--------- | :------- | :-----------: |
| ADR-001 | [Decision] | [Impact] |     ✅/❌     |

## Agent Performance Observations

| Agent   | Stage | Observation     | Recommendation        |
| :------ | :---: | :-------------- | :-------------------- |
| [Agent] |  [N]  | [What happened] | [For future projects] |

## Knowledge Items to Promote to Tier 3

1. [Pattern/heuristic to promote] — [rationale]
2. ...
```

---

## 5. Tier 3 — Institutional Memory (Permanent)

**What:** Distilled patterns, heuristics, and best practices that transcend individual projects.

**Storage:** `company/library/topics/institutional-memory.md`

**Update Cycle:** Quarterly review by CTO + CPO + CSO

**Format:**

```markdown
# Institutional Memory — Organizational Knowledge Base

## Architecture Patterns

### Pattern: [Name]

- **Source:** Project [ID], Stage [N]
- **Context:** [When this applies]
- **Decision:** [What to do]
- **Outcome:** [What happened when we applied it]
- **Confidence:** [High | Medium | Low] (based on N projects)

## Security Heuristics

### Heuristic: [Name]

- **Source:** Project [ID], Red Team Report
- **Rule:** [The heuristic]
- **Evidence:** [N] projects confirmed this pattern
- **Counter-examples:** [Any exceptions]

## Process Improvements

### Improvement: [Name]

- **Source:** Project [ID] Retrospective
- **Before:** [Old process]
- **After:** [New process]
- **Impact:** [Measurable improvement]

## Estimation Calibration

### Stage [N] — [Stage Name]

- **Average duration:** [N days] (across [N] projects)
- **Variance range:** [±N%]
- **Common blockers:** [List]
- **Estimation adjustment factor:** [multiplier]
```

---

## 6. Knowledge Retrieval Rules

When an agent begins work at any pipeline stage, the orchestrator **must**:

1. **Check Tier 3** — Is there an institutional memory entry relevant to this stage or decision?
2. **Check Tier 2** — Are there retrospectives from similar past projects?
3. **Inject relevant knowledge** into the agent's Zone B context (per MVC Profile)
4. **Never dump all tiers** — apply MVC filtering to select only relevant entries

### Retrieval Priority Matrix

| Agent Context Need    | Tier to Check                                | Example                                               |
| :-------------------- | :------------------------------------------- | :---------------------------------------------------- |
| Architecture decision | Tier 3 Patterns → Tier 2 ADR Effectiveness   | "KMP vs Flutter — what worked last time?"             |
| Estimation accuracy   | Tier 3 Calibration                           | "Stage 5 typically takes 2.3x the initial estimate"   |
| Security posture      | Tier 3 Heuristics → Tier 2 Red Team findings | "Certificate pinning implementation pitfalls"         |
| Defect prevention     | Tier 2 Defect Metrics → Tier 3 Process       | "Stage 6 typically finds 40% of defects in API layer" |
| Team staffing         | Tier 2 Agent Observations                    | "Agent X excels at Compose migration tasks"           |

---

## 7. Promotion Pipeline (Tier 2 → Tier 3)

```
Project completes Stage 10
    ↓
CTO convenes retrospective panel
    ↓
Panel identifies candidate patterns/heuristics
    ↓
Candidate validated across ≥ 2 projects (or P0-level importance)
    ↓
CTO drafts Tier 3 entry
    ↓
CPO + CSO review for completeness
    ↓
Entry added to institutional-memory.md
    ↓
Quarterly review: prune stale entries, update confidence levels
```

---

## 8. Anti-Patterns

| Anti-Pattern                | Why It's Harmful                                | Prevention                                         |
| :-------------------------- | :---------------------------------------------- | :------------------------------------------------- |
| **Knowledge hoarding**      | Agent learns something but doesn't record it    | All agents must file observations in retrospective |
| **Stale memory**            | Tier 3 entry no longer applies but isn't pruned | Quarterly review with confidence decay             |
| **Over-retrieval**          | Dumping all Tier 3 into every context window    | MVC filtering — only relevant entries              |
| **Anecdote-as-policy**      | One project's outlier becomes permanent rule    | Require ≥2 project validation for Tier 3           |
| **Copy-paste architecture** | Blindly reusing ADRs from past projects         | Each project's ADRs must be authored fresh         |

---

## 9. Integration Points

| Component                               | Integration                                                 |
| :-------------------------------------- | :---------------------------------------------------------- |
| `stage-transition-schemas.md`           | Tier 1 artifacts stored per schema version                  |
| `inter-agent-communication-protocol.md` | Retrospective observations follow Escalation Message format |
| `mvc-context-profile.md`                | Tier 2/3 retrieval is a Zone B context item                 |
| `context-engineering.md`                | Knowledge retrieval follows MVC filtering rules             |
| `pipeline.md` § Stage 10                | Retrospective is mandatory before project closure           |
