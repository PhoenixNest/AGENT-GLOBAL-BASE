# Prompt Engineering

Research, patterns, and integration guides for maximizing LLM capability through prompt design.

## Structure

```txt
prompt-engineering/
├── README.md                 # This file — overview & navigation
├── fundamentals/
│   ├── research.md           # Core taxonomy: techniques, frameworks, pitfalls, evaluation
│   └── quick-reference.md    # Template library, anti-patterns, debugging checklist, decision tree
├── patterns/
│   └── advanced-patterns.md  # 12 advanced patterns (Socratic, Pre-Mortem, Devil's Advocate, etc.)
└── workspace/
    ├── agent-conversation.md # How prompt engineering operates during agent conversation
    ├── strategy.md           # Workspace-specific prompt engineering strategy & gap analysis
    └── integration-guide.md  # How to integrate PE into skills, hooks, rules, agents, and config
```

## Quick Navigation

| I want to...                                  | Read this                                                            |
| --------------------------------------------- | -------------------------------------------------------------------- |
| Learn prompt engineering fundamentals         | [`fundamentals/research.md`](fundamentals/research.md)               |
| Get a ready-to-use prompt template            | [`fundamentals/quick-reference.md`](fundamentals/quick-reference.md) |
| Use advanced prompting techniques             | [`patterns/advanced-patterns.md`](patterns/advanced-patterns.md)     |
| Understand how PE works in agent conversation | [`workspace/agent-conversation.md`](workspace/agent-conversation.md) |
| Plan PE optimization for this workspace       | [`workspace/strategy.md`](workspace/strategy.md)                     |
| Integrate PE into skills, hooks, rules        | [`workspace/integration-guide.md`](workspace/integration-guide.md)   |

## Document Status

| Document              | Version | Last Updated |
| --------------------- | ------- | ------------ |
| research.md           | 1.1     | 2026-04-24   |
| quick-reference.md    | 1.1     | 2026-04-24   |
| advanced-patterns.md  | 1.1     | 2026-04-24   |
| agent-conversation.md | 1.0     | 2026-04-24   |
| strategy.md           | 1.1     | 2026-04-24   |
| integration-guide.md  | 1.0     | 2026-04-24   |

---

## Related Modules

| Module                                                     | Relationship                                                                                                                                                                                              |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`context-engineering/`](../context-engineering/README.md) | Provides the container (context window slots) into which prompt engineering patterns are placed. Prompt engineering answers _how to write_ an instruction; context engineering answers _where to put it_. |
| [`harness-engineering/`](../harness-engineering/README.md) | Contains operational prompt templates wired to harness patterns (see `harness-engineering/patterns/prompt-templates.md`).                                                                                 |

---

_Claude Lab Research Team — 2026-04-24_
