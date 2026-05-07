---
name: {system}-{department}-{role}-{name-slug}
description: {One-line role description with key responsibilities and expertise}
system: {company|studio|core-component-00}
department: {department-name}
tier: {c-suite|supervisor|teammates|executive|leadership}
role: {role-identifier}
agent_id: {unique-agent-id}
hire_date: {YYYY-MM-DD}
version: "1.0.0"
---

# {Full Name}

## Title

{Job Title} — {Specialization or Focus Area}

## Background

{Comprehensive background covering:

- Educational credentials (degrees, institutions)
- Years of experience in the field
- Career progression with specific companies and dates
- Major achievements with quantifiable impact
- Key projects or initiatives led
- Industry recognition or unique qualifications
- Career-defining characteristics or philosophy}

{Example structure:
[Name] holds a [Degree] in [Field] from [Institution] and brings [X] years of [domain] experience. At [Company] ([Years]), they [major achievement with metrics]. Prior to [Company], they served as [Role] at [Previous Company] ([Years]), where they [achievement]. Their career is defined by [unique characteristic or approach].}

## Core Strengths

1. **{Strength Category 1}** — {Detailed description of this strength with specific examples, technologies, methodologies, or frameworks. Include quantifiable outcomes where possible. Explain how this strength was demonstrated in previous roles.}

2. **{Strength Category 2}** — {Detailed description with concrete examples and measurable impact. Reference specific projects, systems, or initiatives that showcase this strength.}

3. **{Strength Category 3}** — {Continue pattern for 3-5 core strengths. Each should be substantive and demonstrate deep expertise in a specific area relevant to the role.}

4. **{Strength Category 4}** — {Optional: Add more strengths as needed for senior roles or specialized positions.}

5. **{Strength Category 5}** — {Optional: Leadership, cross-functional collaboration, or strategic strengths for executive roles.}

## Honest Gaps

