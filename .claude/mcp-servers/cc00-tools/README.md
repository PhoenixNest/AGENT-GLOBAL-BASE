# CC-00 Tools MCP Server

CC-00 implementation helpers and ASE compliance tools for LLM systems.

## Features

- **ASE Compliance Validation**: Check systems against ASE compliance standard
- **Maturity Assessment**: Assess system maturity (Levels 0-5)
- **Context Budget Monitoring**: Track and manage context window usage
- **Handoff Analysis**: Recommend optimal handoff tier for agent transitions

## Installation

```bash
# Install with uv
uv pip install -e .

# Or install from package
uvx cc00-tools-server@latest
```

## Configuration

Registered for Claude Code in the project-root `.mcp.json`:

```json
{
  "mcpServers": {
    "cc00-tools": {
      "command": "python",
      "args": [
        "${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/cc00-tools/server.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Tools

### `validate_ase_compliance`

Validate ASE compliance for an LLM system.

**Parameters:**

- `system_name` (string): Name of the system to validate
- `layers` (array, optional): List of layers to check (default: all 5 layers)
  - Valid layers: `prompt-engineering`, `context-engineering`, `harness-engineering`, `retrieval-augmented-generation`, `multi-agent-engineering`

**Returns:** JSON with compliance report including gaps and verdict

### `assess_maturity`

Assess maturity level of an LLM system (Levels 0-5).

**Parameters:**

- `system_name` (string): Name of the system to assess

**Returns:** JSON with maturity assessment and recommendations

**Maturity Levels:**

- **Level 0 — Ad-Hoc**: No systematic approach
- **Level 1 — Repeatable**: Basic patterns established
- **Level 2 — Defined**: Documented processes
- **Level 3 — Managed**: Quantitative management
- **Level 4 — Optimizing**: Continuous improvement
- **Level 5 — Research-Grade**: Novel contributions

### `check_context_budget`

Check context budget and provide recommendations.

**Parameters:**

- `context_size` (int): Current context size in tokens
- `model` (string, optional): Model name (default: "claude-sonnet-4.5")
  - Valid models: `claude-sonnet-4.5`, `claude-opus-4`, `claude-haiku-4`, `gpt-4`, `gpt-4-32k`, `gpt-4-turbo`

**Returns:** JSON with budget analysis and recommendations

**Status Levels:**

- **healthy**: < 50% usage
- **warning**: 50-75% usage
- **critical**: 75-90% usage
- **overflow_risk**: > 90% usage

### `analyze_handoff`

Analyze agent-to-agent handoff and recommend tier.

**Parameters:**

- `from_agent` (string): Source agent name
- `to_agent` (string): Target agent name
- `context_size` (int): Size of context to hand off (tokens)

**Returns:** JSON with handoff analysis and recommended tier

**Handoff Tiers:**

- **Full**: Complete conversation history + all artifacts
- **Scoped**: Task-relevant subset + key decisions
- **Minimal**: Task specification + final output only

## Usage Examples

### Validate ASE Compliance

```typescript
// In Claude Code
"Check if my RAG system is ASE compliant";
// Tool: validate_ase_compliance(system_name="my-rag-system")
```

### Assess System Maturity

```typescript
// In Claude Code
"What maturity level is my agent system?";
// Tool: assess_maturity(system_name="my-agent-system")
```

### Check Context Budget

```typescript
// In Claude Code
"Check if my context budget is healthy - currently at 150000 tokens";
// Tool: check_context_budget(context_size=150000, model="claude-sonnet-4.5")
```

### Analyze Handoff

```typescript
// In Claude Code
"What handoff tier should I use from orchestrator to worker with 25000 tokens?";
// Tool: analyze_handoff(from_agent="orchestrator", to_agent="worker", context_size=25000)
```

## ASE Compliance Layers

This tool validates against the five ASE layers:

1. **Prompt Engineering**: Instruction patterns and constraints
2. **Context Engineering**: Context window management and handoffs
3. **Harness Engineering**: Error boundaries and safety controls
4. **RAG**: Retrieval pipelines and knowledge management
5. **Multi-Agent**: Swarm orchestration and coordination

## Development

```bash
# Install dependencies
uv pip install -e .

# Run server locally
python server.py

# Test tools
# (Use Claude Code to test tool invocations)
```

## References

- ASE Compliance Standard: `core-component-00/agent-systems-engineering/governance/compliance-standard.md`
- Maturity Model: `core-component-00/agent-systems-engineering/governance/maturity-model.md`
- Context Handoff Protocol: `core-component-00/context-engineering/patterns/multi-agent-handoff.md`
- ADR-ASE-001: `core-component-00/agent-systems-engineering/governance/adr-ase-001.md`

## License

MIT
