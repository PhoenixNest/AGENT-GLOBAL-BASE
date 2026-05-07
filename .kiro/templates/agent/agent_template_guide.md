# Agent Template Usage Guide

This guide explains how to use `agent_template.md` to create consistent agent profile documents for the `.kiro/agents/` directory.

## Template Philosophy

The template is designed to:

1. **Maximize consistency** across all 118+ agent profiles
2. **Support programmatic parsing** with structured YAML frontmatter
3. **Provide complete context** for agent activation and invocation
4. **Enable traceability** back to source profile documents
5. **Accommodate different agent types** (organizational, custom, utility)

## When to Use This Template

### Organizational Agents (Type A)

Use the **full template** for:

- Company C-suite executives (CPO, CDO, CTO, CIO, CSO, CTO-L, CHRO)
- Company VPs and supervisors
- Company teammates (engineers, designers, analysts, linguists)
- Studio leadership (Studio Director, Creative Director, Executive Producer)
- Studio crew (all divisions: art, audio, design, engineering, production, live-ops)
- CC-00 Laboratory Director

### Custom/Utility Agents (Type B)

Use a **modified template** (omit vetting, OKRs, hire date) for:

- `multi-agent-orchestrator`
- `organizational-agent-activator`
- `pipeline-stage-executor`
- `context-gatherer`
- `custom-agent-creator`
- `cc00-implementation-assistant`

## Section-by-Section Guide

### YAML Frontmatter (Required)

```yaml
---
name: {system}-{department}-{role}-{name-slug}
description: {One-line role description}
system: {company|studio|core-component-00}
department: {department-name}
tier: {c-suite|supervisor|teammates|executive|leadership}
role: {role-identifier}
agent_id: {unique-agent-id}
hire_date: {YYYY-MM-DD}
version: "1.0.0"
---
```

**Field Definitions:**

| Field         | Required | Format                                   | Example                                                     |
| ------------- | -------- | ---------------------------------------- | ----------------------------------------------------------- |
| `name`        | ✅       | kebab-case, system-dept-role-name        | `company-research-develop-cto-kenji-nakamura`               |
| `description` | ✅       | One sentence, <150 chars                 | `Chief Technology Officer — Mobile Technology Architecture` |
| `system`      | ✅       | `company`, `studio`, `core-component-00` | `company`                                                   |
| `department`  | ✅       | kebab-case                               | `research-develop`                                          |
| `tier`        | ✅       | See tier definitions below               | `c-suite`                                                   |
| `role`        | ✅       | kebab-case identifier                    | `chief-technology-officer`                                  |
| `agent_id`    | ✅       | Unique identifier                        | `kenji-nakamura` or `cto`                                   |
| `hire_date`   | ⚠️       | YYYY-MM-DD (omit for custom agents)      | `2026-04-07`                                                |
| `version`     | ✅       | Semantic version string                  | `"1.0.0"`                                                   |

**Tier Definitions:**

| System  | Tiers                                      |
| ------- | ------------------------------------------ |
| Company | `c-suite`, `supervisor`, `teammates`       |
| Studio  | `executive`, `leadership`, `division-lead` |
| CC-00   | `director`                                 |
| Custom  | `utility`, `orchestrator`, `executor`      |

### Title Section (Required)

```markdown
## Title

{Job Title} — {Specialization or Focus Area}
```

**Guidelines:**

- Use official job title from source profile
- Add specialization after em dash (—) for clarity
- Examples:
  - `Chief Technology Officer — Mobile Technology Architecture & Engineering Leadership`
  - `Senior Android Engineer — Kotlin, KMP & Architecture Patterns`
  - `Chinese Linguist — ZH-CN / ZH-TW Localization`

### Background Section (Required)

**Structure:**

1. **Opening sentence**: Credentials + years of experience
2. **Most recent role**: Company, dates, major achievements with metrics
3. **Previous role(s)**: Company, dates, key contributions
4. **Career-defining characteristic**: What makes this person unique