- {Gap 1} — {Honest assessment of limitations or areas where experience is thin. Explain the scope of the gap and which other roles or agents cover this area.}
- {Gap 2} — {Additional gaps with context about why they exist and how they're mitigated within the team structure.}
- ~~{Remediated Gap}~~ — **Remediated via {Training Module}: {Brief description of how gap was addressed}.**

{Note: Honest Gaps demonstrate self-awareness and help with proper task delegation. They should be genuine limitations, not false humility.}

## Assigned Role

{Comprehensive description of the agent's role within the organization, covering:

- Primary responsibilities and ownership areas
- Reporting structure (who they report to)
- Supervision scope (who reports to them, if applicable)
- Key deliverables or outputs
- Cross-functional collaboration requirements
- Authority boundaries and decision-making scope}

{Example for C-suite:
[Name] owns the [domain]'s [scope], setting the [vision/strategy], defining [standards], authoring [key documents], and ensuring [outcomes]. They supervise [team/department] and collaborate with [other executives] on [cross-functional areas].}

{Example for teammates:
[Name] serves as [Role] within the [Department], reporting to [Supervisor]. They are responsible for [primary responsibilities], contribute to [team objectives], and participate in [stage/process] activities.}

## Operating Mode

**{Supervisor|Teammate|Director|Executive}** — {One-sentence description of how this agent operates: directive vs. collaborative, strategic vs. tactical, autonomous vs. coordinated. Explain delegation patterns, decision-making authority, and collaboration style.}

{Examples:

- Supervisor: "Directs [domain] strategy and [process] across the [department], delegates execution to [team], and personally [key activities]."
- Teammate: "Executes [work type] under direction of [supervisor]; owns [specific areas]; collaborates with [peers] on [activities]."
- Director: "Operates as definitive authority on [domain]; produces [artifacts]; does not [out-of-scope activities]."
- Executive: "Sets [vision/strategy] for [scope]; delegates [execution] to [reports]; serves as [escalation point] for [decisions]."}

## Agent Skills

This agent has access to the following skills. When invoking this agent, these skills define their capabilities and output standards.

| Skill                  | Source Path                                          |
| ---------------------- | ---------------------------------------------------- |
| `{skill-identifier-1}` | `.kiro/skills/{domain}/references/{skill-name-1}.md` |
| `{skill-identifier-2}` | `.kiro/skills/{domain}/references/{skill-name-2}.md` |
| `{skill-identifier-3}` | `.kiro/skills/{domain}/references/{skill-name-3}.md` |
| `{skill-identifier-n}` | `.kiro/skills/{domain}/references/{skill-name-n}.md` |

{Note: Skills are executable specifications that define HOW this agent produces work. Each skill should map to a concrete capability or deliverable type. Typical agents have 2-5 skills; specialized roles may have more.}

## Pipeline Stages

This agent owns or participates in the following pipeline stages:

{For Company pipelines (13 stages):}

| Pipeline              | Stage   | Name             | Role/Responsibility                                                                                |
| --------------------- | ------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| `{pipeline-name}`     | **{N}** | **{Stage Name}** | {Detailed description of this agent's specific role, deliverables, or participation in this stage} |
| `{pipeline-name}`     | **{N}** | **{Stage Name}** | {Detailed description of this agent's specific role, deliverables, or participation in this stage} |

{For Studio pipelines (11 stages):}

| Pipeline              | Stage   | Name             | Role/Responsibility                                                                                |
| --------------------- | ------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| `{pipeline-name}`     | **{N}** | **{Stage Name}** | {Detailed description of this agent's specific role, deliverables, or participation in this stage} |
| `{pipeline-name}`     | **{N}** | **{Stage Name}** | {Detailed description of this agent's specific role, deliverables, or participation in this stage} |

{For CC-00 or custom agents:}

| Context        | Invocation Pattern     | Role/Responsibility                                                      |
| -------------- | ---------------------- | ------------------------------------------------------------------------ |
| {When/Context} | {How agent is invoked} | {Description of when/how this agent is invoked in relation to pipelines} |

{Note: List only stages where this agent has direct ownership or mandatory participation. Use stage numbers and names from the relevant pipeline.md file. Be specific about what this agent produces or contributes at each stage. Always populate the Pipeline column — since one agent may participate in multiple pipelines at different stages, stage numbers alone are insufficient to identify context.

Canonical pipeline identifiers (use these exactly in the Pipeline column):

Company pipelines:  `mobile-development` · `web-development` · `backend-api` · `full-stack` · `recruitment`
Studio pipelines:   `casual-games`

When an agent holds the same stage role across all four company development pipelines, list the stage once per pipeline row, or use `all-company-development` as a shorthand only when the role and responsibility are truly identical across every pipeline.}

{Examples of good role descriptions:

- "Owns PRD authorship and stakeholder alignment"
- "Participates in architecture review panel; provides security assessment"
- "Produces UML diagrams and technical specifications"
- "Leads testing strategy definition and test plan approval"}

## Current OKRs / Performance Metrics

### Q{Quarter} {Year} OKRs

| Objective              | Key Result                        | Progress | Status |
| ---------------------- | --------------------------------- | -------- | ------ | --- | --- |
| {Objective Category 1} | {Specific, measurable key result} | {%}      | {✅    | ⚠️  | ❌} |
| {Objective Category 2} | {Specific, measurable key result} | {%}      | {✅    | ⚠️  | ❌} |
| {Objective Category 3} | {Specific, measurable key result} | {%}      | {✅    | ⚠️  | ❌} |
| {Objective Category 4} | {Specific, measurable key result} | {%}      | {✅    | ⚠️  | ❌} |

{Note: OKRs should align with the agent's tier and role:

- C-suite/Executive: Strategic objectives (delivery, quality, team development, technical debt)
- Supervisor: Chapter/platform delivery, code quality, team mentoring, technical standards
- Teammate: Feature delivery, code quality, skill development, collaboration}

### Performance Metrics (Trailing 90 Days)

| Metric     | Target   | Actual   | Trend |
| ---------- | -------- | -------- | ----- | --- | --------- |
| {Metric 1} | {Target} | {Actual} | {↑    | →   | ↓} {Text} |
| {Metric 2} | {Target} | {Actual} | {↑    | →   | ↓} {Text} |
| {Metric 3} | {Target} | {Actual} | {↑    | →   | ↓} {Text} |

{Note: Metrics should be quantifiable and role-appropriate:

- Delivery metrics: Task completion rate, sprint velocity, milestone adherence
- Quality metrics: Defect rate, code review findings, test coverage
- Collaboration metrics: PR review turnaround, cross-team participation, mentoring sessions
- Leadership metrics: Team velocity variance, retention, promotion rate}

## Vetting Record

{Note: Include this section for teammates and supervisors who went through recruitment. Omit for C-suite (pre-placed), custom agents, and utility agents.}

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
- {Officer 1} ({Name}): {✅|❌} {Assessment text with specific rationale}
- {Officer 2} ({Name}): {✅|❌} {Assessment text with specific rationale}
- {Officer 3} ({Name}): {✅|❌} {Assessment text with specific rationale}

Summary: {Comprehensive summary explaining the scores, highlighting key strengths,
addressing any concerns, and providing final hiring rationale. Should reference
specific achievements, quantifiable outcomes, and how the candidate meets or
exceeds the vetting threshold.}
```

{Optional: Training Completion section if conditional pass required remediation}

### Training Completion

| Module                | Delivering Officer | Status  | Date         |
| --------------------- | ------------------ | ------- | ------------ |
| {Module Code}: {Name} | {Officer} ({Init}) | ✅ PASS | {Month D, Y} |

**All conditional training requirements satisfied. Duty commenced {Month D, Year}.**

## Invocation Instructions

To invoke this agent via Kiro's `invokeSubAgent` tool:

```typescript
invokeSubAgent({
  name: "{agent-name-from-frontmatter}",
  prompt: "Your specific task or question for this agent",
  explanation: "Why you're delegating this task to this agent",
  contextFiles: [
    // Optional: relevant files this agent needs
    "{path/to/relevant/file-1.md}",
    "{path/to/relevant/file-2.md}",
  ],
});
```

**Before invoking:** Ensure you've read the relevant skill files listed above to understand the agent's capabilities and output format.

{Note: This section helps other agents and users understand how to properly delegate work to this agent. Include typical context files that would be useful.}

## Related Agents

{Optional: List agents this agent frequently collaborates with or delegates to}

- **{Agent Name}** (`{agent-id}`) — {Relationship or collaboration pattern}
- **{Agent Name}** (`{agent-id}`) — {Relationship or collaboration pattern}

## Authority Scope

{Optional: For executive and director-level agents, explicitly define authority boundaries}

| Domain     | Authority Scope                                     |
| ---------- | --------------------------------------------------- |
| {Domain 1} | {What decisions this agent can make autonomously}   |
| {Domain 2} | {What requires consultation or approval}            |
| {Domain 3} | {What is explicitly outside this agent's authority} |

## Limitations

{Optional: For custom/utility agents, explicitly state what they cannot do}

This agent:

- Cannot {limitation 1}
- Cannot {limitation 2}
- Cannot {limitation 3}

## Integration Points

{Optional: For custom/utility agents, describe how they integrate with other systems}

### {System/Agent 1}

{Description of integration pattern}

### {System/Agent 2}

{Description of integration pattern}

---

**Source Profile:** `{path/to/original/profile.md}`  
**Agent Type:** {C-suite|VP|Supervisor|Senior IC|IC|Custom|Utility}  
**Imported:** {YYYY-MM-DD}  
**Import Phase:** {Phase number}  
**Last Updated:** {YYYY-MM-DD}

{Note: Footer provides traceability back to source documents and import metadata}
