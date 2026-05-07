# Hook Template Usage Guide

This guide explains how to create Kiro hooks using the `hook_template.json` template.

## What Are Hooks?

Hooks allow agent actions to automatically trigger based on IDE events. When an event occurs (file save, prompt submit, tool use, etc.), the hook executes a specified action (ask agent or run command).

## Hook Schema

All hooks must follow this JSON schema:

```json
{
  "name": "string (required)",
  "version": "string (required)",
  "description": "string (optional)",
  "when": {
    "type": "string (required)",
    "patterns": ["array (conditional)"],
    "toolTypes": ["array (conditional)"]
  },
  "then": {
    "type": "string (required)",
    "prompt": "string (conditional)",
    "command": "string (conditional)",
    "timeout": "number (optional)"
  }
}
```

## Field Definitions

### Top-Level Fields

| Field         | Type   | Required    | Description                             |
| ------------- | ------ | ----------- | --------------------------------------- |
| `name`        | string | ✅ Yes      | Display name for the hook (shown in UI) |
| `version`     | string | ✅ Yes      | Semantic version (e.g., "1.0.0")        |
| `description` | string | ⚠️ Optional | Brief description of what the hook does |

### `when` Object (Event Trigger)

| Field       | Type   | Required       | Description                                         |
| ----------- | ------ | -------------- | --------------------------------------------------- |
| `type`      | string | ✅ Yes         | Event type (see Event Types below)                  |
| `patterns`  | array  | ⚠️ Conditional | File patterns (required for file events)            |
| `toolTypes` | array  | ⚠️ Conditional | Tool categories or regex (required for tool events) |

### `then` Object (Action)

| Field     | Type   | Required       | Description                              |
| --------- | ------ | -------------- | ---------------------------------------- |
| `type`    | string | ✅ Yes         | Action type: "askAgent" or "runCommand"  |
| `prompt`  | string | ⚠️ Conditional | Prompt for agent (required for askAgent) |
| `command` | string | ⚠️ Conditional | Shell command (required for runCommand)  |
| `timeout` | number | ⚠️ Optional    | Timeout in seconds (default: 60)         |

## Event Types

### File Events

| Event Type    | Trigger                        | Requires `patterns` |
| ------------- | ------------------------------ | ------------------- |
| `fileEdited`  | When a user saves a code file  | ✅ Yes              |
| `fileCreated` | When a user creates a new file | ✅ Yes              |
| `fileDeleted` | When a user deletes a file     | ✅ Yes              |

**Pattern Examples:**

- `"*.md"` — All Markdown files
- `"*.ts"` — All TypeScript files
- `"*.tsx"` — All TSX files
- `"src/**/*.js"` — All JS files in src directory
- `"**/*.test.ts"` — All test files

### Agent Events

| Event Type     | Trigger                         | Requires `patterns` |
| -------------- | ------------------------------- | ------------------- |
| `promptSubmit` | When a message is sent to agent | ❌ No               |
| `agentStop`    | When agent execution completes  | ❌ No               |

### Tool Events

| Event Type    | Trigger                   | Requires `toolTypes` |
| ------------- | ------------------------- | -------------------- |
| `preToolUse`  | Before a tool is executed | ✅ Yes               |
| `postToolUse` | After a tool is executed  | ✅ Yes               |

**Tool Type Categories:**

- `"read"` — File reading tools
- `"write"` — File writing tools
- `"shell"` — Shell command execution
- `"web"` — Web search and fetch
- `"spec"` — Spec-related tools
- `"*"` — All tools

**Tool Type Regex:**

- `".*sql.*"` — Any tool with "sql" in the name
- `".*database.*"` — Any tool with "database" in the name
- `"git.*"` — Any tool starting with "git"

### Task Events

| Event Type          | Trigger                     | Requires `patterns` |
| ------------------- | --------------------------- | ------------------- |
| `preTaskExecution`  | Before a spec task starts   | ❌ No               |
| `postTaskExecution` | After a spec task completes | ❌ No               |

### Manual Events

| Event Type      | Trigger                          | Requires `patterns` |
| --------------- | -------------------------------- | ------------------- |
| `userTriggered` | When user manually triggers hook | ❌ No               |

## Action Types

### `askAgent` Action

Sends a message to the agent to remind it of something or request an action.

**Required Fields:**

- `type`: `"askAgent"`
- `prompt`: The message to send to the agent

**Example:**

```json
{
  "then": {
    "type": "askAgent",
    "prompt": "Review the changes for code quality and security issues"
  }
}
```

### `runCommand` Action

Executes a shell command.

**Required Fields:**

- `type`: `"runCommand"`
- `command`: The shell command to execute

**Optional Fields:**

- `timeout`: Timeout in seconds (default: 60)

**Example:**

```json
{
  "then": {
    "type": "runCommand",
    "command": "npm run lint",
    "timeout": 120
  }
}
```

## Complete Examples

### Example 1: Prettier on Save

```json
{
  "name": "Prettier Auto-Format",
  "version": "1.0.0",
  "description": "Auto-format Markdown files on save per AGENTS.md § 8.7",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.md"]
  },
  "then": {
    "type": "runCommand",
    "command": "prettier --write"
  }
}
```

### Example 2: Lint TypeScript on Save