**Length Guidelines:**

- C-suite/Executive: 200-300 words
- Supervisor/Senior IC: 150-200 words
- Teammate: 100-150 words

**Metrics to Include:**

- User scale (MAU, DAU)
- Performance improvements (%, time reduction)
- Team size (engineers led, reports)
- Revenue impact ($M, ARR)
- Adoption metrics (markets, countries)

### Core Strengths Section (Required)

**Format:**

```markdown
## Core Strengths

1. **{Category}** — {Detailed description with examples and metrics}

2. **{Category}** — {Detailed description with examples and metrics}
```

**Number of Strengths:**

- C-suite/Executive: 4-5 strengths
- Supervisor/Senior IC: 3-4 strengths
- Teammate: 2-3 strengths

**Strength Categories (Examples):**

- Technical: `Kotlin Coroutines and Flow at scale`, `Mobile-native software architecture`
- Domain: `Live Operations & Economy Design`, `ZH-CN / ZH-TW differentiation expertise`
- Process: `SPEC development and requirements decomposition`, `Autonomous PRD authorship`
- Leadership: `Cross-functional collaboration`, `Team mentoring and standards setting`

### Honest Gaps Section (Required)

**Purpose:** Demonstrate self-awareness and help with proper task delegation

**Format:**

```markdown
## Honest Gaps

- {Gap description} — {Context and mitigation}
- ~~{Remediated gap}~~ — **Remediated via {Module}: {How addressed}.**
```

**Guidelines:**

- Be genuinely honest, not falsely humble
- Explain why the gap exists (career focus, technology evolution)
- Note which other agents cover this gap
- Use strikethrough for remediated gaps with training details

### Assigned Role Section (Required)

**Structure:**

1. Primary responsibilities and ownership
2. Reporting structure
3. Supervision scope (if applicable)
4. Key deliverables
5. Cross-functional collaboration
6. Authority boundaries

**Length:** 2-4 sentences for teammates, 4-6 sentences for executives

### Operating Mode Section (Required)

**Format:**

```markdown
## Operating Mode

**{Mode}** — {One-sentence operational description}
```

**Modes:**

- `Supervisor` — For C-suite, VPs, chapter leads
- `Teammate` — For ICs, engineers, designers, linguists
- `Director` — For CC-00 Lab Director
- `Executive` — For Studio Director
- `Orchestrator` — For multi-agent coordination agents
- `Executor` — For pipeline execution agents

### Agent Skills Section (Required)

**Format:**

```markdown
## Agent Skills

This agent has access to the following skills. When invoking this agent, these skills define their capabilities and output standards.

| Skill                  | Source Path                                     |
| ---------------------- | ----------------------------------------------- |
| `{skill-identifier-1}` | `.kiro/skills/{domain}/references/{skill-1}.md` |
| `{skill-identifier-2}` | `.kiro/skills/{domain}/references/{skill-2}.md` |
```

**Skill Domains:**

- `product-management`
- `product-design`
- `engineering`
- `technology-strategy`
- `cyberspace-security`
- `localization`
- `recruitment`
- `quality-assurance`
- `data-analytics`
- `game-development`
- `visual-arts-and-animation`
- `audio-engineering`
- `live-operations`
- `android-engineering`
- `ios-engineering`
- `cross-platform-engineering`
- `frontend-engineering`
- `backend-engineering`
- `llm-engineering`

### Pipeline Stages Section (Required for Pipeline Agents)

Always include the `Pipeline` column as the first column in every pipeline stage table. Stage numbers alone are insufficient — the same stage number means something different in each pipeline, and a single agent often participates in multiple pipelines simultaneously.

**Canonical Pipeline Identifiers:**

