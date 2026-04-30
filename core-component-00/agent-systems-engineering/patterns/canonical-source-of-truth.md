# Pattern: Canonical Source of Truth (CSOT)

| Field        | Value                            |
| ------------ | -------------------------------- |
| **Category** | Governance · Identity Management |
| **Layer**    | Cross-cutting (Layers 1 + 2)     |
| **Status**   | Ratified — ADR-ASE-001           |

---

## Problem

In a multi-agent system — especially one where the same agent persona operates across
multiple AI platforms (Claude, Cursor, Gemini CLI, etc.) — agent identity is defined
independently in each platform's configuration file. Over time these definitions drift:
a constraint added in one platform is forgotten in another; a role boundary is clarified
in one file but remains vague in the rest.

**Identity drift** produces agents that behave inconsistently depending on which platform
invokes them, making the system unpredictable and impossible to reason about as a whole.

---

## Solution

Define a single **Canonical Source of Truth** document that holds the authoritative
specification for every agent's identity. All platform-specific configurations are
**adapters** — they translate the canonical definition into the format each platform
requires, but they never contradict or extend it independently.

```
canonical/
└── AGENTS.md           ← Authoritative agent definitions — single source of truth
    adapters/
    ├── claude.md       ← Platform-specific translation (Claude Code / API)
    ├── cursor.md       ← Platform-specific translation (Cursor IDE)
    └── gemini.md       ← Platform-specific translation (Gemini CLI)
```

**Rule:** If an adapter definition conflicts with the canonical source, the canonical
source wins and the adapter is corrected — not the other way around.

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
`AGENTS.md`. Platform-specific configuration files (e.g., `.cursor/rules/`, skill
files, system prompts) are adapters.

**Authority hierarchy for resolving conflicts:**
`AGENTS.md` > `pipeline.md` > `agent/profile.md` > `library/overview/*.md` > `library/departments/*.md`

---

## How to Apply

1. **Write the canonical definition first.** Before configuring any platform, write the
   agent's role, constraints, escalation criteria, and output format in `AGENTS.md`.

2. **Create platform adapters by translation.** For each platform that will invoke this
   agent, create a platform-specific file that translates the canonical definition into
   the platform's required format. Add nothing new.

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

- `core-component-00/prompt-engineering/` — Patterns for writing canonical agent identities
- `core-component-00/context-engineering/patterns/multi-agent-handoff.md` — How canonical
  context slot definitions are communicated between agents
