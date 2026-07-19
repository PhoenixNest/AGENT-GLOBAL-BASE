# Pattern: Canonical Source of Truth (CSOT)

| Field        | Value                            |
| ------------ | -------------------------------- |
| **Category** | Governance · Identity Management |
| **Layer**    | Cross-cutting (Layers 1 + 2)     |
| **Status**   | Ratified — ADR-ASE-001           |

---

## Problem

In a multi-agent system, agent identity is often defined across many files — platform
configuration, pipeline definitions, profile documents, and skill files. Over time these
definitions drift: a constraint added in one file is forgotten in another; a role boundary
is clarified in one document but remains vague elsewhere.

**Identity drift** produces agents that behave inconsistently across invocations, making
the system unpredictable and impossible to reason about as a whole.

---

## Solution

Define a single **Canonical Source of Truth** document that holds the authoritative
specification for every agent's identity. All platform-specific configurations are
**adapters** — they translate the canonical definition into the format each platform
requires, but they never contradict or extend it independently.

```
AGENTS.md                          ← Canonical source of truth (workspace root)
company/
├── departments/**/agent/profile.md ← Per-agent canonical identity documents
└── pipeline/*/pipeline.md          ← Pipeline stage authority definitions
```

**Rule:** If any document conflicts with a higher-authority canonical source, the
lower-authority document is corrected — never the other way around.

---

## Structure

A canonical agent definition contains:

| Element                     | Description                                                                       |
| --------------------------- | --------------------------------------------------------------------------------- |
| **Role**                    | The agent's expertise boundary — what it does and does not own                    |
| **Behavioural constraints** | Explicit list of permitted and forbidden behaviours                               |
| **Communication protocol**  | How the agent communicates with other agents (output format, severity vocabulary) |
| **Escalation criteria**     | Conditions under which the agent escalates to a human or supervisor               |
| **Output format**           | Schema or format specification for machine-parseable outputs                      |
| **Authority scope**         | Which pipeline stages, artefacts, or decisions this agent owns                    |

Platform adapters translate this definition without adding or removing constraints.

---

## In This Workspace

The canonical source of truth for this organisation is:

> `AGENTS.md` — root of the workspace

Every agent activated in any pipeline must be consistent with the definitions in
`AGENTS.md`. Tool configuration files, skill files, and system prompts are adapters —
they translate the canonical definition into the format each context requires.

**Authority hierarchy for resolving conflicts:**
`AGENTS.md` > `pipeline.md` > `agent/profile.md` > `library/overview/*.md` > `library/departments/*.md`

---

## How to Apply

1. **Write the canonical definition first.** Before configuring any platform, write the
   agent's role, constraints, escalation criteria, and output format in `AGENTS.md`.

2. **Create adapters by translation.** For each context that will invoke this agent
   (tool configuration, pipeline stage, skill file), ensure it translates the canonical
   definition without adding or removing constraints.

3. **Audit adapters against the canonical source.** When the canonical definition changes,
   review all adapters and update them. A changed constraint in `AGENTS.md` that is not
   reflected in an adapter is a compliance gap.

4. **Resolve conflicts in favour of the canonical source.** If an adapter and the
   canonical source disagree, correct the adapter. Never correct the canonical source
   to match an adapter without going through the authority chain.

---

## Consequences

**Benefits:**

- Agent behaviour is predictable regardless of which platform invokes it
- Changes to agent identity are made in one place and propagate to all platforms
- Auditing agent compliance is straightforward — check one document

**Trade-offs:**

- Requires discipline to maintain adapter consistency after canonical updates
- Adds overhead when a platform requires a feature that the canonical source doesn't
  address — requires a canonical update first, then adapter update

---

## Related Patterns

- [`anti-pattern-firewall.md`](./anti-pattern-firewall.md) — Canonical enumeration of
  forbidden agent behaviours
- [`defect-severity-vocabulary.md`](./defect-severity-vocabulary.md) — Shared
  classification system referenced in canonical definitions
- [`paired-artifacts.md`](./paired-artifacts.md) — Ensures related canonical documents
  travel together

## CC-00 References

- `core-component-00/engineering/prompt-engineering/` — Patterns for writing canonical agent identities
- `core-component-00/engineering/context-engineering/patterns/multi-agent-handoff.md` — How canonical
  context slot definitions are communicated between agents