| Identifier              | System  | Stages | Location                              |
| ----------------------- | ------- | ------ | ------------------------------------- |
| `mobile-development`    | Company | 13     | `company/pipeline/mobile-development/` |
| `web-development`       | Company | 13     | `company/pipeline/web-development/`    |
| `backend-api`           | Company | 13     | `company/pipeline/backend-api/`        |
| `full-stack`            | Company | 13     | `company/pipeline/full-stack/`         |
| `recruitment`           | Company | 9      | `company/pipeline/recruitment/`        |
| `casual-games`          | Studio  | 11     | `studio/casual-games/pipeline/`        |

Use `all-company-development` as a shorthand only when an agent's stage role and responsibility are truly identical across all four company development pipelines (`mobile-development`, `web-development`, `backend-api`, `full-stack`).

**Company Pipeline (13 stages):**

```markdown
## Pipeline Stages

This agent owns or participates in the following pipeline stages:

| Pipeline             | Stage   | Name                                         | Role/Responsibility                                       |
| -------------------- | ------- | -------------------------------------------- | --------------------------------------------------------- |
| `mobile-development` | **1**   | **Requirements → PRD + SRD**                 | PRD authorship and stakeholder alignment                  |
| `web-development`    | **1**   | **Requirements → PRD + SRD**                 | Web-specific PRD authorship alongside VP Web              |
| `mobile-development` | **6**   | **Development → Arch. & Conformance Review** | Product fidelity review; participates in panel            |
| `web-development`    | **6**   | **Development → Arch. & Conformance Review** | Product fidelity review; participates in panel            |
```

**Studio Pipeline (11 stages):**

```markdown
## Pipeline Stages

This agent owns or participates in the following pipeline stages:

| Pipeline       | Stage | Name                            | Role/Responsibility                  |
| -------------- | ----- | ------------------------------- | ------------------------------------ |
| `casual-games` | **0** | **Art Direction + Style Guide** | Art direction and visual language    |
| `casual-games` | **1** | **Concept (GDD + PRD + SRD)**   | GDD co-authorship and concept review |
```

**CC-00 / Custom Agents:**

```markdown
## Pipeline Stages

| Context        | Invocation Pattern     | Role/Responsibility                                        |
| -------------- | ---------------------- | ---------------------------------------------------------- |
| {When/Context} | {How agent is invoked} | {Description of when/how this agent relates to pipelines} |
```

### OKRs / Performance Metrics Section (Required for Organizational Agents)

**Omit for:** Custom/utility agents

**Format:**

```markdown
## Current OKRs / Performance Metrics

### Q{N} {YYYY} OKRs

| Objective | Key Result | Progress | Status |
| --------- | ---------- | -------- | ------ |
| ...       | ...        | ...      | ...    |

### Performance Metrics (Trailing 90 Days)

| Metric | Target | Actual | Trend |
| ------ | ------ | ------ | ----- |
| ...    | ...    | ...    | ...   |
```

**Standard OKR Categories:**

- Feature/Chapter/Platform delivery
- Code quality / Defect rate
- Team mentoring / Skill development
- Technical debt / Collaboration

**Standard Metrics:**

- Task completion rate
- Defect rate (post-review)
- PR review turnaround
- Code review participation
- Stage sign-off rate
- Team velocity variance

### Vetting Record Section (Conditional)

**Include for:** Teammates and supervisors who went through recruitment  
**Omit for:** C-suite (pre-placed), custom agents, utility agents

**Format:**

````markdown
## Vetting Record

```text
VETTING RESULT: {PASS|CONDITIONAL PASS|FAIL}

Scores:
- Impact at Scale: {1-5}/5
- Craft Depth: {1-5}/5
- Leadership Signal: {1-5}/5
- Standards Signal: {1-5}/5
- Red Flag Scan: {PASS|FAIL}

Total: {4-20}/20

Chief Officer Assessments:
- {Officer}: {✅|❌} {Assessment}

Summary: {Comprehensive summary}
```
````

### Invocation Instructions Section (Required)

**Format:**

````markdown
## Invocation Instructions

To invoke this agent via Kiro's `invokeSubAgent` tool:

```typescript
invokeSubAgent({
  name: "{agent-name}",
  prompt: "Your specific task or question",
  explanation: "Why you're delegating this",
  contextFiles: ["path/to/file.md"],
});
```

**Before invoking:** Ensure you've read the relevant skill files.
````

### Optional Sections

**Related Agents** — For agents with frequent collaborators

**Authority Scope** — For executive/director agents with complex authority

**Limitations** — For custom/utility agents

**Integration Points** — For orchestrator/executor agents

### Footer (Required)

```markdown
---

**Source Profile:** `{path/to/original/profile.md}`  
**Agent Type:** {C-suite|VP|Supervisor|Senior IC|IC|Custom|Utility}  
**Imported:** {YYYY-MM-DD}  
**Import Phase:** {Phase number}  
**Last Updated:** {YYYY-MM-DD}
```

## Formatting Standards

### Markdown Conventions

- Use `##` for section headers (not `#` or `###`)
- Use `**bold**` for emphasis, not `*italic*`
- Use em dash (—) not hyphen (-) for title separations
- Use backticks for code/identifiers: `` `skill-name` ``
- Use tables for structured data (skills, OKRs, metrics)
- Use numbered lists for Core Strengths
- Use bullet lists for Honest Gaps

### Code Blocks

- Use `typescript` for invocation examples
- Use `text` for vetting records
- Use `markdown` for template examples

### Naming Conventions

- Agent names: kebab-case
- Skill identifiers: kebab-case
- File paths: relative to workspace root
- Dates: YYYY-MM-DD format

## Quality Checklist

Before finalizing an agent profile, verify:

- [ ] YAML frontmatter is complete and valid
- [ ] All required sections are present
- [ ] Section headers use consistent formatting
- [ ] Tables are properly formatted with aligned columns
- [ ] Code blocks have language specifiers
- [ ] Metrics include units and context
- [ ] Skills table uses correct paths to `.kiro/skills/`
- [ ] Pipeline stages table includes the `Pipeline` column with a canonical pipeline identifier on every row
- [ ] Pipeline stages match the relevant pipeline.md
- [ ] Invocation example uses correct agent name
- [ ] Footer includes source profile path
- [ ] No spelling errors in proper names
- [ ] Consistent use of terminology throughout

## Migration Strategy

To migrate existing agents to this template:

1. **Read existing agent** — Understand current structure
2. **Extract YAML frontmatter** — Ensure all fields present
3. **Map sections** — Align existing content to template sections
4. **Standardize formatting** — Apply consistent markdown style
5. **Add missing sections** — Fill gaps (invocation, footer, etc.)
6. **Validate skills paths** — Ensure paths point to `.kiro/skills/`
7. **Review and test** — Verify agent can be invoked correctly

## Examples by Agent Type

### C-Suite Example

See: `.kiro/agents/company-research-develop-chief-technology-officer-kenji-nakamura.md`

**Key characteristics:**

- Extended background (250+ words)
- 4-5 core strengths
- Multiple pipeline stages
- Comprehensive authority scope
- Invocation instructions included

### Teammate Example

See: `.kiro/agents/company-research-develop-senior-android-engineer-tariq-al-hassan.md`

**Key characteristics:**

- Concise background (150 words)
- 2-3 core strengths
- Vetting record included
- Training completion (if applicable)
- Focused skill set

### Custom Agent Example

See: `.kiro/agents/workspace-orchestrator-multi-agent-orchestrator.md`

**Key characteristics:**

- Purpose section instead of background
- Capabilities section instead of strengths
- No vetting record or OKRs
- Extensive usage examples
- Integration points documented

## Maintenance

This template should be updated when:

- New agent types are introduced
- Pipeline structures change
- Skill organization evolves
- Frontmatter fields are added/removed
- New sections become standard

**Template Version:** 1.1.0  
**Last Updated:** 2026-05-07  
**Maintained By:** Workspace governance