```json
{
  "name": "Lint TypeScript",
  "version": "1.0.0",
  "description": "Run ESLint on TypeScript files when saved",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.ts", "*.tsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run lint",
    "timeout": 120
  }
}
```

### Example 3: Review Write Operations

```json
{
  "name": "Review Write Operations",
  "version": "1.0.0",
  "description": "Ask agent to verify write operations follow coding standards",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Verify this write operation follows our coding standards and doesn't introduce security issues"
  }
}
```

### Example 4: Git Commit Reminder

```json
{
  "name": "Git Commit Reminder",
  "version": "1.0.0",
  "description": "Remind agent to commit changes after task completion",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Task completed. Remember to commit the changes with a descriptive commit message following the workspace conventions."
  }
}
```

### Example 5: Test on Code Change

```json
{
  "name": "Run Tests on Code Change",
  "version": "1.0.0",
  "description": "Run test suite when source code is modified",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.ts", "src/**/*.tsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run test",
    "timeout": 300
  }
}
```

### Example 6: Pipeline Stage Gate Check

```json
{
  "name": "Pipeline Stage Gate",
  "version": "1.0.0",
  "description": "Verify stage gate requirements before advancing pipeline",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Before advancing to the next pipeline stage, verify all deliverables are complete and user approval has been obtained if required."
  }
}
```

### Example 7: Security Review for Database Tools

```json
{
  "name": "Database Operation Security Review",
  "version": "1.0.0",
  "description": "Review database operations for security before execution",
  "when": {
    "type": "preToolUse",
    "toolTypes": [".*sql.*", ".*database.*"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this database operation for SQL injection risks, proper parameterization, and authorization checks."
  }
}
```

### Example 8: Context Budget Check

```json
{
  "name": "Context Budget Monitor",
  "version": "1.0.0",
  "description": "Check context budget before starting new tasks",
  "when": {
    "type": "preTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check current context budget. If approaching limit, consider running context compression before starting this task."
  }
}
```

## Best Practices

### 1. Naming Conventions

- Use descriptive names that explain what the hook does
- Keep names concise (under 50 characters)
- Use title case for display names

**Good:**

- "Prettier Auto-Format"
- "Lint TypeScript on Save"
- "Review Write Operations"

**Bad:**

- "hook1"
- "my-hook"
- "test"

### 2. Description Guidelines

- Explain what the hook does and why
- Reference relevant documentation (e.g., "per AGENTS.md § 8.7")
- Keep descriptions under 100 characters

### 3. Pattern Specificity

- Be as specific as possible with file patterns
- Use `**` for recursive directory matching
- Avoid overly broad patterns like `*` alone

**Good:**

- `"src/**/*.ts"` — TypeScript files in src
- `"*.test.ts"` — Test files
- `"company/pipeline/**/*.md"` — Pipeline docs

**Bad:**

- `"*"` — Too broad
- `"*.js"` — Might match unwanted files

### 4. Command Safety

- Ensure commands are safe and non-destructive
- Set appropriate timeouts for long-running commands
- Test commands manually before adding to hooks

### 5. Prompt Clarity

- Write clear, actionable prompts for `askAgent`
- Specify what the agent should check or do
- Include context about why the check is needed

## Common Use Cases

### Code Quality

```json
{
  "name": "Code Quality Check",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.ts"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run lint && npm run test"
  }
}
```

### Security Review

```json
{
  "name": "Security Review",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review for security issues: input validation, authentication, authorization, data sanitization"
  }
}
```

### Pipeline Compliance

```json
{
  "name": "Pipeline Stage Compliance",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Verify task output meets pipeline stage requirements and quality standards"
  }
}
```

### Git Workflow

```json
{
  "name": "Git Worktree Check",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": [".*git.*"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "If this is multi-agent work, ensure git worktree isolation is being used per AGENTS.md § 8.5"
  }
}
```

## Troubleshooting

### Hook Not Triggering

**Check:**

1. Event type is correct
2. Patterns match the files being edited
3. Hook file is valid JSON
4. Hook is enabled in Kiro settings

### Command Failing

**Check:**

1. Command is valid for your shell (PowerShell on Windows)
2. Timeout is sufficient for command execution
3. Required tools are installed (npm, prettier, etc.)
4. Working directory is correct

### Agent Not Responding to Prompt

**Check:**

1. Prompt is clear and actionable
2. Agent has necessary context
3. Prompt doesn't conflict with other hooks

## File Naming

Hook files should be named descriptively using kebab-case:

**Good:**

- `prettier-on-save.json`
- `lint-typescript.json`
- `review-write-operations.json`
- `pipeline-stage-gate.json`

**Bad:**

- `hook1.json`
- `myHook.json`
- `test.json`

## Location

All hooks should be placed in:

```
.kiro/hooks/{hook-name}.json
```

## Validation

Before committing a hook, validate:

- [ ] JSON is valid (no syntax errors)
- [ ] All required fields are present
- [ ] Event type is valid
- [ ] Patterns/toolTypes are appropriate for event type
- [ ] Action type matches required fields (prompt for askAgent, command for runCommand)
- [ ] Command has been tested manually
- [ ] Timeout is appropriate for command
- [ ] Description is clear and concise

## Related Documentation

- **AGENTS.md** — § 8.5 Git and Version Control
- **Key Kiro Features** — Hooks section in system prompt
- **Hook Examples** — `.kiro/hooks/` directory

---

**Template Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance
