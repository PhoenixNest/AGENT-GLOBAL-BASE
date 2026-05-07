# {Power Name} Power

**Version:** 1.0.0  
**Status:** {Active|Under Development|Deprecated}  
**Authority:** {Reference to AGENTS.md or other governing document}

---

## Overview

The **{Power Name} Power** provides comprehensive support for {high-level description of what this power enables}.

This Power packages:

- **{Component 1}**: {Brief description}
- **{Component 2}**: {Brief description}
- **{Component 3}**: {Brief description}
- **{Component 4}**: {Brief description}

---

## What This Power Provides

### 1. {Major Capability 1}

{Detailed description of the first major capability this power provides}

**Key Features:**

- {Feature 1}
- {Feature 2}
- {Feature 3}

**Access Pattern:**

```
{path/to/resources}
```

### 2. {Major Capability 2}

{Detailed description of the second major capability}

**Components:**

| Component     | Location | Purpose   |
| ------------- | -------- | --------- |
| {Component 1} | `{path}` | {Purpose} |
| {Component 2} | `{path}` | {Purpose} |
| {Component 3} | `{path}` | {Purpose} |

### 3. {Major Capability 3}

{Continue for all major capabilities}

### 4. {Documentation/Templates/Resources}

{If this power includes templates, documentation, or other resources, list them here}

**Available Templates:**

- **{Template 1}** — `{path}` — {Purpose}
- **{Template 2}** — `{path}` — {Purpose}
- **{Template 3}** — `{path}` — {Purpose}

**Documentation:**

- **{Doc 1}** — `{path}` — {Description}
- **{Doc 2}** — `{path}` — {Description}

### 5. {Steering Files/Auto-Activation}

{If this power includes steering files that auto-activate, document them}

Conditional steering files auto-activate when working in relevant directories:

- `{steering-file-1}.md` — {When it activates and what it provides}
- `{steering-file-2}.md` — {When it activates and what it provides}
- `{steering-file-3}.md` — {When it activates and what it provides}

---

## How to Use This Power

### Activate the Power

```typescript
kiroPowers({
  action: "activate",
  powerName: "{power-name}",
});
```

**What happens when you activate:**

1. {Step 1 of activation}
2. {Step 2 of activation}
3. {Step 3 of activation}

### Basic Usage Pattern

{Provide a step-by-step guide for basic usage}

**Step 1: {Action}**

{Description and example}

```typescript
// Example code or command
```

**Step 2: {Action}**

{Description and example}

**Step 3: {Action}**

{Description and example}

### Advanced Usage

{Document advanced usage patterns or features}

#### {Advanced Feature 1}

{Description and example}

#### {Advanced Feature 2}

{Description and example}

---

## Key Concepts

### {Concept 1}

{Detailed explanation of a key concept users need to understand}

**Important Rules:**

| Rule         | Applies To | Detail        |
| ------------ | ---------- | ------------- |
| **{Rule 1}** | {Scope}    | {Explanation} |
| **{Rule 2}** | {Scope}    | {Explanation} |
| **{Rule 3}** | {Scope}    | {Explanation} |

### {Concept 2}

{Continue for all key concepts}

---

## Governance and Rules

{Document any governance rules, constraints, or requirements}

### Mandatory Rules

{List non-negotiable rules that must be followed}

1. **{Rule 1}** — {Explanation and rationale}
2. **{Rule 2}** — {Explanation and rationale}
3. **{Rule 3}** — {Explanation and rationale}

### Best Practices

{List recommended practices}

1. **{Practice 1}** — {Explanation}
2. **{Practice 2}** — {Explanation}
3. **{Practice 3}** — {Explanation}

### Common Violations

{Document common mistakes and how to avoid them}

| Violation     | Impact            | Prevention     |
| ------------- | ----------------- | -------------- |
| {Violation 1} | {What goes wrong} | {How to avoid} |
| {Violation 2} | {What goes wrong} | {How to avoid} |

---

## Integration with Other Powers

{Explain how this power relates to other powers}

### Related Powers

- **{Power 1}** — {Relationship and when to use together}
- **{Power 2}** — {Relationship and when to use together}
- **{Power 3}** — {Relationship and when to use together}

### Power Dependencies

{If this power depends on or requires other powers}

**Required:**

