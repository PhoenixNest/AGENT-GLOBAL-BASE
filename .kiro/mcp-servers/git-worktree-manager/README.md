# Git Worktree Manager MCP Server

Git worktree management for multi-agent parallel work. Implements the git worktree isolation pattern from CC-00.

## Features

- **Worktree Creation**: Create isolated worktrees for parallel agent work
- **Worktree Removal**: Clean up worktrees after task completion
- **Worktree Listing**: View all active worktrees
- **Branch Merging**: Merge agent branches back to main
- **Status Monitoring**: Check worktree status and changes

## Installation

```bash
# Install with uv
uv pip install -e .

# Or install from package
uvx git-worktree-manager-server@latest
```

## Configuration

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "git-worktree-manager": {
      "command": "uvx",
      "args": ["git-worktree-manager-server@latest"],
      "env": {
        "WORKSPACE_ROOT": "c:\\Users\\ASUS\\Documents\\Code\\Local\\agent-global-base",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "create_worktree",
        "remove_worktree",
        "list_worktrees",
        "merge_branch"
      ]
    }
  }
}
```

## Tools

### `create_worktree`

Create isolated git worktree for agent.

**Parameters:**

- `agent_name` (string): Name of the agent (e.g., "backend", "frontend")
- `task` (string): Task description (e.g., "dark-mode-api")
- `base_branch` (string, optional): Base branch to branch from (default: "master")

**Returns:** JSON with worktree creation results

### `remove_worktree`

Remove agent's worktree.

**Parameters:**

- `agent_name` (string): Name of the agent
- `force` (bool, optional): Force removal even if worktree has uncommitted changes

**Returns:** JSON with removal results

### `list_worktrees`

List all git worktrees.

**Returns:** JSON with list of worktrees

### `merge_branch`

Merge agent's branch back to target branch.

**Parameters:**

- `agent_name` (string): Name of the agent
- `target_branch` (string, optional): Target branch to merge into (default: "master")
- `no_ff` (bool, optional): Use --no-ff flag for merge (default: True)

**Returns:** JSON with merge results

### `get_worktree_status`

Get status of agent's worktree.

**Parameters:**

- `agent_name` (string): Name of the agent

**Returns:** JSON with worktree status

## Git Worktree Isolation Pattern

This server implements the five-phase lifecycle from CC-00:

| Phase             | Action                                                                  |
| ----------------- | ----------------------------------------------------------------------- |
| **1 — Provision** | Orchestrator creates one worktree per agent                             |
| **2 — Execute**   | Each agent works exclusively in its worktree; commits on its own branch |
| **3 — Integrate** | Orchestrator or Integration Agent merges branches into master           |
| **4 — Resolve**   | Integration Agent handles any merge conflicts                           |
| **5 — Clean up**  | Remove worktrees and prune stale entries                                |

## Branch Naming Convention

Branches follow: `agent/<agent-name>/<task>`

Example: `agent/backend/dark-mode-api`

## Usage Examples

### Create Worktree for Agent

```typescript
// In Kiro IDE
"Create a worktree for backend agent to work on dark-mode-api";
// Tool: create_worktree(agent_name="backend", task="dark-mode-api")
```

### List All Worktrees

```typescript
// In Kiro IDE
"Show me all active worktrees";
// Tool: list_worktrees()
```

### Merge Agent's Work

```typescript
// In Kiro IDE
"Merge backend agent's work into master";
// Tool: merge_branch(agent_name="backend", target_branch="master")
```

### Remove Worktree

```typescript
// In Kiro IDE
"Remove the backend agent's worktree";
// Tool: remove_worktree(agent_name="backend")
```

## Development

```bash
# Install dependencies
uv pip install -e .

# Run server locally
python server.py

# Test tools
# (Use Kiro IDE to test tool invocations)
```

## Reference

Full specification: `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

## License

MIT
