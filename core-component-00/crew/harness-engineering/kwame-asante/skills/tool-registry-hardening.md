---
name: cc00-tool-registry-hardening
description: Tool whitelist, call-limit, and dangerous-task detection implementation for tool_registry.py. Owned by Kwame Asante (Senior Research Engineer, Harness Engineering). Trigger: tool registry, tool whitelist, dangerous task detection, call limits.
version: "1.0.0"
---

# Tool Registry Hardening

**Skill ID:** tool-registry-hardening
**Role:** Senior Research Engineer — Harness Engineering
**Seniority:** L3 — Senior

## Overview

Production implementation of `core-component-00/engineering/harness-engineering/implementations/tool_registry.py`
— tool whitelisting, per-session call limits, and dangerous-task pattern detection for
agent-invoked tool calls.

## Tools & Frameworks

| Tool                    | Proficiency | Use Case                                          |
| ----------------------- | ----------- | ------------------------------------------------- |
| Python                  | Expert      | Registry and detection-rule implementation        |
| Rule-based classifiers  | Advanced    | Dangerous-task pattern matching                   |
| pytest + red-team cases | Expert      | Adversarial coverage of whitelist bypass attempts |

## Module Ownership

- Maintains `tool_registry.py`: per-agent tool whitelists, session-scoped call-limit enforcement,
  and the dangerous-task detection ruleset (destructive commands, credential access, irreversible
  operations)
- Owns the red-team test suite that continuously attempts to construct tool-call sequences that
  bypass whitelist or call-limit enforcement
- Escalates any confirmed bypass to Dr. Vance immediately — a tool-registry bypass is treated as an
  R0-equivalent defect regardless of exploitability in the current deployment

## Scenarios & Trade-offs

### Scenario 1: Whitelist Too Restrictive for Legitimate Multi-Step Task

- **Approach:** Whitelists are scoped per-agent-role, not global; a role needing a wider tool set
  gets an explicit, reviewed whitelist rather than a blanket allow
- **Trade-off:** Per-role whitelists add configuration overhead vs. one global list, but prevent
  privilege creep across unrelated agent roles
- **Quality Bar:** No agent role has an undocumented tool grant; every whitelist entry traces to a
  documented need

### Scenario 2: Dangerous-Task Pattern False Positives

- **Approach:** Detection rules flag for confirmation rather than silently blocking, except for a
  small hard-blocked set (credential exfiltration, irreversible destructive commands without
  confirmation)
- **Trade-off:** Flag-for-confirmation preserves legitimate workflows but requires a human-in-the-
  loop path to exist and be tested
- **Quality Bar:** False-positive rate on the red-team + legitimate-task corpus tracked and reported
  quarterly

## Quality Standards

- Every whitelist change is reviewed against the red-team suite before merge
- Call-limit enforcement is tested under concurrent/rapid-fire call patterns, not just sequential
- Dangerous-task detection rules are versioned and changes are logged with rationale

## References

- `core-component-00/engineering/harness-engineering/implementations/tool_registry.py`
- Harness Engineering: Production Patterns for Reliable LLM Execution (Dr. Vance, framework spec, 2025)
