---
inclusion: { auto|fileMatch|manual }
fileMatchPattern: { pattern }
description: { One-line description of what this steering file provides }
version: "1.0.0"
---

# {Steering File Title}

{Provide a brief introduction explaining what this steering file covers and when it should be used.}

**Example:**
This steering file provides core workspace conventions that apply to all work in the `agent-global-base` workspace. These rules are extracted from AGENTS.md and are mandatory for all AI executor agents.

---

## Inclusion Behavior

**Inclusion Type:** `{auto|fileMatch|manual}`

{Explain when this steering file is activated}

**Auto Inclusion:**

- This file is automatically included in all Kiro sessions
- Always active regardless of context

**File Match Inclusion:**

- Activates when files matching `{pattern}` are read into context
- Pattern: `{fileMatchPattern}`
- Example: `README*`, `*.pipeline.md`, `company/pipeline/**`

**Manual Inclusion:**

- Only activated when explicitly requested via context key (`#`)
- User must manually include this steering file

---

## Purpose and Scope

### What This Steering File Covers

{List the major topics or areas covered}

- {Topic 1}
- {Topic 2}
- {Topic 3}
- {Topic n}

### What This Steering File Does NOT Cover

{List what's explicitly out of scope}

- {Out of scope 1}
- {Out of scope 2}

### When to Use This Guidance

{Explain scenarios where this steering file is relevant}

**Use this when:**

- {Scenario 1}
- {Scenario 2}
- {Scenario 3}

**Do NOT use this when:**

- {Anti-pattern 1}
- {Anti-pattern 2}

---

## Core Principles

{Document the fundamental principles or rules}

### Principle 1: {Principle Name}

{Detailed explanation of the principle}

**Rationale:**
{Why this principle exists}

**Application:**
{How to apply this principle in practice}

**Examples:**

**Good:**

```
{Example of correct application}
```

**Bad:**

```
{Example of incorrect application}
```

### Principle 2: {Principle Name}

{Continue for all core principles}

---

## Rules and Conventions

{Document specific rules that must be followed}

### {Rule Category 1}

{Introduction to this category of rules}

| Rule         | Applies To | Detail                 |
| ------------ | ---------- | ---------------------- |
| **{Rule 1}** | {Scope}    | {Detailed explanation} |
| **{Rule 2}** | {Scope}    | {Detailed explanation} |
| **{Rule 3}** | {Scope}    | {Detailed explanation} |

### {Rule Category 2}

{Continue for all rule categories}

---

## Workflows and Processes

{Document standard workflows or processes}

### {Workflow 1 Name}

{Description of when to use this workflow}

**Steps:**

1. **{Step 1}** — {Description}
   - {Detail 1}
   - {Detail 2}

2. **{Step 2}** — {Description}
   - {Detail 1}
   - {Detail 2}

3. **{Step 3}** — {Description}
   - {Detail 1}
   - {Detail 2}

**Example:**

```typescript
// Example implementation
{
  code;
}
```

### {Workflow 2 Name}

{Continue for all workflows}

---

## Standards and Formats

{Document formatting standards, naming conventions, or structural requirements}

### {Standard Category 1}

{Description}

| Item Type | Convention   | Example   |
| --------- | ------------ | --------- |
| {Item 1}  | {Convention} | {Example} |
| {Item 2}  | {Convention} | {Example} |
| {Item 3}  | {Convention} | {Example} |

### {Standard Category 2}

{Continue for all standard categories}

---

## Decision Trees

{If applicable, provide decision trees for complex choices}

### When to {Decision Point}

```
Question: {Decision question}
├─ If {Condition A}
│  └─ Action: {What to do}
│     └─ Rationale: {Why}
├─ If {Condition B}
│  └─ Action: {What to do}
│     └─ Rationale: {Why}
└─ If {Condition C}
   └─ Action: {What to do}
      └─ Rationale: {Why}
```

---

## Templates and Examples

{Provide templates or examples for common artifacts}

### {Template 1 Name}

**Purpose:** {What this template is for}

**Format:**

```markdown
{template-content}
```

**Required Sections:**

- {Section 1} — {Purpose}
- {Section 2} — {Purpose}
- {Section 3} — {Purpose}

### {Template 2 Name}

{Continue for all templates}

---

## Common Patterns

{Document common patterns or idioms}

### Pattern 1: {Pattern Name}

**Context:** {When to use this pattern}

**Implementation:**

```typescript
{
  code - example;
}
```

**Benefits:**

- {Benefit 1}
- {Benefit 2}

**Drawbacks:**

- {Drawback 1}
- {Drawback 2}

### Pattern 2: {Pattern Name}

{Continue for all patterns}

---

## Anti-Patterns

{Document what NOT to do}

### Anti-Pattern 1: {Anti-Pattern Name}

**Description:** {What this anti-pattern looks like}

**Why It's Wrong:**
{Explanation of the problems}

**Example:**

```typescript
// BAD: Don't do this
{
  bad - example;
}
```

**Correct Approach:**

```typescript
// GOOD: Do this instead
{
  good - example;
}
```

### Anti-Pattern 2: {Anti-Pattern Name}

{Continue for all anti-patterns}

---

## Integration Points

{Document how this guidance integrates with other systems}

### Integration with {System 1}

{Explanation of integration}

**Key Touchpoints:**

- {Touchpoint 1}
- {Touchpoint 2}

### Integration with {System 2}

{Continue for all integrations}

---

## Authority and Hierarchy

{If applicable, document authority structures or hierarchies}

### {Hierarchy Name}

```
{Visual representation of hierarchy}
```

**Key Principles:**

1. **{Principle 1}** — {Explanation}
2. **{Principle 2}** — {Explanation}
3. **{Principle 3}** — {Explanation}

---

## Escalation Paths

{Document when and how to escalate issues}

### When to Escalate

{Criteria for escalation}

| Situation     | Escalate To | Timeframe |
| ------------- | ----------- | --------- |
| {Situation 1} | {Who}       | {When}    |
| {Situation 2} | {Who}       | {When}    |
| {Situation 3} | {Who}       | {When}    |

### Escalation Process

1. {Step 1}
2. {Step 2}
3. {Step 3}

---

## Quality Gates

{If applicable, document quality gates or checkpoints}

### {Gate 1 Name}

**Trigger:** {When this gate is evaluated}

**Criteria:**

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

**Pass Condition:** {What constitutes passing}

**Fail Condition:** {What constitutes failing}

**Remediation:** {What to do if failed}

### {Gate 2 Name}

{Continue for all gates}

---

## Monitoring and Metrics

{If applicable, document monitoring or metrics}

### Key Metrics

| Metric     | Target   | Measurement Method |
| ---------- | -------- | ------------------ |
| {Metric 1} | {Target} | {How to measure}   |
| {Metric 2} | {Target} | {How to measure}   |
| {Metric 3} | {Target} | {How to measure}   |

### Tracking Requirements

{Document any tracking requirements}

**Required Files:**

- `{file-1}` — {Purpose}
- `{file-2}` — {Purpose}

**Update Frequency:** {How often to update}

---

## Troubleshooting

{Provide troubleshooting guidance}

### Issue: {Problem Description}

**Symptoms:**

- {Symptom 1}
- {Symptom 2}

**Root Cause:**
{Explanation}

**Solution:**
{Step-by-step resolution}

### Issue: {Another Problem}

{Continue for common issues}

---

## Best Practices

{List best practices for following this guidance}

1. **{Best Practice 1}** — {Explanation and rationale}
2. **{Best Practice 2}** — {Explanation and rationale}
3. **{Best Practice 3}** — {Explanation and rationale}
4. **{Best Practice n}** — {Explanation and rationale}

---

## Common Mistakes

{Document common mistakes and how to avoid them}

| Mistake     | Impact            | Prevention     |
| ----------- | ----------------- | -------------- |
| {Mistake 1} | {What goes wrong} | {How to avoid} |
| {Mistake 2} | {What goes wrong} | {How to avoid} |
| {Mistake 3} | {What goes wrong} | {How to avoid} |

---

## Quick Reference

{Provide a quick reference section for common lookups}

### {Reference Category 1}

{Quick lookup information}

### {Reference Category 2}

{Quick lookup information}

---

## Checklists

{Provide checklists for common tasks}

### {Checklist 1 Name}

Use this checklist when {scenario}:

- [ ] {Item 1}
- [ ] {Item 2}
- [ ] {Item 3}
- [ ] {Item n}

### {Checklist 2 Name}

{Continue for all checklists}

---

## Related Steering Files

{List related steering files that provide complementary guidance}

- **{Steering File 1}** — `.kiro/steering/{file-1}.md` — {Relationship}
- **{Steering File 2}** — `.kiro/steering/{file-2}.md` — {Relationship}
- **{Steering File 3}** — `.kiro/steering/{file-3}.md` — {Relationship}

---

## References

### Internal Documentation

- **AGENTS.md** — {Relevant section references}
- **{Doc 1}** — `{path}` — {Description}
- **{Doc 2}** — `{path}` — {Description}

### External Resources

{Optional: Links to external standards or documentation}

- **{Resource 1}** — {URL} — {Description}
- **{Resource 2}** — {URL} — {Description}

---

## Maintenance

**Version:** 1.0.0  
**Last Updated:** {YYYY-MM-DD}  
**Maintained By:** {Responsible team or agent}  
**Review Frequency:** {How often this should be reviewed}

### Version History

| Version | Date         | Changes         |
| ------- | ------------ | --------------- |
| 1.0.0   | {YYYY-MM-DD} | Initial version |

### Planned Updates

{Optional: Planned improvements}

- {Update 1}
- {Update 2}

---

_This steering file is {automatically included|conditionally activated|manually activated} and provides {brief summary of purpose}._
