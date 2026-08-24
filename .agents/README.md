# .agents — Antigravity Workspace Customization Layer

This directory contains workspace-level customizations for **Google Antigravity (AGY)**, enabling full compatibility with the **`AGENT-GLOBAL-BASE`** multi-system architecture.

---

## Directory Layout

```text
.agents/
├── skills.json                   ← Declares external skill paths (.claude/skills)
├── hooks.json                    ← Antigravity lifecycle hooks configuration
├── mcp_config.json               ← MCP servers configuration (workspace-knowledge, agent-memory)
├── hooks/
│   └── antigravity_hook_adapter.py ← JSON protocol adapter for lifecycle hooks
├── rules/                        ← Symlinks to project markdown rules (.claude/rules/*.md)
└── agents/                       ← Functional subagent definition files
```

---

## Features & Integration

1. **Progressive Skill Loading**: Configured via `skills.json` to load all 21 domain skill routers without duplicating markdown files.
2. **Hierarchical Rules**: Root `AGENTS.md` and 28 directory-level `AGENTS.md` symlinks ensure folder-scoped rules are automatically loaded by Antigravity.
3. **MCP Connectivity**: Configures `workspace-knowledge` and `agent-memory` servers with portable commands.
4. **Lifecycle Hooks**: Adapts `PreInvocation`, `PreToolUse`, and `PostToolUse` events to enforce ASGF prompt quality, git safety, and rate-limiting gates.
5. **Subagents**: Defines `organizational-agent-activator`, `pipeline-stage-executor`, `cc00-implementation-assistant`, and `multi-agent-orchestrator`.