- {Power name} — {Why it's required}

**Optional:**

- {Power name} — {When it's useful}

---

## Quick Start Examples

### Example 1: {Common Use Case 1}

**Scenario:** {Describe the scenario}

**Steps:**

```typescript
// 1. Activate the power
kiroPowers({ action: "activate", powerName: "{power-name}" });

// 2. {Action}
{code or command}

// 3. {Action}
{code or command}

// 4. {Action}
{code or command}
```

**Expected Result:**
{What should happen}

### Example 2: {Common Use Case 2}

**Scenario:** {Describe the scenario}

**Steps:**

```typescript
// Implementation
```

**Expected Result:**
{What should happen}

### Example 3: {Advanced Use Case}

**Scenario:** {Describe a more complex scenario}

**Steps:**

```typescript
// Implementation
```

**Expected Result:**
{What should happen}

---

## Reference Guide

### {Reference Section 1}

{Provide detailed reference information}

#### {Subsection}

{Details}

### {Reference Section 2}

{Continue for all reference sections}

---

## Templates Overview

{If this power provides templates, document them in detail}

### {Template 1 Name}

**Location:** `{path/to/template}`

**Purpose:** {What this template is for}

**Sections:**

1. {Section 1} — {Purpose}
2. {Section 2} — {Purpose}
3. {Section 3} — {Purpose}

**Usage:**

```bash
# Copy template
cp {path/to/template} {destination}

# Fill in sections
# ...
```

### {Template 2 Name}

{Continue for all templates}

---

## Monitoring and Tracking

{If this power involves progress tracking or monitoring}

### Required Files

{List any files that must be maintained}

| File       | Purpose   | Location   | Required When |
| ---------- | --------- | ---------- | ------------- |
| `{file-1}` | {Purpose} | {Location} | {Condition}   |
| `{file-2}` | {Purpose} | {Location} | {Condition}   |

### Progress Tracking Format

{Provide format or template for progress tracking}

```markdown
# {Tracking Document Title}

{Template content}
```

---

## Troubleshooting

{Provide solutions to common issues}

### Issue: {Problem Description}

**Symptoms:**

- {Symptom 1}
- {Symptom 2}

**Solution:**

{Step-by-step resolution}

```typescript
// Example solution code
```

### Issue: {Another Problem}

{Continue for common issues}

---

## Advanced Topics

{Document advanced features or edge cases}

### {Advanced Topic 1}

{Detailed explanation}

### {Advanced Topic 2}

{Detailed explanation}

---

## API Reference

{If this power provides programmatic APIs or tools}

### {Function/Tool 1}

**Signature:**

```typescript
{function-signature}
```

**Parameters:**

| Parameter | Type   | Required    | Description   |
| --------- | ------ | ----------- | ------------- |
| {param1}  | {type} | ✅ Yes      | {Description} |
| {param2}  | {type} | ⚠️ Optional | {Description} |

**Returns:**

{Return value description}

**Example:**

```typescript
{
  example - usage;
}
```

### {Function/Tool 2}

{Continue for all APIs}

---

## Configuration

{If this power requires configuration}

### Configuration File

**Location:** `{path/to/config}`

**Format:**

```json
{
  "setting1": "value",
  "setting2": "value"
}
```

**Settings:**

| Setting    | Type   | Default   | Description   |
| ---------- | ------ | --------- | ------------- |
| {setting1} | {type} | {default} | {Description} |
| {setting2} | {type} | {default} | {Description} |

---

## Performance and Optimization

{If relevant, document performance considerations}

### Performance Tips

1. **{Tip 1}** — {Explanation}
2. **{Tip 2}** — {Explanation}
3. **{Tip 3}** — {Explanation}

### Resource Requirements

{Document any resource requirements or constraints}

| Resource     | Requirement   | Notes   |
| ------------ | ------------- | ------- |
| {Resource 1} | {Requirement} | {Notes} |
| {Resource 2} | {Requirement} | {Notes} |

---

## Security Considerations

{If this power has security implications}

### Security Best Practices

1. **{Practice 1}** — {Explanation}
2. **{Practice 2}** — {Explanation}

### Security Risks

{Document potential security risks and mitigations}

| Risk     | Severity | Mitigation        |
| -------- | -------- | ----------------- |
| {Risk 1} | {Level}  | {How to mitigate} |
| {Risk 2} | {Level}  | {How to mitigate} |

---

## References

### Internal Documentation

- **{Doc 1}** — `{path}` — {Description}
- **{Doc 2}** — `{path}` — {Description}
- **AGENTS.md** — {Relevant section references}

### External Resources

{Optional: Links to external documentation}

- **{Resource 1}** — {URL} — {Description}
- **{Resource 2}** — {URL} — {Description}

### Related Powers

- **{Power 1}** — `.kiro/powers/{power-1}/POWER.md`
- **{Power 2}** — `.kiro/powers/{power-2}/POWER.md`

---

## Changelog

### Version History

| Version | Date         | Changes         |
| ------- | ------------ | --------------- |
| 1.0.0   | {YYYY-MM-DD} | Initial release |

### Planned Enhancements

{Optional: Future improvements}

- {Enhancement 1}
- {Enhancement 2}

---

## Support and Maintenance

**Power Maintained By:** {Responsible team or agents}  
**Last Updated:** {YYYY-MM-DD}  
**Status:** {Active|Under Development|Deprecated}  
**Support Contact:** {How to get help}

---

_This power follows the Kiro Powers specification and is maintained according to ECOSYSTEM_SPEC.md governance._
